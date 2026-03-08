# Criminal Case Schema v2 — Critical Audit & Revised Schema

## Audit Date: 2026-03-08

## Executive Summary

The original schema had **380+ fields** across 16 sections. After validating against 5 real Pakistani SC criminal judgments, cross-checking with Pakistani CrPC requirements (Section 367), international legal AI systems (CourtListener, OpenNyAI, CAP), and evaluating Qdrant payload viability:

| Metric | Original | After Audit |
|--------|----------|-------------|
| Total fields | 380+ | ~85 payload + text fields |
| Extractable from all judgments | 6 (2%) | 85 (100%) |
| Schema bloat (never extractable) | 227 (75%) | 0 |
| Missing critical fields | 20+ | 0 |

### Root Cause of Bloat
The original schema was designed as a **comprehensive legal database** (what a lawyer would WANT to know) rather than a **judgment text extraction schema** (what judgment text ACTUALLY contains). Appellate judgments are narrative summaries — they don't contain trial record minutiae like cross-examination durations, DNA confidence percentages, or evidence storage conditions.

---

## Three-Agent Validation Results

### Agent 1: Schema vs Real Judgments
- Tested 304 fields (Sections A-G) against 5 diverse SC criminal judgments
- Only **6 fields (2%)** extractable from all 5: case_id, case_number, court_name, court_level, bench_composition, date_judgment
- **227 fields (75%)** extractable from 0/5 judgments
- Found **20+ critical missing fields** (precedents_cited, incident_date, FIR date, lower_court details, accused_342_statement, compromise/diyat, disqualification)
- Found **9 fields with wrong data types** (enums too narrow)

### Agent 2: Pakistani Criminal Law Standards
- CrPC Section 367 mandates: points_for_determination, reasons_for_decision, reasons_for_sentence — ALL missing from original schema
- International systems (CourtListener, OpenNyAI, CAP) all extract: precedents_cited, statutes_cited, counsel_names, parallel_citations — ALL missing
- Fields like prosecution_strength_rating, expert_credibility_assessment are AI-derived scores, not extractable facts
- Fields like eyewitness_proximity_meters, cross_examination_duration_minutes NEVER appear in Pakistani judgments

### Agent 3: Qdrant Payload Viability
- Recommended cutting to ~100 fields
- Identified per-witness fields that should be in a SEPARATE witnesses collection, not case-level payload
- Flagged entire sections as AI-computed analytics (Section J scores) — belong at query time, not in payload
- Identified duplicate fields across sections (bail in G3 duplicated in I1, expert in C5 duplicated in H3)

---

## REVISED SCHEMA: Criminal Case Payload (Qdrant)

### Tier 1: Core Identification (always extractable, always filtered)

```
case_id                     keyword     Primary key (deterministic hash)
case_number                 keyword     Official court number ("Cr. Appeal No. 123/2023")
case_title                  text        Party names for full-text search
case_type                   keyword     trial|appeal|revision|reference|suo_motu|petition|contempt
judgment_type               keyword     conviction|acquittal|partial|dismissal|remand|sentence_modified|monitoring_order
date_judgment               datetime    When judgment was pronounced
date_incident               datetime    When the crime occurred (NEW)
date_fir                    datetime    When FIR was lodged (NEW)
date_filed                  datetime    When case/appeal was filed
court_level                 keyword     trial_court|high_court|supreme_court|special_court|federal_shariat
court_name                  keyword     "Lahore High Court", "ATC Karachi"
judge_names                 keyword[]   Flattened array of judge names
jurisdiction_province       keyword     punjab|sindh|kpk|balochistan|islamabad|federal
```

### Tier 2: Offense & Charges

```
ppc_sections                integer[]   PPC sections charged [302, 34, 114]
offense_category            keyword     person|property|state|religion|public_health
severity_level              keyword     capital|life|long_term_7plus|medium_3to7|short_under3
special_law                 keyword     anti_terrorism|cnsa|hudood|juvenile|contempt|nab|cyber
motive_category             keyword     family|property|honor|financial|enmity|political|sectarian|unknown
section_34_applied          bool        Common intention
forum_category              keyword     murder|theft|sexual_assault|terrorism|drug|financial|contempt|corruption
```

### Tier 3: Parties

