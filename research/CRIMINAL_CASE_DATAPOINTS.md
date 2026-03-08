# Critical Criminal Case Judgment Datapoints for Pakistani Legal AI System

**Purpose**: This document identifies every critical datapoint a Pakistani criminal defense or prosecution lawyer needs when working on cases. Designed for maximum search relevance, filtering, pattern recognition, and case strategy.

**Author Context**: Synthesized from Pakistani Penal Code (PPC), Criminal Procedure Code (CrPC), Qanun-e-Shahadat (Evidence Law), case law precedents, and judicial practice guidelines.

---

## SECTION A: CASE IDENTIFICATION & JURISDICTION

### A1: Case Registry Information
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **case_id** | string (unique) | Unique identification for searching and linking | "CRL-A-2024-5432", "D-123-2023" |
| **case_title** | string | Party names - search by defendant, complainant, victim | "State v. Muhammad Ahmed Khan", "PTI v. Federation" |
| **case_type** | enum | Differentiates trial vs. appeal vs. revision | ["trial", "appeal", "revision", "reference"] |
| **judgment_type** | enum | Conviction, acquittal, or mixed verdicts | ["conviction", "acquittal", "partial_conviction", "dismissal"] |
| **date_judgment** | date | Critical for precedent chronology and trend analysis | "2023-06-15" |
| **date_filed** | date | Tracks case duration from filing to judgment | "2021-03-20" |
| **case_duration_days** | number | Case processing speed metric | 945 |
| **court_level** | enum | Determines appeal pathway and precedent weight | ["trial_court", "high_court", "supreme_court", "special_court"] |
| **court_name** | string | Specific court for jurisdiction/venue appeals | "Lahore High Court", "Anti-Terrorism Court, Islamabad" |
| **bench_composition** | array[object] | Judge names matter for jurisprudential patterns | [{name: "Justice Iftikhar Muhammad Chaudhry", role: "presiding"}, {name: "Justice Javed Iqbal", role: "member"}] |
| **case_number** | string | Official court numbering | "Cr. Appeal No. 123/2023" |

### A2: Jurisdiction & Venue
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **jurisdiction_type** | enum | Subject matter jurisdiction | ["criminal", "terrorism", "narcotic", "hudood", "juvenile", "commercial"] |
| **jurisdiction_province** | enum | Determines applicable procedural rules | ["punjab", "sindh", "kpk", "balochistan", "islamabad"] |
| **forum_category** | enum | Case classification for precedent matching | ["murder", "theft", "sexual_assault", "terrorism", "drug_trafficking", "financial_crime"] |
| **trial_court_jurisdiction** | enum | Original jurisdiction level | ["district", "sessions", "additional_sessions"] |
| **territorial_jurisdiction** | string | Geographic specificity | "Karachi District", "Rawalpindi" |

---

## SECTION B: OFFENSE INFORMATION (The "What")

### B1: Penal Code Offenses (Chapter Structure)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **ppc_sections_charged** | array[object] | Primary offense tracking | [{section: 302, title: "Murder", severity: "capital"}, {section: 34, title: "Common Intention", severity: "modifier"}] |
| **ppc_section_number** | string | Specific PPC provision | "302", "379", "423-A" |
| **offense_title_ppc** | string | Human-readable offense name | "Qatl-e-Amd (Intentional Murder)", "Theft", "Cheating" |
| **offense_category** | enum | Grouping for pattern analysis | ["crime_against_person", "crime_against_property", "crime_against_state", "crime_against_religion", "crime_affecting_public_health"] |
| **severity_level** | enum | Prison range classification | ["capital_offense", "life_imprisonment", "long_term_7plus", "medium_term_3to7", "short_term_under3"] |
| **section_type** | enum | How offense operates | ["substantive", "modifying", "alternate_provision"] |
| **ipc_equivalent** | string | For comparison to Indian cases | "Indian IPC 302" |

### B2: Specific Offense Details (Murder Example - Most Common)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **murder_category** | enum | Sentencing pathways differ significantly | ["qatal_i_amd_premeditated", "qatal_i_khata_unintentional", "qatal_i_azhar_heat_of_passion"] |
| **premeditation_indicators** | array[string] | Evidence strength for motive/intent | ["prior_enmity", "weapon_procurement", "planning_evidence", "time_gap_between_act_and_death"] |
| **motive_identified** | enum | Critical for prosecution burden | ["family_dispute", "property", "enmity", "honor", "financial", "love_affair", "political", "sectarian", "unknown"] |
| **provocation_claimed** | boolean | Defense mitigating factor | true/false |
| **provocation_evidence** | array[string] | If claimed, what establishes it | ["assault", "insult", "infidelity_discovery", "legal_wrong"] |

### B3: Alternative Offense Charges (Burden Shifting)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **alternate_charges** | array[object] | Fallback convictions for jury nullification risk | [{section: 304, title: "Causing Death by Negligence", plea_status: "charged"}] |
| **modifying_sections** | array[object] | Change quantum of offense | [{section: 34, title: "Act of Several Persons in Furtherance of Common Intention"}, {section: 114, title: "Abetment"}] |
| **section_34_applied** | boolean | "Common intention" - expands liability | true/false |
| **section_114_applied** | boolean | "Abetment" - vicarious liability | true/false |
| **abetment_type** | enum | If Section 114: how did accused abet | ["instigator", "conspirator", "aid_provider", "encourager"] |

### B4: Special Law Offenses (Outside PPC)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **special_law_offense** | enum | Requires different evidence/procedure | ["anti_terrorism_act", "narcotics_cnsa", "hudood_ordinance", "juvenile_justice", "acid_control_act", "cyber_crime"] |
| **ata_offense** | object | Anti-Terrorism Act specifics | {section: "6", schedule: "I", offense_title: "Act of Terrorism", mandatory_death: true} |
| **ata_schedule** | enum | ATA has schedules of terrorism | ["schedule_1_terrorism", "schedule_2_prohibition", "schedule_3_armed_groups"] |
| **cnsa_substance** | enum | Narcotic Control substance type | ["opium", "heroin", "cocaine", "cannabis", "hashish", "morphine", "psychotropic"] |
| **cnsa_quantity_grams** | number | "Large quantity" = trafficking vs. possession | 500 |
| **hudood_offense_type** | enum | Islamic law specific | ["zina_unlawful_sexual", "qazf_false_accusation", "theft", "alcohol_consumption"] |
| **hudood_evidence_requirement** | string | Stringent witness requirements | "4_adult_male_muslim_witnesses_for_zina" |
| **juvenile_case** | boolean | Age-based jurisdiction trigger | true/false |

### B5: Narcotics-Specific (CNSA) Datapoints
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **section_cnsa** | string | Specific CNSA section | "8", "9", "14", "15" |
| **cnsa_section_title** | string | Offense type | "Possession", "Trafficking", "Production", "Financing Drug Trade" |
| **drug_quantity_kg** | number | Distinguishes possession vs. trafficking | 2.5 |
| **quantity_threshold_purity_percent** | number | "Large quantity" varies by substance | 95.5 |
| **quantity_classification** | enum | Prosecution category | ["personal_possession", "commercial_quantity", "large_commercial", "trafficking_intent_indicators"] |
| **recovery_location** | string | Where drugs seized | "residence", "vehicle", "public_place", "trafficking_route" |
| **recovery_circumstances** | enum | Legality of search affects admissibility | ["lawful_search_warrant", "voluntary_disclosure", "consent_search", "contested_search", "warrantless_search"] |
| **drug_purity_percent** | number | Quality affects sentencing | 85 |

### B6: Financial Crime Details
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **financial_crime_amount_pkr** | number | Sentencing severity correlates | 500000000 |
| **cheating_section** | enum | PPC Section 420, variants | ["420_cheating", "465_forgery", "468_forgery_for_fraud", "471_using_forged_document"] |
| **fraud_category** | enum | Pattern analysis | ["bank_fraud", "insurance_fraud", "real_estate", "tender_rigging", "advance_fee_scam"] |
| **victims_count** | number | Aggravating factor | 150 |
| **recovery_amount_pkr** | number | Prosecution success metric | 250000000 |

---

## SECTION C: PARTIES & PARTICIPANTS

