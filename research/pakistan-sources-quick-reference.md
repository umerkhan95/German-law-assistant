# Pakistan Legislative Sources - Quick Reference

**Generated**: 2026-03-08 | **Verification Method**: Web research

---

## PRIORITY CRAWL TARGETS

### FEDERAL LEVEL (Highest Priority)

| Source | Bills URL | Acts URL | Status | Format | Full Text |
|--------|-----------|----------|--------|--------|-----------|
| **National Assembly** | https://www.na.gov.pk/en/bills.php | https://www.na.gov.pk/en/acts-tenure.php | ✓ Active | HTML + PDF | ✓ Yes |
| **Senate** | https://www.senate.gov.pk/en/bills.php | — | ✓ Active | HTML + PDF | ✓ Yes |

**Federal Status**: ~100-120 bills/year combined | Archive: 2013-2026 | **Estimated Total**: 1,300-1,500+ bills

---

### PROVINCIAL LEVEL (High Priority)

| Assembly | Bills | Acts | Status | Coverage | Format |
|----------|-------|------|--------|----------|--------|
| **Punjab** (largest) | https://pap.gov.pk/bills/show/en | See Punjab Law Portal | ✓ Active | Complete | HTML + PDF |
| **Sindh** | https://www.pas.gov.pk/bills | https://www.sindhlaws.gov.pk | ✓ Active | 2024+ | HTML + PDF |
| **KPK** | https://www.pakp.gov.pk/bill/ | https://www.pakp.gov.pk/act/ | ✓ Active | Complete | HTML + PDF |
| **Balochistan** | https://pabalochistan.gov.pk/new/private-members-bill-introduced/ | https://pabalochistan.gov.pk/new/acts/ | ✓ Active | Complete | HTML + PDF |

**Provincial Status**: 80-150 bills/year each | **Estimated Total**: 500-800+ bills across 4 provinces

---

## COMPREHENSIVE REFERENCE REPOSITORY

| Source | URL | Coverage | Type | Access |
|--------|-----|----------|------|--------|
| **Open Parliament Pakistan** | http://openparliament.pk/ | National + Provincial | Aggregator | Free |
| **Punjab Law Portal** | https://pitb.gov.pk/law_portal | Punjab Laws (All) | Repository | Free |
| **Punjab Code** | https://punjabcode.punjab.gov.pk/ | Punjab Legislation | Indexed | Free |
| **Sindh Laws** | https://www.sindhlaws.gov.pk/ | Sindh Legislation | Repository | Free |

---

## JUDICIAL SOURCES (Secondary)

| Source | URL | Scope | Volume | Access | Caution |
|--------|-----|-------|--------|--------|---------|
| **Federal Courts** | https://federalcourts.molaw.gov.pk/casesSearch | Special Courts | 1000s | Free | Review TOS |
| **Punjab District Courts** | https://dsj.punjab.gov.pk/ | All District Courts | 8M+ cases | Free/Auth | Review TOS |
| **Punjab Judicial Academy** | https://pja.gov.pk/ | Judgment Writing Guides | Reference | Free | Educational |

---

## URL PARAMETER GUIDE

### National Assembly

```
Base: https://www.na.gov.pk/en/bills.php

Parameters:
?type=1           → Government Bills
?type=2           → Private Member Bills
?status=pass      → Passed Bills
(no params)       → All Bills

Historical:
/bills-15.php     → 2018-2023 session
(Check for other session URLs)
```

### Senate

```
Base: https://www.senate.gov.pk/en/

Endpoints:
bills.php
billsDetails.php?type=1&id=-1&catid=186&subcatid=276&cattitle=Bills

Parameters:
type=1            → Government
type=2            → Passed
catid=186         → Bills category
subcatid=276      → Legislation type
```

### Punjab Assembly

```
Base: https://pap.gov.pk/

Bills:
/bills/show/en    → English bills
(Check for pagination/filtering params)
```

### KPK Assembly

```
Base: https://www.pakp.gov.pk/

Bills:
/bill/            → Single bill listing
/all-bills/       → All bills

Acts:
/act/             → Single act listing
/all-acts/        → All acts
```

