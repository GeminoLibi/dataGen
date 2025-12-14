# Implementation Plan: Consistency Fixes

## Overview

This document outlines the step-by-step implementation plan to fix the critical consistency issues identified in the evaluation analysis.

## Phase 1: Create Consistency Manager Classes

### 1.1 Create `src/consistency_managers.py`

**Purpose**: Centralized classes to maintain consistency across document generation.

**Classes to Create**:

1. **JurisdictionManager**
   - Maintains: state, county, city, police department, court, judge
   - Methods: `get_jurisdiction()`, `get_department()`, `get_judge()`, `set_multi_jurisdictional()`

2. **OfficerRegistry**
   - Maintains: officer name → badge number, department mapping
   - Methods: `register_officer()`, `get_badge()`, `get_department()`, `get_officer()`

3. **EntityValidator**
   - Maintains: entity name → attributes (gender, age, description) mapping
   - Methods: `register_entity()`, `validate_consistency()`, `get_entity_attributes()`

4. **TimelineManager**
   - Maintains: base incident time, event sequence
   - Methods: `set_incident_time()`, `get_911_time()`, `get_response_time()`, `validate_sequence()`

5. **LocationManager**
   - Maintains: primary location, related locations, geographic consistency
   - Methods: `set_primary_location()`, `add_related_location()`, `validate_geographic_consistency()`

### 1.2 Integration Points

- Initialize all managers in `CaseGenerator.__init__()`
- Pass managers to document generation methods
- Use managers in `_generate_incident_report()`, `_create_search_warrant()`, etc.

---

## Phase 2: Fix Search Warrant Generation

### 2.1 Update `generate_search_warrant_affidavit()`

**Current Issue**: Uses random `fake.state()`, `fake.city()`, random badge numbers

**Fix**:
```python
def generate_search_warrant_affidavit(
    officer: Person, 
    target_address: str, 
    crime_type: str, 
    evidence_description: str,
    jurisdiction_manager: JurisdictionManager,  # NEW
    officer_registry: OfficerRegistry  # NEW
) -> str:
    # Use jurisdiction_manager.get_jurisdiction() instead of fake.state()
    # Use jurisdiction_manager.get_department() instead of fake.city() + " PD"
    # Use officer_registry.get_badge(officer.full_name) instead of random
    # Use officer_registry.get_department(officer.full_name) instead of random
```

### 2.2 Update `generate_search_warrant()`

**Same fixes as 2.1** - use consistency managers instead of random generation.

### 2.3 Update `_create_search_warrant()` in `CaseGenerator`

**Fix**: Pass consistency managers to warrant generation functions.

---

## Phase 3: Fix Officer Consistency

### 3.1 Register Officers Early

**In `CaseGenerator.generate_case()`**:
- Register `reporting_officer` immediately after creation
- Register any officers created during case generation
- Ensure all officers have consistent badge numbers and departments

### 3.2 Update All Document Generators

**Find all places that generate officer information**:
- CAD logs
- Incident reports
- Search warrants
- Evidence logs
- Warrant returns

**Fix**: Use `officer_registry.get_badge()` and `officer_registry.get_department()` instead of random generation.

---

## Phase 4: Fix Entity Identity Consistency

### 4.1 Register Entities Early

**In `CaseGenerator.generate_case()`**:
- Register all persons (victims, suspects, witnesses) with their attributes
- Store: name, gender, age, physical description, address

### 4.2 Validate Before Document Generation

**Before generating 911 transcript, CAD log, incident report**:
- Validate that victim/suspect names match registered entities
- Validate that descriptions match registered attributes
- If intentional errors (typos), ensure they're consistent

### 4.3 Fix 911/CAD Generation

**In `generate_911_script()` and `generate_cad_log()`**:
- Use registered victim information instead of random generation
- Match caller description to actual victim
- Align timestamps with timeline manager

---

## Phase 5: Fix Timeline Consistency

### 5.1 Establish Base Timeline

**In `CaseGenerator.generate_case()`**:
- Set incident time as base time
- Calculate 911 call time (should be after incident, with realistic delay)
- Calculate response time (should be after 911 call)
- Calculate warrant times (should be after response)