### C1: Prosecution/State Information
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **state_complainant** | string | "State" vs. private complainant affects burden | "The State", "Federation of Pakistan" |
| **prosecuting_agency** | enum | Different agencies, different capabilities | ["police_investigation", "fbi_equivalent", "revenue_board", "anti_corruption", "counter_terrorism"] |
| **police_station_fir** | string | Original FIR location | "Police Station Gulberg, Lahore" |
| **fir_number** | string | Links to original report | "FIR-2021-4532" |
| **investigating_officer_name** | string | Key witness credibility | "Inspector Muhammad Hassan" |
| **io_rank** | enum | Seniority affects credibility | ["sub_inspector", "inspector", "dsp", "asu"] |
| **io_competency_concerns** | array[string] | Defense red flags | ["previous_acquittals", "complaint_against_io", "lack_of_training", "conflict_of_interest"] |
| **prosecutor_name** | string | Prosecution legal counsel | "Additional Prosecutor General" |
| **prosecution_strength_rating** | enum | Internal assessment | ["weak", "moderate", "strong", "very_strong"] |

### C2: Accused/Defendant Information
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **accused_full_name** | string | Primary identification | "Muhammad Ahmed Khan s/o Ali Khan" |
| **accused_aliases** | array[string] | Known by other names | ["Aamir", "Ahmad Chacha"] |
| **accused_age_at_offense** | number | Juvenile jurisdiction trigger (under 18) | 25 |
| **accused_dob** | date | Age determination disputes | "1998-05-15" |
| **accused_age_determination_method** | enum | Relevant for juvenile cases | ["birth_certificate", "school_records", "medical_examination", "claimed_age"] |
| **accused_previous_convictions** | array[object] | Character evidence | [{case_id: "CRL-2019-1234", offense: "theft", sentence: "2_years", date: "2019-06-10"}] |
| **accused_prior_custody_history** | boolean | Shows compliance/danger to society | true |
| **criminal_history_count** | number | Sentencing aggravating factor | 3 |
| **accomplices_count** | number | Scope of conspiracy | 2 |
| **accomplices_details** | array[object] | Co-accused names and roles | [{name: "Bilal Khan", role: "instigator", status: "acquitted"}] |
| **fugitive_status** | boolean | Fled investigation/trial | true |
| **accused_address** | string | Jurisdiction and residence stability | "House No. 5, Street 3, Gulberg II, Lahore" |
| **socio_economic_status** | enum | Mitigating/aggravating for sentencing | ["poor", "lower_middle", "middle", "upper_middle", "wealthy"] |
| **education_level** | enum | Mitigating factor for rehabilitation potential | ["illiterate", "primary", "matric", "intermediate", "graduate", "postgraduate"] |

### C3: Victim/Complainant Information
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **victim_name** | string | Murder/assault cases | "Fatima Bibi d/o Ghulam Muhammad" |
| **victim_age_at_death** | number | Aggravating if child | 8 |
| **victim_relationship_to_accused** | enum | Motive and defense claims | ["spouse", "child", "parent", "sibling", "employer", "servant", "stranger"] |
| **complainant_name** | string | FIR lodger (may not be victim) | "Iqbal Khan, father of deceased" |
| **complainant_relation_to_victim** | string | Credibility assessment | "brother" |
| **complainant_motive_bias** | array[string] | Defense impeachment angle | ["family_enmity", "land_dispute", "revenge", "false_accusation_history"] |
| **multiple_complaints** | boolean | Filing multiple FIRs (different courts) | true |
| **complaint_delay_days** | number | Affects immediacy of report | 45 |
| **delay_explanation** | string | FIR lodger's account | "victim_hospitalized" |

### C4: Witness Information (Defense Use)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **witness_count_prosecution** | number | Burden strength indicator | 12 |
| **witness_count_defense** | number | Defense credibility counter | 5 |
| **eyewitness_count** | number | Direct evidence rarity | 1 |
| **pww_count** | number | "Prosecution Witness Witnesses" - examined in court | 8 |
| **prosecution_witness_list** | array[object] | All examined prosecution witnesses | [{name: "Constable Ali", designation: "witness_police", examination_date: "2022-05-10", verdict: "credible"}] |
| **dw_count** | number | "Defense Witness" count | 4 |
| **defense_witness_list** | array[object] | All defense witnesses | [{name: "Muhammad Khan (brother)", designation: "character_witness", examination_date: "2022-06-15"}] |
| **court_witness_count** | number | Court-appointed independent witnesses | 0 |

### C5: Expert Witnesses
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **expert_witness_present** | boolean | Changes evidence weight significantly | true |
| **expert_type** | enum | Different standards per type | ["forensic_pathologist", "forensic_chemistry", "ballistics", "dna_expert", "polygraph", "psychological", "medical"] |
| **expert_name** | string | Credibility in jurisdiction | "Dr. Qaiser Malik, Pathologist" |
| **expert_qualification** | string | Training and credentials | "MBBS, Diploma in Forensic Medicine, Government Medical College Lahore" |
| **expert_experience_years** | number | Weight of testimony | 15 |
| **expert_previous_cases_examined** | number | Track record | 200 |
| **expert_findings_key** | array[string] | Direct quote from report | ["time_of_death_22to24_hours", "injury_consistent_with_blunt_force"] |
| **expert_court_examination_date** | date | When expert gave testimony | "2023-03-20" |
| **expert_credibility_assessment** | enum | Judge's evaluation (from judgment) | ["highly_credible", "credible", "partially_credible", "not_credible"] |
| **defense_expert_present** | boolean | Counter-expert evidence | true |
| **conflicting_expert_opinions** | boolean | Creates reasonable doubt opportunity | true |

---

## SECTION D: EVIDENCE - THE PROSECUTION'S CASE STRENGTH

### D1: Physical Evidence Registry
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **physical_evidence_count** | number | Overall case strength | 8 |
| **physical_evidence_list** | array[object] | Itemized with chain of custody issues | [{item_no: 1, description: "12-bore shotgun", recovery_location: "under_bed", recovery_date: "2021-03-22", custody_chain_breaks: false}] |
| **weapon_recovered** | boolean | Direct evidence of instrumentality | true |
| **weapon_type** | enum | Specificity of injury match | ["firearm", "knife", "blunt_object", "poison", "other"] |
| **weapon_forensic_tested** | boolean | Critical for strength assessment | true |
| **weapon_ballistics_match** | boolean | Firearm linked to projectiles/victims | true |
| **weapon_fingerprints_found** | boolean | Identification evidence | true |
| **fingerprints_matched_to_accused** | boolean | Direct link | false |

### D2: Chain of Custody (CrPC Section 103 Critical)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **chain_of_custody_documented** | boolean | Legal admissibility requirement | true |
| **custody_chain_complete** | boolean | Defense exploit point - gaps destroy evidence | true |
| **custody_break_incidents** | array[object] | Each gap weakens prosecution | [{date: "2021-04-10", from: "IO Hassan", to: "unknown", gap_reason: "file_transferred_then_lost_for_3_days", impact: "high"}] |
| **custody_witnesses_present** | boolean | CrPC 103 requires witnesses during recovery | true |
| **recovery_witnesses_examination** | enum | Were they examined in court? | ["both_examined", "one_examined", "neither_examined"] |
| **recovery_witness_credibility** | array[enum] | Individual assessments | ["credible", "credible"] |
| **evidence_sealing_methodology** | enum | Legal requirement | ["sealed_properly", "sealed_inadequately", "unsealed"] |
| **seal_integrity_maintained** | boolean | Tamper-proof chain | true |
| **storage_conditions** | string | Degradation/contamination issues | "Police evidence locker, Room 3, temperature uncontrolled" |

### D3: Forensic Evidence
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **forensic_evidence_type** | array[enum] | Reliability varies by type | ["dna", "fingerprint", "ballistics", "toxicology", "trace_evidence"] |
| **dna_test_conducted** | boolean | Modern evidence strength | true |
| **dna_lab_name** | string | Lab credibility (government vs. private) | "Punjab Forensic Science Agency" |
| **dna_sample_source** | enum | What was tested | ["blood", "saliva", "hair", "semen", "tissue"] |
| **dna_match_accused** | boolean | Direct link | true |
| **dna_match_confidence_percent** | number | Statistical reliability | 99.9 |
| **dna_results_contested** | boolean | Defense challenges | false |
| **fingerprint_evidence** | boolean | Presence of fingerprints | true |
| **fingerprints_from_location** | string | Where recovered | "Kitchen knife handle" |
| **fingerprints_matched_accused** | boolean | Identification strength | true |
| **ballistics_test_done** | boolean | Firearm cases | true |
| **ballistics_match_projectiles** | boolean | Bullet to weapon | true |
| **ballistics_match_casings** | boolean | Shell casings to weapon | true |
| **toxicology_test** | boolean | Poison/drug cases | true |
| **toxicology_substance_found** | enum | What was detected | ["arsenic", "strychnine", "opiates"] |
| **trace_evidence_collected** | boolean | Hair, fiber, glass, soil | true |

