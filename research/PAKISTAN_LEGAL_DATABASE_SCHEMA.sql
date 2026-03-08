-- Pakistan Legal AI System - Database Schema
-- Comprehensive schema for Constitutional, Tax, and Labour Law court judgments
-- Generated: March 8, 2026

-- ============================================================================
-- CORE ENTITIES
-- ============================================================================

CREATE TABLE courts (
  court_id VARCHAR(36) PRIMARY KEY,
  court_name VARCHAR(255) NOT NULL,
  court_type ENUM(
    'supreme_court',
    'high_court_islamabad',
    'high_court_sindh',
    'high_court_lahore',
    'high_court_peshawar',
    'labor_court_provincial',
    'atir',
    'nirc',
    'tribunal_specialized'
  ) NOT NULL,
  jurisdiction_geographic VARCHAR(255),
  jurisdiction_subject_matter TEXT,
  UNIQUE KEY (court_name, court_type)
);

CREATE TABLE cases (
  case_id VARCHAR(36) PRIMARY KEY,
  court_id VARCHAR(36) NOT NULL,
  case_number VARCHAR(50) NOT NULL,
  case_title VARCHAR(500) NOT NULL,
  pld_citation VARCHAR(100),
  decision_date DATE NOT NULL,
  filing_date DATE,
  decision_year INT,
  bench_size INT,
  dissenting_judges INT DEFAULT 0,
  legal_domain ENUM('constitutional_law', 'tax_law', 'labour_law', 'multi_domain') NOT NULL,
  case_status ENUM('decided', 'pending', 'withdrawn', 'dismissed', 'allowed_in_part') NOT NULL,

  -- Metadata
  judge_names TEXT,
  judgment_length_pages INT,
  judgment_url VARCHAR(500),
  summary_text TEXT,

  FOREIGN KEY (court_id) REFERENCES courts(court_id),
  UNIQUE KEY (court_id, case_number),
  INDEX idx_decision_date (decision_date),
  INDEX idx_legal_domain (legal_domain),
  INDEX idx_year (decision_year)
);

CREATE TABLE judges (
  judge_id VARCHAR(36) PRIMARY KEY,
  judge_name VARCHAR(255) NOT NULL,
  court_id VARCHAR(36),
  appointment_date DATE,
  retirement_date DATE,
  specialization TEXT,
  FOREIGN KEY (court_id) REFERENCES courts(court_id)
);

CREATE TABLE case_judges (
  case_judge_id VARCHAR(36) PRIMARY KEY,
  case_id VARCHAR(36) NOT NULL,
  judge_id VARCHAR(36) NOT NULL,
  bench_position INT,
  opinion_type ENUM('majority', 'concurring', 'dissenting') DEFAULT 'majority',
  FOREIGN KEY (case_id) REFERENCES cases(case_id),
  FOREIGN KEY (judge_id) REFERENCES judges(judge_id)
);

-- ============================================================================
-- CONSTITUTIONAL LAW SCHEMA
-- ============================================================================

CREATE TABLE constitutional_cases (
  constitutional_case_id VARCHAR(36) PRIMARY KEY,
  case_id VARCHAR(36) NOT NULL UNIQUE,
  petition_type ENUM(
    'Article_8_void_law',
    'Article_14_dignity',
    'Article_17_movement',
    'Article_18_profession',
    'Article_19_expression',
    'Article_20_religion',
    'Article_184_3_constitution_petition',
    'Article_199_writ_petition',
    'Article_225_election_petition',
    'Article_227_supervisory',
    'other_fundamental_right'
  ) NOT NULL,

  -- Fundamental right claimed
  fundamental_right_claimed VARCHAR(255),
  fundamental_right_articles INT ARRAY,

  -- Law challenged
  law_challenged VARCHAR(500),
  statute_section_challenged VARCHAR(100),
  alleged_inconsistency_type ENUM(
    'abridges_right',
    'takes_away_right',
    'in_derogation_of_right',
    'arbitrary_application',
    'disproportionate_restriction'
  ),

  -- Locus standi
  petitioner_type ENUM(
    'aggrieved_party',
    'public_interest_litigant',
    'affected_group',
    'civil_society',
    'union_representative'
  ),
  locus_standi_established BOOLEAN,
  public_importance_threshold_met BOOLEAN,
  public_importance_justification TEXT,

  -- Review and remedies
  pre_petition_remedies_exhausted ENUM(
    'no_adequate_remedy_exists',
    'high_court_pending',
    'admin_forum_ineffective',
    'tribunal_pending'
  ),

  -- Court decision
  admissibility_decision ENUM(
    'maintainable',
    'not_maintainable',
    'rejected_locus_standi',
    'rejected_non_exhaustion'
  ),

  petition_outcome ENUM(
    'granted_with_relief',
    'allowed_in_part',
    'dismissed',
    'disposed_with_direction',
    'remanded_high_court'
  ),

  interpretation_applied ENUM(
    'strict_construction',
    'purposive_interpretation',
    'literal_reading',
    'harmonious_construction',
    'fundamental_rights_primacy'
  ),

  -- Relief granted
  relief_granted TEXT,
  law_declared_void BOOLEAN,
  injunction_issued BOOLEAN,
  declaration_of_nullity BOOLEAN,

  -- Basic structure doctrine
  basic_structure_doctrine_invoked BOOLEAN,
  basic_structure_elements TEXT,

  FOREIGN KEY (case_id) REFERENCES cases(case_id),
  INDEX idx_petition_type (petition_type),
  INDEX idx_fundamental_right (fundamental_right_claimed)
);

CREATE TABLE judicial_review_cases (
  judicial_review_id VARCHAR(36) PRIMARY KEY,
  case_id VARCHAR(36) NOT NULL UNIQUE,

  review_ground_invoked ENUM(
    'ultra_vires',
    'procedural_fairness_violation',
    'irrationality',
    'proportionality_breach',
    'discrimination',
    'natural_justice_denial',
    'fettering_discretion',
    'bad_faith',
    'patent_illegality'
  ),

  authority_reviewed ENUM(
    'executive_decision',
    'administrative_order',
    'legislative_act',
    'subordinate_court',
    'quasi_judicial_tribunal',
    'statutory_body'
  ),

  natural_justice_breach_alleged BOOLEAN,
  natural_justice_defect_type TEXT,

  irrationality_test_applied BOOLEAN,
  irrationality_result ENUM(
    'unreasonable_decision',
    'absurdity_manifest',
    'outside_rational_range',
    'satisfies_rationality'
  ),

  proportionality_analysis_conducted BOOLEAN,
  proportionality_result ENUM(
    'proportionate',
    'disproportionately_burdensome',
    'less_restrictive_means_available'
  ),

  discrimination_head_claimed VARCHAR(100),
  discrimination_finding ENUM(
    'discrimination_proven',
    'no_discrimination',
    'discrimination_justified',
    'classification_reasonable'
  ),

  standard_of_review_applied ENUM(
    'strict_scrutiny',
    'intermediate_scrutiny',
    'rational_basis_test',
    'manifest_absurdity',
    'heightened_rationality'
  ),

  decision_outcome ENUM(
    'decision_quashed',
    'decision_upheld',
    'decision_remitted',
    'order_partially_quashed',
    'order_suspended'
  ),

  FOREIGN KEY (case_id) REFERENCES cases(case_id),
  INDEX idx_review_ground (review_ground_invoked),
  INDEX idx_standard_of_review (standard_of_review_applied)
);