### 5.2 Update All Timestamp Generation

**In all document generators**:
- Use `timeline_manager.get_911_time()` instead of random
- Use `timeline_manager.get_response_time()` instead of random
- Validate that all timestamps follow logical sequence

### 5.3 Fix CCTV/ALPR Timestamps

**In `_generate_cctv_surveillance()` and `_generate_alpr_hits()`**:
- Ensure timestamps align with incident timeline
- If different time zone, add explanation
- Validate that surveillance times are relevant to incident

---

## Phase 6: Fix Location Consistency

### 6.1 Establish Primary Location

**In `CaseGenerator.generate_case()`**:
- Set incident location as primary location
- Store victim address, suspect address, search locations
- Validate geographic consistency

### 6.2 Update Location References

**In all document generators**:
- Use `location_manager.get_primary_location()` for incident location
- Use `location_manager.get_victim_address()` for victim references
- Validate that related locations are in same geographic area

### 6.3 Fix Weather Data

**In weather generation**:
- Use location from `location_manager` instead of random
- Ensure weather matches location and date
- Align weather across all documents

---

## Phase 7: Strengthen Crime-Type Filtering

### 7.1 Review All Evidence Generation

**Check all evidence generation methods**:
- `_generate_evidence_and_warrants()`
- `_generate_cctv_surveillance()`
- `_generate_iot_evidence()`
- `_generate_alpr_hits()`
- `_generate_vehicle_evidence()`

**Ensure**: All use `_should_generate_physical_evidence()` or crime-type specific checks.

### 7.2 Add Vehicle Evidence Check

**In vehicle evidence generation**:
- Check if crime type warrants vehicle evidence
- Phone scams shouldn't have EDR/infotainment unless vehicle is part of scam
- Only generate vehicle evidence for physical crimes or when vehicle is relevant

---

## Phase 8: Testing & Validation

### 8.1 Generate Test Cases

- Generate 20 cases across all crime types
- Vary complexity levels (Low, Medium, High)
- Include all modifiers

### 8.2 Run AI Evaluation

- Use `evaluate_case_ai.py` to evaluate all cases
- Target: Average consistency score > 8.5/10
- Zero critical inconsistencies

### 8.3 Manual Review

- Review sample cases for remaining issues
- Fix any edge cases
- Document any intentional inconsistencies

---

## File Changes Summary

### New Files
- `src/consistency_managers.py` - All consistency manager classes

### Modified Files
- `src/utils.py` - Update warrant generation functions
- `src/generators.py` - Integrate consistency managers, fix document generation
- `src/models.py` - Add consistency manager fields to Case (if needed)

### Testing Files
- `test_consistency.py` - Unit tests for consistency managers
- `test_case_generation.py` - Integration tests for full case generation

---

## Success Criteria

1. **Zero jurisdiction inconsistencies** across all test cases
2. **Zero officer badge/department inconsistencies** across all test cases
3. **Zero entity identity contradictions** across all test cases
4. **<5% timeline discrepancies** (minor only, with explanations)
5. **100% crime-type appropriate evidence** across all test cases
6. **Average consistency score > 8.5/10** in AI evaluations
7. **Average overall quality score > 8.5/10** in AI evaluations

---

## Timeline Estimate

- **Phase 1**: 2-3 hours (Create consistency managers)
- **Phase 2**: 1-2 hours (Fix warrant generation)
- **Phase 3**: 1-2 hours (Fix officer consistency)
- **Phase 4**: 2-3 hours (Fix entity consistency)
- **Phase 5**: 1-2 hours (Fix timeline consistency)
- **Phase 6**: 1-2 hours (Fix location consistency)
- **Phase 7**: 1-2 hours (Strengthen crime-type filtering)
- **Phase 8**: 2-3 hours (Testing & validation)

**Total**: 11-19 hours

---

## Next Steps

1. Review and approve this implementation plan
2. Create `src/consistency_managers.py` with all manager classes
3. Begin Phase 2 fixes (warrant generation)
4. Iterate through phases systematically
5. Test after each phase
6. Final validation with AI evaluation

