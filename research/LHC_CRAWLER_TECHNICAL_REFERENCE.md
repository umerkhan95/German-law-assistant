# Lahore High Court Legal AI Crawler - Technical Reference

**Quick Reference for Implementation**

---

## PORTAL MAPPING

```
┌─────────────────────────────────────────────────────────────────┐
│ LAHORE HIGH COURT JUDGMENT DATA SOURCES                          │
└─────────────────────────────────────────────────────────────────┘

1. PRIMARY: data.lhc.gov.pk
   ├─ Search Forms: /reported_judgments/judgments_approved_for_reporting
   ├─ Query Endpoint: /dynamic/approved_judgments_result_new.php?year=YYYY
   ├─ Format: HTML search + links to PDFs
   ├─ Volume: 4,078 approved judgments
   ├─ Coverage: Sitting judges + Former judges + Green Bench
   └─ Priority: ★★★★★ HIGHEST

2. SUPPLEMENTARY: sys.lhc.gov.pk/appjudgments/
   ├─ Access: Direct PDF enumeration
   ├─ URL Format: /appjudgments/[YYYY]LHC[NNNN].pdf
   ├─ Format: Direct PDF files
   ├─ Volume: Subset of all judgments
   ├─ Pattern: Sequential numbering by year
   └─ Priority: ★★★★ HIGH

3. SECONDARY: library.lhc.gov.pk
   ├─ Content: Judge compendiums (PDF)
   ├─ Access: KOHA ILS at koha.lhc.gop.pk
   ├─ Format: PDF documents
   ├─ Volume: Judge-specific (limited frequency)
   └─ Priority: ★★★ MEDIUM

4. INFORMATION ONLY: lhc.gov.pk
   ├─ Content: Navigation hub + announcements
   ├─ Format: HTML
   ├─ Judgment Links: Redirect to data.lhc.gov.pk
   └─ Priority: ★ REFERENCE ONLY
```

---

## URL PATTERNS & ENDPOINTS

### Critical URLs

```
# Main entry points (currently TIMEOUT)
https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting
https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting_by_former_judges
https://data.lhc.gov.pk/reported_judgments/green_bench_orders

# Dynamic query endpoints (with parameters)
https://data.lhc.gov.pk/dynamic/approved_judgments_result_new.php?year=2024
https://data.lhc.gov.pk/dynamic/approved_judgments_result_new.php?year=2023
https://data.lhc.gov.pk/dynamic/approved_judgments_result_former_judges.php?year=2024

# Direct PDF access pattern
https://sys.lhc.gov.pk/appjudgments/2024LHC4177.pdf
https://sys.lhc.gov.pk/appjudgments/2023LHC6532.pdf

# Library system
https://library.lhc.gov.pk/Home/Compendium
https://koha.lhc.gop.pk (OPAC)

# Alternative language versions
https://data.lhc.gov.pk/urdu/reported_judgments/judgments_approved_for_reporting
```

---

## DATA FIELDS

### Standard Judgment Record

```python
{
    # Identifiers
    "case_number": "C.R.324/2003",        # String
    "case_type": "Civil Revision",         # From case_number regex
    "judgment_year": 2003,                 # Extracted from case_number
    "judgment_number": "4177",             # From URL pattern

    # Temporal
    "judgment_date": "2024-03-16",        # DD.MM.YYYY format
    "crawl_timestamp": "2024-03-08T14:30", # ISO 8601

    # Judicial
    "judges": ["Justice Name 1", "Justice Name 2"],  # Array
    "bench_name": "LAHORE",                # Or "MULTAN", "RAWALPINDI"
    "bench_type": "Regular",               # Or "Green Bench"

    # Parties
    "appellant": "Party A",                # Primary party
    "respondent": "Party B",               # Secondary party

    # Status
    "reported_status": "Approved",         # Always "Approved" in main DB
    "judge_category": "Sitting",           # Or "Former"

    # Access
    "html_url": "https://data.lhc.gov.pk/...",
    "pdf_url": "https://sys.lhc.gov.pk/appjudgments/2024LHC4177.pdf",
    "source_portal": "data.lhc.gov.pk",

    # Content
    "full_text": "Complete judgment text from PDF extraction",
    "case_summary": "Extracted or generated summary",
}
```

