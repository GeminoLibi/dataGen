#!/usr/bin/env python3
"""
AI-powered case evaluation tool.
Uses the evaluation prompt to analyze generated cases.
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

EVALUATION_PROMPT = """You are an expert forensic analyst and law enforcement case reviewer tasked with evaluating procedurally generated case documents. Your role is to assess the quality, consistency, realism, and investigative coherence of these documents as if they were real case files.

## Your Evaluation Criteria

### 1. Internal Consistency
- **Entity Consistency**: Do names, phone numbers, addresses, IP addresses, vehicle information, and other identifiers remain consistent across all documents?
- **Timeline Consistency**: Do dates, times, and chronological sequences make logical sense? Are there temporal contradictions?
- **Location Consistency**: Do geographic coordinates, addresses, and location references align across documents?
- **Evidence Chain**: Does the evidence collection, chain of custody, and processing follow a logical sequence?
- **Personnel Consistency**: Do officer names, badge numbers, and roles remain consistent? Do entity error patterns (typos, misspellings) remain consistent for the same person?

### 2. Crime-Type Appropriateness
- **Evidence Relevance**: Are the types of evidence appropriate for the crime type?
  - Physical crimes (Homicide, Assault, Burglary) should have physical evidence (fingerprints, DNA, ballistics, etc.)
  - Non-physical crimes (Fraud, Phone Scam, Cybercrime) should focus on digital/paper trails, NOT physical evidence
- **Investigation Flow**: Does the investigation follow a logical path appropriate for the crime type?
  - Phone scams: Initial report → Phone records → DNS/IP investigation → Follow-up
  - Homicide: Scene investigation → Autopsy → Ballistics → DNA → Witness interviews
  - Cybercrime: Network logs → IP tracking → Malware analysis → Attribution
- **Document Types**: Are the document types appropriate? (e.g., no latent fingerprints for phone scams, no phone records investigation for simple theft)

### 3. Realism and Authenticity
- **Document Structure**: Do documents follow realistic formats for law enforcement documents?
- **Language and Tone**: Is the language appropriate for the document type and author (officer, system, AI)?
- **Error Patterns**: Are errors (typos, misspellings, data corruption) consistent with the entity generating them?
- **Investigation Depth**: Is the level of detail appropriate for the complexity level?
- **Professional Jargon**: Is law enforcement terminology used correctly?
- **Legal Formatting**: Do legal documents (warrants, affidavits) follow proper legal structure?

### 4. Narrative Coherence
- **Story Arc**: Does the case tell a coherent story from initial report through investigation?
- **Motivation Alignment**: Do suspect motivations align with crime methods and evidence?
- **Relationship Logic**: Do relationships between suspects, victims, and witnesses make sense?
- **Crime Method Consistency**: Is the method of operation consistent across documents?
- **Alibi Logic**: Do alibis make sense, and are there logical alibi breakers?

### 5. Technical Accuracy
- **Digital Forensics**: Are IP addresses, MAC addresses, phone numbers, and other technical identifiers in correct formats?
- **Geographic Data**: Are coordinates, addresses, and location data realistic and consistent?
- **Financial Records**: Do transaction patterns, account numbers, and financial data follow realistic formats?
- **Timestamps**: Are timestamps in consistent formats and logically sequenced?
- **Hash Values**: Are file hashes in correct formats (MD5, SHA256)?

### 6. Investigation Quality
- **Lead Development**: Do investigative leads develop logically from evidence?
- **Follow-up Actions**: Are follow-up actions appropriate given the evidence collected?
- **Warrant Justification**: Do search warrants have appropriate probable cause?
- **Evidence Collection**: Is evidence collection method appropriate for the evidence type?
- **Cross-References**: Do documents appropriately reference other documents in the case?

### 7. Hidden Gems and Subtle Clues
- **Needle in Haystack**: Are there subtle clues embedded in junk data that require analysis to discover?
- **Pattern Recognition**: Are there patterns across documents that would require AI/analytical tools to identify?
- **Technical Indicators**: Are there technical connections (IP addresses, phone numbers, accounts) that link entities?
- **Temporal Patterns**: Are there time-based patterns that reveal connections?
- **Cross-Document Consistency**: Do subtle details (like a phone number in an unrelated document) create connections?

### 8. Complexity Appropriateness
- **Low Complexity**: Should have basic documents, minimal evidence, straightforward narrative
- **Medium Complexity**: Should have moderate detail, some conflicting information, multiple evidence types
- **High Complexity**: Should have extensive detail, conflicting narratives, hidden connections, large data dumps, sophisticated investigation

