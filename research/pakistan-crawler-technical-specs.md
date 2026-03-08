# Pakistan Legislative Crawler - Technical Implementation Specifications

**Date**: 2026-03-08
**Purpose**: Detailed technical specifications for building a crawler

---

## DATA SOURCE MAPPING

### TIER 1: HIGH PRIORITY (Stable, Well-Structured)

#### 1.1 National Assembly of Pakistan

**Base URL**: `https://www.na.gov.pk/en/`

**Bill Endpoints**:
```
/bills.php                              # All bills
/bills.php?type=1                       # Government bills
/bills.php?type=2                       # Private member bills
/bills.php?status=pass                  # Passed bills
/bills-15.php?status=pass               # 2018-2023 session
```

**Bill Document URLs** (extracted from page):
```
Pattern: /uploads/documents/{id}.pdf
Example: /uploads/documents/649959d307ba6_291.pdf
```

**Extraction Fields**:
- Bill Number: `<td>91 of 2025</td>`
- Title: Linked text in table
- Date: Date column
- Type: Government or Private Member
- Status: Current status column
- Document link: PDF href in row

**Implementation Notes**:
- Query parameters are stable
- PDF links follow predictable pattern
- No login required
- Implement 2-3 second delays between requests
- Handle timeout errors with exponential backoff

---

#### 1.2 Senate of Pakistan

**Base URL**: `https://www.senate.gov.pk/en/`

**Bill Endpoints**:
```
/bills.php?id=-1&catid=186&subcatid=276&cattitle=Bills              # All bills
/billsDetails.php?type=1&id=-1&catid=186&subcatid=276&cattitle=Bills # Government
/billsDetails.php?type=2&id=-1&catid=186&subcatid=276               # Passed
/gbna.php?catid=186&cattitle=Bills&leftcatid=279                    # From NA
```

**Parameter Reference**:
- `catid=186` → Bills category
- `subcatid=276` → Specific legislation
- `type=1` → Government
- `type=2` → Passed

**Extraction Fields**:
- Bill Number
- Title
- Date
- Sponsor
- Status
- Committee information

**Implementation Notes**:
- Complex query structure but consistent
- Use parameter builder to construct URLs
- Handle category/subcategory navigation
- Store parameter mappings for reference

---

#### 1.3 Punjab Law Portal (PITB)

**Base URL**: `https://pitb.gov.pk/law_portal` or `https://law.punjab.gov.pk/law_portal`

**Coverage**: All Punjab legislation

**Features**:
- Full-text search capability
- Covers Bills, Acts, Rules, Notifications
- Searchable database (HTML forms)

**Implementation Notes**:
- POST-based search (likely)
- Very large database
- Slow search response times possible
- Consider direct HTML index if available
- Rate limit aggressively (1-2 second delays)

**Extraction Strategy**:
1. Identify searchable categories
2. Query each category systematically
3. Extract results from search pages
4. Follow links to full text (PDF/HTML)

---

### TIER 2: MEDIUM PRIORITY (Provincial)

#### 2.1 Punjab Assembly

**Base URL**: `https://pap.gov.pk/`

**Bill Endpoints**:
```
/bills/show/en                          # All bills
[Additional filtering parameters needed]
```

**Document Format**: HTML listings + PDF downloads

**Implementation Notes**:
- Language parameter: `/en` for English
- Modern interface (likely JavaScript-based)
- May require browser automation or JavaScript execution
- Follow pagination carefully

---

#### 2.2 Sindh Assembly

**Base URL**: `https://www.pas.gov.pk/` or `https://www.sindhlaws.gov.pk/`

**Bill Endpoints**:
```
/bills                                  # Primary
/Gazette.aspx?pg=BILLS                  # Law Department
```

**Alternative Source**:
```
https://www.sindhlaws.gov.pk/SindhIndex.aspx # Indexed laws
```

**Implementation Notes**:
- Multiple entry points
- Check both PAS and Law Department
- Reconcile overlapping records

---

#### 2.3 KPK Assembly

**Base URL**: `https://www.pakp.gov.pk/`

**Bill Endpoints**:
```
/bill/                                  # Bills listing
/all-bills/                             # Complete bills
/act/                                   # Acts
/all-acts/                              # Complete acts
```

**Implementation Notes**:
- Well-organized URL structure
- Separate bills and acts sections
- Clean, predictable paths

---

#### 2.4 Balochistan Assembly

**Base URL**: `https://pabalochistan.gov.pk/new/`

**Bill Endpoints**:
```
/acts/                                  # Acts
/private-members-bill-introduced/       # Introduced bills
```

**Implementation Notes**:
- New portal (pabalochistan.gov.pk/new/)
- Old portal still accessible (old.pabalochistan.gov.pk)
- Check both for completeness
- May have duplicate records