### Field Extraction Rules

| Field | Extraction Method | Example | Regex/Logic |
|-------|-------------------|---------|------------|
| case_number | PDF header parsing | C.R.324/2003 | `(\w\.\w+\.+\d+/\d{4})` |
| case_type | case_number prefix | Civil Revision | Split on "." |
| judgment_date | PDF header | 16.03.2012 | `(\d{2}\.\d{2}\.\d{4})` |
| judges | PDF presiding section | Justice X, Justice Y | Split on "and" or ", " |
| bench_name | PDF location header | LAHORE | Uppercase location after "HIGH COURT" |
| appellant | Case header first party | Name A | First party mentioned |
| respondent | Case header second party | Name B | "vs" or "v." following party |

---

## SEARCH PARAMETERS (INFERRED)

### Known Parameters

```
?year=[YYYY]          # Filter by judgment year (2020-2024)
?page=[N]             # Pagination (default page size unknown)
?judge=[NAME]         # Filter by judge name (unconfirmed)
?bench=[LOCATION]     # Filter by bench (unconfirmed)
```

### Parameter Testing Strategy

```python
# Test pagination
urls = [
    f"...?year=2024&page=1",
    f"...?year=2024&page=2",
    # Detect max page
]

# Test filters
urls = [
    f"...?year=2024&judge=ASHTAR",
    f"...?year=2024&bench=MULTAN",
    # Reverse-engineer filter names
]
```

---

## CRAWLING STRATEGY

### Option A: Form-Based (Recommended)

```
1. Hit /reported_judgments/judgments_approved_for_reporting
2. Parse search form fields
3. Submit to /dynamic/approved_judgments_result_new.php
4. Parse HTML result table
5. Extract judgment links
6. Download PDFs (data.lhc.gov.pk or sys.lhc.gov.pk)
7. Parse PDF for structured data
```

### Option B: Direct Enumeration (Fallback)

```
For year in 2020..2024:
    For n in 1..5000:
        url = f"https://sys.lhc.gov.pk/appjudgments/{year}LHC{n}.pdf"
        Try:
            GET url
            Parse PDF if 200 OK
            Skip if 404 or 403
```

### Option C: Library Index (Validation)

```
1. Scrape library.lhc.gov.pk/Home/Compendium
2. Extract judge-specific judgment lists
3. Cross-reference against main DB
4. Identify missing/unreported judgments
```

---

## IMPLEMENTATION CHECKLIST

### Pre-Crawl Setup

- [ ] Verify connectivity from intended deployment server
- [ ] Test with VPN/proxy if Pakistan IP needed
- [ ] Obtain written permission from LHC IT department
- [ ] Document legal basis for data usage (copyright/fair use)
- [ ] Set User-Agent to identify your crawler
- [ ] Implement request logging for audit trail
- [ ] Set up error monitoring and alerting

### Connectivity Testing

```bash
# Test basic connectivity
curl -I --max-time 10 https://data.lhc.gov.pk/

# Test with browser-like headers
curl -I \
  -H "User-Agent: Mozilla/5.0..." \
  --max-time 10 \
  https://data.lhc.gov.pk/

# Test from Pakistan IP if available
ssh user@pakistan-server "curl -I https://data.lhc.gov.pk/"
```

### Data Extraction

```python
import requests
from bs4 import BeautifulSoup
import pdfplumber

# Pseudocode
def crawl_lhc_data():
    years = range(2020, 2025)

    for year in years:
        url = f"https://data.lhc.gov.pk/dynamic/approved_judgments_result_new.php?year={year}"

        # Fetch and parse
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract judgment rows
        judgments = soup.find_all('tr', class_='judgment-row')

        for judgment in judgments:
            case_num = judgment.find('td', class_='case_number').text
            pdf_link = judgment.find('a', class_='pdf')['href']

            # Download PDF
            pdf_response = requests.get(pdf_link)

            # Extract text
            with pdfplumber.open(pdf_response.content) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()

            # Parse structured fields
            data = parse_judgment_text(text)

            # Store
            save_to_database(data)
```