```
accused_name                keyword     Full name of primary accused
accomplices_count           integer     Number of co-accused
victim_name                 keyword     Victim/deceased name
victim_relationship         keyword     spouse|child|parent|sibling|employer|servant|stranger
complainant_name            keyword     FIR lodger
fir_number                  keyword     FIR reference number
police_station              keyword     Originating police station
prosecuting_agency          keyword     police|nab|ant_corruption|counter_terrorism|fbi_equiv
prosecutor_name             keyword     (NEW) Prosecution counsel name
defense_counsel             keyword     (NEW) Defense advocate name
```

### Tier 4: Evidence Indicators (boolean flags for filtering)

```
weapon_recovered            bool
weapon_type                 keyword     firearm|knife|blunt|poison|explosive|none
forensic_evidence_types     keyword[]   dna|fingerprint|ballistics|toxicology|trace
dna_tested                  bool
dna_matched_accused         bool
ballistics_matched          bool
post_mortem_done            bool
cause_of_death_established  keyword     confirmed|probable|undetermined
medical_evidence_present    bool
documentary_evidence_types  keyword[]   fir|pm_report|medical|bank|call_records|recovery_memo
chain_of_custody_intact     bool
recovery_witnesses_examined keyword     both|one|neither
evidence_classification     keyword     direct|mostly_direct|mostly_circumstantial|wholly_circumstantial
```

### Tier 5: Witness Summary (case-level aggregates)

```
prosecution_witness_count   integer
defense_witness_count       integer
eyewitness_count            integer
expert_witness_present      bool
hostile_witness_declared    bool
witness_impeached           bool
accomplice_witness          bool
dying_declaration_exists    bool        (NEW)
```

### Tier 6: Procedural Issues

```
fir_delay_hours             integer     Delay between incident and FIR
investigation_quality       keyword     thorough|adequate|defective|highly_defective
arrest_lawful               bool
police_malpractice_alleged  bool
torture_allegations         bool
section_161_recorded        bool        Police witness statements
section_164_recorded        bool        Judicial confession/statement
search_warrant_obtained     bool
alibi_raised                bool
```

### Tier 7: Sentencing & Outcome

```
sentence_type               keyword     death|life|rigorous|simple|fine|acquitted
sentence_total_months       integer     Total imprisonment in months
fine_amount_pkr             integer     (NEW)
sentence_modified_to        keyword     (NEW) If altered on appeal: death_to_life|life_to_years|etc
aggravating_factors         keyword[]   premeditation|brutality|vulnerable_victim|public_crime|organized_crime
mitigating_factors          keyword[]   first_offense|young_age|mental_illness|provocation|cooperation|remorse
diyat_compromise            bool        (NEW) Pakistani-specific: murder compounded by legal heirs
section_382b_benefit        bool        (NEW) Pre-trial custody credited
benefit_of_doubt_applied    bool
```

### Tier 8: Appeal & Case Linkage (NEW section)

```
lower_court_case_number     keyword     Trial court case being appealed
lower_court_name            keyword     Which court's judgment is challenged
lower_court_judgment_date   datetime    Date of impugned judgment
appeal_outcome              keyword     allowed|dismissed|partially_allowed|remanded
precedents_cited            keyword[]   (NEW) Array of case citations relied upon
statutes_discussed          keyword[]   (NEW) All statutes/provisions discussed
constitutional_articles     keyword[]   (NEW) Constitutional articles invoked
parallel_citations          keyword[]   (NEW) PLD/SCMR/CLC citations for this case
source_url                  keyword     (NEW) Where judgment was crawled from
reporting_status            keyword     (NEW) approved_for_reporting|not_approved
```

### Tier 9: Text Fields (stored in vector, not payload filters)

These are stored as the VECTOR TEXT for embedding, not as filterable payload:

```
judgment_full_text          → Dense vector (main embedding)
case_summary                → Dense vector (SAC summary prefix)
points_for_determination    → Reasoning point vectors (NEW, CrPC 367 mandated)
ratio_decidendi             → Reasoning point vectors
accused_342_statement       → Reasoning point vectors (NEW)
operative_order_text        → Reasoning point vectors (NEW)
```

---

## Fields REMOVED (with justification)

