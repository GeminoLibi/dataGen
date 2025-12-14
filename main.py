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
    
    # Ask if user wants single case or trend
    generation_types = {
        "1": "Single Case",
        "2": "Trend (Multiple Related Cases)"
    }

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
        
        trend_choice = Prompt.ask("\nSelect [bold red]Trend Type[/bold red]", default="1")
        trend_type = trend_types.get(trend_choice, "Serial Offender")
        
        num_cases = IntPrompt.ask("How many related cases to generate?", default=5)

        # Complexity selection for trend
        console.print("\n[bold]Complexity Level:[/bold]")
        for key, comp in complexities.items():
            console.print(f"{key}. {comp}")

        complexity_choice = Prompt.ask("\nSelect [bold yellow]Complexity[/bold yellow] (1-3)", default="2")
        complexity = complexities.get(complexity_choice, complexities["2"])

        # Subject status for trend
        console.print("\n[bold]Subject Status:[/bold]")
        console.print("[dim]Note: Selecting 'Unknown' provides additional identification clarity options.[/dim]")
        for key, status in subject_statuses.items():
            console.print(f"{key}. {status}")

        subject_choice = Prompt.ask("\nSelect [bold cyan]Subject Status[/bold cyan] (1-3)", default="1")
        subject_status = subject_statuses.get(subject_choice, subject_statuses["1"])

        # Subject identification clarity for unknown cases
        subject_clarity = None
        if subject_status == "Unknown":
            console.print("\n[bold magenta]Subject Identification Clarity:[/bold magenta]")
            for key, desc in SUBJECT_CLARITY_OPTIONS.items():
                console.print(f"[cyan]{key}[/cyan]: {desc}")
            subject_clarity = Prompt.ask("\nSelect [bold magenta]Identification Approach[/bold magenta]",
                                       choices=list(SUBJECT_CLARITY_OPTIONS.keys()), default="Embedded")

        identification_status = Prompt.ask(
            "\n[bold magenta]Identification Status[/bold magenta]",
            choices=["Identified", "Unidentified"],
            default="Identified"
        )
        
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
        
        with console.status("Processing trend generation...", spinner="dots"):
            trend_gen = TrendGenerator()
            cases, registry = trend_gen.generate_trend(trend_type, num_cases, complexity, final_modifiers, subject_status, subject_clarity, identification_status)
        
        console.clear()
        console.print(Panel(f"[bold]{trend_type} Trend[/bold]\nTrend ID: {registry.trend_id}\nCases Generated: {len(cases)}", title="Trend Generation Complete", border_style="blue"))
        
        # Export all cases
        export_paths = []
        for case in cases:
            export_path = CaseExporter.export(case)
            export_paths.append(export_path)
        
        console.print(f"\n[bold blue]All cases exported to:[/bold blue]")
        for path in export_paths:
            console.print(f"  - {path}")
        
        console.print(f"\n[bold green]Trend Generation Complete. Master investigation file included.[/bold green]")
        return

    # Predefined crime types for onboarding
    crime_types = {
        "1": "Homicide",
        "2": "Assault",
        "3": "Robbery",
        "4": "Burglary",
        "5": "Theft",
        "6": "Fraud",
        "7": "Drug Possession",
        "8": "Domestic Violence",
        "9": "Stalking",
        "10": "Arson"
    }

    console.print("\n[bold]Available Crime Types:[/bold]")
    for key, crime in crime_types.items():
        console.print(f"{key}. {crime}")

    crime_choice = Prompt.ask("\nSelect [bold red]Crime Type[/bold red] (number or name)", default="1")

    # Handle both number and name input
    if crime_choice in crime_types:
        crime_type = crime_types[crime_choice]
    elif crime_choice.isdigit() and crime_choice in crime_types:
        crime_type = crime_types[crime_choice]
    else:
        # Check if they typed the crime name directly
        for key, crime in crime_types.items():
            if crime_choice.lower() == crime.lower():
                crime_type = crime
                break
        else:
            # Default fallback
            crime_type = crime_types["1"]

    # Complexity selection
    complexities = {
        "1": "Low",
        "2": "Medium",
        "3": "High"
    }

    console.print("\n[bold]Complexity Level:[/bold]")
    for key, comp in complexities.items():
        console.print(f"{key}. {comp}")

    complexity_choice = Prompt.ask("\nSelect [bold yellow]Complexity[/bold yellow] (1-3)", default="2")
    complexity = complexities.get(complexity_choice, complexities["2"])

    # Subject status (known vs unknown)
    subject_statuses = {
        "1": "Known",
        "2": "Unknown",
        "3": "Partially Known"
    }

    console.print("\n[bold]Subject Status:[/bold]")
    console.print("[dim]Note: Selecting 'Unknown' provides additional identification clarity options.[/dim]")
    for key, status in subject_statuses.items():
        console.print(f"{key}. {status}")

    subject_choice = Prompt.ask("\nSelect [bold cyan]Subject Status[/bold cyan] (1-3)", default="2")
    subject_status = subject_statuses.get(subject_choice, subject_statuses["2"])

    # Subject identification clarity for unknown cases
    subject_clarity = None
    if subject_status == "Unknown":
        console.print("\n[bold magenta]Subject Identification Clarity:[/bold magenta]")
        for key, desc in SUBJECT_CLARITY_OPTIONS.items():
            console.print(f"[cyan]{key}[/cyan]: {desc}")
        subject_clarity = Prompt.ask("\nSelect [bold magenta]Identification Approach[/bold magenta]",
                                   choices=list(SUBJECT_CLARITY_OPTIONS.keys()), default="Embedded")

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
    
    with console.status("Processing procedural generation...", spinner="dots"):
        generator = CaseGenerator()
        case = generator.generate_case(crime_type, complexity, final_modifiers, subject_status=subject_status, subject_clarity=subject_clarity)

    # Output
    console.clear()
    console.print(Panel(f"[bold]{case.title}[/bold]\nID: {case.id}\nStatus: {case.status}", title="Case Briefing", border_style="blue"))
    
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
        console.print("\n[red]Generation cancelled.[/red]")
        sys.exit(0)

