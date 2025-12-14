#!/usr/bin/env python3
"""
Test script to generate a MOD-IN case analysis document.
"""

import sys
from pathlib import Path
from rich.console import Console

sys.path.insert(0, str(Path(__file__).parent))

from src.generators import CaseGenerator
from src.exporter import CaseExporter
from src.case_analyzer import generate_mod_in_for_case

console = Console()

def main():
    """Generate a test case and create MOD-IN analysis."""
    console.print("[cyan]Generating test case...[/cyan]")
    
    generator = CaseGenerator()
    case = generator.generate_case(
        crime_type="Assault",
        complexity="High",
        modifiers=["Phone data pull", "IP logs", "Financial Records"],
        subject_status="Known"
    )
    
    if not case:
        console.print("[red]Failed to generate case![/red]")
        return
    
    console.print(f"[green]Generated case: {case.id}[/green]")
    
    # Generate MOD-IN
    console.print("[cyan]Generating MOD-IN analysis...[/cyan]")
    mod_in = generate_mod_in_for_case(case, detective_name="Detective Sarah Martinez", badge_number=4827)
    
    # Export case
    exporter = CaseExporter()
    case_dir = exporter.export(case, base_path="test_mod_in_cases")
    
    console.print(f"[green]Case exported to: {case_dir}[/green]")
    console.print(f"[green]MOD-IN analysis included in export![/green]")
    console.print("")
    console.print("[cyan]MOD-IN Preview:[/cyan]")
    console.print("")
    
    # Show first 50 lines
    lines = mod_in.split('\n')
    for line in lines[:50]:
        console.print(line)
    
    console.print("")
    console.print(f"[yellow]... ({len(lines) - 50} more lines)[/yellow]")
    console.print("")
    console.print(f"[green]Full MOD-IN saved to: {case_dir}/MOD-IN_CASE_ANALYSIS.md[/green]")

if __name__ == "__main__":
    main()

