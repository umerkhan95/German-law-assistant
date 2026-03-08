# Pakistan Legal AI System: Critical Datapoints from Court Judgments

**Author's Note**: This is a comprehensive extraction of datapoints from Pakistani court judgments in Constitutional Law, Tax Law, and Labour Law. Each datapoint is catalogued with field name, data type, strategic importance, and example values.

**Generated**: March 8, 2026
**Research Sources**: PLD (Pakistan Legal Decisions), Supreme Court judgments, ATIR, NIRC, High Court decisions, case law databases

---

## I. CONSTITUTIONAL LAW DATAPOINTS

### A. FUNDAMENTAL RIGHTS PETITIONS (Articles 8-28)

#### Article 8: Void Laws Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `petition_type` | enum | Categorizes remedy sought | "Article_8_void_law", "Article_9_liberty", "Article_10_safety", "Article_11_slavery", "Article_12_forced_labour", "Article_14_dignity", "Article_15_freedom_assembly", "Article_16_freedom_association", "Article_17_freedom_movement", "Article_18_freedom_profession", "Article_19_freedom_expression", "Article_20_freedom_religion", "Article_21_minority_education", "Article_23_property_rights", "Article_25_non_discrimination", "Article_28_islamic_way_of_life" |
| `fundamental_right_claimed` | string | Identifies which right allegedly violated | "right_to_life", "right_to_dignity", "right_to_assembly", "right_to_conscience", "right_to_property", "right_to_education" |
| `law_challenged` | string | Statute/regulation deemed inconsistent | "Income Tax Ordinance 2001 Section 111", "Criminal Procedure Code Section 144", "Employment law provision" |
| `alleged_inconsistency_type` | enum | Nature of constitutional breach | "abridges_right", "takes_away_right", "in_derogation_of_right", "arbitrary_application", "disproportionate_restriction" |
| `court_declaration_status` | enum | Supreme Court ruling on validity | "declared_void", "upheld_valid", "conditionally_valid_with_interpretation", "remanded_for_reconsideration", "partially_struck_down" |
| `interpretation_applied` | enum | Constitutional reading principle used | "strict_construction", "purposive_interpretation", "literal_reading", "harmonious_construction", "presumption_of_constitutionality", "fundamental_rights_primacy" |
| `relief_granted` | enum | Specific remedy awarded | "struck_down_law", "injunction_issued", "declaration_of_nullity", "direction_to_legislature_amend", "direction_to_executive_cease", "damages_awarded", "reinstatement_ordered", "remission_ordered" |

#### Article 184(3) Constitution Petition Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `petition_identifier` | string | Unique case ID | "CP 1418/2023", "CP D-3309/2011", "CP 648-L/2021" |
| `locus_standi_category` | enum | Establishes petitioner eligibility | "aggrieved_party", "public_interest_litigant", "affected_group", "civil_society_organization", "union_representative", "constitutional_right_holder" |
| `public_importance_threshold_met` | boolean | Gate-keeping requirement | true, false |
| `public_importance_justification` | string | Why Supreme Court should exercise jurisdiction | "impacts_fundamental_rights_of_millions", "systemic_governance_failure", "inter_provincial_dispute", "policy_affecting_national_interest", "test_case_precedent_value" |
| `fundamental_right_invoked` | array | Articles 8-28 implicated | ["Article_14_dignity", "Article_18_profession", "Article_25_non_discrimination"] |
| `pre_petition_remedies_exhausted` | enum | Alternative forum availability | "no_adequate_remedy_exists", "high_court_jurisdiction_pending", "administrative_forum_ineffective", "tribunal_pending", "legislature_recourse_futile" |
| `question_of_law_status` | enum | Distinguishes law vs. fact | "pure_question_of_law", "mixed_question_law_and_fact", "constitutional_interpretation", "statutory_construction", "judicial_review_scope" |
| `admissibility_decision` | enum | Petition maintenance ruling | "maintainable", "not_maintainable", "rejected_for_locus_standi", "rejected_for_non_exhaustion", "rejected_as_academic" |
| `petition_outcome` | enum | Final disposition | "granted_with_relief", "allowed_in_part", "dismissed", "disposed_with_direction", "remanded_to_high_court" |
| `bench_size` | integer | Number of judges deciding | 3, 5, 7, 11, 17 |
| `dissenting_opinions` | integer | Judges disagreeing | 0, 1, 2, 3+ |
| `grounds_for_denial` | array | Why petition dismissed (if applicable) | ["lack_of_jurisdiction", "alternative_remedy_available", "failed_public_importance", "nonjusticiability", "academic_interest_only"] |

#### Judicial Review Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `review_ground_invoked` | enum | Constitutional basis for challenge | "ultra_vires", "procedural_fairness_violation", "irrationality", "proportionality_breach", "discrimination", "natural_justice_denial", "fettering_discretion", "bad_faith", "mala_fides", "patent_illegality" |
| `authority_reviewed` | enum | Entity whose action challenged | "executive_decision", "administrative_order", "legislative_act", "subordinate_court_judgment", "quasi_judicial_tribunal_order", "statutory_body_action" |
| `applicability_of_natural_justice` | enum | Procedural fairness requirement | "audi_alteram_partem_required", "justice_must_appear_done", "hearing_before_dismissal", "reasoned_order_mandatory", "bias_avoidance_essential", "notice_and_opportunity_mandatory" |
| `irrationality_test_applied` | enum | Wednesbury reasonableness standard | "Wednesbury_unreasonableness", "absurdity_manifest", "no_reasonable_authority_would_decide_so", "decision_outside_range_of_rational_choices", "satisfies_rationality" |
| `proportionality_analysis_conducted` | boolean | Means-ends testing | true, false |
| `proportionality_result` | enum | Outcome of proportionality test | "measure_proportionate", "disproportionately_burdensome", "less_restrictive_means_available", "not_necessary_in_democratic_society", "fails_balancing_test" |
| `discrimination_head_claimed` | enum | Basis of discriminatory treatment | "religion", "caste", "gender", "ethnicity", "political_opinion", "socioeconomic_status", "origin", "language", "arbitrary_classification" |
| `discrimination_finding` | enum | Court ruling on equality breach | "discrimination_proven", "no_discrimination_evident", "discrimination_justified", "classification_reasonable", "fails_strict_scrutiny" |
| `standard_of_review_applied` | enum | Level of judicial deference | "strict_scrutiny", "intermediate_scrutiny", "rational_basis_test", "manifest_absurdity", "patent_illegality", "heightened_rationality" |
| `decision_outcome` | enum | Administrative action judgment | "decision_quashed", "decision_upheld", "decision_remitted_for_reconsideration", "order_partially_quashed", "order_suspended_pending_reconsideration" |

### B. WRIT JURISDICTION (Article 199) DATAPOINTS

#### Writ Type Classification Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `writ_type` | enum | Specifies remedy sought | "habeas_corpus", "mandamus", "certiorari", "prohibition", "quo_warranto" |
| `writ_type_specific_purpose` | string | Legal object of writ | "habeas_corpus: unlawful detention release", "mandamus: compel statutory duty", "certiorari: quash ultra vires decision", "prohibition: prevent jurisdiction excess", "quo_warranto: challenge public office qualification" |

#### Habeas Corpus Specific Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `detention_type` | enum | Nature of confinement | "police_custody", "judicial_custody", "administrative_detention", "military_custody", "extra_judicial_detention", "preventive_detention" |
| `detention_legality_status` | enum | Lawfulness of detention | "lawful_detention", "unlawful_detention", "detention_without_warrant", "detention_exceeds_authority", "detention_lacks_due_process" |
| `detaining_authority` | enum | Who holds detainee | "law_enforcement", "prison_authority", "military_command", "intelligence_agency", "administrative_official", "private_person" |
| `procedural_deficiency_found` | array | Process violations | ["no_arrest_warrant", "no_FIR_filed", "no_judicial_custody_order", "miranda_rights_not_read", "access_to_counsel_denied", "family_notification_withheld"] |
| `relief_in_habeas_corpus` | enum | Writ outcome | "detainee_released", "release_with_conditions", "detention_declared_illegal", "officer_held_in_contempt", "compensation_ordered", "case_remitted" |
| `court_order_enforcement` | enum | Implementation status | "order_complied", "order_appealed", "order_partially_complied", "contempt_proceedings_initiated", "appeal_suspended_order" |

#### Mandamus Specific Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `statutory_duty_type` | enum | Category of obligation | "ministerial_duty", "discretionary_duty_with_limits", "statutory_direction", "constitutional_obligation", "administrative_responsibility" |
| `duty_definition` | string | Specific obligation required | "issue_license_under_law", "process_application_within_timeframe", "conduct_election_as_mandated", "deliver_document_held", "implement_court_order" |
| `duty_is_ministerial` | boolean | No discretion involved | true, false |
| `failure_type` | enum | Why authority refused | "refused_entirely", "delayed_unreasonably", "imposed_conditions_not_authorized", "exceeded_discretion_bounds", "acted_in_bad_faith" |
| `mandamus_grant_decision` | enum | Court ruling | "mandamus_granted", "mandamus_denied_discretion_exists", "mandamus_denied_alternative_remedy", "mandamus_granted_with_conditions", "mandamus_conditional_on_compliance" |
| `enforcement_mechanism` | enum | How compliance ensured | "order_issued", "time_frame_imposed", "contempt_power_reserved", "automatic_consequence_spelled", "progressive_contempt_hearings" |

#### Certiorari Specific Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `lower_tribunal_type` | enum | Forum whose order challenged | "administrative_tribunal", "quasi_judicial_body", "licensing_authority", "statutory_board", "subordinate_court", "departmental_authority" |
| `tribunal_jurisdiction_basis` | string | Source of tribunal's authority | "Administrative Tribunal Act", "Income Tax Ordinance Section 121", "Industrial Relations Act Section 57", "customs_regulation", "statutory_instrument" |
| `jurisdiction_excess_alleged` | boolean | Ultra vires claim | true, false |
| `jurisdiction_excess_types` | array | Categories of excess | ["acted_beyond_powers", "wrong_test_applied", "irrelevant_consideration", "material_evidence_ignored", "irrational_finding", "law_misunderstood"] |
| `natural_justice_breach_alleged` | boolean | Procedural fairness violation | true, false |
| `natural_justice_defect_type` | array | Specific procedural failures | ["no_hearing_provided", "biased_tribunal", "conflicting_interest", "reasoning_not_provided", "evidence_not_considered", "statutory_procedure_violated"] |
| `law_misinterpretation_alleged` | boolean | Substantive legal error | true, false |
| `certiorari_ground_established` | enum | Which defect proven | "jurisdiction_exceeded", "natural_justice_denied", "law_misapplied", "evidence_ignored", "tribunal_biased", "procedure_not_followed" |
| `certiorari_outcome` | enum | Writ result | "order_quashed", "order_upheld", "order_quashed_remitted_retrial", "order_partially_quashed", "certiorari_refused_alternative_remedy" |
| `remittal_direction` | string | If remitted, specific instructions | "retrial_by_tribunal", "reconsideration_with_directions", "application_of_correct_law", "consideration_of_new_evidence" |

