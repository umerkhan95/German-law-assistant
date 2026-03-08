# Criminal Schema v2 — Revision: LLM-Reasoned Fields Restored

## Context

The v2 audit correctly cut ~295 fields from 380+ → 85. However, it made a critical error: it treated LLM-reasoned classification fields the same as "not in text" fields.

**The distinction:**
- **Directly extractable**: regex/pattern match (dates, case numbers, judge names) ✓ Kept in v2
- **LLM-reasoned**: LLM reads context and classifies (investigation_quality, prosecution_strength) ✗ Wrongly cut
- **Genuinely absent**: info simply not in the text (DNA confidence %, cross-exam duration in minutes) ✓ Correctly cut

## Re-Audit Results

| Category | Count | Action |
|----------|-------|--------|
| A: RESTORE (LLM can reliably fill) | ~65 | Add back to schema |
| B: CORRECTLY CUT (genuinely not in text) | ~195 | Stay cut |
| C: MOVE TO REASONING POINTS (vector text, not payload) | ~35 | Not in payload, stored as vectors |

## Revised Totals

| Version | Payload Fields | Vector Text Fields |
|---------|---------------|-------------------|
| v1 (original) | 380+ | 0 |
| v2 (over-cut) | 85 | 0 |
| **v2.1 (final)** | **~150** | **~35 reasoning points** |

## Three-Tier Field Classification

### Tier A: Directly Extractable (regex/NER) — ~85 fields
All fields from v2 schema. Case ID, court, dates, judge names, PPC sections, parties, basic evidence booleans, sentence details, appeal linkage.

### Tier B: LLM-Reasoned Classifications — ~65 fields (RESTORED)

These require the LLM to read surrounding context and make a judgment call. All are HIGH or MEDIUM filter value.

**Top 10 highest-value restores:**
1. `prosecution_strength_rating` — keyword (weak|moderate|strong|very_strong)
2. `defense_strategy_primary` — keyword (alibi|mistaken_identity|self_defense|insanity|procedural_defect|reasonable_doubt|false_implication)
3. `prosecution_strategy_primary` — keyword (eyewitness|circumstantial_chain|forensic|confession|motive_opportunity)
4. `motive_strength` — keyword (strong|weak|none)
5. `motive_proven` — bool
6. `conviction_strength` — keyword (unassailable|strong|weak|overturned)
7. `witness_interest_in_case` — keyword (family|financial|neutral)
8. `judgment_reasoning_quality` — keyword (thorough|adequate|superficial|contradictory)
9. `fir_discrepancies_with_testimony` — keyword[] (location_changed|weapon_different|accused_count_changed)
10. `investigation_defect_description` — keyword[] (witness_not_examined|scene_not_visited|evidence_not_collected)

**Full list of restored LLM-reasoned fields:**

#### Offense Classification
- `murder_category` — keyword (qatal_i_amd|khata|azhar)
- `premeditation_indicators` — keyword[] (prior_enmity|weapon_procurement|planning_evidence)
- `provocation_claimed` — bool
- `abetment_type` — keyword (instigator|conspirator|aid_provider)
- `cnsa_quantity_classification` — keyword (personal|commercial|trafficking)
- `recovery_circumstances` — keyword (lawful_warrant|warrantless|consent|contested)

#### Parties & Credibility
- `accused_age_at_offense` — integer
- `criminal_history_count` — integer
- `complainant_relation_to_victim` — keyword
- `complainant_motive_bias` — keyword[] (family_enmity|land_dispute|revenge)
- `witness_interest_in_case` — keyword
- `witness_relationship_to_parties` — keyword
- `witness_impeachment_ground` — keyword[] (prior_inconsistent|interest|bias|enmity)
- `accomplice_testimony_corroboration` — bool
- `conflicting_expert_opinions` — bool

#### Evidence Assessment
- `motive_strength` — keyword
- `motive_proven` — bool
- `alibi_evidence_strength` — keyword (strong|weak|none)
- `presence_at_crime_scene` — keyword (confirmed|likely|unproven)
- `last_seen_together_evidence` — bool
- `consciousness_of_guilt_evidence` — keyword[] (fled|destroyed_evidence|bribed_witness)
- `recovery_from_possession` — bool
- `pm_report_quality` — keyword (detailed|standard|minimal)
- `injury_count` — integer
- `injury_severity` — keyword (fatal|grievous|simple)
- `weapon_forensic_tested` — bool
- `hearsay_exception_applied` — keyword (dying_declaration|res_gestae|admission)
- `evidence_illegally_obtained` — bool
- `similar_fact_evidence` — bool
- `expert_opinion_overruled` — bool
- `accused_prior_criminal_convictions` — bool

