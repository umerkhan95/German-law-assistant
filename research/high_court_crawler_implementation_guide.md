# High Court Legal Crawler - Implementation Guide

**Status**: Ready to implement Tiers 1 & 2; Tier 3 requires direct contact  
**Estimated documents**: 80,000+ judgments  
**Setup time**: 2-3 weeks for both courts

---

## TIER 1: Peshawar High Court (PHC) - PRIORITY 1

### Quick Facts
- **Complexity**: Easy
- **Blocking**: None
- **CAPTCHA**: No
- **Rate limit**: 2-5 req/sec OK
- **Expected success**: 95%+
- **Estimated content**: 50,000+ judgments

### Crawler Entry Points

#### 1. Reported Judgments (PHCCMS)
```
URL: https://www.peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php
Technology: jQuery DataTables
Pagination: 25 records/page (configurable)

Filters Available:
├── Year: 2010-2026 dropdown
├── Judge: Full judge name dropdown (iterate all)
├── Category: [All, Criminal, Civil, Revenue, Constitutional, Service, Corporate]
└── Search parameters: TBD (must capture from DataTables)

Crawling Strategy:
1. Get year dropdown values
2. Get judge dropdown values
3. Get category dropdown values
4. Iterate: for each (year, judge, category) combination:
   - Request PHCCMS with filter params
   - Parse DataTables response
   - Extract judgment links
   - Download PDFs from /PHCCMS/judgments/[CASE_REF].pdf
   - Extract metadata: case#, title, judge, date, category
```

#### 2. Abbottabad Bench
```
URL: https://peshawarhcatd.gov.pk/search_cases.phc
Search Methods:
├── Party Details: "Search Case with Party First Name, Second Name or with case auto number"
├── FIR Number: dedicated link
└── Case Number: advanced search

Crawling Strategy:
1. Enumerate common party names (major law firms, advocate names)
2. Enumerate common FIR numbers (sequential range)
3. Request case search with each parameter
4. Parse results for case metadata
5. Download associated judgment PDFs
```

#### 3. Mingora Bench (Swat)
```
URL: https://www.peshawarhcmb.gov.pk/
Similar structure to Abbottabad bench
Additional features: cause lists, daily orders, counsel registry

Crawling Strategy:
1. Similar to Abbottabad
2. Extract from cause lists (daily updates)
3. Parse counsel registry for cross-references
4. Monitor tentative fixed cases calendar
```

#### 4. Case Diary System
```
URL: https://diary.peshawarhighcourt.gov.pk/
Purpose: Real-time case proceeding updates
Requirement: Advocate login (if needed)

Features Available:
├── Advocate case diary
├── Real-time proceedings
├── Case search
└── FIR linkage search

Crawling Strategy:
1. Check if public access available
2. If login required: contact court for bulk access
3. Otherwise: crawl public case data
```

### PDF URL Pattern
```
https://peshawarhighcourt.gov.pk/PHCCMS/judgments/[CASE_REF].pdf

Examples:
- 236-of-15.pdf
- w.p-1372-M-of-2022.pdf
- WP-No.-1292-2013-and-2-connected-cases.pdf

Strategy:
1. Discover CASE_REF from search results
2. Construct URL
3. Download directly
4. Extract text from PDF
```

### Expected Fields (Inferred)
```
From search results:
├── Case number
├── Case type (Criminal, Civil, Revenue, Constitutional, Service, Corporate)
├── Parties (plaintiff, defendant)
├── Judge name
├── Decision date
├── Citation reference
├── Link to full judgment PDF

From PDF extraction:
├── Full judgment text
├── Headnotes
├── Laws discussed
├── Case history
└── Orders
```

