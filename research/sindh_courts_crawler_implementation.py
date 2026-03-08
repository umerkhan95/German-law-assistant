"""
Sindh High Court & District Courts Legal Crawler
Tier 1: cases.districtcourtssindh.gos.pk
Purpose: Extract case metadata for legal AI training

Author: Legal AI Team
Date: March 8, 2026
"""

import asyncio
import json
import logging
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, quote

import aiohttp
from crawl4ai import AsyncWebCrawler, CrawlResult
import asyncpg
from bs4 import BeautifulSoup
import dateutil.parser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sindh_crawler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_URL = "https://cases.districtcourtssindh.gos.pk"
SEARCH_ENDPOINT = f"{BASE_URL}/case-search"

# All districts from verification report
DISTRICTS = [
    # Karachi subdivisions
    "Karachi (South)",
    "Karachi (West)",
    "Karachi (East)",
    "Karachi (Central)",
    "Karachi (Malir)",
    # Other Sindh districts
    "Hyderabad",
    "Thatta",
    "Badin",
    "Dadu",
    "Jamshoro @ Kotri",
    "Tharparkar @ Mithi",
    "Mirpurkhas",
    "Umerkot",
    "Sanghar",
    "Naushahro Feroze",
    "Shaheed Benazirabad",
    "Sukkur",
    "Khairpur",
    "Ghotki",
    "Larkana",
    "KAMBER-SHAHDADKOT @ KAMBER",
    "Shikarpur",
    "Jacobabad",
    "Kashmore @ Kandhkot",
    "Tando Allahyar",
    "Tando Muhammad Khan",
    "Matiari",
    "Sujawal",
]

CASE_STATUS_OPTIONS = ["Pending", "Disposal", "All"]
CRAWL_DELAY = 2  # seconds between requests
RATE_LIMIT_PER_MINUTE = 30
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # exponential backoff multiplier

# ============================================================================
# DATABASE SETUP
# ============================================================================

class DatabaseManager:
    """Manage PostgreSQL connections and operations"""

    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool = None

    async def connect(self):
        """Initialize connection pool"""
        self.pool = await asyncpg.create_pool(
            self.db_url,
            min_size=5,
            max_size=20,
            command_timeout=60,
        )
        await self._create_tables()
        logger.info("Database connected")

    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database disconnected")

    async def _create_tables(self):
        """Create necessary tables if not exist"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS cases (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    case_id_hash TEXT UNIQUE NOT NULL,
                    case_number TEXT NOT NULL,
                    case_type TEXT,
                    year_filed INTEGER,
                    district TEXT NOT NULL,
                    court_name TEXT NOT NULL,
                    bench_location TEXT,
                    plaintiff TEXT,
                    defendant TEXT,
                    judge_name TEXT,
                    current_status TEXT,
                    hearing_date TEXT,
                    disposal_date TEXT,
                    detail_url TEXT,
                    document_available BOOLEAN DEFAULT FALSE,
                    crawled_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    raw_data JSONB,
                    INDEX idx_case_number (case_number),
                    INDEX idx_district (district),
                    INDEX idx_year (year_filed),
                    INDEX idx_status (current_status)
                );

                CREATE TABLE IF NOT EXISTS crawl_progress (
                    id SERIAL PRIMARY KEY,
                    district TEXT NOT NULL,
                    year_start INTEGER NOT NULL,
                    year_end INTEGER NOT NULL,
                    case_status TEXT NOT NULL,
                    records_found INTEGER DEFAULT 0,
                    records_processed INTEGER DEFAULT 0,
                    errors_count INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'pending',
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    UNIQUE(district, year_start, year_end, case_status)
                );

                CREATE TABLE IF NOT EXISTS crawl_errors (
                    id SERIAL PRIMARY KEY,
                    district TEXT,
                    year INTEGER,
                    case_status TEXT,
                    error_type TEXT,
                    error_message TEXT,
                    timestamp TIMESTAMP DEFAULT NOW(),
                    retry_count INTEGER DEFAULT 0
                );
            """)

    async def insert_case(self, case_data: Dict) -> bool:
        """Insert or update case record"""
        try:
            case_id_hash = case_data['case_id_hash']
            async with self.pool.acquire() as conn:
                result = await conn.execute("""
                    INSERT INTO cases (
                        case_id_hash, case_number, case_type, year_filed,
                        district, court_name, bench_location, plaintiff, defendant,
                        judge_name, current_status, hearing_date, disposal_date,
                        detail_url, document_available, raw_data
                    ) VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16
                    )
                    ON CONFLICT (case_id_hash) DO UPDATE SET
                        current_status = EXCLUDED.current_status,
                        hearing_date = EXCLUDED.hearing_date,
                        updated_at = NOW()
                """,
                    case_data['case_id_hash'],
                    case_data['case_number'],
                    case_data.get('case_type'),
                    case_data.get('year_filed'),
                    case_data['district'],
                    case_data['court_name'],
                    case_data.get('bench_location'),
                    case_data.get('plaintiff'),
                    case_data.get('defendant'),
                    case_data.get('judge_name'),
                    case_data['current_status'],
                    case_data.get('hearing_date'),
                    case_data.get('disposal_date'),
                    case_data.get('detail_url'),
                    case_data.get('document_available', False),
                    json.dumps(case_data)
                )
            return result == "INSERT 0 1" or "UPDATE 1" in result
        except Exception as e:
            logger.error(f"Error inserting case: {e}")
            return False

    async def update_progress(self, district: str, year_start: int, year_end: int,
                            case_status: str, records_found: int):
        """Update crawl progress tracking"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO crawl_progress
                    (district, year_start, year_end, case_status, records_found, status, started_at)
                VALUES ($1, $2, $3, $4, $5, 'in_progress', NOW())
                ON CONFLICT (district, year_start, year_end, case_status) DO UPDATE SET
                    records_found = $5,
                    updated_at = NOW()
            """, district, year_start, year_end, case_status, records_found)

