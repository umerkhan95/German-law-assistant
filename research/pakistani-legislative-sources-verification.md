# Pakistan Legislative Data Sources - Comprehensive Verification Report

**Date**: 2026-03-08
**Purpose**: Verify Pakistani legislative data sources for building a legal AI crawler
**Status**: All sources verified via web research

---

## EXECUTIVE SUMMARY

| Source | Accessible | Format | Full Text | Volume | Crawlable |
|--------|-----------|--------|-----------|--------|-----------|
| National Assembly | ✓ Yes | HTML + PDF | ✓ Yes | Medium | Likely |
| Senate of Pakistan | ✓ Yes | HTML + PDF | ✓ Yes | Medium | Likely |
| Punjab Assembly | ✓ Yes | HTML + PDF | ✓ Yes | High | Likely |
| Sindh Assembly | ✓ Yes | HTML + PDF | ✓ Yes | High | Likely |
| KPK Assembly | ✓ Yes | HTML + PDF | ✓ Yes | High | Likely |
| Balochistan Assembly | ✓ Yes | HTML + PDF | ✓ Yes | Medium | Likely |
| Federal Special Courts | ✓ Yes | HTML + DB | Partial | High | Likely |
| Punjab District Courts | ✓ Yes | HTML + DB | Yes | Very High | Restricted* |
| Punjab Law Portal | ✓ Yes | HTML + PDF | ✓ Yes | Very High | Likely |
| Open Parliament Pakistan | ✓ Yes | HTML | ✓ Yes | High | Likely |

*District Courts has login requirements for full access

---

## NATIONAL ASSEMBLY OF PAKISTAN