### Crawling Code Template (Python)
```python
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class PeshawarHighCourtCrawler:
    def __init__(self):
        self.base_url = "https://www.peshawarhighcourt.gov.pk"
        self.phccms_url = f"{self.base_url}/PHCCMS/reportedJudgments.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Legal AI Crawler v1.0'
        })
        
    def get_filters(self):
        """Extract available filter values from page"""
        resp = self.session.get(self.phccms_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        years = [opt.get('value') for opt in soup.select('select[name="year"] option')]
        judges = [opt.get('value') for opt in soup.select('select[name="judge"] option')]
        categories = [opt.get('value') for opt in soup.select('select[name="category"] option')]
        
        return {
            'years': years,
            'judges': judges,
            'categories': categories
        }
    
    def search_judgments(self, year=None, judge=None, category=None, page=1):
        """Search with filters"""
        params = {
            'page': page,
            'year': year or 'all',
            'judge': judge or 'all',
            'category': category or 'all'
        }
        resp = self.session.get(self.phccms_url, params=params)
        return self.parse_datatable_response(resp)
    
    def parse_datatable_response(self, response):
        """Parse DataTables JSON response"""
        try:
            data = response.json()
            results = []
            for row in data.get('data', []):
                results.append({
                    'case_number': row[0],
                    'parties': row[1],
                    'judge': row[2],
                    'date': row[3],
                    'category': row[4],
                    'pdf_url': row[5] if len(row) > 5 else None
                })
            return results
        except:
            return []
    
    def crawl_all(self):
        """Main crawl routine"""
        filters = self.get_filters()
        results = []
        
        for year in filters['years'][:5]:  # Test with 5 years first
            for judge in filters['judges'][:10]:  # Test with 10 judges first
                for category in filters['categories']:
                    print(f"Crawling: {year}, {judge}, {category}")
                    
                    for page in range(1, 100):  # Paginate through results
                        judgments = self.search_judgments(year, judge, category, page)
                        if not judgments:
                            break
                        
                        for judgment in judgments:
                            results.append(judgment)
                            if judgment['pdf_url']:
                                self.download_pdf(judgment['pdf_url'])
        
        return results
    
    def download_pdf(self, url):
        """Download judgment PDF"""
        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                filename = url.split('/')[-1]
                with open(f'pdfs/{filename}', 'wb') as f:
                    f.write(resp.content)
                return True
        except Exception as e:
            print(f"PDF download failed: {url} - {e}")
        return False

# Usage
crawler = PeshawarHighCourtCrawler()
judgments = crawler.crawl_all()
```

---

## TIER 2: Islamabad High Court (IHC) - PRIORITY 2

### Quick Facts
- **Complexity**: Medium
- **Blocking**: None detected, but unknown
- **CAPTCHA**: Unknown (none observed)
- **Rate limit**: 1-2 req/sec MAX
- **Expected success**: 70-80%
- **Estimated content**: 30,000+ judgments
- **Special handling**: Timeout retries, session management

### Crawler Entry Points

#### 1. Case Search (MIS Portal)
```
URL: https://mis.ihc.gov.pk/frmCseSrch
Technology: ASP.NET + AJAX
Backend method: srchCseIhc_ByInst
Response format: JSON

Search Parameters:
├── Case Number (mandatory)
│   └── Numeric, format: W.P.-2494-2025, etc
├── Case Year (optional)
├── Case Category (optional)
├── Party Name (mandatory for this search)
│   └── Alphabetic validation
├── FIR Number (optional)
├── Diary Number (optional)
└── Diary Type (dropdown)

Result Fields:
├── case_code
├── case_number
├── case_title
├── parties
├── bench_name
├── hearing_date
├── status
└── attachment_links

Crawling Strategy:
1. Enumerate case types: W.P., I.C.A., I.T.R., Crl. Misc., S.T.R., Cust. Ref., F.A.O., O.W.P.
2. Enumerate years: 2000-2026
3. For each (type, year):
   - Search by case number (iterate 1-9999)
   - Parse AJAX JSON response
   - Extract metadata
4. Handle timeouts with exponential backoff
```

#### 2. Order/Case Law Search
```
URL: https://mis.ihc.gov.pk/frmSrchOrdr
Technology: ASP.NET + form-based
Response format: Card layouts (HTML)

Search Options:
├── Keyword Search (6+ chars)
├── Case Number (numeric)
├── Case Title/Party (5+ chars)
├── Judge/Bench (dropdown)
├── Citation (book, year, page)
└── Advanced (case#, judge, party, date range)

Result Fields:
├── case_number
├── citation_reference
├── party_names
├── judge_composition
├── subject_classification
├── order_date
├── approval_status (Approved for Reporting / Important)
├── discussed_laws
└── headnotes

Crawling Strategy:
1. Get judge dropdown values
2. Iterate judges
3. Get citation books list
4. Search by citation + judge + year
5. Parse HTML card layouts
6. Extract metadata
```

