"""
Comprehensive test script for CLI case generation.
Tests all possible combinations of options to find breaking points.
"""
import sys
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from src.config import (
    CRIME_TYPES, COMPLEXITY_LEVELS, SUBJECT_STATUS_OPTIONS, 
    SUBJECT_CLARITY_OPTIONS, INVESTIGATIVE_MODIFIERS, TREND_TYPES
)
from src.generators import CaseGenerator
from src.trend_generator import TrendGenerator
from src.exporter import CaseExporter

console = Console()

class TestResult:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.errors = []

def test_single_case_combinations():
    """Test all single case combinations."""
    console.print("\n[bold blue]Testing Single Case Combinations[/bold blue]")
    results = TestResult()
    
    generator = CaseGenerator()
    
    # Test each crime type
    for crime_key, crime_type in CRIME_TYPES.items():
        for complexity in COMPLEXITY_LEVELS:
            for subject_status in SUBJECT_STATUS_OPTIONS:
                # Test with and without modifiers
                for use_modifiers in [False, True]:
                    # Test subject clarity for unknown cases
                    subject_clarity = None
                    if subject_status == "Unknown":
                        for clarity_option in SUBJECT_CLARITY_OPTIONS.keys():
                            test_name = f"{crime_type} | {complexity} | {subject_status} | {clarity_option} | Modifiers: {use_modifiers}"
                            modifiers = ["Phone data pull"] if use_modifiers else []
                            
                            try:
                                case = generator.generate_case(
                                    crime_type, complexity, modifiers,
                                    subject_status=subject_status,
                                    subject_clarity=clarity_option
                                )
                                if case and case.id:
                                    results.passed.append(test_name)
                                else:
                                    results.failed.append(f"{test_name} - No case generated")
                            except Exception as e:
                                results.failed.append(f"{test_name} - {str(e)}")
                                results.errors.append(f"{test_name}\n{str(e)}")
                    else:
                        test_name = f"{crime_type} | {complexity} | {subject_status} | Modifiers: {use_modifiers}"
                        modifiers = ["Phone data pull"] if use_modifiers else []
                        
                        try:
                            case = generator.generate_case(
                                crime_type, complexity, modifiers,
                                subject_status=subject_status,
                                subject_clarity=subject_clarity
                            )
                            if case and case.id:
                                results.passed.append(test_name)
                            else:
                                results.failed.append(f"{test_name} - No case generated")
                        except Exception as e:
                            results.failed.append(f"{test_name} - {str(e)}")
                            results.errors.append(f"{test_name}\n{str(e)}")
    
    return results

def test_trend_combinations():
    """Test all trend combinations."""
    console.print("\n[bold blue]Testing Trend Combinations[/bold blue]")
    results = TestResult()
    
    trend_gen = TrendGenerator()
    
    # Test each trend type
    for trend_key, trend_type in TREND_TYPES.items():
        for complexity in COMPLEXITY_LEVELS:
            for subject_status in SUBJECT_STATUS_OPTIONS:
                subject_clarity = None
                if subject_status == "Unknown":
                    for clarity_option in SUBJECT_CLARITY_OPTIONS.keys():
                        test_name = f"{trend_type} | {complexity} | {subject_status} | {clarity_option} | 3 cases"
                        
                        try:
                            cases, registry = trend_gen.generate_trend(
                                trend_type, 3, complexity, [],
                                subject_status=subject_status,
                                subject_clarity=clarity_option,
                                identification_status="Identified"
                            )
                            if cases and len(cases) > 0:
                                results.passed.append(test_name)
                            else:
                                results.failed.append(f"{test_name} - No cases generated")
                        except Exception as e:
                            results.failed.append(f"{test_name} - {str(e)}")
                            results.errors.append(f"{test_name}\n{str(e)}")
                else:
                    test_name = f"{trend_type} | {complexity} | {subject_status} | 3 cases"
                    
                    try:
                        cases, registry = trend_gen.generate_trend(
                            trend_type, 3, complexity, [],
                            subject_status=subject_status,
                            subject_clarity=subject_clarity,
                            identification_status="Identified"
                        )
                        if cases and len(cases) > 0:
                            results.passed.append(test_name)
                        else:
                            results.failed.append(f"{test_name} - No cases generated")
                    except Exception as e:
                        results.failed.append(f"{test_name} - {str(e)}")
                        results.errors.append(f"{test_name}\n{str(e)}")
    
    return results

