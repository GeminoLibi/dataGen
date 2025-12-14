from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class Role(Enum):
    SUSPECT = "Suspect"
    VICTIM = "Victim"
    WITNESS = "Witness"
    OFFICER = "Officer"

@dataclass
class Vehicle:
    id: str
    make: str
    model: str
    color: str
    year: int
    license_plate: str
    vin: str = ""
    owner_id: Optional[str] = None
    registered_address: str = ""

@dataclass
class Weapon:
    id: str
    type: str  # Firearm, Knife, Blunt Object
    make: str
    model: str
    serial_number: str
    caliber: Optional[str] = None  # For firearms
    registered_owner_id: Optional[str] = None

@dataclass
class DigitalDevice:
    type: str # Phone, Laptop, Tablet
    make: str
    mac_address: str
    ip_address: Optional[str] = None
    imei: Optional[str] = None # For phones
    phone_number: Optional[str] = None # For phones
    owner_id: Optional[str] = None # Links back to Person.id

@dataclass
class Person:
    id: str
    first_name: str
    last_name: str
    role: Role
    age: int
    address: str
    phone_number: str
    notes: str = ""
    vehicles: List[Vehicle] = field(default_factory=list)
    devices: List[DigitalDevice] = field(default_factory=list)
    weapons: List[Weapon] = field(default_factory=list)
    email: str = ""
    bank_accounts: List[str] = field(default_factory=list) # IBANs
    aliases: List[str] = field(default_factory=list) # Sockpuppet usernames/fake names
    personality: str = "Neutral"  # RPG personality archetype
    motive: str = ""  # Crime motive
    criminal_history: List[str] = field(default_factory=list)  # Prior convictions
    social_handle: Optional[str] = None  # Social media handle
    reliability_score: int = 50  # Witness reliability (0-100)
    relationships: Dict[str, str] = field(default_factory=dict)  # Relationships to other persons
    
    # Physical description fields
    gender: str = ""  # male, female, other
    height: str = ""  # e.g., "5'10""
    weight: int = 0  # in pounds
    hair_color: str = ""  # e.g., "brown", "blonde", "black"
    eye_color: str = ""  # e.g., "brown", "blue", "green"
    facial_hair: str = ""  # e.g., "none", "beard", "mustache", "goatee"
    build: str = ""  # e.g., "slim", "average", "stocky", "muscular"
    driver_license_number: str = ""  # Driver's license number
    driver_license_state: str = ""  # State that issued the license

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def physical_description(self) -> str:
        """Generate a formatted physical description."""
        parts = []
        if self.height:
            parts.append(self.height)
        if self.build:
            parts.append(self.build + " build")
        if self.hair_color:
            parts.append(self.hair_color + " hair")
        if self.eye_color:
            parts.append(self.eye_color + " eyes")
        if self.facial_hair and self.facial_hair != "none":
            parts.append(self.facial_hair)
        if self.weight > 0:
            parts.append(f"{self.weight} lbs")
        return ", ".join(parts) if parts else "Description not available"

class EvidenceType(Enum):
    PHYSICAL = "Physical"
    DIGITAL = "Digital"
    DOCUMENT = "Document"
    FORENSIC = "Forensic"
    FINANCIAL = "Financial"
    MEDIA = "Media"
    BIOMETRIC = "Biometric"
    BALLISTIC = "Ballistic"
    SURVEILLANCE = "Surveillance"

@dataclass
class Evidence:
    id: str
    type: EvidenceType
    description: str
    collected_by: str  # Officer Name
    collected_at: datetime
    location_found: str
    chain_of_custody: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict) # For things like file size, hash, etc.

@dataclass
class IncidentReport:
    id: str
    reporting_officer: Person
    incident_date: datetime
    incident_location: str
    incident_type: str
    narrative: str
    involved_persons: List[Person]
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    weather_condition: Optional[str] = None

@dataclass
class Case:
    id: str
    title: str
    description: str
    crime_type: str
    complexity: str
    date_opened: datetime
    status: str = "OPEN"
    reporting_officer: Optional[Person] = None
    persons: List[Person] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)
    incident_report: Optional[IncidentReport] = None
    documents: List[str] = field(default_factory=list) # Raw text of generated docs
    modifiers: List[str] = field(default_factory=list)

    def add_person(self, person: Person):
        self.persons.append(person)

    def add_evidence(self, evidence: Evidence):
        self.evidence.append(evidence)