#### Procedural Assessment
- `fir_discrepancies_with_testimony` — keyword[]
- `investigation_defect_description` — keyword[]
- `section_164_voluntariness_challenged` — bool
- `section_164_officer_present` — keyword (police_absent|police_present_violation)
- `police_brutality_fir` — bool
- `fir_based_on_suspicion_only` — bool
- `defense_adequate` — keyword (thorough|adequate|inadequate)
- `charges_framed_properly` — bool
- `cross_examination_quality_assessment` — keyword
- `eyewitness_visibility_conditions` — keyword (daylight|twilight|darkness)
- `eyewitness_familiarity_with_accused` — keyword (familiar|stranger)
- `eyewitness_identification_procedure_defects` — keyword[]

#### Sentencing Assessment
- `prosecution_strength_rating` — keyword
- `conviction_certainty` — keyword (beyond_reasonable_doubt|benefit_of_doubt)
- `conviction_strength` — keyword
- `brutality_level` — keyword (extreme|moderate|minimal)
- `victim_vulnerability` — keyword (child|elderly|disabled|none)
- `provocation_evidence_weight` — keyword (grave|minor|none)
- `mental_illness` — bool
- `intoxication_at_time` — bool
- `cooperation_with_prosecution` — bool
- `remorse_shown` — bool
- `first_offense` — bool

#### Strategy & Patterns
- `defense_strategy_primary` — keyword
- `prosecution_strategy_primary` — keyword
- `self_defense_claimed` — bool
- `insanity_plea` — bool
- `confession_voluntary` — bool
- `confession_corroborated` — bool
- `confessional_statement` — bool
- `honor_crime_defense` — bool
- `honor_crime_motive` — keyword
- `sexual_offense_type` — keyword
- `victim_delay_reporting` — integer
- `sectarian_violence_case` — bool
- `rape_murder_combined` — bool
- `grounds_for_appeal_list` — keyword[]
- `defect_fatal_to_conviction` — bool
- `defects_cumulatively_fatal` — bool
- `eyewitness_sole_evidence` — bool
- `reasonable_doubt_not_applied_ground` — bool
- `judgment_reasoning_quality` — keyword

### Tier C: Reasoning Points (vector text, not payload) — ~35 fields
Stored as separate vectors in `pk_legal_principles` and `pk_evidence_patterns` collections:

- `cause_of_death_description` — forensic narrative
- `injury_pattern_analysis` — pathology findings
- `dying_declaration_content` — verbatim quote
- `accused_342_statement` — accused's own statement
- `provocation_evidence` — what provoked the accused
- `motive_evidence` — evidence items proving motive
- `recovery_explanation` — accused's account
- `knowledge_only_culprit_would_have` — "secret knowledge" items
- `sentence_justification_leniency` — reasoning for lenient sentence
- `fir_discrepancy_details` — specific contradictions (full text)
- `investigation_defect_details` — specific gaps (full text)
- `expert_findings_key` — direct quotes from expert reports
- `accomplices_details` — co-accused names, roles, statuses
- `witness_admission_during_cross` — specific admissions
- `points_for_determination` — CrPC 367 mandated legal questions
- `ratio_decidendi` — binding legal principle
- `operative_order_text` — the actual court order

## Correctly Cut (STAY CUT) — ~195 fields

All 0-100 numeric scores, exact measurements (meters, seconds, minutes), per-witness granular attributes, trial record minutiae (evidence sealing, recovery memo photos), external data fields (IO prior acquittals, accused address/DOB), duplicates across sections, and non-discriminating fields (always true/false).

## Implementation Note

For Qdrant payload, the LLM extraction pipeline should:
1. First pass: regex/NER for Tier A fields (fast, high confidence)
2. Second pass: LLM reasoning for Tier B fields (slower, medium-high confidence)
3. Third pass: LLM extraction for Tier C reasoning points (stored as separate vectors)

Each Tier B field should include a `_confidence` companion field (high|medium|low) so downstream agents know how much to trust the classification.