---

### TIER 3: SUPPLEMENTARY (Special Purpose)

#### 3.1 Open Parliament Pakistan (FAFEN)

**Base URL**: `http://openparliament.pk/`

**Key Sections**:
```
/legislative-tracker/                   # Bill tracking
/bill-details/                          # Bill details
/how-parliament-functions/bill-to-an-act/
```

**Advantages**:
- Centralized for multiple legislatures
- Full text Acts available
- Metadata: mover, party, session, sitting
- Subscription/notification capability

**Implementation Notes**:
- Curated data (better quality than raw scraping)
- FAFEN maintains this as service
- Consider as validation source
- Check for API documentation

---

#### 3.2 Federal Special Courts

**Base URL**: `https://federalcourts.molaw.gov.pk/`

**Case Search**:
```
/casesSearch                            # Main search interface
/courts?Province=F                      # Federal courts
/courts?Province=P                       # Punjab courts
```

**Implementation Notes**:
- Database-driven system
- Province parameter filtering
- Likely has search form interface
- May require POST requests

**Caution**: Judge rate limiting carefully for large result sets

---

#### 3.3 Punjab District Courts

**Base URL**: `https://dsj.punjab.gov.pk/`

**Case Search**:
```
/casedetail/[case-id]                   # Individual cases
/                                       # Main portal
/login                                  # Authenticated access
```

**Case ID Format**: UUID (e.g., `fef873297a125268a4a4bc01c`)

**Volume**: 8,000,000+ cases

**Implementation Notes**:
- **CRITICAL**: Review Terms of Service before crawling
- Very large database (rate limit strictly)
- Consider request rate caps (100-200 cases/day)
- Judgment text availability varies by case
- May require authentication for full text

---

## CRAWLER IMPLEMENTATION ARCHITECTURE

### Module 1: Source Configuration

```python
# sources.py
SOURCES = {
    'national_assembly': {
        'base_url': 'https://www.na.gov.pk/en/',
        'bill_endpoints': [
            {'path': 'bills.php', 'params': {}},
            {'path': 'bills.php', 'params': {'type': '1'}},
            {'path': 'bills.php', 'params': {'type': '2'}},
            {'path': 'bills.php', 'params': {'status': 'pass'}},
        ],
        'rate_limit_seconds': 2,
        'timeout_seconds': 10,
        'verify_ssl': True,
        'extract_fields': ['bill_number', 'title', 'date', 'type', 'status'],
        'document_url_pattern': r'/uploads/documents/(.+?).pdf'
    },
    # ... more sources
}
```

### Module 2: HTML Extraction

```python
# extractors.py
class BillListExtractor:
    """Extract bill metadata from list pages"""

    def extract_bills(self, html: str, source: str) -> List[Dict]:
        """
        Parse HTML listing page and extract bill records

        Returns:
            List of dicts with:
            - bill_number: str
            - title: str
            - date_introduced: str (YYYY-MM-DD)
            - type: str ('Government' | 'Private Member')
            - status: str
            - document_url: str
            - source_url: str
        """
        pass

class PDFExtractor:
    """Extract full text from bill PDFs"""

    def extract_text(self, pdf_bytes: bytes) -> str:
        """Extract full text from PDF"""
        pass

    def extract_metadata(self, pdf_path: str) -> Dict:
        """Extract PDF metadata"""
        pass
```

### Module 3: Data Storage

```python
# models.py
class Bill(BaseModel):
    id: UUID
    source: str  # 'national_assembly', 'senate', etc.
    bill_number: str
    title: str
    date_introduced: datetime
    date_passed: Optional[datetime]
    bill_type: str  # 'Government' | 'Private Member'
    status: str  # 'Passed', 'Pending', etc.
    mover: Optional[str]
    committee: Optional[str]
    summary: Optional[str]
    full_text: str  # Extracted from PDF
    source_url: str
    document_url: str
    scraped_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            'example': {
                'bill_number': '91 of 2025',
                'title': 'Some Amendment Bill, 2025',
                'date_introduced': '2025-06-15',
                'status': 'Passed',
                'source': 'national_assembly'
            }
        }
```

### Module 4: Crawler Queue Management

```python
# queue_manager.py
class CrawlerQueue:
    """Manage crawl tasks with rate limiting"""

    def __init__(self, source_config: Dict):
        self.config = source_config
        self.last_request_time = {}

    def add_task(self, url: str, priority: int = 0):
        """Add URL to crawl queue"""
        pass

    def get_next_task(self) -> Optional[str]:
        """Get next URL respecting rate limits"""
        # Check if enough time has passed since last request
        # Return URL if ready, None if rate-limited
        pass

    def mark_complete(self, url: str, status: str):
        """Mark task as complete/failed"""
        pass
```

