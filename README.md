# Law Enforcement Case Data Generator

A procedural generator for creating realistic, comprehensive law enforcement case data. This tool generates cohesive case briefings with incident reports, evidence artifacts, witness statements, and investigative documents suitable for AI training and analysis.

## Features

- **Crime-Type-Specific Generation**: Each crime type generates appropriate documents and evidence
  - Physical crimes (Homicide, Assault, Burglary) include physical evidence (fingerprints, DNA, ballistics)
  - Non-physical crimes (Fraud, Phone Scam, Cybercrime) focus on digital/paper trails
  - Proper investigation flows (e.g., Phone Scam: Initial Report → Phone Records → DNS/IP → Follow-up)

- **Multiple Complexity Levels**: Low, Medium, High
- **Subject Status Options**: Known, Unknown, Partially Known suspects
- **Evidence Modifiers**: 
  - Phone data pull
  - IP logs
  - DNS records
  - ALPR (Automated License Plate Reader)
  - Email dump
  - Body cam
  - Financial records
  - Data-Heavy Phone Dump
  - Data-Heavy IP Logs
  - Data-Heavy Financial
  - Extra Junk Data
  - Random Events

- **Trend Generation**: Create multiple related cases with shared entities
  - Serial Offender
  - Organized Crime
  - Crime Ring
  - Victim Pattern
  - Location Pattern
  - Mixed

- **AI Enhancement** (Optional): Enhance procedural text with AI models
  - Anthropic Claude
  - OpenAI GPT
  - Google Gemini
  - xAI Grok
  - Local models (Ollama)

- **Entity-Based Error System**: Realistic errors based on entity profiles (officers, systems, AI)
- **Hidden Gems**: Subtle clues injected into junk data for AI discovery
- **RPG Mechanics**: Probabilistic outcomes and character-driven narratives

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/GeminoLibi/dataGen.git
cd dataGen
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Optional: AI Enhancement Dependencies

If you want to use AI enhancement, install the appropriate package:

```bash
# Anthropic
pip install anthropic

# OpenAI
pip install openai

# Google Gemini
pip install google-generativeai

# xAI
pip install xai

# Local models (Ollama)
pip install requests
```

## Usage

### Command Line Interface

```bash
python main.py
```

The CLI will guide you through:
1. Selecting crime type
2. Choosing complexity level
3. Selecting modifiers
4. Setting subject status
5. Optionally generating a trend of related cases

### Web Interface

```bash
python web_interface.py
```

Then open your browser to `http://localhost:5000`

The web interface provides:
- All CLI options in a user-friendly form
- AI enhancement configuration
- Trend generation options

### Building Standalone Executable

#### Windows
```bash
build.bat
```

#### Linux/Mac
```bash
chmod +x build.sh
./build.sh
```

The executable will be in the `dist/` directory.

## Project Structure

```
dataGen/
├── src/
│   ├── __init__.py
│   ├── models.py          # Data models (Case, Person, Evidence, etc.)
│   ├── generators.py      # Core case generation logic
│   ├── utils.py           # Utility functions and helpers
│   ├── exporter.py        # Case export functionality
│   ├── crime_specific_generators.py  # Crime-type-specific generators
│   ├── ai_enhancer.py     # AI model integration
│   └── trend_generator.py # Trend generation logic
├── main.py                # CLI entry point
├── web_interface.py       # Flask web interface
├── requirements.txt       # Python dependencies
├── build_executable.spec  # PyInstaller configuration
├── build.bat              # Windows build script
├── build.sh               # Linux/Mac build script
└── README.md              # This file
```

## Generated Case Structure

Each generated case includes:

- **CASE_BRIEFING.md**: Summary of the case with involved persons and evidence
- **documents/**: Individual artifact files
  - Incident reports
  - Witness statements
  - Evidence collection logs
  - Search warrants
  - Phone records
  - IP logs
  - Financial records
  - And many more...

## Crime Types Supported

- Homicide
- Assault
- Robbery
- Burglary
- Theft
- Fraud
- Drug Possession
- Domestic Violence
- Stalking
- Arson
- Cybercrime
- Phone Scam

## Examples

### Generate a Phone Scam Case

```bash
python main.py
# Select: Phone Scam
# Complexity: Medium
# Modifiers: Phone data pull, IP logs, DNS records
# Subject Status: Unknown
```

This will generate:
- Initial victim report
- Phone records investigation
- DNS/IP investigation
- Follow-up investigation report
- And more...

### Generate a Homicide Case

```bash
python main.py
# Select: Homicide
# Complexity: High
# Modifiers: Phone data pull, Body Cam, Financial Records
# Subject Status: Known
```

This will generate:
- 911 dispatch transcript
- Incident report with physical evidence
- Witness statements
- Ballistics reports
- Autopsy reports
- And more...

## Configuration

### AI Enhancement

To use AI enhancement, configure in the web interface or modify `web_interface.py`:

1. Select AI provider
2. Enter API key (or base URL for local models)
3. Generated documents will be enhanced for more natural language

### Entity Profiles

Entity profiles control error rates and document quality. These are automatically generated but can be customized in `src/generators.py`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is for training and educational purposes only. Generated data is fictional and should not be used for actual law enforcement purposes.

## AI Evaluation

The project includes an AI evaluation system for analyzing generated cases. See `AI_EVALUATION_PROMPT.md` for the evaluation criteria and `evaluate_case_ai.py` for the evaluation tool.

### Quick Evaluation

```bash
# Generate evaluation prompt (for manual use with any AI)
python evaluate_case_ai.py cases/CASE-XXXXX

# Use with OpenAI
python evaluate_case_ai.py cases/CASE-XXXXX --ai openai --api-key YOUR_KEY

# Use with Anthropic Claude
python evaluate_case_ai.py cases/CASE-XXXXX --ai anthropic --api-key YOUR_KEY
```

The evaluation assesses:
- Internal consistency (entities, timelines, locations)
- Crime-type appropriateness
- Realism and authenticity
- Narrative coherence
- Technical accuracy
- Investigation quality
- Hidden gems and subtle clues

## Support

For issues, questions, or contributions, please open an issue on GitHub.