#### 3. Library System (Optional)
```
URL: https://mis.ihc.gov.pk/frmLibDtl
Purpose: Book catalog + online legal databases
Content: 18,415 books, law journals, foreign law resources

Strategy:
Low priority - mostly reference materials
Focus on Pennsylvania Law site & PLJ Law Site links
```

### PDF Download Pattern
```
Pattern: https://mis.ihc.gov.pk/attachments/judgements/[CASE_ID]/[FILE_NUMBER]/[FILENAME].pdf

Components:
├── CASE_ID: Numeric (e.g., 199260)
├── FILE_NUMBER: Integer (1, 2, etc)
└── FILENAME: [TYPE]_[NUMBER]_[YEAR]_[TIMESTAMP].pdf

Examples:
- 199260/1/W.P._NO._2494_OF_2025_638896524549921705.pdf
- 172935/1/W.P._No.198_and_199-2024_638422384977043765.pdf

Strategy:
1. Extract from case search results (attachment links)
2. Construct URL if pattern identified
3. Download with timeout handling
```

### Case Types Supported
```
W.P.         - Writ Petition
I.C.A.       - Islamabad Court Appeal
I.T.R.       - Income Tax Review
Crl. Misc.   - Criminal Miscellaneous
S.T.R.       - Sales Tax Review
Cust. Ref.   - Customs Reference
F.A.O.       - First Appeal in Order
O.W.P.       - Original Writ Petition
```

### Special Handling Required

#### Timeout Handling
```python
import time

def exponential_backoff(attempt, max_attempts=3):
    """Exponential backoff: 1s, 5s, 30s"""
    wait_times = [1, 5, 30]
    if attempt < max_attempts:
        wait_time = wait_times[min(attempt, len(wait_times)-1)]
        time.sleep(wait_time)
        return True
    return False

def fetch_with_timeout_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response
            elif response.status_code in [429, 503]:  # Rate limit or service unavailable
                if exponential_backoff(attempt):
                    continue
                else:
                    raise Exception("Max retries exceeded")
        except requests.Timeout:
            if exponential_backoff(attempt):
                continue
            else:
                raise
    return None
```

#### Session Persistence
```python
class IHCMISCrawler:
    def __init__(self):
        self.session = requests.Session()
        # ASP.NET session handling
        self.session.headers.update({
            'User-Agent': 'Legal AI Crawler v1.0',
            'Accept': 'application/json, text/plain, */*'
        })
        
    def handle_session_cookies(self):
        """Maintain ASPNET session cookies"""
        # First request establishes session
        initial_resp = self.session.get(
            'https://mis.ihc.gov.pk/frmCseSrch'
        )
        # Subsequent requests use same session
        return initial_resp
```