### D4: Documentary Evidence
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **documentary_evidence_count** | number | Paper trail strength | 25 |
| **document_type** | array[enum] | Each category has different authentication rules | ["fir", "medical_report", "post_mortem_report", "police_memo", "letter", "bank_document", "land_record"] |
| **forged_document_charges** | boolean | Separate offense | true |
| **document_authentication_method** | enum | How original verified | ["original_produced", "certified_copy", "digital_copy"] |
| **document_chain_of_custody** | boolean | Same scrutiny as physical | true |
| **bank_records_obtained** | boolean | Financial crime cases | true |
| **call_records_obtained** | boolean | Mobile evidence | true |
| **call_record_analysis_done** | boolean | Expert analysis of patterns | true |

### D5: Medical Evidence (Injury Cases)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **post_mortem_done** | boolean | Establishes cause of death | true |
| **post_mortem_report_available** | boolean | Critical for murder cases | true |
| **pm_report_quality** | enum | Legal standard | ["detailed_with_findings", "standard", "minimal"] |
| **cause_of_death_established** | enum | Prosecution burden | ["confirmed_cause", "probable_cause", "undetermined"] |
| **cause_of_death_description** | string | Direct quote | "Hemorrhage due to stab wound to left chest, penetrating left lung and heart" |
| **time_of_death_estimated_hours** | string | Narrows criminal event window | "18-24 hours before post mortem" |
| **time_of_death_range_precision** | enum | Narrower = stronger | ["general_1to2_days", "specific_12hours", "very_specific_2hours"] |
| **injury_count** | number | "Overkill" shows rage/motive | 23 |
| **injury_severity** | enum | Defense argues self-defense impossibility | ["fatal", "grievous", "simple"] |
| **injury_pattern_analysis** | string | Forensic pathology finding | "Multiple stab wounds in cruciform pattern, consistent with heated passion" |
| **medical_opinion_defense_claim** | string | If self-defense: could injuries be self-inflicted | "Post mortem examiner testified injuries could not be self-inflicted" |
| **injury_consistent_with_accused_strength** | boolean | Can smaller accused inflict injuries | false |
| **injury_weapon_type_match** | boolean | Wounds match recovered weapon | true |

### D6: Circumstantial Evidence (Highest Risk for Defense)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **evidence_type_distribution** | enum | Case strength assessment | ["direct_only", "mostly_direct_some_circumstantial", "mostly_circumstantial_some_direct", "wholly_circumstantial"] |
| **circumstantial_evidence_count** | number | Multiple weak links or few strong links | 7 |
| **motive_evidence** | array[string] | Shows accused had reason | ["property_dispute_documents", "witness_testimony_enmity", "inheritance_claims"] |
| **motive_strength** | enum | Prosecution ease of proof | ["strong_provable_motive", "weak_alleged_motive", "no_clear_motive"] |
| **opportunity_evidence** | array[string] | Shows accused could have done it | ["presence_at_location", "access_to_location", "no_alibi"] |
| **presence_at_crime_scene** | enum | Eyewitness vs. circumstantial | ["confirmed_eyewitness", "likely_from_circumstance", "unproven"] |
| **alibi_defense_raised** | boolean | Defense counters opportunity | true |
| **alibi_evidence_strength** | enum | How solid is alibi | ["strong_with_multiple_witnesses", "weak_single_witness", "no_corroboration"] |
| **last_seen_together_evidence** | boolean | "Seen together" shortly before/after | true |
| **recovery_from_possession** | boolean | Stolen property recovered from accused | true |
| **recovery_explanation** | string | Accused's account | "I purchased the mobile phone from shopkeeper, not aware it was stolen" |
| **consciousness_of_guilt_evidence** | array[string] | Behavioral indicators | ["fled_jurisdiction", "attempted_suicide", "destroyed_evidence", "tried_to_bribe_witness"] |
| **flight_after_arrest** | boolean | Escape attempt | true |
| **evidence_destruction_evidence** | boolean | Wash hands, change clothes, etc. | true |
| **knowledge_only_culprit_would_have** | array[string] | "Secret knowledge" test | ["location_of_weapon_before_recovery", "detail_of_victims_injuries"] |

---

## SECTION E: PROCEDURAL DEFECTS & EXPLOITATION (Defense Ammunition)

### E1: FIR Recording Defects
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **fir_recorded_by_whom** | enum | Must be officer, not accused | ["police_officer", "accused_own_statement", "complainant_directly"] |
| **fir_recording_delay_hours** | number | Immediacy affects credibility | 3 |
| **fir_oral_vs_written** | enum | CrPC 154 requires writing | ["oral_reduced_to_writing", "written_directly", "recorded_days_later"] |
| **fir_lodger_examination_done** | boolean | Must be examined in court (Qanun-e-Shahadat) | true |
| **fir_discrepancies_with_testimony** | array[string] | Defense impeachment ground | ["location_changed", "weapon_type_different", "number_of_accused_changed"] |
| **fir_section_objectionable** | boolean | Section 302 charged but later downgraded to 304 | true |
| **fir_vague_description** | boolean | Insufficient particulars | false |
| **fir_based_on_suspicion_only** | boolean | No credible information | false |

### E2: Investigation Defects (Major Defense Argument)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **investigation_quality_assessment** | enum | Judge will note defects | ["thorough_systematic", "adequate", "defective", "highly_defective"] |
| **investigation_defect_description** | array[string] | Specific gaps to exploit | ["key_witness_not_examined", "crime_scene_not_visited_by_io", "relevant_evidence_not_collected", "no_interrogation_notes_recorded"] |
| **investigation_length_days** | number | Rushed investigations more error-prone | 120 |
| **investigation_completion_premature** | boolean | Closed before all leads followed | false |
| **investigating_officer_competency** | enum | Experience/training assessment | ["experienced", "average", "inexperienced"] |
| **police_malpractice_alleged** | boolean | Torture, false evidence planting | true |
| **police_brutality_fir** | boolean | Counter-FIR against IO | true |
| **io_prior_acquittals** | number | Track record of failed prosecutions | 5 |

### E3: Arrest & Custody Defects
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **arrest_lawful** | boolean | Unlawful arrest voids all evidence collected | true |
| **arrest_warrant_obtained** | boolean | Required for cognizable offense | true |
| **arrest_without_warrant_justification** | string | CrPC 41 exceptions | "Suspect fleeing, imminent escape danger" |
| **arrest_date** | date | Links to detention rules | "2021-03-25" |
| **arrest_time_recorded** | boolean | Must be documented | true |
| **custody_duration_total_days** | number | CrPC 167 limits police custody | 7 |
| **police_custody_days** | number | Max 3 before magistrate | 3 |
| **police_custody_magistrate_visits** | number | Should visit every 3 days | 2 |
| **judicial_custody_obtained** | boolean | After police custody ends | true |
| **remand_order_copy_given_accused** | boolean | Must provide, often skipped | false |
| **torture_allegations** | boolean | Major plea ground | false |
| **torture_medical_examination** | boolean | Was torture examined by doctor | true |
| **custody_illegal_extension** | boolean | Beyond CrPC 167 limits | false |

### E4: Section 161 CrPC Defects (Police Statements)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **section_161_statements_recorded** | boolean | Police examination of witness | true |
| **section_161_statements_count** | number | Quantity of police witness statements | 8 |
| **section_161_examination_notes_quality** | enum | Detailed or summary | ["detailed_verbatim", "summary", "minimal_notes"] |
| **section_161_statement_given_to_defense** | boolean | Must provide copy before trial | false |
| **section_161_statement_examined_in_court** | boolean | To be substantive, must examine in court | true |
| **section_161_inconsistency_with_testimony** | array[string] | Defense use to impeach | ["date_different", "details_omitted"] |
| **section_161_privilege_claimed** | boolean | Witness refuses to answer | false |