### 9. Entity Error System Evaluation
- **Consistency**: Do the same entities (officers, systems) show consistent error patterns?
- **Realism**: Are errors realistic for the entity type?
  - Human errors: typos, misspellings, omissions, bias
  - Automated errors: data corruption, missing fields, accessibility issues
  - AI errors: incomplete data, formatting issues
- **Appropriate Frequency**: Are error rates appropriate (not too many, not too few)?

### 10. Data Volume and Junk Data
- **Appropriate Volume**: Does the data volume match the complexity and modifiers?
- **Junk Data Quality**: Is junk data realistic and not obviously labeled as "unrelated"?
- **Signal-to-Noise**: Is there an appropriate balance between relevant and irrelevant data?
- **Hidden Clues**: Are relevant clues appropriately hidden in junk data?

## Evaluation Process

1. **Initial Scan**: Read through all documents to understand the case structure
2. **Entity Mapping**: Create a map of all entities (persons, vehicles, devices, accounts, locations)
3. **Timeline Construction**: Build a chronological timeline of events
4. **Evidence Chain Review**: Trace evidence from collection through processing
5. **Cross-Reference Check**: Verify all cross-references between documents
6. **Crime-Type Validation**: Verify evidence and investigation flow matches crime type
7. **Consistency Audit**: Check for contradictions and inconsistencies
8. **Realism Assessment**: Evaluate authenticity and professional quality
9. **Hidden Pattern Analysis**: Look for subtle connections and patterns
10. **Final Scoring**: Provide overall quality score and specific recommendations

## Output Format

Provide your evaluation in the following format:

### Case ID: [Case ID]
### Crime Type: [Type]
### Complexity: [Level]

#### Strengths
- [List specific strengths with examples]

#### Issues Found
- [List specific issues with document references]
  - **Severity**: Critical / Major / Minor
  - **Type**: Consistency / Realism / Appropriateness / Technical
  - **Location**: [Document name and section]

#### Consistency Score: X/10
- Entity consistency: X/10
- Timeline consistency: X/10
- Location consistency: X/10
- Evidence chain: X/10

#### Realism Score: X/10
- Document structure: X/10
- Language/tone: X/10
- Error patterns: X/10
- Professional quality: X/10

#### Crime-Type Appropriateness: X/10
- Evidence relevance: X/10
- Investigation flow: X/10
- Document types: X/10

#### Investigation Quality: X/10
- Lead development: X/10
- Follow-up actions: X/10
- Warrant justification: X/10

#### Hidden Gems/Patterns: X/10
- Subtle clues present: Yes/No
- Pattern complexity: X/10
- Discoverability: X/10

#### Overall Quality Score: X/10

### Recommendations
- [Specific, actionable recommendations for improvement]

## Important Notes

- These documents are **procedurally generated** - evaluate them as if they were real, but understand they are training data
- Focus on **internal consistency** - the documents should be consistent with themselves
- **Realism over perfection** - some errors and inconsistencies are expected and realistic
- **Crime-type awareness** is critical - evaluate whether evidence types match the crime
- **Hidden patterns** should be discoverable but not obvious
- Consider that these are meant to be **challenging for AI analysis** - they should require pattern recognition and cross-document analysis

## Red Flags to Identify

- Physical evidence in non-physical crimes (fingerprints in phone scams)
- Missing appropriate evidence for crime type (no phone records in phone scam)
- Contradictory information without explanation
- Entities that change characteristics inconsistently
- Timeline impossibilities
- Evidence that appears without proper chain of custody
- Documents that are obviously "fake" or "unrelated" (should be subtle)
- Investigation flow that doesn't match crime type
- Missing investigation steps that should be present
- Overly perfect documents (unrealistic for human-generated content)

## Evaluation Philosophy

Remember: The goal is not perfection, but **realistic, internally consistent, procedurally generated case data** that:
1. Challenges AI to find patterns and connections
2. Requires cross-document analysis
3. Contains appropriate evidence for the crime type
4. Follows realistic investigation flows
5. Includes realistic errors and inconsistencies
6. Has hidden gems that require analytical discovery

