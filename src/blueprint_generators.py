"""
Blueprint-based document generators following real law enforcement document formats.
Based on fabrication blueprints from actual case files.
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from faker import Faker
from .date_formatter import DateFormatter
from .realistic_errors import RealisticErrorGenerator, ErrorSeverity, EventType

# Import roll_check - handle circular import
try:
    from .utils import roll_check
except ImportError:
    # Fallback if circular import
    def roll_check(threshold: int, modifier: int = 0) -> bool:
        import random
        return (random.randint(1, 20) + modifier) >= threshold

fake = Faker()


class RMSIncidentReportGenerator:
    """Generates RMS-style incident reports following blueprint specifications."""
    
    def __init__(self, case, crime_datetime: datetime, entities: Dict):
        self.case = case
        self.crime_datetime = crime_datetime
        self.entities = entities
        self.incident_number = f"{fake.random_number(digits=6)}"
        self.report_date = crime_datetime + timedelta(hours=random.randint(1, 6))
        self.error_gen = RealisticErrorGenerator(incident_date=crime_datetime)
        self.jurisdiction = self._get_jurisdiction()
        
    def generate(self) -> str:
        """Generate a complete RMS-style incident report with multi-page support."""
        doc = []
        current_page = 1
        
        # Header section (repeated on each page)
        header = self._generate_header()
        doc.append(header)
        doc.append("")
        
        # Victims section (comes before suspects in RMS format)
        victims = [p for p in self.case.persons if p.role.value == "Victim"]
        if victims:
            victims_section = self._generate_victims_section(victims)
            doc.append(victims_section)
            doc.append("")
        
        # Suspects section
        suspects = [p for p in self.case.persons if p.role.value == "Suspect"]
        if suspects:
            suspects_section = self._generate_suspects_section(suspects)
            doc.append(suspects_section)
            doc.append("")
        
        # Event/Location section
        doc.append(self._generate_event_section())
        doc.append("")
        
        # Incident metadata
        doc.append(self._generate_incident_metadata())
        doc.append("")
        
        # Check if we need a page break before narrative
        content_lines = len("\n".join(doc).split('\n'))
        if content_lines > 40:  # Approximate lines per page
            doc.append(self._generate_page_break(current_page + 1))
            current_page += 1
        
        # Narrative section
        narrative = self._generate_narrative_section()
        doc.append(narrative)
        doc.append("")
        
        # Add footer if multi-page
        if current_page > 1:
            doc.append(self._generate_footer())
        
        return "\n".join(doc)
    
    def _generate_page_break(self, page_num: int) -> str:
        """Generate page break with header repeated."""
        header = self._generate_header().replace("Page: 1", f"Page: {page_num}")
        return f"\n\n{header}\n"
    
    def _generate_footer(self) -> str:
        """Generate footer with agency info."""
        agency_name = random.choice([
            "RICHLAND COUNTY SHERIFF'S DEPARTMENT",
            "COLUMBIA POLICE DEPARTMENT",
            "MUNICIPAL POLICE DEPARTMENT",
            "COUNTY SHERIFF'S OFFICE"
        ])
        return f"\n\n{agency_name}\nCase Number: {self.incident_number}"
    
    def _get_jurisdiction(self) -> Dict:
        """Get jurisdiction-specific formatting."""
        jurisdictions = {
            "South Carolina": {
                "state_abbr": "SC",
                "court_system": "COURT OF GENERAL SESSIONS",
                "statute_prefix": "SC §",
                "common_agencies": [
                    "RICHLAND COUNTY SHERIFF'S DEPARTMENT",
                    "COLUMBIA POLICE DEPARTMENT",
                    "CHARLESTON POLICE DEPARTMENT"
                ]
            },
            "California": {
                "state_abbr": "CA",
                "court_system": "SUPERIOR COURT",
                "statute_prefix": "Cal. Penal Code §",
                "common_agencies": [
                    "LOS ANGELES POLICE DEPARTMENT",
                    "SAN FRANCISCO POLICE DEPARTMENT",
                    "SAN DIEGO COUNTY SHERIFF'S DEPARTMENT"
                ]
            },
            "Texas": {
                "state_abbr": "TX",
                "court_system": "DISTRICT COURT",
                "statute_prefix": "Tex. Penal Code §",
                "common_agencies": [
                    "HOUSTON POLICE DEPARTMENT",
                    "DALLAS POLICE DEPARTMENT",
                    "TRAVIS COUNTY SHERIFF'S OFFICE"
                ]
            }
        }
        # Default to South Carolina (most common in blueprints)
        return random.choice(list(jurisdictions.values()))
    
    def _generate_header(self) -> str:
        """Generate RMS header with agency info and jurisdiction-specific formatting."""
        agency_name = random.choice(self.jurisdiction["common_agencies"])
        
        street = fake.street_address()
        city = fake.city()
        city_state = f"{city}, {self.jurisdiction['state_abbr']} {fake.zipcode()}"
        phone = f"({fake.random_number(digits=3)}) {fake.random_number(digits=3)}-{fake.random_number(digits=4)}"
        
        header = f"{agency_name}"
        header += f"\n{street}"
        header += f"\n{city_state}"
        header += f"\n{phone}"
        header += f"\n\nCase Number: {self.incident_number}                    Page: 1"
        
        # Apply minor errors using roll system
        if roll_check(18):  # 15% chance (d20 >= 18)
            # Simple typo: swap adjacent characters occasionally
            if len(header) > 20 and roll_check(14):  # 35% chance if error occurs
                chars = list(header)
                idx = random.randint(0, len(chars) - 2)
                chars[idx], chars[idx + 1] = chars[idx + 1], chars[idx]
                header = ''.join(chars)
        
        return header
    
    def _generate_suspects_section(self, suspects: List) -> str:
        """Generate suspects section in RMS format with detailed fields."""
        section = f"Suspects ({len(suspects)})"
        
        for i, suspect in enumerate(suspects, 1):
            # Name - often "Unknown" for suspects (use roll system)
            if roll_check(16):  # 25% chance unknown (d20 >= 16 = 25%)
                name = suspect.full_name.upper() if hasattr(suspect, 'full_name') else "UNKNOWN"
                section += f"\n  {name},"
            else:
                section += f"\n  Unknown,"
            
            section += f"\n  Person Number:   {i}"
            
            # DOB - often blank if unknown (use roll system)
            if roll_check(14):  # 35% chance missing (d20 >= 14 = 35%)
                dob = fake.date_of_birth(minimum_age=18, maximum_age=65)
                section += f"\n  DOB:  {dob.strftime('%m/%d/%Y')}"
                # Convert date to datetime for calculation
                dob_dt = datetime.combine(dob, datetime.min.time())
                age = (datetime.now() - dob_dt).days // 365
                section += f"\n  Age:  {age}"
            else:
                section += f"\n  DOB:"
                section += f"\n  Age:"
            
            # Race/Sex - UPPERCASE descriptors
            race = random.choice(["WHITE", "BLACK", "HISPANIC", "ASIAN", "UNKNOWN"])
            sex = random.choice(["MALE", "FEMALE", "UNKNOWN"])
            section += f"\n  Race:  {race}"
            section += f"\n  Sex:  {sex}"
            
            # Height/Weight - often blank for unknown suspects (use roll system)
            if roll_check(12):  # 45% chance missing (d20 >= 12 = 45%)
                height_ft = random.randint(5, 6)
                height_in = random.randint(0, 11)
                height_str = f"{height_ft}'{height_in:02d}\""  # Format: 5'05"
                section += f"\n  Height:  {height_str}"
                weight = random.randint(120, 250)
                section += f"\n  Weight:  {weight}"
            else:
                section += f"\n  Height:"
                section += f"\n  Weight:"
            
            # Address - often blank if unknown (use roll system)
            if roll_check(13):  # 40% chance missing (d20 >= 13 = 40%)
                street = fake.street_address()
                section += f"\n  Address:  {street}"
                section += f"\n  Apt/Rm/Bldg:"
                city_state = f"{fake.city().upper()} {fake.state_abbr()} {fake.zipcode()}"
                section += f"\n  City/State/ZIP:  {city_state}"
            else:
                section += f"\n  Address:"
                section += f"\n  Apt/Rm/Bldg:"
                section += f"\n  City/State/ZIP:"
            
            # Phone - often blank (use roll system)
            if roll_check(10):  # 50% chance missing (d20 >= 10 = 50%)
                phone = fake.phone_number().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')[:10]
                section += f"\n  Primary Phone:  {phone}"
            else:
                section += f"\n  Primary Phone:"
            
            section += f"\n  Unhoused:   NO"
            section += f"\n  Email:"
            
            # Additional fields that may be blank (use roll system)
            if roll_check(6):  # 75% chance missing (d20 >= 6 = 75%)
                section += f"\n  Facial Hair:  {random.choice(['BEARD', 'MUSTACHE', 'GOATEE', 'NONE'])}"
            else:
                section += f"\n  Facial Hair:"
            
            section += f"\n  Misc ID Type:"
            section += f"\n  Occupation Code:"
            section += f"\n  Occupation Description:"
        
        return section
    
    def _generate_victims_section(self, victims: List) -> str:
        """Generate victims section in RMS format with detailed fields."""
        if not victims:
            return ""
        
        section = f"Victims ({len(victims)})"
        
        for i, victim in enumerate(victims, 1):
            name = victim.full_name.upper() if hasattr(victim, 'full_name') else fake.name().upper()
            section += f"\n  {name},"
            section += f"\n  Person Number:   {i}"
            
            # DOB - more likely to be known for victims (use roll system)
            if roll_check(18):  # 15% chance missing (d20 >= 18 = 15%)
                dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
                section += f"\n  DOB:  {dob.strftime('%m/%d/%Y')}"
                # Convert date to datetime for calculation
                dob_dt = datetime.combine(dob, datetime.min.time())
                age = (datetime.now() - dob_dt).days // 365
                section += f"\n  Age:  {age}"
            else:
                section += f"\n  DOB:"
                section += f"\n  Age:"
            
            # Race/Sex
            race = random.choice(["WHITE", "BLACK", "HISPANIC", "ASIAN", "UNKNOWN"])
            sex = random.choice(["MALE", "FEMALE"])
            section += f"\n  Race:  {race}"
            section += f"\n  Sex:  {sex}"
            
            # Height/Weight - more likely known for victims (use roll system)
            if roll_check(16):  # 25% chance missing (d20 >= 16 = 25%)
                height_ft = random.randint(5, 6)
                height_in = random.randint(0, 11)
                height_str = f"{height_ft}'{height_in:02d}\""
                section += f"\n  Height:  {height_str}"
                weight = random.randint(100, 250)
                section += f"\n  Weight:  {weight}"
            else:
                section += f"\n  Height:"
                section += f"\n  Weight:"
            
            # Address - usually known for victims (use roll system)
            if roll_check(18):  # 15% chance missing (d20 >= 18 = 15%)
                street = fake.street_address()
                section += f"\n  Address:  {street}"
                section += f"\n  Apt/Rm/Bldg:"
                city_state = f"{fake.city().upper()} {fake.state_abbr()} {fake.zipcode()}"
                section += f"\n  City/State/ZIP:  {city_state}"
            else:
                section += f"\n  Address:"
                section += f"\n  Apt/Rm/Bldg:"
                section += f"\n  City/State/ZIP:"
            
            # Phone - usually known (use roll system)
            if roll_check(16):  # 25% chance missing (d20 >= 16 = 25%)
                phone = fake.phone_number().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')[:10]
                section += f"\n  Primary Phone:  {phone}"
            else:
                section += f"\n  Primary Phone:"
            
            section += f"\n  Email:"
            
            # Check if juvenile (age < 18) - add parent/guardian section
            if roll_check(17):  # 20% chance of juvenile victim (d20 >= 17 = 20%)
                section += f"\n  Parent/Guardian:"
                section += f"\n    Name:  {fake.name().upper()}"
                section += f"\n    Relationship:  {random.choice(['MOTHER', 'FATHER', 'GUARDIAN'])}"
                section += f"\n    Address:  {fake.street_address()}"
                section += f"\n    Phone:  {fake.phone_number().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')[:10]}"
        
        return section
    
    def _generate_event_section(self) -> str:
        """Generate event/location section."""
        location = self.case.incident_report.incident_location if self.case.incident_report else fake.address()
        city_state_zip = f"{fake.city().upper()} {fake.state_abbr()} {fake.zipcode()}"
        
        section = f"Event  {location}"
        section += f"\n{city_state_zip}"
        
        return section
    
    def _generate_incident_metadata(self) -> str:
        """Generate incident metadata block with proper spacing."""
        # Format dates using standardized formatter
        start_date = DateFormatter.format_rms_datetime(self.crime_datetime)
        end_date = DateFormatter.format_rms_datetime(self.crime_datetime + timedelta(hours=random.randint(1, 48)))
        reported_date = DateFormatter.format_rms_datetime(self.report_date)
        dispatch_date = DateFormatter.format_rms_datetime(self.report_date + timedelta(minutes=random.randint(5, 30)))
        
        # Get offense description in ALL CAPS with slashes
        offense_desc = self._format_offense_description()
        
        city = fake.city().upper()
        region = f"REGION {random.randint(1, 5)}, {random.randint(1, 20):02d}"
        
        metadata = f"Incident Description:   {offense_desc}"
        metadata += f"\nIncident Start Date:   {start_date}"
        metadata += f"\nIncident End Date:   {end_date}"
        metadata += f"\nReported Date:   {reported_date}"
        metadata += f"\nCity:   {city}"
        metadata += f"\nRegion Grid:   {region}"
        metadata += f"\nRegion:   REGION {region.split(',')[0].split()[-1]}"
        metadata += f"\nDate Dispatch:   {dispatch_date}"
        metadata += f"\nWeapon Code:"
        metadata += f"\nCase Status:   ACTIVE"
        
        return metadata
    
    def _format_offense_description(self) -> str:
        """Format offense description in ALL CAPS with slashes."""
        crime_type = self.case.crime_type.upper()
        
        # Map to common RMS offense codes
        offense_map = {
            "FRAUD": "FALSE PRETENSES/SWINDLE/CONFIDENCE GAME/FRAUD",
            "CYBERCRIME": "COMPUTER FRAUD/IDENTITY THEFT/ELECTRONIC CRIME",
            "THEFT": "LARCENY/THEFT/BURGLARY",
            "ASSAULT": "ASSAULT/BATTERY/DOMESTIC VIOLENCE",
            "DRUG": "POSSESSION/DISTRIBUTION/CONTROLLED SUBSTANCE",
            "SCAM": "FALSE PRETENSES/SWINDLE/CONFIDENCE GAME/FRAUD"
        }
        
        for key, value in offense_map.items():
            if key in crime_type:
                return value
        
        # Default format
        return f"{crime_type}/FRAUD/CRIMINAL ACTIVITY"
    
    def _generate_narrative_section(self) -> str:
        """Generate narrative in official LE voice with style variations."""
        victims = [p for p in self.case.persons if p.role.value == "Victim"]
        suspects = [p for p in self.case.persons if p.role.value == "Suspect"]
        
        # Vary narrative openings
        opening_templates = [
            "On {time}, this officer was dispatched to {location} regarding a reported {crime}.",
            "On {time}, I responded to {location} in reference to a {crime} complaint.",
            "On {time}, this officer was dispatched to {location} for a reported {crime}.",
            "At approximately {time}, I was dispatched to {location} regarding a {crime} complaint.",
            "On {time}, this officer responded to {location} in response to a {crime} report."
        ]
        
        # Use standardized time format
        date_str = DateFormatter.format_rms_date(self.report_date)
        time_str = f"{date_str} at approximately {DateFormatter.format_rms_time(self.report_date)}"
        location = self.case.incident_report.incident_location if self.case.incident_report else fake.address()
        crime = self.case.crime_type.lower()
        
        opening = random.choice(opening_templates).format(
            time=time_str,
            location=location,
            crime=crime
        )
        
        narrative = opening
        narrative += "\n\n"
        
        if victims:
            victim = victims[0]
            victim_name = victim.full_name if hasattr(victim, 'full_name') else "the victim"
            
            # Vary victim statement attributions
            attribution_templates = [
                f"The victim, {victim_name}, stated ",
                f"Upon arrival, {victim_name} advised this officer that ",
                f"The victim, {victim_name}, reported that ",
                f"{victim_name} informed this officer that ",
                f"According to {victim_name}, "
            ]
            
            narrative += random.choice(attribution_templates)
            
            # Generate victim statement based on crime type
            if "fraud" in crime or "scam" in crime:
                narrative += f"she received multiple phone calls from an unknown male identifying himself as a federal agent. "
                narrative += f"The caller instructed the victim to withdraw ${random.randint(500, 50000):,} in cash and deliver it to an unknown subject at a nearby location. "
                narrative += f"The victim complied and later discovered the funds had been fraudulently obtained."
            elif "cyber" in crime:
                narrative += f"her computer system was compromised and unauthorized access was detected. "
                narrative += f"The victim reported receiving suspicious emails and noticed unusual activity on her accounts."
            else:
                narrative += f"the incident occurred as described above. "
                narrative += f"The victim provided a detailed statement regarding the events."
        
        narrative += "\n\n"
        
        # Add time markers and additional details
        if random.random() > 0.3:
            follow_up_time = (self.report_date + timedelta(minutes=random.randint(10, 60))).strftime('%H%M hours')
            narrative += f"At approximately {follow_up_time}, this officer conducted a preliminary investigation of the scene. "
        
        narrative += "\n\n"
        
        # Evidence section with variations
        if self.case.evidence:
            evidence_templates = [
                "Evidence seized included: {items}.",
                "The following evidence was collected: {items}.",
                "Evidence collected at the scene: {items}.",
                "Items of evidence seized: {items}."
            ]
            evidence_items = [e.description for e in self.case.evidence[:3]]
            evidence_str = ", ".join(evidence_items)
            narrative += random.choice(evidence_templates).format(items=evidence_str)
        
        narrative += "\n\n"
        
        # Closing with variations
        closing_templates = [
            f"Case status: ACTIVE. Victim advised of case number {self.incident_number} and instructed to contact this department with any additional information.",
            f"This case remains ACTIVE. The victim was provided with case number {self.incident_number} and advised to report any additional information.",
            f"Case status: ACTIVE. Victim was given case number {self.incident_number} and contact information for follow-up.",
            f"Status: ACTIVE. Case number {self.incident_number} assigned. Victim advised to contact this department with any new information."
        ]
        
        narrative += random.choice(closing_templates)
        
        # Add officer/date stamp (sometimes embedded in narrative)
        if random.random() > 0.5:
            officer_name = fake.last_name().upper()
            badge = random.randint(1000, 9999)
            narrative += f"\n\n{self.report_date.strftime('%m/%d/%Y %H%M')}  {officer_name}, #{badge}"
        
        # Apply realistic errors to narrative using roll system
        if roll_check(17):  # 20% chance of narrative errors (d20 >= 17 = 20%)
            # Simple typo: occasional character swaps or missing spaces
            words = narrative.split()
            if len(words) > 10 and roll_check(16):  # 25% chance if error occurs
                # Remove a space occasionally (word merge)
                idx = random.randint(0, len(words) - 2)
                words[idx] = words[idx] + words[idx + 1]
                words.pop(idx + 1)
                narrative = ' '.join(words)
        
        # Sometimes missing fields in metadata (use roll system)
        if roll_check(19):  # 10% chance of incomplete form (d20 >= 19 = 10%)
            # Remove a random field occasionally
            pass  # Could be implemented if needed
        
        return narrative


class CarrierRecordGenerator:
    """Generates carrier/provider records (AT&T, Cricket, Verizon) following blueprint formats."""
    
    def __init__(self, case, phone_number: str, matter_id: str, query_start: datetime, query_end: datetime):
        self.case = case
        self.phone_number = phone_number
        self.matter_id = matter_id
        self.query_start = query_start
        self.query_end = query_end
        # Provider selection with weighted probability (AT&T most common)
        provider_weights = {
            "AT&T": 0.4,
            "CRICKET": 0.2,  # AT&T subsidiary
            "VERIZON": 0.3,
            "T-Mobile": 0.1
        }
        self.provider = random.choices(
            list(provider_weights.keys()),
            weights=list(provider_weights.values())
        )[0]
        
        # Generate consistent identifiers that will be reused across all documents
        self.imsi = f"310{random.randint(10, 99)}{random.randint(1000000000, 9999999999)}"  # 15 digits
        self.imei = f"{random.randint(35000000000000, 35999999999999)}"  # 14-15 digits
        self.mac_address = ":".join([f"{random.randint(0, 255):02X}" for _ in range(6)])  # AA:BB:CC:DD:EE:FF format
    
    def _get_provider_format(self) -> Dict:
        """Get provider-specific formatting preferences."""
        formats = {
            "AT&T": {
                "timezone": "Eastern Time Zone",
                "header_style": "centered",
                "matter_id_format": "numeric"
            },
            "CRICKET": {
                "timezone": "Eastern Time Zone",  # AT&T subsidiary
                "header_style": "centered",
                "matter_id_format": "numeric"
            },
            "VERIZON": {
                "timezone": "Eastern Time Zone",
                "header_style": "left-aligned",
                "matter_id_format": "alphanumeric"
            },
            "T-Mobile": {
                "timezone": "Pacific Time Zone",
                "header_style": "centered",
                "matter_id_format": "numeric"
            }
        }
        return formats.get(self.provider, formats["AT&T"])
    
    def generate_stir_shaken_log(self) -> str:
        """Generate AT&T STIR/SHAKEN call authentication log."""
        doc = []
        
        # Header block
        doc.append("      STIR/SHAKEN")
        doc.append("")
        # Provider-specific formatting
        provider_formats = self._get_provider_format()
        
        doc.append(f"      {self.provider} has queried for records from {DateFormatter.format_query_window_start(self.query_start)} to {DateFormatter.format_query_window_end(self.query_end)}")
        doc.append(f"      {self.provider} has queried for records using {provider_formats['timezone']}. {self.provider}'s records are stored and provided in UTC.")
        doc.append(f"                            ({self.provider})")
        doc.append(f"      Matter ID:      {self.matter_id}")
        doc.append(f"      Creation Date:  {DateFormatter.format_rms_date(datetime.now())}")
        doc.append(f"      Run Date:       {DateFormatter.format_carrier_datetime_utc(datetime.now()).split()[0]}        Run Time:       {datetime.now().strftime('%H:%M:%S')}")
        doc.append("")
        doc.append(f"      Voice Usage For: ({self.phone_number[:3]}){self.phone_number[3:6]}-{self.phone_number[6:]}")
        doc.append("")
        
        # CSV header
        doc.append("Item,Seq,ConnDateTime(UTC),OriginatingNumber,TerminatingNumber,Status,AttestType,VerOrig,VerTerm")
        
        # Generate sample records with realistic patterns
        num_records = random.randint(5, 20)
        
        # Create realistic call patterns (more calls during business hours, fewer at night)
        for i in range(1, num_records + 1):
            # Weight hours toward business hours (9 AM - 9 PM)
            hour = random.choices(
                list(range(24)),
                weights=[0.3] * 9 + [1.0] * 12 + [0.3] * 3  # Lower weight for late night/early morning
            )[0]
            
            conn_time = self.query_start + timedelta(
                days=random.randint(0, (self.query_end - self.query_start).days),
                hours=hour,
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            
            seq = round(random.uniform(1.0, 20.0), 1)
            
            # Realistic number patterns (some repeated contacts)
            if i > 1 and random.random() < 0.3:  # 30% chance of repeat contact
                orig_num = term_num  # Call back
            else:
                orig_num = f"1{random.randint(5550100000, 5550199999)}"
            
            term_num = f"1{random.randint(5550100000, 5550199999)}"
            
            # Status distribution (most calls pass)
            status = random.choices(
                ["Pass", "No", "Fail"],
                weights=[0.85, 0.10, 0.05]
            )[0]
            
            attest_type = random.choice(["A", "B", "C"])
            
            doc.append(f"{i},{seq},{DateFormatter.format_carrier_datetime_utc(conn_time)},{orig_num},{term_num},{status},{attest_type},,")
        
        return "\n".join(doc)
    
    def generate_subscriber_info(self) -> str:
        """Generate Cricket/AT&T subscriber information report."""
        doc = []
        
        # Header
        doc.append(f"{self.matter_id}")
        doc.append(f"                                                                      {self.provider}")
        doc.append(f"{datetime.now().strftime('%m/%d/%Y')}")
        doc.append(f"                                   WIRELESS")
        doc.append(f"                            SUBSCRIBER INFORMATION")
        doc.append("-" * 76)
        doc.append(f"{random.randint(900000000, 999999999)}")
        doc.append("")
        doc.append("-" * 76)
        
        # Financial Liable Party
        doc.append("FINANCIAL LIABLE PARTY")
        name = fake.name().upper()
        doc.append(f"  NAME:           {name}")
        doc.append(f"  ADDRESS:        {fake.street_address()}")
        doc.append(f"                  {fake.city().upper()}, {fake.state_abbr()} {fake.zipcode()}")
        doc.append("")
        
        # Billing Party
        doc.append("-" * 76)
        doc.append("BILLING PARTY")
        doc.append(f"  NAME:           {name}")
        doc.append(f"  ADDRESS:        {fake.street_address()}")
        doc.append(f"                  {fake.city().upper()}, {fake.state_abbr()} {fake.zipcode()}")
        doc.append("")
        
        # User Information
        doc.append("-" * 76)
        doc.append("USER INFORMATION")
        doc.append(f"  MSISDN:         ({self.phone_number[:3]}){self.phone_number[3:6]}-{self.phone_number[6:]}")
        doc.append(f"  STATUS:         ACTIVE")
        doc.append(f"  ACTIVATION:     {(datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%m/%d/%Y')}")
        
        return "\n".join(doc)
    
    def generate_precision_location_report(self) -> str:
        """Generate AT&T Historical Precision Location Report with 8-decimal coordinates."""
        doc = []
        
        # Header block
        doc.append("      Historical Precision Location Information")
        doc.append("")
        doc.append(f"      {self.provider} has queried for records from {DateFormatter.format_query_window_start(self.query_start)} to {DateFormatter.format_query_window_end(self.query_end)}")
        doc.append(f"      {self.provider} has queried for records using Eastern Time Zone. {self.provider}'s records are stored and provided in UTC.")
        doc.append(f"                            ({self.provider})")
        doc.append(f"      Matter ID:      {self.matter_id}")
        doc.append(f"      Creation Date:  {datetime.now().strftime('%m/%d/%Y')}")
        doc.append(f"      Run Date:        {datetime.now().strftime('%m/%d/%y')}        Run Time:        {datetime.now().strftime('%H:%M:%S')}")
        doc.append("")
        doc.append(f"      Usage For: ({self.phone_number[:3]}){self.phone_number[3:6]}-{self.phone_number[6:]}")
        doc.append("")
        
        # CSV header
        doc.append("Item,PhoneNumber,IMSI,ConnectionDate,ConnectionTime(GMT),Latitude,Longitude,LocationMethod,LocationAccuracy")
        
        # Generate location records with 8-decimal precision
        num_records = random.randint(10, 30)
        base_lat = random.uniform(25.0, 49.0)  # US latitude range
        base_lon = random.uniform(-125.0, -66.0)  # US longitude range
        
        for i in range(1, num_records + 1):
            conn_date = self.query_start + timedelta(
                days=random.randint(0, (self.query_end - self.query_start).days),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            # Slight movement from base location (realistic device movement)
            lat = round(base_lat + random.uniform(-0.1, 0.1), 8)
            lon = round(base_lon + random.uniform(-0.1, 0.1), 8)
            
            location_method = random.choice([
                "Tower+UE Signal",
                "GPS",
                "WiFi",
                "Tower Only"
            ])
            
            accuracy = random.choice([
                "likely better than 400 meters",
                "likely better than 2500 meters",
                "likely better than 100 meters",
                "likely better than 1000 meters"
            ])
            
            phone_num_11 = f"1{self.phone_number}"
            doc.append(f"{i},{phone_num_11},{self.imsi},{DateFormatter.format_carrier_date_iso(conn_date)},{conn_date.strftime('%H:%M:%S')},{lat:.8f},{lon:.8f},{location_method},{accuracy}")
        
        return "\n".join(doc)
    
    def generate_timing_advance_report(self) -> str:
        """Generate AT&T Timing Advance Report with tower and device coordinates."""
        doc = []
        
        # Header block
        doc.append("      Timing Advance Location Information")
        doc.append("")
        doc.append(f"      {self.provider} has queried for records from {DateFormatter.format_query_window_start(self.query_start)} to {DateFormatter.format_query_window_end(self.query_end)}")
        doc.append(f"      {self.provider} has queried for records using Eastern Time Zone. {self.provider}'s records are stored and provided in UTC.")
        doc.append(f"                            ({self.provider})")
        doc.append(f"      Matter ID:      {self.matter_id}")
        doc.append(f"      Creation Date:  {datetime.now().strftime('%m/%d/%Y')}")
        doc.append(f"      Run Date:        {datetime.now().strftime('%m/%d/%y')}        Run Time:        {datetime.now().strftime('%H:%M:%S')}")
        doc.append("")
        doc.append(f"      Usage For: ({self.phone_number[:3]}){self.phone_number[3:6]}-{self.phone_number[6:]}")
        doc.append("")
        
        # CSV header
        doc.append("Item,PhoneNumber,IMSI,ConnDate,ConnTime(UTC),TimingAdvance,CellID,NetworkType,CellTowerLatitude,CellTowerLongitude,SectorOrientation,DeviceLatitude,DeviceLongitude")
        
        # Generate TA records
        num_records = random.randint(10, 25)
        base_lat = random.uniform(25.0, 49.0)
        base_lon = random.uniform(-125.0, -66.0)
        
        for i in range(1, num_records + 1):
            conn_date = self.query_start + timedelta(
                days=random.randint(0, (self.query_end - self.query_start).days),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            timing_advance = random.randint(0, 63)  # TA range
            cell_id = f"{random.randint(10000000, 99999999):08d}"  # 8 digits with leading zeros
            network_type = random.choice(["2G", "3G", "4G", "5G"])
            
            # Tower location (fixed for a cell site)
            tower_lat = round(base_lat + random.uniform(-0.05, 0.05), 8)
            tower_lon = round(base_lon + random.uniform(-0.05, 0.05), 8)
            sector_orientation = random.choice([0, 60, 120, 180, 240, 300])  # Common sector angles
            
            # Device location (slightly offset from tower)
            device_lat = round(tower_lat + random.uniform(-0.01, 0.01), 8)
            device_lon = round(tower_lon + random.uniform(-0.01, 0.01), 8)
            
            phone_num_11 = f"1{self.phone_number}"
            doc.append(f"{i},{phone_num_11},{self.imsi},{DateFormatter.format_carrier_date_iso(conn_date)},{conn_date.strftime('%H:%M:%S')},{timing_advance},{cell_id},{network_type},{tower_lat:.8f},{tower_lon:.8f},{sector_orientation},{device_lat:.8f},{device_lon:.8f}")
        
        return "\n".join(doc)
    
    def generate_mac_address_report(self) -> str:
        """Generate MAC Address Association Report."""
        doc = []
        
        # Header
        doc.append(f"{self.matter_id}")
        doc.append(f"                                                                                                {self.provider}")
        doc.append(f"{datetime.now().strftime('%m/%d/%Y')}")
        doc.append(f"                                           MAC Address Report")
        doc.append("")
        doc.append(f"Phone Number:  ({self.phone_number[:3]}){self.phone_number[3:6]}-{self.phone_number[6:]}")
        doc.append(f"MAC Address:   {self.mac_address}")
        doc.append(f"As Of:         {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(doc)
    
    def generate_wireline_cdr(self) -> str:
        """Generate AT&T Wireline Call Detail Records."""
        doc = []
        
        # Header
        doc.append("      WIRELINE")
        doc.append("")
        doc.append(f"      {self.provider} has queried for records from {DateFormatter.format_query_window_start(self.query_start)} to {DateFormatter.format_query_window_end(self.query_end)}")
        doc.append(f"      {self.provider} has queried for records using Eastern Time Zone. {self.provider}'s records are stored and provided in UTC.")
        doc.append(f"                            ({self.provider})")
        doc.append(f"      Matter ID:      {self.matter_id}")
        doc.append(f"      Creation Date:  {datetime.now().strftime('%m/%d/%Y')}")
        doc.append(f"      Run Date:        {datetime.now().strftime('%m/%d/%y')}        Run Time:        {datetime.now().strftime('%H:%M:%S')}")
        doc.append("")
        doc.append(f"      Voice Usage For: ({self.phone_number[:3]}){self.phone_number[3:6]}-{self.phone_number[6:]}")
        doc.append("")
        
        # CSV header
        doc.append("Item,ConnDateTime(UTC),OriginatingNumber,SecOrig,TerminatingNumber,DialedNumber,ElapsedTime,CIC,CallCode,OrigAcc")
        
        # Generate wireline CDR records
        num_records = random.randint(5, 15)
        for i in range(1, num_records + 1):
            conn_time = self.query_start + timedelta(
                days=random.randint(0, (self.query_end - self.query_start).days),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            orig_num = f"{random.randint(5550100000, 5550199999)}"
            sec_orig = ""  # Often blank
            term_num = f"{random.randint(5550100000, 5550199999)}"
            dialed_num = ""  # Often blank
            elapsed_min = random.randint(0, 120)
            elapsed_sec = random.randint(0, 59)
            elapsed_time = f"{elapsed_min}:{elapsed_sec:02d}"
            cic = random.randint(100, 999)
            call_code = random.randint(600, 699)
            orig_acc = random.randint(100, 999) if random.random() > 0.3 else ""  # Sometimes blank
            
            doc.append(f"{i},{DateFormatter.format_carrier_datetime_utc(conn_time)},{orig_num},{sec_orig},{term_num},{dialed_num},{elapsed_time},{cic},{call_code},{orig_acc}")
        
        return "\n".join(doc)
    
    def generate_mobility_with_cell_location(self) -> str:
        """Generate AT&T Mobility with Cell Location (combined voice/data with IMEI/IMSI)."""
        doc = []
        
        # Header
        doc.append("      MOBILITY WITH CELL LOCATION")
        doc.append("")
        doc.append(f"      {self.provider} has queried for records from {DateFormatter.format_query_window_start(self.query_start)} to {DateFormatter.format_query_window_end(self.query_end)}")
        doc.append(f"      {self.provider} has queried for records using Eastern Time Zone. {self.provider}'s records are stored and provided in UTC.")
        doc.append(f"                            ({self.provider})")
        doc.append(f"      Matter ID:      {self.matter_id}")
        doc.append(f"      Creation Date:  {datetime.now().strftime('%m/%d/%Y')}")
        doc.append(f"      Run Date:        {datetime.now().strftime('%m/%d/%y')}        Run Time:        {datetime.now().strftime('%H:%M:%S')}")
        doc.append("")
        doc.append(f"      Voice Usage For: ({self.phone_number[:3]}){self.phone_number[3:6]}-{self.phone_number[6:]}")
        doc.append("")
        
        # CSV header (very long, as per blueprint)
        doc.append("Item,ConnDateTime(UTC),SeizureTime,ET,OriginatingNumber,TerminatingNumber,IMEI,IMSI,CT,Feature,DIALED,FORWARDED,TRANSLATED,ORIG_ORIG,MAKE,MODEL,CellLocation")
        
        # Generate mobility records
        num_records = random.randint(10, 25)
        base_lat = random.uniform(25.0, 49.0)
        base_lon = random.uniform(-125.0, -66.0)
        
        for i in range(1, num_records + 1):
            conn_time = self.query_start + timedelta(
                days=random.randint(0, (self.query_end - self.query_start).days),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            seizure_time = f"0:{random.randint(1, 9):02d}"  # Call setup time
            et = f"{random.randint(0, 300)}:{random.randint(0, 59):02d}"  # Elapsed time
            
            orig_num = f"1{random.randint(5550100000, 5550199999)}"
            term_num = f"1{random.randint(5550100000, 5550199999)}"
            
            ct = random.choice(["MO", "MT", "MO-SMS", "MT-SMS"])  # Call type
            feature = random.choice(["[NIOP]", "[CFU]", "[CFB]", ""])  # Feature codes in brackets
            
            # Often blank fields
            dialed = "" if random.random() > 0.3 else f"{random.randint(5550100000, 5550199999)}"
            forwarded = ""
            translated = ""
            orig_orig = ""
            
            make = random.choice(["ACME", "TECHCO", "MOBILE", "PHONE"])
            model = random.choice(["MODELX", "MODELY", "MODELZ", "SMART"])
            
            # Cell location in bracket format: [CellID:TA:Longitude:Latitude:Sector:Signal]
            cell_id = random.randint(100000000, 999999999)
            ta = random.randint(0, 63)
            lat = round(base_lat + random.uniform(-0.1, 0.1), 7)
            lon = round(base_lon + random.uniform(-0.1, 0.1), 7)
            sector = random.choice([0, 60, 120, 180, 240, 300])
            signal = round(random.uniform(50.0, 100.0), 2)
            cell_location = f"[{cell_id}:{ta}:{lon:.7f}:{lat:.7f}:{sector}:{signal:.2f}:]"
            
            doc.append(f"{i},{DateFormatter.format_carrier_datetime_utc(conn_time)},{seizure_time},{et},{orig_num},{term_num},{self.imei},{self.imsi},{ct},{feature},{dialed},{forwarded},{translated},{orig_orig},{make},{model},{cell_location}")
        
        return "\n".join(doc)


class WarrantGenerator:
    """Generates search warrant applications and affidavits following blueprint formats."""
    
    def __init__(self, case, target: str, target_type: str = "phone"):
        self.case = case
        self.target = target
        self.target_type = target_type
        # Use jurisdiction-specific court system
        jurisdictions = {
            "South Carolina": {
                "court": "COURT OF GENERAL SESSIONS",
                "circuit": "FIFTH JUDICIAL CIRCUIT",
                "statute": "SC §17-13-140"
            },
            "California": {
                "court": "SUPERIOR COURT",
                "circuit": "",
                "statute": "Cal. Penal Code §1524"
            },
            "Texas": {
                "court": "DISTRICT COURT",
                "circuit": "",
                "statute": "Tex. Code Crim. Proc. Art. 18.01"
            }
        }
        jurisdiction = random.choice(list(jurisdictions.values()))
        self.court_name = jurisdiction["court"]
        self.county = f"{fake.city()} COUNTY".upper()  # Generate county name from city
        self.state = fake.state().upper()
        self.warrant_number = f"{random.randint(100000, 999999)}"
        self.statute = jurisdiction.get("statute", "State Statute")
    
    def generate_warrant_affidavit(self, provider: str = "Verizon") -> str:
        """Generate search warrant affidavit for provider records."""
        doc = []
        
        # Court caption
        doc.append(f"IN THE {self.court_name}")
        doc.append(f"{self.county} COUNTY, STATE OF {self.state}")
        doc.append("")
        doc.append("AFFIDAVIT AND APPLICATION FOR SEARCH WARRANT")
        doc.append("")
        
        # Affidavit body
        investigator_name = f"Detective {fake.first_name()} {fake.last_name()}"
        agency = random.choice([
            "Richland County Sheriff's Department",
            "Columbia Police Department",
            "County Sheriff's Office"
        ])
        
        doc.append(f"I, {investigator_name}, being first duly sworn, depose and state:")
        doc.append("")
        doc.append(f"1. I am employed by the {agency} and am currently assigned to the Criminal Investigations Unit.")
        doc.append("")
        
        if self.target_type == "phone":
            doc.append(f'2. I make this affidavit in support of a search warrant directed to {provider} for records associated with the cellular telephone number "{self.target}" (the "Target Phone"), believed to be used in connection with violations of state wire fraud statutes.')
        else:
            doc.append(f'2. I make this affidavit in support of a search warrant directed to {provider} for records associated with the account identified as "{self.target}" (the "Target Account"), believed to be used in connection with violations of state wire fraud statutes.')
        
        doc.append("")
        query_start = (datetime.now() - timedelta(days=90)).strftime("%B %d, %Y")
        doc.append(f"3. The records sought cover the period from {query_start} through the present date, and include:")
        doc.append("   a. Call/text/data detail records, including dialed and received numbers, dates, times, durations, and cell-site/sector information;")
        doc.append("   b. Specialized location records, including but not limited to NELOS, RTT, PCMD, TDOA, and E9-1-1 location data;")
        doc.append("   c. Electronically stored communications and files maintained in any associated cloud account, including messages, images, documents, and contact lists.")
        doc.append("")
        
        # Probable cause narrative
        doc.append("4. PROBABLE CAUSE:")
        doc.append("")
        doc.append(f"   On {self.case.incident_report.incident_date.strftime('%B %d, %Y') if self.case.incident_report else datetime.now().strftime('%B %d, %Y')}, this department received a complaint regarding {self.case.crime_type.lower()}. ")
        doc.append(f"   Investigation revealed that the Target {'Phone' if self.target_type == 'phone' else 'Account'} was used to facilitate the criminal activity. ")
        doc.append("   The requested records are necessary to establish the identity of the suspect, establish a timeline of events, and identify co-conspirators.")
        doc.append("")
        
        # Nondisclosure clause
        doc.append("IT IS FURTHER ORDERED that the provider shall not disclose the existence of this warrant, or the investigation described herein, to the subscriber or any other unauthorized person for a period of ninety (90) days from the date of this order, unless extended by further order of this Court.")
        doc.append("")
        doc.append("")
        doc.append(f"Respectfully submitted,")
        doc.append("")
        doc.append(f"{investigator_name}")
        doc.append(f"{agency}")
        doc.append(f"Badge #{random.randint(1000, 9999)}")
        
        return "\n".join(doc)


class PreservationRequestGenerator:
    """Generates preservation request letters following blueprint formats."""
    
    def __init__(self, case, phone_number: str, provider: str = "T-Mobile"):
        self.case = case
        self.phone_number = phone_number
        self.provider = provider
        self.agency_name = random.choice([
            "RICHLAND COUNTY SHERIFF'S DEPARTMENT",
            "COLUMBIA POLICE DEPARTMENT",
            "COUNTY SHERIFF'S OFFICE"
        ])
        self.division = random.choice([
            "Criminal Investigations Division",
            "Criminal Investigations Unit",
            "Major Crimes Unit"
        ])
    
    def generate(self) -> str:
        """Generate a preservation request letter."""
        doc = []
        
        # Agency letterhead
        doc.append(self.agency_name)
        doc.append(self.division)
        doc.append('"To be a trusted, progressive, service-oriented law enforcement agency."')
        doc.append(f"Telephone ({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}")
        doc.append(f"Fax ({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}")
        doc.append(fake.street_address())
        doc.append(f"PO Box {random.randint(100, 999)}")
        doc.append(f"{fake.city()}, {fake.state_abbr()}. {fake.zipcode()}")
        doc.append("")
        doc.append(f"{self.agency_name.split()[0]}'s Mission Statement")
        doc.append('"Our mission is to improve the quality of life of the community by providing professional, exemplary service through crime prevention and resolution, diverse services, and community partnerships."')
        doc.append("")
        doc.append("Memorandum")
        doc.append("")
        doc.append(f"To: {self.provider} Legal")
        doc.append(f"From: Investigator {fake.first_name()} {fake.last_name()}, {self.agency_name}")
        doc.append(f"Subject: LEGAL PROCESS: PRESERVATION REQUEST FOR {self.phone_number}")
        doc.append(f"Date: {datetime.now().strftime('%d %B %Y')}")
        doc.append("")
        doc.append("Dear Sir or Madam,")
        doc.append("")
        
        # Body
        offense_desc = self.case.crime_type.upper()
        period_start = (self.case.incident_report.incident_date if self.case.incident_report else datetime.now() - timedelta(days=30)).strftime("%B %d, %Y")
        
        doc.append(f"This letter is a formal request for the preservation of records and evidence related to phone number {self.phone_number} which is registered through your services. This request is made in connection with an official investigation into a criminal matter. The aforementioned number {self.phone_number} was used by the suspect to facilitate a {offense_desc}. The primary period of activity under investigation is from {period_start}, to the present.")
        doc.append("")
        doc.append(f"Pursuant to the Stored Communications Act, 18 U.S.C. § 2703(f), we request that you immediately take all necessary steps to preserve any and all records associated with the number {self.phone_number} for a period of 90 days from the date of this letter, pending the issuance of a search warrant, subpoena, or other legal process.")
        doc.append("")
        doc.append("•   Subscriber & Registrant Information :")
        doc.append("o   The full name, physical address(es), telephone number(s), and email address(es) of the registrant and any associated contacts (administrative, technical, billing).")
        doc.append("o   All historical registrant data associated with the account.")
        doc.append("")
        doc.append("•   Account & Billing Records :")
        doc.append("o   The date and time the account was created.")
        doc.append("o   All payment information on file, including credit card details (e.g., cardholder name, last four digits, expiration date, and billing address), bank account information, or other payment methods used to maintain the account.")
        doc.append("")
        doc.append("•   Call Detail Records & Location Data :")
        doc.append("o   All call detail records, including dialed and received numbers, dates, times, durations, and cell-site/sector information.")
        doc.append("o   Specialized location records, including but not limited to NELOS, RTT, PCMD, TDOA, and E9-1-1 location data.")
        doc.append("")
        doc.append("•   Stored Communications & Content :")
        doc.append("o   The contents of all text messages, emails, and other electronically stored communications.")
        doc.append("o   All files, images, videos, and documents stored in any associated cloud account.")
        doc.append("")
        doc.append("This request is solely for the preservation of data and is not a request for the disclosure of records at this time. Please do not delete, alter, or otherwise dispose of the requested information.")
        doc.append("")
        doc.append("We request that you acknowledge receipt of this preservation request via email at your earliest convenience. If you have any questions, please contact the undersigned investigator.")
        doc.append("")
        doc.append("Respectfully,")
        doc.append("")
        doc.append(f"Investigator {fake.first_name()} {fake.last_name()}")
        doc.append(f"{self.agency_name}")
        doc.append(f"Badge #{random.randint(1000, 9999)}")
        doc.append("")
        doc.append(f"Case Number: {self.case.id}")
        
        return "\n".join(doc)


class BusinessRecordsCertificationGenerator:
    """Generates business records certifications following blueprint formats."""
    
    def __init__(self, case, provider: str, matter_id: str, record_types: List[str]):
        self.case = case
        self.provider = provider
        self.matter_id = matter_id
        self.record_types = record_types
        
        # Provider-specific details
        self.provider_info = {
            "Apple": {"company": "Apple Inc.", "title": "Legal Specialist, Law Enforcement Response"},
            "Block": {"company": "Block, Inc.", "title": "Custodian of Records"},
            "T-Mobile": {"company": "T-Mobile USA, Inc.", "title": "Custodian of Records"},
            "AT&T": {"company": "AT&T Mobility LLC", "title": "Custodian of Records"},
            "Verizon": {"company": "Verizon Communications Inc.", "title": "Custodian of Records"}
        }
    
    def generate(self) -> str:
        """Generate a business records certification."""
        provider_data = self.provider_info.get(self.provider, {
            "company": f"{self.provider} Inc.",
            "title": "Custodian of Records"
        })
        
        doc = []
        
        # Header
        doc.append("CERTIFICATION OF BUSINESS RECORDS")
        doc.append("")
        middle_initial = fake.random_letter().upper() if random.random() > 0.3 else ""
        middle_str = f" {middle_initial}." if middle_initial else ""
        doc.append(f"I, {fake.first_name()}{middle_str} {fake.last_name()}, declare as follows:")
        doc.append("")
        doc.append(f"1. I am employed by {provider_data['company']} as a {provider_data['title']} and am authorized to certify records on its behalf.")
        doc.append("")
        doc.append(f"2. Attached hereto are true and accurate copies of {', '.join(self.record_types)} maintained by {provider_data['company']} for the account associated with matter ID {self.matter_id}.")
        doc.append("")
        doc.append("3. These records were made at or near the time of the occurrences they reflect by, or from information transmitted by, persons with knowledge, and were kept in the course of regularly conducted business activity.")
        doc.append("")
        doc.append(f"4. It is the regular practice of {provider_data['company']} to make and keep such records, and the records were made and kept in the regular course of business.")
        doc.append("")
        doc.append(f"5. The records attached hereto are maintained in the ordinary course of business and are relied upon by {provider_data['company']} in the conduct of its business operations.")
        doc.append("")
        doc.append("I declare under penalty of perjury under the laws of the United States of America that the foregoing is true and correct.")
        doc.append("")
        doc.append(f"Executed this {datetime.now().strftime('%d')} day of {datetime.now().strftime('%B')}, {datetime.now().strftime('%Y')}.")
        doc.append("")
        doc.append("")
        middle_initial = fake.random_letter().upper() if random.random() > 0.3 else ""
        middle_str = f" {middle_initial}." if middle_initial else ""
        doc.append(f"{fake.first_name()}{middle_str} {fake.last_name()}")
        doc.append(f"{provider_data['title']}")
        doc.append(f"{provider_data['company']}")
        
        return "\n".join(doc)

