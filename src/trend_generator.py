"""
Trend Generator - Creates multiple related cases with shared entities and relationships.
"""
from datetime import datetime, timedelta
import random
from typing import List, Dict, Optional, Tuple

from .models import Case, Person, Role, Vehicle, DigitalDevice
from .generators import CaseGenerator
from .utils import generate_person, generate_vehicle, generate_device, geo_mgr, fake


class TrendRegistry:
    """Manages shared entities and relationships across multiple cases in a trend."""
    
    def __init__(self, trend_id: str):
        self.trend_id = trend_id
        self.shared_entities = {
            'suspects': [],
            'victims': [],
            'witnesses': [],
            'vehicles': [],
            'devices': [],
            'phone_numbers': [],
            'ip_addresses': [],
            'email_addresses': [],
            'bank_accounts': [],
            'locations': []
        }
        self.case_relationships = []
        self.timeline = []
        self.trend_type = None
        
    def add_shared_suspect(self, person: Person, case_ids: List[str]):
        """Add a suspect that appears in multiple cases."""
        self.shared_entities['suspects'].append({
            'person': person,
            'case_ids': case_ids,
            'person_id': person.id
        })
    
    def add_shared_victim(self, person: Person, case_ids: List[str]):
        """Add a victim that appears in multiple cases."""
        self.shared_entities['victims'].append({
            'person': person,
            'case_ids': case_ids,
            'person_id': person.id
        })
    
    def add_shared_vehicle(self, vehicle: Vehicle, case_ids: List[str]):
        """Add a vehicle that appears in multiple cases."""
        self.shared_entities['vehicles'].append({
            'vehicle': vehicle,
            'case_ids': case_ids,
            'vin': vehicle.vin
        })
    
    def add_shared_device(self, device: DigitalDevice, case_ids: List[str]):
        """Add a device that appears in multiple cases."""
        self.shared_entities['devices'].append({
            'device': device,
            'case_ids': case_ids,
            'imei': device.imei,
            'phone_number': device.phone_number,
            'ip_address': device.ip_address
        })
    
    def link_cases(self, case1_id: str, case2_id: str, connection_type: str, details: str = ""):
        """Link two cases with a relationship."""
        self.case_relationships.append({
            'case1': case1_id,
            'case2': case2_id,
            'connection_type': connection_type,
            'details': details
        })
    
    def add_to_timeline(self, case_id: str, crime_date: datetime, crime_type: str):
        """Add a case to the chronological timeline."""
        self.timeline.append({
            'case_id': case_id,
            'crime_date': crime_date,
            'crime_type': crime_type
        })
        self.timeline.sort(key=lambda x: x['crime_date'])