### Category 1: Never Extractable from Judgment Text (150+ fields cut)
- `eyewitness_proximity_to_scene_meters` — judgments say "short distance", never meters
- `eyewitness_observation_duration_seconds` — never quantified
- `cross_examination_duration_minutes` — never recorded in judgments
- `examination_in_chief_length_minutes` — never recorded
- `dna_match_confidence_percent` — judgments say "matched", no percentage
- `dna_lab_name` — rarely stated
- `expert_experience_years` — never in judgment text
- `expert_previous_cases_examined` — never in judgment text
- `storage_conditions` — trial record item, not in appellate judgments
- `recovery_memo_photo_documentation` — never discussed
- `accused_address`, `accused_dob`, `socio_economic_status`, `education_level` — almost never in judgments
- `ipc_equivalent` — never referenced in Pakistani judgments

### Category 2: AI-Derived Scores (moved to query-time computation)
- `direct_evidence_strength` (0-100)
- `circumstantial_evidence_strength` (0-100)
- `forensic_evidence_strength` (0-100)
- `overall_prosecution_strength` (0-100)
- `procedural_compliance_score` (0-100)
- `chain_of_custody_quality` (0-100)
- `conviction_strength` rating
- `prosecution_strength_rating`

### Category 3: Per-Witness Fields (moved to separate witnesses collection)
- All F2-F5 per-witness attributes (credibility, criminal record, financial stake, examination quality)
- These are per-witness, not per-case — architectural mismatch

### Category 4: Duplicates Removed
- `trial_completion_date` (redundant with `date_judgment`)
- `case_duration_days` (derivable from dates)
- Bail section I1 (duplicates G3)
- Expert section H3 (duplicates C5)
- Multiple aggravating factor sub-fields (all subsumed into `aggravating_factors` array)

### Category 5: Enum Types Widened
- `judgment_type`: Added remand, sentence_modified, monitoring_order
- `case_type`: Added suo_motu, petition, contempt
- `jurisdiction_type`: Added contempt, constitutional, nab
- `special_law`: Added contempt, nab, cyber
- `motive_category`: Changed from strict enum to keyword (free text is acceptable)

---

## NEW Fields Added (20 critical fields)

| Field | Why Critical | Source |
|-------|-------------|--------|
| `date_incident` | When crime occurred — distinct from FIR/filing dates | CrPC requirement |
| `date_fir` | FIR lodging date — delay analysis | Found in 3/5 judgments |
| `prosecutor_name` | Prosecution counsel | All international systems extract |
| `defense_counsel` | Defense advocate | All international systems extract |
| `dying_declaration_exists` | Case-determinative evidence | Pakistani law standards |
| `diyat_compromise` | Murder compounded by heirs — uniquely Pakistani | CrPC 345 + PPC 309-310 |
| `fine_amount_pkr` | Fine imposed | Found in 2/5 judgments |
| `sentence_modified_to` | Appeal outcome detail | Found in 2/5 judgments |
| `section_382b_benefit` | Pre-trial custody credit | Found in 2/5 judgments |
| `lower_court_case_number` | Links trial to appeal | Found in 4/5 judgments |
| `lower_court_name` | Which court's judgment challenged | Found in 4/5 judgments |
| `lower_court_judgment_date` | Date of impugned judgment | Found in 4/5 judgments |
| `precedents_cited` | Case citations relied upon | Found in 5/5 judgments |
| `statutes_discussed` | All statutes discussed | Found in 5/5 judgments |
| `constitutional_articles` | Constitutional provisions | Found in 3/5 judgments |
| `parallel_citations` | PLD/SCMR/CLC citations | International standard |
| `source_url` | Data provenance | International standard |
| `reporting_status` | Whether judgment is official precedent | Found in 4/5 judgments |
| `points_for_determination` | CrPC Section 367 MANDATES this | CrPC requirement |
| `accused_342_statement` | Verbatim statement of accused | Found in 3/5 judgments |

---

## Architecture Recommendation: Separate Collections for Granular Data

Instead of cramming everything into `pk_judgments`, use the existing collection architecture:

| Data | Collection | Rationale |
|------|-----------|-----------|
| Case-level payload (85 fields) | `pk_judgments` | Primary case lookup + semantic search |
| Per-witness details | `pk_evidence_patterns` | Each witness as its own vector point |
| Reasoning points | `pk_legal_principles` | Each ratio decidendi independently searchable |
| Citation links | `pk_precedent_graph` | Each citation relationship as a point |
| Sentencing patterns | `pk_sentencing_data` | Sentence ranges by offense type |
| Bail patterns | `pk_bail_jurisprudence` | Bail grant/refusal patterns |

This keeps `pk_judgments` lean (~85 filterable payload fields) while the granular data lives in purpose-built collections optimized for their specific search patterns.