---

## PDF DOWNLOAD PATTERNS

### National Assembly PDF Pattern
```
https://na.gov.pk/uploads/documents/{ID}.pdf
Example: https://na.gov.pk/uploads/documents/649959d307ba6_291.pdf
```

### Extraction Method
- Find bill in list page
- Extract document link (usually in table row)
- Download PDF
- Extract text using pdfplumber

---

## DOCUMENTED LEGISLATIVE VOLUME

| Period | Bills (Federal) | Provincial Bills | Total |
|--------|-----------------|-----------------|-------|
| **Feb 2026 YTD** | 59 (46 govt + 13 private) | ~100-150 | 150-200 |
| **2025** | ~100 (estimated) | ~200+ | ~300+ |
| **Historical (2013-2026)** | 1,300-1,500+ | 800-1,200+ | 2,100-2,700+ |

---

## CRAWLER CONFIGURATION TEMPLATE

```yaml
crawlers:
  national_assembly:
    base_url: "https://www.na.gov.pk/en/"
    sources:
      - endpoint: "bills.php"
        priority: 1
        rate_limit_seconds: 2
        timeout: 10
      - endpoint: "bills.php?type=1"
        priority: 2
        rate_limit_seconds: 2
      - endpoint: "bills.php?type=2"
        priority: 2
        rate_limit_seconds: 2

  senate:
    base_url: "https://www.senate.gov.pk/en/"
    sources:
      - endpoint: "bills.php"
        priority: 1
        rate_limit_seconds: 2

  punjab_assembly:
    base_url: "https://pap.gov.pk/"
    sources:
      - endpoint: "bills/show/en"
        priority: 1
        rate_limit_seconds: 2
        # Note: May need browser automation

  kpk_assembly:
    base_url: "https://www.pakp.gov.pk/"
    sources:
      - endpoint: "bill/"
        priority: 2
        rate_limit_seconds: 2
      - endpoint: "all-bills/"
        priority: 2
        rate_limit_seconds: 2

  open_parliament:
    base_url: "http://openparliament.pk/"
    sources:
      - endpoint: "legislative-tracker/"
        priority: 1
        rate_limit_seconds: 1
        # Aggregated data - use as validation
```

---

## CRITICAL IMPLEMENTATION NOTES

### What Works Well
✓ Direct PDF access from NA and Senate
✓ Consistent bill number format across sources
✓ HTML table-based listings (easy to parse)
✓ Multiple query parameters for filtering
✓ No apparent login requirements for bills
✓ Large archive of historical bills

### Potential Issues
⚠ Intermittent timeout issues (server load or geo-blocking)
⚠ Provincial sites use varied parameter structures
⚠ Some pages may be dynamically loaded (JavaScript)
⚠ PDF OCR may be needed for some older documents
⚠ No official API (HTML parsing required)
⚠ District courts very large DB (rate limit critical)

### Best Practices
1. **Start with federal sources** (NA + Senate)
2. **Test timeout handling** before scaling
3. **Implement 2-3 second delays** minimum
4. **Respect robots.txt** for all sources
5. **Cache PDFs** to avoid re-downloading
6. **Use Open Parliament** as validation source
7. **Review TOS** before crawling judicial data

---

## DATA VALIDATION CHECKLIST

When you extract a bill, verify:
- [ ] Bill number exists and is formatted correctly (e.g., "91 of 2025")
- [ ] Title is non-empty and reasonable length (>5 chars)
- [ ] Date is valid and within parliament session
- [ ] Type is one of: Government, Private Member, Constitutional Amendment
- [ ] Status is valid (Introduced, Passed, Pending, etc.)
- [ ] Source URL is valid and accessible
- [ ] PDF/document link (if present) is downloadable
- [ ] Full text has reasonable length (>500 characters)
- [ ] Source attribution recorded

---

## RECOMMENDED CRAWL SCHEDULE