### E5: Section 164 CrPC Defects (Judicial Statements)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **section_164_statement_recorded** | boolean | Magistrate-recorded confession/statement | true |
| **section_164_officer_present** | enum | Police should NOT be present during recording | ["police_absent_correct", "police_present_violation", "ambiguous"] |
| **section_164_voluntariness** | boolean | Legal requirement | true |
| **section_164_voluntariness_challenged** | boolean | Defense argument of coercion | true |
| **section_164_recording_magistrate_independence** | boolean | Could magistrate be biased | false |
| **section_164_accused_represented** | boolean | Right to counsel during recording | false |
| **section_164_translation_required** | boolean | If not in accused's language | true |
| **section_164_translation_certified** | boolean | Was translation official | false |

### E6: Evidence Collection Procedure Violations
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **search_warrant_obtained** | boolean | Required for property search (CrPC 94-100) | false |
| **search_without_warrant_justification** | string | Exceptions: consent, exigent circumstances | "Accused consented to search" |
| **search_witness_present** | boolean | CrPC 103 requires independent witnesses | true |
| **search_witness_examination_in_court** | boolean | Witnesses must testify | false |
| **recovery_memo_prepared** | boolean | Written record of recovery | true |
| **recovery_memo_signed_by_witnesses** | boolean | Both search and recovery witnesses | true |
| **recovery_memo_photo_documentation** | boolean | Photos of scene, evidence | false |
| **recovery_memo_video_documentation** | boolean | Video record (modern practice) | false |
| **evidence_mislabeling** | boolean | Wrong exhibit number/description | false |
| **evidence_contamination_risk** | boolean | Exposed to elements/animals | true |

---

## SECTION F: WITNESS CREDIBILITY & EXAMINATION

### F1: Eyewitness Evidence Quality
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **eyewitness_present_crime_scene** | boolean | Direct observation vs. hearsay | true |
| **eyewitness_proximity_to_scene_meters** | number | Distance affects reliability | 10 |
| **eyewitness_visibility_conditions** | enum | Light, weather, obstruction | ["bright_daylight", "twilight", "darkness_no_light", "darkness_with_light"] |
| **eyewitness_observation_duration_seconds** | number | Brief sighting vs. prolonged observation | 45 |
| **eyewitness_familiarity_with_accused** | enum | Knew accused before or first seeing | ["familiar", "stranger", "glimpse_only"] |
| **eyewitness_prior_identification_procedure** | boolean | ID parade, photo album, etc. | true |
| **eyewitness_identification_procedure_defects** | array[string] | Defense challenges (Doll test issues) | ["no_parade_conducted", "suggestive_parade", "accused_obvious"] |
| **eyewitness_in_court_identification** | boolean | Pointed out accused in court | true |
| **eyewitness_prior_statement_consistent** | boolean | Statement to police matches court testimony | true |
| **eyewitness_prior_police_statement_date** | date | How soon after crime | "2021-03-22" |

### F2: Witness Credibility Factors (Qanun-e-Shahadat Article 135-151)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **witness_education_level** | enum | Affects comprehension and reliability | ["illiterate", "primary", "matric", "graduate"] |
| **witness_character** | enum | General reputation for truthfulness | ["good", "neutral", "questionable", "bad"] |
| **witness_criminal_record** | boolean | Prior convictions affect credibility | true |
| **witness_credibility_impeached** | boolean | Defense successfully challenged witness | true |
| **witness_impeachment_ground** | array[enum] | Qanun-e-Shahadat Article 151 grounds | ["prior_conviction", "prior_inconsistent_statement", "interest_in_case", "bias", "enmity"] |
| **witness_interest_in_case** | enum | Beneficiary of verdict | ["defendant", "plaintiff_party", "neutral_party", "financial_interest"] |
| **witness_relationship_to_parties** | enum | Family, enemy, employer | ["family_member", "friend", "enemy", "neutral"] |
| **witness_bias_alleged** | boolean | Prejudiced against accused | true |
| **witness_prior_enmity_with_accused** | boolean | Makes testimony suspect | false |
| **witness_financial_stake** | boolean | Inheritance, property, debt affected | true |

### F3: Cross-Examination Record
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **cross_examination_conducted** | boolean | Right to cross-examine (Qanun-e-Shahadat Article 141) | true |
| **cross_examination_duration_minutes** | number | Intense cross-examination weakens testimony | 120 |
| **cross_examination_quality_assessment** | enum | Judge notes effectiveness | ["thorough_effective", "adequate", "superficial", "defensive_lawyer_incompetent"] |
| **witness_answers_satisfactory** | enum | Judge's assessment of responses | ["fully_answered", "evasive", "contradicted"] |
| **witness_admission_during_cross** | boolean | Witness admitted inconsistency/lie | true |
| **witness_confession_during_cross** | boolean | Admitted something damaging | false |
| **hostile_witness_declared** | boolean | Judge declared prosecution witness hostile | true |
| **hostile_witness_redirect_examination** | boolean | Prosecutor trying to rehab testimony | true |

### F4: Witness Examination Quality Issues
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **examination_in_chief_question_quality** | enum | Leading questions not allowed | ["non_leading_proper", "leading_improper"] |
| **examination_in_chief_length_minutes** | number | Detailed or rushed | 45 |
| **leading_questions_in_chief** | boolean | Not allowed (Qanun-e-Shahadat Article 136, 141) | false |
| **examination_incomplete** | boolean | Key areas not covered | false |
| **re_examination_allowed** | boolean | Clarify cross-exam points | true |
| **witness_memory_questioned** | boolean | "Do you remember..." credibility test | true |
| **witness_detail_recall_ability** | enum | Specific vs. vague | ["vivid_detailed", "general_outline", "vague"] |
| **contradictions_in_testimony** | number | Internal inconsistencies count | 3 |

### F5: Witness Types & Their Legal Treatment
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **witness_category** | enum | Different competency rules (Qanun-e-Shahadat Article 118-122) | ["adult_citizen", "child", "mental_disability", "interested_party", "police"] |
| **child_witness_age** | number | Competency threshold varies by age | 8 |
| **child_witness_competency_assessed** | boolean | Judge must test understanding | true |
| **child_witness_oath_taken** | boolean | Can child take oath, or unsworn statement | true |
| **police_witness_credibility_extra_scrutiny** | boolean | Courts examine police evidence closely | true |
| **accomplice_witness** | boolean | Co-accused testifying for prosecution | false |
| **accomplice_testimony_corroboration** | boolean | Must have independent corroboration | true |
| **lady_witness_privacy_maintained** | enum | Gender witness protection | ["public_examination", "female_judge_if_available", "privacy_screen"] |
| **expert_witness_opinion_allowed** | boolean | Beyond facts, expert opinions (Qanun-e-Shahadat Article 45) | true |

---

## SECTION G: PROCEDURAL & JURISDICTIONAL ISSUES

### G1: Trial Procedure Compliance
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **charges_framed_properly** | boolean | CrPC 225 requirements | true |
| **charges_read_to_accused** | boolean | Accused must hear charges | true |
| **charges_explained_in_language** | enum | Urdu or local language | ["urdu", "english_with_translation", "local_language"] |
| **plea_recorded_clear** | boolean | Accused guilty/not guilty response | true |
| **plea_voluntary** | boolean | Not coerced | true |
| **plea_recorded_in_writing** | boolean | Documented | true |
| **trial_procedure_followed** | enum | CrPC 229-229A | ["proper_order_charges_plea_hearing", "irregular_procedure", "summary_trial"] |
| **accused_legal_representation** | enum | Right to counsel | ["represented_by_advocate", "pro_bono_advocate", "self_represented"] |
| **accused_state_counsel_appointed** | boolean | If indigent | false |
| **defense_adequate** | enum | Judge's assessment of defense quality | ["thorough_competent", "adequate", "inadequate", "ineffective"] |

### G2: Trial Duration & Delays
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **trial_start_date** | date | When formal trial began | "2021-07-10" |
| **trial_completion_date** | date | Final judgment | "2023-06-15" |
| **trial_adjournment_count** | number | Excessive delays hurt prosecution case | 15 |
| **adjournment_reasons** | array[enum] | Some grounds legitimate, some not | ["witness_unavailable", "advocate_unavailable", "court_busy", "no_reason_given"] |
| **witness_gap_between_evidence_and_judgment_months** | number | Memory degradation over time | 18 |
| **appeal_pending_at_judgment** | boolean | Was case heard while bail appeal pending | false |

