import os
from rich.console import Console
from .models import Case

console = Console()

class CaseExporter:
    @staticmethod
    def export(case: Case, base_path: str = "cases"):
        # Create case directory
        case_dir = os.path.join(base_path, case.id)
        os.makedirs(case_dir, exist_ok=True)
        
        # Create documents directory
        docs_dir = os.path.join(case_dir, "documents")
        os.makedirs(docs_dir, exist_ok=True)

        # Generate and write MOD-IN case analysis
        try:
            from .case_analyzer import generate_mod_in_for_case
            mod_in = generate_mod_in_for_case(case)
            with open(os.path.join(case_dir, "MOD-IN_CASE_ANALYSIS.md"), "w", encoding="utf-8") as f:
                f.write(mod_in)
        except Exception as e:
            console.print(f"[yellow]Warning: Could not generate MOD-IN analysis: {e}[/yellow]")
        
        # Write Case Briefing
        with open(os.path.join(case_dir, "CASE_BRIEFING.md"), "w", encoding="utf-8") as f:
            f.write(f"# {case.title}\n")
            f.write(f"**ID:** {case.id}\n")
            f.write(f"**Status:** {case.status}\n")
            f.write(f"**Date Opened:** {case.date_opened.strftime('%Y-%m-%d')}\n")
            f.write(f"**Crime Type:** {case.crime_type}\n")
            f.write(f"**Complexity:** {case.complexity}\n\n")
            
            f.write("## Narrative\n")
            if case.incident_report:
                f.write(f"{case.incident_report.narrative}\n\n")
            
            f.write("## Involved Persons\n")
            for person in case.persons:
                f.write(f"- **{person.role.value}:** {person.full_name} (Age: {person.age})\n")
                f.write(f"  - Phone: {person.phone_number}\n")
                f.write(f"  - Notes: {person.notes}\n")
            
            f.write("\n## Evidence Log\n")
            for ev in case.evidence:
                f.write(f"- **[{ev.type.value}]** {ev.description} (ID: {ev.id})\n")
                f.write(f"  - Location: {ev.location_found}\n")
                if ev.metadata:
                    f.write(f"  - Metadata: {ev.metadata}\n")

        # Write Documents
        for i, doc in enumerate(case.documents):
            # Try to infer a title from the first line if it looks like a header
            lines = doc.split('\n')
            filename = f"doc_{i+1:03d}.txt"
            if lines and lines[0].startswith("---") and lines[0].endswith("---"):
                # Clean up title
                safe_title = lines[0].replace("-", "").strip().replace(" ", "_").replace("/", "_").replace("\\", "_").replace("(", "").replace(")", "").replace(",", "")
                if safe_title:
                    # Truncate long titles to avoid Windows path length issues
                    if len(safe_title) > 30:
                        safe_title = safe_title[:30]
                    filename = f"doc_{i+1:03d}_{safe_title}.txt"
            
            with open(os.path.join(docs_dir, filename), "w", encoding="utf-8") as f:
                f.write(doc)
                
        return case_dir

