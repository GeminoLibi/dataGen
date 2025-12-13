# Changelog - Crime Type Specific Generation & AI Enhancement

## Major Updates

### 1. Crime-Type-Specific Document Generation
- **New Module**: `src/crime_specific_generators.py`
  - Generates documents based on the specific crime type
  - Phone scams now generate proper investigation flow:
    - Initial victim report (got called by X, said Y, did Z)
    - Phone records investigation (burner VoIP phone → other phones)
    - DNS/Website investigation (website → IPs → residential IP)
    - Follow-up investigation reports
  - Physical crimes (homicide, assault, burglary) generate appropriate physical evidence
  - Non-physical crimes (fraud, scams) skip inappropriate evidence (latents, footprints, etc.)

### 2. RPG Mechanics Based on Crime Type
- Generation now branches from crime type as the starting point
- Each crime type has its own investigation flow
- Evidence types are filtered based on crime type appropriateness

### 3. AI Model Integration
- **New Module**: `src/ai_enhancer.py`
  - Supports multiple AI providers:
    - Anthropic Claude
    - OpenAI GPT
    - Google Gemini
    - xAI Grok
    - Local models (Ollama)
  - Enhances procedural text to be more natural and less robotic
  - Maintains professionalism while improving realism

### 4. Web Interface Updates
- Added AI enhancement options in Flask interface
- Users can select AI provider and enter API keys
- Local model support with configurable base URL and model name
- AI enhancement is optional (defaults to procedural only)

## Technical Changes

### Generator Updates
- `_should_generate_physical_evidence()`: Determines if crime type needs physical evidence
- Crime-specific documents generated before generic ones
- Physical evidence (fingerprints, ballistics, etc.) only for appropriate crimes
- ALPR hits only for crimes with vehicles

### Integration Points
- Crime-specific generators integrated into main generation flow
- AI enhancer applied post-generation to all documents
- Graceful fallback if AI models unavailable

## Usage

### Crime Type Awareness
The system now automatically:
- Generates appropriate documents for each crime type
- Skips inappropriate evidence (e.g., no latents for phone scams)
- Creates investigation chains that make sense for the crime

### AI Enhancement
To use AI enhancement:
1. Select AI provider in web interface
2. Enter API key (or base URL for local models)
3. Generated documents will be enhanced for more natural language

## Notes
- AI packages are optional dependencies
- System works fully without AI (procedural only)
- AI enhancement can be slow for large documents
- Local models require Ollama or compatible server running