### G3: Bail/Custody History (CrPC 496-498)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **bail_application_count** | number | Repeated applications show persistence/desperation | 4 |
| **bail_applications_granted** | number | Success rate | 1 |
| **bail_granted_amount_pkr** | number | Surety requirement | 500000 |
| **bail_sureties_provided** | number | How many sureties | 2 |
| **bail_sureties_financial_status** | enum | Can sureties actually cover amount | ["wealthy", "moderate", "poor"] |
| **pre_arrest_bail_status** | enum | Anticipatory/protective bail (CrPC 498) | ["granted", "denied", "not_sought"] |
| **pre_arrest_bail_interim** | boolean | Ad-interim bail before hearing | true |
| **post_arrest_bail_status** | enum | Regular bail after arrest | ["granted", "denied", "pending"] |
| **bail_conditions_imposed** | array[string] | Reporting, restrictions, sureties | ["report_weekly_to_police", "international_travel_ban", "reside_at_fixed_address"] |
| **bail_conditions_compliance** | boolean | Did accused follow conditions | true |
| **bail_cancellation** | boolean | Bail cancelled and arrested | false |
| **bail_cancellation_ground** | enum | Why cancelled | ["non_compliance", "new_evidence", "threat_to_witness"] |
| **custody_in_jail_total_months** | number | Pre-trial detention duration | 8 |
| **custody_credited_to_sentence** | boolean | Time served counted as sentence | true |
| **custody_credit_days** | number | How many days credited | 240 |

---

## SECTION H: EVIDENCE LAW SPECIFICS (Qanun-e-Shahadat)

### H1: Evidence Types & Admissibility
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **evidence_type_breakdown** | object | Composition of prosecution case | {direct: 30, circumstantial: 50, hearsay: 10, expert: 10} |
| **hearsay_evidence_present** | boolean | Qanun-e-Shahadat Article 60 bars hearsay | true |
| **hearsay_exception_applied** | enum | Limited exceptions (dying declaration, res gestae) | ["dying_declaration", "res_gestae", "admission_by_party", "none_applicable"] |
| **dying_declaration_evidence** | boolean | Exception: victim's last words | true |
| **dying_declaration_content** | string | What victim said | "It was Ahmed who shot me" |
| **dying_declaration_witness** | string | Who heard it | "Constable Muhammad Ali" |
| **res_gestae_evidence** | boolean | Spontaneous utterance during event | false |
| **leading_question_objection** | boolean | Improper questioning method | true |
| **evidence_illegally_obtained** | boolean | Fruit of the poisonous tree | false |
| **evidence_illegally_obtained_type** | enum | How obtained illegally | ["unlawful_search", "coerced_statement", "torture_induced"] |

### H2: Character Evidence (Qanun-e-Shahadat Article 41-55)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **character_evidence_by_prosecution** | boolean | Prosecution attacks defense character (rare) | false |
| **character_evidence_by_defense** | boolean | Defense calls character witnesses | true |
| **character_witness_count_defense** | number | How many character witnesses | 3 |
| **character_witness_examination** | string | Reputation or personal knowledge | "personal_knowledge_of_honesty" |
| **accused_reputation_community** | enum | General community perception | ["good", "neutral", "bad"] |
| **accused_prior_criminal_convictions** | boolean | Can be used to attack character | true |
| **prior_conviction_admissibility** | enum | When allowed, when not | ["admissible_if_relevant", "admissible_with_limitation", "not_admissible"] |
| **similar_fact_evidence** | boolean | Similar offenses in past | false |
| **similar_fact_relevance** | enum | Shows pattern or modus operandi | ["pattern_evidence", "modus_operandi", "not_admissible"] |

### H3: Expert Evidence Standards (Qanun-e-Shahadat Article 45-51)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **expert_qualified_properly** | boolean | Meets Article 45 requirements | true |
| **expert_opinion_basis** | enum | Founded on facts in case or other cases | ["case_facts", "general_knowledge", "mixed"] |
| **expert_opinion_admissible** | boolean | Beyond lay persons' knowledge | true |
| **expert_opinion_weight** | enum | Judge's assessment | ["high_weight", "moderate_weight", "little_weight"] |
| **conflicting_expert_opinions** | boolean | Different experts disagree | true |
| **expert_bias_alleged** | boolean | Expert favored prosecution | true |
| **expert_examination_by_defense** | boolean | Defense cross-examined expert | true |
| **expert_opinion_overruled** | boolean | Judge rejected expert opinion | false |

---

## SECTION I: BAIL JURISPRUDENCE (Critical for Sentencing Prediction)

### I1: Bail Principles (CrPC 496-498 and Supreme Court Case Law)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **offense_nature** | enum | Heinous vs. bailable offenses | ["heinous_capital", "serious_non_capital", "bailable"] |
| **offense_gravity** | enum | Severity assessment | ["most_serious", "serious", "moderate", "minor"] |
| **presumption_of_innocence** | enum | How much weight given | ["strong_presumption", "weak_presumption", "rebuttable"] |
| **flight_risk_assessment** | enum | Likelihood accused will flee | ["high_risk", "moderate_risk", "low_risk"] |
| **flight_indicators** | array[string] | Factors showing flight likelihood | ["no_fixed_address", "foreign_nationality", "prior_flight", "resources_to_flee"] |
| **danger_to_society** | enum | Threat to public safety | ["high_danger", "moderate_danger", "low_danger"] |
| **danger_to_witnesses** | enum | Will accused interfere with witnesses | ["high_risk", "moderate_risk", "low_risk"] |
| **witness_intimidation_evidence** | boolean | History of threats/intimidation | true |
| **witness_intimidation_specifics** | array[string] | What did accused do | ["visited_witness_home", "threatened_family", "offered_bribe"] |

### I2: Sentencing Principles (Critical for All Cases)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **conviction_certainty** | enum | How confident judge of guilt | ["beyond_reasonable_doubt", "moral_certainty", "doubt_exists"] |
| **sentence_imposed_years** | number | Prison term length | 10 |
| **sentence_imposed_months** | number | Additional months | 6 |
| **sentence_type** | enum | Form of punishment | ["death_penalty", "life_imprisonment", "rigorous_imprisonment", "simple_imprisonment", "fine"] |
| **sentence_quantum_justified** | boolean | Judge explained sentence reasoning | true |
| **sentence_explained_in_judgment** | boolean | Reasoning documented | true |

### I3: Aggravating Factors (Increase Sentence)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **aggravating_factors_identified** | array[enum] | Judge noted circumstances worsening guilt | ["premeditation_clear", "brutality", "vulnerable_victim", "abuse_of_trust", "multiple_victims", "prior_conviction"] |
| **premeditation_evident** | boolean | Planned in advance | true |
| **brutality_level** | enum | Violence severity | ["extreme_sadistic", "brutal", "normal_violence", "minimal"] |
| **victim_vulnerability** | enum | Victim's defenselessness | ["child", "elderly", "disabled", "stranger", "acquaintance"] |
| **abuse_of_trust** | boolean | Accused was trusted by victim | true |
| **abuse_of_trust_type** | enum | Relationship abuse | ["parent_to_child", "teacher_to_student", "employer_to_servant", "spiritual_leader"] |
| **multiple_victims** | boolean | More than one victim | true |
| **prior_conviction_same_type** | boolean | Repeat offender | true |
| **organized_crime_connection** | boolean | Part of organized crime gang | true |
| **weapon_used_dangerous** | boolean | Dangerous weapon vs. fists | true |
| **weapon_sophistication** | enum | Level of premeditation shown by weapon | ["firearm", "explosive", "knife", "poison", "blunt_object"] |
| **injuries_excessive** | boolean | "Overkill" showing rage | true |
| **victim_age_child** | boolean | Child victim aggravates massively | true |
| **victim_age_elderly** | boolean | Elderly victim also aggravates | false |
| **victim_female_assaulted** | boolean | Gender crimes penalized harshly | true |
| **sexual_nature_of_crime** | boolean | Sexual crime or rape | true |
| **torture_involved** | boolean | Prolonged suffering | true |
| **public_nature_crime** | boolean | Committed in public vs. private | true |
| **lack_of_remorse** | boolean | Accused shows no regret | true |

