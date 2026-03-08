# Sindh High Court Legal Crawler - Technical Specification

**Document Purpose**: Exact data structures and implementation patterns for legal AI crawler

---

## Source Priority Matrix

```
TIER 1 - PRIMARY (Production Ready)
├─ cases.districtcourtssindh.gos.pk
│  ├─ Accessibility: 100%
│  ├─ Robots.txt: Allow all
│  ├─ Data Volume: 500K-2M cases
│  ├─ Crawl Complexity: Medium
│  └─ Recommended Start: YES

TIER 2 - SECONDARY (Medium Effort)
├─ digital.shc.gov.pk
│  ├─ Accessibility: 100%
│  ├─ Robots.txt: Allow all
│  ├─ Data Volume: 10K-50K cases
│  ├─ Crawl Complexity: High (reCAPTCHA)
│  └─ Recommended Start: After Tier 1

TIER 3 - INFORMATIONAL (Low Priority)
├─ sindhhighcourt.gov.pk
│  ├─ Data: Portal/announcements only
│  └─ Skip: Use other sources

TIER 4 - DEPRECATED (Avoid)
├─ cases.shc.gov.pk (Unreachable)
├─ caselaw.shc.gov.pk (Timeout)
└─ Status: Do not implement
```

---

## TIER 1: cases.districtcourtssindh.gos.pk Specification

### A. Entry Point & Navigation

**Base URL**: `https://cases.districtcourtssindh.gos.pk/case-search`

**Navigation Structure**:
```
GET https://cases.districtcourtssindh.gos.pk/
  └─ /case-search (main search interface)
  └─ /high-court-cases/list (high court specific)
  └─ /special-causelist (commercial litigation corridor)
  └─ /release-writs/home (writ search)
```

**Robots.txt**:
```
User-agent: *
Disallow:
```
✓ No restrictions. Full site crawlable.

### B. Search Form Structure

**Form Endpoint**: POST/GET `https://cases.districtcourtssindh.gos.pk/case-search`

**Required Parameters**:
```
district          : string (dropdown selection from list below)
year_from         : integer (YYYY format, optional)
year_to           : integer (YYYY format, optional)
court_type        : string (dropdown, default: "NIL-Default Court Type")
case_category     : string (dropdown, default: "All")
case_status       : string (enum: "Pending", "Disposal", "All")
```

### C. District/Location Enumeration

**Total Districts**: 27 + Karachi subdivisions (30 searchable locations)

**Complete List**:
```
KARACHI SUBDIVISIONS (5):
  "Karachi (South)"
  "Karachi (West)"
  "Karachi (East)"
  "Karachi (Central)"
  "Karachi (Malir)"

SINDH DISTRICTS (22):
  "Hyderabad"
  "Thatta"
  "Badin"
  "Dadu"
  "Jamshoro @ Kotri"
  "Tharparkar @ Mithi"
  "Mirpurkhas"
  "Umerkot"
  "Sanghar"
  "Naushahro Feroze"
  "Shaheed Benazirabad"
  "Sukkur"
  "Khairpur"
  "Ghotki"
  "Larkana"
  "KAMBER-SHAHDADKOT @ KAMBER"
  "Shikarpur"
  "Jacobabad"
  "Kashmore @ Kandhkot"
  "Tando Allahyar"
  "Tando Muhammad Khan"
  "Matiari"
  "Sujawal"
```

**Crawler Loop Strategy**:
```python
districts = [
  "Karachi (South)", "Karachi (West)", "Karachi (East)",
  "Karachi (Central)", "Karachi (Malir)",
  "Hyderabad", "Thatta", "Badin", "Dadu", "Jamshoro @ Kotri",
  # ... (23 more)
  "Sujawal"
]

for district in districts:
    for year in range(2000, 2026):
        for case_status in ["Pending", "Disposal", "All"]:
            search(district, year_from=year, year_to=year, case_status)
            sleep(2)  # Rate limiting
```