### Module 5: Error Handling

```python
# errors.py
class CrawlerError(Exception):
    """Base crawler error"""
    pass

class RateLimitedError(CrawlerError):
    """Server returned rate limit error"""
    pass

class TimeoutError(CrawlerError):
    """Request timeout"""
    pass

class PDFExtractionError(CrawlerError):
    """Failed to extract from PDF"""
    pass

# Retry strategies
class RetryStrategy:
    @staticmethod
    def exponential_backoff(attempt: int, base_delay: int = 2) -> int:
        """Return delay in seconds: 2, 4, 8, 16, 32..."""
        return base_delay ** min(attempt, 5)
```

---

## FIELD MAPPING ACROSS SOURCES

### Standard Bill Fields (Normalized)

```
Database Schema:
- pk_id: UUID (primary key)
- source_identifier: str (e.g., 'na_2025_91')
- bill_number: str (e.g., '91 of 2025')
- legislative_body: enum ('National Assembly', 'Senate', 'Punjab Assembly', etc.)
- province: str (null for federal, 'Punjab', 'Sindh', etc.)
- title_en: str
- title_ur: Optional[str] (where available)
- bill_type: enum ('Government', 'Private Member', 'Constitutional Amendment')
- introduction_date: date
- introduction_sitting: Optional[str] (session/sitting reference)
- mover_name: str
- mover_party: Optional[str]
- current_status: enum ('Introduced', 'Referred to Committee', 'Passed', 'Rejected', 'Pending')
- status_date: date (last status update)
- committee_referred: Optional[str]
- committee_report_received: bool
- passed_date: Optional[date]
- votes_for: Optional[int]
- votes_against: Optional[int]
- votes_abstain: Optional[int]
- assent_date: Optional[date]
- act_number: Optional[str] (if passed)
- related_ordinances: Optional[List[str]]
- full_text_url: str
- full_text_format: enum ('PDF', 'HTML', 'Both')
- full_text_language: enum ('English', 'Urdu', 'Both')
- extracted_text: Optional[str] (OCR'd if needed)
- summary: Optional[str] (AI-generated)
- key_clauses: Optional[List[str]]
- amendments: Optional[List[Dict]] (bill amendments)
- related_bills: Optional[List[str]] (cross-references)
- source_url: str (where crawled from)
- crawled_at: datetime
- last_updated: datetime
- data_quality_score: float (0-1)
```

---

## EXTRACTION PATTERNS

### Pattern 1: National Assembly Bills Table

```html
<table>
<tr>
  <td>91 of 2025</td>
  <td><a href="/bills-details.php?id=123">Bill Title Here</a></td>
  <td>2025-06-15</td>
  <td>Government</td>
  <td>Passed</td>
  <td><a href="/uploads/documents/abc123.pdf">PDF</a></td>
</tr>
</table>
```

**XPath/CSS Selectors**:
```
Bill Number: td[0]
Title & Link: td[1] > a
Date: td[2]
Type: td[3]
Status: td[4]
Document: td[5] > a::attr(href)
```

---

### Pattern 2: Provincial Assembly Listings

```html
<div class="bill-item">
  <h3>Bill Title</h3>
  <span class="bill-number">123 of 2025</span>
  <span class="date">2025-01-15</span>
  <span class="status">Passed</span>
  <a href="/bills/123" class="details">Details</a>
</div>
```

**CSS Selectors**:
```
.bill-item
  h3 → title
  .bill-number → number
  .date → date
  .status → status
  a.details::attr(href) → details_url
```

---

## PDF EXTRACTION STRATEGY

### For Bill Full Text

```python
import pdfplumber

def extract_bill_text(pdf_path: str) -> Dict:
    """Extract text and metadata from bill PDF"""
    with pdfplumber.open(pdf_path) as pdf:
        metadata = pdf.metadata

        # Extract all text
        full_text = '\n'.join(page.extract_text() for page in pdf.pages)

        # Detect sections (typical bill structure)
        sections = detect_sections(full_text)

        return {
            'full_text': full_text,
            'page_count': len(pdf.pages),
            'creation_date': metadata.get('CreationDate'),
            'title': metadata.get('Title'),
            'sections': sections,
            'tables': extract_tables(pdf)
        }
```

### Bill Structure Recognition

```python
# Typical Pakistan bill structure
BILL_SECTIONS = [
    r'^A BILL$',
    r'^OBJECTS AND REASONS$',
    r'^STATEMENT OF OBJECTS AND REASONS',
    r'^\d+\.\s+Short title and commencement',
    r'^\d+\.\s+Definitions',
    r'^\d+\.\s+[A-Z]',  # Section headings
    r'^SCHEDULE$',
]

def detect_bill_sections(text: str) -> Dict[str, Tuple[int, int]]:
    """Identify section boundaries in bill text"""
    pass
```