### Crawling Code Template (Python)
```python
import requests
import json
import time
from urllib.parse import urlencode

class IHCMISCrawler:
    def __init__(self):
        self.base_url = "https://mis.ihc.gov.pk"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Legal AI Crawler v1.0',
            'Accept': 'application/json'
        })
        self.rate_limit_delay = 0.5  # 2 req/sec = 0.5s delay
        
    def search_by_case_number(self, case_type, case_number, case_year):
        """Search MIS by case number"""
        url = f"{self.base_url}/frmCseSrch"
        params = {
            'cseTyp': case_type,
            'cseNo': case_number,
            'cseYr': case_year
        }
        
        return self._fetch_with_retry(url, params)
    
    def search_by_party(self, party_name):
        """Search MIS by party name"""
        url = f"{self.base_url}/frmCseSrch"
        params = {
            'cseTyp': 'party',
            'partyNm': party_name
        }
        
        return self._fetch_with_retry(url, params)
    
    def search_by_citation(self, book, year, page):
        """Search order/law by citation"""
        url = f"{self.base_url}/frmSrchOrdr"
        params = {
            'srchTyp': 'citation',
            'book': book,
            'year': year,
            'page': page
        }
        
        return self._fetch_with_retry(url, params)
    
    def _fetch_with_retry(self, url, params, max_retries=3):
        """Fetch with exponential backoff"""
        wait_times = [1, 5, 30]
        
        for attempt in range(max_retries):
            try:
                resp = self.session.get(url, params=params, timeout=30)
                
                if resp.status_code == 200:
                    time.sleep(self.rate_limit_delay)
                    return resp
                elif resp.status_code in [429, 503]:
                    wait = wait_times[min(attempt, len(wait_times)-1)]
                    print(f"Rate limited. Waiting {wait}s...")
                    time.sleep(wait)
                    continue
                else:
                    resp.raise_for_status()
                    
            except requests.Timeout:
                wait = wait_times[min(attempt, len(wait_times)-1)]
                print(f"Timeout. Waiting {wait}s...")
                time.sleep(wait)
                continue
                
            except Exception as e:
                print(f"Error: {e}")
                return None
        
        return None
    
    def parse_case_search_response(self, response):
        """Parse AJAX JSON response"""
        try:
            data = response.json()
            cases = []
            
            for case in data.get('data', []):
                cases.append({
                    'case_code': case.get('caseCode'),
                    'case_number': case.get('caseNumber'),
                    'case_title': case.get('caseTitle'),
                    'parties': case.get('parties'),
                    'bench': case.get('benchName'),
                    'hearing_date': case.get('hearingDate'),
                    'status': case.get('status'),
                    'judgment_link': case.get('judgmentUrl')
                })
            
            return cases
        except Exception as e:
            print(f"Parse error: {e}")
            return []
    
    def crawl_all_cases(self):
        """Main crawl routine"""
        case_types = ['W.P.', 'I.C.A.', 'I.T.R.', 'Crl. Misc.', 'S.T.R.', 
                      'Cust. Ref.', 'F.A.O.', 'O.W.P.']
        years = range(2000, 2027)
        
        all_cases = []
        
        for case_type in case_types:
            for year in years:
                print(f"Crawling {case_type}/{year}...")
                
                # Try case numbers 1-9999 (adjust based on typical range)
                for case_num in range(1, 1000):
                    resp = self.search_by_case_number(case_type, case_num, year)
                    
                    if resp:
                        cases = self.parse_case_search_response(resp)
                        all_cases.extend(cases)
                        
                        if not cases:
                            break  # No results for this range
        
        return all_cases

# Usage
crawler = IHCMISCrawler()
cases = crawler.crawl_all_cases()
```

### Important Notes
- **Main site (ihc.gov.pk) is UNRELIABLE** - Use MIS portal only
- **robots.txt timed out** - Assume allowed, but respectful crawling recommended
- **CAPTCHA not observed** but may appear - integrate CapSolver if needed
- **Rate limiting unknown** - Start slow (1 req/sec), monitor for 429/503
- **Session persistence required** - Use same requests.Session throughout

---

## TIER 3: Balochistan High Court (BHC) - SKIP OR CONTACT

### Quick Facts
- **Blocking**: Incapsula WAF (active)
- **CAPTCHA**: Yes (Incapsula)
- **Portal**: Nuxt.js SPA (requires JS rendering)
- **Recommended action**: Contact court directly

### Blocking Details
```
Error: Incapsula incident ID: 1347000610552490059-366543650274086726
Blocks: https://bhc.gov.pk/resources/judgments
       https://portal.bhc.gov.pk/judgments/

Causes:
├── Automated crawler detection (ASN, patterns)
├── High request rate detected
├── Missing/suspicious user agents
└── Non-interactive browsing behavior
```

### If You Must Access (Not Recommended)

#### Option A: Contact Court Directly (RECOMMENDED)
```
Method: Email
Address: IT Department, Balochistan High Court
Subject: Bulk Judgment Data Request for Legal AI Research
Content:
  - Purpose: Academic/legal research
  - Scope: All reported judgments (2000-2026)
  - Format: PDF or database export
  - Timeline: 2-4 weeks typical
  - Attribution: Offer to attribute court properly

Expected success rate: 70%+
Cost: Free
Effort: Low
```