def test_modifier_combinations():
    """Test various modifier combinations."""
    console.print("\n[bold blue]Testing Modifier Combinations[/bold blue]")
    results = TestResult()
    
    generator = CaseGenerator()
    
    # Test individual modifiers
    for mod_key, (mod_name, mod_desc) in INVESTIGATIVE_MODIFIERS.items():
        test_name = f"Single Case | Fraud | Medium | Known | Modifier: {mod_name}"
        
        try:
            case = generator.generate_case(
                "Fraud", "Medium", [mod_name],
                subject_status="Known"
            )
            if case and case.id:
                results.passed.append(test_name)
            else:
                results.failed.append(f"{test_name} - No case generated")
        except Exception as e:
            results.failed.append(f"{test_name} - {str(e)}")
            results.errors.append(f"{test_name}\n{str(e)}")
    
    # Test multiple modifiers together
    test_combinations = [
        ["Phone data pull", "Financial Records"],
        ["Data-Heavy Phone Dump", "Data-Heavy IP Logs"],
        ["Phone data pull", "IP logs", "Financial Records", "Body Cam"],
    ]
    
    for combo in test_combinations:
        test_name = f"Single Case | Fraud | Medium | Known | Modifiers: {', '.join(combo)}"
        
        try:
            case = generator.generate_case(
                "Fraud", "Medium", combo,
                subject_status="Known"
            )
            if case and case.id:
                results.passed.append(test_name)
            else:
                results.failed.append(f"{test_name} - No case generated")
        except Exception as e:
            results.failed.append(f"{test_name} - {str(e)}")
            results.errors.append(f"{test_name}\n{str(e)}")
    
    return results

def print_results(single_results, trend_results, modifier_results):
    """Print comprehensive test results."""
    console.print("\n" + "="*80)
    console.print("[bold green]TEST RESULTS SUMMARY[/bold green]")
    console.print("="*80)
    
    total_passed = len(single_results.passed) + len(trend_results.passed) + len(modifier_results.passed)
    total_failed = len(single_results.failed) + len(trend_results.failed) + len(modifier_results.failed)
    
    table = Table(title="Test Statistics")
    table.add_column("Category", style="cyan")
    table.add_column("Passed", style="green")
    table.add_column("Failed", style="red")
    
    table.add_row("Single Cases", str(len(single_results.passed)), str(len(single_results.failed)))
    table.add_row("Trends", str(len(trend_results.passed)), str(len(trend_results.failed)))
    table.add_row("Modifiers", str(len(modifier_results.passed)), str(len(modifier_results.failed)))
    table.add_row("TOTAL", str(total_passed), str(total_failed))
    
    console.print(table)
    
    # Show failures
    all_failures = single_results.failed + trend_results.failed + modifier_results.failed
    all_errors = single_results.errors + trend_results.errors + modifier_results.errors
    
    if all_failures:
        console.print(f"\n[bold red]Failed Tests ({len(all_failures)}):[/bold red]")
        for failure in all_failures[:20]:  # Show first 20
            console.print(f"  [red]FAILED:[/red] {failure}")
        if len(all_failures) > 20:
            console.print(f"  ... and {len(all_failures) - 20} more failures")
    
    if all_errors:
        console.print(f"\n[bold yellow]Error Details:[/bold yellow]")
        for error in all_errors[:5]:  # Show first 5 detailed errors
            console.print(f"[dim]{error}[/dim]\n")

def main():
    console.print("[bold]Comprehensive CLI Test Suite[/bold]")
    console.print("Testing all possible combinations...\n")
    
    single_results = test_single_case_combinations()
    trend_results = test_trend_combinations()
    modifier_results = test_modifier_combinations()
    
    print_results(single_results, trend_results, modifier_results)
    
    total_failed = len(single_results.failed) + len(trend_results.failed) + len(modifier_results.failed)
    
    if total_failed == 0:
        console.print("\n[bold green]All tests passed![/bold green]")
        sys.exit(0)
    else:
        console.print(f"\n[bold red]{total_failed} test(s) failed[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Testing cancelled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Fatal error:[/red] {str(e)}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)