---

## RATE LIMITING CONFIGURATION

### Per-Source Rate Limits

```python
RATE_LIMITS = {
    'national_assembly': {
        'requests_per_second': 0.5,        # 2 second delay
        'concurrent_connections': 1,
        'timeout_seconds': 10,
        'retry_on_timeout': True,
        'max_retries': 3,
        'backoff_factor': 2
    },
    'senate': {
        'requests_per_second': 0.5,
        'concurrent_connections': 1,
        'timeout_seconds': 10,
    },
    'punjab_law_portal': {
        'requests_per_second': 1.0,         # 1 second delay (safer for large DB)
        'concurrent_connections': 1,
        'timeout_seconds': 15,
    },
    'district_courts': {
        'requests_per_second': 0.2,         # 5 second delay (VERY large DB)
        'concurrent_connections': 1,
        'timeout_seconds': 20,
        'max_results_per_day': 200,         # Hard limit
        'respect_robots_txt': True,
        'review_tos_required': True
    }
}
```

### Request Throttling Implementation

```python
from asyncio import sleep
from time import time

class RateLimiter:
    def __init__(self, requests_per_second: float):
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0

    async def wait(self):
        """Wait until safe to make next request"""
        elapsed = time() - self.last_request_time
        if elapsed < self.min_interval:
            await sleep(self.min_interval - elapsed)
        self.last_request_time = time()
```

---

## MONITORING & LOGGING

### Crawler Health Metrics

```python
class CrawlerMetrics:
    def __init__(self):
        self.total_urls_crawled = 0
        self.successful_extractions = 0
        self.failed_extractions = 0
        self.timeout_errors = 0
        self.rate_limit_errors = 0
        self.total_documents_extracted = 0
        self.last_crawl_timestamp = None

    def get_health_status(self) -> Dict:
        success_rate = (self.successful_extractions /
                       (self.successful_extractions + self.failed_extractions))
        return {
            'success_rate': success_rate,
            'urls_crawled': self.total_urls_crawled,
            'documents_extracted': self.total_documents_extracted,
            'timeout_rate': self.timeout_errors / self.total_urls_crawled,
            'last_crawl': self.last_crawl_timestamp
        }
```

### Logging Strategy

```python
# Standard format for all log entries
LOG_FORMAT = {
    'timestamp': 'ISO8601',
    'source': 'source_name',
    'url': 'full_url_crawled',
    'status_code': 'HTTP status',
    'extracted_items': 'count',
    'duration_seconds': 'float',
    'error': 'error_message if any',
    'retry_attempt': 'int'
}
```

---

## TESTING STRATEGY

### Unit Tests

```python
def test_bill_extraction_national_assembly():
    """Test bill list extraction from NA page"""
    html = load_fixture('na_bills_page.html')
    bills = BillListExtractor.extract_bills(html, 'national_assembly')
    assert len(bills) > 0
    assert 'bill_number' in bills[0]
    assert 'title' in bills[0]

def test_pdf_extraction():
    """Test PDF text extraction"""
    pdf_path = load_fixture('sample_bill.pdf')
    text = PDFExtractor.extract_text(pdf_path)
    assert len(text) > 100
    assert 'SHORT TITLE' in text.upper()

def test_rate_limiting():
    """Test rate limiter respects delays"""
    limiter = RateLimiter(0.5)  # 2 second delay
    start = time()
    await limiter.wait()
    duration = time() - start
    assert duration >= 1.9  # Allow 100ms tolerance
```

### Integration Tests

```python
def test_crawl_national_assembly_bills():
    """End-to-end test: crawl NA, extract bills"""
    # Only run against staging or with approval
    # Crawl first 5 bills from NA
    # Verify extraction quality
    pass

def test_document_download():
    """Test downloading and extracting PDF from actual source"""
    pass
```

---

## DEPLOYMENT CHECKLIST

- [ ] robots.txt validation for all sources
- [ ] Terms of Service review (especially district courts)
- [ ] Rate limiting tested and verified
- [ ] Timeout/error handling stress tested
- [ ] Database schema created and indexed
- [ ] PDF extraction library tested (pdfplumber)
- [ ] Logging and monitoring configured
- [ ] Data quality validation rules defined
- [ ] Backup strategy for PDFs implemented
- [ ] Update frequency schedule defined
- [ ] Alerting configured for errors/timeouts
- [ ] Documentation for field mappings created
- [ ] User authentication for sensitive data planned
- [ ] API endpoint created for data access (if applicable)

---

**Technical Specifications Version**: 1.0
**Last Updated**: 2026-03-08