### I4: Mitigating Factors (Reduce Sentence)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **mitigating_factors_identified** | array[enum] | Judge noted circumstances favoring leniency | ["youth", "first_offense", "good_character", "provocation", "mental_illness", "duress", "family_hardship"] |
| **accused_age_young** | boolean | Youth shows rehabilitation potential | true |
| **accused_age_at_crime** | number | How young when committed offense | 18 |
| **first_offense** | boolean | No prior convictions | true |
| **family_dependents** | number | Number of dependents accused supports | 3 |
| **family_hardship** | boolean | Imprisonment causes family suffering | true |
| **good_character_evidence** | boolean | Family/community supports accused | true |
| **provocation_claim** | boolean | Victim provoked the crime | true |
| **provocation_evidence_weight** | enum | How substantial the provocation | ["grave_provocation", "minor_provocation", "no_real_provocation"] |
| **mental_illness** | boolean | Psychological factors | true |
| **mental_illness_type** | enum | Diagnosed condition | ["schizophrenia", "bipolar", "depression", "temporary_insanity"] |
| **mental_illness_linked_to_crime** | boolean | Illness caused the offense | true |
| **mental_illness_treatment_ongoing** | boolean | Under medical care | true |
| **intoxication_at_time** | boolean | Drugs/alcohol reduced responsibility | true |
| **intoxication_voluntary** | boolean | Self-induced vs. forced | true |
| **intoxication_crime_link** | boolean | Did intoxication cause crime | true |
| **duress_claim** | boolean | Forced by someone | false |
| **duress_imminent_threat** | boolean | Threat of immediate harm | true |
| **duress_third_party_threat** | string | Who threatened accused | "Gang leader threatened to kill family" |
| **cooperation_with_prosecution** | boolean | Turned approver/informer | false |
| **remorse_shown** | boolean | Accused expressed genuine remorse | true |
| **restitution_made** | boolean | Accused paid compensation | true |
| **restitution_amount_pkr** | number | How much compensation | 500000 |
| **rehabilitation_potential** | enum | Can accused be reformed | ["high", "moderate", "low"] |
| **institutional_conduct** | enum | Behavior in jail during trial | ["exemplary", "good", "problematic"] |

---

## SECTION J: CONVICTION QUALITY METRICS (For AI Confidence Scoring)

### J1: Evidence Strength Scoring
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **direct_evidence_strength** | number (0-100) | AI metric: percentage confidence from direct evidence | 75 |
| **circumstantial_evidence_strength** | number (0-100) | Completeness of circumstantial chain | 60 |
| **forensic_evidence_strength** | number (0-100) | Reliability of forensic findings | 85 |
| **witness_credibility_aggregate** | number (0-100) | Combined witness reliability | 70 |
| **expert_evidence_reliability** | number (0-100) | Expert opinion weight | 65 |
| **overall_prosecution_strength** | number (0-100) | Composite prosecution case strength | 72 |
| **conviction_risk_defense** | number (0-100) | Likelihood of conviction if trial proceeds | 72 |
| **acquittal_risk_prosecution** | number (0-100) | Opposite metric | 28 |

### J2: Procedural Strength Scoring
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **procedural_compliance_score** | number (0-100) | How well investigation followed law | 65 |
| **chain_of_custody_quality** | number (0-100) | Evidence integrity | 80 |
| **arrest_legality_score** | number (0-100) | Lawfulness of arrest/detention | 90 |
| **trial_fairness_score** | number (0-100) | Due process compliance | 75 |
| **defense_adequacy_score** | number (0-100) | Quality of defense representation | 60 |
| **appellable_defects_count** | number | Grounds for appeal/revision | 3 |

### J3: Judgment Quality Indicators
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **judgment_reasoning_quality** | enum | Judge's explanation of verdict | ["thorough_detailed", "adequate", "superficial", "contradictory"] |
| **judgment_contradictions** | number | Internal logical conflicts | 0 |
| **precedent_citation_count** | number | Cases cited | 12 |
| **precedent_application_correct** | boolean | Precedents applied appropriately | true |
| **judgment_length_pages** | number | Detailed vs. summary judgment | 45 |
| **judgment_appeal_likelihood** | enum | Assessment of appeal success odds | ["very_likely", "likely", "unlikely", "very_unlikely"] |

---

## SECTION K: CASE-SPECIFIC PATTERNS FOR SEARCH

### K1: Common Defense Strategies (What Defense Lawyer Searches For)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **defense_strategy_primary** | enum | Main line of defense | ["alibi", "mistaken_identity", "self_defense", "insanity", "reasonable_doubt", "procedural_defect"] |
| **alibi_presented** | boolean | Accused was elsewhere | true |
| **alibi_witnesses** | number | People supporting alibi | 2 |
| **alibi_corroboration** | enum | How strong | ["strong_independent_corroboration", "family_corroboration_only", "accused_uncorroborated"] |
| **mistaken_identity_raised** | boolean | Wrong person accused | false |
| **mistaken_identity_evidence** | array[string] | Why identification flawed | ["poor_visibility", "long_time_gap", "similarity_to_real_culprit"] |
| **self_defense_claimed** | boolean | CrPC 96-106 claim | true |
| **self_defense_section** | enum | Which section of law | ["section_96_private_defense", "section_97_extent", "section_99_nighttime_property"] |
| **self_defense_injury_cause** | string | How accused injured | "Victim attacked first with knife" |
| **self_defense_proportionality** | enum | Was response proportional | ["proportional_reasonable", "excessive_force", "no_threat_present"] |
| **insanity_plea** | boolean | CrPC 84 mental capacity | false |
| **insanity_medical_evidence** | boolean | Psychiatric reports | false |
| **intoxication_partial_defense** | boolean | Reduces mens rea requirement | true |
| **intoxication_specific_intent** | boolean | Specific intent crime allowing defense | true |
| **provocation_defense** | boolean | Grave and sudden provocation | true |
| **provocation_threshold_met** | enum | Legal standard met | ["yes_clear_provocation", "borderline", "no_provocation"] |

### K2: Prosecution Patterns (What Prosecutor Searches For)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **prosecution_strategy_primary** | enum | Main line of attack | ["motive_opportunity", "circumstantial_chain", "forensic_evidence", "confessional_statement"] |
| **motive_proven** | boolean | Why accused did it | true |
| **motive_witnesses** | number | How many testified about motive | 3 |
| **opportunity_proven** | boolean | Accused was there | true |
| **opportunity_timeline** | enum | How tight is timeline | ["very_tight_minutes", "loose_hours", "unclear"] |
| **possession_recovery** | boolean | Stolen goods or weapon recovered | true |
| **possession_accused_home** | boolean | Found at accused residence | true |
| **confessional_statement** | boolean | Accused confessed | true |
| **confession_voluntary** | boolean | Not coerced (legal requirement) | true |
| **confession_detailed** | boolean | Specific details only culprit knows | true |
| **confession_corroborated** | boolean | Evidence supports confession | true |
| **confession_court_examination** | boolean | Confessing witness examined in court | true |
| **recovery_by_confession** | boolean | Witness found weapon via confession | true |
| **recovery_witness_credibility** | boolean | Person guiding to recovery credible | true |

### K3: Sentencing Pattern Search (Precedent Matching)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **similar_offense_precedents** | array[string] | Link to similar cases | ["Murder with premeditation 2021", "Honor killing 2022", "Planned murder due to enmity 2020"] |
| **similar_offense_sentences** | array[number] | Years imposed in similar cases | [10, 15, 12] |
| **similar_facts_matching_count** | number | How many facts match precedent cases | 6 |
| **sentencing_range_identified** | string | Precedent-based range | "10-15 years rigorous imprisonment" |
| **sentence_above_range** | boolean | Judge imposed higher sentence | false |
| **sentence_within_range** | boolean | Judge followed precedent range | true |
| **sentence_below_range** | boolean | Judge imposed lower sentence | false |
| **sentence_justification_leniency** | string | Why lower if applicable | "First offense, young age, mitigating circumstances" |
| **sentencing_discretion_exercised** | boolean | Judge had discretion | true |

---

## SECTION L: CASE OUTCOME & APPEALS

### L1: Conviction Quality Assessment
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **conviction_strength** | enum | Confidence level in verdict | ["unassailable", "strong", "adequate", "weak", "very_weak"] |
| **reasonable_doubt_risk** | enum | Could verdict be overturned on doubt | ["minimal_risk", "moderate_risk", "substantial_risk", "very_likely_overturn"] |
| **grounds_for_appeal_count** | number | How many appealable issues | 4 |
| **grounds_for_appeal_list** | array[enum] | Specific appealable defects | ["chain_of_custody_break", "procedural_defect_arrest", "unreliable_witness", "expert_opinion_rejected"] |
| **likelihood_appeal_success** | enum | Appellate court reversal odds | ["very_likely_success", "likely_success", "uncertain", "unlikely_success"] |

