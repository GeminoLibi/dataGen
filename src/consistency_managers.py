"""
Consistency manager classes to maintain internal consistency across case documents.
These managers ensure that entities, locations, jurisdictions, officers, and timelines
remain coherent throughout document generation.
"""

from typing import Dict, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from faker import Faker
import random

fake = Faker()


@dataclass
class Jurisdiction:
    """Represents a consistent jurisdiction for a case."""
    state: str
    county: str
    city: str
    police_department: str
    court_name: str
    judge_name: str
    
    def __post_init__(self):
        """Generate consistent jurisdiction if not provided."""
        if not self.state:
            self.state = "State of " + fake.state()
        if not self.county:
            self.county = fake.city() + " County"
        if not self.city:
            self.city = fake.city()
        if not self.police_department:
            self.police_department = self.city + " Police Department"
        if not self.court_name:
            self.court_name = self.county + " Court"
        if not self.judge_name:
            self.judge_name = "Judge " + fake.last_name()


class JurisdictionManager:
    """Manages consistent jurisdiction information for a case."""
    
    def __init__(self, base_location: Optional[str] = None):
        """
        Initialize jurisdiction manager.
        
        Args:
            base_location: Optional address string to extract location from.
                          If None, generates a consistent jurisdiction.
        """
        self.jurisdiction = self._generate_jurisdiction(base_location)
        self.multi_jurisdictional = False
        self.additional_jurisdictions: List[Jurisdiction] = []
    
    def _generate_jurisdiction(self, base_location: Optional[str] = None) -> Jurisdiction:
        """Generate a consistent jurisdiction."""
        # If base_location provided, try to extract state/city info
        # Otherwise, generate a consistent one
        state = "State of " + fake.state()
        county = fake.city() + " County"
        city = fake.city()
        
        return Jurisdiction(
            state=state,
            county=county,
            city=city,
            police_department=city + " Police Department",
            court_name=county + " Court",
            judge_name="Judge " + fake.last_name()
        )
    
    def get_jurisdiction(self) -> Jurisdiction:
        """Get the primary jurisdiction."""
        return self.jurisdiction
    
    def get_state(self) -> str:
        """Get the state."""
        return self.jurisdiction.state
    
    def get_county(self) -> str:
        """Get the county."""
        return self.jurisdiction.county
    
    def get_city(self) -> str:
        """Get the city."""
        return self.jurisdiction.city
    
    def get_department(self) -> str:
        """Get the police department name."""
        return self.jurisdiction.police_department
    
    def get_court(self) -> str:
        """Get the court name."""
        return self.jurisdiction.court_name
    
    def get_judge(self) -> str:
        """Get the judge name."""
        return self.jurisdiction.judge_name
    
    def set_multi_jurisdictional(self, jurisdictions: List[Jurisdiction]):
        """Set additional jurisdictions for multi-jurisdictional cases."""
        self.multi_jurisdictional = True
        self.additional_jurisdictions = jurisdictions


@dataclass
class OfficerInfo:
    """Information about an officer."""
    name: str
    badge_number: int
    department: str
    rank: str = "Officer"
    
    def __post_init__(self):
        """Set default rank if not provided."""
        if not self.rank:
            self.rank = random.choice(["Officer", "Detective", "Sergeant", "Lieutenant"])