# ============================================================================
# CASE DATA EXTRACTION
# ============================================================================

class CaseExtractor:
    """Extract case data from search results"""

    @staticmethod
    def parse_case_number(case_no_text: str) -> Dict:
        """
        Parse case number string into components.

        Format: "CaseType YYYY/YYYY, Plaintiff V/S Defendant"
        Example: "Criminal Bail Application 2020/2024, Shehzad Ghulam Hussain
                  son of Ghulam Hussain V/S The State"
        """
        import re

        case_data = {
            'case_number': case_no_text,
            'case_type': None,
            'year_filed': None,
            'plaintiff': None,
            'defendant': None,
        }

        # Pattern: CaseType YYYY/YYYY, Parties
        pattern = r"^(.+?)\s+(\d{4})/(\d{4}),\s+(.+?)\s+V/S\s+(.+)$"
        match = re.search(pattern, case_no_text.strip())

        if match:
            case_data['case_type'] = match.group(1).strip()
            case_data['year_filed'] = int(match.group(2))
            case_data['plaintiff'] = match.group(4).strip()
            case_data['defendant'] = match.group(5).strip()

        return case_data

    @staticmethod
    def parse_court_name(court_name_text: str) -> Dict:
        """
        Parse court name to extract judge and bench location.

        Format: "Judge Title, District (Subdivision)"
        """
        import re

        court_data = {
            'court_name': court_name_text,
            'judge_name': None,
            'bench_location': None,
        }

        # Try to extract judge title (before comma)
        parts = court_name_text.split(',')
        if len(parts) >= 1:
            court_data['judge_name'] = parts[0].strip()

        # Extract location (in parentheses)
        location_match = re.search(r'\(([^)]+)\)', court_name_text)
        if location_match:
            court_data['bench_location'] = location_match.group(1).strip()

        return court_data

    @staticmethod
    def parse_status(status_text: str) -> Dict:
        """
        Parse status field to extract current status and dates.

        Formats:
        - "Disposed 04/Jul/2024"
        - "Pending"
        - "Adjourned to 15/Mar/2026"
        """
        import re

        status_data = {
            'current_status': None,
            'disposal_date': None,
            'hearing_date': None,
        }

        if 'Disposed' in status_text:
            status_data['current_status'] = 'Disposed'
            # Extract date
            date_match = re.search(r'(\d{2}/\w+/\d{4})', status_text)
            if date_match:
                try:
                    status_data['disposal_date'] = dateutil.parser.parse(
                        date_match.group(1),
                        dayfirst=True
                    ).isoformat()
                except:
                    status_data['disposal_date'] = date_match.group(1)

        elif 'Pending' in status_text:
            status_data['current_status'] = 'Pending'

        elif 'Adjourned' in status_text:
            status_data['current_status'] = 'Adjourned'
            # Extract next hearing date
            date_match = re.search(r'(\d{2}/\w+/\d{4})', status_text)
            if date_match:
                try:
                    status_data['hearing_date'] = dateutil.parser.parse(
                        date_match.group(1),
                        dayfirst=True
                    ).isoformat()
                except:
                    status_data['hearing_date'] = date_match.group(1)

        return status_data

    @classmethod
    def extract_from_table_row(cls, row_html: str, district: str) -> Optional[Dict]:
        """
        Extract case data from a table row.

        Returns dict with all case fields or None if parse fails.
        """
        try:
            soup = BeautifulSoup(row_html, 'html.parser')
            cells = soup.find_all('td')

            if len(cells) < 6:
                return None

            # Extract cell contents
            s_no = cells[0].get_text(strip=True)
            case_no_text = cells[1].get_text(strip=True)
            court_name_text = cells[2].get_text(strip=True)
            status_text = cells[3].get_text(strip=True)
            hearing_date_text = cells[4].get_text(strip=True)

            # Check if document available
            action_cell = cells[5].get_text(strip=True)
            document_available = "NOT FOUND" not in action_cell

            # Parse components
            case_parts = cls.parse_case_number(case_no_text)
            court_parts = cls.parse_court_name(court_name_text)
            status_parts = cls.parse_status(status_text)

            # Create case ID hash for deduplication
            case_id_hash = hashlib.md5(
                f"{case_no_text}|{court_name_text}|{district}".encode()
            ).hexdigest()

            # Merge all data
            case_data = {
                'case_id_hash': case_id_hash,
                'district': district,
                'document_available': document_available,
                **case_parts,
                **court_parts,
                **status_parts,
            }

            # Add hearing date if in status
            if hearing_date_text and not case_data.get('hearing_date'):
                try:
                    case_data['hearing_date'] = dateutil.parser.parse(
                        hearing_date_text,
                        dayfirst=True
                    ).isoformat()
                except:
                    case_data['hearing_date'] = hearing_date_text

            return case_data

        except Exception as e:
            logger.error(f"Error parsing table row: {e}")
            return None