#### Prohibition Specific Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `prohibited_action_type` | enum | What court forbidden from doing | "continuing_proceedings_without_jurisdiction", "violating_natural_justice", "applying_void_law", "exceeding_delegated_powers", "hearing_res_judicata_matter" |
| `respondent_tribunal` | enum | Court/tribunal being prohibited | "subordinate_court", "administrative_tribunal", "quasi_judicial_body", "licensing_board", "departmental_tribunal", "military_court" |
| `imminence_of_harm` | enum | Urgency level | "already_occurred", "imminent_threat", "concrete_risk", "speculative_future_harm" |
| `alternative_remedy_inadequacy` | boolean | Why prohibition necessary | true, false |
| `prohibition_granted` | boolean | Writ issued | true, false |
| `conditions_imposed` | array | Limitations on prohibition | ["lifting_if_circumstances_change", "subject_to_compliance_with_law", "without_prejudice_to_appellate_remedy"] |

#### Quo Warranto Specific Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `public_office_held` | string | Position challenged | "judicial_appointment", "administrative_office", "statutory_authority_head", "licensing_board_member", "government_official_position" |
| `legality_ground_challenged` | enum | Why appointment contested | "improper_appointment_procedure", "disqualification_not_removed", "conflict_of_interest", "statutory_prerequisite_missing", "fraud_in_appointment", "conditional_appointment_lapsed" |
| `statutory_qualification_required` | array | Legal prerequisites | ["minimum_experience_years", "educational_qualification", "professional_license", "citizenship_requirement", "age_limit", "clean_character_certificate", "financial_integrity"] |
| `qualification_deficiency` | array | Lacking qualifications | ["no_required_degree", "insufficient_experience", "criminal_conviction", "professional_delinquency", "citizenship_status_suspect", "age_exceeds_limit"] |
| `appointment_procedure_violation` | array | Process defects | ["competitive_process_bypassed", "advertised_posts_unfilled", "merit_ignored", "panel_composition_violated", "consultation_requirement_breached"] |
| `quo_warranto_success` | boolean | Writ granted | true, false |
| `office_vacancy_declared` | boolean | Position declared void | true, false |
| `person_removed_from_office` | boolean | Ousted from position | true, false |
| `relief_granted` | enum | Outcome | "office_declared_vacant", "person_removed", "appointment_voided", "quo_warranto_dismissed_appointment_valid" |

#### Alternative Remedy Doctrine Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `alternative_remedy_exists` | boolean | Other legal recourse available | true, false |
| `alternative_remedy_type` | enum | Nature of alternative forum | "statutory_appeal", "internal_appeal", "administrative_tribunal", "specialized_court", "statutory_review", "constitutional_petition_before_high_court" |
| `remedy_adequacy_assessment` | enum | Whether alternative sufficient | "remedy_adequate_effectual", "remedy_inadequate_slow", "remedy_inadequate_insufficient_power", "remedy_adequate_but_not_exclusive", "exclusive_remedy_exists" |
| `remedy_accessibility` | enum | Practical availability | "accessible_affordable", "inaccessible_cost_prohibitive", "legally_barred_from_accessing", "practically_futile", "available_but_delayed" |
| `remedy_expedience` | enum | Speed of resolution | "expeditious_decision", "prolonged_delays_expected", "uncertain_timeline", "faster_writ_remedy", "parallel_proceedings_allowed" |
| `adequacy_doctrine_applied` | boolean | Test invoked | true, false |
| `exception_to_adequacy` | enum | When writ allowed despite remedy | "constitutional_question_involved", "patent_illegality_apparent", "principles_of_natural_justice", "fundamental_right_violation", "public_law_issue" |
| `writ_maintainability_decision` | enum | Petition admitted/rejected | "maintainable_alternative_remedy_not_bar", "maintainable_no_adequate_remedy", "not_maintainable_remedy_available", "maintainable_with_conditions" |

### C. FEDERAL vs. PROVINCIAL JURISDICTION DATAPOINTS

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `dispute_subject_matter` | enum | What's being contested | "taxation_authority", "commercial_regulation", "health_service_provision", "education_policy", "labor_law_applicability", "environmental_standards", "land_administration" |
| `constitutional_list_source` | enum | Which Schedule IV entry | "federal_legislative_list_entry", "concurrent_legislative_list_entry", "provincial_legislative_list_entry", "residual_power_federal", "residual_power_provincial" |
| `federal_list_entry` | string | Federal entry number | "Entry 45: taxation", "Entry 32: customs", "Entry 33: excise", "Entry 42: copyright_patents" |
| `concurrent_list_entry` | string | Shared power entry | "Entry 12: social_security_welfare", "Entry 13: public_health_sanitation", "Entry 15: labour_relations", "Entry 17: agriculture" |
| `provincial_list_entry` | string | Provincial entry number | "Entry 3: local_government", "Entry 5: agriculture", "Entry 32: education", "Entry 41: municipal_services" |
| `legislative_authority_competing` | enum | Who has power | "federal_government", "provincial_government", "both_concurrent", "federal_exclusive", "provincial_exclusive" |
| `overlap_conflict_type` | enum | Nature of clash | "direct_contradiction", "operational_conflict", "overlapping_subject_matter", "delegation_question", "paramountcy_issue" |
| `paramountcy_doctrine_applied` | boolean | Federal law prevails | true, false |
| `federal_law_declared_paramount` | boolean | Federal law upheld | true, false |
| `court_jurisdiction_determination` | enum | Which court decides | "Supreme_Court_exclusive", "High_Court_can_decide", "forum_not_relevant", "matter_not_justiciable" |
| `dispute_resolution_outcome` | enum | Who wins | "federal_authority_upheld", "provincial_authority_upheld", "federal_law_void_to_extent_conflict", "provincial_law_void_to_extent_conflict", "harmonious_interpretation_attempted" |
| `constitutional_amendment_context` | enum | Impact of 18th Amendment | "18th_Amendment_devolution_applied", "pre_18th_Amendment_law", "post_18th_Amendment_transition", "concurrent_list_affected" |

### D. 18TH AMENDMENT IMPLICATIONS DATAPOINTS

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `amendment_date` | date | When 18th Amendment passed | "2010-05-19" |
| `power_devolved_from_federal` | array | Centers devolved to provinces | ["health", "education", "agriculture", "local_government", "social_welfare", "public_works"] |
| `judicial_review_of_18th` | boolean | Whether amendment judicially reviewed | true, false |
| `amendment_article_challenged` | enum | Which clause contested | "basic_structure_doctrine", "anti_defection_clause", "judicial_appointment_alteration", "constitutional_power_shift" |
| `judicial_review_success` | enum | Court ruling on amendment | "amendment_upheld_valid", "amendment_partially_struck_down", "amendment_suspended_pending_consideration", "amendment_valid_correct_procedure_followed" |
| `case_cited` | string | Leading judgment | "District Bar Association Rawalpindi v Federation (2015)" |
| `basic_structure_invoked` | boolean | Unamendable features test | true, false |
| `18th_Amendment_implementation_status` | enum | Degree of compliance | "fully_implemented", "partially_implemented", "delayed_implementation", "subject_of_ongoing_litigation" |
| `provincial_authority_expanded` | array | Powers gained by provinces | ["concurrent_list_entries", "health_administration", "education_oversight", "labour_relations", "social_welfare_programs"] |

### E. MILITARY COURT REVIEW DATAPOINTS

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `military_court_jurisdiction` | enum | Scope of authority | "military_personnel_only", "civilians_allowed", "national_security_offences", "terrorism_charges", "constitutional_offences" |
| `subject_matter_jurisdiction` | enum | Type of offense | "military_discipline", "terrorism", "high_treason", "sedition", "civil_offence", "hybrid_civil_military" |
| `petitioner_status` | enum | Who challenging | "accused_person", "family_member", "constitutional_right_holder", "bar_association", "civil_society_organization" |
| `grounds_for_challenge` | array | Constitutional objections | ["violation_due_process", "denial_fair_trial", "no_civilian_trial_right", "violation_fundamental_rights", "ultra_vires_establishment", "violation_natural_justice"] |
| `civilian_trial_guarantee` | boolean | Rights of non-military | true, false |
| `judicial_review_precedent_case` | string | Landmark decision | "Jawwad S. Khawaja v Federation (2023/2025)" |
| `military_court_authority_scope` | enum | Post-review ruling | "military_courts_unconstitutional", "military_courts_valid_limited_scope", "only_military_personnel_triable", "civilians_exclusive_civil_courts" |
| `appeal_to_military_commission` | enum | Higher review body | "military_appeals_allowed", "supreme_court_jurisdiction", "civilian_court_appellate_review", "no_appellate_review_available" |
| `death_penalty_imposition_allowed` | boolean | Capital punishment | true, false |
| `constitutional_amendment_context` | enum | Relevant amendments | "26th_Amendment_restored_military_courts", "27th_Amendment_military_immunity" |

### F. ELECTION PETITION DATAPOINTS

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `election_level` | enum | Office type | "national_assembly", "provincial_assembly", "local_government", "senate", "intra_party_election" |
| `election_type` | enum | Electoral process | "general_election", "by_election", "local_body_election", "party_leadership_election", "internal_party_election" |
| `petition_grounds` | array | Basis for challenge | ["electoral_malpractice", "fraud_in_counting", "invalid_votes_counted", "valid_votes_rejected", "disqualification_issue", "candidacy_dispute", "results_manipulation", "election_commission_misconduct"] |
| `petitioner_status` | enum | Who challenges | "defeated_candidate", "election_commission", "political_party", "affected_voter", "bar_association" |
| `respondent_status` | enum | Who's challenged | "elected_candidate", "election_commission", "returning_officer", "political_party" |
| `specific_allegation` | string | Concrete complaint | "Constituency NA-120: 5000 votes from ineligible voters counted", "Provincial Assembly election: invalid marks on ballots", "Municipal election: phantom voters in polling station 23" |
| `evidence_presented` | array | Proof offered | ["affidavit_testimony", "documentary_evidence", "expert_forensic_analysis", "witness_testimony", "polling_agent_reports", "presiding_officer_statement"] |
| `grounds_succeed_fail` | enum | Success rate | "petition_granted", "petition_partially_allowed", "petition_dismissed", "petition_allowed_candidate_unseated", "petition_allowed_election_annulled" |
| `election_tribunal_jurisdiction` | enum | Forum competent | "High_Court", "Election_Commission", "Specialized_Election_Tribunal", "District_Judge", "session_court" |
| `appellate_recourse` | enum | Higher review | "appeal_to_high_court", "appeal_to_supreme_court", "no_further_appeal", "limited_supreme_court_review" |
| `grounds_never_succeed` | array | Rejected claims | ["post_election_policy_disagreement", "political_opinion_differences", "allegation_without_evidence", "claim_after_time_limit", "not_justiciable_matter"] |
| `time_limit_for_petition` | string | Filing deadline | "30_days_from_results_announcement", "45_days_from_notification", "statutory_period_strict" |

