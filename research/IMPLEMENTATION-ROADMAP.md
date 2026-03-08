# Pakistan Legislative Crawler - Implementation Roadmap

## Visual Overview

### Source Hierarchy
```
┌─────────────────────────────────────────────────────────────┐
│         PAKISTAN LEGISLATIVE DATA SOURCES                    │
└─────────────────────────────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
    │ Federal │      │Provincial│     │ Judicial│
    └────┬────┘      └────┬────┘      └────┬────┘
         │                 │                 │
    ┌────┴─────┐    ┌──────┴──────┐    ┌───┴───┐
    │           │    │             │    │       │
┌───▼──┐  ┌────▼┐ ┌─▼──┐ ┌──┐ ┌──┐ └─▼──┐ └───▼───┐
│  NA  │  │Senate│ │Pun.│ │Sin│ │KPK│ │Fed│ │District│
└───┬──┘  └────┬┘ │ Asm│ │dh │ │Asm│ │Crt│ │ Courts │
    │          │  └─┬──┘ └──┬┘ └──┬┘ └───┘ └───────┘
    │          │    │       │    │
    └──────────┴────┴───────┴────┘
              │
    ┌─────────▼──────────┐
    │ AGGREGATOR: Open   │
    │ Parliament PK      │
    └────────────────────┘
```

## Implementation Phases

### PHASE 1: Foundation (Week 1-2)
```
┌─────────────────────────────────────┐
│ MVP: National Assembly Crawler      │
├─────────────────────────────────────┤
│ ✓ Setup Python project structure    │
│ ✓ Create database schema            │
│ ✓ Build HTML parser (BeautifulSoup) │
│ ✓ Implement PDF extractor           │
│ ✓ Add rate limiter (2s delays)      │
│ ✓ Write unit tests                  │
│ ✓ Validate on 20 sample bills       │
└─────────────────────────────────────┘
  OUTPUT: 2000+ bills in database
```

### PHASE 2: Expansion (Week 3-4)
```
┌──────────────────────────────────┐
│ Federal + Provincial Crawlers    │
├──────────────────────────────────┤
│ + Senate crawler                 │
│ + Punjab Assembly crawler        │
│ + Sindh Assembly crawler         │
│ + KPK Assembly crawler           │
│ + Balochistan Assembly crawler   │
│ + Cross-validation with Open     │
│   Parliament Pakistan            │
└──────────────────────────────────┘
  OUTPUT: 2500+ bills + acts
```

### PHASE 3: Polish (Week 5-6)
```
┌──────────────────────────────────┐
│ Production Hardening             │
├──────────────────────────────────┤
│ + Change detection system        │
│ + Scheduled crawling (Celery)    │
│ + Error monitoring & alerting    │
│ + API endpoint (FastAPI)         │
│ + Documentation                  │
│ + Performance optimization       │
└──────────────────────────────────┘
  OUTPUT: Production-ready system
```

## Data Flow Architecture

```
┌────────────────────────────────────────────────────────────┐
│                   CRAWLER ORCHESTRATOR                     │
└────────────────────────────────────────────────────────────┘
                           │
     ┌─────────────────────┼─────────────────────┐
     │                     │                     │
┌────▼───┐           ┌─────▼─────┐         ┌───▼────┐
│  URL   │           │  FETCHER  │         │ RATE   │
│QUEUE   │──────────▶│ (requests)│────────▶│LIMITER │
└────────┘           └─────┬─────┘         └────────┘
                           │
                      ┌────▼────┐
                      │ PARSER  │
                      │(BS4/    │
                      │Selenium)│
                      └────┬────┘
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
┌─────▼─────┐    ┌────────▼────────┐    ┌─────▼─────┐
│HTML        │    │PDF EXTRACTOR   │    │DATA       │
│EXTRACTOR   │    │(pdfplumber/    │    │NORMALIZER │
│            │    │pytesseract)    │    │           │
└─────┬─────┘    └────────┬────────┘    └─────┬─────┘
      │                   │                    │
      └───────────────────┼────────────────────┘
                          │
                    ┌─────▼──────┐
                    │VALIDATION  │
                    │(dedup,     │
                    │quality     │
                    │check)      │
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │ DATABASE   │
                    │(PostgreSQL)│
                    └────────────┘
```