class TrendGenerator:
    """Generates multiple related cases that share entities and relationships."""
    
    # Trend type configuration
    TREND_TYPES = {
        "Serial Offender": {
            "crime_types": ["Burglary", "Robbery", "Assault", "Burglary", "Robbery", "Assault", "Homicide"],
            "time_span_days": (180, 365),
            "case_spacing_days": (14, 42)
        },
        "Organized Crime": {
            "crime_types": ["Fraud", "Robbery", "Drug Possession", "Fraud", "Robbery"],
            "time_span_days": (90, 180),
            "case_spacing_days": (7, 21)
        },
        "Crime Ring": {
            "crime_types": ["Fraud", "Theft", "Drug Possession", "Robbery", "Burglary", "Fraud", "Assault"],
            "time_span_days": (120, 240),
            "case_spacing_days": (10, 30)
        },
        "Victim Pattern": {
            "crime_types": ["Stalking", "Fraud", "Theft", "Burglary", "Assault"],
            "time_span_days": (90, 180),
            "case_spacing_days": (14, 35)
        },
        "Location Pattern": {
            "crime_types": ["Burglary", "Vandalism", "Theft", "Burglary", "Assault"],
            "time_span_days": (60, 120),
            "case_spacing_days": (7, 21)
        }
    }
    
    def __init__(self):
        self.trend_registry = None
        self.case_generator = CaseGenerator()
        self.identification_status = "Identified"
        
    def generate_trend(
        self,
        trend_type: str,
        num_cases: int,
        base_complexity: str,
        base_modifiers: List[str],
        subject_status: str = "Known",
        subject_clarity: str = None,
        identification_status: str = "Identified"
    ) -> Tuple[List[Case], TrendRegistry]:
        """
        Generate a trend of related cases.
        
        Args:
            trend_type: Type of trend pattern
            num_cases: Number of cases to generate
            base_complexity: Complexity level for cases
            base_modifiers: List of modifiers to apply
            subject_status: Known/Unknown/Partially Known
            identification_status: Identified (known links) or Unidentified (hidden links)
        """
        trend_id = f"TREND-{random.randint(100000, 999999)}"
        self.trend_registry = TrendRegistry(trend_id)
        self.trend_registry.trend_type = trend_type
        self.identification_status = identification_status
        
        # Generate cases based on trend type
        trend_generators = {
            "Serial Offender": self._generate_serial_offender_trend,
            "Organized Crime": self._generate_organized_crime_trend,
            "Crime Ring": self._generate_crime_ring_trend,
            "Victim Pattern": self._generate_victim_pattern_trend,
            "Location Pattern": self._generate_location_pattern_trend,
            "Mixed": self._generate_mixed_trend
        }
        
        generator = trend_generators.get(trend_type, self._generate_mixed_trend)
        cases = generator(num_cases, base_complexity, base_modifiers, subject_status)
        
        # Generate master investigation file (only for Identified trends)
        if identification_status == "Identified":
            master_case = self._generate_master_investigation_file(cases)
            cases.append(master_case)
        
        return cases, self.trend_registry
    
    # ========== TREND GENERATION METHODS ==========
    
    def _generate_serial_offender_trend(
        self,
        num_cases: int,
        complexity: str,
        modifiers: List[str],
        subject_status: str
    ) -> List[Case]:
        """Generate cases with same suspect committing multiple crimes."""
        serial_suspect = self._create_equipped_suspect(min_age=25, max_age=45)
        config = self.TREND_TYPES["Serial Offender"]
        start_date = datetime.now() - timedelta(days=random.randint(*config["time_span_days"]))
        
        cases = []
        for i in range(num_cases):
            crime_type = config["crime_types"][min(i, len(config["crime_types"]) - 1)]
            crime_date = start_date + timedelta(days=i * random.randint(*config["case_spacing_days"]))
            
            case = self._generate_related_case(
                crime_type=crime_type,
                complexity=complexity,
                modifiers=modifiers,
                subject_status=subject_status,
                subject_clarity=subject_clarity,
                shared_suspect=serial_suspect,
                crime_date=crime_date,
                case_number=i + 1
            )
            
            cases.append(case)
            # Add suspect to registry (accumulate case IDs)
            existing_entry = next((e for e in self.trend_registry.shared_entities['suspects'] 
                                 if e['person_id'] == serial_suspect.id), None)
            if existing_entry:
                existing_entry['case_ids'].append(case.id)
            else:
                self.trend_registry.add_shared_suspect(serial_suspect, [case.id])
            self.trend_registry.add_to_timeline(case.id, crime_date, crime_type)
            
            # Link cases if Identified
            if i > 0 and self.identification_status == "Identified":
                self.trend_registry.link_cases(
                    cases[i-1].id, case.id, "Same Suspect",
                    f"Suspect {serial_suspect.full_name} appears in both cases"
                )
        
        return cases
    
    def _generate_organized_crime_trend(
        self,
        num_cases: int,
        complexity: str,
        modifiers: List[str],
        subject_status: str
    ) -> List[Case]:
        """Generate cases with multiple suspects working together."""
        num_members = random.randint(3, 5)
        organization = [self._create_equipped_suspect(min_age=28, max_age=50) for _ in range(num_members)]
        shared_vehicle = generate_vehicle(organization[0].id, organization[0].address)
        shared_phone = generate_device(organization[0].id, "Phone")
        
        config = self.TREND_TYPES["Organized Crime"]
        start_date = datetime.now() - timedelta(days=random.randint(*config["time_span_days"]))
        
        cases = []
        for i in range(num_cases):
            crime_type = config["crime_types"][i % len(config["crime_types"])]
            crime_date = start_date + timedelta(days=i * random.randint(*config["case_spacing_days"]))
            case_members = random.sample(organization, k=random.randint(2, min(3, len(organization))))

            case = self._generate_related_case(
                crime_type=crime_type,
                complexity=complexity,
                modifiers=modifiers,
                subject_status=subject_status,
                subject_clarity=subject_clarity,
                shared_suspects=case_members,
                shared_vehicle=shared_vehicle if random.random() < 0.6 else None,
                shared_device=shared_phone if random.random() < 0.5 else None,
                crime_date=crime_date,
                case_number=i + 1
            )
            
            cases.append(case)
            for member in case_members:
                self.trend_registry.add_shared_suspect(member, [case.id])
            if shared_vehicle:
                self.trend_registry.add_shared_vehicle(shared_vehicle, [case.id])
            if shared_phone:
                self.trend_registry.add_shared_device(shared_phone, [case.id])
            
            self.trend_registry.add_to_timeline(case.id, crime_date, crime_type)
            
            # Link cases if Identified
            if i > 0 and self.identification_status == "Identified":
                for prev_case in cases[:i]:
                    self.trend_registry.link_cases(
                        prev_case.id, case.id, "Shared Suspects",
                        "Multiple organization members appear in both cases"
                    )
        
        return cases
    
    def _generate_crime_ring_trend(
        self,
        num_cases: int,
        complexity: str,
        modifiers: List[str],
        subject_status: str
    ) -> List[Case]:
        """Generate cases with network of suspects, various crime types."""
        num_members = random.randint(5, 8)
        ring_members = [self._create_equipped_suspect(min_age=22, max_age=55) for _ in range(num_members)]
        shared_accounts = [fake.iban() for _ in range(random.randint(2, 4))]
        shared_phones = [generate_device(ring_members[0].id, "Phone") for _ in range(random.randint(2, 3))]
        
        config = self.TREND_TYPES["Crime Ring"]
        start_date = datetime.now() - timedelta(days=random.randint(*config["time_span_days"]))
        
        cases = []
        for i in range(num_cases):
            crime_type = config["crime_types"][i % len(config["crime_types"])]
            crime_date = start_date + timedelta(days=i * random.randint(*config["case_spacing_days"]))
            case_members = random.sample(ring_members, k=random.randint(1, 3))
            
            shared_account = random.choice(shared_accounts) if random.random() < 0.4 else None
            shared_devices = random.sample(shared_phones, k=random.randint(1, 2)) if random.random() < 0.5 else []

            case = self._generate_related_case(
                crime_type=crime_type,
                complexity=complexity,
                modifiers=modifiers,
                subject_status=subject_status,
                subject_clarity=subject_clarity,
                shared_suspects=case_members,
                shared_accounts=[shared_account] if shared_account else [],
                shared_devices=shared_devices,
                crime_date=crime_date,
                case_number=i + 1
            )
            
            cases.append(case)
            for member in case_members:
                self.trend_registry.add_shared_suspect(member, [case.id])
            for device in shared_devices:
                self.trend_registry.add_shared_device(device, [case.id])
            
            self.trend_registry.add_to_timeline(case.id, crime_date, crime_type)
        
        return cases
    
    def _generate_victim_pattern_trend(
        self,
        num_cases: int,
        complexity: str,
        modifiers: List[str],
        subject_status: str
    ) -> List[Case]:
        """Generate cases where same victim is targeted multiple times."""
        repeat_victim = generate_person(Role.VICTIM, min_age=30, max_age=70)
        repeat_victim.devices = [generate_device(repeat_victim.id, "Phone")]
        if not repeat_victim.email:
            repeat_victim.email = f"{repeat_victim.first_name.lower()}.{repeat_victim.last_name.lower()}@{fake.domain_name()}"
        
        config = self.TREND_TYPES["Victim Pattern"]
        start_date = datetime.now() - timedelta(days=random.randint(*config["time_span_days"]))
        
        cases = []
        for i in range(num_cases):
            crime_type = config["crime_types"][i % len(config["crime_types"])]
            crime_date = start_date + timedelta(days=i * random.randint(*config["case_spacing_days"]))
            
            case = self._generate_related_case(
                crime_type=crime_type,
                complexity=complexity,
                modifiers=modifiers,
                subject_status=subject_status,
                subject_clarity=subject_clarity,
                shared_victim=repeat_victim,
                crime_date=crime_date,
                case_number=i + 1
            )
            
            cases.append(case)
            # Accumulate case IDs for shared victim
            existing_entry = next((e for e in self.trend_registry.shared_entities['victims'] 
                                 if e['person_id'] == repeat_victim.id), None)
            if existing_entry:
                existing_entry['case_ids'].append(case.id)
            else:
                self.trend_registry.add_shared_victim(repeat_victim, [case.id])
            self.trend_registry.add_to_timeline(case.id, crime_date, crime_type)
            
            # Link cases if Identified
            if i > 0 and self.identification_status == "Identified":
                self.trend_registry.link_cases(
                    cases[i-1].id, case.id, "Same Victim",
                    f"Victim {repeat_victim.full_name} targeted in both cases"
                )
        
        return cases
    
    def _generate_location_pattern_trend(
        self,
        num_cases: int,
        complexity: str,
        modifiers: List[str],
        subject_status: str
    ) -> List[Case]:
        """Generate cases at same/similar locations."""
        base_location = fake.address().replace('\n', ', ')
        base_lat, base_lon = geo_mgr.get_random_city_location()
        
        self.trend_registry.shared_entities['locations'].append({
            'address': base_location,
            'lat': base_lat,
            'lon': base_lon,
            'case_ids': []
        })
        
        config = self.TREND_TYPES["Location Pattern"]
        start_date = datetime.now() - timedelta(days=random.randint(*config["time_span_days"]))
        
        cases = []
        for i in range(num_cases):
            crime_type = config["crime_types"][i % len(config["crime_types"])]
            crime_date = start_date + timedelta(days=i * random.randint(*config["case_spacing_days"]))
            location_variation = geo_mgr.get_coords_in_radius(base_lat, base_lon, 0.1)
            
            case = self._generate_related_case(
                crime_type=crime_type,
                complexity=complexity,
                modifiers=modifiers,
                subject_status=subject_status,
                subject_clarity=subject_clarity,
                fixed_location=base_location,
                fixed_coords=location_variation,
                crime_date=crime_date,
                case_number=i + 1
            )
            
            cases.append(case)
            self.trend_registry.shared_entities['locations'][0]['case_ids'].append(case.id)
            self.trend_registry.add_to_timeline(case.id, crime_date, crime_type)
            
            # Link cases if Identified
            if i > 0 and self.identification_status == "Identified":
                self.trend_registry.link_cases(
                    cases[i-1].id, case.id, "Same Location",
                    f"Both crimes occurred at/near {base_location}"
                )
        
        return cases
    
    def _generate_mixed_trend(
        self,
        num_cases: int,
        complexity: str,
        modifiers: List[str],
        subject_status: str
    ) -> List[Case]:
        """Generate cases with mixed patterns."""
        shared_suspect = self._create_equipped_suspect(min_age=30, max_age=45)
        shared_victim = generate_person(Role.VICTIM, min_age=35, max_age=65)
        shared_location = fake.address().replace('\n', ', ')
        
        start_date = datetime.now() - timedelta(days=random.randint(180, 365))
        crime_types = ["Burglary", "Robbery", "Fraud", "Assault", "Theft", "Burglary"]
        
        cases = []
        for i in range(num_cases):
            crime_type = crime_types[i % len(crime_types)]
            crime_date = start_date + timedelta(days=i * random.randint(14, 42))
            pattern = random.choice(["suspect", "victim", "location", "none"])
            
            if pattern == "suspect" and random.random() < 0.6:
                case = self._generate_related_case(
                    crime_type, complexity, modifiers, subject_status, subject_clarity,
                    shared_suspect=shared_suspect, crime_date=crime_date, case_number=i + 1
                )
                self.trend_registry.add_shared_suspect(shared_suspect, [case.id])
            elif pattern == "victim" and random.random() < 0.5:
                case = self._generate_related_case(
                    crime_type, complexity, modifiers, subject_status, subject_clarity,
                    shared_victim=shared_victim, crime_date=crime_date, case_number=i + 1
                )
                # Accumulate case IDs
                existing_entry = next((e for e in self.trend_registry.shared_entities['victims'] 
                                     if e['person_id'] == shared_victim.id), None)
                if existing_entry:
                    existing_entry['case_ids'].append(case.id)
                else:
                    self.trend_registry.add_shared_victim(shared_victim, [case.id])
            elif pattern == "location":
                case = self._generate_related_case(
                    crime_type, complexity, modifiers, subject_status, subject_clarity,
                    fixed_location=shared_location, crime_date=crime_date, case_number=i + 1
                )
            else:
                case = self._generate_related_case(
                    crime_type, complexity, modifiers, subject_status, subject_clarity,
                    crime_date=crime_date, case_number=i + 1
                )
            
            cases.append(case)
            self.trend_registry.add_to_timeline(case.id, crime_date, crime_type)
        
        return cases
    
    # ========== HELPER METHODS ==========
    
    def _create_equipped_suspect(self, min_age: int = 25, max_age: int = 50) -> Person:
        """Create a suspect with vehicles, devices, email, and bank accounts."""
        suspect = generate_person(Role.SUSPECT, min_age=min_age, max_age=max_age)
        suspect.vehicles = [generate_vehicle(suspect.id, suspect.address)]
        suspect.devices = [generate_device(suspect.id, "Phone")]
        if not suspect.email:
            suspect.email = f"{suspect.first_name.lower()}.{suspect.last_name.lower()}@{fake.domain_name()}"
        if not suspect.bank_accounts:
            suspect.bank_accounts = [fake.iban()]
        return suspect
    
    def _get_suspects(self, case: Case) -> List[Person]:
        """Get all suspects from a case."""
        return [p for p in case.persons if p.role == Role.SUSPECT]
    
    def _get_victims(self, case: Case) -> List[Person]:
        """Get all victims from a case."""
        return [p for p in case.persons if p.role == Role.VICTIM]
    
    def _inject_shared_suspect(self, case: Case, suspect: Person):
        """Replace first suspect with shared suspect and copy assets."""
        existing = self._get_suspects(case)
        if existing:
            case.persons.remove(existing[0])
        case.add_person(suspect)
        # Copy assets to the person in the case
        person_in_case = next((p for p in case.persons if p.id == suspect.id), None)
        if person_in_case:
            person_in_case.vehicles = suspect.vehicles.copy() if suspect.vehicles else []
            person_in_case.devices = suspect.devices.copy() if suspect.devices else []
    
    def _inject_shared_suspects(self, case: Case, suspects: List[Person]):
        """Replace all suspects with shared suspects."""
        existing = self._get_suspects(case)
        for s in existing:
            case.persons.remove(s)
        for s in suspects:
            case.add_person(s)
    
    def _inject_shared_victim(self, case: Case, victim: Person):
        """Replace first victim with shared victim."""
        existing = self._get_victims(case)
        if existing:
            case.persons.remove(existing[0])
        case.add_person(victim)
    
    def _inject_shared_assets(self, case: Case, vehicle: Optional[Vehicle] = None,
                             device: Optional[DigitalDevice] = None,
                             devices: Optional[List[DigitalDevice]] = None,
                             accounts: Optional[List[str]] = None):
        """Inject shared vehicles, devices, or accounts into first suspect."""
        suspects = self._get_suspects(case)
        if not suspects:
            return
        
        target = suspects[0]
        if vehicle:
            target.vehicles = [vehicle]
        if device:
            target.devices = [device]
        if devices:
            target.devices = devices
        if accounts:
            target.bank_accounts = accounts
    
    def _generate_related_case(
        self,
        crime_type: str,
        complexity: str,
        modifiers: List[str],
        subject_status: str,
        subject_clarity: str = None,
        crime_date: datetime = None,
        case_number: int = 1,
        shared_suspect: Optional[Person] = None,
        shared_suspects: Optional[List[Person]] = None,
        shared_victim: Optional[Person] = None,
        shared_vehicle: Optional[Vehicle] = None,
        shared_device: Optional[DigitalDevice] = None,
        shared_devices: Optional[List[DigitalDevice]] = None,
        shared_accounts: Optional[List[str]] = None,
        fixed_location: Optional[str] = None,
        fixed_coords: Optional[Tuple[float, float]] = None
    ) -> Case:
        """Generate a single case with shared entities."""
        # Generate base case
        case = self.case_generator.generate_case(crime_type, complexity, modifiers, subject_status, subject_clarity)
        
        # Override crime date
        if crime_date:
            case.date_opened = datetime.now()
            if case.incident_report:
                case.incident_report.incident_date = crime_date
        
        # Inject shared entities
        if shared_suspect:
            self._inject_shared_suspect(case, shared_suspect)
        elif shared_suspects:
            self._inject_shared_suspects(case, shared_suspects)
        
        if shared_victim:
            self._inject_shared_victim(case, shared_victim)
        
        self._inject_shared_assets(
            case, shared_vehicle, shared_device, shared_devices, shared_accounts
        )
        
        # Set fixed location
        if fixed_location and case.incident_report:
            case.incident_report.incident_location = fixed_location
            if fixed_coords:
                case.incident_report.latitude = str(fixed_coords[0])
                case.incident_report.longitude = str(fixed_coords[1])
        
        # Update case title and add investigation notes based on identification status
        if self.identification_status == "Identified":
            case.title = f"{case.title} [Trend Case #{case_number} - Linked Investigation]"
            if case_number > 1:
                investigation_note = f"""
--- INVESTIGATION NOTE ---
Case #{case_number} in suspected linked series.
Investigating potential connections to previous cases.
Pattern analysis ongoing.
"""
                case.documents.append(investigation_note)
        # For Unidentified, keep original title (cases appear independent)
        
        return case
    
    def _generate_master_investigation_file(self, cases: List[Case]) -> Case:
        """Generate a master investigation file that links all cases in the trend."""
        trend_id = self.trend_registry.trend_id
        master_id = f"{trend_id}-MASTER"
        
        # Create master case
        master_case = Case(
            id=master_id,
            title=f"Master Investigation - {self.trend_registry.trend_type} Trend {trend_id}",
            description=f"Master investigation file linking {len(cases)} related cases. Cases are suspected to be linked but connections require proof.",
            crime_type="Multi-Case Investigation",
            complexity="High",
            date_opened=datetime.now(),
            status="OPEN",
            modifiers=[]
        )
        
        # Aggregate all persons from all cases (preserving physical descriptions and driver's license info)
        aggregated_persons = self._aggregate_persons_across_cases(cases)
        for person in aggregated_persons:
            master_case.add_person(person)
        
        # Aggregate all vehicles and link to owners
        aggregated_vehicles = self._aggregate_vehicles_across_cases(cases)
        for vehicle in aggregated_vehicles:
            # Find owner if owner_id is set
            if vehicle.owner_id:
                for person in master_case.persons:
                    if person.id == vehicle.owner_id:
                        if vehicle not in person.vehicles:
                            person.vehicles.append(vehicle)
                        break
        
        # Generate master investigation document
        doc = self._build_master_investigation_document(cases)
        master_case.documents.append(doc)
        
        return master_case
    
    def _aggregate_persons_across_cases(self, cases: List[Case]) -> List[Person]:
        """Aggregate persons across all cases, merging data and preserving physical descriptions."""
        person_map = {}  # full_name -> Person
        
        for case in cases:
            for person in case.persons:
                key = person.full_name.lower()
                if key not in person_map:
                    # First occurrence - add to map
                    person_map[key] = person
                else:
                    # Person already exists - merge data (preserve most complete data)
                    existing = person_map[key]
                    # Merge physical descriptions (prefer non-empty values)
                    if not existing.height and person.height:
                        existing.height = person.height
                    if not existing.weight and person.weight > 0:
                        existing.weight = person.weight
                    if not existing.hair_color and person.hair_color:
                        existing.hair_color = person.hair_color
                    if not existing.eye_color and person.eye_color:
                        existing.eye_color = person.eye_color
                    if not existing.facial_hair and person.facial_hair:
                        existing.facial_hair = person.facial_hair
                    if not existing.build and person.build:
                        existing.build = person.build
                    if not existing.gender and person.gender:
                        existing.gender = person.gender
                    # Merge driver's license (prefer non-empty)
                    if not existing.driver_license_number and person.driver_license_number:
                        existing.driver_license_number = person.driver_license_number
                        existing.driver_license_state = person.driver_license_state
                    # Merge other data
                    if not existing.email and person.email:
                        existing.email = person.email
                    if not existing.address and person.address:
                        existing.address = person.address
                    if not existing.phone_number and person.phone_number:
                        existing.phone_number = person.phone_number
                    # Merge aliases
                    for alias in person.aliases:
                        if alias not in existing.aliases:
                            existing.aliases.append(alias)
                    # Merge vehicles
                    for vehicle in person.vehicles:
                        if vehicle not in existing.vehicles:
                            existing.vehicles.append(vehicle)
                    # Merge devices
                    for device in person.devices:
                        if device not in existing.devices:
                            existing.devices.append(device)
                    # Merge criminal history
                    for history in person.criminal_history:
                        if history not in existing.criminal_history:
                            existing.criminal_history.append(history)
        
        return list(person_map.values())
    
    def _aggregate_vehicles_across_cases(self, cases: List[Case]) -> List[Vehicle]:
        """Aggregate vehicles across all cases."""
        vehicle_map = {}  # license_plate -> Vehicle
        
        for case in cases:
            for person in case.persons:
                for vehicle in person.vehicles:
                    if vehicle.license_plate and vehicle.license_plate not in vehicle_map:
                        vehicle_map[vehicle.license_plate] = vehicle
        
        return list(vehicle_map.values())
    
    def _build_master_investigation_document(self, cases: List[Case]) -> str:
        """Build the master investigation document content."""
        trend_id = self.trend_registry.trend_id
        
        doc = f"""--- MASTER INVESTIGATION FILE ---
TREND ID: {trend_id}
TREND TYPE: {self.trend_registry.trend_type}
IDENTIFICATION STATUS: IDENTIFIED (Suspected Links - Proof Required)
DATE CREATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
INVESTIGATING AGENCY: {fake.company()} Police Department
CASE COUNT: {len(cases)} related cases

================================================================================
EXECUTIVE SUMMARY
================================================================================

This master investigation file consolidates {len(cases)} related cases that have been
identified as part of a {self.trend_registry.trend_type} pattern. Analysis of these cases
reveals significant connections through shared entities, locations, and modus operandi.

*** IMPORTANT: While connections are suspected, definitive proof linking these cases
is still being established. This investigation aims to build the evidentiary chain
necessary to prove the relationships between cases.

INVESTIGATION STATUS: ACTIVE - BUILDING CASE FOR LINKAGE
PRIORITY: HIGH
ASSIGNED DETECTIVES: {fake.first_name()} {fake.last_name()}, {fake.first_name()} {fake.last_name()}

================================================================================
TIMELINE OF CASES
================================================================================
"""
        
        for i, timeline_entry in enumerate(self.trend_registry.timeline, 1):
            doc += f"""
{i}. CASE {timeline_entry['case_id']}
   Date: {timeline_entry['crime_date'].strftime('%Y-%m-%d %H:%M')}
   Type: {timeline_entry['crime_type']}
   Status: OPEN
"""
        
        doc += self._build_shared_entities_section()
        doc += self._build_case_relationships_section()
        doc += self._build_investigative_notes_section(cases)
        
        return doc
    
    def _build_shared_entities_section(self) -> str:
        """Build the shared entities analysis section."""
        doc = f"""
================================================================================
SHARED ENTITIES ANALYSIS
================================================================================

SUSPECTS APPEARING IN MULTIPLE CASES:
"""
        for suspect_entry in self.trend_registry.shared_entities['suspects']:
            person = suspect_entry['person']
            case_ids = suspect_entry['case_ids']
            doc += f"""
- {person.full_name} (Age: {person.age}, DOB: {fake.date_of_birth(minimum_age=person.age, maximum_age=person.age).strftime('%Y-%m-%d')})
  Gender: {person.gender.title() if person.gender else 'Unknown'}
  Phone: {person.phone_number}
  Email: {person.email if person.email else 'N/A'}
  Address: {person.address}
  Physical Description: {person.physical_description if person.physical_description != 'Description not available' else 'Not available'}
  Driver's License: {person.driver_license_number} ({person.driver_license_state}) if person.driver_license_number else 'Not on file'
  Appears in Cases: {', '.join(case_ids)}
  Vehicles: {', '.join([f'{v.year} {v.make} {v.model} ({v.license_plate})' for v in person.vehicles]) if person.vehicles else 'None'}
  Devices: {', '.join([d.phone_number or d.imei for d in person.devices if d.phone_number or d.imei]) if person.devices else 'None'}
"""
        
        if self.trend_registry.shared_entities['victims']:
            doc += f"""
VICTIMS APPEARING IN MULTIPLE CASES:
"""
            for victim_entry in self.trend_registry.shared_entities['victims']:
                person = victim_entry['person']
                case_ids = victim_entry['case_ids']
                doc += f"""
- {person.full_name}
  Phone: {person.phone_number}
  Appears in Cases: {', '.join(case_ids)}
"""
        
        if self.trend_registry.shared_entities['vehicles']:
            doc += f"""
VEHICLES APPEARING IN MULTIPLE CASES:
"""
            for vehicle_entry in self.trend_registry.shared_entities['vehicles']:
                vehicle = vehicle_entry['vehicle']
                case_ids = vehicle_entry['case_ids']
                doc += f"""
- {vehicle.color} {vehicle.make} {vehicle.model} ({vehicle.year})
  License Plate: {vehicle.license_plate}
  VIN: {vehicle.vin}
  Appears in Cases: {', '.join(case_ids)}
"""
        
        if self.trend_registry.shared_entities['devices']:
            doc += f"""
DEVICES APPEARING IN MULTIPLE CASES:
"""
            for device_entry in self.trend_registry.shared_entities['devices']:
                device = device_entry['device']
                case_ids = device_entry['case_ids']
                doc += f"""
- {device.type} - {device.make}
  Phone: {device.phone_number or 'N/A'}
  IMEI: {device.imei or 'N/A'}
  IP: {device.ip_address or 'N/A'}
  Appears in Cases: {', '.join(case_ids)}
"""
        
        return doc
    
    def _build_case_relationships_section(self) -> str:
        """Build the case relationships section."""
        doc = f"""
================================================================================
CASE RELATIONSHIPS
================================================================================
"""
        for rel in self.trend_registry.case_relationships:
            doc += f"""
- {rel['case1']} <-> {rel['case2']}
  Connection: {rel['connection_type']}
  Details: {rel['details']}
"""
        return doc
    
    def _build_investigative_notes_section(self, cases: List[Case]) -> str:
        """Build the investigative notes and next steps section."""
        time_span = (self.trend_registry.timeline[-1]['crime_date'] - 
                    self.trend_registry.timeline[0]['crime_date']).days if len(self.trend_registry.timeline) > 1 else 0
        
        doc = f"""
================================================================================
INVESTIGATIVE NOTES
================================================================================

Pattern Analysis:
- Total Cases: {len(cases)}
- Time Span: {time_span} days
- Shared Suspects: {len(self.trend_registry.shared_entities['suspects'])}
- Shared Victims: {len(self.trend_registry.shared_entities['victims'])}
- Shared Vehicles: {len(self.trend_registry.shared_entities['vehicles'])}
- Shared Devices: {len(self.trend_registry.shared_entities['devices'])}

Recommended Actions:
1. Cross-reference all cases for additional connections
2. Analyze timeline for escalation patterns
3. Review shared entity communications and movements
4. Coordinate with other jurisdictions if applicable
5. Consider task force formation for complex pattern

NEXT STEPS:
- Build evidentiary chain proving case connections
- Obtain warrants for cross-case evidence collection
- Interview shared entities about multiple incidents
- Financial investigation of shared accounts
- Digital forensics on shared devices
- Geographic analysis of crime locations
- Present findings to prosecutor for charging decisions

================================================================================
"""
        return doc