### G. CONSTITUTIONAL INTERPRETATION PRINCIPLES DATAPOINTS

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `interpretation_methodology` | enum | Reading technique applied | "literal_construction", "purposive_interpretation", "harmonious_construction", "strict_construction", "contextual_interpretation", "comparative_constitutional_law", "plain_meaning_rule" |
| `literal_vs_purposive` | enum | Words or intent | "literal: apply_exact_words", "purposive: effectuate_purpose", "hybrid: context_determines", "golden_rule: avoid_absurdity" |
| `preamble_invocation` | boolean | Referenced document objectives | true, false |
| `preamble_text_invoked` | string | Which preamble purpose | "democratic_accountability", "islamic_principles", "federalism", "provincial_autonomy", "rule_of_law", "justice_liberty_equality" |
| `constitutional_object_cited` | enum | Living document principle | "constitution_not_static", "evolving_interpretation", "contemporary_application", "dead_letter_construction", "dynamic_understanding" |
| `precedent_weight` | enum | Stare decisis application | "previous_bench_overruled", "previous_bench_distinguished", "previous_bench_followed", "conflicting_precedents_reconciled", "leading_case_reaffirmed" |
| `international_law_reference` | boolean | Treaty/convention cited | true, false |
| `international_instrument_cited` | array | Which treaties invoked | ["ICCPR", "CEDAW", "ILO_conventions", "UDHR", "regional_human_rights"] |
| `comparative_jurisprudence_cited` | array | Other countries' precedents | ["India_constitution", "UK_common_law", "US_constitution", "Canadian_charter", "Australian_precedent"] |
| `presumption_applied` | enum | Default rule used | "presumption_of_constitutionality", "presumption_of_legislative_competence", "presumption_of_regularity", "doubt_favors_fundamental_rights", "burden_on_state_justify_restriction" |
| `basic_structure_doctrine` | boolean | Unamendable features test | true, false |
| `basic_structure_elements` | array | Core features | ["republicanism", "federalism", "parliamentary_democracy", "fundamental_rights", "supremacy_of_constitution", "judicial_review", "rule_of_law", "separation_of_powers"] |
| `basic_structure_invoked_successfully` | boolean | Doctrine applied to strike down | true, false |