### PDF Parsing Libraries

```python
# Option 1: pdfplumber (recommended)
import pdfplumber
with pdfplumber.open("judgment.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()

# Option 2: PyPDF2
from PyPDF2 import PdfReader
reader = PdfReader("judgment.pdf")
text = reader.pages[0].extract_text()

# Option 3: Apache Tika (heavier but more robust)
from tika import parser
parsed = parser.from_file("judgment.pdf")
text = parsed["content"]
```

---

## FIELD PARSING PATTERNS

### Case Number Extraction

```python
import re

# Pattern: Court/Type + Number + Year
pattern = r'([A-Z]+\.?[A-Z]*\.?\s*[^/]*)/(\d{4})'
# Matches: C.R.324/2003, W.Ps.542/1995, Civil Revision No.100/2005

def extract_case_number(text):
    match = re.search(pattern, text)
    if match:
        return match.group(0)  # Returns full case number
    return None
```

### Judge Name Extraction

```python
# Look for "Passed by" or "Before" sections
judge_patterns = [
    r'Passed by\s+(.+?)(?:\.|,)',
    r'Before\s+(.+?)(?:\.|,)',
    r'Hon\'?ble?\s+(?:Mr\.|Mrs\.|Justice)\s+(.+?)(?:\.|,)',
]

def extract_judges(text):
    judges = []
    for pattern in judge_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        judges.extend(matches)
    return [j.strip() for j in judges if j]
```

### Date Extraction

```python
date_pattern = r'(\d{1,2})\.(\d{1,2})\.(\d{4})'  # DD.MM.YYYY
# Also handle: DD-MM-YYYY, DD/MM/YYYY

def parse_judgment_date(text):
    match = re.search(date_pattern, text)
    if match:
        day, month, year = match.groups()
        return f"{year}-{month}-{day}"  # Convert to ISO
    return None
```

---

## ERROR HANDLING

### Network Errors

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session_with_retries():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Usage
session = get_session_with_retries()
response = session.get(url, timeout=10)
```

### Rate Limiting

```python
import time
import threading

class RateLimiter:
    def __init__(self, requests_per_second=1):
        self.min_interval = 1.0 / requests_per_second
        self.last_request = 0
        self.lock = threading.Lock()

    def wait(self):
        with self.lock:
            elapsed = time.time() - self.last_request
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_request = time.time()

limiter = RateLimiter(requests_per_second=1)
```

### Timeout & Connection Issues

```python
try:
    response = requests.get(url, timeout=10)
except requests.Timeout:
    # Handle: Site unreachable (current issue)
    log.error(f"Timeout: {url}")
    retry_later()
except requests.ConnectionError:
    # Handle: Network unavailable
    log.error(f"Connection failed: {url}")
    retry_later()
except Exception as e:
    log.error(f"Unexpected error: {e}")
```

---

## DATA VALIDATION

### Deduplication

```python
def is_duplicate(case_number, judgment_date, existing_records):
    """Check if judgment already exists"""
    return any(
        r['case_number'] == case_number and
        r['judgment_date'] == judgment_date
        for r in existing_records
    )
```

### Field Validation

```python
def validate_judgment_record(record):
    """Validate extracted data"""
    required_fields = ['case_number', 'judgment_date', 'judges', 'bench_name']

    # Check required fields
    for field in required_fields:
        if not record.get(field):
            raise ValueError(f"Missing required field: {field}")

    # Validate date format
    if not re.match(r'\d{4}-\d{2}-\d{2}', record['judgment_date']):
        raise ValueError("Invalid date format")

    # Validate case number format
    if not re.match(r'[A-Z]+\.\w*\.?\s*\d+/\d{4}', record['case_number']):
        raise ValueError("Invalid case number format")

    return True