CREATE TABLE writ_jurisdiction_cases (
  writ_case_id VARCHAR(36) PRIMARY KEY,
  case_id VARCHAR(36) NOT NULL UNIQUE,

  writ_type ENUM(
    'habeas_corpus',
    'mandamus',
    'certiorari',
    'prohibition',
    'quo_warranto'
  ) NOT NULL,

  -- Alternative remedy doctrine
  alternative_remedy_exists BOOLEAN,
  alternative_remedy_type VARCHAR(255),
  remedy_adequacy_assessment ENUM(
    'adequate_effectual',
    'inadequate_slow',
    'inadequate_insufficient_power',
    'adequate_but_not_exclusive'
  ),
  remedy_accessibility ENUM(
    'accessible_affordable',
    'inaccessible_cost_prohibitive',
    'legally_barred',
    'practically_futile'
  ),
  remedy_expedience ENUM(
    'expeditious_decision',
    'prolonged_delays',
    'uncertain_timeline',
    'faster_writ_remedy'
  ),
  exception_to_adequacy ENUM(
    'constitutional_question',
    'patent_illegality',
    'natural_justice_violation',
    'fundamental_right_violation',
    'public_law_issue'
  ),

  writ_maintainability_decision ENUM(
    'maintainable',
    'not_maintainable_remedy_available',
    'maintainable_with_conditions'
  ),

  writ_granted BOOLEAN,

  FOREIGN KEY (case_id) REFERENCES cases(case_id),
  INDEX idx_writ_type (writ_type),
  INDEX idx_writ_granted (writ_granted)
);

-- Habeas corpus specific
CREATE TABLE habeas_corpus_cases (
  habeas_case_id VARCHAR(36) PRIMARY KEY,
  writ_case_id VARCHAR(36) NOT NULL UNIQUE,

  detention_type ENUM(
    'police_custody',
    'judicial_custody',
    'administrative_detention',
    'military_custody',
    'extra_judicial',
    'preventive_detention'
  ),

  detention_legality_status ENUM(
    'lawful',
    'unlawful',
    'without_warrant',
    'exceeds_authority',
    'lacks_due_process'
  ),

  detaining_authority ENUM(
    'law_enforcement',
    'prison',
    'military',
    'intelligence_agency',
    'administrative_official',
    'private_person'
  ),

  procedural_deficiency_found TEXT,

  relief_in_habeas_corpus ENUM(
    'detainee_released',
    'release_with_conditions',
    'detention_declared_illegal',
    'officer_held_contempt',
    'compensation_ordered'
  ),

  court_order_enforcement ENUM(
    'order_complied',
    'order_appealed',
    'order_partially_complied',
    'contempt_proceedings'
  ),

  FOREIGN KEY (writ_case_id) REFERENCES writ_jurisdiction_cases(writ_case_id),
  INDEX idx_detention_type (detention_type),
  INDEX idx_legality (detention_legality_status)
);

-- Mandamus specific
CREATE TABLE mandamus_cases (
  mandamus_case_id VARCHAR(36) PRIMARY KEY,
  writ_case_id VARCHAR(36) NOT NULL UNIQUE,

  statutory_duty_type ENUM(
    'ministerial_duty',
    'discretionary_duty_with_limits',
    'statutory_direction',
    'constitutional_obligation',
    'administrative_responsibility'
  ),

  duty_definition TEXT,
  duty_is_ministerial BOOLEAN,

  failure_type ENUM(
    'refused_entirely',
    'delayed_unreasonably',
    'imposed_unauthorized_conditions',
    'exceeded_discretion_bounds',
    'acted_in_bad_faith'
  ),

  mandamus_grant_decision ENUM(
    'granted',
    'denied_discretion_exists',
    'denied_alternative_remedy',
    'granted_with_conditions'
  ),

  enforcement_mechanism TEXT,

  FOREIGN KEY (writ_case_id) REFERENCES writ_jurisdiction_cases(writ_case_id)
);

-- Certiorari specific
CREATE TABLE certiorari_cases (
  certiorari_case_id VARCHAR(36) PRIMARY KEY,
  writ_case_id VARCHAR(36) NOT NULL UNIQUE,

  lower_tribunal_type ENUM(
    'administrative_tribunal',
    'quasi_judicial_body',
    'licensing_authority',
    'statutory_board',
    'subordinate_court',
    'departmental_authority'
  ),

  jurisdiction_excess_alleged BOOLEAN,
  jurisdiction_excess_type TEXT,

  natural_justice_breach_alleged BOOLEAN,
  natural_justice_defect_type TEXT,

  law_misinterpretation_alleged BOOLEAN,

  certiorari_ground_established ENUM(
    'jurisdiction_exceeded',
    'natural_justice_denied',
    'law_misapplied',
    'evidence_ignored',
    'tribunal_biased',
    'procedure_not_followed'
  ),

  certiorari_outcome ENUM(
    'order_quashed',
    'order_upheld',
    'order_quashed_remitted',
    'order_partially_quashed',
    'certiorari_refused'
  ),

  remittal_direction TEXT,

  FOREIGN KEY (writ_case_id) REFERENCES writ_jurisdiction_cases(writ_case_id)
);

-- Quo warranto specific
CREATE TABLE quo_warranto_cases (
  quo_warranto_case_id VARCHAR(36) PRIMARY KEY,
  writ_case_id VARCHAR(36) NOT NULL UNIQUE,

  public_office_held VARCHAR(255),

  legality_ground_challenged ENUM(
    'improper_procedure',
    'disqualification_not_removed',
    'conflict_of_interest',
    'statutory_prerequisite_missing',
    'fraud_in_appointment',
    'conditional_appointment_lapsed'
  ),

  statutory_qualification_required TEXT,
  qualification_deficiency TEXT,
  appointment_procedure_violation TEXT,

  quo_warranto_success BOOLEAN,
  office_vacancy_declared BOOLEAN,
  person_removed_from_office BOOLEAN,

  relief_granted ENUM(
    'office_declared_vacant',
    'person_removed',
    'appointment_voided',
    'quo_warranto_dismissed'
  ),

  FOREIGN KEY (writ_case_id) REFERENCES writ_jurisdiction_cases(writ_case_id)
);