## Database Schema (Simplified)

```
TABLE: bills
┌─────────────────────────────────┐
│ id (UUID)                       │ ◄──── Primary Key
│ source (varchar)                │ ◄──── 'NA', 'Senate', 'PA', etc.
│ bill_number (varchar) UNIQUE    │ ◄──── '91 of 2025'
│ title (text)                    │ ◄──── Bill title
│ date_introduced (date)          │ ◄──── When introduced
│ bill_type (enum)                │ ◄──── Government/Private/Amendment
│ status (varchar)                │ ◄──── Passed/Pending/Referred
│ mover (varchar)                 │ ◄──── Sponsor name
│ full_text (text)                │ ◄──── Extracted from PDF
│ source_url (text)               │ ◄──── Original source
│ document_url (text)             │ ◄──── PDF/HTML link
│ crawled_at (timestamp)          │ ◄──── When we crawled
│ updated_at (timestamp)          │ ◄──── Last update
│ data_quality_score (float)      │ ◄──── 0.0-1.0
└─────────────────────────────────┘

INDEXES:
- source + bill_number (unique)
- source + date_introduced
- status
- crawled_at
```

## Technology Stack

### Core Components
```
Web Framework: FastAPI          (for API)
Crawler: requests + bs4         (HTTP + parsing)
PDF: pdfplumber + pytesseract   (extraction + OCR)
DB: PostgreSQL + SQLAlchemy     (storage)
Task Queue: Celery + Redis      (scheduling)
Testing: pytest                 (validation)
```

### Deployment
```
Containerization: Docker
Orchestration: Docker Compose (dev) / Kubernetes (prod)
Monitoring: Prometheus + Grafana
Logging: ELK Stack
CI/CD: GitHub Actions
```

## Crawler Configuration Examples

### Conservative (Safe)
```yaml
rate_limit_seconds: 3
timeout: 15
retries: 5
backoff_factor: 2
concurrent_connections: 1
```

### Balanced (Recommended)
```yaml
rate_limit_seconds: 2
timeout: 10
retries: 3
backoff_factor: 2
concurrent_connections: 1
```

### Aggressive (Only for private servers)
```yaml
rate_limit_seconds: 1
timeout: 8
retries: 2
backoff_factor: 2
concurrent_connections: 2
```

## Quality Assurance Checklist

```
DATA EXTRACTION
├── ✓ Bill numbers match source format
├── ✓ Titles are non-empty (>5 chars)
├── ✓ Dates are valid and within parliament session
├── ✓ Types are valid enum values
├── ✓ Status matches known states
├── ✓ URLs are accessible
└── ✓ PDFs download successfully

TEXT QUALITY
├── ✓ Full text > 500 characters
├── ✓ No excessive special characters
├── ✓ Common words present (bill, act, section, etc.)
├── ✓ Sentence structure intact
└── ✓ OCR confidence > 85% (if OCR'd)

DEDUPLICATION
├── ✓ No duplicate bill_numbers per source
├── ✓ Cross-source duplicates identified
├── ✓ Merge candidates reviewed manually
└── ✓ Source attribution preserved

COVERAGE
├── ✓ All expected sources present
├── ✓ All sessions represented
├── ✓ No large gaps in years
├── ✓ Historical archives complete
└── ✓ Recent bills within 48 hours
```

## Monitoring Dashboard

```
┌─────────────────────────────────────────────────┐
│           CRAWLER HEALTH DASHBOARD              │
├─────────────────────────────────────────────────┤
│                                                 │
│  Total Bills Crawled: 2,547 ▓▓▓▓▓▓▓▓░░░       │
│  Success Rate: 98.5% ▓▓▓▓▓▓▓▓▓▓░░░░░░         │
│                                                 │
│  Last Crawl: 2 hours ago                       │
│  Next Crawl: in 4 hours                        │
│                                                 │
│  Errors (24h): 12 (timeout: 8, parse: 4)     │
│  Retry Success: 91.7%                          │
│                                                 │
│  Database Size: 4.2 GB                         │
│  Average Extract Time: 2.3 sec/bill            │
│                                                 │
│  Sources:                                      │
│  ├─ National Assembly: 850/850 ✓              │
│  ├─ Senate: 620/620 ✓                         │
│  ├─ Punjab: 450/450 ✓                         │
│  ├─ Sindh: 280/280 ✓                          │
│  ├─ KPK: 210/210 ✓                            │
│  └─ Balochistan: 147/147 ✓                    │
│                                                 │
│  Alerts: 0 Critical, 0 Warning                │
└─────────────────────────────────────────────────┘
```