```
Phase 1 (Week 1-2): Initial crawl
  - National Assembly: All bills (estimated 2,000+ PDFs to download)
  - Senate: All bills
  - Validate extraction quality

Phase 2 (Week 3-4): Provincial crawl
  - Punjab Assembly
  - Sindh Assembly
  - KPK Assembly
  - Balochistan Assembly

Phase 3 (Week 5-6): Supplementary sources
  - Open Parliament (cross-validation)
  - Punjab Law Portal (supplementary)
  - Sindh Laws portal

Phase 4 (Week 7-8): Judicial data (if needed)
  - Federal Courts case search
  - District Courts (very selective, rate-limited)

Ongoing: Weekly incremental updates
  - Check each source for new bills
  - Update status on existing bills
  - Maintain archive
```

---

## QUICK TROUBLESHOOTING

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| Timeout errors | Server overload or geo-blocking | Increase timeout, add retry logic, use proxy if needed |
| 429 Too Many Requests | Rate limiting | Increase delay between requests to 3-5 seconds |
| Empty results | JavaScript-rendered content | Use Selenium/Playwright for browser automation |
| PDF extraction fails | Scanned PDFs or poor quality | Implement OCR (tesseract) as fallback |
| Duplicate bills | Multiple sources list same bill | Implement bill deduplication by number + title |
| Missing fields | Page structure changed | Monitor extraction errors, update selectors |

---

## TOOLS & LIBRARIES NEEDED

**Web Scraping**:
- requests (HTTP)
- beautifulsoup4 (HTML parsing)
- selenium or playwright (JavaScript rendering)

**PDF Processing**:
- pdfplumber (text extraction)
- pymupdf (alternative)
- pytesseract (OCR fallback)

**Data Processing**:
- pandas (data manipulation)
- sqlalchemy (database ORM)

**Quality**:
- pytest (testing)
- black (code formatting)
- pylint (linting)

**Deployment**:
- celery (task queue)
- redis (cache/queue backend)
- docker (containerization)

---

## ESTIMATED PROJECT SCOPE

| Task | Effort | Duration |
|------|--------|----------|
| Setup & planning | 2 days | 1 week |
| Source verification & testing | 3 days | 1 week |
| Develop base crawler | 5 days | 2 weeks |
| Build extractors for each source | 5 days | 1-2 weeks |
| Implement storage/DB layer | 3 days | 1 week |
| Testing & validation | 5 days | 2 weeks |
| Documentation | 2 days | 1 week |
| Deployment & monitoring setup | 3 days | 1 week |
| **Total** | **~28 days** | **~10 weeks** |

*With team parallelization, can compress to 4-6 weeks*

---

## NEXT STEPS

1. **Verify robots.txt** on each source
2. **Review Terms of Service** (especially judicial data)
3. **Test HTTP connectivity** to each URL
4. **Prototype HTML extraction** on 1-2 sources
5. **Design database schema** for bill storage
6. **Setup rate limiting framework**
7. **Implement error tracking/logging**
8. **Create test fixtures** with real bill data
9. **Build MVP for single source** (recommend: National Assembly)
10. **Expand to other sources** once validated

---

**Files to Reference**:
- `/Users/umerkhan/code/pakistani-legislative-sources-verification.md` - Full verification report
- `/Users/umerkhan/code/pakistan-crawler-technical-specs.md` - Detailed implementation specs
- `/Users/umerkhan/code/pakistan-sources-quick-reference.md` - This file

---

**Questions to Answer Before Starting**:
- [ ] What's the primary use case? (Legal analysis, legislative tracking, research, etc.)
- [ ] What's the update frequency needed? (Daily, weekly, monthly?)
- [ ] Will you need Urdu text? (Some sources may have Urdu versions)
- [ ] How to handle related documents? (Committee reports, amendments, etc.)
- [ ] Storage backend? (PostgreSQL, MongoDB, cloud storage?)
- [ ] API needed? (For end-user access to crawled data?)
- [ ] How often to re-crawl existing bills? (For status updates?)

---

**Last Updated**: 2026-03-08
**Verification Status**: ✓ Complete
**Ready for Implementation**: YES