CREATE TABLE federal_provincial_jurisdiction_cases (
  fed_prov_case_id VARCHAR(36) PRIMARY KEY,
  case_id VARCHAR(36) NOT NULL UNIQUE,

  dispute_subject_matter VARCHAR(255),

  federal_list_entry VARCHAR(100),
  concurrent_list_entry VARCHAR(100),
  provincial_list_entry VARCHAR(100),

  legislative_authority_competing ENUM(
    'federal',
    'provincial',
    'concurrent',
    'federal_exclusive',
    'provincial_exclusive'
  ),

  overlap_conflict_type ENUM(
    'direct_contradiction',
    'operational_conflict',
    'overlapping_subject_matter',
    'delegation_question',
    'paramountcy_issue'
  ),

  paramountcy_doctrine_applied BOOLEAN,
  federal_law_declared_paramount BOOLEAN,

  court_jurisdiction_determination VARCHAR(255),

  dispute_resolution_outcome ENUM(
    'federal_upheld',
    'provincial_upheld',
    'federal_law_void_conflict',
    'provincial_law_void_conflict',
    'harmonious_interpretation'
  ),

  eighteenth_amendment_context ENUM(
    'devolution_applied',
    'pre_18th_amendment',
    'post_18th_amendment',
    'concurrent_list_affected'
  ),

  FOREIGN KEY (case_id) REFERENCES cases(case_id),
  INDEX idx_dispute_subject (dispute_subject_matter),
  INDEX idx_amendment_context (eighteenth_amendment_context)
);

CREATE TABLE military_court_review_cases (
  military_case_id VARCHAR(36) PRIMARY KEY,
  case_id VARCHAR(36) NOT NULL UNIQUE,

  military_court_jurisdiction ENUM(
    'military_personnel_only',
    'civilians_allowed',
    'national_security_offences',
    'terrorism_charges',
    'constitutional_offences'
  ),

  subject_matter_jurisdiction VARCHAR(255),

  petitioner_status ENUM(
    'accused_person',
    'family_member',
    'constitutional_holder',
    'bar_association',
    'civil_society'
  ),

  grounds_for_challenge TEXT,
  civilian_trial_guarantee BOOLEAN,

  military_court_authority_scope ENUM(
    'unconstitutional',
    'valid_limited_scope',
    'only_military_personnel',
    'civilians_exclusive_civil_courts'
  ),

  appeal_to_military_commission ENUM(
    'military_appeals_allowed',
    'supreme_court_jurisdiction',
    'civilian_court_appellate',
    'no_appellate_review'
  ),

  death_penalty_imposition_allowed BOOLEAN,

  constitutional_amendment_context VARCHAR(255),

  FOREIGN KEY (case_id) REFERENCES cases(case_id)
);

-- ============================================================================
-- TAX LAW SCHEMA
-- ============================================================================

CREATE TABLE tax_cases (
  tax_case_id VARCHAR(36) PRIMARY KEY,
  case_id VARCHAR(36) NOT NULL UNIQUE,

  tax_type ENUM(
    'income_tax',
    'sales_tax',
    'customs_duty',
    'federal_excise',
    'agricultural_income'
  ) NOT NULL,

  assessment_year VARCHAR(10),
  tax_year_period VARCHAR(50),

  assessee_ntn VARCHAR(50),
  assessee_category ENUM(
    'individual',
    'company',
    'partnership',
    'association_persons',
    'joint_venture',
    'trust',
    'ngo',
    'non_resident'
  ),

  income_source_category ENUM(
    'salary_wages',
    'business_profit',
    'capital_gain',
    'rental_income',
    'agricultural_income',
    'other_income',
    'exempt_income'
  ),

  assessment_forum ENUM(
    'assessing_officer',
    'commissioner_appeals',
    'atir',
    'high_court',
    'supreme_court'
  ),

  FOREIGN KEY (case_id) REFERENCES cases(case_id),
  INDEX idx_tax_type (tax_type),
  INDEX idx_assessment_year (assessment_year),
  INDEX idx_assessee_category (assessee_category)
);

CREATE TABLE income_tax_assessment (
  assessment_id VARCHAR(36) PRIMARY KEY,
  tax_case_id VARCHAR(36) NOT NULL UNIQUE,

  notice_section_issued ENUM(
    'Section_114',
    'Section_115',
    'Section_120',
    'Section_121',
    'Section_147',
    'Section_148'
  ),

  notice_issued_date DATE,
  assessee_response_date DATE,
  response_adequacy ENUM(
    'adequate_complete',
    'inadequate_missing',
    'non_response_default',
    'partially_responsive',
    'belatedly_filed'
  ),

  assessment_order_issued BOOLEAN,
  assessment_order_date DATE,

  tax_assessed_amount_pkr BIGINT,
  tax_liability_amount_pkr BIGINT,

  penalty_amount_pkr BIGINT DEFAULT 0,
  penalty_section_imposed VARCHAR(50),

  interest_amount_pkr BIGINT DEFAULT 0,
  interest_calculation_period VARCHAR(100),

  addition_to_income BIGINT DEFAULT 0,
  addition_reason TEXT,

  -- Depreciation and expenses
  depreciation_claimed BIGINT DEFAULT 0,
  depreciation_allowed BIGINT DEFAULT 0,
  depreciation_disallowed BIGINT DEFAULT 0,

  expense_category_disputed TEXT,
  expense_claimed_pkr BIGINT DEFAULT 0,
  expense_allowed_pkr BIGINT DEFAULT 0,
  expense_disallowed_pkr BIGINT DEFAULT 0,
  disallowance_reason TEXT,

  record_keeping_deficiency TEXT,

  assessment_finality_status ENUM(
    'final_no_appeal',
    'appeal_possible_commissioner',
    'appeal_possible_tribunal',
    'appeal_possible_high_court',
    'under_appeal'
  ),

  FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id),
  INDEX idx_notice_section (notice_section_issued),
  INDEX idx_assessment_order_date (assessment_order_date)
);

CREATE TABLE section_111_addition (
  section_111_id VARCHAR(36) PRIMARY KEY,
  assessment_id VARCHAR(36) NOT NULL,

  section_111_applicability BOOLEAN,
  section_111_notice_issued BOOLEAN,
  notice_issue_date DATE,

  clause_invoked ENUM(
    'unexplained_sources',
    'cash_evidence',
    'failure_explain_discrepancy',
    'failure_explain_acquisition',
    'failure_explain_investment'
  ),

  income_or_asset_claimed TEXT,
  assessee_explanation_provided BOOLEAN,
  explanation_adequacy ENUM(
    'satisfactory',
    'unsatisfactory',
    'no_explanation',
    'not_believable',
    'partial'
  ),

  addition_ground VARCHAR(255),
  addition_amount_final_pkr BIGINT,

  burden_of_proof ENUM(
    'assessee_prove_legality',
    'revenue_prove_illegality',
    'balanced_burden',
    'assessee_initial',
    'shifting_burden'
  ),

  addition_upheld_on_appeal ENUM(
    'upheld',
    'reduced_partially',
    'deleted_entirely',
    'modified',
    'remitted'
  ),

  FOREIGN KEY (assessment_id) REFERENCES income_tax_assessment(assessment_id)
);