## Crawler Execution Timeline

```
Day 1:   National Assembly init crawl    → 850 bills
Day 2:   Senate init crawl                → 620 bills
Day 3-4: Punjab Assembly init crawl       → 450 bills
Day 5:   Sindh Assembly init crawl        → 280 bills
Day 6:   KPK Assembly init crawl          → 210 bills
Day 7:   Balochistan Assembly crawl       → 147 bills
Day 8:   Open Parliament validation       → Cross-check
Day 9:   Re-run any failed extractions    → Fix issues
Day 10:  Full data validation             → QA check
Day 11:  Setup scheduled updates          → Daily/Weekly
Day 12:  Setup monitoring & alerting      → Production ready
Day 13:  Documentation & hand-off         → Complete

TOTAL: 2,557 legislative documents
```

## File Structure Template

```
pakistan-legislative-crawler/
├── README.md
├── requirements.txt
├── setup.py
├── .env.example
├── docker-compose.yml
├── Dockerfile
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py                    # Source configurations
│   ├── models.py                    # SQLAlchemy models
│   ├── database.py                  # DB connection
│   │
│   ├── crawlers/
│   │   ├── __init__.py
│   │   ├── base.py                  # Base crawler class
│   │   ├── national_assembly.py
│   │   ├── senate.py
│   │   ├── provincial.py
│   │   └── open_parliament.py
│   │
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── html_extractor.py        # Parse bill listings
│   │   ├── pdf_extractor.py         # Extract bill text
│   │   └── validator.py             # Data validation
│   │
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── celery_app.py            # Celery config
│   │   ├── tasks.py                 # Crawl tasks
│   │   └── scheduler.py             # Cron jobs
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app
│   │   └── routes/
│   │       ├── bills.py             # GET /api/bills
│   │       ├── search.py            # GET /api/search
│   │       └── stats.py             # GET /api/stats
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       ├── rate_limiter.py
│       ├── pdf_downloader.py
│       └── deduplicator.py
│
├── tests/
│   ├── __init__.py
│   ├── test_extractors.py
│   ├── test_crawlers.py
│   ├── test_models.py
│   └── fixtures/
│       ├── sample_bills.html
│       └── sample_bill.pdf
│
├── docs/
│   ├── architecture.md
│   ├── api_spec.md
│   ├── deployment.md
│   └── troubleshooting.md
│
└── scripts/
    ├── init_db.py                   # Create tables
    ├── migrate_db.py                # Schema migrations
    ├── validate_data.py             # Data quality check
    └── export_csv.py                # Bulk export
```

## Success Criteria

### MVP (Week 2)
- ✓ National Assembly crawler working
- ✓ 850 bills extracted and stored
- ✓ 98%+ extraction accuracy
- ✓ PDF download working
- ✓ Basic tests passing

### Phase 2 (Week 4)
- ✓ All federal + provincial crawlers working
- ✓ 2,500+ bills in database
- ✓ Open Parliament validation complete
- ✓ Deduplication working
- ✓ API endpoint functional

### Production (Week 6)
- ✓ Scheduled crawling running
- ✓ Change detection working
- ✓ Monitoring & alerting active
- ✓ Zero manual interventions (auto-recovery)
- ✓ 99.5%+ uptime
- ✓ <1% failure rate

---

**Ready to start?** Begin with Phase 1: MVP Implementation

**Files needed:**
1. pakistani-legislative-sources-verification.md
2. pakistan-crawler-technical-specs.md
3. pakistan-sources-quick-reference.md
4. VERIFICATION-SUMMARY.md

**Next step**: Verify robots.txt and review Terms of Service
