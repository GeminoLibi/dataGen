#!/usr/bin/env python3
"""Generate comprehensive QA test cases for all crime types."""
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from src.generators import CaseGenerator
from src.exporter import CaseExporter

console = Console()

# Crime types with appropriate modifiers
CRIME_CONFIGS = [
    # Physical Crimes
    {"type": "Homicide", "complexity": "High", "modifiers": ["Phone data pull", "Body Cam", "Financial Records"], "status": "Known"},
    {"type": "Assault", "complexity": "Medium", "modifiers": ["Phone data pull", "Body Cam"], "status": "Known"},
    {"type": "Robbery", "complexity": "High", "modifiers": ["Phone data pull", "CCTV", "ALPR"], "status": "Partially Known"},
    {"type": "Burglary", "complexity": "Low", "modifiers": ["IP logs"], "status": "Unknown"},
    {"type": "Theft", "complexity": "Low", "modifiers": [], "status": "Known"},
    {"type": "Arson", "complexity": "Medium", "modifiers": ["IP logs", "Financial Records"], "status": "Known"},
    
    # Non-Physical Crimes
    {"type": "Fraud", "complexity": "High", "modifiers": ["Phone data pull", "IP logs", "DNS records", "Financial Records", "Data-Heavy Financial"], "status": "Partially Known"},
    {"type": "Cybercrime", "complexity": "High", "modifiers": ["Data-Heavy IP Logs", "DNS records", "Email Dump"], "status": "Unknown"},
    
    # Phone Scam (test crime-specific generation)
    {"type": "Phone Scam", "complexity": "Medium", "modifiers": ["Phone data pull", "IP logs", "DNS records"], "status": "Unknown"},
    
    # Additional variations
    {"type": "Drug Possession", "complexity": "Medium", "modifiers": ["Phone data pull"], "status": "Known"},
    {"type": "Domestic Violence", "complexity": "Medium", "modifiers": ["Body Cam", "Phone data pull"], "status": "Known"},
    {"type": "Stalking", "complexity": "High", "modifiers": ["Phone data pull", "IP logs", "Email Dump"], "status": "Partially Known"},
]

def generate_qa_cases():
    """Generate all QA test cases."""
    console.print("[bold blue]Generating QA Test Cases[/bold blue]")
    
    # Clean old QA cases
    qa_dir = "cases_qa"
    if os.path.exists(qa_dir):
        import shutil
        shutil.rmtree(qa_dir)
    os.makedirs(qa_dir, exist_ok=True)
    
    generator = CaseGenerator()
    results = []
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Generating cases...", total=len(CRIME_CONFIGS))
        
        for i, config in enumerate(CRIME_CONFIGS, 1):
            progress.update(task, description=f"Generating {config['type']} ({config['complexity']})...")
            
            try:
                case = generator.generate_case(
                    config['type'],
                    config['complexity'],
                    config['modifiers'],
                    config['status']
                )
                
                if case:
                    # Export to QA directory
                    export_path = CaseExporter.export(case, base_path=qa_dir)
                    
                    results.append({
                        "config": config,
                        "case": case,
                        "path": export_path,
                        "success": True
                    })
                    console.print(f"[green]✓[/green] {config['type']} - {case.id} ({len(case.documents)} docs, {len(case.evidence)} evidence)")
                else:
                    results.append({
                        "config": config,
                        "case": None,
                        "path": None,
                        "success": False,
                        "error": "Case generation returned None"
                    })
                    console.print(f"[red]✗[/red] {config['type']} - Generation failed")
                    
            except Exception as e:
                results.append({
                    "config": config,
                    "case": None,
                    "path": None,
                    "success": False,
                    "error": str(e)
                })
                console.print(f"[red]✗[/red] {config['type']} - Error: {e}")
            
            progress.advance(task)
    
    return results

if __name__ == "__main__":
    results = generate_qa_cases()
    console.print(f"\n[bold]Generated {sum(1 for r in results if r['success'])}/{len(results)} cases[/bold]")