CREATE TABLE section_122_bja (
  bja_id VARCHAR(36) PRIMARY KEY,
  assessment_id VARCHAR(36) NOT NULL,

  section_122_invoked BOOLEAN,
  section_111_order_precedent BOOLEAN,
  sequential_procedure_followed BOOLEAN,
  section_122_show_cause_date DATE,

  grounds_for_bja TEXT,

  assessing_officer_estimate BIGINT,
  estimation_methodology TEXT,
  estimation_reasonable_basis BOOLEAN,

  estimated_income_upheld_appeal ENUM(
    'upheld',
    'reduced',
    'increased',
    'substituted',
    'deleted'
  ),

  FOREIGN KEY (assessment_id) REFERENCES income_tax_assessment(assessment_id)
);

CREATE TABLE show_cause_notice_recovery (
  scn_id VARCHAR(36) PRIMARY KEY,
  assessment_id VARCHAR(36) NOT NULL,

  show_cause_notice_issued BOOLEAN,
  scn_issue_date DATE,
  scn_section_basis VARCHAR(100),
  scn_subject_matter TEXT,
  scn_relief_sought TEXT,

  assessee_response_filed BOOLEAN,
  response_filing_date DATE,
  response_within_timeframe BOOLEAN,
  response_content_adequacy ENUM(
    'complete_satisfactory',
    'partial_incomplete',
    'non_substantive',
    'legalistic_evasive',
    'missing_evidence'
  ),

  evidence_accompanying_response TEXT,

  recovery_proceedings_initiated BOOLEAN,
  recovery_demand_amount_pkr BIGINT,
  recovery_method_employed VARCHAR(255),

  bank_guarantee_security_amount BIGINT DEFAULT 0,

  recovery_stay_granted BOOLEAN,
  stay_order_date DATE,
  stay_condition VARCHAR(255),

  recovery_amount_collected_pkr BIGINT DEFAULT 0,
  recovery_completion_status ENUM(
    'fully_recovered',
    'partially_recovered',
    'pending',
    'stayed'
  ),

  FOREIGN KEY (assessment_id) REFERENCES income_tax_assessment(assessment_id),
  INDEX idx_recovery_status (recovery_completion_status)
);

CREATE TABLE tax_exemption_concession (
  exemption_id VARCHAR(36) PRIMARY KEY,
  tax_case_id VARCHAR(36) NOT NULL,

  exemption_type ENUM(
    'agricultural_income',
    'reduced_capital_gains_rate',
    'concessional_dividend_rate',
    'industrial_sector_rate',
    'export_promotion_relief',
    'research_development_relief',
    'fdi_incentive_rate'
  ),

  concessional_rate_percentage INT,
  normal_rate_percentage INT,
  rate_differential_pkr BIGINT,

  concession_statutory_basis VARCHAR(255),
  concession_conditions TEXT,

  assessee_concession_compliance ENUM(
    'all_conditions_met',
    'some_conditions_met',
    'no_conditions_met',
    'conditions_met_belatedly',
    'conditions_violated'
  ),

  concession_allowed_amount_pkr BIGINT DEFAULT 0,
  concession_allowed_percentage INT,
  concession_disallowed_reason TEXT,

  FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id),
  INDEX idx_exemption_type (exemption_type)
);

-- Agricultural Income Exemption
CREATE TABLE agricultural_income_exemption (
  agri_exempt_id VARCHAR(36) PRIMARY KEY,
  exemption_id VARCHAR(36) NOT NULL UNIQUE,

  agricultural_income_claimed BIGINT,
  section_41_exemption_invoked BOOLEAN,
  income_sourced_from_agriculture BOOLEAN,

  agricultural_activity_type ENUM(
    'crop_cultivation',
    'livestock_raising',
    'dairy_farming',
    'horticulture',
    'forestry',
    'aquaculture',
    'agro_industry'
  ),

  agricultural_income_deemed_excluded BOOLEAN,
  exemption_applicable_percentage INT,

  province_agriculture_taxed ENUM(
    'cannot_tax',
    'can_tax_above_threshold',
    'can_tax_provincial_law',
    'provincial_exemption_parallel'
  ),

  provincial_threshold_limit_pkr BIGINT,
  agricultural_income_exceeds_threshold BOOLEAN,

  provincial_tax_applied ENUM(
    'no_tax',
    'tax_applies',
    'tax_deferred',
    'tax_later_assessed'
  ),

  exemption_documentation_provided TEXT,

  exemption_challenged_by_revenue BOOLEAN,
  challenge_ground TEXT,

  exemption_upheld_on_challenge ENUM(
    'confirmed',
    'denied',
    'partial_exemption',
    'case_specific',
    'conditional'
  ),

  atir_agricultural_exemption_appeal BOOLEAN,
  atir_decision_agricultural ENUM(
    'upheld_exemption',
    'denied_exemption',
    'modified_scope'
  ),

  FOREIGN KEY (exemption_id) REFERENCES tax_exemption_concession(exemption_id)
);

CREATE TABLE transfer_pricing_case (
  tp_case_id VARCHAR(36) PRIMARY KEY,
  tax_case_id VARCHAR(36) NOT NULL,

  transfer_pricing_issue_raised BOOLEAN,
  related_party_transaction BOOLEAN,
  related_party_status VARCHAR(255),

  transaction_type ENUM(
    'goods_supply',
    'service_provision',
    'loan_advances',
    'royalty_payment',
    'rent_lease',
    'management_fee',
    'ip_license'
  ),

  declared_transfer_price_pkr BIGINT,
  arm_length_price_estimated_pkr BIGINT,
  price_variance_pkr BIGINT,
  price_variance_percentage INT,

  transfer_pricing_method_used VARCHAR(255),
  method_appropriateness ENUM(
    'appropriate',
    'inappropriate',
    'method_incorrect',
    'not_supported'
  ),

  comparables_analysis_conducted BOOLEAN,
  comparable_companies_identified INT,
  comparable_data_source VARCHAR(255),

  transfer_pricing_adjustment_made BOOLEAN,
  adjustment_amount_pkr BIGINT DEFAULT 0,

  adjustment_interest_calculation BOOLEAN,
  interest_amount_tp_pkr BIGINT DEFAULT 0,

  transfer_pricing_documentation_required BOOLEAN,
  documentation_adequacy TEXT,

  transfer_pricing_dispute_resolution ENUM(
    'atir_appeal_filed',
    'mutual_agreement_procedure',
    'apa_sought',
    'high_court_writ'
  ),

  advance_pricing_agreement_sought BOOLEAN,
  apa_status ENUM(
    'apa_concluded',
    'apa_pending',
    'apa_not_pursued',
    'unilateral_apa',
    'bilateral_apa'
  ),

  FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id),
  INDEX idx_transaction_type (transaction_type)
);