### L2: Appeal Status
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **appeal_filed** | boolean | Case appealed to higher court | true |
| **appeal_filed_by** | enum | Who is appealing | ["prosecution", "defense", "both"] |
| **appeal_case_number** | string | Appellate court case ID | "Cr.A. No. 456/2023" |
| **appeal_filing_date** | date | When appeal lodged | "2023-07-15" |
| **appeal_stay_granted** | boolean | Sentence stayed pending appeal | true |
| **appeal_bail_pending** | boolean | Accused released pending appeal | true |
| **appeal_hearing_date** | date | When appellate court heard case | "2024-03-20" |
| **appeal_status** | enum | Current status | ["pending", "decided", "disposed", "dismissed"] |
| **appeal_verdict** | enum | If decided, what was outcome | ["appeal_allowed_conviction_quashed", "appeal_dismissed_conviction_upheld", "appeal_partially_allowed_sentence_reduced"] |
| **appeal_court_judgment_date** | date | When appellate decision issued | "2024-06-10" |

### L3: Supreme Court/Final Status
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **supreme_court_petition_filed** | boolean | Petition for special leave to appeal (PLD reference) | true |
| **supreme_court_petition_number** | string | Case number | "Crl. P.L.D. No. 789/2024" |
| **supreme_court_petition_date** | date | When filed | "2024-07-10" |
| **supreme_court_hearing_date** | date | If heard | "2025-02-15" |
| **supreme_court_decision** | enum | Outcome if decided | ["petition_allowed_case_remitted", "petition_dismissed", "pending"] |
| **final_verdict_status** | enum | Case finality | ["final_binding", "under_appeal", "awaiting_supreme_court"] |
| **time_to_finality_years** | number | How long to reach final verdict | 4.25 |

---

## SECTION M: SPECIAL OFFENSE CATEGORIES - DETAILED DATAPOINTS

### M1: Sexual Offenses (PPC Sections 375-376)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **sexual_offense_type** | enum | Different legal standards | ["rape", "statutory_rape", "consensual_intercourse", "sodomy", "indecent_assault", "harassment"] |
| **rape_with_consent_defense** | boolean | "She consented" allegation | true |
| **victim_age** | number | Minor victims = no consent possible | 16 |
| **victim_age_at_offense** | number | When crime occurred | 12 |
| **victim_age_virgin_status** | boolean | Outdated legal consideration (still used) | true |
| **victim_character_attacked** | boolean | Defense attacks victim reputation | true |
| **victim_prior_relationships** | boolean | Prosecution raises | false |
| **force_used_evidence** | boolean | Physical coercion | true |
| **force_evidence_type** | enum | What shows force | ["witness_testimony", "medical_injury", "victim_statement"] |
| **penetration_established** | boolean | Medical evidence of sexual contact | true |
| **medical_examination_evidence** | boolean | Rape kit, medical report | true |
| **medical_examination_timely** | boolean | Done shortly after crime | false |
| **medical_examination_delay_hours** | number | How long delayed | 48 |
| **dna_evidence_rape_kit** | boolean | DNA from rape kit | true |
| **dna_accused_match** | boolean | DNA matches accused | true |
| **virginity_test_performed** | boolean | Outdated/invalid test done | true |
| **virginity_test_legal_value** | boolean | Has any legal weight | false |
| **victim_delay_reporting** | number | Days before reporting | 5 |
| **delay_reporting_explained** | string | Why delayed | "Fear of social stigma, family pressure" |
| **consent_age_of_consent_violation** | boolean | Minor cannot consent legally | true |
| **age_of_consent_ppc** | number | Legal age of consent | 16 |

### M2: Murder with Sexual Element (Heinous Crimes)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **rape_murder_combined** | boolean | Sexual assault then murder | true |
| **sexual_assault_pre_death** | boolean | Happened before killing | true |
| **sexual_assault_post_death** | boolean | Necrophilia allegations | false |
| **injury_pattern_sexual_violence** | boolean | Injuries show sexual brutality | true |
| **multiple_assailants** | number | Gang rape scenario | 3 |
| **gang_rape_dynamics** | string | How offenders participated | "3 perpetrators, 1 guarded victim, others assaulted" |

### M3: Terrorism Cases (ATA 1997 Specific)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **ata_trial_court** | boolean | Anti-Terrorism Court (ATC) only | true |
| **ata_death_penalty_case** | boolean | Capital offense charged | true |
| **ata_bail_availability** | boolean | Restricted bail in ATA cases | true |
| **ata_evidence_standard** | enum | Different burden | ["beyond_reasonable_doubt", "circumstantial_evidence_allowed"] |
| **ata_schedule_offense_level** | enum | Schedule I, II, III | ["schedule_1_terrorism", "schedule_2_terrorism_financing"] |
| **ata_financing_alleged** | boolean | Funding terrorism | true |
| **ata_financing_evidence** | array[string] | Bank transfers, hawala, etc. | ["bank_transfers", "hawala_evidence", "witness_testimony"] |
| **ata_armed_group_connection** | boolean | Linked to terrorist organization | true |
| **ata_organization_name** | enum | Which terrorist group | ["ttp", "al_qaeda", "isis", "lashkar", "jaish"] |
| **ata_organization_evidence** | array[string] | How linked to group | ["recruitment_evidence", "training_camp_attendance", "literature_possession"] |
| **ata_mandatory_death_penalty** | boolean | If death caused, death penalty mandatory | true |
| **ata_death_penalty_imposed** | boolean | Was death penalty actually given | false |
| **ata_death_penalty_waived_reasons** | enum | Why death penalty not imposed | ["no_death_caused", "mitigating_circumstances", "young_age"] |

### M4: Honor Crimes (Culturally Significant)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **honor_crime_defense** | boolean | "Victim brought shame" claim | true |
| **honor_crime_statute** | string | PPC Section 302 with honor defense | "Section 302 with Article 338-G reference" |
| **honor_crime_motive** | enum | Claimed dishonor reason | ["extramarital_affair", "unwanted_marriage_refusal", "elopement", "relationships_with_outsiders"] |
| **victim_relationship_honor** | enum | Who harmed family honor | ["wife_suspect_adultery", "daughter_relationships", "sister_elopement"] |
| **family_council_decision** | boolean | Jirga or Panchayat decided victim death | true |
| **forced_confession** | boolean | Family forced accused to confess | true |
| **honor_crime_accomplices** | number | Family members involved | 4 |
| **honor_crime_apology_settlement** | boolean | Family paid diyat/settled | true |
| **honor_crime_mitigation_claimed** | boolean | Judge considers "family honor" | true |
| **judge_sympathy_honor_defense** | enum | Did judge show sympathy to honor claim | ["sympathetic_light", "neutral_treatment", "skeptical_of_honor_claim"] |

### M5: Sectarian Violence Cases
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **sectarian_violence_case** | boolean | Shia-Sunni violence | true |
| **sectarian_motive_proven** | boolean | Prosecution linked to sectarian hatred | true |
| **sectarian_organization_involved** | boolean | Militant group connection | true |
| **sectarian_premeditation** | boolean | Planned sectarian killing | true |
| **victim_sectarian_identity** | enum | Religious sect of victim | ["shia", "sunni"] |
| **accused_sectarian_identity** | enum | Religious sect of accused | ["sunni"] |
| **sectarian_hate_speech_evidence** | boolean | Accused made sectarian statements | true |
| **sectarian_hate_speech_sample** | string | Quote from accused | "Infidels deserve death" |
| **sectarian_killing_pattern** | boolean | Part of series of sectarian killings | true |
| **sectarian_violence_area** | string | Geographic concentration | "Karachi Shia neighborhoods" |
| **religious_leader_involvement** | boolean | Clerics incited violence | true |
| **ata_sectarian_terrorism** | boolean | Charged under ATA sectarian terrorism | true |

---

## SECTION N: LEGAL TECHNICALITIES & GROUNDS FOR APPEAL

### N1: Appellable Defects (Why Cases Get Reversed)
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **appellable_defect_1** | enum | First ground for appeal | ["illegal_arrest", "chain_of_custody_broken", "unreliable_witness"] |
| **appellable_defect_details_1** | string | Specific issue | "Police custody extended 2 weeks beyond CrPC 167 limit" |
| **appellable_defect_2** | enum | Second ground | ["section_164_statement_police_present"] |
| **appellable_defect_3** | enum | Third ground | ["expert_opinion_unreliable"] |
| **appellable_defect_4** | enum | Fourth ground | ["procedural_non_compliance"] |
| **defect_fatal_to_conviction** | boolean | Does single defect overturn conviction | false |
| **defects_cumulatively_fatal** | boolean | Do multiple defects together overturn | true |

