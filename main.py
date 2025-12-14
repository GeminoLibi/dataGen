import sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from src.generators import CaseGenerator
from src.config import CRIME_TYPES, COMPLEXITY_LEVELS, SUBJECT_STATUS_OPTIONS, SUBJECT_CLARITY_OPTIONS, INVESTIGATIVE_MODIFIERS, TREND_TYPES, AI_MODELS

console = Console()

def main():
    console.print(Panel.fit("[bold blue]Law Enforcement Case Generator[/bold blue]", subtitle="Procedural Generation System"))
    
    # Define common option dictionaries (used by both single case and trend workflows)
    generation_types = {
        "1": "Single Case",
        "2": "Trend (Multiple Related Cases)"
    }

    complexities = {
        "1": "Low",
        "2": "Medium",
        "3": "High"
    }

    subject_statuses = {
        "1": "Known",
        "2": "Unknown",
        "3": "Partially Known"
    }
    
    # Ask if user wants single case or trend

    console.print("\n[bold]Generation Type:[/bold]")
    for key, gen_type in generation_types.items():
        console.print(f"{key}. {gen_type}")

    generation_choice = Prompt.ask("\nSelect [bold blue]Generation Type[/bold blue] (1-2)", default="1")

    if generation_choice in generation_types:
        generation_type = generation_types[generation_choice]
    else:
        # Handle direct input (e.g., if they type "Single Case")
        for key, gen_type in generation_types.items():
            if generation_choice.lower() == gen_type.lower():
                generation_type = gen_type
                break
        else:
            # Default fallback
            generation_type = generation_types["1"]
    
    if generation_type == generation_types["2"]:
        from src.trend_generator import TrendGenerator
        from src.exporter import CaseExporter
        
        trend_types = {
            "1": "Serial Offender",
            "2": "Organized Crime",
            "3": "Crime Ring",
            "4": "Victim Pattern",
            "5": "Location Pattern",
            "6": "Mixed"
        }
        
        console.print("\n[bold]Available Trend Types:[/bold]")
        for key, trend in trend_types.items():
            console.print(f"{key}. {trend}")
        
        trend_choice = Prompt.ask("\nSelect [bold red]Trend Type[/bold red] (1-6)", default="1")
        trend_type = trend_types.get(trend_choice, "Serial Offender")
        
        # Crime type selection for trend
        console.print("\n[bold]Crime Types (for trend cases):[/bold]")
        for key, crime in CRIME_TYPES.items():
            console.print(f"{key}. {crime}")
        
        crime_type_input = Prompt.ask("\nSelect crime type(s) (comma-separated numbers 1-12, or leave empty for variety)", default="")
        
        selected_crime_types = []
        if crime_type_input.strip():
            choices = [choice.strip() for choice in crime_type_input.split(",")]
            for choice in choices:
                if choice in CRIME_TYPES:
                    selected_crime_types.append(CRIME_TYPES[choice])
                elif choice.isdigit() and choice in CRIME_TYPES:
                    selected_crime_types.append(CRIME_TYPES[choice])
        
        # If no crime types selected, use variety (will be handled by trend generator)
        if not selected_crime_types:
            selected_crime_types = None  # Signal to use default variety
        
        num_cases = IntPrompt.ask("How many related cases to generate?", default=5)

        # Complexity selection for trend
        console.print("\n[bold]Complexity Level:[/bold]")
        for key, comp in complexities.items():
            console.print(f"{key}. {comp}")

        complexity_choice = Prompt.ask("\nSelect [bold yellow]Complexity[/bold yellow] (1-3)", default="2")
        complexity = complexities.get(complexity_choice, complexities["2"])

        # Subject status for trend
        console.print("\n[bold]Subject Status:[/bold]")
        for key, status in subject_statuses.items():
            console.print(f"{key}. {status}")

        subject_choice = Prompt.ask("\nSelect [bold cyan]Subject Status[/bold cyan] (1-3)", default="1")
        subject_status = subject_statuses.get(subject_choice, subject_statuses["1"])

        # Subject identification clarity (applies to all cases)
        clarity_options = {
            "1": "Embedded",
            "2": "Investigative"
        }
        console.print("\n[bold magenta]Subject Identification Approach:[/bold magenta]")
        for key, clarity_key in clarity_options.items():
            desc = SUBJECT_CLARITY_OPTIONS[clarity_key]
            console.print(f"{key}. {clarity_key}: {desc}")
        
        clarity_choice = Prompt.ask("\nSelect [bold magenta]Identification Approach[/bold magenta] (1-2)", default="1")
        subject_clarity = clarity_options.get(clarity_choice, clarity_options["1"])

        # Identification Status
        identification_options = {
            "1": "Identified",
            "2": "Unidentified"
        }
        console.print("\n[bold magenta]Identification Status:[/bold magenta]")
        for key, status in identification_options.items():
            console.print(f"{key}. {status}")
        
        identification_choice = Prompt.ask("\nSelect [bold magenta]Identification Status[/bold magenta] (1-2)", default="1")
        identification_status = identification_options.get(identification_choice, identification_options["1"])
        
        if identification_status == "Identified":
            console.print("[yellow]Identified: Cases are known to be linked, but connections need to be proven.[/yellow]")
        else:
            console.print("[yellow]Unidentified: Cases appear unrelated; connections hidden but discoverable via AI/analysis.[/yellow]")
        
        # Modifiers
        modifier_options = {
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
            "11": ("Random Events", "Add unpredictable events like car wrecks")
        }
        
        console.print("\n[bold]Available Investigative Modifiers:[/bold]")
        for key, (name, desc) in modifier_options.items():
            console.print(f"{key}. [cyan]{name}[/cyan] - {desc}")
        
        modifier_input = Prompt.ask("\nSelect modifiers (comma-separated numbers, or leave empty)", default="")
        final_modifiers = []
        if modifier_input.strip():
            choices = [choice.strip() for choice in modifier_input.split(",")]
            for choice in choices:
                if choice in modifier_options:
                    final_modifiers.append(modifier_options[choice][0])
        
        console.print(f"\n[green]Generating trend: {trend_type} with {num_cases} cases...[/green]")
        
        try:
            with console.status("Processing trend generation...", spinner="dots"):
                trend_gen = TrendGenerator()
                cases, registry = trend_gen.generate_trend(trend_type, num_cases, complexity, final_modifiers, subject_status, subject_clarity, identification_status, selected_crime_types)
            
            if not cases:
                console.print("[red]Error: No cases were generated.[/red]")
                return
            
            console.clear()
            console.print(Panel(f"[bold]{trend_type} Trend[/bold]\nTrend ID: {registry.trend_id}\nCases Generated: {len(cases)}", title="Trend Generation Complete", border_style="blue"))
            
            # Export all cases to trend folder (using trend ID)
            export_paths = []
            trend_folder = f"cases/{registry.trend_id}"
            for i, case in enumerate(cases, 1):
                try:
                    export_path = CaseExporter.export(case, base_path=trend_folder)
                    export_paths.append(export_path)
                except Exception as e:
                    console.print(f"[yellow]Warning: Failed to export case {i}: {e}[/yellow]")
            
            if export_paths:
                console.print(f"\n[bold blue]All cases exported to:[/bold blue]")
                for path in export_paths:
                    console.print(f"  - {path}")
            
            console.print(f"\n[bold green]Trend Generation Complete. Master investigation file included.[/bold green]")
            return  # Exit after successful trend generation
        except Exception as e:
            console.print(f"[red]Error during trend generation:[/red] {str(e)}")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
            return

    # Use CRIME_TYPES from config (includes all 12 types)
    console.print("\n[bold]Available Crime Types:[/bold]")
    for key, crime in CRIME_TYPES.items():
        console.print(f"{key}. {crime}")

    crime_choice = Prompt.ask("\nSelect [bold red]Crime Type[/bold red] (1-12)", default="1")

    # Handle both number and name input
    if crime_choice in CRIME_TYPES:
        crime_type = CRIME_TYPES[crime_choice]
    elif crime_choice.isdigit() and crime_choice in CRIME_TYPES:
        crime_type = CRIME_TYPES[crime_choice]
    else:
        # Check if they typed the crime name directly
        for key, crime in CRIME_TYPES.items():
            if crime_choice.lower() == crime.lower():
                crime_type = crime
                break
        else:
            # Default fallback
            crime_type = CRIME_TYPES["1"]

    # Complexity selection
    console.print("\n[bold]Complexity Level:[/bold]")
    for key, comp in complexities.items():
        console.print(f"{key}. {comp}")

    complexity_choice = Prompt.ask("\nSelect [bold yellow]Complexity[/bold yellow] (1-3)", default="2")
    complexity = complexities.get(complexity_choice, complexities["2"])

    # Subject status (known vs unknown)
    console.print("\n[bold]Subject Status:[/bold]")
    for key, status in subject_statuses.items():
        console.print(f"{key}. {status}")

    subject_choice = Prompt.ask("\nSelect [bold cyan]Subject Status[/bold cyan] (1-3)", default="2")
    subject_status = subject_statuses.get(subject_choice, subject_statuses["2"])

    # Subject identification approach (applies to all cases)
    clarity_options = {
        "1": "Embedded",
        "2": "Investigative"
    }
    console.print("\n[bold magenta]Subject Identification Approach:[/bold magenta]")
    for key, clarity_key in clarity_options.items():
        desc = SUBJECT_CLARITY_OPTIONS[clarity_key]
        console.print(f"{key}. {clarity_key}: {desc}")
    
    clarity_choice = Prompt.ask("\nSelect [bold magenta]Identification Approach[/bold magenta] (1-2)", default="1")
    subject_clarity = clarity_options.get(clarity_choice, clarity_options["1"])

    # Available modifiers with descriptions
    modifier_options = {
        "1": ("Phone data pull", "Extract phone records, texts, and call logs"),
        "2": ("IP logs", "Network traffic analysis and IP address tracking"),
        "3": ("DNS records", "Domain name resolution and internet history"),
        "4": ("Body Cam", "Officer body camera footage and transcripts"),
        "5": ("Email Dump", "Email account contents and metadata"),
        "6": ("Financial Records", "Bank statements and transaction analysis"),
        "7": ("Data-Heavy Phone Dump", "MASSIVE phone extraction with thousands of records"),
        "8": ("Data-Heavy IP Logs", "MASSIVE network logs with 10K+ entries"),
        "9": ("Data-Heavy Financial", "MASSIVE financial records with years of transactions"),
        "10": ("Extra Junk Data", "Generate extensive irrelevant documents for filtering challenge")
    }

    console.print("\n[bold]Available Investigative Modifiers:[/bold]")
    for key, (name, desc) in modifier_options.items():
        console.print(f"{key}. [cyan]{name}[/cyan] - {desc}")

    modifier_input = Prompt.ask("\nSelect modifiers (comma-separated numbers, or leave empty for basic case)", default="")

    final_modifiers = []
    if modifier_input.strip():
        choices = [choice.strip() for choice in modifier_input.split(",")]
        for choice in choices:
            if choice in modifier_options:
                final_modifiers.append(modifier_options[choice][0])
            elif choice.isdigit() and choice in modifier_options:
                final_modifiers.append(modifier_options[choice][0])
            else:
                # Allow custom modifiers if user types something else
                final_modifiers.append(choice)

    console.print(f"\n[green]Generating case for {crime_type} (Complexity: {complexity}, Subjects: {subject_status})...[/green]")
    
    try:
        with console.status("Processing procedural generation...", spinner="dots"):
            generator = CaseGenerator()
            case = generator.generate_case(crime_type, complexity, final_modifiers, subject_status=subject_status, subject_clarity=subject_clarity)
        
        if not case:
            console.print("[red]Error: Case generation failed.[/red]")
            return
        
        # Output
        console.clear()
        console.print(Panel(f"[bold]{case.title}[/bold]\nID: {case.id}\nStatus: {case.status}", title="Case Briefing", border_style="blue"))
    except Exception as e:
        console.print(f"[red]Error during case generation:[/red] {str(e)}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return
    
    # People Table
    table = Table(title="Involved Persons")
    table.add_column("Name", style="cyan")
    table.add_column("Role", style="magenta")
    table.add_column("Notes")
    
    for person in case.persons:
        table.add_row(person.full_name, person.role.value, person.notes[:50] + "...")
    
    console.print(table)
    
    # Evidence Table
    ev_table = Table(title="Evidence Log")
    ev_table.add_column("ID", style="dim")
    ev_table.add_column("Type")
    ev_table.add_column("Description")
    ev_table.add_column("Location")
    
    for ev in case.evidence:
        ev_table.add_row(ev.id[:8], ev.type.value, ev.description, ev.location_found)
        
    console.print(ev_table)
    
    # Documents
    console.print("\n[bold underline]Case Documents[/bold underline]")
    for i, doc in enumerate(case.documents):
        console.print(Panel(doc, title=f"Document #{i+1}", border_style="green"))
    
    # Export to Folder
    from src.exporter import CaseExporter
    export_path = CaseExporter.export(case)
    console.print(f"\n[bold blue]Case exported to folder:[/bold blue] {export_path}")

    console.print("\n[bold green]Case Generation Complete.[/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Generation cancelled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        console.print("[dim]Please report this error if it persists.[/dim]")
        import traceback
        console.print(f"\n[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)