CREATE TABLE atir_appellate_process (
  atir_id VARCHAR(36) PRIMARY KEY,
  tax_case_id VARCHAR(36) NOT NULL,

  commissioner_appeal_filed BOOLEAN,
  commissioner_appeal_date DATE,
  commissioner_appeal_decision ENUM(
    'allowed',
    'dismissed',
    'allowed_in_part',
    'remanded',
    'modified'
  ),
  commissioner_appeal_outcome_pkr BIGINT,

  further_appeal_to_atir_filed BOOLEAN,
  atir_appeal_filed_date DATE,
  atir_memorandum_grounds TEXT,
  atir_appeal_period VARCHAR(100),

  atir_appeal_admission_status ENUM(
    'admitted',
    'rejected_belated',
    'rejected_no_grounds',
    'rejected_no_jurisdiction'
  ),

  atir_bench_constitution ENUM(
    'single_accountant',
    'accountant_and_judicial',
    'judicial_member_alone',
    'three_member_bench'
  ),

  atir_hearing_conducted BOOLEAN,
  atir_hearing_date DATE,
  assessee_representation_at_atir VARCHAR(100),

  atir_decision_delivered BOOLEAN,
  atir_decision_date DATE,

  atir_decision_type ENUM(
    'upheld_assessment',
    'reduced_assessment',
    'deleted_assessment',
    'modified_assessment',
    'remitted_reconsideration',
    'allowed_in_part'
  ),

  atir_final_tax_liability_pkr BIGINT,
  atir_relief_granted_pkr BIGINT,
  atir_relief_percentage INT,

  atir_decision_finality_status ENUM(
    'atir_order_final',
    'high_court_appeal_law',
    'high_court_appeal_facts',
    'appeal_rights_limited'
  ),

  FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id),
  INDEX idx_atir_decision_type (atir_decision_type),
  INDEX idx_atir_decision_date (atir_decision_date)
);

CREATE TABLE sales_tax_case (
  sales_tax_id VARCHAR(36) PRIMARY KEY,
  tax_case_id VARCHAR(36) NOT NULL UNIQUE,

  sales_tax_liability_assessed_pkr BIGINT,
  sales_tax_return_filed BOOLEAN,
  return_filing_date DATE,

  sales_tax_audit_conducted BOOLEAN,
  audit_refund_claim BOOLEAN,

  refund_amount_claimed_pkr BIGINT,
  refund_allowed_pkr BIGINT,
  refund_disallowed_pkr BIGINT,

  input_tax_credit_claimed BIGINT,
  input_tax_credit_allowed BIGINT,
  input_tax_credit_disallowed BIGINT,
  itc_disallowance_reason TEXT,

  sales_tax_evasion_alleged BOOLEAN,
  penalty_for_evasion_pkr BIGINT,

  sales_tax_appeal_tribunal VARCHAR(255),

  FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id)
);

CREATE TABLE customs_case (
  customs_id VARCHAR(36) PRIMARY KEY,
  tax_case_id VARCHAR(36) NOT NULL UNIQUE,

  customs_duty_assessed_pkr BIGINT,
  customs_assessment_type ENUM(
    'provisional_assessment',
    'final_assessment',
    'reassessment',
    'best_judgment_assessment'
  ),

  goods_classification_dispute BOOLEAN,
  declared_classification VARCHAR(50),
  revenue_classification VARCHAR(50),
  classification_consequence_pkr BIGINT,

  goods_valuation_dispute BOOLEAN,
  declared_value_pkr BIGINT,
  customs_appraised_value_pkr BIGINT,
  valuation_variance_percentage INT,
  valuation_methodology_used VARCHAR(255),

  similar_goods_comparables_used BOOLEAN,

  customs_exemption_claimed BOOLEAN,
  exemption_sro_cited VARCHAR(50),
  exemption_conditions_compliance ENUM(
    'all_met',
    'some_missing',
    'not_verifiable'
  ),

  exemption_allowed BOOLEAN,

  duty_refund_claim BOOLEAN,
  refund_period_applicable VARCHAR(100),

  customs_appeal_tribunal_jurisdiction VARCHAR(255),

  FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id),
  INDEX idx_goods_classification (declared_classification)
);

CREATE TABLE federal_excise_case (
  excise_id VARCHAR(36) PRIMARY KEY,
  tax_case_id VARCHAR(36) NOT NULL UNIQUE,

  excise_duty_assessed_pkr BIGINT,
  excisable_goods_category VARCHAR(100),
  excise_assessment_method VARCHAR(100),
  excise_rate_applicable_percentage INT,
  excise_liability_calculated_pkr BIGINT,

  excise_return_filing_status VARCHAR(100),
  excise_audit_assessment BOOLEAN,

  excise_penalty_imposed VARCHAR(100),
  excise_penalty_amount_pkr BIGINT,

  excise_dispute_resolution VARCHAR(100),

  FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id)
);

-- ============================================================================
-- LABOUR LAW SCHEMA
-- ============================================================================

CREATE TABLE labour_cases (
  labour_case_id VARCHAR(36) PRIMARY KEY,
  case_id VARCHAR(36) NOT NULL UNIQUE,

  labour_law_domain ENUM(
    'industrial_relations',
    'collective_bargaining',
    'unfair_labour_practice',
    'dismissal_termination',
    'wages_payment',
    'workplace_safety',
    'trade_union_rights',
    'strike_lockout'
  ) NOT NULL,

  establishment_name VARCHAR(255),
  establishment_industry VARCHAR(255),
  establishment_worker_count INT,

  labour_court_forum ENUM(
    'provincial_labor_court',
    'nirc',
    'wage_board',
    'wages_officer',
    'conciliation_board'
  ),

  FOREIGN KEY (case_id) REFERENCES cases(case_id),
  INDEX idx_labour_domain (labour_law_domain),
  INDEX idx_labour_forum (labour_court_forum)
);

CREATE TABLE collective_bargaining (
  cba_id VARCHAR(36) PRIMARY KEY,
  labour_case_id VARCHAR(36) NOT NULL,

  trade_union_registered BOOLEAN,
  union_name VARCHAR(255),
  union_registration_date DATE,
  union_membership_count INT,

  collective_bargaining_agent_status ENUM(
    'certified_cba',
    'uncertified',
    'cba_application_pending',
    'cba_status_challenged'
  ),

  cba_determination_date DATE,
  membership_percentage_for_cba INT,
  membership_verification_method VARCHAR(255),

  exclusive_bargaining_rights_granted BOOLEAN,
  bargaining_scope_coverage TEXT,

  collective_agreement_negotiated BOOLEAN,
  agreement_negotiation_dates VARCHAR(100),
  agreement_effective_period VARCHAR(100),

  agreement_wage_increase_percentage INT,
  agreement_wage_increase_amount_pkr BIGINT,

  agreement_fringe_benefits TEXT,
  agreement_working_hours VARCHAR(100),
  agreement_overtime_provisions VARCHAR(100),

  agreement_dispute_resolution_clause BOOLEAN,
  agreement_dispute_escalation_levels INT,
  agreement_arbitration_clause BOOLEAN,
  agreement_strike_lockout_clause VARCHAR(255),

  agreement_ratification_by_membership BOOLEAN,
  ratification_vote_percentage INT,

  agreement_registered_nirc_labor_court BOOLEAN,
  agreement_enforcement_mechanism VARCHAR(255),

  FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id),
  INDEX idx_cba_status (collective_bargaining_agent_status)
);

