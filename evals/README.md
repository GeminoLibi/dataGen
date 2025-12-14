# Evaluation Documents

This directory contains AI-generated evaluations of procedurally generated case documents.

## Files

- **Original .docx files**: Evaluation documents in Word format
- **Converted .txt files**: Text versions for easier analysis and processing

## Conversion

To convert .docx files to .txt, run:

```bash
cd evals
python convert_docx_to_txt.py
```

The script will:
- Automatically install `python-docx` if needed
- Convert all .docx files in this directory to .txt
- Skip files that have already been converted

## Evaluation Format

These evaluations follow the criteria defined in `AI_EVALUATION_PROMPT.md` and assess:

- Internal consistency (entities, timelines, locations)
- Crime-type appropriateness
- Realism and authenticity
- Narrative coherence
- Technical accuracy
- Investigation quality
- Hidden gems and subtle clues
- Complexity appropriateness
- Entity error system evaluation
- Data volume and junk data quality

Each evaluation includes:
- Strengths identified
- Issues found (with severity and location)
- Scoring across multiple dimensions
- Specific recommendations

## Usage

These evaluations can be used to:
- Identify patterns in generator issues
- Improve the case generation system
- Benchmark generator quality
- Train evaluation models