### D. Court Type Enumeration

**Total Options**: 19 main court types (hierarchical structure)

```
BASIC COURTS:
  "District Courts"
  "Anti-Terrorism Courts"
  "Anti-Corruption Courts"
  "Banking Courts"
  "Labour Courts"

SPECIALIZED COURTS:
  "Special Court (CNS)"
  "Special Court (Offence in Banks)"
  "Special Court Commercial"

TRIBUNALS & APPELLATE:
  "Appellate Tribunal Sindh Revenue Board"
  "Environmental Protection Tribunal"
  "Accountability Courts"
  "Insurance Tribunal"
  "Foreign Exchange Appellate Tribunal"
  "Federal Service Tribunal"
  "Intellectual Property Tribunal"
  "Appellate Tribunal Local Councils Sindh"
  "Consumer Protection Court"
  "Commercial Courts (Magistrate)"
  "Custom, Taxation & Anti Smuggling Court"
  "Customs, Excise & Sales Tax Appellate Tribunal"
  "Removal of Anti Encroachment"
  "Drug Court"
  "Gas Theft"
```

### E. Case Category Enumeration

**Total Categories**: 250+ (hierarchical by court type)

**Sample Structure** (by frequency):
```
CRIMINAL CASES (Most Common):
  "PPC" (Penal Code)
  "Criminal Appeals"
  "Criminal Bail Application"
  "Criminal Petition U/S 22-A"
  "Habeas Corpus"
  "Criminal Reference"
  "Arms Ordinance" (Multiple: 13-A, 13-D, 13-E, 16-B, 23, 24-A, 25-A)
  "Anti-Terrorism Act 1997"
  "Special Cases (S.T.A)"
  "Money Laundering"
  "Terror Financing"
  "Dacoity/Robbery"
  "Kidnapping" (Various types)
  "Bomb blast"
  "Bhatta Ransom"

CIVIL CASES (Common):
  "Small Causes"
  "Ist Class Civil Suits"
  "IInd Class Civil Suits"
  "IIIrd Class Civil Suits"
  "Civil Appeals"
  "Civil Executions"
  "Civil Revisions"
  "Civil Misc. Applications"
  "Rent Cases"
  "First Rent Appeals (F.R.A.)"
  "Land Acquisition Applications"
  "Election Appeals"
  "Election Petitions"

FAMILY CASES:
  "Family Suits"
  "Family Appeals"
  "Family Executions"
  "Dissolution of Muslim Marriages Act, 1939"
  "G&W Cases" (Guardianship & Wards)

SPECIALIZED:
  "Commercial Litigation Corridor (CLC)"
  "Banking Court Cases"
  "IP Tribunal Cases"
  "Labour Matters"
  "Environmental Cases"
  "Intellectual Property"

WRIT PETITIONS:
  "Human Rights Petition"
  "Constitutional Petitions"
  "Habeas Corpus" (listed separately)
```

**Crawling Strategy for Categories**:
- Default to "All" for initial crawl (easiest)
- Run category-specific crawls for legal AI training (higher quality filtering)

### F. Search Results Table Structure

**Table Endpoint**: Form submission returns HTML table

**Result Table Format**:
```
<table>
  <thead>
    <tr>
      <th>S.No</th>
      <th>Case No</th>
      <th>Court Name</th>
      <th>Status</th>
      <th>Hearing Date</th>
      <th>Action</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Criminal Bail Application 2020/2024, Shehzad Ghulam Hussain son of Ghulam Hussain V/S The State</td>
      <td>Additional District & Sessions Judge XI, Karachi (South)</td>
      <td>Disposed 04/Jul/2024</td>
      <td>04/Jul/2024</td>
      <td>
        <button onclick="viewCase(...)">View</button>
        OR
        "NOT FOUND" (text)
      </td>
    </tr>
    <!-- More rows -->
  </tbody>
</table>
```