CREATE TABLE trade_union_rights (
  union_rights_id VARCHAR(36) PRIMARY KEY,
  labour_case_id VARCHAR(36) NOT NULL,

  freedom_of_association_right ENUM(
    'protected',
    'restricted_certain_categories',
    'curtailed_emergency',
    'recognized_constitutional'
  ),

  right_to_form_union ENUM(
    'unrestricted',
    'requires_government_approval',
    'requires_threshold_members',
    'prohibited_certain_sectors'
  ),

  membership_threshold_for_union INT,
  union_leadership_election VARCHAR(255),
  union_officer_term_limit VARCHAR(100),

  check_off_right ENUM(
    'union_authorized_deduction',
    'member_consent_required',
    'management_obligation',
    'voluntary_arrangement'
  ),

  union_access_workplace VARCHAR(255),
  union_officials_protection VARCHAR(255),

  unfair_labor_practice_against_union TEXT,
  union_rights_violation_proven BOOLEAN,

  remedy_union_rights_violation ENUM(
    'reinstatement_dismissed_member',
    'back_wages_benefits',
    'declaration_wrongful',
    'cease_desist_order',
    'damages_awarded'
  ),

  FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id)
);

CREATE TABLE strike_lockout (
  strike_lockout_id VARCHAR(36) PRIMARY KEY,
  labour_case_id VARCHAR(36) NOT NULL,

  strike_notice_issued BOOLEAN,
  strike_notice_date DATE,
  strike_notice_period_required VARCHAR(100),
  strike_notice_period_complied BOOLEAN,

  strike_reason_category VARCHAR(255),

  strike_start_date DATE,
  strike_duration_days INT,
  strike_participation_percentage INT,

  strike_legal_status ENUM(
    'legal_proper_procedure',
    'illegal_no_notice',
    'illegal_essential_service',
    'illegal_contractual_ban',
    'lawful_after_notice'
  ),

  essential_service_exemption VARCHAR(255),

  government_intervention_strike BOOLEAN,
  intervention_type VARCHAR(255),

  lockout_notice_issued BOOLEAN,
  lockout_notice_date DATE,
  lockout_notice_period_given VARCHAR(100),
  lockout_reason VARCHAR(255),

  lockout_legality ENUM(
    'legal_lockout',
    'illegal_reprisal',
    'illegal_absence_notice',
    'conditional_legality'
  ),

  strike_lockout_resolution_mechanism ENUM(
    'negotiation_agreement',
    'conciliation_board',
    'arbitration_award',
    'labor_court_order',
    'voluntary_arbitration'
  ),

  strike_settlement_date DATE,
  strike_settlement_terms TEXT,

  FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id),
  INDEX idx_strike_status (strike_legal_status),
  INDEX idx_lockout_legality (lockout_legality)
);

CREATE TABLE unfair_labour_practice (
  ulp_id VARCHAR(36) PRIMARY KEY,
  labour_case_id VARCHAR(36) NOT NULL,

  ulp_type ENUM(
    'employer_interference_union_formation',
    'employer_intimidation_membership',
    'employer_discrimination_union',
    'employer_denial_access',
    'employer_discharge_unionism',
    'employer_refusal_bargain',
    'employer_discrimination_complaint',
    'employee_violence_destruction',
    'employee_intimidation',
    'employee_sit_in_occupation',
    'employee_sabotage'
  ) NOT NULL,

  ulp_perpetrator_type VARCHAR(255),

  specific_ulp_incident TEXT,

  protected_activity_engaged_in ENUM(
    'forming_union',
    'union_membership',
    'union_leadership',
    'filing_complaint',
    'testifying_case',
    'union_organizing',
    'strike_participation'
  ),

  causation_between_activity_treatment ENUM(
    'temporal_proximity',
    'management_stated_reason',
    'discriminatory_pattern',
    'burden_shifted_employer',
    'no_causal_link'
  ),

  employer_defense_offered TEXT,
  legitimate_reason_credibility ENUM(
    'credible_reason',
    'pretextual_reason',
    'insufficient_evidence',
    'time_sequence_contradicts',
    'inconsistent_policy'
  ),

  ulp_finding_by_labor_court ENUM(
    'ulp_proven',
    'ulp_not_proven',
    'ulp_partially_proven',
    'ulp_proven_fault_employee',
    'ulp_continued_employment_not_possible'
  ),

  ulp_remedy_ordered TEXT,

  reinstatement_with_or_without_backpay ENUM(
    'reinstatement_full_backpay',
    'reinstatement_partial_backpay',
    'reinstatement_no_backpay',
    'compensation_instead',
    'lump_sum_settlement'
  ),

  amount_awarded_backpay_pkr BIGINT DEFAULT 0,
  amount_awarded_damages_pkr BIGINT DEFAULT 0,

  cease_desist_order_issued BOOLEAN,
  cease_desist_specific_direction TEXT,

  ulp_appeal_filed BOOLEAN,
  ulp_appeal_outcome ENUM(
    'lower_court_upheld',
    'ulp_reversed',
    'ulp_modified',
    'remedy_varied',
    'remanded_new_trial'
  ),

  FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id),
  INDEX idx_ulp_type (ulp_type),
  INDEX idx_ulp_finding (ulp_finding_by_labor_court)
);

CREATE TABLE dismissal_termination (
  dismissal_id VARCHAR(36) PRIMARY KEY,
  labour_case_id VARCHAR(36) NOT NULL,

  termination_type ENUM(
    'termination_simpliciter',
    'termination_misconduct',
    'termination_redundancy',
    'termination_retirement',
    'termination_death',
    'termination_incapacity'
  ),

  termination_on_misconduct BOOLEAN,
  misconduct_allegation TEXT,
  misconduct_type_category VARCHAR(255),

  serious_misconduct_standard VARCHAR(255),

  grounds_for_dismissal_non_misconduct VARCHAR(255),
  economic_necessity_demonstrated BOOLEAN,

  retrenchment_selection_criteria VARCHAR(255),
  selection_criteria_discriminatory BOOLEAN,

  procedural_requirements_dismissal TEXT,

  termination_notice_provided BOOLEAN,
  notice_period_length_months INT,
  notice_requirement_statutory_basis VARCHAR(255),

  notice_waived_with_compensation BOOLEAN,
  notice_period_compensation_pkr BIGINT DEFAULT 0,

  termination_letter_issued BOOLEAN,
  termination_letter_specifies_reason BOOLEAN,

  final_settlement_calculated BOOLEAN,
  gratuity_payable BOOLEAN,
  gratuity_amount_pkr BIGINT DEFAULT 0,
  gratuity_calculation_method VARCHAR(255),
  gratuity_eligibility_criterion VARCHAR(255),

  earned_leave_payment BIGINT DEFAULT 0,
  earned_leave_encashment_rate VARCHAR(255),

  other_allowances_outstanding_pkr BIGINT DEFAULT 0,
  total_final_settlement_pkr BIGINT,

  settlement_dispute BOOLEAN,
  settlement_dispute_resolution VARCHAR(255),

  FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id),
  INDEX idx_termination_type (termination_type),
  INDEX idx_misconduct_disputed (termination_on_misconduct)
);

