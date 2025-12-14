# src/config.py
CRIME_TYPES = {
    "1": "Homicide", "2": "Assault", "3": "Robbery", "4": "Burglary", "5": "Theft",
    "6": "Fraud", "7": "Drug Possession", "8": "Domestic Violence", "9": "Stalking",
    "10": "Arson", "11": "Cybercrime", "12": "Phone Scam"
}

COMPLEXITY_LEVELS = ["Low", "Medium", "High"]
SUBJECT_STATUS_OPTIONS = ["Known", "Unknown", "Partially Known"]

# Subject identification clarity for unknown cases
SUBJECT_CLARITY_OPTIONS = {
    "Embedded": "Solution is embedded in case data (traditional approach)",
    "Investigative": "Create list of possible subjects for further investigation (realistic scenarios)"
}

INVESTIGATIVE_MODIFIERS = {
    "1": ("Phone data pull", "Extract phone records, texts, and call logs"),
    "2": ("IP logs", "Network traffic analysis and IP address tracking"),
    "3": ("DNS records", "Domain name resolution and internet history"),
    "4": ("Body Cam", "Officer body camera footage and transcripts"),
    "5": ("Email Dump", "Email account contents and metadata"),
    "6": ("Financial Records", "Bank statements and transaction analysis"),
    "7": ("Data-Heavy Phone Dump", "MASSIVE phone extraction with thousands of records"),
    "8": ("Data-Heavy IP Logs", "MASSIVE network logs with 10K+ entries"),
    "9": ("Data-Heavy Financial", "MASSIVE financial records with years of transactions"),
    "10": ("Extra Junk Data", "Generate extensive irrelevant documents for filtering challenge"),
    "11": ("Random Events", "Add unpredictable events like car wrecks"),
    "12": ("ALPR", "Automated License Plate Reader hits")
}

TREND_TYPES = {
    "1": "Serial Offender", "2": "Organized Crime", "3": "Crime Ring",
    "4": "Victim Pattern", "5": "Location Pattern", "6": "Mixed"
}

AI_MODELS = {
    "anthropic": "Anthropic Claude",
    "openai": "OpenAI GPT",
    "gemini": "Google Gemini",
    "xai": "xAI Grok",
    "local": "Local Model (Ollama)"
}