**Data Extraction Pattern**:
```python
# For each row in results table:
row = {
    "s_no": cell_0_text,
    "case_no": cell_1_text,              # EXTRACT: All case details
    "court_name": cell_2_text,           # EXTRACT: Bench location
    "status": cell_3_text,               # EXTRACT: Status & date
    "hearing_date": cell_4_text,         # EXTRACT: Next hearing
    "action_url": cell_5_button_onclick, # EXTRACT: Case detail link (if exists)
    "case_available": cell_5_text != "NOT FOUND"
}

# Parse case_no field for details:
pattern = r"(\w+)\s+(\d{4})/(\d{4}),\s+(.+?)\s+V/S\s+(.+)"
match = re.search(pattern, row["case_no"])
if match:
    case_type, year_filed, year_current, plaintiff, defendant = match.groups()
```

### G. Case Detail Page Structure

**Detail URL Pattern**:
- Not directly visible in search results
- "NOT FOUND" text indicates page doesn't exist in database
- When available: Click "Action" button returns case details

**Expected Detail Page Fields** (when available):
```
Case Information:
  - Case Number (full)
  - Case Type
  - Year Filed
  - Court Jurisdiction
  - Judge Name
  - Court Location/Bench

Parties:
  - Plaintiff/Petitioner Name(s)
  - Plaintiff Address
  - Defendant/Respondent Name(s)
  - Defendant Address
  - Counsel Names (if available)

Case Details:
  - FIR Number (criminal cases)
  - Statement of Facts
  - Charges/Claims
  - Pleas/Defenses
  - Evidence Summary

Orders/Judgment:
  - Hearing Dates
  - Interim Orders
  - Final Judgment/Disposal Date
  - Judge's Findings
  - Judgment Text (if digitized)

Case Status:
  - Current Status (Pending/Disposed)
  - Last Updated Date
  - Next Hearing Date (if pending)
```

### H. Pagination Strategy

**Observation**: Not visible in initial snapshots, but likely present

**Expected Pagination**:
- Search results return 10-20 cases per page
- Pagination controls appear at bottom of table
- Standard patterns: "Next", "Previous", page numbers, or "Load More"

**Crawler Approach**:
```python
# After initial search, check for pagination
def handle_pagination(page_html):
    # Look for:
    # - Next button (class: 'pagination-next', 'next-page', etc.)
    # - Page numbers
    # - "Load More" button
    # - Pagination info: "Showing 1-20 of 500"

    next_page_url = extract_next_page_link(page_html)
    while next_page_url:
        results.extend(parse_results(fetch(next_page_url)))
        sleep(1)  # Rate limit
        next_page_url = extract_next_page_link(last_response)
```

### I. Data Quality & Anomalies

**Known Issues**:
1. **Incomplete Digitization**: 80% of cases return "NOT FOUND" on detail page
2. **Party Names**: May contain Urdu characters (Unicode handling required)
3. **Court Names**: Format varies (e.g., "Additional District & Sessions Judge XI" vs variations)
4. **Date Parsing**: Multiple formats observed (DD/Mon/YYYY, YYYY-MM-DD)
5. **Duplicate Cases**: Same case may appear in multiple districts (concurrent jurisdiction)

**Handling Strategy**:
```python
# Character encoding
response.encoding = 'utf-8'
case_data = {
    'plaintiff': clean_unicode(plaintiff_text),
    'defendant': clean_unicode(defendant_text)
}

# Date parsing
import dateutil.parser
hearing_date = dateutil.parser.parse(hearing_date_string)

# Deduplication
case_id = hashlib.md5(
    f"{case_no}|{court_name}|{year_filed}".encode()
).hexdigest()
```

### J. Crawl4AI Configuration