CREATE TABLE standing_orders (
  standing_orders_id VARCHAR(36) PRIMARY KEY,
  labour_case_id VARCHAR(36) NOT NULL,

  standing_orders_application BOOLEAN,
  establishment_size_minimum INT,
  standing_orders_registered BOOLEAN,
  standing_orders_registration_date DATE,

  standing_orders_statutory_basis VARCHAR(255),
  standing_order_provisions_covered TEXT,

  standing_order_clause_number VARCHAR(50),
  standing_order_11a_application BOOLEAN,

  standing_order_11a_trigger VARCHAR(255),
  standing_order_11a_notice_requirement VARCHAR(255),
  standing_order_11a_compensation_required BOOLEAN,
  standing_order_11a_compensation_amount VARCHAR(255),

  standing_order_modification_request BOOLEAN,
  modification_by_mutual_consent BOOLEAN,
  modification_by_government_direction BOOLEAN,

  standing_order_violation_alleged BOOLEAN,
  standing_order_violation_type TEXT,

  standing_order_enforcement_forum VARCHAR(255),

  FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id)
);

CREATE TABLE workmen_compensation (
  wc_id VARCHAR(36) PRIMARY KEY,
  labour_case_id VARCHAR(36) NOT NULL,

  workplace_accident_occurred BOOLEAN,
  accident_date DATE,
  accident_location VARCHAR(255),
  accident_nature VARCHAR(255),

  injury_severity_classification ENUM(
    'minor_first_aid',
    'moderate_lost_time',
    'serious_hospitalization',
    'permanent_disability',
    'fatal',
    'occupational_disease'
  ),

  lost_time_days INT,
  permanent_disability_declared BOOLEAN,
  disability_percentage INT,

  employment_caused_accident ENUM(
    'arising_out_employment',
    'in_course_employment',
    'not_work_related',
    'causal_relationship_disputed'
  ),

  workers_compensation_claim_filed BOOLEAN,
  claim_filing_date DATE,
  compensation_claim_amount_pkr BIGINT,

  claim_documentation_provided TEXT,

  medical_examination_conducted BOOLEAN,
  medical_expert_appointed VARCHAR(255),
  medical_opinion_disability_percentage INT,

  employer_liability_acknowledged ENUM(
    'admitted',
    'denied',
    'disputed',
    'subject_to_dispute'
  ),

  negligence_employer_alleged BOOLEAN,
  employer_negligence_defense TEXT,

  compensation_awarded_pkr BIGINT DEFAULT 0,
  compensation_calculation_basis VARCHAR(255),

  medical_treatment_costs_covered BOOLEAN,
  rehabilitation_allowance_provided BOOLEAN,
  dependent_compensation_if_death BOOLEAN,
  dependent_allowance_pkr BIGINT DEFAULT 0,

  pension_disability_granted BOOLEAN,
  pension_monthly_amount_pkr INT DEFAULT 0,

  FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id),
  INDEX idx_injury_severity (injury_severity_classification),
  INDEX idx_claim_status (workers_compensation_claim_filed)
);

CREATE TABLE nirc_specific_case (
  nirc_specific_id VARCHAR(36) PRIMARY KEY,
  labour_case_id VARCHAR(36) NOT NULL,

  nirc_applicable_jurisdiction ENUM(
    'islamabad_capital_territory',
    'trans_provincial',
    'federal_jurisdiction'
  ),

  establishment_trans_provincial_status BOOLEAN,

  nirc_original_jurisdiction TEXT,
  matter_within_nirc_jurisdiction VARCHAR(255),

  alternative_labor_forum_available BOOLEAN,
  election_of_forum VARCHAR(255),

  nirc_application_filed BOOLEAN,
  application_filing_date DATE,
  nirc_reference_number VARCHAR(100),

  applicant_type VARCHAR(255),
  respondent_type VARCHAR(255),

  nirc_bench_constitution ENUM(
    'single_judge',
    'two_judge_bench',
    'three_judge_bench',
    'full_commission'
  ),

  nirc_hearing_scheduled BOOLEAN,
  hearing_date_nirc DATE,
  parties_representation VARCHAR(255),

  evidence_presented_hearing TEXT,
  hearing_concluded BOOLEAN,
  hearing_arguments_recorded BOOLEAN,

  nirc_order_reserved BOOLEAN,
  nirc_order_delivered BOOLEAN,
  nirc_order_delivery_date DATE,

  nirc_finding_on_merits ENUM(
    'application_allowed',
    'application_dismissed',
    'application_allowed_in_part',
    'application_disposed_with_direction',
    'remanded_investigation'
  ),

  nirc_relief_ordered TEXT,
  nirc_reasoned_order_issued BOOLEAN,

  order_reasoning_detail_level VARCHAR(255),
  precedent_cited_in_decision TEXT,
  constitutional_or_statutory_provision_interpreted TEXT,

  relief_implementation_mechanism VARCHAR(255),
  implementation_timeline VARCHAR(100),
  post_order_compliance_monitoring BOOLEAN,

  appeal_against_nirc_order BOOLEAN,
  appeal_to_forum VARCHAR(255),
  appeal_filing_date DATE,
  appeal_grounds TEXT,

  appellate_court_jurisdiction VARCHAR(255),
  appellate_decision ENUM(
    'appeal_allowed_reversed',
    'appeal_dismissed_upheld',
    'appeal_allowed_partially',
    'remitted_reconsidering',
    'sent_back_new_inquiry'
  ),

  FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id),
  INDEX idx_nirc_jurisdiction (nirc_applicable_jurisdiction),
  INDEX idx_nirc_finding (nirc_finding_on_merits)
);

CREATE TABLE payment_of_wages (
  pwa_id VARCHAR(36) PRIMARY KEY,
  labour_case_id VARCHAR(36) NOT NULL,

  wage_payment_dispute_raised BOOLEAN,
  wage_payment_complaint_filed BOOLEAN,
  complaint_forum VARCHAR(255),

  wages_claimed_pkr BIGINT,
  period_wages_unpaid VARCHAR(100),
  wage_payment_delay_days INT,

  unpaid_wage_type VARCHAR(255),

  deduction_from_wages_claimed BOOLEAN,
  deduction_amount_pkr BIGINT DEFAULT 0,
  deduction_reason_stated_by_employer VARCHAR(255),

  deduction_legality ENUM(
    'legal_deduction',
    'illegal_wage_deduction',
    'deduction_exceeds_limits',
    'deduction_without_consent',
    'deduction_against_statute'
  ),

  wage_payment_law_violation BOOLEAN,
  violation_section_pwa VARCHAR(100),

  employer_defense_offered TEXT,

  court_finding_wages_owed ENUM(
    'wages_fully_awarded',
    'wages_partially_awarded',
    'wages_denied',
    'wages_awarded_with_interest'
  ),

  award_amount_pkr BIGINT DEFAULT 0,

  interest_on_unpaid_wages_awarded BOOLEAN,
  interest_rate_percentage INT DEFAULT 0,
  interest_period_months INT DEFAULT 0,

  total_award_with_interest_pkr BIGINT,

  payment_deadline_from_order VARCHAR(100),
  non_compliance_consequences VARCHAR(255),

  FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id),
  INDEX idx_deduction_legality (deduction_legality),
  INDEX idx_court_finding (court_finding_wages_owed)
);

