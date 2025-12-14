from datetime import datetime, timedelta
import random
import json
import os
import tempfile
from typing import List, Dict, Optional
from faker import Faker

from .models import Case, Person, Role, IncidentReport, Evidence, EvidenceType, DigitalDevice, Weapon
from .realistic_errors import RealisticErrorGenerator, EventType, ErrorSeverity
from .utils import (
    generate_case_id, generate_person, generate_date_near, generate_file_hash,
    generate_ip, generate_vehicle, generate_device, generate_weapon, generate_interrogation_dialogue,
    generate_motive, geo_mgr, generate_corp_name, generate_social_posts,
    generate_911_script, generate_cctv_log, generate_browser_history, generate_autopsy_report,
    generate_weather, generate_afis_report, generate_witness_statement, 
    generate_blockchain_ledger, generate_bau_profile, generate_recovered_data,
    generate_ncic_report, generate_iot_logs, generate_burner_receipt,
    generate_uc_report, generate_wiretap_transcript, generate_jailhouse_informant_statement,
    generate_drone_log, generate_k9_report, generate_trash_pull_log,
    generate_entomology_report, generate_toxicology_screen, generate_coroner_scene_notes,
    generate_financial_csv, generate_warrant_return, generate_lineup_form,
    generate_dna_phenotype_report, generate_search_warrant_affidavit,
    generate_phishing_log, generate_pi_report, generate_dark_web_post,
    generate_witsec_profile, generate_ci_contract, generate_network_map,
    generate_soil_analysis_report, generate_infotainment_log, generate_predictive_policing_report,
    generate_cad_log,
    generate_evidence_bagging_log, generate_discovery_index,
    d20, roll_check
)