**Crawl4AI Strategy Block**:
```yaml
strategy:
  type: "form-based"
  crawl_delay: 2  # seconds between requests
  rate_limit:
    per_minute: 30
    per_hour: 1000

  search_patterns:
    - district: [all 27]
    - year_from: [2000-2025]
    - case_status: ["All", "Pending", "Disposal"]
    - case_category: ["All"]  # Start with "All", expand if needed

  extraction:
    - selector: "table tbody tr"
      fields:
        - s_no: "td:nth-child(1)"
        - case_no: "td:nth-child(2)"
        - court_name: "td:nth-child(3)"
        - status: "td:nth-child(4)"
        - hearing_date: "td:nth-child(5)"
        - detail_link: "td:nth-child(6) button@onclick"

  pagination:
    - detect: "next_page_link"
    - follow: true
    - max_pages: unlimited
    - wait_between_pages: 2000  # milliseconds

error_handling:
  - retry_failed: true
  - retry_count: 3
  - skip_not_found: true
  - log_failures: true
```

### K. Expected Data Volume

**Estimation**:
- **Total Records**: 500,000 - 2,000,000 cases
- **By Scope**:
  - Karachi alone: ~100,000 cases/year × 10-20 years = 1,000,000+
  - All 27 districts: 2,000,000+ cases (conservative)
- **Digitized Judgments**: 10% available = 50,000-100,000 PDFs
- **Crawl Time**: 100-200 hours for complete extraction (with 2-sec delays)

**Storage Requirements**:
- Metadata only: ~500 MB (JSON records)
- With PDFs: 50-200 GB (assuming avg 2-5 MB per PDF)
- Database (SQLite/PostgreSQL): 1-2 GB

---

## TIER 2: digital.shc.gov.pk Specification

### A. Entry Point

**Base URL**: `https://digital.shc.gov.pk/`

**Robots.txt**:
```
User-agent: *
Disallow:
```
✓ Fully crawlable

**Navigation**:
```
GET https://digital.shc.gov.pk/
  └─ /search-citation (citation-based case law search)
  └─ /advocate/register (registration - skip)
  └─ /login (authentication - skip public crawl)
```

### B. Citation Search Form

**Endpoint**: POST `https://digital.shc.gov.pk/search-citation`

**Form Fields**:
```
citation_year : string (YYYY, required)
journal        : string (dropdown, required)
journal_part   : string (dropdown, depends on journal, optional)
page_no        : string (integer, optional)
```

**Journal Options** (21 total):
```
SHC             - Sindh High Court Reports
PLD             - Pakistan Legal Decisions
SCMR            - Supreme Court Monthly Review
CLC             - Commercial Law Cases
PCr.LJ          - Pakistan Criminal Law Journal
PTD             - Pakistan Tax Decisions
PLC             - Pakistan Law Cases
CLD             - Constitutional Law Decisions
YLR             - Yearly Law Reports
OTHER           - Miscellaneous journals

SBLR            - Sindh Bar Law Reports
MLD             - Muslim Law Decisions
PSC             - Pakistan Supreme Court
TAX             - Tax Reports
NLR             - National Law Reports
AC              - Appeals Cases
CLJ             - Commercial Law Journal
SD              - Sindh Digest
TD              - Tax Digest
UC              - Unreported Cases
PLJ             - Pakistan Law Journal

SLJ, SLR        - Sindh Law Reports
PCr.R           - Pakistan Criminal Reports
PTCL            - Pakistan Telecom Law
PLC (CS)        - PLC Computer Science
```

### C. Search Strategy

**Challenge**: Citation-based search requires knowing case citation in advance

**Possible Crawler Approaches**:

**Option 1 - Brute Force** (Recommended):
```python
journals = ["SHC", "PLD", "SCMR", "CLC", ...]
years = range(2000, 2026)
page_ranges = range(1, 5000)  # Estimate max pages per journal per year

for journal in journals:
    for year in years:
        for page in page_ranges:
            search_params = {
                'citation_year': year,
                'journal': journal,
                'page_no': page
            }
            result = search(search_params)
            if result.has_data:
                extract_case(result)
            else:
                break  # No more pages for this journal/year
            sleep(2)  # Rate limit
```