Evaluate accordingly.
"""

def load_case_documents(case_dir: Path) -> dict:
    """Load all documents from a case directory."""
    case_data = {
        'briefing': None,
        'documents': []
    }
    
    # Load briefing
    briefing_path = case_dir / "CASE_BRIEFING.md"
    if briefing_path.exists():
        case_data['briefing'] = briefing_path.read_text(encoding='utf-8')
    
    # Load all documents
    docs_dir = case_dir / "documents"
    if docs_dir.exists():
        for doc_file in sorted(docs_dir.glob("*.txt")):
            case_data['documents'].append({
                'name': doc_file.name,
                'content': doc_file.read_text(encoding='utf-8')
            })
    
    return case_data

def prepare_evaluation_prompt(case_data: dict, case_id: str) -> str:
    """Prepare the full evaluation prompt with case data."""
    prompt = EVALUATION_PROMPT
    prompt += "\n\n" + "="*80 + "\n"
    prompt += "CASE TO EVALUATE\n"
    prompt += "="*80 + "\n\n"
    
    prompt += f"## Case Briefing\n\n{case_data['briefing']}\n\n" if case_data['briefing'] else ""
    
    prompt += "## Documents\n\n"
    for i, doc in enumerate(case_data['documents'], 1):
        prompt += f"### Document {i}: {doc['name']}\n\n"
        prompt += f"```\n{doc['content'][:2000]}\n```\n\n"  # First 2000 chars
        if len(doc['content']) > 2000:
            prompt += f"[... {len(doc['content']) - 2000} more characters ...]\n\n"
    
    prompt += "\n" + "="*80 + "\n"
    prompt += "END OF CASE DATA\n"
    prompt += "="*80 + "\n\n"
    prompt += "Please provide your evaluation using the format specified above.\n"
    
    return prompt

def evaluate_case_with_ai(case_dir: Path, ai_provider: str = "openai", api_key: str = None):
    """Evaluate a case using AI."""
    case_id = case_dir.name
    case_data = load_case_documents(case_dir)
    
    if not case_data['documents']:
        console.print(f"[red]No documents found in {case_dir}[/red]")
        return
    
    console.print(f"[cyan]Loading case: {case_id}[/cyan]")
    console.print(f"[cyan]Found {len(case_data['documents'])} documents[/cyan]")
    
    prompt = prepare_evaluation_prompt(case_data, case_id)
    
    # Save prompt for manual use
    prompt_file = case_dir / "AI_EVALUATION_PROMPT.txt"
    prompt_file.write_text(prompt, encoding='utf-8')
    console.print(f"[green]Evaluation prompt saved to: {prompt_file}[/green]")
    
    # If AI provider is specified, use it
    if ai_provider and api_key:
        try:
            if ai_provider.lower() == "openai":
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert forensic analyst and law enforcement case reviewer."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=4000
                )
                evaluation = response.choices[0].message.content
                
                # Save evaluation
                eval_file = case_dir / "AI_EVALUATION_RESULT.md"
                eval_file.write_text(evaluation, encoding='utf-8')
                console.print(f"[green]Evaluation saved to: {eval_file}[/green]")
                
                # Display evaluation
                console.print(Panel(Markdown(evaluation), title=f"AI Evaluation: {case_id}", border_style="blue"))
                
            elif ai_provider.lower() == "anthropic":
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
                evaluation = message.content[0].text
                
                # Save evaluation
                eval_file = case_dir / "AI_EVALUATION_RESULT.md"
                eval_file.write_text(evaluation, encoding='utf-8')
                console.print(f"[green]Evaluation saved to: {eval_file}[/green]")
                
                # Display evaluation
                console.print(Panel(Markdown(evaluation), title=f"AI Evaluation: {case_id}", border_style="blue"))
            else:
                console.print(f"[yellow]AI provider '{ai_provider}' not yet implemented. Prompt saved for manual use.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error calling AI: {e}[/red]")
            console.print(f"[yellow]Prompt saved to {prompt_file} for manual evaluation[/yellow]")
    else:
        console.print(f"[yellow]No AI provider specified. Prompt saved to: {prompt_file}[/yellow]")
        console.print("[cyan]You can copy this prompt and use it with any AI model for evaluation.[/cyan]")

def main():
    """Main evaluation function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate generated case documents using AI")
    parser.add_argument("case_path", help="Path to case directory to evaluate")
    parser.add_argument("--ai", choices=["openai", "anthropic", "none"], default="none", help="AI provider to use")
    parser.add_argument("--api-key", help="API key for AI provider")
    
    args = parser.parse_args()
    
    case_dir = Path(args.case_path)
    if not case_dir.exists():
        console.print(f"[red]Case directory not found: {case_dir}[/red]")
        return
    
    evaluate_case_with_ai(case_dir, args.ai, args.api_key)

if __name__ == "__main__":
    main()

