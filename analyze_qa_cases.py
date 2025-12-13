#!/usr/bin/env python3
"""Analyze generated QA cases for consistency, realism, and depth."""
import os
import re
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from collections import defaultdict

console = Console()

def analyze_case_consistency(case_dir: Path) -> dict:
    """Analyze a single case for internal consistency."""
    issues = []
    strengths = []
    
    # Read case briefing
    briefing_path = case_dir / "CASE_BRIEFING.md"
    if not briefing_path.exists():
        issues.append("Missing CASE_BRIEFING.md")
        return {"issues": issues, "strengths": strengths}
    
    briefing = briefing_path.read_text(encoding='utf-8')
    
    # Extract key entities
    persons = re.findall(r'\*\*(.*?):\*\* (.*?) \(', briefing)
    case_id = re.search(r'\*\*ID:\*\* (.*)', briefing)
    crime_type = re.search(r'\*\*Crime Type:\*\* (.*)', briefing)
    
    if case_id:
        case_id = case_id.group(1).strip()
    if crime_type:
        crime_type = crime_type.group(1).strip()
    
    # Check documents
    docs_dir = case_dir / "documents"
    if not docs_dir.exists():
        issues.append("Missing documents directory")
        return {"issues": issues, "strengths": strengths}
    
    doc_files = list(docs_dir.glob("*.txt"))
    if len(doc_files) < 3:
        issues.append(f"Too few documents: {len(doc_files)}")
    else:
        strengths.append(f"Good document count: {len(doc_files)}")
    
    # Analyze document content
    person_names = set()
    phone_numbers = set()
    addresses = set()
    ip_addresses = set()
    email_addresses = set()
    
    for doc_file in doc_files:
        try:
            content = doc_file.read_text(encoding='utf-8')
            
            # Extract entities
            names = re.findall(r'([A-Z][a-z]+ [A-Z][a-z]+)', content)
            person_names.update(names)
            
            phones = re.findall(r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})', content)
            phone_numbers.update(phones)
            
            ips = re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', content)
            ip_addresses.update(ips)
            
            emails = re.findall(r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', content)
            email_addresses.update(emails)
            
            # Check for crime-type appropriateness
            if crime_type:
                if "Scam" in crime_type or "Fraud" in crime_type:
                    # Should NOT have physical evidence
                    if any(term in content for term in ["Latent Fingerprints", "footprints", "tire tracks", "ballistics", "DNA traces"]):
                        issues.append(f"Physical evidence in non-physical crime: {doc_file.name}")
                elif "Homicide" in crime_type or "Assault" in crime_type:
                    # Should have physical evidence
                    if len(doc_files) > 5 and not any(term in content for term in ["Fingerprint", "DNA", "ballistic", "autopsy", "forensic"]):
                        if "INCIDENT REPORT" not in content:  # Skip initial reports
                            issues.append(f"Missing physical evidence in violent crime: {doc_file.name}")
            
            # Check document depth
            if len(content) < 200:
                issues.append(f"Shallow document: {doc_file.name} ({len(content)} chars)")
            elif len(content) > 1000:
                strengths.append(f"Detailed document: {doc_file.name} ({len(content)} chars)")
            
            # Check for consistency markers
            if case_id and case_id not in content and "CASE" in content:
                # Case ID should appear in most documents
                pass  # Not critical
            
        except Exception as e:
            issues.append(f"Error reading {doc_file.name}: {e}")
    
    # Check entity consistency
    if len(person_names) > 0:
        strengths.append(f"Multiple entities referenced: {len(person_names)} names")
    if len(phone_numbers) > 1:
        strengths.append(f"Phone numbers tracked: {len(phone_numbers)}")
    if len(ip_addresses) > 0:
        strengths.append(f"IP addresses tracked: {len(ip_addresses)}")
    
    # Check for investigation flow (for non-physical crimes)
    if crime_type and ("Scam" in crime_type or "Fraud" in crime_type):
        has_initial_report = any("INITIAL" in d.read_text(encoding='utf-8')[:200] for d in doc_files)
        has_followup = any("FOLLOW" in d.read_text(encoding='utf-8')[:200] for d in doc_files)
        has_phone_investigation = any("PHONE RECORDS" in d.read_text(encoding='utf-8')[:200] for d in doc_files)
        
        if not has_initial_report:
            issues.append("Missing initial victim report for scam/fraud case")
        if not has_followup:
            issues.append("Missing follow-up investigation report")
        if not has_phone_investigation and len(doc_files) > 3:
            issues.append("Missing phone records investigation (expected for scam)")
    
    return {
        "issues": issues,
        "strengths": strengths,
        "stats": {
            "doc_count": len(doc_files),
            "person_names": len(person_names),
            "phone_numbers": len(phone_numbers),
            "ip_addresses": len(ip_addresses),
            "email_addresses": len(email_addresses)
        }
    }

def analyze_all_cases():
    """Analyze all QA cases."""
    console.print(Panel.fit("[bold blue]QA Case Analysis[/bold blue]"))
    
    qa_dir = Path("cases_qa")
    if not qa_dir.exists():
        console.print("[red]QA cases directory not found. Run generate_qa_cases.py first.[/red]")
        return
    
    case_dirs = [d for d in qa_dir.iterdir() if d.is_dir() and d.name.startswith("CASE-")]
    
    if not case_dirs:
        console.print("[red]No cases found in QA directory.[/red]")
        return
    
    console.print(f"\n[cyan]Analyzing {len(case_dirs)} cases...[/cyan]\n")
    
    all_issues = defaultdict(list)
    all_strengths = defaultdict(list)
    case_results = []
    
    for case_dir in case_dirs:
        analysis = analyze_case_consistency(case_dir)
        case_results.append({
            "case_id": case_dir.name,
            "analysis": analysis
        })
        
        for issue in analysis["issues"]:
            all_issues[case_dir.name].append(issue)
        for strength in analysis["strengths"]:
            all_strengths[case_dir.name].append(strength)
    
    # Create summary table
    table = Table(title="Case Analysis Summary")
    table.add_column("Case ID", style="cyan")
    table.add_column("Issues", style="red")
    table.add_column("Strengths", style="green")
    table.add_column("Documents", justify="right")
    table.add_column("Entities", justify="right")
    
    for result in case_results:
        case_id = result["case_id"]
        analysis = result["analysis"]
        issues_count = len(analysis["issues"])
        strengths_count = len(analysis["strengths"])
        doc_count = analysis["stats"]["doc_count"]
        entity_count = analysis["stats"]["person_names"]
        
        table.add_row(
            case_id,
            str(issues_count),
            str(strengths_count),
            str(doc_count),
            str(entity_count)
        )
    
    console.print(table)
    
    # Detailed issues
    if all_issues:
        console.print("\n[bold red]Issues Found:[/bold red]")
        for case_id, issues in all_issues.items():
            if issues:
                console.print(f"\n[red]{case_id}:[/red]")
                for issue in issues[:5]:  # Show first 5 issues
                    console.print(f"  - {issue}")
                if len(issues) > 5:
                    console.print(f"  ... and {len(issues) - 5} more")
    
    # Summary
    total_issues = sum(len(issues) for issues in all_issues.values())
    total_strengths = sum(len(strengths) for strengths in all_strengths.values())
    
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Total Issues: {total_issues}")
    console.print(f"  Total Strengths: {total_strengths}")
    console.print(f"  Cases Analyzed: {len(case_dirs)}")
    
    return {
        "case_results": case_results,
        "total_issues": total_issues,
        "total_strengths": total_strengths
    }

if __name__ == "__main__":
    analyze_all_cases()

