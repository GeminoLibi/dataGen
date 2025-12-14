#!/usr/bin/env python3
"""Test HIGH complexity FRAUD case generation with AI enhancement"""
import sys
from src.generators import CaseGenerator
from src.exporter import CaseExporter
from src.ai_enhancer import AIEnhancer, debug_print

print("=" * 70)
print("Testing HIGH Complexity FRAUD Case Generation")
print("=" * 70)
print()

# Appropriate modifiers for FRAUD case
modifiers = [
    "Phone data pull",
    "IP logs", 
    "DNS records",
    "Email Dump",
    "Financial Records",
    "Data-Heavy Phone Dump",
    "Data-Heavy IP Logs",
    "Data-Heavy Financial",
    "Extra Junk Data"
]

print(f"Crime Type: Fraud")
print(f"Complexity: High")
print(f"Modifiers: {len(modifiers)}")
for mod in modifiers:
    print(f"  - {mod}")
print()

# Initialize AI enhancer with Gemini
print("Initializing AI Enhancer (Gemini)...")
# API key should be set via environment variable or input
api_key = os.environ.get('GEMINI_API_KEY', '')
if not api_key:
    print("ERROR: GEMINI_API_KEY environment variable not set")
    sys.exit(1)
ai_enhancer = AIEnhancer(model_type='gemini', api_key=api_key)
print("[OK] AI Enhancer ready")
print()

# Generate case
print("Generating case...")
print("(This will take a while with AI enhancement)")
print()

generator = CaseGenerator()
case = generator.generate_case(
    crime_type="Fraud",
    complexity="High",
    modifiers=modifiers,
    subject_status="Known"
)

if not case:
    print("ERROR: Case generation returned None")
    sys.exit(1)

print(f"[OK] Case generated: {case.id}")
print(f"  - Documents: {len(case.documents)}")
print(f"  - Evidence: {len(case.evidence)}")
print(f"  - Persons: {len(case.persons)}")
print()

# Enhance with AI
print("Enhancing documents with AI...")
print("(This will take several minutes - watch for [AI_DEBUG] messages)")
print()

enhanced_count = 0
for i, doc in enumerate(case.documents, 1):
    print(f"Enhancing document {i}/{len(case.documents)}...", end=" ", flush=True)
    try:
        enhanced = ai_enhancer.enhance_document(doc, "Fraud", "report")
        case.documents[i-1] = enhanced
        enhanced_count += 1
        print("[OK]")
    except Exception as e:
        print(f"[ERROR] {e}")

print()
print(f"[OK] Enhanced {enhanced_count}/{len(case.documents)} documents")
print()

# Export
print("Exporting case...")
case_path = CaseExporter.export(case)
print(f"[OK] Case exported to: {case_path}")
print()

print("=" * 70)
print("Test Complete!")
print("=" * 70)