# ============================================================================
# CRAWLER
# ============================================================================

class SindhCourtsC rawler:
    """Main crawler orchestrator"""

    def __init__(self, db_url: str):
        self.db = DatabaseManager(db_url)
        self.extractor = CaseExtractor()
        self.session = None
        self.request_times = []  # Track request timing for rate limiting

    async def init(self):
        """Initialize crawler"""
        await self.db.connect()
        self.session = aiohttp.ClientSession()
        logger.info("Crawler initialized")

    async def close(self):
        """Cleanup"""
        await self.db.disconnect()
        if self.session:
            await self.session.close()

    async def _rate_limit(self):
        """Implement rate limiting (30 req/min = 1 req/2 sec)"""
        await asyncio.sleep(CRAWL_DELAY)

    async def _search_cases(
        self,
        district: str,
        year_from: int,
        year_to: int,
        case_status: str = "All"
    ) -> Optional[CrawlResult]:
        """
        Execute search request.

        Returns raw HTML result from Crawl4AI or None on failure.
        """
        await self._rate_limit()

        search_params = {
            'district': district,
            'year_from': year_from,
            'year_to': year_to,
            'case_status': case_status,
            'court_type': 'NIL-Default Court Type',
            'case_category': 'All',
        }

        logger.info(
            f"Searching: {district} | {year_from}-{year_to} | {case_status}"
        )

        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                async with AsyncWebCrawler() as crawler:
                    result = await crawler.arun(
                        url=SEARCH_ENDPOINT,
                        method="GET",
                        params=search_params,
                        wait_for="table tbody",
                        timeout=REQUEST_TIMEOUT,
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    )

                    if result.status_code == 200:
                        return result

                    logger.warning(
                        f"Search returned status {result.status_code}. "
                        f"Retry {retry_count + 1}/{MAX_RETRIES}"
                    )

            except asyncio.TimeoutError:
                logger.warning(f"Timeout during search. Retry {retry_count + 1}/{MAX_RETRIES}")

            except Exception as e:
                logger.error(f"Error during search: {e}. Retry {retry_count + 1}/{MAX_RETRIES}")

            retry_count += 1
            if retry_count < MAX_RETRIES:
                await asyncio.sleep(CRAWL_DELAY * (RETRY_BACKOFF ** retry_count))

        return None

    async def _extract_results(self, html: str, district: str) -> List[Dict]:
        """
        Extract all cases from result HTML.

        Uses BeautifulSoup to parse table structure.
        """
        cases = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table')

            if not table:
                logger.warning(f"No table found for {district}")
                return cases

            tbody = table.find('tbody')
            if not tbody:
                logger.warning(f"No tbody found in table for {district}")
                return cases

            rows = tbody.find_all('tr')
            logger.info(f"Found {len(rows)} rows for {district}")

            for row in rows:
                case = self.extractor.extract_from_table_row(str(row), district)
                if case:
                    cases.append(case)

            return cases

        except Exception as e:
            logger.error(f"Error extracting results: {e}")
            return cases

    async def crawl_district_year(
        self,
        district: str,
        year_from: int,
        year_to: int,
        case_status: str
    ) -> Tuple[int, int]:
        """
        Crawl single district/year/status combination.

        Returns (records_found, records_inserted).
        """
        logger.info(f"Crawling: {district} ({year_from}-{year_to}) {case_status}")

        result = await self._search_cases(district, year_from, year_to, case_status)

        if not result:
            logger.error(f"Failed to fetch results for {district}")
            return (0, 0)

        cases = await self._extract_results(result.html, district)
        inserted = 0

        for case in cases:
            if await self.db.insert_case(case):
                inserted += 1

        logger.info(
            f"District complete: {district} | Found: {len(cases)} | "
            f"Inserted: {inserted}"
        )

        return (len(cases), inserted)

    async def crawl_all(
        self,
        start_year: int = 2000,
        end_year: int = 2025
    ) -> Dict:
        """
        Execute full crawl of all districts and years.

        Returns summary statistics.
        """
        logger.info("Starting full crawl")
        stats = {
            'total_cases_found': 0,
            'total_cases_inserted': 0,
            'total_errors': 0,
            'start_time': datetime.now(),
        }

        tasks = []

        for district in DISTRICTS:
            for year in range(start_year, end_year + 1):
                for status in CASE_STATUS_OPTIONS:
                    # Create task for each search combination
                    task = self.crawl_district_year(district, year, year, status)
                    tasks.append(task)

        # Execute tasks with concurrency limit (5 concurrent)
        semaphore = asyncio.Semaphore(5)

        async def bounded_task(task):
            async with semaphore:
                return await task

        results = await asyncio.gather(*[bounded_task(t) for t in tasks], return_exceptions=True)

        for result in results:
            if isinstance(result, tuple):
                stats['total_cases_found'] += result[0]
                stats['total_cases_inserted'] += result[1]
            elif isinstance(result, Exception):
                logger.error(f"Task error: {result}")
                stats['total_errors'] += 1

        stats['end_time'] = datetime.now()
        stats['duration_hours'] = (
            stats['end_time'] - stats['start_time']
        ).total_seconds() / 3600

        logger.info(f"Crawl complete: {json.dumps(stats, default=str, indent=2)}")
        return stats

# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Main entry point"""
    db_url = "postgresql://crawler:password@localhost:5432/sindh_courts"

    crawler = SindhCourtsC rawler(db_url)

    try:
        await crawler.init()

        # Start crawl
        stats = await crawler.crawl_all(start_year=2020, end_year=2024)

        # Save statistics
        with open('crawl_stats.json', 'w') as f:
            json.dump(stats, f, default=str, indent=2)

        logger.info(f"Crawl statistics saved to crawl_stats.json")

    except Exception as e:
        logger.error(f"Fatal error: {e}")

    finally:
        await crawler.close()

if __name__ == "__main__":
    asyncio.run(main())
