#!/usr/bin/env python3
"""
Test script to verify consistency improvements.
Generates a test case and checks for consistency issues.
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.generators import CaseGenerator
from src.exporter import CaseExporter

console = Console()

def check_consistency(case_dir: Path) -> dict:
    """Check a generated case for consistency issues."""
    issues = {
        "jurisdiction": [],
        "officer_badges": [],
        "entity_names": [],
        "timeline": []
    }
    
    # Read all documents
    docs_dir = case_dir / "documents"
    if not docs_dir.exists():
        return issues
    
    documents = {}
    for doc_file in docs_dir.glob("*.txt"):
        documents[doc_file.name] = doc_file.read_text(encoding='utf-8')
    
    # Check jurisdiction consistency
    jurisdictions = set()
    for doc_name, content in documents.items():
        if "SEARCH_WARRANT" in doc_name or "AFFIDAVIT" in doc_name:
            # Extract state
            for line in content.split('\n'):
                if "State of" in line:
                    state = line.strip()
                    jurisdictions.add(state)
                    break
    
    if len(jurisdictions) > 1:
        issues["jurisdiction"].append(f"Multiple jurisdictions found: {jurisdictions}")
    
    # Check officer badge consistency
    officer_badges = {}  # officer_name -> set of badge numbers
    for doc_name, content in documents.items():
        if "SEARCH_WARRANT" in doc_name or "AFFIDAVIT" in doc_name or "INCIDENT_REPORT" in doc_name:
            # Look for badge numbers
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "Badge #" in line or "Badge:" in line:
                    # Try to extract officer name from previous lines
                    officer_name = None
                    for j in range(max(0, i-5), i):
                        if "Officer" in lines[j] or "Detective" in lines[j]:
                            # Extract name
                            parts = lines[j].split()
                            for k, part in enumerate(parts):
                                if part in ["Officer", "Detective"] and k+1 < len(parts):
                                    officer_name = " ".join(parts[k+1:k+3]) if k+2 < len(parts) else parts[k+1]
                                    break
                            if officer_name:
                                break
                    
                    # Extract badge number
                    badge_match = None
                    if "Badge #" in line:
                        badge_match = line.split("Badge #")[1].strip().split()[0]
                    elif "Badge:" in line:
                        badge_match = line.split("Badge:")[1].strip().split()[0]
                    
                    if badge_match and officer_name:
                        if officer_name not in officer_badges:
                            officer_badges[officer_name] = set()
                        officer_badges[officer_name].add(badge_match)
    
    for officer, badges in officer_badges.items():
        if len(badges) > 1:
            issues["officer_badges"].append(f"Officer {officer} has multiple badge numbers: {badges}")
    
    return issues

def main():
    """Generate test cases and check consistency."""
    console.print("[cyan]Generating test case to verify consistency improvements...[/cyan]")
    
    generator = CaseGenerator()
    
    # Generate a test case
    test_case = generator.generate_case(
        crime_type="Assault",
        complexity="High",
        modifiers=["Phone data pull", "IP logs"],
        subject_status="Known"
    )
    
    if not test_case:
        console.print("[red]Failed to generate case![/red]")
        return
    
    console.print(f"[green]Generated case: {test_case.id}[/green]")
    console.print(f"[green]Documents: {len(test_case.documents)}[/green]")
    
    # Export case
    exporter = CaseExporter()
    case_dir_str = exporter.export(test_case, base_path="test_cases")
    case_dir = Path(case_dir_str)
    
    console.print(f"[green]Exported to: {case_dir}[/green]")
    
    # Check consistency
    console.print("\n[cyan]Checking consistency...[/cyan]")
    issues = check_consistency(case_dir)
    
    # Display results
    table = Table(title="Consistency Check Results")
    table.add_column("Category", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Details", style="yellow")
    
    total_issues = 0
    for category, issue_list in issues.items():
        if issue_list:
            status = f"[red]❌ {len(issue_list)} issue(s)[/red]"
            details = "\n".join(issue_list[:3])  # Show first 3
            if len(issue_list) > 3:
                details += f"\n... and {len(issue_list) - 3} more"
            total_issues += len(issue_list)
        else:
            status = "[green]✅ OK[/green]"
            details = "No issues found"
        
        table.add_row(category.replace("_", " ").title(), status, details)
    
    console.print("\n")
    console.print(table)
    
    if total_issues == 0:
        console.print("\n[green]✅ All consistency checks passed![/green]")
    else:
        console.print(f"\n[yellow]⚠️  Found {total_issues} consistency issue(s)[/yellow]")
        console.print("[yellow]Review the case documents for details.[/yellow]")
    
    return case_dir

if __name__ == "__main__":
    main()