class OfficerRegistry:
    """Maintains consistent officer information across documents."""
    
    def __init__(self, primary_department: str):
        """
        Initialize officer registry.
        
        Args:
            primary_department: The primary police department for the case.
        """
        self.primary_department = primary_department
        self.officers: Dict[str, OfficerInfo] = {}
        self.badge_counter = 1000  # Start badge numbers at 1000
    
    def register_officer(self, name: str, department: Optional[str] = None, 
                         badge_number: Optional[int] = None, rank: Optional[str] = None) -> OfficerInfo:
        """
        Register an officer or get existing officer info.
        
        Args:
            name: Officer's full name
            department: Department name (defaults to primary_department)
            badge_number: Badge number (auto-assigned if not provided)
            rank: Officer rank (defaults to random)
        
        Returns:
            OfficerInfo object
        """
        # Normalize name for lookup
        normalized_name = name.strip()
        
        # If officer already registered, return existing info
        if normalized_name in self.officers:
            return self.officers[normalized_name]
        
        # Create new officer
        if not department:
            department = self.primary_department
        if not badge_number:
            badge_number = self.badge_counter
            self.badge_counter += 1
        
        officer = OfficerInfo(
            name=normalized_name,
            badge_number=badge_number,
            department=department,
            rank=rank or random.choice(["Officer", "Detective", "Sergeant", "Lieutenant"])
        )
        
        self.officers[normalized_name] = officer
        return officer
    
    def get_officer(self, name: str) -> Optional[OfficerInfo]:
        """Get officer info by name."""
        return self.officers.get(name.strip())
    
    def get_badge(self, name: str) -> int:
        """Get badge number for an officer."""
        officer = self.get_officer(name)
        if officer:
            return officer.badge_number
        # If not found, register with auto-assigned badge
        return self.register_officer(name).badge_number
    
    def get_department(self, name: str) -> str:
        """Get department for an officer."""
        officer = self.get_officer(name)
        if officer:
            return officer.department
        # If not found, register with default department
        return self.register_officer(name).department
    
    def get_rank(self, name: str) -> str:
        """Get rank for an officer."""
        officer = self.get_officer(name)
        if officer:
            return officer.rank
        return self.register_officer(name).rank


@dataclass
class EntityAttributes:
    """Attributes of an entity (person)."""
    name: str
    gender: str
    age: int
    physical_description: str
    address: str
    phone_number: Optional[str] = None
    height: str = ""
    weight: int = 0
    hair_color: str = ""
    eye_color: str = ""
    facial_hair: str = ""
    build: str = ""
    driver_license_number: str = ""
    driver_license_state: str = ""
    
    def matches(self, other: 'EntityAttributes', strict: bool = False) -> Tuple[bool, List[str]]:
        """
        Check if this entity matches another.
        
        Args:
            other: Other entity to compare
            strict: If True, requires exact match. If False, allows minor variations.
        
        Returns:
            Tuple of (matches, list of differences)
        """
        differences = []
        
        # Name matching (allows for typos if not strict)
        if strict:
            if self.name.lower() != other.name.lower():
                differences.append(f"Name mismatch: '{self.name}' vs '{other.name}'")
        else:
            # Allow for minor typos (e.g., "Sarah Rogers" vs "S rahaRogers")
            name1_clean = ''.join(self.name.lower().split())
            name2_clean = ''.join(other.name.lower().split())
            if name1_clean != name2_clean and abs(len(name1_clean) - len(name2_clean)) > 2:
                differences.append(f"Name mismatch: '{self.name}' vs '{other.name}'")
        
        # Gender must match
        if self.gender.lower() != other.gender.lower():
            differences.append(f"Gender mismatch: '{self.gender}' vs '{other.gender}'")
        
        # Age can vary slightly (allow ±5 years for witness descriptions)
        if not strict and abs(self.age - other.age) > 5:
            differences.append(f"Age mismatch: {self.age} vs {other.age}")
        elif strict and self.age != other.age:
            differences.append(f"Age mismatch: {self.age} vs {other.age}")
        
        return len(differences) == 0, differences