#### Option B: JavaScript Rendering + Stealth Mode
```
Requirements:
├── Crawl4ai with Chromium (JS execution)
├── Stealth mode enabled
├── Proxy rotation (residential)
├── CapSolver integration (CAPTCHA)
└── Very aggressive rate limiting (1 req/10 sec)

Success probability: <50%
Risk: Permanent IP ban
Not recommended unless desperate
```

#### Option C: Paid Crawling Service
```
Provider: crawlbase.com
Cost: $50-200/month
Success rate: 80-90%
Effort: High (integration + monitoring)
Timeline: 1-2 weeks setup

NOT RECOMMENDED - cost not justified
```

### Blocked Endpoints
```
https://bhc.gov.pk/resources/judgments                    ❌ Blocked
https://bhc.gov.pk/resources/judgments/[justice]/...      ❌ Blocked
https://portal.bhc.gov.pk/judgments/                      ❌ Blocked
```

### Potentially Accessible Endpoints
```
https://bhc.gov.pk/beta/introduction/about                ✓ (might work)
https://bhc.gov.pk/beta/resources/case-status             ✓ (might work)
```

---

## IMPLEMENTATION ROADMAP

### Week 1: PHC Setup (Tier 1)
- [ ] Day 1-2: Analyze PHCCMS filter parameters
- [ ] Day 3-4: Write judgment scraper
- [ ] Day 5: Test with 100-judgment sample
- [ ] Day 6-7: Full crawl (50,000+ judgments)

### Week 2-3: IHC Setup (Tier 2)
- [ ] Day 1-2: Reverse-engineer AJAX responses
- [ ] Day 3-4: Write case search scraper
- [ ] Day 5-6: Implement timeout/retry logic
- [ ] Day 7-10: Full crawl with monitoring (30,000+ judgments)

### Week 4+: BHC (Contact or Skip)
- [ ] Day 1: Draft email to BHC IT
- [ ] Day 2-28: Wait for response
- [ ] Decision: Proceed or skip

---

## Data Processing Pipeline

```
Raw crawl results
    ↓
[Judgment PDF]
    ├── Text extraction (pdfplumber or PyPDF2)
    ├── Metadata parsing (case#, judge, date, parties)
    ├── Citation detection (PLD, SCMR, etc)
    └── Law section indexing
    ↓
[Cleaned metadata]
    ├── Party name normalization
    ├── Judge name standardization
    ├── Case type classification
    └── Citation validation
    ↓
[Database storage]
    ├── PostgreSQL/Supabase (metadata)
    ├── Vector DB (embeddings for semantic search)
    └── S3/R2 (full text PDFs)
    ↓
[AI Training]
    ├── Legal document understanding
    ├── Citation linking
    ├── Case outcome prediction
    └── Legal research assist
```

---

## Monitoring & Maintenance

### During Crawl
```
Metrics to track:
├── Requests/sec (should be 2-5 for PHC, 1-2 for IHC)
├── Success rate (%)
├── Average response time (ms)
├── Timeout count (should be minimal)
├── 429/503 rate limit responses
├── PDF download success rate
└── Data extraction errors
```

### Error Handling
```python
# Log all errors with context
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)

# Monitor for blocking
if "Incapsula" in response.text or response.status_code == 403:
    logging.error("BLOCKED! Stop crawling immediately")
    raise Exception("WAF blocking detected")
```

---

## Final Recommendations

1. **Start with PHC (Tier 1)** - Lowest risk, highest success
2. **Add IHC (Tier 2)** after PHC working - More complex but doable
3. **Skip BHC (Tier 3)** - Contact court instead of trying to bypass Incapsula
4. **Total estimated content**: 80,000+ judgments across both courts
5. **Implementation time**: 3-4 weeks for full crawl + data processing

---

**Last Updated**: 2026-03-08  
**Report**: See high_court_verification_report.md for detailed findings