### N2: Witness-Related Appeal Grounds
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **witness_identification_procedure_defect** | boolean | Improperly conducted | true |
| **witness_identification_parade_suggestive** | boolean | Line-up unfair | true |
| **witness_cross_examination_denied** | boolean | Fundamental right violation | false |
| **witness_hostile_not_declared** | boolean | Should have been declared hostile | true |
| **witness_examined_multiple_times_inconsistency** | boolean | Prior statement contradicts trial testimony | true |
| **eyewitness_sole_evidence** | boolean | Only witness, single point failure | false |
| **eyewitness_reliability_tested** | boolean | Proper cross-examination done | true |

### N3: Evidence-Related Appeal Grounds
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **evidence_illegally_obtained_ground** | boolean | Fruit of poisonous tree | false |
| **evidence_chain_of_custody_broken_ground** | boolean | Tampered with evidence | true |
| **evidence_no_corroboration_circumstantial** | boolean | Weak circumstantial chain | false |
| **evidence_conflicting_expert_opinions_ground** | boolean | Experts disagreed | true |
| **evidence_medical_report_not_examined_ground** | boolean | Doctor didn't testify | true |
| **evidence_forensic_report_reliability_ground** | boolean | Lab standards questioned | false |
| **evidence_search_warrant_absent_ground** | boolean | Unlawful search | false |

### N4: Conviction Legality Grounds
| Field Name | Data Type | Why It Matters | Example Values |
|---|---|---|---|
| **burden_of_proof_shifted_ground** | boolean | Accused had to prove innocence (illegal) | false |
| **presumption_of_innocence_violated_ground** | boolean | Court presumed guilt | false |
| **reasonable_doubt_not_applied_ground** | boolean | Court ignored doubt | true |
| **conviction_purely_circumstantial_no_link_ground** | boolean | Chain of circumstantial evidence incomplete | false |
| **guilty_plea_involuntary_ground** | boolean | Plea was coerced | false |

---

## SECTION O: SEARCH FILTER COMBINATIONS (For AI Queries)

### O1: Defense Lawyer Searches
**Example Filter Combinations for Building Defense Strategy:**

1. **"Find all murder cases with weak eyewitness evidence + procedural defects + successful defenses"**
   - Filters: `offense_type = murder`, `eyewitness_count < 2`, `appellable_defects > 2`, `judgment_type = acquittal`

2. **"Murder cases where chain of custody was broken but conviction still upheld"**
   - Filters: `custody_chain_complete = false`, `judgment_type = conviction`, `appeal_filed = true`, `court_level = high_court`

3. **"Find all cases with successful alibi defenses in Lahore High Court"**
   - Filters: `defense_strategy = alibi`, `alibi_corroboration = strong`, `judgment_type = acquittal`, `court_name = Lahore High Court`

4. **"Sexual assault cases with successful victim-credibility attack by defense"**
   - Filters: `offense_type = rape`, `victim_character_attacked = true`, `judgment_type = acquittal`, `court_level = high_court`

5. **"Cases with wrongful conviction due to IO incompetence"**
   - Filters: `io_competency_concerns` populated, `appeal_verdict = conviction_quashed`, `sentencing_range = justice_denied`

### O2: Prosecutor Searches
**Example Filter Combinations for Building Prosecution Case:**

1. **"Successful murder convictions based on circumstantial evidence only"**
   - Filters: `evidence_type = circumstantial_only`, `conviction_strength = strong`, `appeal_verdict = conviction_upheld`, `sentencing_range = 10_plus_years`

2. **"Murder with premeditation + motive + opportunity cases"**
   - Filters: `murder_category = qatal_i_amd`, `motive_proven = true`, `opportunity_proven = true`, `premeditation_evident = true`, `judgment_type = conviction`

3. **"Drug trafficking cases with successful conviction using forensic evidence"**
   - Filters: `special_law = cnsa`, `forensic_evidence_type = drug_analysis`, `conviction_strength = strong`, `sentences_imposed = 5_plus`

4. **"Terrorism convictions with financing evidence + organization link"**
   - Filters: `ata_financing_alleged = true`, `ata_organization_connection = true`, `conviction_strength = strong`

### O3: Judge/Court Searches
**Example Filter Combinations for Sentencing Guidance:**

1. **"Murder convictions with aggravating circumstances only - no mitigating factors"**
   - Filters: `murder_category = qatal_i_amd`, `aggravating_factors` > 3, `mitigating_factors` = none, `judgment_type = conviction`

2. **"Precedent for honor crime sentencing in murder cases"**
   - Filters: `honor_crime_defense = true`, `offense_type = murder`, `judgment_type = conviction`, `province = punjab`, `date_judgment > 2015`

3. **"Sentencing comparisons for rape cases with life imprisonment"**
   - Filters: `offense_type = rape`, `sentence_imposed = life_imprisonment`, `court_level = trial_court`, `appeal_verdict = sentence_upheld`

4. **"First offenders convicted of serious crimes - sentencing precedents"**
   - Filters: `first_offense = true`, `severity_level = serious`, `judgment_type = conviction`, `sentence_imposed > 5_years`

---

## SECTION P: CRITICAL NOTES FOR AI IMPLEMENTATION

### Data Quality Considerations:
1. **Source Reliability**: Judgment text from official court databases (SHC, IHC, LHC) vs. newspaper reports
2. **Extraction Accuracy**: OCR on scanned judgments introduces errors - verify critical datapoints
3. **Missing Data**: Many older judgments lack key datapoints (expert qualification, witness examination dates)
4. **Interpretation Required**: Some judgments use ambiguous language on key facts

### Sensitivity Areas:
1. **Sexual Offenses**: Victim privacy (section 166 CrPC)
2. **Juveniles**: Age determination can be disputed - verify sources
3. **Witness Identity**: Sometimes concealed in judgment for safety
4. **Financial Amounts**: Diyat (blood money) amounts vary by custom/sect

### For Case Relevance Matching:
1. **Temporal Clustering**: Recent cases (past 5 years) more useful for current jurisprudence
2. **Court Hierarchy**: Supreme Court precedents weighted higher than trial court
3. **Fact Similarity**: Match on **combination** of facts, not single element
4. **Procedural vs. Substantive**: Filter separately - procedural defects may not affect precedent value for guilt analysis

---

## SOURCES

Research synthesized from:
- [Pakistan Penal Code - Wikipedia](https://en.wikipedia.org/wiki/Pakistan_Penal_Code)
- [Pakistan Penal Code - Government Source](http://nasirlawsite.com/laws/ppc.htm)
- [Pakistan Code Government](https://pakistancode.gov.pk/english/)
- [Code of Criminal Procedure 1898](https://fmu.gov.pk/docs/laws/Code_of_criminal_procedure_1898.pdf)
- [Qanun-e-Shahadat Order 1984](http://nasirlawsite.com/laws/evidence.htm)
- [Anti-Terrorism Act 1997](https://sindhlaws.gov.pk/setup/Library/LIB-18-000002.pdf)
- [Control of Narcotic Substances Act 1997](https://na.gov.pk/uploads/documents/Control-Narcotic-Substances-Act-XXV.pdf)
- [Juvenile Justice System Act 2018](https://lpr.adb.org/sites/default/files/2024-07/pakistan-juvenile-justice-system-act-2018.pdf)
- [Guidelines on Writing Judgments - Punjab Judicial Academy](https://pja.gov.pk/system/files/hbgjwj.pdf)
- [Handbook on Murder Trial - Punjab Judicial Academy](https://pja.gov.pk/system/files/hbmtss.hpdf)
- [Bail and Bonds - Prosecutor General Punjab](https://pg.punjab.gov.pk/)
- [Pakistan Capital Punishment Study - Reprieve](https://reprieve.org/wp-content/uploads/sites/2/2019/04/Pakistan-Capital-Punishment-Study.pdf)
- [Scope of Circumstantial Evidence in Pakistan - Law and Policy Review](https://journals.umt.edu.pk/index.php/lpr/article/view/5251)
- [Challenges for Expert Evidence - Journal of Forensic Science and Medicine](https://journals.lww.com/jfsm/fulltext/2022/08020/challenges_for_expert_evidence_in_the_justice.5.aspx)
- Supreme Court Case Law precedents cited throughout