class EntityValidator:
    """Validates and maintains entity consistency."""
    
    def __init__(self):
        """Initialize entity validator."""
        self.entities: Dict[str, EntityAttributes] = {}
        self.known_errors: Dict[str, Dict[str, str]] = {}  # entity_name -> {field: error_value}
    
    def register_entity(self, name: str, gender: str, age: int, 
                       physical_description: str, address: str, 
                       phone_number: Optional[str] = None,
                       height: str = "", weight: int = 0,
                       hair_color: str = "", eye_color: str = "",
                       facial_hair: str = "", build: str = "",
                       driver_license_number: str = "", driver_license_state: str = "") -> EntityAttributes:
        """
        Register an entity or get existing entity.
        
        Args:
            name: Entity's full name
            gender: Gender (male/female/other)
            age: Age in years
            physical_description: Physical description
            address: Address
            phone_number: Optional phone number
        
        Returns:
            EntityAttributes object
        """
        normalized_name = name.strip()
        
        # If entity already registered, validate consistency
        if normalized_name in self.entities:
            existing = self.entities[normalized_name]
            new_attrs = EntityAttributes(
                name=normalized_name,
                gender=gender,
                age=age,
                physical_description=physical_description,
                address=address,
                phone_number=phone_number
            )
            
            matches, differences = existing.matches(new_attrs, strict=True)
            if not matches:
                # Log the inconsistency but keep existing (first registration wins)
                print(f"Warning: Entity '{normalized_name}' registered with different attributes: {differences}")
            return existing
        
        # Register new entity
        entity = EntityAttributes(
            name=normalized_name,
            gender=gender,
            age=age,
            physical_description=physical_description,
            address=address,
            phone_number=phone_number,
            height=height,
            weight=weight,
            hair_color=hair_color,
            eye_color=eye_color,
            facial_hair=facial_hair,
            build=build,
            driver_license_number=driver_license_number,
            driver_license_state=driver_license_state
        )
        self.entities[normalized_name] = entity
        return entity
    
    def get_entity(self, name: str) -> Optional[EntityAttributes]:
        """Get entity attributes by name."""
        return self.entities.get(name.strip())
    
    def validate_consistency(self, name: str, gender: Optional[str] = None,
                           age: Optional[int] = None, 
                           physical_description: Optional[str] = None) -> Tuple[bool, List[str]]:
        """
        Validate that provided attributes match registered entity.
        
        Returns:
            Tuple of (is_consistent, list_of_errors)
        """
        entity = self.get_entity(name)
        if not entity:
            return True, []  # Entity not registered yet, can't validate
        
        errors = []
        
        if gender and entity.gender.lower() != gender.lower():
            errors.append(f"Gender mismatch for {name}: registered '{entity.gender}', provided '{gender}'")
        
        if age and abs(entity.age - age) > 2:  # Allow 2 year variance
            errors.append(f"Age mismatch for {name}: registered {entity.age}, provided {age}")
        
        if physical_description and entity.physical_description.lower() != physical_description.lower():
            # Physical description can vary, so only flag major contradictions
            if "male" in entity.physical_description.lower() and "female" in physical_description.lower():
                errors.append(f"Gender contradiction in description for {name}")
            elif "female" in entity.physical_description.lower() and "male" in physical_description.lower():
                errors.append(f"Gender contradiction in description for {name}")
        
        return len(errors) == 0, errors
    
    def record_error(self, entity_name: str, field: str, error_value: str):
        """Record an intentional error (typo) for an entity."""
        normalized_name = entity_name.strip()
        if normalized_name not in self.known_errors:
            self.known_errors[normalized_name] = {}
        self.known_errors[normalized_name][field] = error_value
    
    def get_error(self, entity_name: str, field: str) -> Optional[str]:
        """Get a recorded error for an entity field."""
        normalized_name = entity_name.strip()
        if normalized_name in self.known_errors:
            return self.known_errors[normalized_name].get(field)
        return None