-- ============================================================================
-- PROCEDURAL AND CROSS-CUTTING TABLES
-- ============================================================================

CREATE TABLE statutory_provisions (
  provision_id VARCHAR(36) PRIMARY KEY,
  provision_code VARCHAR(100) NOT NULL,
  provision_title VARCHAR(255),

  statute_name VARCHAR(255),
  statute_year INT,

  provision_text TEXT,
  provision_domain ENUM('constitutional', 'tax', 'labour'),

  UNIQUE KEY (statute_name, provision_code)
);

CREATE TABLE case_statutory_provisions (
  case_provision_id VARCHAR(36) PRIMARY KEY,
  case_id VARCHAR(36) NOT NULL,
  provision_id VARCHAR(36) NOT NULL,

  provision_invoked BOOLEAN,
  provision_interpretation_applied TEXT,

  FOREIGN KEY (case_id) REFERENCES cases(case_id),
  FOREIGN KEY (provision_id) REFERENCES statutory_provisions(provision_id)
);

CREATE TABLE case_precedents (
  precedent_link_id VARCHAR(36) PRIMARY KEY,

  citing_case_id VARCHAR(36) NOT NULL,
  cited_case_id VARCHAR(36) NOT NULL,

  citation_type ENUM(
    'followed',
    'distinguished',
    'overruled',
    'approved',
    'criticized',
    'compared'
  ),

  context_of_citation TEXT,

  FOREIGN KEY (citing_case_id) REFERENCES cases(case_id),
  FOREIGN KEY (cited_case_id) REFERENCES cases(case_id),
  INDEX idx_citation_type (citation_type)
);

CREATE TABLE appeal_proceedings (
  appeal_id VARCHAR(36) PRIMARY KEY,

  original_case_id VARCHAR(36) NOT NULL,
  appellate_case_id VARCHAR(36),

  appeal_filed_date DATE,
  appeal_filing_deadline_days INT,
  appeal_deadline_compliance BOOLEAN,

  belated_appeal_filed BOOLEAN,
  condonation_of_delay_sought BOOLEAN,
  condonation_granted BOOLEAN,

  appeal_ground TEXT,

  appellate_court_id VARCHAR(36),

  jurisdiction_appellate_level ENUM(
    'law_questions_only',
    'law_and_fact',
    'discretionary_review',
    'limited_review'
  ),

  new_evidence_admissible ENUM(
    'new_evidence_allowed',
    'only_inadvertence',
    'not_allowed',
    'confined_record'
  ),

  evidence_discovery_during_appeal BOOLEAN,

  appeal_decision_binding ENUM(
    'final_no_appeal',
    'limited_appeal',
    'higher_court_possible'
  ),

  appeal_success_rate INT,

  FOREIGN KEY (original_case_id) REFERENCES cases(case_id),
  FOREIGN KEY (appellate_case_id) REFERENCES cases(case_id),
  FOREIGN KEY (appellate_court_id) REFERENCES courts(court_id),
  INDEX idx_appeal_filed_date (appeal_filed_date)
);

-- ============================================================================
-- INDICES FOR PERFORMANCE
-- ============================================================================

CREATE INDEX idx_cases_court_date ON cases(court_id, decision_date);
CREATE INDEX idx_cases_domain_year ON cases(legal_domain, decision_year);
CREATE INDEX idx_constitutional_cases_petition_type ON constitutional_cases(petition_type);
CREATE INDEX idx_tax_cases_assessment_year ON tax_cases(assessment_year);
CREATE INDEX idx_labour_cases_domain ON labour_cases(labour_law_domain);
CREATE INDEX idx_appeal_proceedings_dates ON appeal_proceedings(appeal_filed_date, appellate_court_id);

-- ============================================================================
-- FOREIGN KEY CONSTRAINTS
-- ============================================================================

ALTER TABLE constitutional_cases ADD FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE;
ALTER TABLE judicial_review_cases ADD FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE;
ALTER TABLE writ_jurisdiction_cases ADD FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE;
ALTER TABLE habeas_corpus_cases ADD FOREIGN KEY (writ_case_id) REFERENCES writ_jurisdiction_cases(writ_case_id) ON DELETE CASCADE;
ALTER TABLE mandamus_cases ADD FOREIGN KEY (writ_case_id) REFERENCES writ_jurisdiction_cases(writ_case_id) ON DELETE CASCADE;
ALTER TABLE certiorari_cases ADD FOREIGN KEY (writ_case_id) REFERENCES writ_jurisdiction_cases(writ_case_id) ON DELETE CASCADE;
ALTER TABLE quo_warranto_cases ADD FOREIGN KEY (writ_case_id) REFERENCES writ_jurisdiction_cases(writ_case_id) ON DELETE CASCADE;

ALTER TABLE income_tax_assessment ADD FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id) ON DELETE CASCADE;
ALTER TABLE section_111_addition ADD FOREIGN KEY (assessment_id) REFERENCES income_tax_assessment(assessment_id) ON DELETE CASCADE;
ALTER TABLE section_122_bja ADD FOREIGN KEY (assessment_id) REFERENCES income_tax_assessment(assessment_id) ON DELETE CASCADE;
ALTER TABLE show_cause_notice_recovery ADD FOREIGN KEY (assessment_id) REFERENCES income_tax_assessment(assessment_id) ON DELETE CASCADE;
ALTER TABLE tax_exemption_concession ADD FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id) ON DELETE CASCADE;
ALTER TABLE agricultural_income_exemption ADD FOREIGN KEY (exemption_id) REFERENCES tax_exemption_concession(exemption_id) ON DELETE CASCADE;
ALTER TABLE transfer_pricing_case ADD FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id) ON DELETE CASCADE;
ALTER TABLE atir_appellate_process ADD FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id) ON DELETE CASCADE;
ALTER TABLE sales_tax_case ADD FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id) ON DELETE CASCADE;
ALTER TABLE customs_case ADD FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id) ON DELETE CASCADE;
ALTER TABLE federal_excise_case ADD FOREIGN KEY (tax_case_id) REFERENCES tax_cases(tax_case_id) ON DELETE CASCADE;

ALTER TABLE collective_bargaining ADD FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id) ON DELETE CASCADE;
ALTER TABLE trade_union_rights ADD FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id) ON DELETE CASCADE;
ALTER TABLE strike_lockout ADD FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id) ON DELETE CASCADE;
ALTER TABLE unfair_labour_practice ADD FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id) ON DELETE CASCADE;
ALTER TABLE dismissal_termination ADD FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id) ON DELETE CASCADE;
ALTER TABLE standing_orders ADD FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id) ON DELETE CASCADE;
ALTER TABLE workmen_compensation ADD FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id) ON DELETE CASCADE;
ALTER TABLE nirc_specific_case ADD FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id) ON DELETE CASCADE;
ALTER TABLE payment_of_wages ADD FOREIGN KEY (labour_case_id) REFERENCES labour_cases(labour_case_id) ON DELETE CASCADE;

