import os
import re
import csv
import io
from rich.console import Console
from .models import Case
from .file_generator import FileGenerator

console = Console()

class CaseExporter:
    @staticmethod
    def _get_case_suffix(case_id: str) -> str:
        """Extract last 4 digits from case ID (e.g., CASE-414373 -> 4373)."""
        # Extract digits from case ID
        digits = ''.join(filter(str.isdigit, case_id))
        if len(digits) >= 4:
            return digits[-4:]
        # Fallback: use all digits if less than 4
        return digits.zfill(4) if digits else "0000"
    
    @staticmethod
    def _append_case_suffix(filename: str, case_id: str) -> str:
        """Append case suffix to filename before extension."""
        suffix = CaseExporter._get_case_suffix(case_id)
        # Split filename and extension
        if '.' in filename:
            name, ext = filename.rsplit('.', 1)
            return f"{name}_{suffix}.{ext}"
        else:
            return f"{filename}_{suffix}"
    
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

        # Initialize file generator
        file_gen = FileGenerator(docs_dir)
        
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
                    filename = f"doc_{i+1:03d}_{safe_title}"
            
            # Detect file type and generate appropriate file
            doc_lower = doc.lower()
            
            # Helper function to get base filename without extension
            def get_base_filename(fname: str) -> str:
                """Get filename without extension."""
                if '.' in fname:
                    return fname.rsplit('.', 1)[0]
                return fname
            
            # Get base filename and append case suffix
            base_filename = get_base_filename(filename)
            suffix = CaseExporter._get_case_suffix(case.id)
            
            # Financial records - generate as XLSX
            if "financial records" in doc_lower and "csv data" in doc_lower:
                try:
                    # Find CSV section
                    csv_start = doc.find("Date,Description")
                    if csv_start != -1:
                        csv_content = doc[csv_start:]
                        csv_lines = [line.strip() for line in csv_content.split('\n') if line.strip() and not line.startswith('-')]
                        if csv_lines:
                            reader = csv.reader(csv_lines)
                            rows = list(reader)
                            if len(rows) > 1:
                                headers = rows[0]
                                data = rows[1:]
                                xlsx_filename = f"{base_filename}_{suffix}.xlsx"
                                file_gen.generate_xlsx(data, headers, xlsx_filename)
                                continue
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not generate XLSX for financial records: {e}[/yellow]")
            
            # Evidence log - generate as XLSX
            if "evidence log" in doc_lower and "csv data" in doc_lower:
                try:
                    csv_start = doc.find("Evidence ID,")
                    if csv_start == -1:
                        csv_start = doc.find("Evidence ID,")
                    if csv_start != -1:
                        csv_content = doc[csv_start:]
                        csv_lines = [line.strip() for line in csv_content.split('\n') if line.strip() and not line.startswith('-')]
                        if csv_lines:
                            reader = csv.reader(csv_lines)
                            rows = list(reader)
                            if len(rows) > 1:
                                headers = rows[0]
                                data = rows[1:]
                                xlsx_filename = f"{base_filename}_{suffix}.xlsx"
                                file_gen.generate_xlsx(data, headers, xlsx_filename)
                                continue
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not generate XLSX for evidence log: {e}[/yellow]")
            
            # Phone records - generate as XLSX
            if "phone records" in doc_lower and "csv data" in doc_lower:
                try:
                    csv_start = doc.find("Date,Time,")
                    if csv_start != -1:
                        csv_content = doc[csv_start:]
                        csv_lines = [line.strip() for line in csv_content.split('\n') if line.strip() and not line.startswith('-')]
                        if csv_lines:
                            reader = csv.reader(csv_lines)
                            rows = list(reader)
                            if len(rows) > 1:
                                headers = rows[0]
                                data = rows[1:]
                                xlsx_filename = f"{base_filename}_{suffix}.xlsx"
                                file_gen.generate_xlsx(data, headers, xlsx_filename)
                                continue
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not generate XLSX for phone records: {e}[/yellow]")
            
            # Incident reports - generate as PDF
            if "incident report" in doc_lower:
                try:
                    pdf_filename = f"{base_filename}_{suffix}.pdf"
                    file_gen.generate_pdf(doc, pdf_filename)
                    continue
                except:
                    pass
            
            # Memos - generate as DOCX
            if "memo" in doc_lower or "department memo" in doc_lower:
                try:
                    docx_filename = f"{base_filename}_{suffix}.docx"
                    file_gen.generate_docx(doc, docx_filename)
                    continue
                except:
                    pass
            
            # Ransom notes - keep as TXT (handwritten style)
            if "ransom note" in doc_lower:
                txt_filename = f"{base_filename}_{suffix}.txt"
                file_gen.generate_txt(doc, txt_filename)
                continue
            
            # Default: write as text file
            txt_filename = f"{base_filename}_{suffix}.txt"
            with open(os.path.join(docs_dir, txt_filename), "w", encoding="utf-8") as f:
                f.write(doc)
                
        return case_dir