class TempFileManager:
    """Manages temporary files for case data persistence and iterative complexity building."""

    def __init__(self, base_temp_dir: str = "temp_cases"):
        self.base_temp_dir = base_temp_dir
        self.temp_files = {}
        os.makedirs(base_temp_dir, exist_ok=True)

    def create_temp_case(self, case_id: str, initial_data: dict) -> str:
        """Create a temporary file for case data persistence."""
        temp_file = os.path.join(self.base_temp_dir, f"{case_id}.json")

        # Initialize with core case data
        case_data = {
            "case_id": case_id,
            "iteration": 0,
            "complexity_level": 0,
            "core_data": initial_data,
            "generated_documents": [],
            "evidence_items": [],
            "consistency_registry": {
                "phone_numbers": [],
                "email_addresses": [],
                "ip_addresses": [],
                "vehicle_vins": [],
                "device_imeis": [],
                "social_handles": [],
                "bank_accounts": []
            },
            "narrative_elements": {},
            "relationships": {},
            "timestamps": {
                "created": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat()
            }
        }

        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(case_data, f, indent=2, default=str)

        self.temp_files[case_id] = temp_file
        return temp_file

    def update_case_data(self, case_id: str, updates: dict, iteration: int = None) -> dict:
        """Update case data in temp file and return current state."""
        temp_file = self.temp_files.get(case_id)
        if not temp_file or not os.path.exists(temp_file):
            raise FileNotFoundError(f"Temp file for case {case_id} not found")

        # Read current data
        with open(temp_file, 'r', encoding='utf-8') as f:
            case_data = json.load(f)

        # Update data
        for key, value in updates.items():
            if key in case_data:
                if isinstance(case_data[key], list) and isinstance(value, list):
                    case_data[key].extend(value)
                elif isinstance(case_data[key], dict) and isinstance(value, dict):
                    case_data[key].update(value)
                else:
                    case_data[key] = value

        # Update iteration and timestamp
        if iteration is not None:
            case_data["iteration"] = iteration
        case_data["timestamps"]["last_modified"] = datetime.now().isoformat()

        # Write back
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(case_data, f, indent=2, default=str)

        return case_data

    def get_case_data(self, case_id: str) -> dict:
        """Retrieve current case data from temp file."""
        temp_file = self.temp_files.get(case_id)
        if not temp_file or not os.path.exists(temp_file):
            raise FileNotFoundError(f"Temp file for case {case_id} not found")

        with open(temp_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def add_consistency_item(self, case_id: str, item_type: str, item_value: str):
        """Add an item to the consistency registry to ensure reuse across documents."""
        temp_file = self.temp_files.get(case_id)
        if not temp_file or not os.path.exists(temp_file):
            return

        with open(temp_file, 'r', encoding='utf-8') as f:
            case_data = json.load(f)

        if item_type not in case_data["consistency_registry"]:
            case_data["consistency_registry"][item_type] = []

        if item_value not in case_data["consistency_registry"][item_type]:
            case_data["consistency_registry"][item_type].append(item_value)

            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(case_data, f, indent=2, default=str)

    def get_consistency_items(self, case_id: str, item_type: str) -> List[str]:
        """Retrieve consistency items for reuse."""
        try:
            case_data = self.get_case_data(case_id)
            return case_data["consistency_registry"].get(item_type, [])
        except:
            return []

    def cleanup_case(self, case_id: str, archive: bool = False):
        """Clean up temp file for a case."""
        temp_file = self.temp_files.get(case_id)
        if temp_file and os.path.exists(temp_file):
            if archive:
                # Move to archive directory
                archive_dir = os.path.join(self.base_temp_dir, "archive")
                os.makedirs(archive_dir, exist_ok=True)
                archive_file = os.path.join(archive_dir, f"{case_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                os.rename(temp_file, archive_file)
            else:
                os.remove(temp_file)

        if case_id in self.temp_files:
            del self.temp_files[case_id]

    def cleanup_all(self, archive: bool = True):
        """Clean up all temp files."""
        for case_id in list(self.temp_files.keys()):
            self.cleanup_case(case_id, archive)


fake = Faker()

class EntityProfile:
    """Tracks attributes for document generators (officers, systems, AI, etc.)"""
    def __init__(self, entity_id: str, entity_type: str, name: str = None):
        self.entity_id = entity_id
        self.entity_type = entity_type  # "human", "automated", "ai"
        self.name = name or f"{entity_type}_{entity_id[:8]}"
        
        if entity_type == "human":
            # Human attributes
            self.intelligence = random.randint(60, 100)  # 60-100 (affects understanding)
            self.writing_skill = random.randint(50, 100)  # 50-100 (affects grammar/spelling)
            self.thoroughness = random.randint(40, 100)  # 40-100 (affects completeness)
            self.bias_level = random.randint(0, 50)  # 0-50 (affects objectivity)
            self.attention_to_detail = random.randint(30, 100)  # 30-100 (affects accuracy)
            self.typo_rate = max(0, 100 - self.writing_skill) / 100.0  # Higher typo rate for poor writers
            self.precision_score = (self.intelligence + self.writing_skill + self.thoroughness + self.attention_to_detail) / 4.0
        elif entity_type == "automated":
            # Automated system attributes
            self.data_corruption_rate = random.uniform(0.001, 0.01)  # 0.1% - 1% corruption
            self.completeness = random.uniform(0.85, 0.99)  # 85-99% complete
            self.precision_score = self.completeness * (1 - self.data_corruption_rate)
        elif entity_type == "ai":
            # AI system attributes
            self.completeness = random.uniform(0.90, 0.98)  # 90-98% complete
            self.data_accessibility = random.uniform(0.80, 0.95)  # 80-95% accessible
            self.precision_score = (self.completeness + self.data_accessibility) / 2.0
        
        # Store in case for consistency
        self.case_id = None
    
    def introduce_error(self, text: str, error_type: str = "auto") -> str:
        """Introduce realistic errors based on entity type and attributes."""
        if self.entity_type == "human":
            return self._human_errors(text)
        elif self.entity_type == "automated":
            return self._automated_errors(text)
        elif self.entity_type == "ai":
            return self._ai_errors(text)
        return text
    
    def _human_errors(self, text: str) -> str:
        """Introduce human errors: typos, misspellings, grammar mistakes."""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            # Skip headers and structured data
            if any(marker in line for marker in ['---', '===', '|', ':', 'Date:', 'Time:', 'ID:']):
                # Still might have typos in names/addresses
                if random.random() < self.typo_rate * 0.3:
                    line = self._introduce_typo(line)
                result.append(line)
                continue
            
            # Full line might have errors
            if random.random() < self.typo_rate:
                line = self._introduce_typo(line)
            
            # Grammar mistakes for low writing skill
            if self.writing_skill < 70 and random.random() < 0.1:
                line = self._introduce_grammar_error(line)
            
            result.append(line)
        
        return '\n'.join(result)
    
    def _introduce_typo(self, text: str) -> str:
        """Introduce common typos."""
        typos = {
            'the': 'teh', 'and': 'adn', 'with': 'wth', 'that': 'taht',
            'this': 'tihs', 'from': 'form', 'have': 'haev', 'were': 'weer',
            'their': 'thier', 'there': 'thre', 'they': 'tehy', 'said': 'saif',
            'would': 'woudl', 'could': 'coudl', 'should': 'shoudl'
        }
        
        words = text.split()
        if words and random.random() < 0.3:
            for i, word in enumerate(words):
                word_lower = word.lower()
                if word_lower in typos and random.random() < 0.3:
                    words[i] = typos[word_lower] if word.islower() else typos[word_lower].capitalize()
                    break
        
        return ' '.join(words)
    
    def _introduce_grammar_error(self, text: str) -> str:
        """Introduce grammar mistakes."""
        # Simple grammar errors
        if " is " in text.lower() and random.random() < 0.5:
            text = text.replace(" is ", " are ", 1)
        if " were " in text.lower() and random.random() < 0.5:
            text = text.replace(" were ", " was ", 1)
        return text
    
    def _automated_errors(self, text: str) -> str:
        """Introduce automated system errors: data corruption, missing fields."""
        if random.random() < self.data_corruption_rate:
            # Corrupt random character
            if len(text) > 10:
                pos = random.randint(0, len(text) - 1)
                text = text[:pos] + random.choice('0123456789ABCDEF') + text[pos+1:]
        
        # Missing data
        if random.random() > self.completeness:
            # Remove random line
            lines = text.split('\n')
            if len(lines) > 3:
                lines.pop(random.randint(1, len(lines) - 2))
                text = '\n'.join(lines)
        
        return text
    
    def _ai_errors(self, text: str) -> str:
        """Introduce AI system errors: incomplete data, accessibility issues."""
        # Missing information
        if random.random() > self.completeness:
            lines = text.split('\n')
            if len(lines) > 2:
                # Mark some data as inaccessible
                inaccessible = random.choice(lines[1:])
                if '|' in inaccessible:
                    parts = inaccessible.split('|')
                    if len(parts) > 1:
                        parts[-1] = '[DATA_NOT_ACCESSIBLE]'
                        lines[lines.index(inaccessible)] = '|'.join(parts)
                        text = '\n'.join(lines)
        
        return text
    
    def misspell_name(self, name: str) -> str:
        """Misspell a name based on attention to detail."""
        if self.attention_to_detail > 80:
            return name  # High attention = correct spelling
        
        # Common name misspellings
        misspellings = {
            'Smith': 'Smyth', 'Johnson': 'Johnsen', 'Williams': 'Williamson',
            'Brown': 'Browne', 'Jones': 'Joans', 'Garcia': 'Garica',
            'Miller': 'Millar', 'Davis': 'Davies', 'Rodriguez': 'Rodrigues',
            'Martinez': 'Martines', 'Hernandez': 'Hernandes', 'Lopez': 'Lopes'
        }
        
        for correct, wrong in misspellings.items():
            if correct in name and random.random() < (100 - self.attention_to_detail) / 100.0:
                return name.replace(correct, wrong)
        
        # Random character swap
        if len(name) > 3 and random.random() < 0.2:
            chars = list(name)
            i, j = random.sample(range(len(chars)), 2)
            chars[i], chars[j] = chars[j], chars[i]
            return ''.join(chars)
        
        return name
    
    def misread_plate(self, plate: str) -> str:
        """Misread license plate based on attention to detail."""
        if self.attention_to_detail > 85:
            return plate
        
        # Common misreads: 0/O, 1/I, 5/S, 8/B
        replacements = {'0': 'O', 'O': '0', '1': 'I', 'I': '1', '5': 'S', 'S': '5', '8': 'B', 'B': '8'}
        
        if random.random() < (100 - self.attention_to_detail) / 100.0:
            chars = list(plate)
            for i, char in enumerate(chars):
                if char in replacements and random.random() < 0.3:
                    chars[i] = replacements[char]
                    break
            return ''.join(chars)
        
        return plate

class CaseGenerator:
    def __init__(self):
        self.case = None
        self.temp_manager = TempFileManager()
        self.current_case_id = None
        self.entities = {}  # Track all entities (officers, systems, etc.)
        if not hasattr(self, 'entities'):
            self.entities = {}
        
        # Consistency managers (initialized in generate_case)
        self.jurisdiction_manager = None
        self.officer_registry = None
        self.entity_validator = None
        self.timeline_manager = None
        self.location_manager = None

    def generate_case(self, crime_type: str, complexity: str, modifiers: List[str], subject_status: str = "Known", subject_clarity: str = None) -> Case:
        """Generate a complete case with comprehensive error handling."""
        try:
            # 1. Timeline Anchor (Time Zero)
            date_opened = datetime.now()
            # Crime happened 3-14 days ago
            crime_dt = date_opened - timedelta(days=random.randint(3, 14), hours=random.randint(0,23))
            self.crime_datetime = crime_dt  # Store for later use
            case_id = generate_case_id()

            # Initialize narrative coherence tracking
            self.narrative_elements = {
                'crime_method': self._generate_crime_method(crime_type),
                'motivation': generate_motive(crime_type),
                'alibi_breakers': [],  # Evidence that breaks alibis
                'false_flags': [],     # Misleading evidence planted by suspects
                'hidden_connections': [], # Relationships not immediately obvious
                'timeline_events': []  # Key events in chronological order
            }

            self.subject_status = subject_status  # Known, Unknown, Partially Known
            self.case = Case(
                id=case_id,
                title=f"{crime_type} Investigation - {case_id}",
                description=f"Investigation into alleged {crime_type}.",
                crime_type=crime_type,
                complexity=complexity,
                date_opened=date_opened,
                modifiers=modifiers
            )

            # 2. Initialize consistency managers
            from .consistency_managers import (
                JurisdictionManager, OfficerRegistry, EntityValidator,
                TimelineManager, LocationManager
            )
            
            # Initialize jurisdiction manager (will be set after we know the location)
            self.jurisdiction_manager = JurisdictionManager()
            
            # Initialize officer registry (will be set after we know the department)
            self.officer_registry = OfficerRegistry(self.jurisdiction_manager.get_department())
            
            # Initialize entity validator
            self.entity_validator = EntityValidator()
            
            # Initialize timeline manager
            self.timeline_manager = TimelineManager(crime_dt)
            
            # Initialize location manager (will be set after we know the location)
            self.location_manager = LocationManager()
            
            # Initialize realistic error generator
            self.error_generator = RealisticErrorGenerator(crime_dt, complexity)
            
            # 3. Initialize entity system (officers, systems, etc.)
            self._initialize_entities(case_id)
            
            # 4. Populate World
            self._populate_people(complexity)
            
            # Register reporting officer with officer registry
            if self.case.reporting_officer:
                self.officer_registry.register_officer(
                    self.case.reporting_officer.full_name,
                    department=self.jurisdiction_manager.get_department()
                )
            
            # Register all persons with entity validator
            for person in self.case.persons:
                # Use person's gender if available, otherwise infer
                gender = person.gender if person.gender else ("male" if person.first_name.lower()[-1] in ['o', 'n', 'r', 's', 't', 'd', 'e'] else "female")
                
                self.entity_validator.register_entity(
                    person.full_name,
                    gender=gender,
                    age=person.age,
                    physical_description=person.physical_description,
                    address=person.address,
                    phone_number=person.phone_number,
                    height=person.height,
                    weight=person.weight,
                    hair_color=person.hair_color,
                    eye_color=person.eye_color,
                    facial_hair=person.facial_hair,
                    build=person.build,
                    driver_license_number=person.driver_license_number,
                    driver_license_state=person.driver_license_state
                )
            
            # Set primary location in location manager
            if self.case.incident_report and self.case.incident_report.incident_location:
                # Extract location info (simplified - would need proper parsing in production)
                location_parts = self.case.incident_report.incident_location.split(',')
                if len(location_parts) >= 2:
                    city = location_parts[-2].strip() if len(location_parts) >= 2 else fake.city()
                    state = location_parts[-1].strip() if len(location_parts) >= 1 else fake.state()
                else:
                    city = fake.city()
                    state = fake.state()
                
                lat = float(self.case.incident_report.latitude) if self.case.incident_report.latitude else 0.0
                lon = float(self.case.incident_report.longitude) if self.case.incident_report.longitude else 0.0
                
                self.location_manager.set_primary_location(
                    self.case.incident_report.incident_location,
                    city, state, lat, lon
                )
            
            self._assign_assets()
            self._establish_relationships()
            
            # Adjust for subject status and clarity approach
            if subject_status == "Unknown":
                if subject_clarity == "Investigative":
                    self._create_investigative_unknown_subjects()
                else:
                    self._make_subjects_unknown()
            elif subject_status == "Partially Known":
                if subject_clarity == "Investigative":
                    self._create_investigative_partial_subjects()
                else:
                    self._make_subjects_partial()
            elif subject_status == "Known":
                if subject_clarity == "Investigative":
                    self._create_investigative_known_subjects()

            # 3. Generate crime-type-specific documents FIRST (before generic ones)
            try:
                from .crime_specific_generators import CrimeSpecificGenerator
                crime_specific_gen = CrimeSpecificGenerator(self.case, crime_type, self.crime_datetime, self.entities)
                crime_specific_docs = crime_specific_gen.generate_crime_specific_documents(complexity, modifiers)
                if crime_specific_docs:
                    self.case.documents.extend(crime_specific_docs)
            except Exception as e:
                # If crime-specific generation fails, continue with generic
                pass
            
            # 4. Generate generic investigative documents (only if appropriate for crime type)
            self._generate_911_call()          # 911 dispatch transcript
            self._generate_cad_report()        # CAD incident report
            self._generate_incident_report()   # Formal incident report (now handles non-physical crimes)

            # 4. Evidence and warrants (if modifiers present)
            if modifiers:
                self._generate_evidence_and_warrants(modifiers)

            # 6. Surveillance and scene investigation (only for physical crimes)
            if self._should_generate_physical_evidence(crime_type):
                self._generate_cctv_surveillance() # CCTV logs
                self._generate_iot_evidence()      # Smart device logs

            # 6. Additional documents based on complexity
            if complexity == "High":
                self._generate_predictive_analytics()  # Predictive policing report
                if "Phone data pull" in modifiers or "IP logs" in modifiers:
                    self._generate_burner_phones(complexity)
            
            # 6.5. Cybercrime-specific bulk logs
            if crime_type == "Cybercrime":
                self._generate_bulk_cyber_logs()

            # 7. Data-heavy generators (if requested)
            if "Data-Heavy Phone Dump" in modifiers:
                self._generate_massive_phone_dump()
            if "Data-Heavy IP Logs" in modifiers:
                self._generate_massive_ip_logs()
            if "Data-Heavy Financial" in modifiers:
                self._generate_massive_financial_records()

            # 8. Generate ALPR hits (only for crimes with vehicles, 10-15% chance)
            if self._should_generate_physical_evidence(crime_type) and any(p.vehicles for p in self.case.persons if p.role == Role.SUSPECT):
                self._generate_alpr_hits()
            
            # 8.5. Generate random events (if modifier present)
            self._generate_random_events(modifiers)
            
            # 9. Inject hidden gems (subtle clues in junk data and patterns)
            if complexity == "High":
                self._inject_hidden_gems()

            # 10. Junk data (always generate, more for high complexity)
            self._generate_junk_data(complexity)
            if "Extra Junk Data" in modifiers:
                self._generate_extensive_junk_data()

            # 10. Lab and forensic reports
            self._generate_lab_reports()       # Lab analysis reports

            # 11. Administrative documents
            self._generate_discovery_package() # Discovery index
            
            # 12. Apply realistic errors and events to generated content
            self._apply_realistic_errors()
            
            # 13. Add error events summary to case
            error_summary = self.error_generator.get_events_summary()
            if error_summary:
                self.case.documents.append(error_summary)

            return self.case
        except Exception as e:
            print(f"❌ ERROR in generate_case: {e}")
            import traceback
            traceback.print_exc()
            # Return a minimal case rather than None to prevent crashes
            if hasattr(self, 'case') and self.case:
                return self.case
            # Create emergency fallback case (Case is already imported at top of file)
            return Case(
                id=case_id,
                title=f"{crime_type} Investigation - {case_id} (ERROR)",
                description=f"Investigation into alleged {crime_type}. Generation encountered errors.",
                crime_type=crime_type,
                complexity=complexity,
                date_opened=date_opened,
                modifiers=modifiers
            )

    def _initialize_entities(self, case_id: str):
        """Initialize entity profiles for officers, systems, AI, etc. and store in temp file."""
        # Create entity profiles for common document generators
        entities_data = {}
        
        # Generate officer profiles (will be created as needed, but pre-generate some)
        for i in range(random.randint(3, 8)):
            officer_id = f"officer_{fake.uuid4()}"
            officer_name = f"{fake.first_name()} {fake.last_name()}"
            entity = EntityProfile(officer_id, "human", officer_name)
            self.entities[officer_id] = entity
            entities_data[officer_id] = {
                "type": "human",
                "name": officer_name,
                "intelligence": entity.intelligence,
                "writing_skill": entity.writing_skill,
                "thoroughness": entity.thoroughness,
                "bias_level": entity.bias_level,
                "attention_to_detail": entity.attention_to_detail,
                "precision_score": entity.precision_score
            }
        
        # Generate automated system profiles
        systems = ["CAD", "ALPR", "CCTV", "EDR", "Fingerprint_Scanner", "DNA_Analyzer"]
        for system_name in systems:
            system_id = f"system_{system_name.lower()}"
            entity = EntityProfile(system_id, "automated", system_name)
            self.entities[system_id] = entity
            entities_data[system_id] = {
                "type": "automated",
                "name": system_name,
                "data_corruption_rate": entity.data_corruption_rate,
                "completeness": entity.completeness,
                "precision_score": entity.precision_score
            }
        
        # Generate AI system profiles
        ai_systems = ["Phone_Analyzer", "Network_Analyzer", "Financial_Analyzer"]
        for ai_name in ai_systems:
            ai_id = f"ai_{ai_name.lower()}"
            entity = EntityProfile(ai_id, "ai", ai_name)
            self.entities[ai_id] = entity
            entities_data[ai_id] = {
                "type": "ai",
                "name": ai_name,
                "completeness": entity.completeness,
                "data_accessibility": entity.data_accessibility,
                "precision_score": entity.precision_score
            }
        
        # Store in temp file for persistence
        try:
            self.temp_manager.update_case_data(case_id, {"entities": entities_data})
        except:
            pass  # Temp file might not exist yet
    
    def _get_or_create_entity(self, entity_id: str, entity_type: str, name: str = None) -> EntityProfile:
        """Get existing entity or create new one."""
        if entity_id in self.entities:
            return self.entities[entity_id]
        
        entity = EntityProfile(entity_id, entity_type, name)
        self.entities[entity_id] = entity
        return entity
    
    def _get_random_officer(self) -> EntityProfile:
        """Get a random officer entity, creating one if needed."""
        officers = [e for e in self.entities.values() if e.entity_type == "human"]
        if officers:
            return random.choice(officers)
        
        # Create new officer
        officer_id = f"officer_{fake.uuid4()}"
        officer_name = f"{fake.first_name()} {fake.last_name()}"
        return self._get_or_create_entity(officer_id, "human", officer_name)

    def _build_case_iteration(self, case_id: str, iteration: int, complexity: str, crime_type: str, modifiers: List[str], date_opened: datetime):
        """Build case complexity iteratively using temp file data."""

        # Read current case data from temp file
        case_data = self.temp_manager.get_case_data(case_id)
        crime_dt = datetime.fromisoformat(case_data["crime_datetime"])

        # Set instance variables for this iteration
        self.crime_datetime = crime_dt
        self.narrative_elements = case_data.get("narrative_elements", self.narrative_elements)

        # Iteration-based complexity building
        if iteration == 0:
            # Base case setup
            self._populate_people_base(case_id, complexity)
        elif iteration == 1:
            # Add relationships and assets
            self._populate_relationships(case_id, complexity)
            self._assign_assets_temp(case_id, complexity)
        elif iteration >= 2:
            # Add complexity layers
            self._add_complexity_layer(case_id, iteration, complexity, modifiers)

        # Update temp file with new iteration data
        updates = {
            "iteration": iteration,
            "complexity_level": iteration,
            "narrative_elements": self.narrative_elements,
            "timestamps": {"last_modified": datetime.now().isoformat()}
        }
        self.temp_manager.update_case_data(case_id, updates, iteration)

    def _populate_people_base(self, case_id: str, complexity: str):
        """Create initial people and store in temp file."""
        # Determine number of people based on complexity
        if complexity == "Low":
            num_suspects = 1
            num_victims = 1
            num_witnesses = 1
        elif complexity == "Medium":
            num_suspects = random.randint(1, 2)
            num_victims = random.randint(1, 2)
            num_witnesses = random.randint(2, 3)
        else:  # High
            num_suspects = random.randint(2, 3)
            num_victims = random.randint(1, 2)
            num_witnesses = random.randint(3, 5)

        people_data = []
        roles_assigned = []

        # Generate suspects
        for i in range(num_suspects):
            person = generate_person(Role.SUSPECT)
            person.id = f"SUSPECT_{i+1}"
            people_data.append({
                "id": person.id,
                "name": person.full_name,
                "role": person.role.value,
                "phone": person.phone_number,
                "email": person.email or f"{person.first_name.lower()}.{person.last_name.lower()}@example.com",
                "address": person.address,
                "personality": person.personality,
                "reliability_score": person.reliability_score
            })
            # Register consistency items
            self.temp_manager.add_consistency_item(case_id, "phone_numbers", person.phone_number)
            self.temp_manager.add_consistency_item(case_id, "email_addresses", person.email)
            roles_assigned.append(person)

        # Generate victims
        for i in range(num_victims):
            person = generate_person(Role.VICTIM)
            person.id = f"VICTIM_{i+1}"
            people_data.append({
                "id": person.id,
                "name": person.full_name,
                "role": person.role.value,
                "phone": person.phone_number,
                "email": person.email or f"{person.first_name.lower()}.{person.last_name.lower()}@example.com",
                "address": person.address,
                "personality": person.personality,
                "reliability_score": person.reliability_score
            })
            self.temp_manager.add_consistency_item(case_id, "phone_numbers", person.phone_number)
            self.temp_manager.add_consistency_item(case_id, "email_addresses", person.email)
            roles_assigned.append(person)

        # Generate witnesses
        for i in range(num_witnesses):
            person = generate_person(Role.WITNESS)
            person.id = f"WITNESS_{i+1}"
            people_data.append({
                "id": person.id,
                "name": person.full_name,
                "role": person.role.value,
                "phone": person.phone_number,
                "email": person.email or f"{person.first_name.lower()}.{person.last_name.lower()}@example.com",
                "address": person.address,
                "personality": person.personality,
                "reliability_score": person.reliability_score
            })
            self.temp_manager.add_consistency_item(case_id, "phone_numbers", person.phone_number)
            self.temp_manager.add_consistency_item(case_id, "email_addresses", person.email)
            roles_assigned.append(person)

        # Generate reporting officer
        officer = generate_person(Role.OFFICER)
        officer.id = "OFFICER_1"
        people_data.append({
            "id": officer.id,
            "name": officer.full_name,
            "role": officer.role.value,
            "phone": officer.phone_number,
            "email": officer.email or f"{officer.first_name.lower()}.{officer.last_name.lower()}@police.gov",
            "address": officer.address,
            "personality": officer.personality,
            "reliability_score": officer.reliability_score
        })

        # Update temp file with people data
        self.temp_manager.update_case_data(case_id, {"people": people_data})

    def _populate_relationships(self, case_id: str, complexity: str):
        """Add relationships between people."""
        case_data = self.temp_manager.get_case_data(case_id)
        people = case_data.get("people", [])

        relationships = {}

        # Create some basic relationships
        suspects = [p for p in people if p["role"] == "SUSPECT"]
        victims = [p for p in people if p["role"] == "VICTIM"]
        witnesses = [p for p in people if p["role"] == "WITNESS"]

        # Suspects might know each other
        for i, s1 in enumerate(suspects):
            for j, s2 in enumerate(suspects):
                if i != j and random.random() < 0.3:
                    relationships[f"{s1['id']}-{s2['id']}"] = "Acquaintance"

        # Witnesses might know victims
        for witness in witnesses:
            for victim in victims:
                if random.random() < 0.4:
                    relationships[f"{witness['id']}-{victim['id']}"] = "Neighbor" if random.random() < 0.5 else "Friend"

        self.temp_manager.update_case_data(case_id, {"relationships": relationships})

    def _assign_assets_temp(self, case_id: str, complexity: str):
        """Assign vehicles, devices, and other assets to people."""
        case_data = self.temp_manager.get_case_data(case_id)
        people = case_data.get("people", [])

        assets = {"vehicles": [], "devices": [], "accounts": []}

        for person in people:
            person_id = person["id"]

            # Assign vehicles (more for suspects in high complexity)
            if person["role"] == "SUSPECT" and complexity == "High":
                num_vehicles = random.randint(1, 2)
            elif person["role"] in ["SUSPECT", "VICTIM"]:
                num_vehicles = 1 if random.random() < 0.7 else 0
            else:
                num_vehicles = 1 if random.random() < 0.3 else 0

            for i in range(num_vehicles):
                vehicle = generate_vehicle(person_id, person["address"])
                assets["vehicles"].append({
                    "id": vehicle.id,
                    "owner_id": person_id,
                    "make": vehicle.make,
                    "model": vehicle.model,
                    "color": vehicle.color,
                    "year": vehicle.year,
                    "license_plate": vehicle.license_plate,
                    "vin": vehicle.vin
                })
                self.temp_manager.add_consistency_item(case_id, "vehicle_vins", vehicle.vin)

            # Assign devices
            num_devices = random.randint(1, 3) if person["role"] != "OFFICER" else 1
            for i in range(num_devices):
                device = generate_device(person_id)
                assets["devices"].append({
                    "id": device.id,
                    "owner_id": person_id,
                    "type": device.device_type,
                    "make": device.make,
                    "model": device.model,
                    "imei": device.imei,
                    "phone_number": device.phone_number,
                    "ip_address": device.ip_address,
                    "mac_address": device.mac_address
                })
                if device.imei:
                    self.temp_manager.add_consistency_item(case_id, "device_imeis", device.imei)
                if device.ip_address:
                    self.temp_manager.add_consistency_item(case_id, "ip_addresses", device.ip_address)

            # Assign bank accounts for suspects/victims
            if person["role"] in ["SUSPECT", "VICTIM"] and random.random() < 0.8:
                num_accounts = random.randint(1, 3)
                for i in range(num_accounts):
                    account = fake.iban()
                    assets["accounts"].append({
                        "id": f"ACCOUNT_{person_id}_{i+1}",
                        "owner_id": person_id,
                        "iban": account,
                        "balance": random.randint(500, 50000)
                    })
                    self.temp_manager.add_consistency_item(case_id, "bank_accounts", account)

        self.temp_manager.update_case_data(case_id, {"assets": assets})

    def _add_complexity_layer(self, case_id: str, iteration: int, complexity: str, modifiers: List[str]):
        """Add additional complexity layers in later iterations."""
        case_data = self.temp_manager.get_case_data(case_id)

        # Add aliases for suspects (iteration 2+)
        if iteration >= 2:
            people = case_data.get("people", [])
            for person in people:
                if person["role"] == "SUSPECT" and random.random() < 0.6:
                    alias = fake.name()
                    if "aliases" not in person:
                        person["aliases"] = []
                    person["aliases"].append(alias)

            self.temp_manager.update_case_data(case_id, {"people": people})

        # Add social media for higher iterations
        if iteration >= 3 and complexity == "High":
            people = case_data.get("people", [])
            for person in people:
                if person["role"] != "OFFICER" and random.random() < 0.7:
                    handle = f"@{person['name'].lower().replace(' ', '_')}_{random.randint(100, 999)}"
                    person["social_handle"] = handle
                    self.temp_manager.add_consistency_item(case_id, "social_handles", handle)

            self.temp_manager.update_case_data(case_id, {"people": people})

    def _generate_final_documents(self, case_id: str):
        """Generate final documents using the enriched temp data."""
        case_data = self.temp_manager.get_case_data(case_id)

        # Load case data for document generation
        people = case_data.get("people", [])
        assets = case_data.get("assets", {})
        relationships = case_data.get("relationships", {})

        # Convert to objects for document generation
        self.case = Case(
            id=case_id,
            title=f"Investigation - {case_id}",
            description="Generated case",
            crime_type=case_data["crime_type"],
            complexity=case_data["complexity"],
            date_opened=datetime.fromisoformat(case_data["date_opened"]),
            modifiers=case_data["modifiers"]
        )

        # Set crime datetime
        self.crime_datetime = datetime.fromisoformat(case_data["crime_datetime"])

        # Generate documents using the enriched data
        self._generate_911_call()
        self._generate_cad_report()
        self._generate_incident_report()

        if case_data["modifiers"]:
            self._generate_evidence_and_warrants(case_data["modifiers"])

        self._generate_cctv_surveillance()
        self._generate_iot_evidence()

        if case_data["complexity"] == "High":
            self._generate_predictive_analytics()
            if "Phone data pull" in case_data["modifiers"] or "IP logs" in case_data["modifiers"]:
                self._generate_burner_phones(case_data["complexity"])

        self._generate_lab_reports()
        self._generate_discovery_package()

        # Store documents and evidence in temp file
        self.temp_manager.update_case_data(case_id, {
            "generated_documents": self.case.documents,
            "evidence_items": self.case.evidence
        })

    def _generate_crime_method(self, crime_type: str) -> str:
        """Generate a specific crime method that will be referenced consistently."""
        methods = {
            "Murder": ["Poisoning", "Stabbing", "Shooting", "Strangulation", "Blunt Force Trauma", "Arson"],
            "Assault": ["Physical Attack", "Weapon Assault", "Robbery with Violence", "Home Invasion"],
            "Robbery": ["Armed Robbery", "Burglary", "ATM Skimming", "Business Robbery", "Street Mugging"],
            "Burglary": ["Forced Entry", "Lock Picking", "Window Entry", "Safe Cracking", "Digital Lock Bypass"],
            "Theft": ["Shoplifting", "Pickpocketing", "Car Theft", "Identity Theft", "Credit Card Fraud"],
            "Cybercrime": ["SQL Injection", "Phishing Attack", "Ransomware", "Data Breach", "Malware Infection", "DDoS Attack"],
            "Financial Crimes": ["Money Laundering", "Wire Fraud", "Tax Evasion", "Ponzi Scheme", "Embezzlement"],
            "Drug Related": ["Drug Trafficking", "Manufacturing", "Distribution", "Possession with Intent"],
            "Fraud": ["Insurance Fraud", "Investment Scam", "Online Fraud", "Identity Fraud", "Check Fraud"]
        }
        return random.choice(methods.get(crime_type, ["Unknown Method"]))

    def _generate_alibi(self, suspect) -> str:
        """Generate a believable alibi for a suspect."""
        alibis = [
            f"At home watching TV, alone",
            f"At work until {random.randint(18, 22)}:00",
            f"Out with friends at {fake.company()} bar",
            f"Visiting family in {fake.city()}",
            f"Grocery shopping at {fake.company()} Supermarket",
            f"At the gym working out",
            f"Driving to {fake.city()} for business",
            f"Home sick with flu symptoms",
            f"At a movie theater watching {fake.catch_phrase()}",
            f"Walking the dog in {fake.street_name()} park"
        ]
        return random.choice(alibis)

    def _generate_alibi_breaker(self, suspect, alibi: str) -> dict:
        """Generate evidence that breaks a suspect's alibi."""
        breakers = {
            "At home watching TV, alone": {
                "evidence": f"Security camera footage shows suspect leaving home at {self.crime_datetime.strftime('%H:%M')}",
                "type": "Video Footage",
                "location": f"Neighbor's Ring Camera - {fake.street_name()}"
            },
            "At work until": {
                "evidence": f"Work badge scan shows suspect left early at {(self.crime_datetime - timedelta(hours=1)).strftime('%H:%M')}",
                "type": "Digital Log",
                "location": f"Employer Security System - {fake.company()}"
            },
            "Out with friends": {
                "evidence": f"Credit card charge at {fake.company()} shows suspect was 15 miles from bar",
                "type": "Financial Record",
                "location": f"Bank Transaction - {fake.company()} Bank"
            },
            "Visiting family": {
                "evidence": f"Cell phone pings show suspect's phone in city center, not family residence",
                "type": "Cell Tower Data",
                "location": f"Phone Carrier Records - {suspect.phone_number}"
            },
            "Grocery shopping": {
                "evidence": f"Store surveillance shows suspect entered store but left after 2 minutes",
                "type": "CCTV Footage",
                "location": f"Store Security - {fake.company()} Supermarket"
            },
            "At the gym": {
                "evidence": f"Gym check-in records show suspect signed out 30 minutes before incident",
                "type": "Digital Log",
                "location": f"Fitness Center Records - {fake.company()} Gym"
            },
            "Driving for business": {
                "evidence": f"Vehicle GPS data shows suspect's car parked near crime scene",
                "type": "GPS Data",
                "location": f"Vehicle Telematics - {suspect.vehicles[0].license_plate if suspect.vehicles else 'Unknown Vehicle'}"
            },
            "Home sick": {
                "evidence": f"Neighbor witnessed suspect loading items into vehicle at {self.crime_datetime.strftime('%H:%M')}",
                "type": "Witness Statement",
                "location": f"Neighbor Interview - {fake.street_name()}"
            },
            "At a movie theater": {
                "evidence": f"Theater ticket scan shows suspect entered theater but concession purchase shows they left early",
                "type": "Digital Record",
                "location": f"Theater POS System - {fake.company()} Cinemas"
            },
            "Walking the dog": {
                "evidence": f"No dog registered to suspect's address, and suspect doesn't own pets",
                "type": "Public Records",
                "location": f"Veterinary Clinic Records - {fake.company()}"
            }
        }

        # Find matching breaker or use generic
        for key, breaker in breakers.items():
            if key in alibi:
                return breaker

        # Generic breaker
        return {
            "evidence": f"Witness places suspect at location inconsistent with stated alibi",
            "type": "Witness Testimony",
            "location": f"Third-party Interview - {fake.name()}"
        }

    def _generate_false_flag(self) -> dict:
        """Generate misleading evidence planted by suspect."""
        false_flags = [
            {
                "description": "Suspicious item planted at crime scene",
                "item": random.choice(["Bloody glove", "Suspicious note", "Fake ID", "Burner phone", "Blood-stained clothing"]),
                "purpose": "Frame another person",
                "planted_by": "Suspect",
                "discovery_clue": "DNA analysis shows item belongs to different person"
            },
            {
                "description": "Fake digital footprint created",
                "item": random.choice(["Phony social media post", "Fake email trail", "GPS spoofing", "Alibi phone call"]),
                "purpose": "Create false timeline",
                "planted_by": "Suspect",
                "discovery_clue": "Digital metadata shows creation time after incident"
            },
            {
                "description": "Witness intimidation or bribery",
                "item": random.choice(["Threatening letter", "Cash payment", "Altered testimony"]),
                "purpose": "Silence witness",
                "planted_by": "Accomplice",
                "discovery_clue": "Financial records show suspicious transactions"
            },
            {
                "description": "Evidence tampering",
                "item": random.choice(["Altered security footage", "Deleted logs", "Contaminated DNA sample"]),
                "purpose": "Destroy evidence",
                "planted_by": "Suspect",
                "discovery_clue": "Digital forensics recover deleted data"
            }
        ]
        return random.choice(false_flags)

    # --- POPULATION & ASSETS ---

    def _populate_people(self, complexity: str):
        officer = generate_person(Role.OFFICER, 25, 55)
        self.case.reporting_officer = officer
        self.case.add_person(officer)

        counts = {"Low": (1, 1, 1), "Medium": (2, 1, 2), "High": (3, 2, 4)}
        n_susp, n_vict, n_wit = counts.get(complexity, (1, 1, 1))

        for _ in range(n_susp): 
            s = generate_person(Role.SUSPECT)
            s.motive = generate_motive(self.case.crime_type)
            self.case.add_person(s)
        for _ in range(n_vict): self.case.add_person(generate_person(Role.VICTIM))
        for _ in range(n_wit): self.case.add_person(generate_person(Role.WITNESS))

    def _assign_assets(self):
        for person in self.case.persons:
            if person.role in [Role.SUSPECT, Role.VICTIM] and person.age > 16:
                # Vehicles: Suspects almost always have one for getaway logic
                if person.role == Role.SUSPECT or random.random() < 0.7:
                    vehicle = generate_vehicle(person.id, person.address)
                    person.vehicles.append(vehicle)
                
                # Phones
                dev = generate_device(person.id, "Phone")
                person.phone_number = dev.phone_number
                person.devices.append(dev)
                
                # Emails/Bank
                person.email = f"{person.first_name.lower()}.{person.last_name.lower()}@{fake.free_email_domain()}"
                person.bank_accounts.append(fake.iban())
                
                # Weapons for violent crimes
                is_violent = any(x in self.case.crime_type for x in ["Murder", "Assault", "Robbery", "Shooting"])
                if is_violent and person.role == Role.SUSPECT:
                    weapon = generate_weapon(person.id)
                    person.weapons.append(weapon)

    def _establish_relationships(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        victims = [p for p in self.case.persons if p.role == Role.VICTIM]
        witnesses = [p for p in self.case.persons if p.role == Role.WITNESS]

        # Complex relationship network
        if len(suspects) > 1:
            for i in range(len(suspects) - 1):
                s1, s2 = suspects[i], suspects[i+1]
                rel = random.choice(["Accomplice", "Rival", "Former Partner", "Family Member", "Business Associate", "Romantic Partner", "Drug Supplier"])
                s1.relationships[s2.id] = rel
                s2.relationships[s1.id] = rel

                # Hidden connections for AI challenge
                if random.random() < 0.3 and self.case.complexity == "High":
                    hidden_rel = random.choice(["Secret Business Partner", "Blackmail Target", "Debt Owed", "Shared Criminal Past"])
                    self.narrative_elements['hidden_connections'].append({
                        'party1': s1.id,
                        'party2': s2.id,
                        'relationship': hidden_rel,
                        'evidence_needed': random.choice(["Financial Records", "Phone Calls", "Witness Testimony", "Digital Footprints"])
                    })

        # Generate alibis and potential alibi breakers
        for suspect in suspects:
            alibi = self._generate_alibi(suspect)
            suspect.notes += f" Alibi: {alibi}"

            # High complexity: create evidence that breaks alibis
            if self.case.complexity == "High" and random.random() < 0.4:
                breaker = self._generate_alibi_breaker(suspect, alibi)
                self.narrative_elements['alibi_breakers'].append(breaker)

        # False flags for misdirection
        if self.case.complexity == "High":
            num_false_flags = random.randint(1, 3)
            for _ in range(num_false_flags):
                false_flag = self._generate_false_flag()
                self.narrative_elements['false_flags'].append(false_flag)

    # --- HIDDEN GEMS (NEEDLE IN HAYSTACK) ---
    
    def _inject_hidden_gems(self):
        """Inject subtle clues and patterns that require AI analysis to discover.
        
        Hidden gems include:
        - VPN drop revealing real location in IP logs
        - Scamming operation patterns in phone logs (victims vs associates)
        - Cross-document consistency (phone numbers, addresses in junk data)
        - EXIF/geotag data in corrupted file logs
        - Temporal patterns (weather matching witness statements)
        - Contact pattern analysis (associates vs victims)
        - Metadata breadcrumbs (timestamps, hashes, coordinates)
        """
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        victims = [p for p in self.case.persons if p.role == Role.VICTIM]
        if not suspects: return
        
        # Store hidden gems for injection into junk data and logs
        self.hidden_gems = {
            'suspect_phone': suspects[0].phone_number if suspects[0].phone_number else None,
            'suspect_address': suspects[0].address,
            'suspect_vehicle': suspects[0].vehicles[0].license_plate if suspects[0].vehicles else None,
            'suspect_email': suspects[0].email if suspects[0].email else None,
            'victim_phones': [v.phone_number for v in victims if v.phone_number],
            'associate_phones': [],  # Will be populated
            'real_location': None,  # Will be set when VPN drops
            'crime_location': None,  # Crime scene location
            'trip_dates': [],  # Dates showing planned trip
            'exif_coords': None,  # GPS coordinates from EXIF
            'scam_victim_numbers': [],  # Numbers that are victims (longer calls during specific period)
            'scam_associate_numbers': [],  # Numbers that are associates (short, frequent calls)
            'vpn_drop_time': None,  # When VPN dropped revealing real IP
            'real_ip': None  # Real IP address (not VPN)
        }
        
        # Get crime location
        if self.case.incident_report:
            self.hidden_gems['crime_location'] = self.case.incident_report.incident_location
        
        # Identify associates (other suspects or people with relationships)
        for suspect in suspects:
            for rel_id, rel_type in suspect.relationships.items():
                other_person = next((p for p in self.case.persons if p.id == rel_id), None)
                if other_person and other_person.phone_number:
                    self.hidden_gems['associate_phones'].append(other_person.phone_number)
        
        # Generate real location (where suspect actually is, revealed by VPN drop)
        suspect_lat = getattr(suspects[0], 'latitude', None)
        suspect_lon = getattr(suspects[0], 'longitude', None)
        if suspect_lat and suspect_lon:
            self.hidden_gems['real_location'] = (suspect_lat, suspect_lon)
        else:
            # Generate a location near the crime scene
            crime_lat, crime_lon = geo_mgr.get_random_city_location()
            self.hidden_gems['real_location'] = geo_mgr.get_coords_in_radius(crime_lat, crime_lon, 50.0)
        
        # Generate trip dates (3-5 days before crime, showing planning)
        trip_start = self.crime_datetime - timedelta(days=random.randint(3, 5))
        trip_end = trip_start + timedelta(days=random.randint(2, 4))
        self.hidden_gems['trip_dates'] = (trip_start, trip_end)
        
        # Generate EXIF coordinates (near crime scene but slightly different)
        exif_lat, exif_lon = geo_mgr.get_coords_in_radius(
            self.hidden_gems['real_location'][0] if self.hidden_gems['real_location'] else geo_mgr.center_lat,
            self.hidden_gems['real_location'][1] if self.hidden_gems['real_location'] else geo_mgr.center_lon,
            2.0
        )
        self.hidden_gems['exif_coords'] = (exif_lat, exif_lon)
        
        # Generate scam victim and associate phone numbers
        # Victims: 5-10 numbers that get longer calls during specific period
        # Associates: 3-7 numbers that get short, frequent calls throughout
        for _ in range(random.randint(5, 10)):
            self.hidden_gems['scam_victim_numbers'].append(fake.phone_number())
        for _ in range(random.randint(3, 7)):
            self.hidden_gems['scam_associate_numbers'].append(fake.phone_number())
        
        # Generate VPN drop time (moment when VPN disconnected, revealing real IP)
        self.hidden_gems['vpn_drop_time'] = self.crime_datetime - timedelta(hours=random.randint(2, 12))
        self.hidden_gems['real_ip'] = generate_ip()  # Real IP (not VPN)

    # --- NOISE GENERATORS (JUNK DATA) ---

    def _generate_junk_data(self, complexity):
        """Injects irrelevant documents to test analyst filtering."""
        num_junk = {"Low": 3, "Medium": 5, "High": 8}.get(complexity, 5)
        
        junk_types = [
            self._generate_unrelated_parking_ticket,
            self._generate_department_memo,
            self._generate_corrupted_file_log,
            self._generate_unrelated_911_call,
            self._generate_traffic_citation,
            self._generate_weather_report,
            self._generate_shift_roster,
            self._generate_equipment_maintenance_log,
            self._generate_unrelated_witness_statement,
            self._generate_old_case_file,
            self._generate_media_request,
            self._generate_unrelated_arrest_report
        ]
        
        for _ in range(num_junk):
            generator = random.choice(junk_types)
            try:
                generator()
            except:
                pass  # Skip if generator fails
    
    def _generate_extensive_junk_data(self):
        """Generate massive amounts of junk data for filtering challenge."""
        for _ in range(random.randint(15, 25)):
            self._generate_junk_data("High")
    
    def _generate_unrelated_parking_ticket(self):
        doc = f"""--- PARKING CITATION ---
Citation #: PC-{fake.random_number(digits=8)}
Date: {(self.case.date_opened - timedelta(days=random.randint(5, 30))).strftime('%Y-%m-%d')}
Time: {random.randint(8, 18)}:{random.randint(0, 59):02d}
Location: {fake.street_address()}
Vehicle: {random.choice(['Silver Honda Civic', 'Blue Toyota Camry', 'Red Ford F-150', 'White Nissan Altima'])}
License Plate: {fake.license_plate()}
Violation: {random.choice(['Expired Meter', 'No Parking Zone', 'Handicap Zone', 'Fire Lane'])}
Fine: ${random.randint(25, 150)}.00
Officer: {fake.first_name()} {fake.last_name()[0]}.
Status: PAID
"""
        self.case.documents.append(doc)
    
    def _generate_department_memo(self):
        doc = f"""--- DEPARTMENT MEMO ---
FROM: Captain {fake.last_name()}
TO: All Personnel
DATE: {(self.case.date_opened - timedelta(days=random.randint(1, 10))).strftime('%Y-%m-%d')}
SUBJECT: {random.choice(['Overtime Sheets', 'Equipment Return', 'Training Mandate', 'Policy Update', 'Budget Cuts', 'Holiday Schedule'])}
{random.choice([
    'All OT sheets for the pay period must be submitted by Friday. No exceptions.',
    'Please return all issued equipment to the armory by end of shift.',
    'Mandatory training session scheduled for next Tuesday at 1400 hours.',
    'New policy regarding body camera usage effective immediately.',
    'Budget constraints require reduction in overtime authorization.',
    'Holiday schedule posted. Sign up sheets available in break room.'
])}
"""
        self.case.documents.append(doc)
    
    def _generate_corrupted_file_log(self):
        """Generate corrupted file log, sometimes with hidden EXIF data."""
        # 30% chance to inject hidden EXIF data
        has_hidden_exif = hasattr(self, 'hidden_gems') and random.random() < 0.3
        
        if has_hidden_exif and self.hidden_gems.get('exif_coords'):
            lat, lon = self.hidden_gems['exif_coords']
            exif_date = (self.crime_datetime - timedelta(days=random.randint(1, 3))).strftime('%Y:%m:%d %H:%M:%S')
            doc = f"""--- DATA RECOVERY LOG ---
File: evidence_img_{random.randint(1, 50):02d}.jpg
Sector: {random.randint(10000, 99999)}
Status: CORRUPTED / UNREADABLE HEADER
Action: Recovery Failed
Attempted Methods: {random.choice(['File carving', 'Hex analysis', 'Header reconstruction'])}
Result: Unable to recover image data

PARTIAL METADATA RECOVERED (FRAGMENTED):
- File Type: JPEG
- Camera: {random.choice(['Canon EOS 5D', 'Nikon D850', 'Sony Alpha 7'])}
- Date Taken: {exif_date}
- GPS Coordinates: {lat:.6f}, {lon:.6f} (RECOVERED FROM EXIF)
- GPS Altitude: {random.randint(100, 500)} meters
- Camera Settings: ISO {random.randint(100, 1600)}, f/{random.choice(['2.8', '4.0', '5.6'])}, 1/{random.randint(60, 500)}s

Note: Image data unrecoverable, but EXIF metadata partially extracted.
Technician: {fake.first_name()} {fake.last_name()}
Date: {(self.case.date_opened - timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d')}
"""
        else:
            doc = f"""--- DATA RECOVERY LOG ---
File: evidence_img_{random.randint(1, 50):02d}.jpg
Sector: {random.randint(10000, 99999)}
Status: CORRUPTED / UNREADABLE HEADER
Action: Recovery Failed
Attempted Methods: {random.choice(['File carving', 'Hex analysis', 'Header reconstruction'])}
Result: Unable to recover image data
Technician: {fake.first_name()} {fake.last_name()}
Date: {(self.case.date_opened - timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d')}
"""
        self.case.documents.append(doc)
    
    def _generate_unrelated_911_call(self):
        """Generate 911 call log, sometimes with hidden suspect phone number."""
        # 20% chance to inject suspect phone number
        has_hidden_phone = hasattr(self, 'hidden_gems') and self.hidden_gems.get('suspect_phone') and random.random() < 0.2
        
        if has_hidden_phone:
            caller_phone = self.hidden_gems['suspect_phone']
        else:
            caller_phone = fake.phone_number()
        
        # Get officer entity
        officer = self._get_random_officer()
        caller_name = fake.name()
        # Officer might misspell caller name
        caller_name = officer.misspell_name(caller_name)
        
        doc = f"""--- 911 CALL LOG ---
Call #: {fake.random_number(digits=8)}
Date: {(self.case.date_opened - timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d %H:%M:%S')}
Caller: {caller_name}
Caller Phone: {caller_phone}
Location: {fake.address().replace(chr(10), ', ')}
Nature: {random.choice(['Noise Complaint', 'Suspicious Person', 'Animal Control', 'Traffic Accident', 'Medical Emergency'])}
Disposition: {random.choice(['Referred to Animal Control', 'No action needed', 'Report taken', 'False alarm'])}
Officer: {officer.name}
"""
        
        # Apply officer errors
        doc = officer.introduce_error(doc)
        self.case.documents.append(doc)
    
    def _generate_traffic_citation(self):
        """Generate traffic citation, sometimes with suspect vehicle/license plate."""
        # 1-2% chance to inject suspect vehicle info (traffic stop)
        has_hidden_vehicle = hasattr(self, 'hidden_gems') and self.hidden_gems.get('suspect_vehicle') and random.random() < random.uniform(0.01, 0.02)
        
        if has_hidden_vehicle:
            license_plate = self.hidden_gems['suspect_vehicle']
            # Use suspect's vehicle make/model if available
            suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
            if suspects and suspects[0].vehicles:
                vehicle = suspects[0].vehicles[0]
                vehicle_desc = f"{vehicle.color} {vehicle.make} {vehicle.model}"
            else:
                vehicle_desc = random.choice(['Black BMW 3 Series', 'White Ford Explorer', 'Silver Toyota Corolla'])
        else:
            license_plate = fake.license_plate()
            vehicle_desc = random.choice(['Black BMW 3 Series', 'White Ford Explorer', 'Silver Toyota Corolla'])
        
        # Sometimes put citation near crime location
        if hasattr(self, 'hidden_gems') and self.hidden_gems.get('crime_location') and random.random() < 0.3:
            # Extract street name from crime location if possible
            location = self.hidden_gems['crime_location']
            street1 = fake.street_name()
            street2 = fake.street_name()
        else:
            street1 = fake.street_name()
            street2 = fake.street_name()
        
        # Get officer entity for citation
        officer = self._get_random_officer()
        
        # Officer might misread plate
        plate_read = license_plate
        if has_hidden_vehicle:
            plate_read = officer.misread_plate(license_plate)
        
        # Officer might misspell vehicle owner name if available
        vehicle_owner_name = ""
        if has_hidden_vehicle and suspects and suspects[0]:
            vehicle_owner_name = suspects[0].full_name
            vehicle_owner_name = officer.misspell_name(vehicle_owner_name)
        
        doc = f"""--- TRAFFIC CITATION ---
Citation #: TC-{fake.random_number(digits=8)}
Date: {(self.case.date_opened - timedelta(days=random.randint(1, 20))).strftime('%Y-%m-%d')}
Time: {random.randint(6, 22)}:{random.randint(0, 59):02d}
Location: {street1} & {street2}
Vehicle: {vehicle_desc}
License: {plate_read}
"""
        if vehicle_owner_name:
            doc += f"Registered Owner: {vehicle_owner_name}\n"
        doc += f"""Violation: {random.choice(['Speeding 15+ over', 'Red Light Violation', 'Improper Lane Change', 'No Insurance'])}
Fine: ${random.randint(100, 500)}.00
Officer: {officer.name}
"""
        
        # Apply officer errors
        doc = officer.introduce_error(doc)
        self.case.documents.append(doc)
    
    def _generate_weather_report(self):
        """Generate weather report, sometimes matching crime date conditions."""
        # 25% chance to match crime date weather (subtle clue)
        match_crime_date = hasattr(self, 'crime_datetime') and random.random() < 0.25
        
        if match_crime_date:
            report_date = self.crime_datetime.strftime('%Y-%m-%d')
            # Use same weather conditions as incident report if available
            if self.case.incident_report and self.case.incident_report.weather_condition:
                conditions = self.case.incident_report.weather_condition
            else:
                conditions = random.choice(['Clear', 'Partly Cloudy', 'Rain', 'Fog', 'Snow'])
        else:
            report_date = self.case.date_opened.strftime('%Y-%m-%d')
            conditions = random.choice(['Clear', 'Partly Cloudy', 'Rain', 'Fog', 'Snow'])
        
        doc = f"""--- WEATHER SERVICE REPORT ---
Date: {report_date}
Location: {fake.city()}, {fake.state_abbr()}
Conditions: {conditions}
Temperature: {random.randint(20, 85)}F
Wind: {random.randint(5, 25)} mph {random.choice(['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW'])}
Humidity: {random.randint(30, 90)}%
Visibility: {random.randint(1, 10)} miles
Forecast: {random.choice(['Sunny', 'Cloudy', 'Chance of rain', 'Clear skies'])}
"""
        self.case.documents.append(doc)
    
    def _generate_shift_roster(self):
        doc = f"""--- SHIFT ROSTER ---
Date: {self.case.date_opened.strftime('%Y-%m-%d')}
Shift: {random.choice(['Day', 'Evening', 'Night'])}
Supervisor: Sergeant {fake.last_name()}
Officers Assigned:
"""
        for _ in range(random.randint(5, 10)):
            doc += f"  - Officer {fake.first_name()} {fake.last_name()[0]}. (Badge #{fake.random_number(digits=4)})\n"
        doc += f"Total Officers: {random.randint(5, 10)}\n"
        self.case.documents.append(doc)
    
    def _generate_equipment_maintenance_log(self):
        doc = f"""--- EQUIPMENT MAINTENANCE LOG ---
Equipment: {random.choice(['Patrol Vehicle #415', 'Body Camera #BC-23', 'Radio Unit #R-45', 'Computer Terminal #CT-12'])}
Date: {(self.case.date_opened - timedelta(days=random.randint(1, 14))).strftime('%Y-%m-%d')}
Issue: {random.choice(['Routine maintenance', 'Battery replacement', 'Software update', 'Cleaning', 'Calibration'])}
Technician: {fake.first_name()} {fake.last_name()}
Status: {random.choice(['Completed', 'In Progress', 'Pending Parts'])}
Cost: ${random.randint(50, 500)}.00
"""
        self.case.documents.append(doc)
    
    def _generate_unrelated_witness_statement(self):
        # Get officer entity
        officer = self._get_random_officer()
        witness_name = fake.name()
        # Officer might misspell witness name
        witness_name = officer.misspell_name(witness_name)
        
        doc = f"""--- WITNESS STATEMENT ---
Case #: CASE-{fake.random_number(digits=6)}
Date: {(self.case.date_opened - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')}
Witness: {witness_name}
Statement: Witness observed {random.choice(['a traffic accident', 'suspicious activity', 'a noise disturbance', 'vandalism'])} at {fake.address().replace(chr(10), ', ')}.
Officer: {officer.name}
Status: Filed
"""
        
        # Apply officer errors
        doc = officer.introduce_error(doc)
        self.case.documents.append(doc)
    
    def _generate_old_case_file(self):
        doc = f"""--- CASE FILE (CLOSED) ---
Case #: CASE-{fake.random_number(digits=6)}
Type: {random.choice(['Theft', 'Vandalism', 'Trespassing', 'Disorderly Conduct'])}
Date Opened: {(self.case.date_opened - timedelta(days=random.randint(60, 365))).strftime('%Y-%m-%d')}
Date Closed: {(self.case.date_opened - timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d')}
Status: {random.choice(['Closed - No Suspect', 'Closed - Prosecuted', 'Closed - Insufficient Evidence'])}
Officer: {fake.first_name()} {fake.last_name()[0]}.
Notes: Case file archived.
"""
        self.case.documents.append(doc)
    
    def _generate_media_request(self):
        doc = f"""--- MEDIA REQUEST ---
Request #: MR-{fake.random_number(digits=6)}
Date: {(self.case.date_opened - timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d')}
Requestor: {fake.company()} News
Request: {random.choice(['Public records request', 'Press release', 'Interview request', 'Photo request'])}
Subject: {random.choice(['General crime statistics', 'Traffic safety', 'Community outreach', 'Department policies'])}
Status: {random.choice(['Pending', 'Approved', 'Denied'])}
Handled By: {fake.first_name()} {fake.last_name()}
"""
        self.case.documents.append(doc)
    
    def _generate_unrelated_arrest_report(self):
        # Get officer entity
        officer = self._get_random_officer()
        suspect_name = fake.name()
        # Officer might misspell suspect name
        suspect_name = officer.misspell_name(suspect_name)
        
        doc = f"""--- ARREST REPORT ---
Arrest #: AR-{fake.random_number(digits=8)}
Date: {(self.case.date_opened - timedelta(days=random.randint(1, 14))).strftime('%Y-%m-%d')}
Suspect: {suspect_name}
Charges: {random.choice(['DUI', 'Public Intoxication', 'Disorderly Conduct', 'Trespassing'])}
Location: {fake.address().replace(chr(10), ', ')}
Officer: {officer.name}
Status: {random.choice(['Booked', 'Released on Citation', 'Transported to Jail'])}

"""
        
        # Apply officer errors
        doc = officer.introduce_error(doc)
        self.case.documents.append(doc)

    def _generate_bulk_cyber_logs(self):
        """Generates massive log files with hidden clues for cybercrime cases."""
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return

        suspect = suspects[0]
        target_ip = suspect.devices[0].ip_address if suspect.devices else generate_ip()
        suspect_email = suspect.email

        # Determine log volume based on crime type
        if "Cyber" in self.case.crime_type or "Financial" in self.case.crime_type:
            num_entries = random.randint(5000, 15000)  # MASSIVE for cybercrimes
        else:
            num_entries = random.randint(500, 2000)

        log_date = self.crime_datetime

        # 1. Web Server Access Logs (Apache/Nginx style)
        self._generate_web_server_logs(target_ip, suspect_email, log_date, num_entries)

        # 2. Firewall Logs
        self._generate_firewall_logs(target_ip, log_date, num_entries // 10)

        # 3. DNS Query Logs
        self._generate_dns_logs(target_ip, log_date, num_entries // 20)

        # 4. Email Server Logs
        self._generate_email_server_logs(suspect_email, log_date, num_entries // 50)

        # 5. Database Access Logs
        self._generate_database_logs(target_ip, log_date, num_entries // 100)

    def _generate_web_server_logs(self, suspect_ip, suspect_email, log_date, num_entries):
        """Generate detailed web server access logs."""
        doc = f"--- WEB SERVER ACCESS LOGS (NGINX/APACHE) ---\n"
        doc += f"Server: web-server-01.{fake.domain_name()}\n"
        doc += f"Log Period: {log_date.strftime('%Y-%m-%d %H:%M:%S')} to {(log_date + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')}\n"
        doc += f"Total Requests: {num_entries:,}\n\n"
        doc += f"Format: timestamp | client_ip | method | url | status | bytes | referrer | user_agent | processing_time\n\n"

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "python-requests/2.25.1",  # Suspicious user agent
            "curl/7.68.0",
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)"
        ]

        urls = [
            "/", "/index.html", "/about.html", "/contact.html", "/products.html",
            "/admin/login.php", "/wp-admin/", "/phpmyadmin/", "/admin.php",
            "/api/user/data", "/api/financial/records", "/api/export/csv",
            "/download/database.sql", "/backup/2023-12-01.zip"
        ]

        # Generate noise traffic
        for i in range(num_entries - 10):  # Save 10 entries for suspicious activity
            t = log_date + timedelta(seconds=random.randint(0, 86400))
            ip = generate_ip()
            method = random.choice(["GET", "POST", "HEAD"])
            url = random.choice(urls[:5])  # Normal pages for noise
            status = random.choice([200, 200, 200, 404, 301, 500])
            bytes_sent = random.randint(1000, 50000)
            referrer = random.choice(["-", f"https://{fake.domain_name()}", f"https://google.com/search?q={fake.word()}"])
            user_agent = random.choice(user_agents[:4])  # Normal user agents for noise
            processing_time = ".02"

            doc += f"{t.strftime('%d/%b/%Y:%H:%M:%S %z')} | {ip} | {method} | {url} | {status} | {bytes_sent} | {referrer} | {user_agent} | {processing_time}s\n"

        # Inject suspicious activity
        suspicious_patterns = [
            (log_date + timedelta(hours=2), suspect_ip, "POST", "/admin/login.php", 200, "python-requests/2.25.1", "[BRUTE FORCE ATTEMPT]"),
            (log_date + timedelta(hours=2, minutes=15), suspect_ip, "POST", "/admin/login.php", 200, "python-requests/2.25.1", "[BRUTE FORCE SUCCESS]"),
            (log_date + timedelta(hours=2, minutes=30), suspect_ip, "GET", "/api/user/data", 200, "python-requests/2.25.1", "[DATA EXFILTRATION]"),
            (log_date + timedelta(hours=3), suspect_ip, "GET", "/api/financial/records", 200, "python-requests/2.25.1", "[FINANCIAL DATA ACCESS]"),
            (log_date + timedelta(hours=3, minutes=30), suspect_ip, "GET", "/download/database.sql", 200, "python-requests/2.25.1", "[DATABASE DUMP]"),
            (log_date + timedelta(hours=4), suspect_ip, "POST", "/admin/upload.php", 200, "python-requests/2.25.1", "[MALWARE UPLOAD]"),
            (log_date + timedelta(hours=6), suspect_ip, "GET", "/api/export/csv", 200, "python-requests/2.25.1", "[BULK DATA EXPORT]"),
            (log_date + timedelta(hours=8), suspect_ip, "POST", "/admin/delete_logs.php", 200, "python-requests/2.25.1", "[LOG TAMPERING]"),
            (log_date + timedelta(hours=12), suspect_ip, "GET", "/", 200, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "[POST-ATTACK RECON]"),
            (log_date + timedelta(hours=18), suspect_ip, "POST", "/api/user/delete", 200, "python-requests/2.25.1", "[DATA DESTRUCTION]")
        ]

        for t, ip, method, url, status, ua, note in suspicious_patterns:
            bytes_sent = random.randint(1000, 50000)
            doc += f"{t.strftime('%d/%b/%Y:%H:%M:%S %z')} | {ip} | {method} | {url} | {status} | {bytes_sent} | - | {ua} | 1.45s {note}\n"

        self.case.documents.append(doc)
        self.case.add_evidence(Evidence(
            id=fake.uuid4(),
            type=EvidenceType.DIGITAL,
            description=f"Web Server Access Logs - {num_entries:,} entries",
            collected_by="Cybersecurity Unit",
            collected_at=self.case.date_opened,
            location_found="Compromised Server"
        ))

    def _generate_firewall_logs(self, suspect_ip, log_date, num_entries):
        """Generate detailed firewall logs."""
        doc = f"--- FIREWALL LOGS (CISCO ASA) ---\n"
        doc += f"Device: FW-01.{fake.domain_name()}\n"
        doc += f"Log Period: {log_date.strftime('%Y-%m-%d %H:%M:%S')} to {(log_date + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')}\n"
        doc += f"Total Events: {num_entries:,}\n\n"

        actions = ["Permit", "Permit", "Permit", "Permit", "Deny", "Drop"]
        protocols = ["TCP", "UDP", "ICMP", "TCP", "TCP", "TCP"]

        # Generate firewall events
        for i in range(num_entries):
            t = log_date + timedelta(seconds=random.randint(0, 86400))
            src_ip = generate_ip()
            dst_ip = generate_ip()
            action = random.choice(actions)
            protocol = random.choice(protocols)
            src_port = random.randint(1024, 65535)
            dst_port = random.choice([80, 443, 22, 3389, 21, 25, 53, 110, 143, 993, 995])

            if i == num_entries // 2:  # Inject suspect activity
                src_ip = suspect_ip
                dst_ip = "192.168.1.100"  # Internal server
                action = "Permit"
                dst_port = 3389  # RDP
                note = "[SUSPICIOUS RDP ACCESS]"

            doc += f"{t.strftime('%Y-%m-%d %H:%M:%S')} | {action} | {protocol} | {src_ip}:{src_port} -> {dst_ip}:{dst_port} | Interface: outside\n"

        self.case.documents.append(doc)

    def _generate_dns_logs(self, suspect_ip, log_date, num_entries):
        """Generate DNS query logs."""
        doc = f"--- DNS QUERY LOGS ---\n"
        doc += f"DNS Server: dns-01.{fake.domain_name()}\n"
        doc += f"Log Period: {log_date.strftime('%Y-%m-%d')}\n"
        doc += f"Total Queries: {num_entries:,}\n\n"

        domains = [
            "google.com", "facebook.com", "amazon.com", "microsoft.com", "apple.com",
            "github.com", "stackoverflow.com", "reddit.com", "youtube.com", "netflix.com",
            "evil-c2-server.xyz", "malware-drop-site.net", "data-exfil-domain.org",
            "phishing-bank-login.com", "ransomware-payment-site.onion"
        ]

        record_types = ["A", "AAAA", "MX", "TXT", "CNAME", "NS"]

        for i in range(num_entries):
            t = log_date + timedelta(seconds=random.randint(0, 86400))
            client_ip = generate_ip()
            domain = random.choice(domains)
            qtype = random.choice(record_types)

            if i == num_entries - 5:  # Inject suspect DNS queries
                client_ip = suspect_ip
                domain = "evil-c2-server.xyz"
                note = "[MALICIOUS DOMAIN]"

            doc += f"{t.strftime('%Y-%m-%d %H:%M:%S')} | {client_ip} | QUERY | {domain} | {qtype} | NOERROR\n"

        self.case.documents.append(doc)

    def _generate_email_server_logs(self, suspect_email, log_date, num_entries):
        """Generate email server logs."""
        doc = f"--- EMAIL SERVER LOGS (POSTFIX/SENDMAIL) ---\n"
        doc += f"Server: mail.{fake.domain_name()}\n"
        doc += f"Log Period: {log_date.strftime('%Y-%m-%d')}\n"
        doc += f"Total Messages: {num_entries:,}\n\n"

        for i in range(num_entries):
            t = log_date + timedelta(seconds=random.randint(0, 86400))
            sender = fake.email()
            recipient = fake.email()
            action = random.choice(["SENT", "RECEIVED", "BOUNCED", "SPAM"])

            if i == num_entries - 3:  # Inject suspect email activity
                sender = suspect_email
                recipient = f"victim@{fake.domain_name()}"
                action = "SENT"
                note = "[PHISHING EMAIL]"

            doc += f"{t.strftime('%Y-%m-%d %H:%M:%S')} | {action} | FROM:{sender} | TO:{recipient} | SIZE:{random.randint(1000, 50000)} bytes\n"

        self.case.documents.append(doc)

    def _generate_database_logs(self, suspect_ip, log_date, num_entries):
        """Generate database access logs."""
        doc = f"--- DATABASE ACCESS LOGS (MYSQL) ---\n"
        doc += f"Database: customer_data\n"
        doc += f"Server: db-01.{fake.domain_name()}\n"
        doc += f"Log Period: {log_date.strftime('%Y-%m-%d %H:%M:%S')} to {(log_date + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')}\n"
        doc += f"Total Queries: {num_entries:,}\n\n"

        queries = [
            "SELECT * FROM users WHERE id = ?",
            "SELECT email, password FROM users LIMIT 1000",
            "SELECT * FROM financial_records WHERE account_id = ?",
            "SELECT ssn, credit_card FROM customers",
            "INSERT INTO logs VALUES (?, 'admin_login', ?)",
            "UPDATE users SET password = ? WHERE email = ?",
            "DELETE FROM audit_logs WHERE timestamp < ?",
            "SELECT * FROM sensitive_data"
        ]

        for i in range(num_entries):
            t = log_date + timedelta(seconds=random.randint(0, 3600))
            user = random.choice(["web_app", "admin", "backup", "monitor"])
            query = random.choice(queries)

            if i == num_entries - 2:  # Inject suspect database activity
                user = "hacker"
                query = "SELECT * FROM financial_records"
                client_ip = suspect_ip
                note = "[UNAUTHORIZED DATA ACCESS]"

            doc += f"{t.strftime('%Y-%m-%d %H:%M:%S')} | {user} | {query} | SUCCESS | {random.randint(1, 100)} rows\n"

        self.case.documents.append(doc)

    # --- PRE-CRIME ---

    def _generate_predictive_analytics(self):
        report_date = self.crime_datetime - timedelta(days=3)
        report = generate_predictive_policing_report(self.case.incident_report.incident_location if self.case.incident_report else "Sector 4", self.case.crime_type)
        self.case.documents.append(f"Date Generated: {report_date.strftime('%Y-%m-%d')}\n{report}")

    def _generate_burner_phones(self, complexity: str):
        if complexity == "Low": return
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        target = suspects[0]

        purchase_date = self.crime_datetime - timedelta(days=2)
        receipt = generate_burner_receipt("Male, 30s, wearing black hoodie, baseball cap", purchase_date)
        self.case.documents.append(receipt)
        self.case.add_evidence(Evidence(id=fake.uuid4(), type=EvidenceType.DOCUMENT, description="Receipt: Prepaid Phone", collected_by="Det", collected_at=self.case.date_opened, location_found="Suspect Trash"))

        burner = generate_device(target.id, "Phone")
        burner.is_burner = True
        burner.make = "Nokia 1100"
        target.devices.append(burner)

        # Generate detailed phone extraction report
        log = f"--- BURNER PHONE FORENSIC EXTRACTION REPORT ---\n"
        log += f"Device: Nokia 1100 (Prepaid/Burner Phone)\n"
        log += f"IMEI: {fake.random_number(digits=15, fix_len=True)}\n"
        log += f"SIM Card ICCID: 8901{fake.random_number(digits=13, fix_len=True)}\n"
        log += f"Phone Number: {burner.phone_number}\n"
        log += f"Carrier: {random.choice(['AT&T Prepaid', 'Verizon Prepaid', 'T-Mobile Prepaid', 'Straight Talk', 'Tracfone'])}\n"
        log += f"Activation Date: {purchase_date + timedelta(hours=1)}\n"
        log += f"Extraction Date: {self.case.date_opened.strftime('%Y-%m-%d %H:%M:%S')}\n"
        log += f"Forensic Tool: Cellebrite UFED 7.63.0.27\n"
        log += f"Analyst: Detective {fake.last_name()}\n\n"

        # Detailed cell tower data
        log += f"INITIAL CELL TOWER CONNECTIONS:\n"
        for i in range(3):
            tower_time = purchase_date + timedelta(hours=1+i)
            tower_id = fake.random_number(digits=4)
            location = fake.city() + ", " + fake.state_abbr()
            log += f"[{tower_time.strftime('%Y-%m-%d %H:%M:%S')}] Connected to Tower {tower_id} - {location}\n"

        log += f"\nCELL TOWER PINGS DURING RELEVANT TIMEFRAME:\n"
        crime_window_start = self.crime_datetime - timedelta(hours=2)
        crime_window_end = self.crime_datetime + timedelta(hours=2)

        current_time = crime_window_start
        while current_time <= crime_window_end:
            if random.random() < 0.6:  # 60% chance of ping in window
                tower_id = fake.random_number(digits=4)
                lat, lon = geo_mgr.get_coords_in_radius(getattr(target, 'latitude', None) or geo_mgr.center_lat, getattr(target, 'longitude', None) or geo_mgr.center_lon, 5.0)
                log += f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Tower {tower_id} - Lat:{lat:.6f} Lon:{lon:.6f}\n"
            current_time += timedelta(minutes=random.randint(5, 15))

        log += f"\nCONTACTS ({random.randint(3, 8)} entries):\n"
        contacts = []
        for _ in range(random.randint(3, 8)):
            contact_name = fake.first_name() + " " + fake.last_name()
            contact_number = fake.phone_number()
            contacts.append((contact_name, contact_number))
            log += f"• {contact_name}: {contact_number}\n"

        log += f"\nCALL LOG ({random.randint(8, 15)} calls):\n"
        log += f"TIME                    | TYPE       | NUMBER           | DURATION | TOWER\n"
        log += f"------------------------|------------|------------------|----------|------\n"

        call_count = random.randint(8, 15)
        for _ in range(call_count):
            call_time = self.crime_datetime - timedelta(days=random.randint(0, 3), hours=random.randint(0, 24))
            call_type = random.choice(["OUTGOING", "INCOMING", "MISSED"])
            call_number = random.choice([c[1] for c in contacts] + [fake.phone_number() for _ in range(3)])
            duration = f"{random.randint(0, 5)}:{random.randint(0, 59):02d}" if call_type in ["OUTGOING", "INCOMING"] else "-"
            tower = fake.random_number(digits=4)
            log += f"{call_time.strftime('%Y-%m-%d %H:%M:%S')} | {call_type:<10} | {call_number:<16} | {duration:<8} | {tower}\n"

        log += f"\nTEXT MESSAGES ({random.randint(12, 25)} messages):\n"
        text_count = random.randint(12, 25)
        for _ in range(text_count):
            msg_time = self.crime_datetime - timedelta(days=random.randint(0, 3), hours=random.randint(0, 24))
            msg_type = random.choice(["SENT", "RECEIVED"])
            msg_number = random.choice([c[1] for c in contacts] + [fake.phone_number() for _ in range(3)])
            # Generate realistic burner phone texts
            if msg_type == "SENT":
                messages = [
                    "You got the package?", "Meet me at the spot tonight", "Everything set for tomorrow?",
                    "Change of plans - different location", "Bring the tools", "Job's on",
                    "Need to lay low for a bit", "Got the address", "What time works for you?",
                    "Keep this number quiet", "Burn this phone after", "Payment ready?"
                ]
            else:
                messages = [
                    "Yeah, got it", "Same place as usual?", "What time?", "Address confirmed",
                    "Got the tools ready", "See you then", "Understood", "Payment received",
                    "Will do", "Location changed", "Package secured", "All set"
                ]
            message = random.choice(messages)
            log += f"[{msg_time.strftime('%Y-%m-%d %H:%M:%S')}] {msg_type:<8} | {msg_number:<16} | {message}\n"

        log += f"\nDEVICE INFORMATION:\n"
        log += f"• Model: Nokia 1100\n"
        log += f"• OS: Nokia OS v1.0\n"
        log += f"• Memory: 1MB internal\n"
        log += f"• Battery Level at Seizure: {random.randint(15, 85)}%\n"
        log += f"• Last Backup: Never\n"
        log += f"• Screen Lock: None\n"
        log += f"• PIN Code: Not set\n"
        log += f"• Auto-lock: Disabled\n"

        log += f"\nFORENSIC NOTES:\n"
        log += f"• Device was powered on at time of seizure\n"
        log += f"• No encryption detected\n"
        log += f"• SIM card removed and preserved separately\n"
        log += f"• Device photographed in place before extraction\n"
        log += f"• Chain of custody maintained throughout process\n"
        log += f"• Data integrity verified with MD5 hash: {fake.md5()}\n"

        self.case.documents.append(log)

    def _generate_phishing_attempt(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        target = suspects[0]
        log = generate_phishing_log(target.email, self.crime_datetime - timedelta(days=3))
        self.case.documents.append(log)

    def _generate_dark_web_activity(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        target = suspects[0]
        item = "Unmarked Weapon" if any(w.id for w in target.weapons) else "Credit Card Data"
        post = generate_dark_web_post(target.social_handle or "AnonUser", item, self.crime_datetime - timedelta(days=7))
        self.case.documents.append(post)
        self.case.add_evidence(Evidence(id=fake.uuid4(), type=EvidenceType.DIGITAL, description="Dark Web Scrape", collected_by="Cyber Unit", collected_at=self.case.date_opened, location_found="Tor Network"))

    # --- THE INCIDENT ---

    def _generate_911_call(self):
        callers = [p for p in self.case.persons if p.role in [Role.VICTIM, Role.WITNESS]]
        caller = callers[0] if callers else self.case.persons[0]
        location = fake.address().replace("\n", ", ")
        
        if self.case.incident_report and self.case.incident_report.incident_location != "See Narrative":
             location = self.case.incident_report.incident_location
        
        # Use timeline manager for call time
        if self.timeline_manager:
            call_time = self.timeline_manager.get_911_time()
        else:
            call_time = self.crime_datetime + timedelta(minutes=2)
        
        # Validate caller entity consistency
        if self.entity_validator:
            caller_entity = self.entity_validator.get_entity(caller.full_name)
            if caller_entity:
                # Use registered caller info
                caller_name = caller.full_name
                caller_phone = caller_entity.phone_number or caller.phone_number
                caller_gender = caller_entity.gender
            else:
                caller_name = caller.full_name
                caller_phone = caller.phone_number
                # Infer gender from first name
                caller_gender = "male" if caller.first_name.lower()[-1] in ['o', 'n', 'r', 's', 't', 'd', 'e'] else "female"
        else:
            caller_name = caller.full_name
            caller_phone = caller.phone_number
            # Infer gender from first name
            caller_gender = "male" if caller.first_name.lower()[-1] in ['o', 'n', 'r', 's', 't', 'd', 'e'] else "female"
        
        # Get dispatcher entity (CAD system)
        dispatcher_entity = self._get_or_create_entity("system_cad", "automated", "CAD System")
        dispatcher_name = f"{fake.first_name()} {fake.last_name()[0]}."
        
        script = generate_911_script(self.case.crime_type, location, caller.role.value)
        
        doc = f"--- 911 DISPATCH TRANSCRIPT ---\n"
        doc += f"Date: {call_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        doc += f"Caller: {caller_name}\n"
        doc += f"Caller Phone: {caller_phone}\n"
        doc += f"ANI/ALI: {caller_phone}\n"  # Use actual caller phone for ANI/ALI
        doc += f"PSAP: {fake.city()} Emergency Communications Center\n"
        doc += f"Dispatcher ID: {fake.random_number(digits=4)}\n"
        doc += f"Dispatcher: {dispatcher_name}\n"
        doc += f"Call Priority: {random.choice(['Priority 1', 'Priority 2', 'Priority 3'])}\n\n"
        doc += f"TRANSCRIPT:\n"
        doc += f"{'='*60}\n"
        for speaker, text in script:
            if speaker == "SYSTEM":
                doc += f"[{speaker}] {text}\n"
            else:
                doc += f"{speaker.upper()}: {text}\n"
        doc += f"{'='*60}\n"
        doc += f"\nCALL DISPOSITION: Transferred to responding agency\n"
        doc += f"RESPONDING UNITS: {random.choice(['Patrol Unit 415-ADAM', 'Patrol Unit 415-BOY', 'Patrol Unit 415-CHARLIE'])}\n"
        doc += f"NOTES: Caller was {random.choice(['calm', 'hysterical', 'upset', 'frightened', 'angry'])}. {random.choice(['Provided detailed description', 'Limited information available', 'Witnessed incident in progress'])}.\n"
        
        # Apply system errors
        doc = dispatcher_entity.introduce_error(doc)
        self.case.documents.append(doc)
        
        if not self.case.incident_report:
            from .models import IncidentReport
            self.case.incident_report = IncidentReport(
                id=fake.uuid4(), reporting_officer=self.case.reporting_officer, 
                incident_date=self.crime_datetime, 
                incident_location=location,
                incident_type=self.case.crime_type, narrative="", 
                involved_persons=self.case.persons
            )

    def _generate_cad_report(self):
        # Use timeline manager for call time
        if self.timeline_manager:
            call_time = self.timeline_manager.get_911_time()
        else:
            call_time = self.crime_datetime + timedelta(minutes=2)
        
        loc = self.case.incident_report.incident_location if self.case.incident_report else fake.address().replace("\n", ", ")
        
        # Get caller info for CAD log (should match 911 caller)
        callers = [p for p in self.case.persons if p.role in [Role.VICTIM, Role.WITNESS]]
        caller = callers[0] if callers else None
        
        caller_name = None
        caller_gender = None
        if caller and self.entity_validator:
            caller_entity = self.entity_validator.get_entity(caller.full_name)
            if caller_entity:
                caller_name = caller_entity.name
                caller_gender = caller_entity.gender
            else:
                caller_name = caller.full_name
                # Infer gender from first name
                caller_gender = "male" if caller.first_name.lower()[-1] in ['o', 'n', 'r', 's', 't', 'd', 'e'] else "female"
        elif caller:
            caller_name = caller.full_name
            # Infer gender from first name
            caller_gender = "male" if caller.first_name.lower()[-1] in ['o', 'n', 'r', 's', 't', 'd', 'e'] else "female"
        
        # Get CAD system entity
        cad_entity = self._get_or_create_entity("system_cad", "automated", "CAD System")
        log = generate_cad_log(call_time, loc, self.case.crime_type, caller_name, caller_gender)
        
        # Apply system errors
        log = cad_entity.introduce_error(log)
        self.case.documents.append(log)

    def _generate_incident_report(self):
        victims = [p for p in self.case.persons if p.role == Role.VICTIM]
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        base_lat, base_lon = geo_mgr.get_random_city_location()
        scene_lat, scene_lon = geo_mgr.get_coords_in_radius(base_lat, base_lon, 0.05)
        wx, temp = generate_weather()

        # Create detailed incident report
        if not self.case.incident_report:
            from .models import IncidentReport
            self.case.incident_report = IncidentReport(
                id=fake.uuid4(),
                reporting_officer=self.case.reporting_officer,
                incident_date=self.crime_datetime,
                incident_location=fake.address().replace("\n", ", "),
                incident_type=self.case.crime_type,
                narrative="",
                involved_persons=self.case.persons,
                latitude=str(scene_lat),
                longitude=str(scene_lon),
                weather_condition=wx
            )

        # Generate comprehensive narrative based on crime type
        if not self._should_generate_physical_evidence(self.case.crime_type):
            # Non-physical crimes (fraud, scams, cybercrime)
            narrative = self._generate_non_physical_incident_report(victims, suspects)
        elif "Cyber" in self.case.crime_type or ("Financial" in self.case.crime_type and "Fraud" not in self.case.crime_type):
            narrative = self._generate_cybercrime_incident_report()
        else:
            narrative = self._generate_standard_incident_report(victims, suspects, wx, temp)

        self.case.incident_report.narrative = narrative

        # Get reporting officer entity (create/get consistent officer)
        officer_id = f"officer_{self.case.reporting_officer.id}"
        officer_entity = self._get_or_create_entity(officer_id, "human", self.case.reporting_officer.full_name)
        
        # Officer might misspell suspect/victim names based on attention to detail
        suspect_names_in_doc = []
        victim_names_in_doc = []
        for suspect in suspects:
            correct_name = suspect.full_name
            misspelled = officer_entity.misspell_name(correct_name)
            if misspelled != correct_name:
                narrative = narrative.replace(correct_name, misspelled)
                suspect_names_in_doc.append(misspelled)
            else:
                suspect_names_in_doc.append(correct_name)
        
        for victim in victims:
            correct_name = victim.full_name
            misspelled = officer_entity.misspell_name(correct_name)
            if misspelled != correct_name:
                narrative = narrative.replace(correct_name, misspelled)
                victim_names_in_doc.append(misspelled)
            else:
                victim_names_in_doc.append(correct_name)
        
        doc = f"--- INCIDENT REPORT ---\n"
        doc += f"INCIDENT REPORT #{fake.random_number(digits=6)}\n"
        doc += f"DATE/TIME: {self.case.incident_report.incident_date.strftime('%Y-%m-%d %H:%M')}\n"
        doc += f"LOCATION: {self.case.incident_report.incident_location}\n"
        doc += f"COORDINATES: {scene_lat:.6f}, {scene_lon:.6f}\n"
        doc += f"WEATHER CONDITIONS: {wx}, {temp}\n"
        doc += f"REPORTING OFFICER: {officer_entity.name}\n"
        doc += f"BADGE #: {fake.random_number(digits=4)}\n"
        doc += f"INCIDENT TYPE: {self.case.crime_type}\n\n"
        doc += f"NARRATIVE:\n{narrative}\n\n"
        doc += f"ACTIONS TAKEN:\n"
        if self._should_generate_physical_evidence(self.case.crime_type):
            doc += f"- Scene secured and documented\n"
            doc += f"- Evidence collection initiated\n"
            doc += f"- Witness statements obtained\n"
            doc += f"- Digital forensics requested\n"
        else:
            doc += f"- Victim statement obtained and documented\n"
            doc += f"- Digital evidence preservation initiated\n"
            doc += f"- Financial records subpoenaed\n"
            doc += f"- Phone carrier records requested\n"
        if "Cyber" in self.case.crime_type:
            doc += f"- Cybersecurity unit notified\n"
            doc += f"- Network logs preserved\n"
            doc += f"- Affected systems isolated\n"
        if "Phone" in self.case.crime_type or "Scam" in self.case.crime_type:
            doc += f"- VoIP provider contacted\n"
            doc += f"- Call detail records requested\n"

        # Apply officer errors (typos, grammar mistakes)
        doc = officer_entity.introduce_error(doc)
        self.case.documents.append(doc)

    def _generate_cybercrime_incident_report(self):
        """Generate detailed cybercrime incident report."""
        suspect = next((p for p in self.case.persons if p.role == Role.SUSPECT), None)
        victim = next((p for p in self.case.persons if p.role == Role.VICTIM), None)

        narrative = f"On {self.case.incident_report.incident_date.strftime('%B %d, %Y at approximately %H:%M')}, "
        narrative += f"the {fake.company()} IT Security Operations Center (SOC) detected anomalous network activity "
        narrative += f"indicating a potential cyber intrusion.\n\n"

        if victim:
            narrative += f"The victim organization, {fake.company()}, reported unauthorized access to their "
            narrative += f"corporate network affecting approximately {random.randint(500, 5000)} user accounts "
            narrative += f"and sensitive financial data.\n\n"

        narrative += f"INITIAL DETECTION:\n"
        narrative += f"- Multiple failed login attempts from suspicious IP addresses\n"
        narrative += f"- Unusual data exfiltration patterns detected\n"
        narrative += f"- Malware signatures identified in network traffic\n"
        narrative += f"- Compromised credentials used to access privileged systems\n\n"

        narrative += f"IMPACT ASSESSMENT:\n"
        narrative += f"- Financial loss estimated at ${fake.random_number(digits=6):,}\n"
        narrative += f"- Personal identifiable information (PII) of {fake.random_number(digits=5):,} individuals potentially compromised\n"
        narrative += f"- Intellectual property theft including proprietary algorithms and customer data\n"
        narrative += f"- Disruption to business operations lasting {random.randint(2, 14)} days\n\n"

        if suspect and suspect.devices:
            device = suspect.devices[0]
            narrative += f"TECHNICAL INDICATORS:\n"
            narrative += f"- Command and Control (C2) server: {generate_ip()}\n"
            narrative += f"- Malware hash: {generate_file_hash('md5')}\n"
            narrative += f"- Attacker IP: {device.ip_address}\n"
            narrative += f"- Compromised domain: {fake.domain_name()}\n\n"

        narrative += f"INVESTIGATION STATUS:\n"
        narrative += f"Digital forensics team has been engaged to perform memory analysis, "
        narrative += f"network packet capture review, and malware reverse engineering. "
        narrative += f"Federal authorities have been notified due to the interstate nature "
        narrative += f"of the cyber intrusion."

        return narrative

    def _should_generate_physical_evidence(self, crime_type: str) -> bool:
        """Determine if crime type requires physical evidence collection."""
        crime_lower = crime_type.lower()
        non_physical_indicators = ["fraud", "scam", "phone", "cybercrime", "cyber"]
        # Financial crimes can be physical (robbery) or non-physical (fraud)
        if "financial" in crime_lower and "fraud" not in crime_lower:
            return True  # Financial crimes like robbery are physical
        return not any(indicator in crime_lower for indicator in non_physical_indicators)
    
    def _generate_non_physical_incident_report(self, victims, suspects):
        """Generate incident report for non-physical crimes (fraud, scams, etc.)."""
        v_name = victims[0].full_name if victims else "Unknown Victim"
        s_name = suspects[0].full_name if suspects else "Unknown Suspect"
        
        crime_method = self.narrative_elements.get('crime_method', 'Unknown Method')
        motivation = self.narrative_elements.get('motivation', 'Financial gain')
        
        narrative = f"On {self.case.incident_report.incident_date.strftime('%B %d, %Y at approximately %H:%M')}, "
        narrative += f"this department received a report of a {self.case.crime_type.lower()} from {v_name}.\n\n"
        
        if victims:
            narrative += f"VICTIM STATEMENT:\n"
            narrative += f"Victim {v_name} reported being contacted via {random.choice(['phone call', 'email', 'text message', 'website', 'social media'])} "
            narrative += f"on {self.case.incident_report.incident_date.strftime('%B %d, %Y')} at approximately "
            narrative += f"{(self.case.incident_report.incident_date - timedelta(minutes=random.randint(30, 120))).strftime('%H:%M')}. "
            narrative += f"The suspect, identified as {s_name if suspects else 'Unknown'}, "
            narrative += f"engaged in {crime_method.lower()} motivated by {motivation.lower()}.\n\n"
        
        narrative += f"INITIAL INVESTIGATION:\n"
        narrative += f"- Crime method: {crime_method}\n"
        narrative += f"- Suspected motivation: {motivation}\n"
        narrative += f"- Method of operation: {random.choice(['Phone-based scam', 'Online fraud', 'Email phishing', 'Social engineering', 'Remote access'])}\n"
        narrative += f"- Communication method: {random.choice(['Phone call', 'Email', 'Text message', 'Website', 'Social media'])}\n\n"
        
        if suspects:
            narrative += f"SUSPECT INFORMATION:\n"
            narrative += f"- Name: {s_name}\n"
            narrative += f"- Age: {suspects[0].age if suspects else 'Unknown'}\n"
            narrative += f"- Known identifiers: {random.choice(['Phone number', 'Email address', 'IP address', 'Bank account', 'Social media account'])}\n"
            narrative += f"- Communication method: {random.choice(['Phone call', 'Email', 'Text message', 'Website form', 'Social media message'])}\n"
            narrative += f"- Suspect location: {random.choice(['Unknown', 'Out of state', 'Out of country', 'Under investigation'])}\n\n"
        
        narrative += f"EVIDENCE RECOVERY:\n"
        evidence_types = ["digital footprints", "email communications", "phone records", "financial transactions", "internet history", "account records"]
        recovered_evidence = random.sample(evidence_types, random.randint(2, 4))
        narrative += f"Evidence observed and collected includes: {', '.join(recovered_evidence)}. "
        narrative += f"Digital forensics and financial investigation have been initiated.\n\n"
        
        narrative += f"INVESTIGATIVE LEADS:\n"
        narrative += f"- Victim statement obtained\n"
        narrative += f"- Phone records investigation initiated\n"
        narrative += f"- Digital forensics preservation initiated\n"
        if "Financial" in self.case.crime_type or "Fraud" in self.case.crime_type or "Scam" in self.case.crime_type:
            narrative += f"- Financial transaction analysis requested\n"
        if "Phone" in self.case.crime_type or "Scam" in self.case.crime_type:
            narrative += f"- Phone carrier records subpoenaed\n"
            narrative += f"- VoIP provider investigation initiated\n"
        
        return narrative
    
    def _generate_standard_incident_report(self, victims, suspects, wx, temp):
        """Generate standard incident report narrative with enhanced coherence."""
        v_name = victims[0].full_name if victims else "Unknown Victim"
        s_name = suspects[0].full_name if suspects else "Unknown Suspect"

        # Use established crime method for consistency
        crime_method = self.narrative_elements['crime_method']
        motivation = self.narrative_elements['motivation']

        narrative = f"On {self.case.incident_report.incident_date.strftime('%B %d, %Y at approximately %H:%M')}, "
        narrative += f"Officer {self.case.reporting_officer.full_name} responded to a call regarding a {self.case.crime_type.lower()} "
        narrative += f"at {self.case.incident_report.incident_location}.\n\n"

        if victims:
            narrative += f"Upon arrival, contact was made with the victim, identified as {v_name}. "
            narrative += f"{v_name} reported being victimized through {crime_method.lower()} motivated by {motivation.lower()}. "
            narrative += f"The incident occurred at approximately "
            narrative += f"{(self.case.incident_report.incident_date - timedelta(minutes=random.randint(30, 120))).strftime('%H:%M')} "
            narrative += f"and involved {s_name} as the primary suspect.\n\n"

        narrative += f"INITIAL INVESTIGATION:\n"
        narrative += f"- Crime method: {crime_method}\n"
        narrative += f"- Suspected motivation: {motivation}\n"
        narrative += f"- Point of entry/exit: {random.choice(['Front door', 'Rear window', 'Side entrance', 'Fire escape', 'Underground access'])}\n"
        narrative += f"- Method of operation: {random.choice(['Solo perpetrator', 'Coordinated team', 'Opportunistic', 'Pre-planned'])}\n\n"

        narrative += f"SCENE DESCRIPTION:\n"
        narrative += f"- Weather conditions: {wx}, temperature {temp}\n"
        narrative += f"- Area lighting: {random.choice(['Well lit', 'Poorly lit', 'Dark'])}\n"
        narrative += f"- Traffic conditions: {random.choice(['Light traffic', 'Heavy traffic', 'No traffic'])}\n"
        narrative += f"- Nearby structures: {random.choice(['Residential area', 'Commercial district', 'Industrial zone'])}\n"
        narrative += f"- Security measures: {random.choice(['No visible security', 'Basic alarm system', 'CCTV cameras', 'Security guard', 'Advanced security system'])}\n\n"

        if suspects:
            narrative += f"SUSPECT INFORMATION:\n"
            narrative += f"- Name: {s_name}\n"
            narrative += f"- Age: {suspects[0].age if suspects else 'Unknown'}\n"
            # Only include physical description for physical crimes
            if self._should_generate_physical_evidence(self.case.crime_type):
                suspect = suspects[0]
                # Use actual suspect physical description
                if suspect.height and suspect.build:
                    desc_parts = [suspect.height, suspect.gender if suspect.gender else "unknown gender"]
                    if suspect.build:
                        desc_parts.append(f"{suspect.build} build")
                    if suspect.hair_color:
                        desc_parts.append(f"{suspect.hair_color} hair")
                    if suspect.eye_color:
                        desc_parts.append(f"{suspect.eye_color} eyes")
                    if suspect.facial_hair and suspect.facial_hair != "none":
                        desc_parts.append(f"{suspect.facial_hair}")
                    narrative += f"- Physical description: {', '.join(desc_parts)}\n"
                else:
                    # Fallback if no description available
                    narrative += f"- Physical description: {random.choice(['5\'10\" male, athletic build', '6\'2\" male, stocky build', '5\'4\" female, slim build', '5\'8\" male, average build'])}\n"
                narrative += f"- Direction of flight: {random.choice(['Northbound', 'Southbound', 'Eastbound', 'Westbound'])}\n"
                narrative += f"- Method of transportation: {random.choice(['On foot', 'Vehicle', 'Bicycle', 'Public transportation'])}\n"
                narrative += f"- Distinctive features: {random.choice(['Tattoo on neck', 'Limping gait', 'Scar on face', 'Colorful backpack', 'None apparent'])}\n\n"
            else:
                narrative += f"- Known identifiers: {random.choice(['Phone number', 'Email address', 'IP address', 'Bank account', 'Social media account'])}\n"
                narrative += f"- Communication method: {random.choice(['Phone call', 'Email', 'Text message', 'Website form', 'Social media message'])}\n"
                narrative += f"- Suspect location: {random.choice(['Unknown', 'Out of state', 'Out of country', 'Under investigation'])}\n\n"

        # Include alibi information if available
        for suspect in suspects:
            if "Alibi:" in suspect.notes:
                alibi = suspect.notes.split("Alibi:")[1].strip()
                narrative += f"SUSPECT ALIBI: {suspect.full_name} claims to have been {alibi}.\n\n"

        # Include false flags if they exist
        if self.narrative_elements['false_flags']:
            narrative += f"INITIAL OBSERVATIONS OF NOTE:\n"
            for flag in self.narrative_elements['false_flags'][:2]:  # Show up to 2 false flags
                narrative += f"- {flag['description']} discovered at scene\n"
            narrative += "\n"

        narrative += f"EVIDENCE RECOVERY:\n"
        # Only include physical evidence for physical crimes
        if self._should_generate_physical_evidence(self.case.crime_type):
            evidence_types = ["footprints", "tire tracks", "broken glass", "discarded items", "blood stains", "clothing fibers", "fingerprints", "DNA traces", "tool marks", "digital footprints"]
            recovered_evidence = random.sample(evidence_types, random.randint(3, 6))
            narrative += f"Physical evidence observed and collected includes: {', '.join(recovered_evidence)}. "
            narrative += f"Forensic evidence collection has been initiated, including {random.choice(['DNA analysis', 'fingerprint processing', 'ballistics examination', 'digital forensics', 'trace evidence analysis'])}.\n\n"
        else:
            # For non-physical crimes, focus on digital/paper evidence
            evidence_types = ["digital footprints", "email communications", "phone records", "financial transactions", "internet history", "account records"]
            recovered_evidence = random.sample(evidence_types, random.randint(2, 4))
            narrative += f"Evidence observed and collected includes: {', '.join(recovered_evidence)}. "
            narrative += f"Digital forensics and financial investigation have been initiated.\n\n"

        # Add investigative leads
        narrative += f"INVESTIGATIVE LEADS:\n"
        narrative += f"- Witness statements from {len([p for p in self.case.persons if p.role == Role.WITNESS])} individuals\n"
        narrative += f"- Surveillance footage review in progress\n"
        narrative += f"- Digital evidence preservation initiated\n"
        if "Financial" in self.case.crime_type:
            narrative += f"- Financial transaction analysis requested\n"
        if "Cyber" in self.case.crime_type:
            narrative += f"- Cybersecurity unit consultation initiated\n"

        return narrative
        self.case.incident_report.weather_condition = wx
        self.case.incident_report.temperature = temp
        
        narrative = f"INCIDENT REPORT #{fake.random_number(digits=6)}\nDATE/TIME: {self.crime_datetime.strftime('%Y-%m-%d %H:%M')}\nLOCATION: {self.case.incident_report.incident_location}\n"
        narrative += f"WEATHER: {wx}, {temp}\nTYPE: {self.case.crime_type}\n"
        narrative += f"SUMMARY: Officer {self.case.reporting_officer.full_name} responded to {self.case.crime_type}. Scene secured at {(self.crime_datetime + timedelta(minutes=20)).strftime('%H:%M')}."
        
        self.case.incident_report.narrative = narrative
        self.case.documents.append(f"--- INCIDENT REPORT ---\n{narrative}")

    def _generate_iot_evidence(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        target = suspects[0]
        if random.random() < 0.4:
            log = generate_iot_logs("Doorbell", target.full_name, self.crime_datetime)
            self.case.documents.append(log)
            self.case.add_evidence(Evidence(id=fake.uuid4(), type=EvidenceType.DIGITAL, description="IoT Logs", collected_by="Cyber", collected_at=self.case.date_opened, location_found="Cloud"))

    # --- SCENE INVESTIGATION ---

    def _generate_evidence_and_warrants(self, modifiers: List[str]):
        collection_start = self.crime_datetime + timedelta(hours=1)
        scene_lat = self.case.incident_report.latitude
        scene_lon = self.case.incident_report.longitude
        collected_items = []
        
        # Fingerprints (only for physical crimes)
        if self._should_generate_physical_evidence(self.case.crime_type):
            phys_ev = Evidence(id=fake.uuid4(), type=EvidenceType.FORENSIC, description="Latent Fingerprints", collected_by=self.case.reporting_officer.full_name, collected_at=collection_start, location_found="Crime Scene")
            self._generate_chain_of_custody(phys_ev, self.case.reporting_officer.full_name, start_date=collection_start)
            self.case.add_evidence(phys_ev)
            collected_items.append("Latent Fingerprint Lift Cards")
        
        is_violent = any(x in self.case.crime_type for x in ["Murder", "Assault", "Robbery"])
        if is_violent: 
            self._gen_ballistics(scene_lat, scene_lon, collection_start)
            collected_items.append("Spent Shell Casings")
        
        if "Phone data pull" in modifiers:
            # self._generate_phone_data()  # TODO: Implement phone data extraction
            collected_items.append("Suspect Mobile Phone (Seized later)")
            
        if "Financial Records" in modifiers: 
            self._generate_financial_csv_dump()
        
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if suspects and suspects[0].vehicles and roll_check(10):
            self._gen_vehicle_telematics(suspects[0])
            
        if collected_items:
            bag_log = generate_evidence_bagging_log(self.case.reporting_officer.full_name, collection_start + timedelta(hours=1), collected_items)
            self.case.documents.append(bag_log)

    def _generate_cctv_surveillance(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        target = suspects[0]
        
        vehicle_desc = f"{target.vehicles[0].color} {target.vehicles[0].make}" if target.vehicles else "Unknown Vehicle"
        wx = self.case.incident_report.weather_condition
        
        log = f"--- CCTV LOG ---\n" + generate_cctv_log("Main St Intersection", "Male subject", vehicle_desc, "Fleeing Scene Northbound", wx)
        self.case.documents.append(log)

    def _generate_k9_search(self):
        res = "Positive Alert" if roll_check(10) else "Negative"
        report = generate_k9_report("Ofc. K9 Handler", "Perimeter Search", res)
        self.case.documents.append(report)

    # --- FOLLOW UP & LABS ---

    def _gen_ballistics(self, lat, lon, collection_time):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT and p.weapons]
        if not suspects: return
        suspect = suspects[0]
        weapon = suspect.weapons[0]
        
        casing_ev = Evidence(id=fake.uuid4(), type=EvidenceType.PHYSICAL, description=f"Spent Shell Casings ({weapon.caliber})", collected_by="Forensics", collected_at=collection_time, location_found="Crime Scene")
        self._generate_chain_of_custody(casing_ev, "Forensics", start_date=collection_time)
        self.case.add_evidence(casing_ev)
        
        warrant_date = self._create_search_warrant(suspect, "Firearms/Weapons")
        gun_ev = Evidence(id=fake.uuid4(), type=EvidenceType.PHYSICAL, description=f"Firearm: {weapon.make} {weapon.model}", collected_by="SWAT", collected_at=warrant_date+timedelta(hours=6), location_found="Residence")
        self.case.add_evidence(gun_ev)
        
        # Generate comprehensive NIBIN report
        from .utils import generate_nibin_report
        doc = generate_nibin_report(casing_ev.id, gun_ev.id, weapon, suspect.full_name)
        self.case.documents.append(doc)

    def _gen_vehicle_telematics(self, suspect):
        vehicle = suspect.vehicles[0]
        warrant_date = self._create_search_warrant(suspect, f"Vehicle EDR/Infotainment ({vehicle.license_plate})")
        
        # Generate comprehensive EDR log
        doc_edr = f"""--- VEHICLE EVENT DATA RECORDER (EDR) LOG ---

Vehicle Information:
VIN: {vehicle.vin}
Make/Model: {vehicle.make} {vehicle.model}
License Plate: {vehicle.license_plate}

EDR Data Extraction Report
Downloaded: {warrant_date + timedelta(days=1)}
Technician: {fake.last_name()}, {fake.last_name()} & Associates

PRE-CRASH DATA (30 seconds before trigger):
Time: {self.crime_datetime.strftime('%H:%M:%S')}
Speed: {random.randint(25, 45)} mph
Engine RPM: {random.randint(1800, 2500)}
Throttle Position: {random.randint(15, 35)}%
Brake Pressure: 0 psi
Seatbelt Status: Fastened
Airbag Status: Armed

CRASH TRIGGER EVENT:
Time: {(self.crime_datetime + timedelta(seconds=2)).strftime('%H:%M:%S')}
Delta-V: {random.randint(8, 15)} mph
Peak G-Force: {round(random.uniform(2.5, 4.2), 1)}g
Duration: {random.randint(80, 150)}ms
Direction: Front impact

POST-CRASH DATA (5 seconds after trigger):
Time: {(self.crime_datetime + timedelta(seconds=5)).strftime('%H:%M:%S')}
Speed: 0 mph
Brake Pressure: {random.randint(1200, 1800)} psi
Airbag Deployment: Driver, Passenger
Stability Control: Activated
ABS Activation: Yes

ADDITIONAL VEHICLE SYSTEMS DATA:
Tire Pressure (FL/FR/RL/RR): {random.randint(28, 32)}/{random.randint(28, 32)}/{random.randint(30, 34)}/{random.randint(30, 34)} psi
Fuel Level: {random.randint(15, 35)}%
Engine Temperature: {random.randint(185, 210)}°F
Battery Voltage: {round(random.uniform(12.2, 13.8), 1)}V

Diagnostic Codes Present:
- P0301: Cylinder 1 Misfire Detected
- C1241: ABS Hydraulic Pump Motor Circuit Failure

Data Integrity: Verified (SHA-256: {fake.sha256()})
EDR Module: Bosch CDR-6000
Firmware Version: 2.4.7"""
        self.case.documents.append(doc_edr)
        
        doc_info = generate_infotainment_log(vehicle, self.crime_datetime)
        self.case.documents.append(doc_info)
        
        self.case.add_evidence(Evidence(id=fake.uuid4(), type=EvidenceType.DIGITAL, description=f"Vehicle Infotainment/EDR", collected_by="Traffic Homicide", collected_at=warrant_date + timedelta(days=1), location_found="Impound Lot"))

    def _generate_forensic_geology(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        target = suspects[0]
        report = generate_soil_analysis_report(target.full_name, "Crime Scene", "Suspect Boots")
        self.case.documents.append(report)
        self.case.add_evidence(Evidence(id=fake.uuid4(), type=EvidenceType.FORENSIC, description="Soil Samples", collected_by="CSI", collected_at=self.case.date_opened, location_found="Boots"))

    def _generate_drone_surveillance(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        target = suspects[0]
        log = generate_drone_log(target.address, "Male, 6ft", self.case.date_opened + timedelta(days=1))
        self.case.documents.append(log)
        if "LOST LINK" not in log:
            self.case.add_evidence(Evidence(id=fake.uuid4(), type=EvidenceType.MEDIA, description="Drone Logs", collected_by="Air Support", collected_at=self.case.date_opened, location_found="Server"))

    def _generate_trash_pull(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        target = suspects[0]
        log = generate_trash_pull_log(target.full_name, self.case.date_opened - timedelta(days=1))
        self.case.documents.append(log)
        if "RECOVERED ITEMS" in log:
            self.case.add_evidence(Evidence(id=fake.uuid4(), type=EvidenceType.PHYSICAL, description="Trash Pull", collected_by="Det", collected_at=self.case.date_opened - timedelta(days=1), location_found="Curbside"))

    def _generate_autopsy_suite(self):
        victims = [p for p in self.case.persons if p.role == Role.VICTIM]
        if not victims: return
        victim = victims[0]
        discovery_time = self.crime_datetime + timedelta(hours=random.randint(1, 12))
        
        report = generate_autopsy_report(victim.full_name, self.case.crime_type, self.crime_datetime)
        self.case.documents.append(report)
        self.case.add_evidence(Evidence(id=fake.uuid4(), type=EvidenceType.DOCUMENT, description="Autopsy Report", collected_by="ME", collected_at=discovery_time + timedelta(days=1), location_found="Morgue"))
        
        tox = generate_toxicology_screen(victim.full_name, self.case.crime_type)
        self.case.documents.append(tox)
        
        scene_notes = generate_coroner_scene_notes(victim.full_name, self.crime_datetime, discovery_time)
        self.case.documents.append(scene_notes)
        
        if roll_check(14):
            bug_report = generate_entomology_report(self.crime_datetime, discovery_time, "Wooded Area", self.case.incident_report.weather_condition)
            self.case.documents.append(bug_report)
            self.case.add_evidence(Evidence(id=fake.uuid4(), type=EvidenceType.FORENSIC, description="Entomological Specimens", collected_by="CSI", collected_at=discovery_time, location_found="Body"))

    def _generate_lineup_results(self):
        witnesses = [p for p in self.case.persons if p.role == Role.WITNESS]
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not witnesses or not suspects: return
        for w in witnesses:
            report = generate_lineup_form(w, suspects[0])
            self.case.documents.append(report)

    def _create_search_warrant(self, target_person: Person, target_type: str) -> datetime:
        from .utils import generate_search_warrant, generate_search_warrant_affidavit
        
        # Use timeline manager for warrant time
        if self.timeline_manager:
            date = self.timeline_manager.get_warrant_time()
        else:
            date = self.case.date_opened + timedelta(hours=random.randint(4, 24))

        # Generate comprehensive affidavit with consistency managers
        affidavit = generate_search_warrant_affidavit(
            self.case.reporting_officer, 
            target_person.address, 
            self.case.crime_type, 
            f"suspicion of {target_type}",
            jurisdiction_manager=self.jurisdiction_manager,
            officer_registry=self.officer_registry,
            incident_date=self.crime_datetime
        )
        self.case.documents.append(affidavit)

        # Generate formal search warrant with consistency managers
        items_to_seize = [target_type, "Digital devices", "Documents related to investigation", "Clothing and personal items"]
        warrant = generate_search_warrant(
            self.case.reporting_officer, 
            target_person.full_name, 
            target_person.address, 
            items_to_seize, 
            self.case.crime_type,
            jurisdiction_manager=self.jurisdiction_manager,
            officer_registry=self.officer_registry
        )
        self.case.documents.append(warrant)

        # Generate warrant return with consistency managers
        seized_items = [target_type] if random.random() > 0.3 else [target_type, "Digital device", "Personal documents"]
        ret = generate_warrant_return(
            target_person.full_name, 
            target_person.address, 
            seized_items,
            officer_registry=self.officer_registry,
            executing_officer=self.case.reporting_officer.full_name if self.case.reporting_officer else None
        )
        self.case.documents.append(ret)

        return date

    def _generate_chain_of_custody(self, evidence: Evidence, officer_name: str, start_date: datetime = None):
        if not start_date: start_date = evidence.collected_at
        evidence.chain_of_custody = [f"{start_date.strftime('%Y-%m-%d %H:%M')} - Collected by {officer_name}"]

    def _generate_lab_reports(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        bio_ev = next((e for e in self.case.evidence if e.type == EvidenceType.FORENSIC), None)
        if bio_ev:
             report = generate_afis_report(suspects[0].full_name, "High")
             self.case.documents.append(report)
             bio_ev.metadata["lab_report"] = "Generated"

    def _generate_discovery_package(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        defendant = suspects[0].full_name
        charges = f"{self.case.crime_type} (Felony)"
        doc = generate_discovery_index(self.case.id, defendant, charges)
        self.case.documents.append(doc)

    # --- PASSTHROUGH GENERATORS ---
    def _gen_osint_profiles(self):
        for p in self.case.persons:
            if p.role == Role.SUSPECT: self.case.documents.append(f"--- OSINT ---\nHandle: {p.social_handle}\n" + "\n".join(generate_social_posts(p.motive)))
    def _generate_shell_companies(self): generate_corp_name()
    def _generate_red_herring(self, c): pass
    def _generate_documents(self): pass
    def _generate_interrogations(self): 
        for s in [p for p in self.case.persons if p.role == Role.SUSPECT]:
            d = generate_interrogation_dialogue(s.personality, self.case.crime_type)
            self.case.documents.append(f"--- INTERROGATION ---\nSubject: {s.full_name}\n" + "\n".join([f"{k}: {v}" for k,v in d]))
    def _generate_alpr_hits(self):
        """Generate ALPR (Automated License Plate Reader) hits with 10-15% chance of suspect vehicle."""
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects or not suspects[0].vehicles:
            return
        
        # 10-15% chance to generate ALPR hit for suspect vehicle
        if random.random() < random.uniform(0.10, 0.15):
            suspect = suspects[0]
            vehicle = suspect.vehicles[0]
            
            # Get ALPR system entity (use human type for misread_plate to work)
            alpr_entity = self._get_or_create_entity("system_alpr", "human", "ALPR System")
            # Set attention_to_detail for ALPR system (lower = more errors)
            if not hasattr(alpr_entity, 'attention_to_detail'):
                alpr_entity.attention_to_detail = random.randint(70, 90)  # ALPR systems have decent but not perfect accuracy
                
            # Generate multiple ALPR hits (cameras at different locations)
            num_hits = random.randint(2, 5)
            hits = []
            
            for i in range(num_hits):
                hit_time = self.crime_datetime + timedelta(
                    hours=random.randint(-12, 12),
                    minutes=random.randint(0, 59)
                )
                
                # Get location near crime scene or suspect's path
                lat, lon = geo_mgr.get_coords_in_radius(
                    getattr(suspect, 'latitude', None) or geo_mgr.center_lat,
                    getattr(suspect, 'longitude', None) or geo_mgr.center_lon,
                    20.0
                )
                
                # ALPR might misread plate based on system precision
                plate_read = vehicle.license_plate
                if alpr_entity.precision_score < 0.90 and random.random() < 0.2:
                    plate_read = alpr_entity.misread_plate(plate_read)
                
                camera_id = f"ALPR-{random.randint(100, 999)}"
                location = f"{fake.street_name()} & {fake.street_name()}"
                
                hits.append({
                    'time': hit_time,
                    'plate': plate_read,
                    'camera': camera_id,
                    'location': location,
                    'lat': lat,
                    'lon': lon,
                    'confidence': random.randint(85, 99) if plate_read == vehicle.license_plate else random.randint(60, 85)
                })
            
            # Sort by time
            hits.sort(key=lambda x: x['time'])
            
            # Generate ALPR report document
            doc = f"""--- AUTOMATED LICENSE PLATE READER (ALPR) HITS ---
System: {fake.company()} ALPR Network
Date Range: {hits[0]['time'].strftime('%Y-%m-%d')} to {hits[-1]['time'].strftime('%Y-%m-%d')}
Total Hits: {num_hits}
Case Number: {self.case.id}

================================================================================
ALPR HIT LOG
================================================================================
TIMESTAMP           | CAMERA ID    | PLATE READ    | LOCATION                    | CONFIDENCE | GPS COORDINATES
--------------------|--------------|---------------|-----------------------------|------------|------------------
"""
            for hit in hits:
                doc += f"{hit['time'].strftime('%Y-%m-%d %H:%M:%S')} | {hit['camera']:<12} | {hit['plate']:<13} | {hit['location']:<27} | {hit['confidence']:<10}% | {hit['lat']:.6f},{hit['lon']:.6f}\n"
            
            doc += f"""
================================================================================
NOTES
================================================================================
- All hits verified against DMV database
- Confidence scores based on image quality and plate visibility
- GPS coordinates from camera location metadata
- System precision: {alpr_entity.precision_score:.2%}

Generated by: {alpr_entity.name}
"""
            
            # Apply system errors
            doc = alpr_entity.introduce_error(doc)
            self.case.documents.append(doc)
            
            # Add as evidence
            self.case.add_evidence(Evidence(
                id=fake.uuid4(),
                type=EvidenceType.SURVEILLANCE,
                description=f"ALPR Hits - {num_hits} detections",
                collected_by="ALPR System",
                collected_at=self.case.date_opened,
                location_found="ALPR Network"
            ))
    
    def _generate_random_events(self, modifiers: List[str]):
        """Generate random events like car wrecks after fleeing scene."""
        if "Random Events" not in modifiers:
            return
        
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects or not suspects[0].vehicles:
            return
        
        # 30% chance of random event
        if random.random() < 0.3:
            suspect = suspects[0]
            vehicle = suspect.vehicles[0]
            
            # Generate car wreck after fleeing
            wreck_time = self.crime_datetime + timedelta(
                hours=random.randint(1, 6),
                minutes=random.randint(0, 59)
            )
            
            wreck_location = fake.address().replace('\n', ', ')
            lat, lon = geo_mgr.get_coords_in_radius(
                getattr(suspect, 'latitude', None) or geo_mgr.center_lat,
                getattr(suspect, 'longitude', None) or geo_mgr.center_lon,
                30.0
            )
            
            # Get officer entity for report
            officer = self._get_random_officer()
            
            # Officer might misspell name or misread plate
            suspect_name = officer.misspell_name(suspect.full_name)
            plate_read = officer.misread_plate(vehicle.license_plate)
            
            doc = f"""--- TRAFFIC ACCIDENT REPORT ---
Report #: AR-{fake.random_number(digits=8)}
Date: {wreck_time.strftime('%Y-%m-%d')}
Time: {wreck_time.strftime('%H:%M:%S')}
Location: {wreck_location}
Latitude: {lat:.6f}
Longitude: {lon:.6f}

VEHICLE INFORMATION:
License Plate: {plate_read}
Vehicle: {vehicle.color} {vehicle.make} {vehicle.model}
VIN: {vehicle.vin}
Registered Owner: {suspect_name}

ACCIDENT DETAILS:
Type: Single Vehicle Accident
Severity: {random.choice(['Minor', 'Moderate', 'Major'])}
Cause: {random.choice(['Driver lost control', 'Excessive speed', 'Failed to negotiate curve', 'Avoiding obstacle'])}
Injuries: {random.choice(['None', 'Minor injuries - driver transported', 'Driver refused medical attention'])}
Damage: {random.choice(['Front end damage', 'Side impact', 'Rollover', 'Total loss'])}
Road Conditions: {random.choice(['Dry', 'Wet', 'Icy', 'Snow covered'])}
Weather: {random.choice(['Clear', 'Rain', 'Fog', 'Snow'])}

OFFICER NOTES:
Vehicle found abandoned at scene. Driver fled on foot prior to arrival.
Witnesses report vehicle was traveling at high rate of speed.
Vehicle registration matches suspect vehicle from active investigation.
Evidence collected from scene.

Reporting Officer: {officer.name}
Badge #: {fake.random_number(digits=4)}
Date: {wreck_time.strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            # Apply officer errors
            doc = officer.introduce_error(doc)
            self.case.documents.append(doc)
            
            # Add as evidence
            self.case.add_evidence(Evidence(
                id=fake.uuid4(),
                type=EvidenceType.PHYSICAL,
                description="Vehicle involved in traffic accident after fleeing scene",
                collected_by=officer.name,
                collected_at=wreck_time,
                location_found=wreck_location
            ))
    def _gen_browser_history_doc(self): pass
    def _generate_crypto_forensics(self): 
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        t = suspects[0]
        if t.crypto_wallet: self.case.documents.append(generate_blockchain_ledger(t.crypto_wallet, 1.5))
    def _generate_financial_csv_dump(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        self.case.documents.append(f"--- BANK CSV ---\n{generate_financial_csv(suspects[0].full_name, self.crime_datetime)}")
    def _generate_bsu_profile(self): self.case.documents.append(generate_bau_profile(self.case.crime_type))
    def _generate_dna_phenotype(self): 
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if suspects: self.case.documents.append(generate_dna_phenotype_report(suspects[0]))
    def _generate_recovered_data(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if suspects: self.case.documents.append(generate_recovered_data(suspects[0].last_name))
    def _generate_leads_sheet(self): self.case.documents.append("--- LEADS SHEET ---\n[X] Evidence Compiled.")
    def _generate_uc_report(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        uc = generate_person(Role.UNDERCOVER); self.case.add_person(uc)
        self.case.documents.append(generate_uc_report(uc.full_name, suspects[0].full_name, self.case.date_opened))
    def _generate_wiretaps(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if len(suspects) >= 2: self.case.documents.append(generate_wiretap_transcript(suspects[0].full_name, suspects[1].full_name, self.case.date_opened))
    def _generate_jailhouse_snitch(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if suspects and suspects[0].criminal_history: self.case.documents.append(generate_jailhouse_informant_statement(suspects[0].full_name))
    def _generate_network_hierarchy(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if len(suspects) >= 3: self.case.documents.append(generate_network_map(suspects))
    def _generate_witness_protection(self):
        witnesses = [p for p in self.case.persons if p.role == Role.WITNESS]
        if witnesses and d20() > 15: self.case.documents.append(generate_witsec_profile(witnesses[0]))
    def _generate_ci_paperwork(self):
        if d20() > 12: self.case.documents.append(generate_ci_contract(fake.name(), self.case.reporting_officer.full_name))
    def _generate_phishing_attempt(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if suspects: self.case.documents.append(generate_phishing_log(suspects[0].email, self.case.date_opened - timedelta(days=3)))
    def _generate_pi_surveillance(self):
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if suspects: self.case.documents.append(generate_pi_report(fake.name(), suspects[0].full_name, self.case.date_opened - timedelta(days=5)))
    def _generate_criminal_history_docs(self): 
        for p in self.case.persons:
            if p.criminal_history: self.case.documents.append(generate_ncic_report(p))
    
    # --- SUBJECT STATUS MODIFIERS ---
    
    def _make_subjects_unknown(self):
        """Remove suspect identities - make it an unknown subject case."""
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        for suspect in suspects:
            # Replace name with description
            suspect.first_name = f"UNKNOWN MALE #{random.randint(1, 99)}"
            suspect.last_name = ""
            suspect.notes = f"Subject description: {random.choice(['5\'10\"', '6\'0\"', '5\'8\"'])} {random.choice(['Caucasian', 'Hispanic', 'African American', 'Asian'])} male, {random.choice(['slim', 'average', 'stocky'])} build. {random.choice(['Dark clothing', 'Hoodie', 'Baseball cap'])}."
            # Remove or obscure identifying info
            suspect.email = ""
            suspect.address = "UNKNOWN"
            suspect.phone_number = None
            for dev in suspect.devices:
                dev.phone_number = None
                dev.imei = None
    
    def _make_subjects_partial(self):
        """Partially known subjects - some info available."""
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        for suspect in suspects:
            if random.random() < 0.5:  # 50% chance to obscure
                suspect.first_name = f"John"  # Generic first name
                suspect.last_name = "DOE"  # Placeholder last name
                suspect.notes += " Partial identification - first name only. Last name unknown."
            # Keep some identifiers but remove others
            if random.random() < 0.3:
                suspect.email = ""
            if random.random() < 0.3:
                suspect.phone_number = None

    def _create_investigative_unknown_subjects(self):
        """Create multiple potential suspects for investigative scenarios.

        Instead of a single unknown suspect, create 3-5 potential persons of interest,
        each with varying levels of suspicious activity but no definitive proof.
        This creates realistic investigative challenges where analysts must
        evaluate multiple leads."""
        # Remove the current suspect role
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        for suspect in suspects:
            suspect.role = Role.WITNESS  # Convert to witness - they might be suspects but not confirmed

        # Create 3-5 potential persons of interest
        num_potential_suspects = random.randint(3, 5)

        for i in range(num_potential_suspects):
            # Create a new person with suspicious but inconclusive evidence
            person = generate_person(Role.WITNESS)  # Start as witness, but add suspicious elements

            # Add varying levels of suspicious activity
            suspicion_level = random.random()

            if suspicion_level < 0.3:  # Low suspicion - minor connections
                person.notes = f"Person of interest #{i+1}: Minor connection to incident. " \
                              f"Located in general vicinity around time of crime. " \
                              f"Possible witness or coincidental presence."
                # Add one piece of weak evidence
                if random.random() < 0.5:
                    person.devices.append(generate_device(person.id, "Phone"))
                person.suspicious_activities = ["Proximity to crime scene"]

            elif suspicion_level < 0.7:  # Medium suspicion - some concerning behavior
                person.notes = f"Person of interest #{i+1}: Demonstrated suspicious behavior. " \
                              f"Multiple connections to elements of the case. " \
                              f"Requires further investigation to rule in/out."
                # Add moderate evidence
                person.devices.append(generate_device(person.id, "Phone"))
                if random.random() < 0.6:
                    person.vehicles.append(generate_vehicle(person.id, person.address))
                person.suspicious_activities = random.sample([
                    "Frequent location changes", "Cash transactions", "Late night activity",
                    "Association with known contacts", "Digital footprint in area"
                ], random.randint(1, 3))

            else:  # High suspicion - significant red flags
                person.notes = f"Person of interest #{i+1}: HIGH PRIORITY. " \
                              f"Multiple red flags and connections to case elements. " \
                              f"Strong investigative lead requiring immediate follow-up."
                # Add substantial evidence
                person.devices.append(generate_device(person.id, "Phone"))
                person.vehicles.append(generate_vehicle(person.id, person.address))
                if random.random() < 0.7:
                    person.weapons.append(generate_weapon(person.id))
                person.suspicious_activities = random.sample([
                    "Direct connection to victim", "Financial transactions with suspect",
                    "Digital communications with involved parties", "Physical evidence links",
                    "Alibi inconsistencies", "Prior similar incidents"
                ], random.randint(2, 4))

            # Add to case as person of interest (witness role but with suspicious notes)
            self.case.add_person(person)

        # Add a case note about the investigative approach
        self.case.description += "\n\nINVESTIGATIVE APPROACH: Multiple persons of interest identified. " \
                                "None definitively identified as perpetrator. " \
                                "Requires analysis of multiple leads and elimination of suspects."

    def _create_investigative_known_subjects(self):
        """Create investigative scenario for known subjects.
        
        Even when subject is known, create multiple potential suspects/leads
        to create realistic investigative challenges where analysts must
        evaluate evidence and eliminate false leads."""
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects:
            return
        
        # Keep the primary suspect but add 2-4 additional persons of interest
        primary_suspect = suspects[0]
        num_additional_leads = random.randint(2, 4)
        
        for i in range(num_additional_leads):
            person = generate_person(Role.WITNESS)
            
            # Vary suspicion levels
            suspicion_level = random.random()
            
            if suspicion_level < 0.4:  # Low suspicion - possible alibi witness or red herring
                person.notes = f"Person of interest #{i+1}: Possible connection to case. " \
                              f"Requires verification of alibi and relationship to primary suspect."
                person.suspicious_activities = ["Possible association", "Alibi verification needed"]
            elif suspicion_level < 0.7:  # Medium suspicion - potential accomplice or alternative suspect
                person.notes = f"Person of interest #{i+1}: Multiple connections to case elements. " \
                              f"Could be accomplice or alternative suspect. Requires thorough investigation."
                person.devices.append(generate_device(person.id, "Phone"))
                person.suspicious_activities = random.sample([
                    "Association with primary suspect", "Similar modus operandi",
                    "Financial connections", "Digital communications"
                ], random.randint(1, 2))
            else:  # High suspicion - strong alternative suspect
                person.notes = f"Person of interest #{i+1}: HIGH PRIORITY ALTERNATIVE SUSPECT. " \
                              f"Strong evidence suggesting possible involvement. " \
                              f"Must be thoroughly investigated and ruled in/out."
                person.devices.append(generate_device(person.id, "Phone"))
                person.vehicles.append(generate_vehicle(person.id, person.address))
                person.suspicious_activities = random.sample([
                    "Strong motive", "Opportunity", "Physical evidence links",
                    "Witness identification", "Prior similar crimes"
                ], random.randint(2, 3))
            
            self.case.add_person(person)
        
        # Update case description
        self.case.description += "\n\nINVESTIGATIVE APPROACH: Primary suspect identified, but multiple " \
                                "persons of interest require investigation. Must evaluate all leads " \
                                "and eliminate false suspects through evidence analysis."

    def _create_investigative_partial_subjects(self):
        """Create investigative scenario for partially known subjects.
        
        When subject is partially known, create multiple potential matches
        and leads that require investigation to confirm identity."""
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects:
            return
        
        # Keep partial info but add 2-4 potential matches
        primary_suspect = suspects[0]
        num_potential_matches = random.randint(2, 4)
        
        for i in range(num_potential_matches):
            person = generate_person(Role.WITNESS)
            
            # Match some characteristics of primary suspect
            if random.random() < 0.5:
                person.first_name = primary_suspect.first_name  # Same first name
            if random.random() < 0.5:
                person.age = primary_suspect.age + random.randint(-3, 3)  # Similar age
            if random.random() < 0.5:
                person.build = primary_suspect.build  # Similar build
            
            suspicion_level = random.random()
            
            if suspicion_level < 0.4:  # Low match - weak similarity
                person.notes = f"Potential match #{i+1}: Partial similarity to suspect description. " \
                              f"Requires further investigation to confirm or rule out."
                person.suspicious_activities = ["Partial description match"]
            elif suspicion_level < 0.7:  # Medium match - multiple similarities
                person.notes = f"Potential match #{i+1}: Multiple characteristics match suspect description. " \
                              f"Strong candidate requiring verification."
                person.devices.append(generate_device(person.id, "Phone"))
                person.suspicious_activities = random.sample([
                    "Description match", "Location match", "Timeline match"
                ], random.randint(1, 2))
            else:  # High match - very similar
                person.notes = f"Potential match #{i+1}: HIGH PRIORITY - Strong match to suspect description. " \
                              f"Multiple characteristics align. Requires immediate investigation."
                person.devices.append(generate_device(person.id, "Phone"))
                person.vehicles.append(generate_vehicle(person.id, person.address))
                person.suspicious_activities = random.sample([
                    "Strong description match", "Location and timeline match",
                    "Physical evidence links", "Witness identification"
                ], random.randint(2, 3))
            
            self.case.add_person(person)
        
        # Update case description
        self.case.description += "\n\nINVESTIGATIVE APPROACH: Suspect partially identified. Multiple " \
                                "potential matches identified requiring investigation to confirm " \
                                "correct suspect identity."

    # --- REALISTIC ERROR HANDLING ---
    
    def _add_document_with_errors(self, document: str, doc_id: str, doc_type: str) -> str:
        """
        Add a document to the case with potential error checking.
        Returns the document (possibly modified with errors).
        """
        current_date = datetime.now()
        
        # Check for document errors
        error_msg = self.error_generator.check_document_error(doc_id, doc_type, current_date)
        if error_msg:
            # Find the severity of the error
            for event in self.error_generator.events_log:
                if event.get('item') == doc_id and event.get('type') == EventType.DOCUMENT_ERROR:
                    severity = event.get('severity')
                    document = self.error_generator.apply_error_to_document(document, error_msg, severity)
                    # Add error note to document
                    document = f"[ERROR LOG: {error_msg}]\n\n{document}"
                    break
        
        return document
    
    def _apply_realistic_errors(self):
        """
        Apply realistic errors to already-generated content.
        This simulates errors that occur AFTER content was generated (e.g., evidence misplaced).
        """
        current_date = datetime.now()
        
        # Check for system errors
        system_error = self.error_generator.check_system_error(current_date)
        if system_error:
            self.case.documents.append(f"\n--- SYSTEM ERROR LOG ---\n{system_error}\n")
        
        # Check for environmental events
        env_event = self.error_generator.check_environmental_event(current_date)
        if env_event:
            self.case.documents.append(f"\n--- ENVIRONMENTAL EVENT LOG ---\n{env_event}\n")
        
        # Check for evidence mishandling (affects already-generated evidence)
        for evidence in self.case.evidence:
            error_msg = self.error_generator.check_evidence_error(
                evidence.id, evidence.type.value, current_date
            )
            if error_msg:
                # Add error note to evidence description
                evidence.description += f"\n\n[ERROR LOG: {error_msg}]"
                # If catastrophic, mark evidence as compromised
                for event in self.error_generator.events_log:
                    if (event.get('item') == evidence.id and 
                        event.get('severity') == ErrorSeverity.CATASTROPHIC):
                        evidence.description += "\n[CRITICAL: EVIDENCE INTEGRITY COMPROMISED]"
                        break
        
        # Apply errors to existing documents (simulate corruption after generation)
        for i, doc in enumerate(self.case.documents):
            if isinstance(doc, str) and len(doc) > 100:  # Only process substantial documents
                doc_id = f"DOC-{i+1:03d}"
                # Small chance of late-stage corruption
                if random.random() < 0.02:  # 2% chance
                    error_msg = self.error_generator.check_document_error(
                        doc_id, "Generated Document", current_date
                    )
                    if error_msg:
                        for event in self.error_generator.events_log:
                            if (event.get('item') == doc_id and 
                                event.get('type') == EventType.DOCUMENT_ERROR):
                                severity = event.get('severity')
                                modified_doc = self.error_generator.apply_error_to_document(
                                    doc, error_msg, severity
                                )
                                self.case.documents[i] = modified_doc
                                break

    # --- MASSIVE DATA GENERATORS ---
    
    def _generate_massive_phone_dump(self):
        """Generate MASSIVE phone extraction with thousands of records."""
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        
        target = suspects[0]
        device = target.devices[0] if target.devices else generate_device(target.id, "Phone")
        
        doc = f"""--- MASSIVE PHONE DATA EXTRACTION REPORT ---
Device: {device.make} {device.model if hasattr(device, 'model') else ''}
IMEI: {device.imei or fake.random_number(digits=15, fix_len=True)}
Phone Number: {device.phone_number or fake.phone_number()}
Extraction Date: {self.case.date_opened.strftime('%Y-%m-%d %H:%M:%S')}
Forensic Tool: Cellebrite UFED Physical Analyzer v7.63.0.27
Analyst: Detective {fake.last_name()}
Case Number: {self.case.id}

================================================================================
CALL LOG - {random.randint(5000, 15000)} CALLS
================================================================================
TIME                    | TYPE       | NUMBER           | DURATION | TOWER | LOCATION
------------------------|------------|------------------|----------|-------|------------------
"""
        
        # Generate thousands of calls
        call_count = random.randint(5000, 15000)
        contacts = [fake.phone_number() for _ in range(random.randint(50, 200))]
        
        # Inject scamming operation patterns if hidden gems exist
        scam_victims = []
        scam_associates = []
        trip_dates = None
        if hasattr(self, 'hidden_gems'):
            scam_victims = self.hidden_gems.get('scam_victim_numbers', [])
            scam_associates = self.hidden_gems.get('scam_associate_numbers', [])
            trip_dates = self.hidden_gems.get('trip_dates')
        
        calls_generated = []
        
        for i in range(call_count):
            call_time = self.crime_datetime - timedelta(days=random.randint(0, 90), hours=random.randint(0, 23), minutes=random.randint(0, 59))
            call_type = random.choice(["OUTGOING", "INCOMING", "MISSED"])
            
            # Scamming pattern logic
            if scam_victims and random.random() < 0.05:  # 5% chance for victim pattern
                # Victims: longer calls during specific period (trip dates or crime period)
                call_number = random.choice(scam_victims)
                if trip_dates and trip_dates[0] <= call_time <= trip_dates[1]:
                    # During trip/crime period: longer calls (5-45 minutes)
                    duration_min = random.randint(5, 45)
                    duration_sec = random.randint(0, 59)
                else:
                    # Outside period: shorter calls or missed
                    if random.random() < 0.7:
                        duration_min = random.randint(0, 3)
                        duration_sec = random.randint(0, 59)
                    else:
                        duration_min = 0
                        duration_sec = 0
                        call_type = "MISSED"
            elif scam_associates and random.random() < 0.08:  # 8% chance for associate pattern
                # Associates: short, frequent calls throughout (consistent pattern)
                call_number = random.choice(scam_associates)
                duration_min = random.randint(0, 2)  # Very short calls
                duration_sec = random.randint(0, 30)
            else:
                # Normal noise calls
                call_number = random.choice(contacts) if random.random() < 0.7 else fake.phone_number()
                duration_min = random.randint(0, 5) if random.random() < 0.8 else random.randint(0, 45)
                duration_sec = random.randint(0, 59)
            
            duration = f"{duration_min}:{duration_sec:02d}" if call_type in ["OUTGOING", "INCOMING"] else "-"
            tower = fake.random_number(digits=4)
            lat, lon = geo_mgr.get_coords_in_radius(geo_mgr.center_lat, geo_mgr.center_lon, 20.0)
            calls_generated.append((call_time, call_type, call_number, duration, tower, lat, lon))
        
        # Sort calls by time
        calls_generated.sort(key=lambda x: x[0])
        
        # Write sorted calls
        for call_time, call_type, call_number, duration, tower, lat, lon in calls_generated:
            doc += f"{call_time.strftime('%Y-%m-%d %H:%M:%S')} | {call_type:<10} | {call_number:<16} | {duration:<8} | {tower} | {lat:.4f},{lon:.4f}\n"
        
        doc += f"""
================================================================================
TEXT MESSAGES - {random.randint(8000, 20000)} MESSAGES
================================================================================
TIME                    | TYPE     | NUMBER           | MESSAGE
------------------------|----------|------------------|----------------------------------------
"""
        
        # Generate thousands of text messages
        msg_count = random.randint(8000, 20000)
        messages = [
            "Hey", "What's up", "Call me", "On my way", "Running late", "See you soon",
            "Got it", "Thanks", "OK", "Sure", "Maybe", "Not sure", "Let me know",
            "Where are you?", "What time?", "Can't make it", "Change of plans"
        ]
        
        # Add trip planning messages if hidden gems exist
        trip_messages = []
        if hasattr(self, 'hidden_gems') and self.hidden_gems.get('trip_dates'):
            trip_start, trip_end = self.hidden_gems['trip_dates']
            city = fake.city()
            trip_messages = [
                f"Booked hotel in {city}",
                f"Flight confirmed for {trip_start.strftime('%m/%d')}",
                f"Meeting at {city} on {trip_start.strftime('%m/%d')}",
                f"Driving to {city} tomorrow",
                f"See you in {city}",
                f"Hotel reservation {city}",
                f"GPS says {random.randint(2, 8)} hours to {city}"
            ]
        
        for i in range(msg_count):
            msg_time = self.crime_datetime - timedelta(days=random.randint(0, 90), hours=random.randint(0, 23), minutes=random.randint(0, 59))
            msg_type = random.choice(["SENT", "RECEIVED"])
            msg_number = random.choice(contacts) if random.random() < 0.6 else fake.phone_number()
            
            # 3% chance to inject trip planning message if trip dates are near
            if trip_messages and hasattr(self, 'hidden_gems') and self.hidden_gems.get('trip_dates'):
                trip_start, trip_end = self.hidden_gems['trip_dates']
                if abs((msg_time - trip_start).days) <= 2 and random.random() < 0.03:
                    message = random.choice(trip_messages)
                    # Use associate phone for trip planning
                    if scam_associates:
                        msg_number = random.choice(scam_associates)
                else:
                    message = random.choice(messages)
            else:
                message = random.choice(messages)
            
            doc += f"{msg_time.strftime('%Y-%m-%d %H:%M:%S')} | {msg_type:<8} | {msg_number:<16} | {message}\n"
        
        doc += f"""
================================================================================
CONTACTS - {len(contacts)} ENTRIES
================================================================================
"""
        for contact in contacts[:100]:  # Show first 100
            name = fake.name()
            doc += f"{name:<30} | {contact}\n"
        
        doc += f"\n[Additional {len(contacts)-100} contacts in database...]\n"
        doc += f"\nTotal Records: {call_count + msg_count} entries\n"
        doc += f"File Size: {random.randint(50, 200)} MB\n"
        doc += f"MD5 Hash: {fake.md5()}\n"
        
        self.case.documents.append(doc)
        self.case.add_evidence(Evidence(
            id=fake.uuid4(),
            type=EvidenceType.DIGITAL,
            description=f"Massive Phone Data Extraction ({call_count + msg_count} records)",
            collected_by="Cyber Unit",
            collected_at=self.case.date_opened,
            location_found="Mobile Device"
        ))
    
    def _generate_massive_ip_logs(self):
        """Generate MASSIVE IP/network logs with 10K+ entries."""
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        
        target_ip = suspects[0].devices[0].ip_address if suspects[0].devices and suspects[0].devices[0].ip_address else generate_ip()
        
        doc = f"""--- MASSIVE NETWORK TRAFFIC LOG ---
Source: {fake.company()} Network Firewall
Date Range: {(self.crime_datetime - timedelta(days=30)).strftime('%Y-%m-%d')} to {self.crime_datetime.strftime('%Y-%m-%d')}
Total Entries: {random.randint(10000, 50000)}
Target IP: {target_ip}
Log Type: Firewall/IDS Combined Log
Format: Extended Log Format (ELF)

================================================================================
TIMESTAMP           | SOURCE IP      | DEST IP        | PROTO | PORT | ACTION | BYTES
--------------------|----------------|----------------|-------|------|--------|--------
"""
        
        entry_count = random.randint(10000, 50000)
        suspicious_entries = random.randint(50, 200)  # Actual attack patterns
        
        # Check for VPN drop pattern
        vpn_drop_time = None
        real_ip = None
        vpn_ip = target_ip  # Assume target_ip is the VPN IP
        if hasattr(self, 'hidden_gems') and self.hidden_gems.get('vpn_drop_time'):
            vpn_drop_time = self.hidden_gems['vpn_drop_time']
            real_ip = self.hidden_gems.get('real_ip', generate_ip())
        
        entries_generated = []
        
        # Generate noise entries
        for i in range(entry_count - suspicious_entries):
            log_time = self.crime_datetime - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
            
            # VPN drop detection: single entry showing real IP
            if vpn_drop_time and abs((log_time - vpn_drop_time).total_seconds()) < 60:
                # Within 1 minute of VPN drop - show real IP
                src_ip = real_ip
                note = "[VPN_DISCONNECTED - REAL_IP_EXPOSED]"
            else:
                # Normal VPN IP or random IP
                if random.random() < 0.1:  # 10% of entries from suspect IP (VPN)
                    src_ip = vpn_ip
                    note = ""
                else:
                    src_ip = generate_ip()
                    note = ""
            
            dest_ip = generate_ip()
            proto = random.choice(["TCP", "UDP", "ICMP"])
            port = random.randint(1, 65535)
            action = random.choice(["ALLOW", "DENY", "LOG"])
            bytes_transferred = random.randint(100, 100000)
            entries_generated.append((log_time, src_ip, dest_ip, proto, port, action, bytes_transferred, note))
        
        # Sort entries by time
        entries_generated.sort(key=lambda x: x[0])
        
        # Write sorted entries
        for log_time, src_ip, dest_ip, proto, port, action, bytes_transferred, note in entries_generated:
            doc += f"{log_time.strftime('%Y-%m-%d %H:%M:%S')} | {src_ip:<14} | {dest_ip:<14} | {proto:<5} | {port:<5} | {action:<6} | {bytes_transferred} {note}\n"
        
        # Inject suspicious patterns around crime time
        for _ in range(suspicious_entries):
            log_time = self.crime_datetime + timedelta(minutes=random.randint(-60, 60), seconds=random.randint(0, 59))
            attack_type = random.choice(["PORT_SCAN", "BRUTE_FORCE", "SQL_INJECTION", "DATA_EXFIL"])
            if attack_type == "PORT_SCAN":
                for port in [22, 80, 443, 3389, 8080]:
                    doc += f"{log_time.strftime('%Y-%m-%d %H:%M:%S')} | {target_ip:<14} | {generate_ip():<14} | TCP   | {port:<5} | DENY   | 0 [PORT_SCAN]\n"
            elif attack_type == "BRUTE_FORCE":
                for _ in range(random.randint(10, 30)):
                    doc += f"{log_time.strftime('%Y-%m-%d %H:%M:%S')} | {target_ip:<14} | {generate_ip():<14} | TCP   | 22    | DENY   | 1500 [FAILED_SSH_LOGIN]\n"
            elif attack_type == "DATA_EXFIL":
                doc += f"{log_time.strftime('%Y-%m-%d %H:%M:%S')} | {target_ip:<14} | {generate_ip():<14} | TCP   | 443   | ALLOW  | {random.randint(500000, 5000000)} [DATA_EXFILTRATION]\n"
        
        doc += f"""
================================================================================
SUMMARY STATISTICS
================================================================================
Total Connections: {entry_count}
Allowed: {random.randint(entry_count//2, entry_count*3//4)}
Denied: {random.randint(entry_count//4, entry_count//2)}
Suspicious Activity Detected: {suspicious_entries}
Top Source IPs: {generate_ip()} ({random.randint(100, 1000)} connections)
Top Destination Ports: 443 ({random.randint(500, 2000)}), 80 ({random.randint(300, 1500)})
File Size: {random.randint(100, 500)} MB
MD5 Hash: {fake.md5()}
"""
        
        self.case.documents.append(doc)
        self.case.add_evidence(Evidence(
            id=fake.uuid4(),
            type=EvidenceType.DIGITAL,
            description=f"Massive Network Traffic Log ({entry_count} entries)",
            collected_by="Cyber Unit",
            collected_at=self.case.date_opened,
            location_found="Network Firewall"
        ))
    
    def _generate_massive_financial_records(self):
        """Generate MASSIVE financial records with years of transactions."""
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if not suspects: return
        
        target = suspects[0]
        account = target.bank_accounts[0] if target.bank_accounts else fake.iban()
        
        transaction_count = random.randint(5000, 20000)
        date_start = (self.crime_datetime - timedelta(days=730)).strftime('%Y-%m-%d')
        date_end = self.crime_datetime.strftime('%Y-%m-%d')
        account_type = random.choice(['Checking', 'Savings', 'Business'])
        bank_name = fake.company()
        subpoena_date = self.case.date_opened.strftime('%Y-%m-%d')
        
        doc = f"""--- MASSIVE FINANCIAL RECORDS DUMP ---
Account Holder: {target.full_name}
Account Number: {account}
Bank: {bank_name} Bank
Date Range: {date_start} to {date_end}
Total Transactions: {transaction_count}
Account Type: {account_type}
Subpoena Date: {subpoena_date}

================================================================================
TRANSACTION LOG
================================================================================
DATE       | TYPE        | DESCRIPTION                    | AMOUNT      | BALANCE
-----------|-------------|--------------------------------|-------------|-------------
"""
        
        balance = random.uniform(1000.0, 50000.0)
        starting_balance = balance
        
        merchants = [fake.company() for _ in range(100)]
        transaction_types = ["DEBIT", "CREDIT", "ATM", "TRANSFER", "FEE", "DEPOSIT"]
        
        total_debits = 0.0
        total_credits = 0.0
        transaction_amounts = []
        
        for i in range(transaction_count):
            trans_date = self.crime_datetime - timedelta(days=random.randint(0, 730))
            trans_type = random.choice(transaction_types)
            
            if trans_type == "DEBIT":
                amount = -random.uniform(5.0, 500.0)
                desc = random.choice(merchants)
                total_debits += abs(amount)
            elif trans_type == "CREDIT":
                amount = random.uniform(10.0, 2000.0)
                desc = f"Payment from {fake.company()}"
                total_credits += amount
            elif trans_type == "ATM":
                amount = -random.uniform(20.0, 500.0)
                desc = f"ATM Withdrawal - {fake.city()}"
                total_debits += abs(amount)
            elif trans_type == "TRANSFER":
                amount = random.choice([-random.uniform(100.0, 5000.0), random.uniform(100.0, 5000.0)])
                desc = f"Transfer to/from {fake.iban()}"
                if amount < 0:
                    total_debits += abs(amount)
                else:
                    total_credits += amount
            elif trans_type == "FEE":
                amount = -random.uniform(5.0, 50.0)
                desc = "Monthly Service Fee"
                total_debits += abs(amount)
            else:  # DEPOSIT
                amount = random.uniform(100.0, 5000.0)
                desc = f"Deposit - {fake.company()}"
                total_credits += amount
            
            balance += amount
            transaction_amounts.append(amount)
            doc += f"{trans_date.strftime('%Y-%m-%d')} | {trans_type:<11} | {desc[:30]:<30} | ${amount:>10.2f} | ${balance:>10.2f}\n"
        
        # Calculate summary statistics
        ending_balance = balance
        avg_trans = sum([abs(a) for a in transaction_amounts]) / len(transaction_amounts) if transaction_amounts else 0.0
        file_size = random.randint(10, 50)
        file_hash = fake.md5()
        
        doc += f"""
================================================================================
SUMMARY
================================================================================
Starting Balance: ${starting_balance:,.2f}
Ending Balance: ${ending_balance:,.2f}
Total Debits: ${total_debits:,.2f}
Total Credits: ${total_credits:,.2f}
Average Transaction: ${avg_trans:.2f}
File Size: {file_size} MB
MD5 Hash: {file_hash}
"""
        
        self.case.documents.append(doc)
        self.case.add_evidence(Evidence(
            id=fake.uuid4(),
            type=EvidenceType.FINANCIAL,
            description=f"Massive Financial Records ({transaction_count} transactions)",
            collected_by="Financial Crimes Unit",
            collected_at=self.case.date_opened,
            location_found="Bank Records"
        ))