class TimelineManager:
    """Manages temporal consistency across documents."""
    
    def __init__(self, incident_time: datetime):
        """
        Initialize timeline manager.
        
        Args:
            incident_time: The base incident time
        """
        self.incident_time = incident_time
        self.events: List[Tuple[datetime, str]] = []  # (time, event_description)
        self._calculate_derived_times()
    
    def _calculate_derived_times(self):
        """Calculate derived times based on incident time."""
        # 911 call: typically 0-30 minutes after incident (or before if witness)
        # For most crimes, call happens shortly after
        delay_minutes = random.randint(0, 30)
        self.call_time = self.incident_time + timedelta(minutes=delay_minutes)
        
        # CAD dispatch: typically 0-2 minutes after 911 call
        self.dispatch_time = self.call_time + timedelta(minutes=random.randint(0, 2))
        
        # Response time: typically 3-15 minutes after dispatch
        self.response_time = self.dispatch_time + timedelta(minutes=random.randint(3, 15))
        
        # Scene processing: starts at response time, lasts 1-4 hours
        self.scene_start = self.response_time
        self.scene_end = self.scene_start + timedelta(hours=random.randint(1, 4))
        
        # Search warrants: typically 4-48 hours after incident
        warrant_delay = random.randint(4, 48)
        self.warrant_time = self.incident_time + timedelta(hours=warrant_delay)
        
        # Add events to timeline
        self.events.append((self.incident_time, "Incident occurred"))
        self.events.append((self.call_time, "911 call received"))
        self.events.append((self.dispatch_time, "CAD dispatch"))
        self.events.append((self.response_time, "Officers arrived on scene"))
        self.events.append((self.scene_start, "Scene processing began"))
        self.events.append((self.scene_end, "Scene processing completed"))
    
    def get_incident_time(self) -> datetime:
        """Get the incident time."""
        return self.incident_time
    
    def get_911_time(self) -> datetime:
        """Get the 911 call time."""
        return self.call_time
    
    def get_dispatch_time(self) -> datetime:
        """Get the CAD dispatch time."""
        return self.dispatch_time
    
    def get_response_time(self) -> datetime:
        """Get the officer response time."""
        return self.response_time
    
    def get_scene_start(self) -> datetime:
        """Get scene processing start time."""
        return self.scene_start
    
    def get_scene_end(self) -> datetime:
        """Get scene processing end time."""
        return self.scene_end
    
    def get_warrant_time(self) -> datetime:
        """Get search warrant time."""
        return self.warrant_time
    
    def add_event(self, time: datetime, description: str):
        """Add a custom event to the timeline."""
        self.events.append((time, description))
        self.events.sort(key=lambda x: x[0])  # Keep sorted
    
    def validate_sequence(self, times: List[datetime]) -> Tuple[bool, List[str]]:
        """
        Validate that a sequence of times is logical.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        sorted_times = sorted(times)
        
        for i in range(len(sorted_times) - 1):
            if sorted_times[i] > sorted_times[i + 1]:
                errors.append(f"Time sequence error: {sorted_times[i]} before {sorted_times[i + 1]}")
        
        return len(errors) == 0, errors
    
    def get_time_for_event_type(self, event_type: str) -> Optional[datetime]:
        """Get time for a specific event type."""
        event_map = {
            "incident": self.incident_time,
            "911": self.call_time,
            "dispatch": self.dispatch_time,
            "response": self.response_time,
            "scene_start": self.scene_start,
            "scene_end": self.scene_end,
            "warrant": self.warrant_time
        }
        return event_map.get(event_type.lower())


@dataclass
class LocationInfo:
    """Information about a location."""
    address: str
    city: str
    state: str
    latitude: float
    longitude: float
    location_type: str  # "incident", "victim", "suspect", "search", etc.


class LocationManager:
    """Manages geographic consistency."""
    
    def __init__(self, primary_location: Optional[LocationInfo] = None):
        """
        Initialize location manager.
        
        Args:
            primary_location: Primary location (incident location)
        """
        self.primary_location = primary_location
        self.locations: Dict[str, LocationInfo] = {}  # location_type -> LocationInfo
        if primary_location:
            self.locations["incident"] = primary_location
    
    def set_primary_location(self, address: str, city: str, state: str, 
                           lat: float, lon: float):
        """Set the primary (incident) location."""
        location = LocationInfo(
            address=address,
            city=city,
            state=state,
            latitude=lat,
            longitude=lon,
            location_type="incident"
        )
        self.primary_location = location
        self.locations["incident"] = location
    
    def add_location(self, location_type: str, address: str, city: str, 
                    state: str, lat: float, lon: float):
        """Add a related location."""
        location = LocationInfo(
            address=address,
            city=city,
            state=state,
            latitude=lat,
            longitude=lon,
            location_type=location_type
        )
        self.locations[location_type] = location
    
    def get_location(self, location_type: str) -> Optional[LocationInfo]:
        """Get a location by type."""
        return self.locations.get(location_type)
    
    def get_primary_location(self) -> Optional[LocationInfo]:
        """Get the primary location."""
        return self.primary_location
    
    def validate_geographic_consistency(self, max_distance_miles: float = 50.0) -> Tuple[bool, List[str]]:
        """
        Validate that related locations are within reasonable distance.
        
        Args:
            max_distance_miles: Maximum distance in miles for related locations
        
        Returns:
            Tuple of (is_consistent, list_of_warnings)
        """
        warnings = []
        
        if not self.primary_location:
            return True, []
        
        # Check all locations are in same state (unless multi-jurisdictional)
        states = set()
        for loc in self.locations.values():
            states.add(loc.state)
        
        if len(states) > 1:
            warnings.append(f"Multiple states in case: {', '.join(states)}. Consider if multi-jurisdictional.")
        
        # Check distances (simplified - would need proper geodetic calculation for production)
        # For now, just check if cities are the same
        cities = set()
        for loc in self.locations.values():
            cities.add(loc.city)
        
        if len(cities) > 3:  # More than 3 different cities might be suspicious
            warnings.append(f"Many different cities in case: {', '.join(cities)}")
        
        return len(warnings) == 0, warnings