**Option 2 - Intelligent Extraction**:
```python
# From Tier 1 results, extract citations
for case in tier1_results:
    if case.has_citation:
        citation = parse_citation(case.citation)
        search(citation.year, citation.journal, citation.page)
        sleep(2)
```

### D. Search Results Structure

**Expected Result Format** (citation lookup):
```
Case Citation:
  Year: 2023
  Journal: SHC (Sindh High Court)
  Page: 152

Case Information:
  Title: Plaintiff v/s Defendant
  Case Number: [Full case ID]
  Judge: Hon'ble Justice [Name]
  Judgment Date: DD/MM/YYYY

Full Text: [HTML or PDF link]
PDF Download: [Direct link to PDF]
```

### E. reCAPTCHA Handling

**Observed**: reCAPTCHA v3/v2 present on page (iframe element detected)

**Mitigation Strategies**:
1. **reCAPTCHA Solver Service**:
   - 2Captcha (https://2captcha.com) - $0.001-0.003 per solve
   - Anti-Captcha (https://anti-captcha.com)
   - CapMonster (https://capmonster.cloud)

2. **Request Patterns**:
   - Space requests 5+ seconds apart
   - Rotate user agents
   - Vary request origins (rotating proxies)
   - Implement exponential backoff on CAPTCHA triggers

3. **Code Example**:
```python
from crawl4ai import AsyncWebCrawler
from twocaptcha import TwoCaptcha

async def search_with_captcha(search_params):
    async with AsyncWebCrawler() as crawler:
        # Initial request
        response = await crawler.arun(
            url="https://digital.shc.gov.pk/search-citation",
            bypass_cache=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

        # If CAPTCHA detected
        if "g-recaptcha" in response.html:
            # Solve CAPTCHA
            solver = TwoCaptcha(apikey="YOUR_KEY")
            result = solver.recaptcha(
                sitekey="6LE...",
                url="https://digital.shc.gov.pk/search-citation"
            )

            # Submit form with token
            await crawler.arun(
                url="https://digital.shc.gov.pk/search-citation",
                method="POST",
                data={
                    **search_params,
                    'g-recaptcha-response': result
                }
            )
```

### F. Data Quality

**Expected High-Quality Data**:
- Curated legal citations (published judgments)
- Complete judgment text (PDFs)
- Standardized metadata
- Judge names and dates verified

**Limitations**:
- Smaller dataset (10,000-50,000 vs. 500,000+ in Tier 1)
- Citation-based search less convenient than full-text search
- Published judgments only (not all cases)

---

## TIER 3: sindhhighcourt.gov.pk Specification

**Purpose**: Informational/Portal only

**Low Priority**: Skip unless needed for court announcements or structural information

**Robots.txt Restriction**:
```
User-agent: *
Disallow: /causelist/
```

**Crawlable Content**:
- Court structure and jurisdiction
- Contact information
- Judicial appointments
- Court announcements
- Links to subdomains (Tier 1 & Tier 2)

**Not Recommended for Case Extraction**

---

## Implementation Roadmap

### Phase 1: Tier 1 Foundation (Weeks 1-4)
```
Week 1: Setup & Testing
  - Deploy Crawl4AI environment
  - Test single district (Karachi South) search
  - Validate data extraction patterns
  - Test pagination handling

Week 2: Scale Preparation
  - Implement district loop
  - Add rate limiting (2-sec delays)
  - Setup data storage (SQLite/PostgreSQL)
  - Implement deduplication logic

Week 3: Full Crawl Execution
  - Execute crawl all 27 districts
  - Monitor for errors/blocks
  - Log progress checkpoints
  - Validate data completeness

Week 4: Data Validation & QA
  - Verify record counts
  - Check for duplicates
  - Validate field extraction
  - Generate metrics report

Output: 300,000-500,000 case metadata records
```

### Phase 2: Tier 2 Integration (Weeks 5-6)
```
Week 5: Citation Search
  - Implement journal enumeration
  - Setup reCAPTCHA solver
  - Test citation search pattern
  - Handle pagination

Week 6: Full Citation Crawl
  - Execute brute-force citation search (10K-50K cases)
  - Cross-reference with Tier 1 results
  - Download available PDFs
  - Merge datasets

Output: 10,000-50,000 published judgments with full text
```

### Phase 3: PDF Extraction & Indexing (Weeks 7-8)
```
Week 7: PDF Download & Storage
  - Download all available PDFs from Tier 1 & 2
  - Implement resume/retry logic
  - Estimate: 50-200 GB storage

Week 8: OCR & Indexing
  - Extract text from PDFs
  - Generate full-text search index
  - Create embeddings for semantic search

Output: Indexed legal documents ready for AI/NLP processing
```

---

## Deployment Configuration

### Docker Compose Setup

```yaml
version: '3.8'
services:
  crawler:
    image: crawl4ai:latest
    environment:
      - CRAWL_DELAY=2
      - RATE_LIMIT_PER_MINUTE=30
      - MAX_WORKERS=5
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    networks:
      - legal_crawler_network

  database:
    image: postgres:15
    environment:
      - POSTGRES_DB=sindh_courts
      - POSTGRES_USER=crawler
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - ./db_data:/var/lib/postgresql/data
    networks:
      - legal_crawler_network

  storage:
    image: minio:latest
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    volumes:
      - ./minio_data:/data
    networks:
      - legal_crawler_network

networks:
  legal_crawler_network:
    driver: bridge
```

### Environment Variables

```
# Crawl Configuration
CRAWL_DELAY_SECONDS=2
RATE_LIMIT_PER_MINUTE=30
MAX_CONCURRENT_REQUESTS=5
RETRY_ATTEMPTS=3
TIMEOUT_SECONDS=30

# Database
DATABASE_URL=postgresql://crawler:password@database:5432/sindh_courts
DATABASE_POOL_SIZE=10

# Storage
MINIO_ENDPOINT=storage:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=sindh-court-documents

# reCAPTCHA (Tier 2)
TWOCAPTCHA_API_KEY=your_api_key
CAPTCHA_THRESHOLD_DELAY=10  # seconds

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/crawler.log
```

---

## Testing Checklist

- [ ] Single district search returns results
- [ ] Pagination handled correctly
- [ ] Table parsing extracts all fields
- [ ] Unicode/Urdu characters handled
- [ ] Case number parsing works
- [ ] Date parsing handles format variations
- [ ] Duplicate detection operational
- [ ] Rate limiting (2-sec delays) enforced
- [ ] Error handling for "NOT FOUND" cases
- [ ] Resume capability from checkpoint
- [ ] Data validation (required fields present)
- [ ] Performance monitoring (requests/hour, records/hour)

---

## Monitoring & Metrics

**Key Metrics to Track**:
```
- Cases extracted per hour
- Error rate (%)
- Duplicate rate (%)
- Crawl completion percentage
- Storage used (GB)
- Requests per minute (actual vs. target)
- Average response time
- CAPTCHA solve rate (Tier 2)
```

**Alerting Thresholds**:
- Error rate > 10% → Investigate
- Crawl stall > 1 hour → Restart
- IP block detected → Pause, wait 24h, retry
- CAPTCHA solve failure rate > 20% → Review solver config

---

## Legal & Ethical Considerations

1. **Terms of Service**: Courts typically allow public access; verify local jurisdiction
2. **Rate Limiting**: Respect server capacity (2-sec delays, max 30 req/min)
3. **Attribution**: Cite Sindh High Court as data source
4. **Data Protection**: Handle party names with care (privacy compliance)
5. **No Commercial Redistribution**: For internal/research use only

---

**Document Version**: 1.0
**Last Updated**: March 8, 2026
**Next Review**: Upon implementation start