```

### Citation Format Validation

```python
# Standard Pakistan Law Report formats
valid_series = ['PLD', 'PLJ', 'SCMR', 'PLC', 'PTD', 'MLD', 'NLR', 'CLC', 'CLD']
citation_pattern = r'({series}) (\d{{4}}) (Lah|Kar|Isl|Pes|Khy) (\d+)'.format(
    series='|'.join(valid_series)
)
```

---

## DATABASE SCHEMA

### Minimal Schema

```sql
CREATE TABLE judgments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    case_number VARCHAR(50) NOT NULL UNIQUE,
    judgment_year INT,
    judgment_date DATE,
    judges JSON,  -- Array of judge names
    bench_name VARCHAR(50),
    appellant VARCHAR(255),
    respondent VARCHAR(255),
    case_type VARCHAR(100),
    reported_status VARCHAR(20),
    judge_category VARCHAR(20),
    full_text LONGTEXT,
    source_portal VARCHAR(50),
    pdf_url VARCHAR(500),
    crawl_timestamp DATETIME,
    FOREIGN KEY (judgment_year) REFERENCES judgment_years(year)
);

CREATE TABLE judgment_years (
    year INT PRIMARY KEY,
    total_count INT,
    crawled BOOLEAN,
    last_crawled DATETIME
);
```

### Search Indexes

```sql
CREATE INDEX idx_case_number ON judgments(case_number);
CREATE INDEX idx_judgment_date ON judgments(judgment_date);
CREATE INDEX idx_bench_name ON judgments(bench_name);
CREATE FULLTEXT INDEX idx_full_text ON judgments(full_text);
```

---

## MONITORING & HEALTH CHECKS

### Health Check Script

```python
def health_check_lhc_portals():
    """Daily health check"""
    portals = {
        'data.lhc.gov.pk': 'https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting',
        'sys.lhc.gov.pk': 'https://sys.lhc.gov.pk/appjudgments/2024LHC1.pdf',
        'library.lhc.gov.pk': 'https://library.lhc.gov.pk/Home/Compendium',
    }

    status = {}
    for name, url in portals.items():
        try:
            response = requests.head(url, timeout=10)
            status[name] = {'status': 'UP', 'code': response.status_code}
        except Exception as e:
            status[name] = {'status': 'DOWN', 'error': str(e)}

    return status
```

### Crawl Metrics

```python
metrics = {
    'total_judgments_crawled': 0,
    'successful_extractions': 0,
    'extraction_success_rate': 0.0,
    'average_pdf_size_kb': 0.0,
    'avg_extraction_time_ms': 0.0,
    'duplicate_records_found': 0,
    'validation_failures': 0,
    'last_update': None,
}
```

---

## ESTIMATED RESOURCE REQUIREMENTS

### Storage
```
Total Judgments: 4,078
Avg PDF Size: 500-1000 KB
Text Extraction: 200-400 KB per judgment
Total Storage Needed: 3-5 GB (with indexes)
```

### Computation
```
Crawl Time: ~10-20 seconds per judgment
Total Crawl Duration: 11-34 hours (non-parallel)
With parallel workers (4): 3-8 hours
PDF Parsing: 1-2 seconds per document
Total Processing: 2-3 hours
```

### Network
```
Requests per judgment: 2-3 (form + PDF + metadata)
Total Requests: 8,000-12,000
At 1 req/sec: 2-3 hours minimum
Bandwidth: ~2-4 GB download
```

---

## TROUBLESHOOTING

| Issue | Cause | Solution |
|-------|-------|----------|
| All sites timeout | IP blocking / ISP filtering | Use VPN/proxy, test from Pakistan IP |
| 403 Forbidden | Rate limiting / WAF block | Reduce request rate, add delays, change User-Agent |
| 404 on PDF URLs | Judgment numbering gaps | Implement error handling, skip missing |
| PDF extraction fails | Scanned documents / OCR required | Add Tesseract OCR, handle gracefully |
| HTML parsing fails | Page structure changed | Implement fallback parsing, monitor closely |
| Duplicate records | Same judgment from multiple sources | Implement deduplication by case number + date |

---

## DEPLOYMENT NOTES

1. **Test Environment**: Set up in staging first, confirm LHC site accessibility
2. **Rate Limiting**: Start with 1 request/second, monitor response
3. **Error Handling**: Implement comprehensive logging
4. **Data Backup**: Regular snapshots of extracted data
5. **Legal Review**: Confirm data usage rights before production
6. **Monitoring**: Daily health checks on portal availability
7. **Updates**: Plan for quarterly updates as new judgments added