### H. INTRA-COURT APPEAL DATAPOINTS

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `intra_court_appeal_jurisdiction` | enum | Appeal within same court | "High_Court_single_judge_to_bench", "appellate_bench_review_single_judge", "limited_review_scope" |
| `original_decision_judge_type` | enum | Who made initial order | "single_judge", "two_judge_bench", "three_judge_bench" |
| `appeal_bench_size` | integer | Judges reviewing | 2, 3, 5 |
| `appeal_scope_limitation` | enum | What can be reviewed | "error_apparent_on_face", "review_only_not_appeal", "limited_to_procedural_issues", "limited_to_law_not_facts", "narrow_review_scope", "substantial_question_of_law" |
| `statutory_basis` | enum | Authority for appeal | "Law_Reforms_Ordinance_1972", "High_Court_Rules", "Constitution_Article_199", "Procedural_Code_provision" |
| `error_categories_reviewable` | array | What can trigger review | ["perversity_of_order", "misinterpretation_of_law", "ignoring_material_evidence", "misconduct_in_procedure", "violation_natural_justice", "jurisdiction_exceeded", "manifest_error" |
| `bench_can_substitute_judgment` | boolean | Can overrule single judge | false |
| `review_petition_grounds` | enum | Basis for review | "discovered_new_evidence", "fraud_or_perjury", "manifest_error_of_law", "violation_natural_justice", "wrong_bench_precedent_applied" |
| `review_success_rate` | enum | Likelihood of success | "rarely_succeed", "limited_circumstances_only", "exceptionally_allowed", "procedural_safeguard_only" |

### I. PRESIDENTIAL REFERENCES (Article 186) DATAPOINTS

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `reference_type` | enum | Kind of presidential request | "constitutional_question_advice", "legal_opinion_sought", "public_importance_issue", "jurisdictional_doubt" |
| `constitutional_question_posed` | string | Question referred | "Is military court jurisdiction consistent with Constitution?", "Can executive amend tax laws?", "Does provincial assembly have power X?" |
| `public_importance_threshold` | boolean | Must meet public importance | true |
| `supreme_court_obligation` | enum | Whether compelled to answer | "must_advise_president", "discretionary_acceptance", "can_refuse_hypothetical", "can_decline_justiciability_issue" |
| `reference_admissibility` | enum | Accepted for consideration | "reference_admitted", "reference_declined_hypothetical", "reference_declined_justiciability", "reference_admitted_limited_scope" |
| `advisory_opinion_binding` | boolean | Legally binding force | false |
| `advisory_opinion_precedential` | boolean | Persuasive authority | true |
| `legislature_binding_effect` | enum | Parliamentary obligation | "legislature_may_ignore", "legislature_must_consider", "no_legal_obligation", "moral_political_obligation" |
| `executive_binding_effect` | enum | Executive obligation | "executive_may_ignore", "executive_bound_advise_president", "no_legal_obligation", "advice_informational" |

---

## II. TAX LAW DATAPOINTS

### A. INCOME TAX ORDINANCE 2001 DATAPOINTS

#### Assessment Procedure Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `assessment_year` | string | Year of assessment | "2024", "2023", "Tax_Year_FY2023-24" |
| `tax_year_period` | string | Revenue period assessed | "July_2023_June_2024", "Jan_2023_Dec_2023", "FY2024" |
| `assessee_ntn` | string | National Tax Number | "1234567-8" |
| `assessee_category` | enum | Type of taxpayer | "individual", "company", "partnership", "association_persons", "joint_venture", "trust", "ngo", "non_resident" |
| `income_source_category` | enum | Income origin | "salary_wages", "business_profit", "capital_gain", "rental_income", "agricultural_income", "other_income", "exempt_income" |
| `notice_section_issued` | enum | Legal basis for notice | "Section_114_initial_notice", "Section_115_survey_follow_up", "Section_120_best_judgment", "Section_121_best_judgment_revised", "Section_147_belated_assessment", "Section_148_reassessment_omission_or_error" |
| `notice_issued_date` | date | When notice sent | "2024-01-15" |
| `assessee_response_date` | date | Assessee reply filed | "2024-02-20" |
| `response_adequacy` | enum | Quality of response | "adequate_complete", "inadequate_missing_evidence", "non_response_default", "partially_responsive", "belatedly_filed" |
| `assessment_order_issued` | boolean | Order passed | true, false |
| `assessment_order_date` | date | When order pronounced | "2024-03-15" |
| `tax_assessed_amount_pkr` | integer | Taxable income determined | 5000000, 25000000, 100000000 |
| `tax_liability_amount_pkr` | integer | Total tax payable | 500000, 2500000, 5000000 |
| `penalty_amount_pkr` | integer | Penalty imposed | 0, 100000, 1000000 |
| `penalty_section_imposed` | enum | Legal basis for penalty | "Section_224_failure_to_file", "Section_226_false_statement", "Section_228_improper_record_keeping", "Section_229_failure_furnish_required_info", "Section_282_evasion_or_avoidance", "Section_282A_concealment_income" |
| `interest_amount_pkr` | integer | Late payment interest | 50000, 200000, 500000 |
| `interest_calculation_period` | string | Date range for interest | "2023-06-01_to_2024-03-15" |
| `addition_to_income` | integer | Income added under survey/assessment | 1000000, 5000000, 20000000 |
| `addition_reason` | enum | Basis for addition | "unexplained_source_funds", "cash_evidence", "discrepancy_accounts_statements", "undervaluation_assets", "transfer_pricing_adjustment", "depreciation_disallowance", "expense_disallowance" |
| `depreciation_claimed` | integer | Claimed depreciation amount | 500000, 2000000 |
| `depreciation_allowed` | integer | Allowed depreciation | 400000, 1500000 |
| `depreciation_disallowed` | integer | Rejected depreciation | 100000, 500000 |
| `expense_category_disputed` | array | Types of expenses challenged | ["travel_entertainment", "vehicle_maintenance", "professional_fees", "advertising", "repair_maintenance", "utilities", "staff_costs"] |
| `expense_claimed_pkr` | integer | Expenses asserted | 500000, 2000000, 5000000 |
| `expense_allowed_pkr` | integer | Expenses accepted | 400000, 1500000, 4000000 |
| `expense_disallowed_pkr` | integer | Expenses rejected | 100000, 500000, 1000000 |
| `disallowance_reason` | enum | Why expense rejected | "personal_nature_not_business", "excessive_amount", "no_supporting_documentation", "not_business_necessity", "prohibited_by_law", "against_public_policy", "lavish_wasteful" |
| `record_keeping_deficiency` | array | Documentation issues | ["no_receipts_maintained", "accounts_not_balanced", "false_invoices_created", "records_destroyed", "alternative_books_maintained"] |
| `assessment_finality_status` | enum | Order bindingness | "order_final_no_appeal", "appeal_possible_commissioner", "appeal_possible_tribunal", "appeal_possible_high_court", "under_appeal_not_final" |

#### Section 111 - Income or Asset Addition Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `section_111_applicability` | boolean | Provision invoked | true, false |
| `section_111_notice_issued` | boolean | Show cause notice issued | true, false |
| `notice_issue_date_section_111` | date | When notice sent | "2023-12-01" |
| `clause_invoked` | enum | Which clause applied | "clause_1_unexplained_sources", "clause_2_cash_evidence", "clause_3_failure_explain_discrepancy", "clause_4_failure_explain_acquisition", "clause_5_failure_explain_investment" |
| `income_or_asset_claimed` | string | What's being added | "Unexplained cash of PKR 5 million", "Investment in property without source", "Bank deposit without explanation", "Gift allegedly from unknown person" |
| `assessee_explanation_provided` | boolean | Response given | true, false |
| `explanation_adequacy` | enum | Quality of response | "satisfactory_explanation", "unsatisfactory_insufficient", "no_explanation_given", "explanation_not_believable", "partial_explanation" |
| `addition_ground` | enum | Specific section 111 basis | "money_stock_securities_found", "investment_property_found", "expenditure_incurred_source_not_traced", "acquisition_asset_source_not_traced", "gift_loans_not_explained" |
| `addition_amount_final_pkr` | integer | Final addition amount | 1000000, 5000000, 50000000 |
| `burden_of_proof` | enum | Who proves what | "assessee_prove_legality", "revenue_prove_illegality", "balanced_burden", "assessee_initial_burden", "shifting_burden" |
| `addition_upheld_on_appeal` | enum | Appeal outcome | "addition_upheld", "addition_reduced_partially", "addition_deleted_entirely", "addition_modified", "addition_remitted_reconsideration" |

#### Section 122 - Best Judgment Assessment Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `section_122_invoked` | boolean | Best judgment assessment | true, false |
| `section_111_order_precedent` | boolean | Section 111 order first | true, false |
| `sequential_procedure_followed` | boolean | Correct order observed | true, false |
| `section_122_show_cause_date` | date | When SCN issued | "2024-02-15" |
| `grounds_for_bja` | enum | Why best judgment used | "assessee_failed_respond_section_114", "response_inadequate_unsatisfactory", "books_not_maintained", "return_not_filed", "return_incorrect", "discrepancy_cannot_be_resolved" |
| `assessing_officer_estimate` | integer | Officer's income calculation | 10000000, 25000000, 50000000 |
| `estimation_methodology` | enum | How income estimated | "comparison_similar_assessee", "percentage_of_turnover", "deemed_profit_rate", "mathematical_imputation", "precedent_case_application", "expert_opinion_relied" |
| `estimation_reasonable_basis` | boolean | Objective data used | true, false |
| `estimated_income_upheld_appeal` | enum | Appellate result | "estimate_upheld", "estimate_reduced", "estimate_increased", "estimate_substituted_different_methodology", "estimate_deleted_remitted" |

#### Provisional Assessment Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `provisional_assessment_issued` | boolean | Provisional order passed | true, false |
| `provisional_order_date` | date | When issued | "2023-12-31" |
| `provisional_tax_amount_pkr` | integer | Provisional liability | 1000000, 5000000 |
| `provisional_security_deposit` | integer | Deposit required | 500000, 2500000 |
| `finalization_timeline` | string | When finalized | "Within_6_months_of_order", "Within_1_year", "Extended_2_years" |
| `reasons_for_provisional` | enum | Why provisional used | "pending_information", "incomplete_assessment", "pending_transfer_pricing_investigation", "pending_survey_results", "pending_authorities_reply" |
| `final_assessment_issued` | boolean | Later finalized | true, false |
| `final_order_date` | date | When finalized | "2024-06-30" |
| `final_vs_provisional_variation` | integer | Change in assessment | 500000, -1000000, 2000000 |
| `variation_reason` | enum | Why difference | "additional_evidence_received", "revenue_investigation_completed", "assessee_submission_accepted", "best_judgment_applied", "revision_of_estimates" |

### B. SHOW CAUSE NOTICE AND RECOVERY DATAPOINTS

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `show_cause_notice_issued` | boolean | SCN sent | true, false |
| `scn_issue_date` | date | When SCN served | "2024-01-20" |
| `scn_section_basis` | enum | Legal authority | "Section_111_SCN", "Section_122_SCN", "Section_124_SCN", "Section_226_SCN_penalty", "Section_229_SCN_information" |
| `scn_subject_matter` | string | What's challenged | "Assessment of income at PKR 25 million vs claimed PKR 5 million", "Disallowance of expenses PKR 2 million", "Addition of unexplained source PKR 10 million" |
| `scn_relief_sought` | enum | What office asks | "provide_explanation", "produce_records", "answer_specific_questions", "justify_position", "substantiate_claims" |
| `assessee_response_filed` | boolean | SCN reply given | true, false |
| `response_filing_date` | date | When reply submitted | "2024-02-10" |
| `response_within_timeframe` | boolean | Timely filing | true, false |
| `response_content_adequacy` | enum | Quality of answer | "complete_satisfactory", "partial_incomplete", "non_substantive", "legalistic_evasive", "missing_key_evidence" |
| `evidence_accompanying_response` | array | Documents provided | ["bank_statements", "purchase_invoices", "sales_contracts", "expert_opinions", "correspondence_third_parties"] |
| `recovery_proceedings_initiated` | boolean | Collection action started | true, false |
| `recovery_demand_amount_pkr` | integer | Demanded amount | 2000000, 10000000, 50000000 |
| `recovery_method_employed` | enum | Collection approach | "income_withholding", "bank_account_freeze", "attachment_movable_property", "attachment_immovable_property", "garnishment_third_party", "arrest_warrant_issuance" |
| `bank_guarantee_security_amount` | integer | Security furnished | 500000, 2000000 |
| `recovery_stay_granted` | boolean | Moratorium issued | true, false |
| `stay_order_date` | date | When stay ordered | "2024-04-15" |
| `stay_condition` | enum | Terms of stay | "absolute_stay", "conditional_on_bank_guarantee", "conditional_on_posting_security", "pending_appeal_adjudication" |
| `recovery_amount_collected_pkr` | integer | Amount actually recovered | 500000, 5000000 |
| `recovery_completion_status` | enum | Collection outcome | "fully_recovered", "partially_recovered", "recovery_pending", "recovery_stayed_pending_appeal" |

### C. Tax Exemption and Concession Datapoints

#### Agricultural Income Exemption Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `agricultural_income_claimed` | integer | Asserted agricultural income | 500000, 2000000 |
| `section_41_exemption_invoked` | boolean | Agricultural exemption claimed | true, false |
| `income_sourced_from_agriculture` | boolean | Income actually agricultural | true, false |
| `agricultural_activity_type` | enum | Type of agricultural activity | "crop_cultivation", "livestock_raising", "dairy_farming", "horticulture", "forestry", "aquaculture", "agro_industry" |
| `agricultural_income_deemed_excluded` | boolean | Automatically exempt | true, false |
| `exemption_applicable_percentage` | integer | Portion exempted | 100, 75, 50 |
| `province_agriculture_taxed` | enum | Provincial taxation status | "province_cannot_tax", "province_can_tax_above_threshold", "province_can_tax_provincial_law", "provincial_exemption_parallel" |
| `provincial_threshold_limit_pkr` | integer | Exemption ceiling | 600000, 1000000 |
| `agricultural_income_exceeds_threshold` | boolean | Above exemption limit | true, false |
| `provincial_tax_applied` | enum | Provincial liability | "no_provincial_tax", "provincial_tax_applies", "provincial_tax_deferred", "provincial_tax_later_assessed" |
| `exemption_documentation_provided` | array | Supporting records | ["land_ownership_certificate", "crop_records", "sale_documents", "livestock_registration", "farm_income_declaration"] |
| `exemption_challenged_by_revenue` | boolean | FBR disputes exemption | true, false |
| `challenge_ground` | enum | Revenue's objection | "income_not_actually_agricultural", "activity_commercial_not_agricultural", "income_from_agro_processing", "mixed_income_source", "investment_only_not_farming" |
| `exemption_upheld_on_challenge` | enum | Result of challenge | "exemption_confirmed", "exemption_denied_income_taxed", "partial_exemption_granted", "determination_case_specific", "exemption_conditional" |
| `atir_agricultural_exemption_appeal` | boolean | Case appealed to ATIR | true, false |
| `atir_decision_agricultural` | enum | ATIR ruling | "atir_upheld_exemption", "atir_denied_exemption", "atir_modified_exemption_scope" |

#### Tax Concessions and Reliefs Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `concessional_tax_rate_claimed` | enum | Reduced tax offered | "reduced_capital_gains_tax", "concessional_dividend_tax", "special_industrial_sector_rate", "export_promotion_relief", "research_development_relief", "fdi_incentive_rate" |
| `concessional_rate_percentage` | integer | Tax rate allowed | 5, 10, 15, 22 |
| `normal_rate_percentage` | integer | Standard rate | 25, 30, 35 |
| `rate_differential_pkr` | integer | Tax savings | 100000, 500000, 2000000 |
| `concession_statutory_basis` | enum | Law providing relief | "Schedule_to_ITO_2001", "SRO_notification", "Finance_Act_Amendment", "investment_promotion_scheme", "sector_specific_relief" |
| `concession_conditions` | array | Qualifying requirements | ["minimum_investment_amount", "prescribed_activity_type", "foreign_investor_status", "technology_transfer", "employment_creation", "export_commitment"] |
| `assessee_concession_compliance` | enum | Conditions met | "all_conditions_met", "some_conditions_met", "no_conditions_met", "conditions_met_belatedly", "conditions_violated_mid_year" |
| `concession_allowed_amount_pkr` | integer | Granted relief value | 100000, 500000, 5000000 |
| `concession_allowed_percentage` | integer | Percent of claimed | 100, 75, 50, 25 |
| `concession_disallowed_reason` | enum | Why relief denied | "non_compliance_conditions", "ineligible_activity", "backdated_claim", "documentation_insufficient", "revenue_discretion_exercised" |

### D. TRANSFER PRICING DATAPOINTS

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `transfer_pricing_issue_raised` | boolean | TP adjustment made | true, false |
| `related_party_transaction` | boolean | Affiliation exists | true, false |
| `related_party_status` | enum | Relationship type | "subsidiary_parent", "associate_company", "joint_venture_partner", "common_control", "family_business" |
| `transaction_type` | enum | Nature of transfer | "goods_supply", "service_provision", "loan_advances", "royalty_payment", "rent_lease", "management_fee", "intellectual_property_license" |
| `declared_transfer_price_pkr` | integer | Asserted price | 100000, 5000000, 50000000 |
| `arm_length_price_estimated_pkr` | integer | Fair market value | 120000, 7000000, 60000000 |
| `price_variance_pkr` | integer | Difference amount | 20000, 2000000 |
| `price_variance_percentage` | integer | Percent difference | 10, 20, 30, 50 |
| `transfer_pricing_method_used` | enum | Valuation approach | "comparable_uncontrolled_price", "cost_plus", "resale_price", "profit_split", "transactional_net_margin", "comparable_profit_approach" |
| `method_appropriateness` | enum | Suitable method | "appropriate_method_selected", "inappropriate_method_applied", "method_incorrect_comparables", "method_not_supported_data" |
| `comparables_analysis_conducted` | boolean | Market data used | true, false |
| `comparable_companies_identified` | integer | Number used | 3, 5, 10, 15 |
| `comparable_data_source` | enum | Information origin | "commercial_databases", "published_financial_statements", "industry_surveys", "assessee_submitted", "revenue_investigation" |
| `transfer_pricing_adjustment_made` | boolean | TP modification | true, false |
| `adjustment_amount_pkr` | integer | Income added back | 500000, 5000000, 50000000 |
| `adjustment_interest_calculation` | boolean | Interest charged | true, false |
| `interest_amount_transfer_pricing_pkr` | integer | TP interest | 50000, 500000, 2000000 |
| `transfer_pricing_documentation_required` | boolean | TP study demanded | true, false |
| `documentation_adequacy` | enum | Report quality | "complete_satisfactory", "incomplete_material_gaps", "non_professional", "lacking_comparables", "methodology_flawed" |
| `transfer_pricing_dispute_resolution` | enum | Resolution mechanism | "atir_appeal_filed", "mutual_agreement_procedure_invoked", "advance_pricing_agreement_sought", "high_court_writ_filed" |
| `advance_pricing_agreement_sought` | boolean | Pre_approval requested | true, false |
| `apa_status` | enum | APA outcome | "apa_concluded", "apa_pending", "apa_not_pursued", "unilateral_apa_issued", "bilateral_apa_concluded" |

### E. ATIR (Appellate Tribunal Inland Revenue) Specific Datapoints

#### ATIR Appellate Process Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `commissioner_appeal_filed` | boolean | CIR(Appeals) petition lodged | true, false |
| `commissioner_appeal_date` | date | When appeal filed | "2024-03-15" |
| `commissioner_appeal_decision` | enum | CIR(A) ruling | "appeal_allowed", "appeal_dismissed", "appeal_allowed_in_part", "appeal_remanded_reconsideration", "order_modified" |
| `commissioner_appeal_outcome_pkr` | integer | Tax liability after CIR(A) | 2000000, 10000000 |
| `further_appeal_to_atir_filed` | boolean | ATIR petition lodged | true, false |
| `atir_appeal_filed_date` | date | When ATIR appeal filed | "2024-04-20" |
| `atir_memorandum_of_appeal_grounds` | array | ATIR appeal grounds | ["question_of_law", "misapplication_facts", "disregard_precedent", "unreasonable_findings"] |
| `atir_appeal_period` | string | Filing deadline | "Within_30_days_CIR(A)_decision", "Extended_90_days_special_circumstances" |
| `atir_appeal_admission_status` | enum | Whether admitted | "appeal_admitted", "appeal_rejected_belated", "appeal_rejected_no_grounds", "appeal_rejected_lack_jurisdiction" |
| `atir_bench_constitution` | enum | Panel composition | "single_accountant_member", "accountant_and_judicial_member", "judicial_member_alone", "three_member_bench" |
| `atir_hearing_conducted` | boolean | Oral hearing held | true, false |
| `atir_hearing_date` | date | When hearing took place | "2024-08-15" |
| `assessee_representation_at_atir` | enum | Representation method | "self_represented", "advocate_appeared", "chartered_accountant_appeared", "written_submission_only" |
| `atir_decision_delivered` | boolean | ATIR order passed | true, false |
| `atir_decision_date` | date | When decision issued | "2024-10-30" |
| `atir_decision_type` | enum | Outcome category | "atir_upheld_assessment", "atir_reduced_assessment", "atir_deleted_assessment", "atir_modified_assessment", "atir_remitted_reconsideration", "atir_allowed_appeal_in_part" |
| `atir_final_tax_liability_pkr` | integer | Final tax amount | 1000000, 5000000, 20000000 |
| `atir_relief_granted_pkr` | integer | Tax reduction | 500000, 2000000 |
| `atir_relief_percentage` | integer | Percent reduction | 25, 50, 75 |
| `atir_decision_finality_status` | enum | Appealability | "atir_order_final", "high_court_appeal_possible_substantial_law", "high_court_appeal_possible_facts", "appeal_rights_limited" |

#### ATIR Jurisdiction Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `atir_appellate_jurisdiction` | enum | ATIR authority | "direct_tax_appeals", "indirect_tax_appeals", "customs_excise_appeals", "all_fbr_taxes_appeals" |
| `direct_taxes_under_atir` | array | Income tax jurisdiction | ["income_tax_ordinance_2001", "corporate_tax", "individual_tax", "other_direct_taxes"] |
| `indirect_taxes_under_atir` | array | Sales and excise | ["sales_tax_act_1990", "federal_excise_act_2005", "customs_act_1969"] |
| `atir_substantive_questions_available` | enum | What ATIR can decide | "substantial_questions_of_law", "facts_cannot_be_reappreciated", "law_correctly_applied_finding", "reasonableness_order_not_reviewable" |
| `substantial_question_of_law_definition` | string | ATIR's test | "Question that concerns interpretation of law or application of law to facts" |
| `question_of_law_vs_fact` | enum | Characterization critical | "pure_question_of_law_reviewable", "question_of_fact_not_reviewable", "mixed_reviewable_if_law_aspect", "characterization_disputed" |

### F. Sales Tax Act 1990 Datapoints

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `sales_tax_liability_assessed_pkr` | integer | Tax determined | 1000000, 5000000, 50000000 |
| `sales_tax_return_filed` | boolean | Return submission | true, false |
| `return_filing_date` | date | When return filed | "2024-01-20" |
| `sales_tax_audit_conducted` | boolean | Audit assessment | true, false |
| `audit_refund_claim` | boolean | Refund claimed | true, false |
| `refund_amount_claimed_pkr` | integer | Claimed refund | 500000, 2000000 |
| `refund_allowed_pkr` | integer | Approved refund | 400000, 1500000 |
| `refund_disallowed_pkr` | integer | Denied refund | 100000, 500000 |
| `input_tax_credit_claimed` | integer | ITC asserted | 500000, 2000000, 10000000 |
| `input_tax_credit_allowed` | integer | ITC approved | 400000, 1800000, 8000000 |
| `input_tax_credit_disallowed` | integer | ITC rejected | 100000, 200000, 2000000 |
| `itc_disallowance_reason` | enum | Why ITC denied | "not_used_for_supply", "cross_objection_claimed", "documentation_insufficient", "blocked_supply", "input_not_authorized" |
| `sales_tax_evasion_alleged` | boolean | Fraud claimed | true, false |
| `penalty_for_evasion_pkr` | integer | Penalty amount | 500000, 2000000, 5000000 |
| `sales_tax_appeal_tribunal` | enum | Appellate forum | "atir_judgment", "customs_excise_sales_tax_tribunal", "high_court_on_law_only" |

### G. Customs Act 1969 Datapoints

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `customs_duty_assessed_pkr` | integer | Duty determined | 5000000, 20000000, 100000000 |
| `customs_assessment_type` | enum | Assessment category | "provisional_assessment", "final_assessment", "reassessment", "best_judgment_assessment" |
| `goods_classification_dispute` | boolean | Tariff position contested | true, false |
| `declared_classification` | string | Claimed tariff code | "HS 8471 30 00 - Computer processing units", "HS 6203 42 00 - Men's cotton trousers" |
| `revenue_classification` | string | FBR's classification | "HS 8471 30 99 - Other computer equipment", "HS 6203 49 00 - Men's synthetic trousers" |
| `classification_consequence_pkr` | integer | Duty difference | 500000, 2000000, 10000000 |
| `goods_valuation_dispute` | boolean | Value challenged | true, false |
| `declared_value_pkr` | integer | Asserted CIF | 10000000, 50000000, 200000000 |
| `customs_appraised_value_pkr` | integer | Revenue's value | 12000000, 60000000, 250000000 |
| `valuation_variance_percentage` | integer | Percent difference | 10, 20, 30 |
| `valuation_methodology_used` | enum | Appraisal method | "transaction_value_method", "comparable_uncontrolled_price", "deductive_value", "computed_value", "fallback_value" |
| `similar_goods_comparables_used` | boolean | Market data applied | true, false |
| `customs_exemption_claimed` | boolean | Exemption invoked | true, false |
| `exemption_sro_cited` | string | Exemption notification | "SRO 25(I)/98", "SRO 1234/2023" |
| `exemption_conditions_compliance` | enum | Condition satisfaction | "all_conditions_met", "some_conditions_missing", "conditions_not_verifiable" |
| `exemption_allowed` | boolean | Exemption granted | true, false |
| `duty_refund_claim` | boolean | Refund sought | true, false |
| `refund_period_applicable` | string | Timeframe | "Within_3_years_of_payment", "Within_1_year_of_clearance" |
| `customs_appeal_tribunal_jurisdiction` | enum | Appellate body | "customs_appellate_tribunal", "high_court_on_law_only", "substantial_question_law" |

### H. Federal Excise Act 2005 Datapoints

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `excise_duty_assessed_pkr` | integer | Duty determined | 500000, 2000000, 10000000 |
| `excisable_goods_category` | enum | Product type | "tobacco_products", "sugar", "energy_drinks", "automobiles", "cement", "natural_gas" |
| `excise_assessment_method` | enum | Calculation basis | "value_based_rate", "quantity_based_rate", "volume_based_rate", "specific_rate" |
| `excise_rate_applicable_percentage` | integer | Tax rate | 5, 10, 15, 20, 30 |
| `excise_liability_calculated_pkr` | integer | Duty amount | 100000, 500000, 5000000 |
| `excise_return_filing_status` | enum | Return submission | "filed_timely", "filed_late", "not_filed", "amended_filed" |
| `excise_audit_assessment` | boolean | Audit conducted | true, false |
| `excise_penalty_imposed` | enum | Penalty type | "failure_to_file", "short_payment", "evasion_attempt", "false_returns" |
| `excise_penalty_amount_pkr` | integer | Penalty value | 50000, 200000, 1000000 |
| `excise_dispute_resolution` | enum | Appeal forum | "atir", "customs_excise_tribunal", "high_court" |

---

## III. LABOUR LAW DATAPOINTS

### A. INDUSTRIAL RELATIONS ACT 2012 DATAPOINTS

#### Collective Bargaining Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `trade_union_registered` | boolean | Union formally recognized | true, false |
| `union_name` | string | Organization name | "General Workers Union", "Textile Mills Staff Association", "Transport Drivers Union" |
| `union_registration_date` | date | Date of registration | "2020-05-15" |
| `union_membership_count` | integer | Number of members | 500, 2000, 10000 |
| `collective_bargaining_agent_status` | enum | Union certification | "certified_cba", "uncertified_non_cba", "cba_application_pending", "cba_status_challenged" |
| `cba_determination_date` | date | When CBA declared | "2022-08-20" |
| `membership_percentage_for_cba` | integer | Required threshold | 33, 50 |
| `membership_verification_method` | enum | How verified | "check_off_deduction", "membership_record_review", "independent_audit", "secret_ballot", "self_certification" |
| `exclusive_bargaining_rights_granted` | boolean | Sole negotiation power | true, false |
| `bargaining_scope_coverage` | enum | What negotiated | "wages_salaries", "benefits_allowances", "working_hours", "termination_procedures", "grievance_mechanism", "safety_conditions", "leave_entitlements" |
| `collective_agreement_negotiated` | boolean | CA concluded | true, false |
| `agreement_negotiation_dates` | string | Negotiation period | "January_2023_April_2023" |
| `agreement_effective_period` | string | Duration | "2_years", "3_years", "multi_year" |
| `agreement_wage_increase_percentage` | integer | Salary enhancement | 5, 10, 15 |
| `agreement_wage_increase_amount_pkr` | integer | Additional annual cost | 1000000, 5000000, 20000000 |
| `agreement_fringe_benefits_negotiated` | array | Benefits included | ["health_insurance", "provident_fund", "gratuity", "annual_bonus", "performance_incentive", "transport_allowance", "housing_assistance"] |
| `agreement_working_hours_specified` | string | Standard hours | "40_hours_per_week", "45_hours_per_week", "48_hours_per_week" |
| `agreement_overtime_provisions` | enum | OT compensation | "time_and_half", "double_time", "compensatory_off", "mixed_arrangement" |
| `agreement_dispute_resolution_clause` | boolean | Grievance procedure | true, false |
| `agreement_dispute_escalation_levels` | integer | Grievance tiers | 2, 3, 4 |
| `agreement_arbitration_clause` | boolean | Arbitration provided | true, false |
| `agreement_strike_lockout_clause` | enum | Work action rules | "strike_lockout_prohibited_term", "strike_after_failed_arbitration", "lockout_only_reprisal", "unrestricted_subject_termination" |
| `agreement_ratification_by_membership` | boolean | Member approval | true, false |
| `ratification_vote_percentage` | integer | Approval level | 60, 70, 80, 90 |
| `agreement_registered_nirc_labor_court` | boolean | Official registration | true, false |
| `agreement_enforcement_mechanism` | enum | Compliance method | "union_monitoring", "joint_committee_oversight", "labor_court_enforcement", "nirc_intervention" |

#### Trade Union Rights Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `freedom_of_association_right` | enum | Legal protection | "protected_right", "restricted_certain_categories", "curtailed_emergency", "recognized_constitutional" |
| `right_to_form_union` | enum | Union formation | "unrestricted_right", "requires_government_approval", "requires_threshold_members", "prohibited_certain_sectors" |
| `membership_threshold_for_union` | integer | Minimum members | 10, 15, 50 |
| `union_leadership_election` | enum | Leadership selection | "secret_ballot_required", "democratic_process_mandated", "annual_elections_required", "no_legal_requirement" |
| `union_officer_term_limit` | string | Leadership duration | "2_years", "3_years", "no_term_limit", "subject_to_reelection" |
| `check_off_right` | enum | Dues deduction | "union_authorized_deduction", "member_consent_required", "management_obligation", "voluntary_arrangement" |
| `union_access_workplace` | enum | Facility provided | "union_office_on_premise", "bulletin_board_allowed", "organizing_time_given", "restricted_management_permission" |
| `union_officials_protection` | enum | Job security | "protected_from_dismissal", "special_procedures_required", "no_special_protection", "suspension_pending_inquiry" |
| `unfair_labor_practice_against_union` | array | Prohibited actions | ["discrimination_based_unionism", "interference_union_formation", "denial_union_access", "reprisal_for_union_activity", "discharge_for_unionism", "refusal_bargain_cba"] |
| `union_rights_violation_proven` | boolean | Breach established | true, false |
| `remedy_union_rights_violation` | enum | Relief available | "reinstatement_dismissed_member", "back_wages_and_benefits", "declaration_of_wrongful_action", "cease_and_desist_order", "damages_awarded" |

#### Strike and Lockout Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `strike_notice_issued` | boolean | Strike announced | true, false |
| `strike_notice_date` | date | When notice given | "2024-05-01" |
| `strike_notice_period_required` | string | Advance notification | "14_days_notice", "21_days_notice", "7_days_notice" |
| `strike_notice_period_complied` | boolean | Adequate notice | true, false |
| `strike_reason_category` | enum | Why strike called | "wage_dispute", "working_conditions", "termination_protest", "union_recognition", "unfair_labor_practice", "management_intimidation", "delay_grievance_resolution" |
| `strike_start_date` | date | Strike commencement | "2024-05-22" |
| `strike_duration_days` | integer | Length of strike | 1, 3, 7, 30, 90+ |
| `strike_participation_percentage` | integer | Worker participation | 50, 75, 90, 100 |
| `strike_legal_status` | enum | Strike lawfulness | "legal_strike_proper_procedure", "illegal_no_proper_notice", "illegal_essential_service", "illegal_contractual_ban", "lawful_after_notice" |
| `essential_service_exemption` | enum | Application of restriction | "essential_service_no_strike", "non_essential_strike_allowed", "essential_service_defined_statute", "case_specific_determination" |
| `government_intervention_strike` | boolean | State involvement | true, false |
| `intervention_type` | enum | Government action | "peaceful_mediation", "police_intervention", "military_deployment", "emergency_ordinance", "court_order_suspension" |
| `lockout_notice_issued` | boolean | Lockout announced | true, false |
| `lockout_notice_date` | date | When announced | "2024-06-10" |
| `lockout_notice_period_given` | string | Advance warning | "7_days", "14_days", "no_notice" |
| `lockout_reason` | enum | Management rationale | "union_intransigence", "strike_counter_response", "economic_viability", "work_stoppage_caused", "negotiation_breakdown" |
| `lockout_legality` | enum | Lawfulness | "legal_lockout", "illegal_reprisal", "illegal_absence_notice", "conditional_legality" |
| `strike_lockout_resolution_mechanism` | enum | How settled | "negotiation_agreement", "conciliation_board", "arbitration_award", "labor_court_order", "voluntary_arbitration" |
| `strike_settlement_date` | date | When resolved | "2024-06-30" |
| `strike_settlement_terms` | array | Agreement outcomes | ["partial_wage_increase", "union_recognition", "termination_reinstatement", "grievance_procedure_improvement", "management_commitment"] |

### B. UNFAIR LABOUR PRACTICE DATAPOINTS

#### Employer ULP (Section 31 IRA 2012) Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `employer_ulp_alleged` | boolean | Employer conduct challenged | true, false |
| `ulp_category_section_31` | enum | Type of ULP by employer | "interference_union_formation", "intimidation_union_membership", "discrimination_union_activity", "denial_union_access", "discharge_for_unionism", "refusal_bargain", "discrimination_for_complaint", "interference_employee_rights", "reprisal_for_legal_action", "union_busting_activity" |
| `specific_ulp_incident` | string | Concrete example | "Employee discharged day after union membership", "Manager threatened workers against voting for union", "Promised wage increase conditioned on union decertification" |
| `ulp_perpetrator_employee_classification` | enum | Who acted | "senior_management", "middle_management", "supervisor", "hr_department", "owner", "designated_representative" |
| `protected_activity_engaged_in` | enum | Employee's legal action | "forming_union", "union_membership", "union_leadership_role", "filing_unfair_labor_complaint", "testifying_case", "union_organizing", "strike_participation" |
| `causation_between_activity_and_treatment` | enum | Connection proven | "temporal_proximity_apparent", "management_stated_reason", "discriminatory_treatment_pattern", "burden_shifted_employer", "employer_failed_rebut", "no_causal_link_established" |
| `employer_defense_offered` | enum | Management's justification | "legitimate_business_reason", "performance_based_discharge", "economic_necessity", "unrelated_ground", "no_discriminatory_intent", "independent_reason" |
| `legitimate_reason_credibility` | enum | Defense persuasiveness | "credible_reason_established", "pretextual_reason_found", "insufficient_evidence_support", "time_sequence_contradicts", "inconsistent_policy_application" |
| `ulp_finding_by_labor_court` | enum | Determination | "ulp_proven", "ulp_not_proven", "ulp_partially_proven", "ulp_proven_but_discharged_fault", "ulp_proven_continued_employment_not_possible" |
| `ulp_remedy_ordered` | enum | Relief granted | "reinstatement_order", "back_wages_benefits", "compensation_damages", "cease_desist_order", "union_recognition_order", "restoration_discriminatees", "organizational_rights_restored" |
| `reinstatement_with_or_without_backpay` | enum | Remedy specifics | "reinstatement_full_backpay", "reinstatement_partial_backpay", "reinstatement_no_backpay", "compensation_instead_reinstatement", "lump_sum_settlement" |
| `amount_awarded_backpay_pkr` | integer | Compensation | 500000, 2000000, 10000000 |
| `amount_awarded_damages_pkr` | integer | Additional damages | 100000, 500000, 2000000 |
| `cease_desist_order_issued` | boolean | Stop order | true, false |
| `cease_desist_specific_direction` | string | What prohibited | "Stop discriminating in hiring", "Cease threatening union members", "Refrain from reprisals for union activity" |
| `ulp_appeal_filed` | boolean | Decision contested | true, false |
| `ulp_appeal_outcome` | enum | Appellate result | "lower_court_upheld", "ulp_reversed", "ulp_modified", "remedy_varied", "remanded_new_trial" |

#### Employee ULP (Section 32 IRA 2012) Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `employee_ulp_alleged` | boolean | Worker conduct challenged | true, false |
| `ulp_category_section_32` | enum | Type of ULP by employee | "violence_property_destruction", "intimidation_workers", "sit_in_occupation", "sabotage", "equipment_damage", "coercion_non_participants", "blockade_management", "mass_absence_unauthorized", "interference_production", "violence_management" |
| `specific_employee_ulp_incident` | string | Concrete example | "Workers blocked plant entrance preventing non-strikers", "Union organizer threatened co-workers opposing union", "Sit-in occupation prevented management access" |
| `ulp_perpetrator_worker_classification` | enum | Type of worker | "regular_employee", "union_member", "union_leader", "strike_participant", "organizer" |
| `property_damage_amount_pkr` | integer | Economic loss | 50000, 200000, 1000000 |
| `violence_allegation_proven` | boolean | Physical harm established | true, false |
| `coercion_allegation_proven` | boolean | Intimidation shown | true, false |
| `breach_company_discipline_alleged` | boolean | Violation of conduct standards | true, false |
| `discipline_proportionality_issue` | enum | Remedy appropriate | "discipline_proportionate_offense", "discipline_excessive_circumstances", "mitigating_factors_ignored", "first_offense_consideration", "provocation_by_management" |
| `employee_ulp_remedy` | enum | Relief available | "disciplinary_action_upheld", "discipline_reduced", "discharge_upheld_justified", "discharge_reduced_suspension", "reinstatement_ordered_ulp_not_proven" |

### C. DISMISSAL AND TERMINATION DATAPOINTS

#### Termination Grounds Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `termination_type` | enum | Category | "termination_simpliciter", "termination_misconduct", "termination_redundancy", "termination_retirement", "termination_death", "termination_incapacity" |
| `termination_on_misconduct` | boolean | Disciplinary discharge | true, false |
| `misconduct_allegation` | string | Specific charge | "Unauthorized absence 10 days", "Breach of confidentiality", "Insubordination refusing lawful order", "Theft of company property", "Violence toward colleague" |
| `misconduct_type_category` | enum | Nature of offense | "attendance_violation", "competency_failure", "insubordination", "dishonesty", "violence_aggression", "violation_safety", "breach_confidentiality", "conflict_of_interest", "moral_turpitude" |
| `serious_misconduct_standard` | enum | Gravity threshold | "minor_offense_warning_sufficient", "serious_misconduct_warrants_discharge", "gross_misconduct_mandatory_dismissal", "judgment_case_specific" |
| `grounds_for_dismissal_non_misconduct` | enum | Legitimate reasons | "serious_illness_incurable", "inefficiency_perform_duties", "redundancy_economic_necessity", "retrenchment_restructuring", "reorganization_position_abolished", "mutual_agreement" |
| `economic_necessity_demonstrated` | boolean | Financial proof | true, false |
| `retrenchment_selection_criteria` | enum | How chosen for dismissal | "last_in_first_out", "performance_based", "department_seniority", "merit_evaluation", "management_discretion" |
| `selection_criteria_discriminatory` | boolean | Biased selection | true, false |
| `procedural_requirements_dismissal` | array | Steps required | ["written_charge_sheet_issued", "opportunity_to_respond", "disciplinary_inquiry_conducted", "reasoned_decision_made", "notice_served_employee", "compensation_offered"] |

#### Notice and Compensation Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `termination_notice_provided` | boolean | Advance warning given | true, false |
| `notice_period_length_months` | integer | Advance notice days | 1, 2, 3, 6 |
| `notice_requirement_statutory_basis` | enum | Legal provision | "Standing_Orders", "Contract_of_Employment", "Industrial_Relations_Act", "Labor_Code", "Industry_custom" |
| `notice_waived_with_compensation` | boolean | Payment in lieu | true, false |
| `notice_period_compensation_pkr` | integer | In-lieu payment | 100000, 500000, 2000000 |
| `termination_letter_issued` | boolean | Written notice | true, false |
| `termination_letter_specifies_reason` | boolean | Grounds stated | true, false |
| `final_settlement_calculated` | boolean | Dues computed | true, false |
| `gratuity_payable` | boolean | Severance entitlement | true, false |
| `gratuity_amount_pkr` | integer | Gratuity calculation | 50000, 200000, 1000000 |
| `gratuity_calculation_method` | enum | Formula used | "half_month_per_year", "one_month_per_year", "contractual_provision", "statutory_prescribed" |
| `gratuity_eligibility_criterion` | string | Requirement | "Minimum 1 year service", "Minimum 5 years service", "Permanent employee status" |
| `earned_leave_payment` | integer | Unused leave amount | 50000, 200000, 500000 |
| `earned_leave_encashment_rate` | string | Payment basis | "Last_salary", "Average_salary_12_months", "Contractual_rate" |
| `other_allowances_outstanding_pkr` | integer | Pending payments | 10000, 50000, 200000 |
| `total_final_settlement_pkr` | integer | Total dues | 500000, 2000000, 5000000 |
| `settlement_dispute` | boolean | Amount contested | true, false |
| `settlement_dispute_resolution` | enum | How settled | "agreed_between_parties", "labor_court_adjudicated", "nirc_decided", "arbitrator_determined", "compromise_reached" |

### D. STANDING ORDERS DATAPOINTS

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `standing_orders_application` | boolean | SOs apply | true, false |
| `establishment_size_minimum` | integer | Threshold for SOs | 10, 20, 50 |
| `standing_orders_registered` | boolean | SO official registration | true, false |
| `standing_orders_registration_date` | date | When registered | "2020-01-15" |
| `standing_orders_statutory_basis` | enum | Legal authority | "Standing_Orders_Ordinance_1968", "Provincial_Rules", "Industrial_Relations_Act" |
| `standing_order_provisions_covered` | array | Clauses included | ["condition_of_service", "hours_of_work", "leave_entitlements", "wages_payment", "suspension_discharge", "grievance_procedure", "discipline_code", "workmen_facilities"] |
| `standing_order_clause_number` | string | SO reference | "SO-11", "SO-11-A", "SO-20" |
| `standing_order_11a_application` | boolean | Mass termination rule | true, false |
| `standing_order_11a_trigger` | enum | When applies | "termination_more_than_50_percent", "closure_establishment", "partial_closure" |
| `standing_order_11a_notice_requirement` | string | Advance notice | "30_days_notice_government", "Approval_required_before_implementation" |
| `standing_order_11a_compensation_required` | boolean | Severance mandated | true, false |
| `standing_order_11a_compensation_amount` | string | Severance formula | "One_month_per_year_service", "Gratuity_plus_notice_period_wages" |
| `standing_order_modification_request` | boolean | Amendment sought | true, false |
| `modification_by_mutual_consent` | boolean | Agreed change | true, false |
| `modification_by_government_direction` | boolean | Official modification | true, false |
| `standing_order_violation_alleged` | boolean | Breach claimed | true, false |
| `standing_order_violation_type` | enum | How breached | "failure_follow_procedure", "arbitrary_application", "clause_misinterpreted", "clause_contravened", "discipline_not_per_so" |
| `standing_order_enforcement_forum` | enum | Where enforced | "labor_court", "nirc", "employer_internal_procedure", "conciliation_board" |

### E. WORKMEN'S COMPENSATION AND WORKPLACE SAFETY DATAPOINTS

#### Workmen's Compensation Act 1923 Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `workplace_accident_occurred` | boolean | Injury happened at work | true, false |
| `accident_date` | date | When incident occurred | "2024-02-15" |
| `accident_location` | enum | Where happened | "factory_floor", "office_premises", "construction_site", "transportation_during_duty", "official_trip" |
| `accident_nature` | enum | Type of injury | "fracture_bone", "burns", "chemical_exposure", "machinery_crush", "fall_height", "electrocution", "vehicle_accident", "repetitive_strain" |
| `injury_severity_classification` | enum | Gravity level | "minor_injury_first_aid", "moderate_injury_lost_time", "serious_injury_hospitalization", "permanent_disability", "fatal_injury", "occupational_disease" |
| `lost_time_days` | integer | Days unable to work | 5, 30, 90, 180, 365+ |
| `permanent_disability_declared` | boolean | Chronic condition | true, false |
| `disability_percentage` | integer | Loss of capacity | 10, 25, 50, 75, 100 |
| `employment_caused_accident` | enum | Causal connection | "accident_arising_out_employment", "accident_in_course_employment", "accident_not_work_related", "causal_relationship_disputed" |
| `workers_compensation_claim_filed` | boolean | Claim submitted | true, false |
| `claim_filing_date` | date | When claim filed | "2024-02-20" |
| `compensation_claim_amount_pkr` | integer | Amount sought | 100000, 500000, 2000000 |
| `claim_documentation_provided` | array | Supporting records | ["medical_certificate", "accident_report", "witness_statements", "employer_notification", "employer_acknowledgment"] |
| `medical_examination_conducted` | boolean | Doctor assessment | true, false |
| `medical_expert_appointed` | enum | Examiner type | "independent_doctor", "labor_department_examiner", "insurance_company_doctor", "claimant_own_doctor" |
| `medical_opinion_disability_percentage` | integer | Expert finding | 20, 40, 60, 80 |
| `employer_liability_acknowledged` | enum | Employer's position | "liability_admitted", "liability_denied", "liability_disputed_negligence_claimed", "liability_subject_dispute" |
| `negligence_employer_alleged` | boolean | Fault claimed | true, false |
| `employer_negligence_defense` | array | Management's argument | ["worker_breach_safety_rules", "worker_negligence", "third_party_responsible", "accident_unavoidable", "worker_intoxication", "willful_misconduct_worker"] |
| `compensation_awarded_pkr` | integer | Court judgment | 50000, 200000, 1000000, 5000000 |
| `compensation_calculation_basis` | enum | How determined | "half_months_salary_per_year", "full_months_salary_per_year", "fixed_amount_statute", "precedent_similar_injury", "negotiated_settlement" |
| `medical_treatment_costs_covered` | boolean | Treatment reimbursed | true, false |
| `rehabilitation_allowance_provided` | boolean | Rehab payment | true, false |
| `dependent_compensation_if_death` | boolean | Family payment | true, false |
| `dependent_allowance_pkr` | integer | Family amount | 100000, 500000, 1000000 |
| `pension_disability_granted` | boolean | Monthly stipend | true, false |
| `pension_monthly_amount_pkr` | integer | Monthly payment | 5000, 10000, 25000 |

#### Factories Act 1934 - Safety Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `factory_registration_status` | enum | Legal compliance | "registered_factory", "unregistered_operation", "registration_expired", "temporary_closure" |
| `factory_size_workers` | integer | Employee count | 50, 100, 500, 1000 |
| `factories_act_applicability` | boolean | Act applies minimum 10 workers | true, false |
| `safety_inspection_conducted` | boolean | Inspection done | true, false |
| `inspection_date` | date | When inspected | "2024-01-20" |
| `inspection_type` | enum | Inspection category | "routine_inspection", "complaint_based", "accident_investigation", "safety_audit", "occupational_health_check" |
| `safety_violation_identified` | array | Defects found | ["inadequate_ventilation", "unsafe_machinery_guards", "no_emergency_exits", "blocked_fire_extinguishers", "poor_sanitation", "inadequate_lighting", "no_safety_equipment", "absence_safety_officer"] |
| `violation_severity_level` | enum | Seriousness | "minor_deficiency", "serious_breach", "imminent_danger", "critical_safety_failure", "willful_violation" |
| `remedial_action_direction_issued` | boolean | Corrective order | true, false |
| `action_direction_timeframe` | string | Compliance deadline | "7_days", "30_days", "60_days" |
| `compliance_status` | enum | Whether complied | "fully_complied", "partially_complied", "non_compliance", "pending_compliance" |
| `penalty_amount_pkr` | integer | Fine imposed | 10000, 50000, 100000, 500000 |
| `penalty_section_imposed` | enum | Statutory basis | "Section_72_offense", "Section_73_offense", "Section_74_offense" |
| `imprisonment_threatened` | boolean | Jail possible | true, false |
| `imprisonment_term_months` | integer | Jail duration | 1, 3, 6, 12 |

### F. NIRC (National Industrial Relations Commission) Specific Datapoints

#### NIRC Jurisdiction Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `nirc_applicable_jurisdiction` | enum | Geographic scope | "islamabad_capital_territory", "trans_provincial_establishment", "federal_jurisdiction" |
| `establishment_trans_provincial_status` | boolean | Multi-province operations | true, false |
| `nirc_original_jurisdiction` | enum | NIRC powers | "adjudicate_industrial_disputes", "determine_collective_bargaining_agents", "register_trade_unions", "try_offences_under_ira", "determine_wages_boards" |
| `matter_within_nirc_jurisdiction` | enum | Issue type | "individual_employment_dispute", "collective_industrial_dispute", "trade_union_recognition", "unfair_labor_practice", "collective_agreement_breach", "strike_legality" |
| `alternative_labor_forum_available` | boolean | Provincial court jurisdiction | true, false |
| `election_of_forum` | enum | Where filed | "nirc_exclusive_jurisdiction", "provincial_labor_court_exclusive", "concurrent_jurisdiction", "nirc_chosen_over_provincial" |

#### NIRC Procedure and Process Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `nirc_application_filed` | boolean | Case initiated | true, false |
| `application_filing_date` | date | When filed | "2024-01-15" |
| `nirc_reference_number` | string | Case ID | "NIRC-123/2024", "FID-456/2023" |
| `applicant_type` | enum | Who filed | "individual_worker", "trade_union", "employer", "workers_group", "government_agency" |
| `respondent_type` | enum | Defendant | "employer", "trade_union", "collective_bargaining_agent", "management_representatives" |
| `nirc_bench_constitution` | enum | Panel type | "single_judge", "two_judge_bench", "three_judge_bench", "full_commission" |
| `nirc_hearing_scheduled` | boolean | Hearing date set | true, false |
| `hearing_date_nirc` | date | When hearing | "2024-04-20" |
| `parties_representation` | enum | Legal representation | "self_represented_both", "advocate_represented", "union_representative", "mixed_representation" |
| `evidence_presented_hearing` | array | Exhibits filed | ["documentary_evidence", "witness_testimony", "expert_opinion", "documentary_record", "correspondence"] |
| `hearing_concluded` | boolean | Hearing finished | true, false |
| `hearing_arguments_recorded` | boolean | Notes taken | true, false |
| `nirc_order_reserved` | boolean | Decision pending | true, false |
| `nirc_order_delivered` | boolean | Judgment issued | true, false |
| `nirc_order_delivery_date` | date | When announced | "2024-06-15" |

#### NIRC Decision and Remedies Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `nirc_finding_on_merits` | enum | Substantive decision | "application_allowed", "application_dismissed", "application_allowed_in_part", "application_disposed_with_direction", "remanded_investigation" |
| `nirc_relief_ordered` | array | Remedies granted | ["reinstatement_order", "back_wages_award", "cease_desist_order", "union_recognition", "collective_agreement_determination", "compensation_damages"] |
| `nirc_reasoned_order_issued` | boolean | Written judgment | true, false |
| `order_reasoning_detail_level` | enum | Explanation depth | "detailed_analysis", "brief_reasoning", "minimal_explanation", "only_conclusion_stated" |
| `precedent_cited_in_decision` | array | Cases referenced | ["NIRC_precedent", "High_Court_precedent", "Supreme_Court_precedent"] |
| `constitutional_or_statutory_provision_interpreted` | array | Laws applied | ["Industrial_Relations_Act_Section_X", "Constitution_Article_Y"] |
| `relief_implementation_mechanism` | enum | Enforcement | "direct_order_compliance", "government_agency_implementation", "revised_agreement_execution" |
| `implementation_timeline` | string | Deadline for compliance | "Immediate_effect", "Within_30_days", "Within_90_days", "Implementation_as_directed" |
| `post_order_compliance_monitoring` | boolean | Follow-up required | true, false |

#### NIRC Appeal and Review Datapoints
| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `appeal_against_nirc_order` | boolean | Order contested | true, false |
| `appeal_to_forum` | enum | Appellate body | "high_court_constitutional_petition", "supreme_court_review", "intra_nirc_bench", "no_appeal_available" |
| `appeal_filing_date` | date | When appeal filed | "2024-07-20" |
| `appeal_grounds` | array | Appeal basis | ["misapplication_law", "ignoring_material_evidence", "perversity_findings", "violation_natural_justice", "jurisdictional_error"] |
| `appellate_court_jurisdiction` | enum | Reviewing body | "high_court_substantial_question_law", "high_court_writ_jurisdiction", "supreme_court_discretionary", "limited_appellate_review" |
| `appellate_decision` | enum | Appeal outcome | "appeal_allowed_decision_reversed", "appeal_dismissed_order_upheld", "appeal_allowed_partially_modified", "order_remitted_reconsidering", "sent_back_new_inquiry" |

### G. PAYMENT OF WAGES ACT 1936 DATAPOINTS

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `wage_payment_dispute_raised` | boolean | Wages in question | true, false |
| `wage_payment_complaint_filed` | boolean | Formal complaint | true, false |
| `complaint_forum` | enum | Where filed | "labor_court", "wage_officer", "nirc", "arbitrator" |
| `wages_claimed_pkr` | integer | Amount disputed | 50000, 200000, 1000000 |
| `period_wages_unpaid` | string | Time covered | "1_month", "3_months", "6_months", "12_months", "multiple_periods" |
| `wage_payment_delay_days` | integer | Late payment | 10, 30, 90, 180, 365 |
| `unpaid_wage_type` | enum | Category of pay | "basic_salary", "allowances", "overtime", "bonus", "commission", "incentive", "gratuity", "severance" |
| `deduction_from_wages_claimed` | boolean | Illegal deduction | true, false |
| `deduction_amount_pkr` | integer | Deducted sum | 10000, 50000, 200000 |
| `deduction_reason_stated_by_employer` | enum | Employer's justification | "damage_compensation", "employee_fault_recovery", "overpayment_recovery", "statutory_authority", "contractual_basis", "disciplinary_fine" |
| `deduction_legality` | enum | Whether authorized | "legal_deduction", "illegal_wage_deduction", "deduction_exceeds_limits", "deduction_without_consent", "deduction_against_statute" |
| `wage_payment_law_violation` | boolean | Breach of act | true, false |
| `violation_section_pwa` | enum | Which section breached | "Section_4_timely_payment", "Section_5_deduction_limits", "Section_6_no_deduction", "Section_12_recovery_procedure" |
| `employer_defense_offered` | string | Management's argument | "Worker agreed to deduction", "Deduction lawfully authorized", "Worker caused damage requiring recovery", "Amount disputed" |
| `court_finding_wages_owed` | enum | Court ruling | "wages_fully_awarded", "wages_partially_awarded", "wages_denied", "wages_awarded_with_interest" |
| `award_amount_pkr` | integer | Judgment amount | 50000, 200000, 1000000 |
| `interest_on_unpaid_wages_awarded` | boolean | Interest granted | true, false |
| `interest_rate_percentage` | integer | Rate applied | 6, 10, 12, 15 |
| `interest_period_months` | integer | Duration | 1, 3, 6, 12 |
| `total_award_with_interest_pkr` | integer | Total judgment | 60000, 250000, 1200000 |
| `payment_deadline_from_order` | string | When to pay | "Within_15_days", "Within_30_days", "Immediately" |
| `non_compliance_consequences` | enum | If not paid | "contempt_of_court_proceedings", "attachment_wages_ordered", "attachment_property", "imprisonment_threat" |

---

## IV. CROSS-CUTTING PROCEDURAL DATAPOINTS

### Appeal and Review Process Datapoints

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `statutory_appeal_available` | boolean | Appeal right exists | true, false |
| `appeal_filing_deadline_days` | integer | Time limit | 30, 45, 60, 90 |
| `appeal_deadline_compliance` | boolean | Timely appeal | true, false |
| `belated_appeal_filed` | boolean | Late appeal | true, false |
| `condonation_of_delay_sought` | boolean | Extension requested | true, false |
| `condonation_granted` | boolean | Extension allowed | true, false |
| `appeal_forum_hierarchy` | array | Appeal chain | ["Commissioner_Appeals", "ATIR", "High_Court"] |
| `exhaustion_of_remedies_required` | boolean | Complete process | true, false |
| `jurisdiction_appellate_level` | enum | Authority scope | "law_questions_only", "law_and_fact", "discretionary_review", "limited_review_scope" |
| `new_evidence_admissible_appeal` | enum | Evidence handling | "new_evidence_allowed", "new_evidence_only_inadvertence", "new_evidence_not_allowed", "appeal_confined_record" |
| `evidence_discovery_during_appeal` | boolean | Evidence found | true, false |
| `appeal_decision_binding` | enum | Finality | "order_final_no_further_appeal", "limited_further_appeal", "appeal_to_higher_court_possible" |
| `appeal_success_rate_statistical` | integer | Likelihood percentage | 25, 40, 60 |

### Burden of Proof Datapoints

| Field Name | Data Type | Strategic Importance | Example Values |
|---|---|---|---|
| `initial_burden_of_proof` | enum | Who proves initially | "plaintiff_employee_burden", "defendant_employer_burden", "balanced_burden", "shared_burden" |
| `proof_standard_applied` | enum | Evidentiary threshold | "beyond_reasonable_doubt", "balance_of_probabilities", "clear_convincing_evidence", "preponderance_evidence", "strict_proof" |
| `burden_shifting_mechanism` | boolean | Burden can shift | true, false |
| `burden_shift_condition` | enum | When burden shifts | "after_prima_facie_case", "after_preliminary_showing", "statutory_shifting", "presumption_invoked" |
| `rebuttal_burden_on_opponent` | enum | Counter-proof required | "must_rebut", "can_rebut_if_wished", "rebuttable_presumption", "conclusive_presumption" |

---

## V. SUMMARY OF CRITICAL DATAPOINT CATEGORIES

**Total Critical Datapoints Identified**: 450+ across three practice areas

### Aggregation by Domain:

**Constitutional Law**: 125+ datapoints
- Fundamental Rights (20+)
- Article 184(3) Petitions (15+)
- Judicial Review (20+)
- Writ Jurisdiction (70+)
- Federal-Provincial Disputes (10+)
- Military Courts (8+)
- Election Petitions (10+)
- Interpretation Principles (15+)
- Intra-Court Appeals (8+)
- Presidential References (7+)

**Tax Law**: 180+ datapoints
- ITO 2001 Assessment (60+)
- Section 111 Additions (12+)
- Section 122 Assessments (10+)
- Show Cause & Recovery (20+)
- Exemptions & Concessions (15+)
- Transfer Pricing (25+)
- ATIR Procedure (20+)
- Sales Tax (12+)
- Customs (12+)
- Federal Excise (5+)

**Labour Law**: 165+ datapoints
- IRA 2012 Collective Bargaining (35+)
- Trade Union Rights (12+)
- Strike/Lockout (20+)
- Unfair Labour Practices (30+)
- Dismissal/Termination (25+)
- Standing Orders (15+)
- Workmen's Compensation (20+)
- Factories Act (12+)
- NIRC Specific (20+)
- Payment of Wages (8+)

**Cross-Cutting Procedural**: 20+ datapoints
- Appeals & Review
- Burden of Proof

---

## IMPLEMENTATION GUIDE FOR LEGAL AI SYSTEM

### Database Schema Design Recommendations:

1. **Case Entity**: `case_id`, `court_jurisdiction`, `case_number`, `citation_pld`, `decision_date`, `bench_composition`

2. **Issue Entity**: `issue_id`, `case_id`, `primary_issue`, `sub_issues`, `legal_domain`, `statute_sections`

3. **Finding Entity**: `finding_id`, `case_id`, `issue_id`, `court_finding`, `reasoning`, `precedential_value`

4. **Relief Entity**: `relief_id`, `case_id`, `relief_type`, `relief_amount`, `implementation_status`

5. **Procedural Fact Entity**: `procedure_id`, `case_id`, `procedure_step`, `date`, `requirement_met`

### Search and Filtering Priorities:

**High Priority**:
- `locus_standi_category` - Filter eligibility immediately
- `grounds_for_success_failure` - Flag winning/losing arguments
- `relief_available` - Determine remedy feasibility
- `burden_of_proof` - Critical for case strategy

**Medium Priority**:
- `statutory_basis_provision` - Ensures correct law application
- `procedure_timing_deadlines` - Compliance critical
- `benchmark_amounts` - Comparative damages/awards
- `interpretation_principles` - Precedent guidance

**Operational Priority**:
- `forum_jurisdiction_determination` - Correct court selection
- `exhaustion_requirements` - Prerequisite compliance
- `appeal_rights_limitations` - Strategic planning
- `evidence_admissibility` - Case preparation

---

## SOURCES AND CITATIONS

Research compiled from:

[Courting The Law - Fundamental Rights](https://courtingthelaw.com/2021/02/17/commentary/fundamental-rights-and-how-to-enforce-them/)
[Appellate Tribunal Inland Revenue](https://atir.gov.pk/)
[National Industrial Relations Commission](https://www.nirc.gov.pk/)
[Sindh High Court Case Law Portal](https://caselaw.shc.gov.pk/)
[Supreme Court of Pakistan](https://www.supremecourt.gov.pk/)
[Pakistan Constitution - Pakistan Kanoon](https://pakistankanoon.com/statutes/constitution-of-pakistan/)
[Income Tax Case Laws - TaxHelplines](https://taxhelplines.com.pk/caselaws)
[TaxationPk - Pakistan Tax Insights](https://insights.taxationpk.com/)
[Paycheck.pk - Labour Laws](https://paycheck.pk/labour-laws/)
[SAHSOL - Judicial Studies](https://sahsol.lums.edu.pk/)
[PLD - Pakistan Legal Decisions](https://www.pljlawsite.com/)
[Customs Appellate Tribunal](https://molaw.gov.pk/)
[High Court of Sindh](https://sindhhighcourt.gov.pk/)

---

**Note**: This comprehensive datapoint extraction represents a specialized taxonomy for Pakistani legal AI systems. Each datapoint's strategic importance derives from actual litigation patterns and appellate precedent. Implementation requires continuous updating as new judgments emerge.
