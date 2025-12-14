# MOD-IN Case Analysis Module

## Overview

The MOD-IN (Modification/Input) case analysis module automatically generates comprehensive case analysis reports for each generated case. These reports follow law enforcement documentation standards and provide a complete investigative summary.

## Features

### Required Sections (All Included)

1. **Overview**
   - Case number
   - Detective name and badge number
   - Date of analysis
   - Case metadata (crime type, complexity, status, dates)

2. **Executive Summary**
   - First-person, past-tense narrative
   - Summary of investigative actions taken
   - Evidence reviewed/collected
   - Key findings
   - Written in factual, concise style

3. **Case Overview**
   - Full narrative from incident report
   - Crime details (type, location, dates, weather)
   - Investigation modifiers
   - Initial responding officer information

4. **Subjects of Investigation**
   - **Suspects**: Complete profiles with age, address, phone, email, motive, criminal history, aliases, vehicles, devices
   - **Victims**: Complete profiles with contact information
   - **Witnesses**: Profiles with reliability scores

5. **Attachments and Physical Evidence**
   - Evidence items grouped by type (Physical, Digital, Forensic, Ballistic, etc.)
   - Chain of custody information
   - Metadata for each evidence item
   - Document attachments categorized by type

6. **Timeline**
   - Chronological sequence of key events
   - Incident time
   - 911 call time
   - Officer response time
   - Evidence collection times
   - Search warrant execution times
   - All times with source attribution

7. **Investigative Activities Summary**
   - Document review summary (categorized by type)
   - Evidence collection summary
   - Subject identification
   - Follow-up actions taken
   - Written in first-person, past-tense

8. **Recommended Next Steps**
   - Subject interviews recommended
   - Victim follow-up actions
   - Forensic analysis recommendations
   - Digital forensics next steps
   - Financial investigation recommendations
   - Surveillance review recommendations
   - Case coordination actions

9. **Working Theory**
   - Current working theory of the case
   - Primary subject identification
   - Motive analysis
   - Evidence supporting theory
   - Method of operation
   - Confidence level (High/Moderate/Low)
   - Alternative theories considered

## Additional Features

### Trend Analysis

The module includes a `TrendAnalyzer` class that can analyze multiple cases to identify:

- **Shared Subjects**: Same suspects appearing in multiple cases
- **Shared Locations**: Same locations involved in multiple cases
- **Shared Vehicles**: Same license plates across cases
- **Shared Phone Numbers**: Same phone numbers across cases
- **Shared Emails**: Same email addresses across cases
- **Similar Crime Types**: Patterns in crime types

### Automatic Generation

MOD-IN documents are automatically generated when cases are exported via `CaseExporter.export()`. The document is saved as `MOD-IN_CASE_ANALYSIS.md` in the case directory.

## Usage

### Single Case Analysis

```python
from src.case_analyzer import generate_mod_in_for_case
from src.generators import CaseGenerator

# Generate a case
generator = CaseGenerator()
case = generator.generate_case("Assault", "High", ["Phone data pull"])

# Generate MOD-IN
mod_in = generate_mod_in_for_case(
    case, 
    detective_name="Detective Sarah Martinez",
    badge_number=4827
)

# Save to file
with open("MOD-IN_CASE_ANALYSIS.md", "w", encoding="utf-8") as f:
    f.write(mod_in)
```

### Trend Analysis Across Cases

```python
from src.case_analyzer import generate_trend_analysis
from src.generators import CaseGenerator

# Generate multiple cases
generator = CaseGenerator()
cases = [
    generator.generate_case("Assault", "High", []),
    generator.generate_case("Burglary", "Medium", []),
    generator.generate_case("Robbery", "High", [])
]

# Generate trend analysis
trend_report = generate_trend_analysis(cases)

# Save to file
with open("TREND_ANALYSIS.md", "w", encoding="utf-8") as f:
    f.write(trend_report)
```

## Document Format

The MOD-IN document follows law enforcement documentation standards:

- **First-person, past-tense** ("I conducted...", "I collected...")
- **Factual and concise** - avoids speculation
- **Source attribution** - references specific documents and files
- **Clear structure** - organized sections with headers
- **Professional tone** - appropriate for law enforcement use

## Integration

The MOD-IN generator is integrated into the case export process. Every case exported via `CaseExporter` automatically includes a `MOD-IN_CASE_ANALYSIS.md` file.

## File Location

MOD-IN documents are saved in the case directory:
```
cases/
  CASE-XXXXXX/
    MOD-IN_CASE_ANALYSIS.md  ← Generated automatically
    CASE_BRIEFING.md
    documents/
      ...
```

## Example Output

See `test_mod_in_cases/CASE-471610/MOD-IN_CASE_ANALYSIS.md` for a complete example of a generated MOD-IN document.