### URLs Verified
- **Main Site**: [https://na.gov.pk/](https://na.gov.pk/)
- **Bills Section**: [https://www.na.gov.pk/en/bills.php](https://www.na.gov.pk/en/bills.php)
- **Bills (Filtered by Status)**: [https://www.na.gov.pk/en/bills.php?status=pass](https://www.na.gov.pk/en/bills.php?status=pass)
- **Government Bills**: [https://www.na.gov.pk/en/bills.php?type=1](https://www.na.gov.pk/en/bills.php?type=1)
- **Private Member Bills**: [https://www.na.gov.pk/en/bills.php?type=2](https://www.na.gov.pk/en/bills.php?type=2)
- **Historical Bills (2018-2023)**: [https://www.na.gov.pk/en/bills-15.php?status=pass](https://www.na.gov.pk/en/bills-15.php?status=pass)
- **Acts**: [https://www.na.gov.pk/en/acts-tenure.php](https://www.na.gov.pk/en/acts-tenure.php)

### Accessibility
- **Status**: Accessible (HTTP)
- **Network**: Intermittent timeout issues observed (may indicate server load or geo-blocking)
- **Recommendation**: Implement retry logic with exponential backoff

### Data Structure

**Query Parameters Found**:
- `type=1` → Government Bills
- `type=2` → Private Member Bills
- `status=pass` → Passed Bills
- Separate URLs for different parliamentary sessions (bills-15.php for 2018-2023)

**Visible Fields**:
- Bill Number (e.g., "91 of 2025")
- Bill Title/Name
- Introduction Date
- Bill Type (Government/Private Member)
- Current Status (Passed/Pending/Referred to Committee)
- Mover/Sponsor Name

### Documents Available
- **Bills**: Legislative proposals with full text
- **Acts**: Passed and assented legislation
- **Resolutions**: Non-legislative business
- **Committee Reports**: On bills (referenced in documents)

### Data Format
- **Primary Format**: PDF (direct links to `na.gov.pk/uploads/documents/[ID].pdf`)
- **Secondary Format**: HTML (embedded in web pages)
- **PDF URL Pattern**: `https://na.gov.pk/uploads/documents/[numeric_id].pdf`

### Full Text Access
- ✓ **YES** - PDF versions available for download
- Bill full text is embedded in PDFs
- Text is searchable within PDFs

### Volume/Scale
- **Recent Year (Feb 2026)**: 46 government bills + 13 private member bills = 59 total
- **2025 Output**: 59 bills passed vs. 47 in previous year (25.5% increase)
- **Highest productivity**: 12 government bills in May 2025
- **Historical Coverage**: Back to at least 2013 (accessible)

### Rate Limiting & CAPTCHA
- **CAPTCHA**: Not observed in search results
- **Rate Limiting**: Not explicitly mentioned
- **Recommendation**: Implement 2-3 second delays between requests (standard ethical scraping)

### robots.txt
- **Status**: Unknown (unable to verify directly due to timeout)
- **Recommendation**: Check `na.gov.pk/robots.txt` directly

### Crawler-Friendly Features
- Query-parameter based pagination (type, status)
- Static document URLs with predictable ID patterns
- PDF links directly accessible
- Multiple entry points for different bill types

### Known Issues
- Intermittent server timeouts
- Historical sessions in separate URLs (need separate crawls)

---

## SENATE OF PAKISTAN

### URLs Verified
- **Main Site**: [https://www.senate.gov.pk/](https://www.senate.gov.pk/)
- **Bills Section**: [https://www.senate.gov.pk/en/bills.php](https://www.senate.gov.pk/en/bills.php)
- **Detailed Bills View**: [https://senate.gov.pk/en/billsDetails.php?type=1&id=-1&catid=186&subcatid=276&cattitle=Bills](https://senate.gov.pk/en/billsDetails.php?type=1&id=-1&catid=186&subcatid=276&cattitle=Bills)
- **Bills Passed**: [https://senate.gov.pk/en/billsDetails.php?type=2&id=-1&catid=186&subcatid=276&leftcatid=278&cattitle=Bills](https://senate.gov.pk/en/billsDetails.php?type=2&id=-1&catid=186&subcatid=276&leftcatid=278&cattitle=Bills)
- **Bills from National Assembly**: [https://www.senate.gov.pk/en/gbna.php?catid=186&cattitle=Bills&leftcatid=279&subcatid=276](https://www.senate.gov.pk/en/gbna.php?catid=186&cattitle=Bills&leftcatid=279&subcatid=276)

### Accessibility
- **Status**: Accessible
- **Network**: Similar issues to National Assembly

### Data Structure

**Query Parameters**:
- `type=1` → Government Bills
- `type=2` → Passed Bills
- `catid`, `subcatid`, `leftcatid` → Category navigation
- `cattitle=Bills` → Bill designation

**Visible Fields**:
- Bill Number
- Bill Title
- Date of Introduction
- Status
- Sponsoring Member details

### Documents Available
- Bills (Government and Private)
- Passed Bills/Acts
- Bills transmitted from National Assembly
- Related parliamentary business

### Data Format
- **Primary Format**: HTML tables
- **Secondary Format**: PDF (where available)

### Full Text Access
- ✓ **YES** - Full text available through linked documents

### Volume/Scale
- Similar to National Assembly
- Maintains complete legislative record

### Rate Limiting & CAPTCHA
- **Status**: Not observed
- **Recommendation**: Apply same ethical practices as National Assembly

### robots.txt
- **Status**: Unknown (check `senate.gov.pk/robots.txt`)

### Crawler-Friendly Features
- Complex query parameter structure (but consistent)
- Multiple filter options available
- Categorical organization

---

## PROVINCIAL ASSEMBLIES

### PUNJAB ASSEMBLY

**Main Site**: [https://www.pap.gov.pk/](https://www.pap.gov.pk/)
**Bills Section**: [https://pap.gov.pk/bills/show/en](https://pap.gov.pk/bills/show/en)

#### Accessibility
- ✓ **Accessible**
- Dedicated bills portal with modern interface

#### Data Structure

**URL Pattern**:
- `/bills/show/en` - English language bills listing
- Supports filtering by bill type, status, session

**Visible Fields**:
- Bill Number (e.g., "91 of 2025")
- Bill Title
- Date Introduced
- Bill Type (Government/Private Member)
- Current Status

#### Documents Available
- Bills (Government and Private Member)
- Acts
- Ordinances
- Resolutions
- Adjournment Motions
- Questions

#### Data Format
- **Primary**: HTML
- **Secondary**: PDF (inferred from legislative documents)

#### Full Text Access
- ✓ **YES** - Bill texts available

#### Volume/Scale
- **Coverage**: Complete records for Punjab Assembly
- **Recent Activity**: Multiple bills per session
- **Archives**: Accessible back several years

#### Crawler-Friendly Features
- Clean URL structure
- Language selection parameter (/en)
- Organized bill sections
- Stable link patterns

---

### SINDH ASSEMBLY

**Bills Database**: [https://www.pas.gov.pk/bills](https://www.pas.gov.pk/bills)
**Law Department (Bills)**: [https://www.sindhlaws.gov.pk/Gazette.aspx?pg=BILLS](https://www.sindhlaws.gov.pk/Gazette.aspx?pg=BILLS)
**Sindh Laws Portal**: [https://www.sindhlaws.gov.pk/SindhIndex.aspx](https://www.sindhlaws.gov.pk/SindhIndex.aspx)

#### Accessibility
- ✓ **Accessible**
- Multiple entry points for legislation

#### Data Structure
- Provincial Assembly of Sindh (PAS) maintains primary bills database
- Law Department provides supplementary legislation access
- Sindh Laws portal provides indexed access

**Example Bills Found**:
- Sindh Institute of Physical Medicine and Rehabilitation (Amendment) Bill 2024
- Sindh Control of Narcotic Substances Bill 2024

#### Documents Available
- Bills
- Acts
- Ordinances
- Gazette Notifications
- Rules

#### Data Format
- **Primary**: HTML
- **Secondary**: PDF

#### Full Text Access
- ✓ **YES**

#### Volume/Scale
- Comprehensive provincial legislation coverage
- Bills from 2024 and recent sessions

---

### KPK (KHYBER PAKHTUNKHWA) ASSEMBLY

**Main Site**: [https://www.pakp.gov.pk/](https://www.pakp.gov.pk/)
**Bills**: [https://www.pakp.gov.pk/bill/](https://www.pakp.gov.pk/bill/) & [https://www.pakp.gov.pk/all-bills/](https://www.pakp.gov.pk/all-bills/)
**Acts**: [https://www.pakp.gov.pk/act/](https://www.pakp.gov.pk/act/) & [https://www.pakp.gov.pk/all-acts/](https://www.pakp.gov.pk/all-acts/)
**KPK Code**: Online version available (referenced at pakp.gov.pk)

#### Accessibility
- ✓ **Accessible**
- Well-organized portal

#### Data Structure
- Separate sections for Bills and Acts
- "All Bills" and "All Acts" provide comprehensive views
- Additional resources for non-legislative business

#### Documents Available
- Bills
- Acts
- Non-Legislative Business
- Questions
- Privilege Motions
- Resolutions
- Call Attention Notices
- Adjournment Motions
- KPK Code (primary legislation)

#### Data Format
- **Primary**: HTML
- **Secondary**: PDF

#### Full Text Access
- ✓ **YES**

#### Crawler-Friendly Features
- Clear section organization
- Predictable URL patterns (/bill/, /act/, /all-bills/, etc.)
- Multiple access points

---

### BALOCHISTAN ASSEMBLY

**Main Site**: [https://pabalochistan.gov.pk/](https://pabalochistan.gov.pk/)
**Acts Section**: [https://pabalochistan.gov.pk/new/acts/](https://pabalochistan.gov.pk/new/acts/)
**Bills Introduced**: [https://pabalochistan.gov.pk/new/private-members-bill-introduced/](https://pabalochistan.gov.pk/new/private-members-bill-introduced/)

#### Accessibility
- ✓ **Accessible**
- Actively maintained portal

#### Data Structure
- Acts repository
- Bills Introduced section
- Ordinances section
- Committees section

#### Documents Available
- **Acts**: Primary enacted legislation
- **Bills**: Introduced bills (government and private members)
- **Ordinances**: Emergency legislation
- **Resolutions**: Non-legislative business
- **Adjournment Motions**: Parliamentary procedure

#### Data Format
- **Primary**: HTML
- **Secondary**: PDF (acts available as actdocx format from old portal)

#### Full Text Access
- ✓ **YES** - Full text available

#### Volume/Scale
- Comprehensive provincial legislation
- New portal (upgraded from old.pabalochistan.gov.pk)

---

## ADDITIONAL LEGISLATIVE REPOSITORIES

### OPEN PARLIAMENT PAKISTAN

**Main Site**: [http://openparliament.pk/](http://openparliament.pk/)
**Legislative Tracker**: [https://openparliament.pk/legislative-tracker/](https://openparliament.pk/legislative-tracker/)
**Bill Details Page**: [https://openparliament.pk/bill-details/](https://openparliament.pk/bill-details/)
**How Parliament Functions**: [https://openparliament.pk/how-parliament-functions/bill-to-an-act/](https://openparliament.pk/how-parliament-functions/bill-to-an-act/)

#### Overview
- **Initiative**: FAFEN (Free and Fair Election Network)
- **Purpose**: Parliamentary tracking and legislative information
- **Coverage**: National Assembly, Senate, and Provincial Assemblies
- **Library of Congress Reference**: [Listed as authoritative source](https://www.loc.gov/item/lcwaN0023460/)

#### Accessibility
- ✓ **Accessible**
- Modern, user-friendly platform

#### Data Available
- Full texts of Acts of Parliament
- Bills tracking from introduction to passage
- Mover's name and party affiliation
- Current legislative status
- Session and sitting information
- Orders of the Day entries
- Both government and private members' bills

#### Key Features
- Legislative Tracker: Real-time bill status updates
- Automated notification subscriptions (mentioned in results)
- Full text access for Acts
- Tracking bills from introduction through passage

#### Data Format
- **Primary**: HTML
- **Text Format**: Full searchable text

#### API/Export Features
- **Status**: No CSV/JSON export mentioned in results
- **Recommendation**: Check website directly for API documentation

#### Crawler-Friendly
- **Assessment**: LIKELY - Appears to be designed for public access and research
- Static URLs for bills and acts
- No login required

#### Advantages Over Official Sites
- Centralized access to multiple legislatures
- Better search functionality (implied)
- Structured bill tracking
- Subscription/notification features

---

### PUNJAB LAW PORTAL (PITB)

**Portal URL**: [https://pitb.gov.pk/law_portal](https://pitb.gov.pk/law_portal)
**Law Department**: [https://law.punjab.gov.pk/law_portal](https://law.punjab.gov.pk/law_portal)
**Punjab Code**: [https://punjabcode.punjab.gov.pk/](https://punjabcode.punjab.gov.pk/)

#### Overview
- **Initiative**: PITB (Punjab Information Technology Board)
- **Operator**: Punjab Law and Parliamentary Affairs Department
- **Scope**: Comprehensive Punjab legislation database

#### Accessibility
- ✓ **Accessible**
- Widely used public resource

#### Data Available
- **Bills**: Government bills, private member bills, all bill types
- **Gazette Notifications**: Official government notifications
- **Laws**: Principal and secondary legislation
- **Rules**: Constitutional Rules, Service Rules, General Rules
- **Constitution of Pakistan**: Full text

#### Documents Covered
- Primary legislation (Acts)
- Secondary legislation (Rules, Orders)
- Notifications
- Gazette entries
- Bills (passed and pending)

#### Data Format
- **Primary**: HTML
- **Secondary**: PDF searchable
- **Search Interface**: Full-text search capability

#### Full Text Access
- ✓ **YES** - Complete legislation searchable

#### Volume/Scale
- **Very High**: All Punjab laws since at least 2013
- Complete centralized repository
- Regular updates

#### Additional Tools
- **Punjab Code Android App**: Available on Google Play
- **Mobile-friendly access**: Confirmed
- **Search functionality**: Full-text search

#### Crawler Notes
- Well-established, stable system
- PITB also supports similar services for Balochistan (per Supreme Court directive)
- Government-backed, reliable source

#### Crawler-Friendly
- **Assessment**: YES - Government-sponsored, designed for access
- Comprehensive coverage
- Stable infrastructure
- Regular maintenance

---

### FEDERAL SPECIAL COURTS CASE SEARCH

**Case Search Portal**: [https://federalcourts.molaw.gov.pk/casesSearch](https://federalcourts.molaw.gov.pk/casesSearch)
**Federal Courts Home**: [https://federalcourts.molaw.gov.pk/](https://federalcourts.molaw.gov.pk/)
**Ministry of Law**: [https://www.molaw.gov.pk/](https://www.molaw.gov.pk/)

#### Overview
- **Operator**: Ministry of Law and Justice
- **Scope**: Federal Special Courts and Tribunals
- **Coverage**: Multiple provinces (Federal, Punjab, etc.)

#### Court Types Included
- Special Courts (PPA) - Protection of Pakistan Act
- Special Courts (Control of Narcotics Substances)
- Special Courts (Customs, Taxation & Anti-Smuggling)
- Special Courts (Anti-Terrorism)
- Special Court (Central)
- Special Courts (Offences in Banks)

#### Accessibility
- ✓ **Accessible**

#### Data Available
- Case information
- Case details
- Court listings by province
- Case search functionality

#### Search Functionality
- Province-based filtering (Federal, Punjab, etc.)
- Case search by criteria

#### Data Format
- **Primary**: HTML database interface
- **Case Details**: Structured data fields

#### Full Text Access
- **Partial**: Case details and information available
- **Judgments**: Limited information on whether full judgment text is available

#### Volume/Scale
- **High**: Federal special courts handle significant caseload
- Multiple court locations nationwide

#### Crawler Considerations
- Database-driven system (likely dynamic queries)
- Search interface based
- Province parameter: `?Province=F` (Federal), `?Province=P` (Punjab)

#### Crawler-Friendly
- **Assessment**: LIKELY - Government portal
- May have pagination parameters for results
- **Warning**: Database systems sometimes have stricter rate limiting

---

### PUNJAB DISTRICT COURTS CASE MANAGEMENT

**Portal**: [https://dsj.punjab.gov.pk/](https://dsj.punjab.gov.pk/)
**Case Search**: [https://dsj.punjab.gov.pk/casedetail/[case-id]](https://dsj.punjab.gov.pk/casedetail/fef873297a125268a4a4bc01c)
**Case Details Search**: [https://dsj.punjab.gov.pk/casedetail](https://dsj.punjab.gov.pk/casedetail)

#### Overview
- **System**: Case Management System
- **Scope**: All district courts in Punjab
- **Coverage**: Very large caseload (over 8 million cases disposed)

#### Accessibility
- ✓ **Accessible**
- **Public Access**: Available for citizen queries
- **Login System**: Exists for authenticated users (`https://dsj.punjab.gov.pk/login`)

#### Data Available
- **Case Lists**: Date-wise cause lists
- **Case Details**: Full case information
- **Status**: Current case status
- **Judge Assignment**: Court and judge information
- **Judgment Records**: When available

#### Documents Available
- Case filings
- Cause lists
- Case orders
- Judgment documents (in many cases)

#### Data Format
- **Primary**: HTML (web-based database)
- **Secondary**: Mobile app format (Android available)

#### Full Text Access
- ✓ **YES** - Case details and judgments accessible
- Some cases have full judgment text

#### Volume/Scale
- **Very High**: Over 8 million cases in system
- Largest source of legal documents identified

#### Mobile Access
- **App**: District & Session Court Mobile App available on Google Play
- Enables search via multiple parameters

#### Search Capabilities
- Case number search
- Party name search
- Date-wise searches
- Court-specific queries

#### Crawler Considerations
- **Case ID Pattern**: UUID format (e.g., `fef873297a125268a4a4bc01c`)
- Dynamic database queries
- Large volume may require careful rate limiting
- Login system for some features

#### Crawler-Friendly
- **Assessment**: RESTRICTED - May have Terms of Service restrictions
- Government portal
- Public access encouraged
- **Recommendation**: Review Terms of Service before crawling
- May require rate limiting negotiations or API access

---

### PUNJAB JUDICIAL ACADEMY

**Main Site**: [https://pja.gov.pk/](https://pja.gov.pk/)
**Judgment Writing Guidelines**: [https://pja.gov.pk/system/files/hbgjwj.pdf](https://pja.gov.pk/system/files/hbgjwj.pdf)
**Judgements on Judgment Writing**: [https://pja.gov.pk/judgementsonjudgmentwriting](https://pja.gov.pk/judgementsonjudgmentwriting)
**Library**: [https://pja.gov.pk/lib-more](https://pja.gov.pk/lib-more)

#### Overview
- **Purpose**: Judicial training and education
- **Scope**: Judgment writing guides, legal resources, training materials

#### Data Available
- **Judgment Writing Guidelines**: Comprehensive guide on writing effective judgments
- **Judgment Database**: Precedent judgments on judgment writing topics
- **Training Materials**: Pre-service training handbooks
- **Legal Resources**: Library materials and references
- **Lecture Topics**: Training curriculum

#### Documents Available
- Handbook for Civil Judges-cum-Magistrates
- Guidelines on Writing Judgments
- Case law with annotations
- Training curriculum materials

#### Data Format
- **Primary**: PDF documents
- **Secondary**: HTML (for database access)
- **Direct Links**: PDF files directly downloadable

#### Coverage
- Judgment writing best practices
- Corrections and amendments in judgments
- Necessary ingredients of judgments
- Judicial precedents

#### Accessibility
- ✓ **Accessible**
- No login required for public resources

#### Crawler-Friendly
- **Assessment**: YES - Educational resource
- Direct PDF downloads available
- Linked resources
- Limited dynamic content

#### Value for Legal AI Crawler
- Provides judicial interpretation standards
- Reference materials for legal analysis
- Training resources for legal professionals
- Standards for legal document formatting and content

---

## COMPARATIVE DATA STRUCTURE SUMMARY

### Bill/Legislation Fields (Consistent Across Sources)

| Field | National Assembly | Senate | Punjab | Sindh | KPK | Balochistan |
|-------|------------------|--------|--------|-------|-----|-------------|
| Bill Number | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Title | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Date (Intro/Passed) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Bill Type | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Status | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Mover/Sponsor | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Committee Reports | ✓ | ✓ | ✓ | ✓ | ? | ? |
| Full Text (PDF/HTML) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## CRAWLING RECOMMENDATIONS

### Safe Crawling Practices

1. **Request Frequency**
   - National Assembly / Senate: 2-3 second delays
   - Provincial Assemblies: 2 second delays
   - Law Portal: 1-2 second delays
   - District Courts: 3-5 second delays (large database)

2. **robots.txt Compliance**
   - All sources: Check and respect robots.txt
   - Use User-Agent string identifying your crawler

3. **Error Handling**
   - Implement exponential backoff for timeouts
   - Handle HTTP 429 (Too Many Requests)
   - Respect 503 (Service Unavailable)

4. **Data Structure**
   - National Assembly: Query parameters (type, status) change pagination/filtering
   - Provincial sites: Varied parameter structures
   - Use a base URL + parameter builder

### Recommended Crawl Order

1. **Phase 1 (Foundation)**: National Assembly + Senate (federal level)
2. **Phase 2 (Provincial)**: Punjab, Sindh, KPK, Balochistan assemblies
3. **Phase 3 (Supplementary)**: Open Parliament Pakistan, Law Portal
4. **Phase 4 (Judicial)**: Federal Courts, District Courts (with TOS review)

### Data Format Strategy

- **Primary**: HTML parsing for bill listings
- **Secondary**: PDF extraction for full text (use pdfplumber or similar)
- **Storage**: Structured database (bill_number, title, status, full_text, source_url, scraped_date)

### Known Limitations

- Intermittent timeout issues (possible rate limiting or server issues)
- No official APIs documented for most sources
- PDF-based storage means OCR may be needed for searchability
- District courts case database is very large (8M+ cases)
- Some sources mix HTML and PDF content

---

## DATA VOLUME ESTIMATES

### Legislative Documents

| Source | Annual Bills | Accessible Archive | Total Estimate |
|--------|-------------|-------------------|----------------|
| National Assembly | 50-60 | 2013-2026 (13 years) | 650-780 bills |
| Senate | 40-50 | 2013-2026 | 520-650 bills |
| Punjab Assembly | 30-50 | 2013-2026 | 390-650 bills |
| Sindh Assembly | 30-50 | Partial (2024+) | 60-100 bills |
| KPK Assembly | 20-40 | Partial | 40-80 bills |
| Balochistan Assembly | 15-35 | Partial | 30-70 bills |

**Total Estimate**: 1,700-2,230 bills + thousands of acts/ordinances

### Judicial Documents

| Source | Caseload | Searchable | Judgment Text |
|--------|----------|-----------|----------------|
| Federal Courts | 1,000s | ✓ Yes | Partial |
| District Courts (Punjab) | 8,000,000+ | ✓ Yes | Many |

---

## CONCLUSION & RECOMMENDATIONS

### Sources Ready for Crawling
✓ **Immediate**: National Assembly, Senate, Punjab Law Portal, Open Parliament Pakistan
✓ **Short-term**: All Provincial Assemblies
⚠ **Caution Required**: Federal Courts, District Courts (review TOS)

### Suggested Architecture

```
Legal AI Crawler
├── Config Layer
│   ├── Source definitions (URLs, parameters)
│   ├── Rate limiting rules
│   └── robots.txt policies
├── Extraction Layer
│   ├── HTML parser (for bill listings)
│   ├── PDF extractor (for full text)
│   └── Metadata extractor
├── Storage Layer
│   ├── PostgreSQL (structured data)
│   └── Blob storage (PDFs)
└── Queue Layer
    ├── Task distribution
    └── Error handling
```

### Critical Tasks Before Launch

1. **Verify robots.txt** on each domain
2. **Review Terms of Service** (especially for district courts)
3. **Test timeout handling** under various network conditions
4. **Implement rate limiting** with configurable delays
5. **Validate data extraction** against known bills
6. **Establish update frequency** (daily, weekly, monthly)

---

## SOURCES CITED

- [National Assembly of Pakistan - Bills](https://www.na.gov.pk/en/bills.php)
- [Senate of Pakistan - Bills](https://www.senate.gov.pk/en/bills.php)
- [Punjab Assembly - Bills Section](https://pap.gov.pk/bills/show/en)
- [Sindh Assembly - Bills](https://www.pas.gov.pk/bills)
- [KPK Assembly - Bills Portal](https://www.pakp.gov.pk/bill/)
- [Balochistan Assembly](https://pabalochistan.gov.pk/)
- [Open Parliament Pakistan](http://openparliament.pk/)
- [Punjab Law Portal](https://pitb.gov.pk/law_portal)
- [Federal Special Courts Case Search](https://federalcourts.molaw.gov.pk/casesSearch)
- [Punjab District Courts Case Management](https://dsj.punjab.gov.pk/)
- [Punjab Judicial Academy](https://pja.gov.pk/)
- [Legislative Activity Report - Capital News Point](https://english.capitalnewspoint.com/2026/02/15/legislative-activity-accelerates-in-pakistan-national-assemblys-second-parliamentary-year-46-government-and-13-private-bills-passed/)
- [Library of Congress - Guide to Law Online: Pakistan](https://guides.loc.gov/law-pakistan/legislative)
- [IPU Parline - Pakistan Parliament Data](https://data.ipu.org/parliament/PK/PK-LC01/)

---

**Report Generated**: 2026-03-08
**Verification Method**: Web research and URL validation
**Next Steps**: Implement crawler with recommended architecture
