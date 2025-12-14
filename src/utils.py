from faker import Faker
import random
import math
from datetime import datetime, timedelta
from typing import Optional, List, Tuple, Dict
from .models import Person, Role, Vehicle, DigitalDevice, Weapon

fake = Faker()

# --- RNG MECHANICS ---
def d20() -> int:
    return random.randint(1, 20)

def roll_check(threshold: int, modifier: int = 0) -> bool:
    """Returns True if d20 + modifier >= threshold."""
    return (d20() + modifier) >= threshold

# --- GEOSPATIAL ---
class GeoManager:
    def __init__(self):
        self.center_lat = float(fake.latitude())
        self.center_lon = float(fake.longitude())
        
    def get_coords_in_radius(self, lat: float, lon: float, radius_km: float) -> Tuple[float, float]:
        radius_deg = radius_km / 111.0
        u = random.random()
        v = random.random()
        w = radius_deg * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)
        new_lat = lat + x
        new_lon = lon + (y / math.cos(math.radians(lat)))
        return (new_lat, new_lon)

    def get_random_city_location(self) -> Tuple[float, float]:
        return self.get_coords_in_radius(self.center_lat, self.center_lon, 15.0)

geo_mgr = GeoManager()

# --- CHARACTER GENERATION ---

def generate_personality() -> str:
    """Generate RPG-style personality archetype for characters."""
    archetypes = [
        "Aggressive", "Cowardly", "Charismatic", "Deceptive", "Intelligent",
        "Impulsive", "Methodical", "Paranoid", "Reckless", "Sociopathic",
        "Calculating", "Erratic", "Confident", "Insecure", "Manipulative"
    ]
    return random.choice(archetypes)

def generate_criminal_history(age: int) -> List[str]:
    """Generate criminal history based on age - older characters more likely to have records."""
    if age < 21:
        return []
    elif age < 30:
        if random.random() < 0.3:
            return [random.choice(["Misdemeanor Possession", "Minor Theft", "Disorderly Conduct"])]
    elif age < 40:
        if random.random() < 0.5:
            return [random.choice(["Felony Theft", "Assault", "Drug Possession", "Burglary"])]
    else:
        if random.random() < 0.7:
            return [random.choice(["Felony Assault", "Robbery", "Drug Distribution", "Burglary", "Battery"])]
    return []

# --- EVIDENCE GENERATORS ---

def generate_evidence_bagging_log(officer_name: str, date: datetime, items: List[str]) -> str:
    """Generates a log of how evidence was packaged."""
    doc = f"--- EVIDENCE COLLECTION & PACKAGING LOG ---\n"
    doc += f"Collecting Officer: {officer_name}\n"
    doc += f"Date/Time: {date.strftime('%Y-%m-%d %H:%M')}\n\n"
    
    doc += "ITEM INVENTORY:\n"
    
    for i, item in enumerate(items, 1):
        bag_type = "Paper Bag" # Default for bio
        if "Phone" in item or "Laptop" in item:
            bag_type = "Faraday Bag (Anti-Static)"
        elif "Gun" in item or "Knife" in item:
            bag_type = "Cardboard Box (Zip-tied)"
        elif "Drugs" in item or "Powder" in item:
            bag_type = "Heat-Sealed Plastic"
            
        seal_num = fake.random_number(digits=7)
        doc += f"{i}. {item}\n"
        doc += f"   - Container: {bag_type}\n"
        doc += f"   - Seal #: {seal_num}\n"
        doc += f"   - Location: Property Room Shelf {random.randint(1,100)}\n"
        
    doc += "\nI certify that these items were sealed in my presence."
    return doc

def generate_discovery_index(case_id: str, defendant: str, charges: str) -> str:
    """Generates the cover sheet for the prosecutor."""
    doc = f"--- DISTRICT ATTORNEY DISCOVERY INDEX ---\n"
    doc += f"Case Number: {case_id}\n"
    doc += f"Defendant: {defendant}\n"
    doc += f"Charges: {charges}\n"
    doc += f"Date Prepared: {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    doc += "CONTENTS PROVIDED:\n"
    doc += "[X] Incident Report\n"
    doc += "[X] Witness Statements (Redacted)\n"
    doc += "[X] CAD Logs\n"
    doc += "[X] Search Warrants & Returns\n"
    doc += "[ ] Lab Results (Pending)\n"
    doc += "[ ] Body Worn Camera Footage (Processing)\n\n"
    
    doc += "PROSECUTOR NOTES:\n"
    doc += "- Flight risk assessment: High.\n"
    doc += "- Prior felonies noted in NCIC.\n"
    doc += "- Ensure chain of custody for Item #1 is airtight before prelim.\n"
    
    return doc

# ... (Previous helper functions maintained below) ...

def generate_cad_log(call_time: datetime, address: str, crime_type: str, 
                     caller_name: Optional[str] = None, caller_gender: Optional[str] = None) -> str:
    """Generate detailed Computer-Aided Dispatch log with realistic codes and actions."""
    incident_num = f"INC-{fake.random_number(digits=8)}"

    # Determine signal codes based on crime type
    signal_codes = {
        "Burglary": "10-31B (Burglary In Progress)",
        "Assault": "10-10 (Fight/Assault)",
        "Robbery": "10-31A (Robbery In Progress)",
        "Homicide": "10-54 (Possible Death)",
        "Drug Possession": "10-32 (Drug Activity)",
        "Domestic Violence": "10-15 (Domestic Dispute)",
        "Stalking": "10-28 (Suspicious Person)",
        "Arson": "10-70 (Fire Alarm)",
        "Theft": "10-57 (Theft)",
        "Fraud": "10-28 (Suspicious Person)"
    }
    signal = signal_codes.get(crime_type, "10-28 (Suspicious Activity)")

    # Use provided caller info or generate random
    if caller_gender:
        caller_desc = caller_gender.upper()
    else:
        caller_desc = random.choice(["FEMALE", "MALE"])
    
    caller_state = random.choice(["HYSTERICAL", "CALM", "UPSET", "FRIGHTENED", "ANGRY"])

    doc = f"--- COMPUTER AIDED DISPATCH (CAD) INCIDENT REPORT ---\n"
    doc += f"Incident #: {incident_num}\n"
    doc += f"Date: {call_time.strftime('%Y-%m-%d')}\n"
    doc += f"CAD System: Versaterm v{random.randint(8, 12)}.{random.randint(0, 9)}\n"
    doc += f"Dispatcher: {fake.first_name()} {fake.last_name()[0]}.\n"
    doc += f"Priority: {random.choice(['PRIORITY 1', 'PRIORITY 2', 'PRIORITY 3'])}\n"
    doc += f"Call Type: {crime_type.upper()}\n"
    doc += f"Signal: {signal}\n"
    doc += f"Location: {address}\n"
    doc += f"Cross Streets: {fake.street_name()} & {fake.street_name()}\n"
    doc += f"Zone: {random.randint(10, 99)}\n"
    doc += f"Beat: {random.randint(100, 999)}\n\n"

    # Timeline with detailed actions
    t0 = call_time
    doc += f"[{t0.strftime('%H:%M:%S')}] CALL RECEIVED - 911 Transfer from Primary PSAP\n"
    if caller_name:
        doc += f"[{t0.strftime('%H:%M:%S')}] CALLER: {caller_name.upper()}, {caller_desc}, {caller_state}, REPORTING {crime_type.upper()} IN PROGRESS\n"
    else:
        doc += f"[{t0.strftime('%H:%M:%S')}] CALLER: {caller_desc}, {caller_state}, REPORTING {crime_type.upper()} IN PROGRESS\n"
    doc += f"[{t0.strftime('%H:%M:%S')}] LOCATION VERIFIED: {address.upper()}\n"

    t1 = t0 + timedelta(seconds=45)
    doc += f"[{t1.strftime('%H:%M:%S')}] UNITS ASSIGNED: 415-ADAM (ADAM-{random.randint(100,999)}), 415-BOY (BOY-{random.randint(100,999)})\n"
    doc += f"[{t1.strftime('%H:%M:%S')}] RESPONSE: CODE 2 (URGENT)\n"
    doc += f"[{t1.strftime('%H:%M:%S')}] RP ADVISES SUSPECT POSSIBLY STILL ON SCENE\n"

    t2 = t0 + timedelta(minutes=2, seconds=15)
    doc += f"[{t2.strftime('%H:%M:%S')}] UNIT 415-ADAM: EN ROUTE FROM {fake.street_name().upper()}\n"
    doc += f"[{t2.strftime('%H:%M:%S')}] UNIT 415-BOY: EN ROUTE FROM {fake.street_name().upper()}\n"
    doc += f"[{t2.strftime('%H:%M:%S')}] ETA: 3-4 MINUTES\n"

    t3 = t0 + timedelta(minutes=3, seconds=30)
    doc += f"[{t3.strftime('%H:%M:%S')}] UNIT 415-ADAM: ARRIVED ON SCENE\n"
    doc += f"[{t3.strftime('%H:%M:%S')}] UNIT 415-ADAM: 10-97 (ON SCENE)\n"
    doc += f"[{t3.strftime('%H:%M:%S')}] UNIT 415-ADAM: REPORTS SEEING SUSPECT FLEEING ON FOOT\n"

    t4 = t0 + timedelta(minutes=4, seconds=10)
    doc += f"[{t4.strftime('%H:%M:%S')}] UNIT 415-BOY: ARRIVED ON SCENE\n"
    doc += f"[{t4.strftime('%H:%M:%S')}] UNIT 415-BOY: 10-97 (ON SCENE)\n"
    doc += f"[{t4.strftime('%H:%M:%S')}] UNITS ESTABLISHING PERIMETER\n"

    t5 = t0 + timedelta(minutes=5, seconds=45)
    doc += f"[{t5.strftime('%H:%M:%S')}] UNIT 415-ADAM: REQUESTING SUPERVISOR - 10-39\n"
    doc += f"[{t5.strftime('%H:%M:%S')}] SUPERVISOR 415-SAM: 10-39 (SUPERVISOR REQUEST)\n"

    t6 = t0 + timedelta(minutes=7, seconds=20)
    doc += f"[{t6.strftime('%H:%M:%S')}] DETECTIVES EN ROUTE - CRIME SCENE UNIT REQUESTED\n"
    doc += f"[{t6.strftime('%H:%M:%S')}] UNIT 415-ADAM: SECURE - CODE 4\n"
    doc += f"[{t6.strftime('%H:%M:%S')}] INCIDENT CONTAINED\n"

    doc += f"\nDISPOSITION: REPORT TAKEN\n"
    doc += f"CLEARANCE CODE: 10-8 (IN SERVICE)\n"
    doc += f"FOLLOW-UP REQUIRED: DETECTIVES\n"
    doc += f"CASE NUMBER ASSIGNED: {fake.random_number(digits=8)}\n"

    doc += f"\nCAD NOTES:\n"
    doc += f"• RP PROVIDED DESCRIPTION: MALE, 30S, HOODIE, FLEEING SOUTHBOUND\n"
    doc += f"• SUSPECT VEHICLE POSSIBLY PARKED NEARBY\n"
    doc += f"• WITNESSES ON SCENE\n"
    doc += f"• PROPERTY DAMAGE REPORTED\n"
    doc += f"• MEDICAL AID NOT REQUIRED\n"

    return doc

def generate_lineup_form(witness: Person, suspect: Person) -> str:
    doc = f"--- PHOTO LINEUP FORM ---\nWitness: {witness.full_name}\n"
    if witness.reliability_score > 80: doc += f"Witness identified {suspect.full_name}."
    else: doc += "No identification made."
    return doc

def generate_soil_analysis_report(suspect_name: str, location_a: str, location_b: str) -> str:
    doc = f"--- SOIL ANALYSIS ---\nSample A: {location_a}\nSample B: {location_b}\n"
    if d20() > 15: doc += "CONCLUSION: MATCH."
    else: doc += "CONCLUSION: INCONCLUSIVE."
    return doc

def generate_infotainment_log(vehicle: Vehicle, crime_time: datetime) -> str:
    """Generate comprehensive vehicle infotainment system logs."""
    vin = getattr(vehicle, 'vin', fake.vin())
    license_plate = getattr(vehicle, 'license_plate', fake.license_plate())

    # Generate multiple log entries around the crime time
    log_entries = []
    for i in range(random.randint(5, 15)):
        time_offset = timedelta(minutes=random.randint(-30, 30))
        event_time = crime_time + time_offset

        events = [
            "Door unlocked via key fob",
            "Engine started",
            "Radio turned on - Station 95.5 FM",
            "Navigation: Route calculated to downtown",
            "Bluetooth connected - Phone paired",
            "Air conditioning adjusted",
            "Seat position changed",
            "Hard braking detected",
            "Speed exceeded 70 mph",
            "Turn signal activated",
            "Emergency brake applied",
            "Rear camera activated",
            "Phone call initiated",
            "Music paused",
            "GPS location logged",
            "Fuel level low warning",
            "Tire pressure warning",
            "Maintenance reminder displayed"
        ]

        event = random.choice(events)
        log_entries.append(f"{event_time.strftime('%Y-%m-%d %H:%M:%S')} | {event}")

    log_entries.sort()  # Sort by time

    report = f"""--- VEHICLE INFOTAINMENT SYSTEM LOG ---

Vehicle Information:
VIN: {vin}
License Plate: {license_plate}
Make/Model: {getattr(vehicle, 'make', 'Unknown')}/{getattr(vehicle, 'model', 'Unknown')}
Year: {getattr(vehicle, 'year', random.randint(2015, 2024))}

System Logs (Extracted {len(log_entries)} events):

{chr(10).join(log_entries)}

Note: Logs extracted from vehicle's CAN bus and infotainment ECU.
Data integrity verified with MD5: {fake.md5()}

Extracted by: Forensic Technician {fake.last_name()}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    return report

def generate_predictive_policing_report(location: str, crime_type: str) -> str:
    """Generate a comprehensive predictive policing analytics report."""
    report_date = datetime.now()
    analysis_period = f"{(report_date - timedelta(days=90)).strftime('%m/%d/%Y')} to {report_date.strftime('%m/%d/%Y')}"

    # Generate fake crime statistics and risk factors
    historical_crimes = random.randint(15, 45)
    risk_score = random.randint(75, 95)
    trend_direction = random.choice(["Increasing", "Stable", "Decreasing"])

    # Generate neighborhood analysis
    demographics = f"""
    Population Density: {random.randint(2500, 8500)} per sq mile
    Median Income: ${random.randint(35000, 125000):,}
    Unemployment Rate: {random.uniform(3.2, 12.8):.1f}%
    Education Level: {random.randint(65, 92)}% high school graduate
    Home Ownership: {random.randint(45, 85)}%
    """

    # Generate risk factors
    risk_factors = [
        f"Recent {crime_type.lower()} incidents in area",
        f"{random.randint(2, 8)}x higher than city average for {crime_type.lower()}",
        f"Proximity to {random.choice(['highway', 'commercial district', 'industrial area', 'residential complex'])}",
        f"Street lighting deficiencies noted in {random.randint(15, 35)}% of area",
        f"Known gang activity in adjacent zones",
        f"Recent population influx from high-crime areas",
        f"Limited police presence after 2200 hours",
        f"Multiple vacant properties in sector"
    ]

    # Generate patrol recommendations
    recommendations = [
        f"Increase patrol frequency in Zone {location} by {random.randint(25, 75)}%",
        f"Implement targeted enforcement on {random.choice(['traffic violations', 'loitering', 'curfew compliance', 'property maintenance'])}",
        f"Coordinate with local businesses for improved surveillance",
        f"Install additional CCTV cameras at key intersections",
        f"Conduct community outreach and problem-solving meetings",
        f"Partner with code enforcement for blight reduction",
        f"Implement license plate recognition in high-risk areas",
        f"Deploy plainclothes officers for proactive enforcement"
    ]

    report = f"""--- PREDICTIVE POLICING ANALYTICS REPORT ---

DEPARTMENT OF PUBLIC SAFETY
{fake.city().upper()} POLICE DEPARTMENT
Predictive Analytics Division

REPORT ID: PRED-{random.randint(10000, 99999)}
GENERATED: {report_date.strftime('%B %d, %Y at %H:%M:%S')}
ANALYSIS PERIOD: {analysis_period}
SYSTEM VERSION: CrimePredict v{random.randint(3, 7)}.{random.randint(0, 9)}.{random.randint(0, 9)}

TARGET ZONE ANALYSIS: {location}

================================================================================
EXECUTIVE SUMMARY
================================================================================

This automated predictive analytics report identifies Zone {location} as having
elevated risk for {crime_type.lower()} incidents. The zone's risk score of {risk_score}/100
places it in the top {random.randint(5, 25)}% of city zones for {crime_type.lower()} potential.

Key findings include {historical_crimes} reported {crime_type.lower()} incidents over the
analysis period, representing a {trend_direction.lower()} trend compared to previous quarters.

================================================================================
DEMOGRAPHIC ANALYSIS
================================================================================

{demographics}

================================================================================
CRIME PATTERN ANALYSIS
================================================================================

INCIDENT BREAKDOWN:
- Total {crime_type} incidents: {historical_crimes}
- Average incidents per month: {historical_crimes/3:.1f}
- Peak incident times: {random.choice(['Evening hours (1800-2200)', 'Late night (2200-0200)', 'Early morning (0200-0600)', 'Weekend afternoons'])}

SPATIAL ANALYSIS:
- Crime hotspots identified: {random.randint(3, 8)}
- Street segments with elevated risk: {random.randint(12, 28)}
- Geographic clustering coefficient: {random.uniform(0.65, 0.89):.2f}

TEMPORAL PATTERNS:
- Day of week distribution: {random.choice(['Friday-Saturday peak', 'Wednesday peak', 'Weekend concentration', 'Distributed throughout week'])}
- Seasonal variation: {random.choice(['Summer increase', 'Winter concentration', 'No seasonal pattern', 'Holiday-related spikes'])}

================================================================================
RISK FACTORS IDENTIFIED
================================================================================

PRIMARY RISK FACTORS:
{chr(10).join(f"• {factor}" for factor in risk_factors[:4])}

SECONDARY RISK FACTORS:
{chr(10).join(f"• {factor}" for factor in risk_factors[4:])}

================================================================================
PATROL DEPLOYMENT RECOMMENDATIONS
================================================================================

IMMEDIATE ACTIONS (Next 72 hours):
{chr(10).join(f"{i+1}. {rec}" for i, rec in enumerate(recommendations[:3]))}

SHORT-TERM STRATEGIES (Next 30 days):
{chr(10).join(f"{i+1}. {rec}" for i, rec in enumerate(recommendations[3:6]))}

LONG-TERM PREVENTION (Next 90 days):
{chr(10).join(f"{i+1}. {rec}" for i, rec in enumerate(recommendations[6:]))}

================================================================================
STATISTICAL CONFIDENCE
================================================================================

Model Accuracy: {random.randint(78, 92)}%
False Positive Rate: {random.uniform(8.5, 23.2):.1f}%
Area Under Curve (AUC): {random.uniform(0.82, 0.94):.2f}

Data Sources Integrated:
- Crime incident reports (weighted: {random.randint(35, 55)}%)
- 911 call data (weighted: {random.randint(15, 25)}%)
- Traffic citation data (weighted: {random.randint(5, 15)}%)
- Building permit records (weighted: {random.randint(5, 15)}%)
- Utility service calls (weighted: {random.randint(5, 15)}%)

================================================================================
DISCLAIMER AND METHODOLOGY
================================================================================

This report is generated using proprietary predictive algorithms and historical
crime data. Results should be used as investigative guidance and not as the
sole basis for law enforcement decisions.

Methodology: Gradient Boosting Machine with temporal weighting
Training data: 5 years historical incidents
Validation method: 10-fold cross-validation

Report generated automatically by CrimePredict Analytics Engine.
For questions, contact: analytics@{fake.city().lower()}pd.gov

================================================================================
END OF REPORT - CONFIDENTIAL LAW ENFORCEMENT DOCUMENT
================================================================================"""

    return report

def generate_dna_phenotype_report(suspect: Person) -> str:
    return f"--- DNA PHENO ---\nSex: Male"

def generate_nibin_report(casing_id: str, firearm_id: str, weapon, suspect_name: str) -> str:
    """Generate comprehensive NIBIN ballistic analysis report."""
    report_date = datetime.now().strftime('%B %d, %Y')
    case_number = f"NIBIN-{random.randint(100000, 999999)}"

    # Generate detailed ballistic analysis
    lands_grooves = f"{random.randint(4, 8)} lands and {random.randint(4, 8)} grooves, {random.choice(['right', 'left'])} twist"
    caliber = getattr(weapon, 'caliber', '9mm')
    rifling = f"{random.uniform(1.0, 1.5):.2f} inches per turn"

    # Generate multiple comparison results
    comparisons = []
    for i in range(random.randint(8, 15)):
        if i == 0:  # Primary match
            result = "IDENTIFIED MATCH"
            confidence = random.randint(95, 99)
        elif i < 3:  # Possible matches
            result = "POSSIBLE MATCH"
            confidence = random.randint(75, 94)
        else:  # Eliminations
            result = "ELIMINATED"
            confidence = random.randint(0, 74)

        comparisons.append(f"Case #{random.randint(100000, 999999)}: {result} ({confidence}% confidence)")

    report = f"""--- NATIONAL INTEGRATED BALLISTIC INFORMATION NETWORK (NIBIN) REPORT ---

DEPARTMENT OF JUSTICE
BUREAU OF ALCOHOL, TOBACCO, FIREARMS AND EXPLOSIVES
NATIONAL INTEGRATED BALLISTIC INFORMATION NETWORK

REPORT NUMBER: {case_number}
DATE GENERATED: {report_date}
REQUESTING AGENCY: {fake.city()} Police Department
SUBMITTING ANALYST: ATF Special Agent {fake.last_name()}

================================================================================
EVIDENCE SUBMISSION DETAILS
================================================================================

Evidence Item 1: Spent Cartridge Case
- NIBIN Entry ID: {casing_id}
- Caliber: {caliber}
- Case Type: Rimless
- Primer Type: Boxer
- Headstamp: {random.choice(['REM', 'WIN', 'FED', 'CCI', 'SPEER'])}

Evidence Item 2: Suspect Firearm
- NIBIN Entry ID: {firearm_id}
- Make/Model: {getattr(weapon, 'make', 'Unknown')}/{getattr(weapon, 'model', 'Unknown')}
- Serial Number: {getattr(weapon, 'serial_number', 'Unknown')}
- Caliber: {caliber}
- Action Type: {random.choice(['Semi-automatic', 'Revolver', 'Bolt action', 'Pump action'])}

================================================================================
MICROSCOPIC COMPARISON ANALYSIS
================================================================================

RIFLING CHARACTERISTICS:
- Number of Lands/Grooves: {lands_grooves}
- Rifling Twist: {rifling}
- Barrel Length: {random.randint(3, 8)} inches
- Groove Depth: {random.uniform(0.001, 0.003):.4f} inches

STRIATION ANALYSIS:
- Breech face marks: {random.randint(85, 95)}% correlation
- Firing pin impressions: {random.randint(90, 98)}% correlation
- Extractor marks: {random.randint(75, 92)}% correlation
- Ejector marks: {random.randint(70, 88)}% correlation

CLASS CHARACTERISTICS:
- Land impressions width: {random.uniform(0.08, 0.12):.3f} inches
- Groove width: {random.uniform(0.09, 0.13):.3f} inches
- Land/groove ratio: {random.uniform(0.95, 1.05):.2f}

================================================================================
DATABASE COMPARISON RESULTS
================================================================================

NIBIN Database Query Results:
Total cases searched: {random.randint(50000, 200000):,}
Time period: Last 10 years
Geographic scope: National database

COMPARISON SUMMARY:
{chr(10).join(comparisons)}

================================================================================
PRIMARY MATCH ANALYSIS
================================================================================

SUSPECTED FIREARM IDENTIFICATION:
Firearm NIBIN ID: {firearm_id}
Suspect Name: {suspect_name}
Recovery Date: {fake.date_this_year().strftime('%m/%d/%Y')}
Recovery Location: {fake.address().replace(chr(10), ', ')}

BALLISTIC MATCH CONFIDENCE:
- Overall correlation: {random.randint(92, 98)}%
- Individual characteristics match: {random.randint(18, 25)}/{random.randint(18, 25)}
- Statistical significance: p < 0.0001
- Error rate: < 0.001%

================================================================================
IMAGING AND DIGITAL ANALYSIS
================================================================================

MICROSCOPIC IMAGING:
- Magnification used: 20x - 80x
- Lighting: Coaxial illumination
- Image capture: Olympus BX51M microscope
- Digital resolution: 3072 x 2304 pixels

3D TOPOGRAPHIC MAPPING:
- Surface deviation mapping completed
- Depth analysis: {random.uniform(0.0001, 0.001):.5f} inches
- Profile correlation coefficient: {random.uniform(0.85, 0.97):.3f}

DIGITAL COMPARISON SOFTWARE:
- Program: IBIS Trail v{random.randint(4, 7)}.{random.randint(0, 9)}
- Correlation algorithm: Congruent Matching Cells (CMC)
- Minimum correlation threshold: {random.randint(6, 12)} CMC points
- Actual correlation: {random.randint(15, 28)} CMC points

================================================================================
QUALITY ASSURANCE AND VERIFICATION
================================================================================

ANALYSIS PERFORMED BY:
Primary Examiner: ATF Special Agent {fake.last_name()}
- Certification: Certified Firearms Examiner
- Experience: {random.randint(8, 22)} years
- Case load: {random.randint(50, 150)} ballistic cases annually

VERIFICATION BY:
Technical Review Officer: ATF Special Agent {fake.last_name()}
- Independent microscopic examination completed
- Digital correlation analysis verified
- Statistical analysis reviewed

================================================================================
CONCLUSION AND OPINION
================================================================================

OPINION: The microscopic examination and digital comparison analysis reveals
that the cartridge case submitted as evidence (NIBIN ID: {casing_id}) was fired
from the submitted suspect firearm (NIBIN ID: {firearm_id}).

This identification is based on the agreement of all discernible class and
individual microscopic characteristics between the evidence cartridge case
and the test fires from the suspect firearm.

The probability that this cartridge case could have been fired from another
firearm of similar class characteristics is extremely remote.

================================================================================
EVIDENTIARY VALUE ASSESSMENT
================================================================================

This identification provides strong scientific evidence linking the suspect
firearm to the crime scene. The match is based on multiple independent
ballistic signatures and has been verified through independent examination.

REPORT STATUS: FINAL
DATE COMPLETED: {report_date}

________________________________________
ATF Special Agent {fake.last_name()}
Certified Firearms Examiner
Bureau of Alcohol, Tobacco, Firearms and Explosives

CONFIDENTIAL - LAW ENFORCEMENT SENSITIVE
NOT FOR PUBLIC DISCLOSURE

================================================================================
END OF NIBIN BALLISTIC ANALYSIS REPORT
================================================================================"""

    return report

def generate_search_warrant_affidavit(officer: Person, target_address: str, crime_type: str, 
                                     evidence_description: str,
                                     jurisdiction_manager=None, officer_registry=None,
                                     incident_date: Optional[datetime] = None) -> str:
    """Generate a comprehensive search warrant affidavit with probable cause."""
    affidavit_date = datetime.now().strftime('%B %d, %Y')
    
    # Use consistency managers if provided
    if jurisdiction_manager:
        jurisdiction = jurisdiction_manager.get_state()
        county_name = jurisdiction_manager.get_county()
        judge_name = jurisdiction_manager.get_judge()
        court_name = jurisdiction_manager.get_court()
    else:
        # Fallback to random (for backward compatibility)
        jurisdiction = "State of " + fake.state()
        county_name = fake.city() + " County"
        judge_name = "Judge " + fake.last_name()
        court_name = fake.last_name().upper() + " County Court"
    
    if officer_registry:
        department = officer_registry.get_department(officer.full_name)
        badge_number = officer_registry.get_badge(officer.full_name)
    else:
        # Fallback to random (for backward compatibility)
        department = fake.city() + " Police Department"
        badge_number = random.randint(1000, 9999)
    
    # Use incident date if provided, otherwise use current date
    if incident_date:
        incident_date_str = incident_date.strftime('%B %d, %Y')
    else:
        incident_date_str = fake.date_this_year().strftime('%B %d, %Y')

    affidavit = f"""--- SEARCH WARRANT AFFIDAVIT ---

{jurisdiction}
County of {county_name}

BEFORE THE HONORABLE JUDGE OF THE {court_name.upper()}

AFFIDAVIT IN SUPPORT OF SEARCH WARRANT

I, {officer.full_name}, being duly sworn, depose and state:

1. I am a peace officer employed by the {department} with over {random.randint(5, 20)} years of experience in criminal investigations.

2. This affidavit is submitted in support of a search warrant for the following location:
   {target_address}

3. I have probable cause to believe that evidence of {crime_type.lower()} is located at the above premises based on the following facts:

   a) On {incident_date_str}, I responded to a report of {crime_type.lower()} at the incident location.

   b) During the investigation, the following evidence was discovered: {evidence_description}

   c) Based on my training and experience, individuals involved in {crime_type.lower()} typically conceal evidence at their residences.

   d) I have received information from reliable sources indicating that the suspect may have returned to the residence with evidence.

4. The evidence sought includes:
   - Digital devices and storage media
   - Documents related to {crime_type.lower()}
   - Clothing and personal items
   - Financial records and correspondence

5. I believe this evidence is currently located at the premises and will be destroyed or removed if not seized immediately.

6. This affidavit is based on my personal knowledge and investigation of this case.

Dated: {affidavit_date}

__________________________________
{officer.full_name}
Badge #{badge_number}
{department}

SWORN TO AND SUBSCRIBED before me this {affidavit_date}.

__________________________________
{judge_name}
{court_name}"""

    return affidavit

def generate_financial_csv(suspect_name: str, crime_date: datetime) -> str:
    return "Date,Desc,Amt\n2023-01-01,ATM,500"

def generate_search_warrant(officer: Person, target_name: str, target_address: str, 
                           items_to_seize: List[str], crime_type: str,
                           jurisdiction_manager=None, officer_registry=None) -> str:
    """Generate a comprehensive search warrant."""
    warrant_date = datetime.now().strftime('%B %d, %Y')
    
    # Use consistency managers if provided
    if jurisdiction_manager:
        jurisdiction = jurisdiction_manager.get_state()
        county_name = jurisdiction_manager.get_county()
        judge_name = jurisdiction_manager.get_judge()
        court_name = jurisdiction_manager.get_court()
    else:
        # Fallback to random (for backward compatibility)
        jurisdiction = "State of " + fake.state()
        county_name = fake.city() + " County"
        judge_name = "Judge " + fake.last_name()
        court_name = fake.last_name().upper() + " County Court"
    
    if officer_registry:
        department = officer_registry.get_department(officer.full_name)
        badge_number = officer_registry.get_badge(officer.full_name)
    else:
        # Fallback to random (for backward compatibility)
        department = fake.city() + " Police Department"
        badge_number = random.randint(1000, 9999)

    warrant = f"""--- SEARCH WARRANT ---

{jurisdiction}
County of {county_name}

TO: ANY PEACE OFFICER OF {jurisdiction.upper()}

WHEREAS, an affidavit has been filed before me alleging probable cause to believe that certain property, namely:

{chr(10).join(f"- {item}" for item in items_to_seize)}

constituting evidence of the crime of {crime_type.upper()}, is concealed in the following premises:

{target_address}

YOU ARE HEREBY COMMANDED to search the above-described premises and to seize and bring before me all such property as may be found therein.

This warrant shall be executed between the hours of 6:00 AM and 10:00 PM.

Given under my hand this {warrant_date}.

__________________________________
{judge_name}
{court_name}

APPROVED BY AFFIDAVIT OF:
{officer.full_name}
Badge #{badge_number}
{department}

WARRANT #: SW-{random.randint(10000, 99999)}"""

    return warrant

def generate_warrant_return(target_name: str, location: str, items: List[str],
                            officer_registry=None, executing_officer: Optional[str] = None,
                            witnessing_officer: Optional[str] = None) -> str:
    """Generate a warrant return showing what was seized."""
    return_date = datetime.now().strftime('%B %d, %Y')

    # Use officer registry if provided
    if officer_registry and executing_officer:
        exec_name = executing_officer
        exec_badge = officer_registry.get_badge(executing_officer)
    else:
        exec_name = f"Detective {fake.last_name()}"
        exec_badge = random.randint(1000, 9999)
    
    if officer_registry and witnessing_officer:
        witness_name = witnessing_officer
        witness_badge = officer_registry.get_badge(witnessing_officer)
    else:
        witness_name = f"Officer {fake.last_name()}"
        witness_badge = random.randint(1000, 9999)

    return_doc = f"""--- SEARCH WARRANT RETURN ---

WARRANT EXECUTION REPORT

Warrant executed on: {return_date}
Location searched: {location}
Target: {target_name}

ITEMS SEIZED:

{chr(10).join(f"{i+1}. {item}" for i, item in enumerate(items))}

All seized items have been properly documented, photographed, and placed into evidence storage.

Executed by: {exec_name}
Badge #{exec_badge}

Witnessed by: {witness_name}
Badge #{witness_badge}

Date: {return_date}"""

    return return_doc

def generate_lineup_report(witness: Person, suspect: Person) -> str:
    return generate_lineup_form(witness, suspect)

def generate_entomology_report(death_time: datetime, discovery_time: datetime, location: str, weather: str) -> str:
    return "--- ENTOMOLOGY ---\nMaggots found."

def generate_toxicology_screen(victim_name: str, cause_of_death: str) -> str:
    return "--- TOX SCREEN ---\nNegative."

def generate_coroner_scene_notes(victim_name: str, death_time: datetime, discovery_time: datetime) -> str:
    return "--- CORONER ---\nBody cold."

def generate_drone_log(location: str, suspect_desc: str, time: datetime) -> str:
    return f"--- DRONE ---\nVisual on {suspect_desc}"

def generate_k9_report(handler_name: str, location: str, result: str) -> str:
    return f"--- K9 ---\nResult: {result}"

def generate_trash_pull_log(suspect_name: str, date: datetime) -> str:
    return f"--- TRASH PULL ---\nFound nothing."

def generate_afis_report(suspect_name: str, quality: str = "High") -> str:
    """Generate comprehensive AFIS fingerprint analysis report."""
    report_date = datetime.now().strftime('%B %d, %Y')
    case_number = f"AFIS-{random.randint(100000, 999999)}"

    # Generate multiple fingerprint matches with confidence scores
    matches = []
    for i in range(random.randint(3, 8)):
        confidence = random.randint(85, 99) if i == 0 else random.randint(60, 84)
        match_name = suspect_name if i == 0 else fake.name()
        match_type = "Primary Match" if i == 0 else "Possible Match"
        matches.append(f"{match_type}: {match_name} ({confidence}% confidence)")

    report = f"""--- AUTOMATED FINGERPRINT IDENTIFICATION SYSTEM (AFIS) REPORT ---

Case Number: {case_number}
Report Date: {report_date}
Submitting Agency: {fake.city()} Police Department
Analyst: Technician {fake.last_name()}

LATENT PRINT ANALYSIS SUMMARY:

Source: Crime Scene Evidence - Latent Print #LP-{random.randint(1000, 9999)}
Location: Door handle, driver's side
Surface: Metal
Development Method: Ninhydrin/CAB
Quality Assessment: {quality} quality print
Pattern Type: {random.choice(['Whorl', 'Loop', 'Arch'])} pattern

FINGERPRINT COMPARISON RESULTS:

{chr(10).join(matches)}

PRIMARY MATCH DETAILS:
Name: {suspect_name}
DOB: {fake.date_of_birth(minimum_age=18, maximum_age=65).strftime('%m/%d/%Y')}
Last Known Address: {fake.address().replace(chr(10), ', ')}
Criminal History: {random.choice(['None', 'Prior misdemeanor', 'Felony record'])}

Fingerprint Classification:
Henry Classification: {random.randint(1, 32)}/{random.randint(1, 32)}/{random.randint(1, 32)}/{random.randint(1, 32)}

Minutiae Points Analyzed: {random.randint(12, 25)}
Matching Points: {random.randint(10, 22)}
False Rejection Rate: < 0.01%
False Acceptance Rate: < 0.001%

DIGITAL IMAGING:
Scanner: CrossMatch L-Scan Guardian
Resolution: 500 PPI
Compression: WSQ (15:1)
Image Quality Score: {random.randint(85, 98)}/100

VERIFICATION PROCESS:
- Automated comparison completed: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}
- Manual verification by certified technician
- Quality assurance review completed

CONCLUSION:
The latent fingerprint from the crime scene matches the known fingerprint of {suspect_name} with high confidence.

Analyst Signature: _______________________________
{fake.last_name()}, Certified Latent Print Examiner
Date: {report_date}"""

    return report

def generate_uc_report(uc_name: str, suspect_name: str, date: datetime) -> str:
    return f"--- UC REPORT ---\nTarget: {suspect_name}"

def generate_wiretap_transcript(suspect_a: str, suspect_b: str, date: datetime) -> str:
    return f"--- WIRETAP ---\n{suspect_a}: 'Hello'"

def generate_jailhouse_informant_statement(suspect_name: str) -> str:
    return f"--- SNITCH ---\nConfession."

def generate_ncic_report(subject: Person) -> str:
    return f"--- NCIC ---\nSubject: {subject.full_name}"

def generate_iot_logs(device_type: str, owner_name: str, crime_time: datetime) -> str:
    return f"--- IOT ---\nDevice: {device_type}"

def generate_burner_receipt(buyer_desc: str, purchase_date: datetime) -> str:
    """Generate detailed store receipt for burner phone purchase."""
    store_names = ["QuickMart", "Speedy Stop", "Corner Store", "Express Fuels", "Budget Mart"]
    store_name = random.choice(store_names)
    store_address = fake.address().replace('\n', ', ')
    clerk_name = fake.first_name()

    # Generate realistic items
    phone_model = random.choice(["Nokia 1100", "Samsung Prepaid", "Basic Flip Phone", "Tracfone"])
    phone_price = round(random.uniform(15.99, 49.99), 2)
    airtime_amount = random.choice([10, 20, 30, 60])  # minutes
    airtime_price = airtime_amount * 0.10  # $0.10 per minute
    tax_rate = 0.0875  # 8.75% tax
    subtotal = phone_price + airtime_price
    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal + tax, 2)

    receipt_number = fake.random_number(digits=6, fix_len=True)
    register_number = random.randint(1, 8)

    doc = f"""========================================
        {store_name.upper()}
========================================
Store #{random.randint(100,999)} - {store_address}

Date: {purchase_date.strftime('%m/%d/%Y')}
Time: {purchase_date.strftime('%I:%M %p')}
Register: {register_number}
Clerk: {clerk_name}
Receipt #: {receipt_number}

----------------------------------------
QTY  ITEM                 PRICE    TOTAL
----------------------------------------
1    {phone_model:<20} ${phone_price:>6.2f} ${phone_price:>7.2f}
1    {airtime_amount} MIN AIRTIME     ${airtime_price:>6.2f} ${airtime_price:>7.2f}

----------------------------------------
SUBTOTAL:                ${subtotal:>10.2f}
TAX (8.75%):             ${tax:>10.2f}
----------------------------------------
TOTAL:                   ${total:>10.2f}

========================================
PAID BY: CASH
CHANGE:  $0.00

NO REFUNDS OR EXCHANGES
KEEP RECEIPT FOR WARRANTY

========================================
BUYER DESCRIPTION: {buyer_desc}
TIME OF PURCHASE: {purchase_date.strftime('%I:%M:%S %p')}

Thank you for shopping at {store_name}!
========================================
"""

    return doc

# def generate_past_crimes(age: int) -> List[CriminalRecord]: return []
def generate_crypto_address(coin_type="BTC") -> str: return "bc1..."
def generate_blockchain_ledger(suspect_wallet: str, amount: float) -> str: return "--- LEDGER ---"
def generate_bau_profile(crime_type: str) -> str: return "--- BAU ---"
def generate_recovered_data(suspect_name: str) -> str: return "--- DATA ---"
def generate_weather() -> Tuple[str, str]: return ("Clear", "70F")
def generate_witness_statement(witness: Person, suspect: Person, vehicle: Vehicle, crime_type: str, weather: str) -> str:
    """Generate detailed witness statement with personality-driven content."""
    doc = f"--- WITNESS STATEMENT ---\n"
    doc += f"Case Number: {fake.random_number(digits=8)}\n"
    doc += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
    doc += f"Time: {datetime.now().strftime('%H:%M')}\n"
    doc += f"Interviewing Officer: Detective {fake.last_name()}\n"
    doc += f"Witness: {witness.full_name}\n"
    doc += f"Witness DOB: {fake.date_of_birth(minimum_age=witness.age, maximum_age=witness.age).strftime('%Y-%m-%d')}\n"
    doc += f"Witness Address: {witness.address}\n"
    doc += f"Witness Phone: {witness.phone_number}\n"
    doc += f"Witness Reliability Score: {witness.reliability_score}/100\n\n"
    
    doc += f"STATEMENT:\n"
    doc += f"{'='*60}\n\n"
    
    # Personality-driven statement
    if witness.personality == "Anxious":
        doc += f"I was really nervous, you know? I saw something but I'm not 100% sure. "
    elif witness.personality == "Confident":
        doc += f"I'm absolutely certain about what I saw. "
    elif witness.personality == "Cooperative":
        doc += f"I want to help in any way I can. "
    elif witness.personality == "Fearful":
        doc += f"I'm scared to talk about this, but I'll tell you what I know. "
    else:
        doc += f"I witnessed the following: "
    
    # Crime-specific details
    if crime_type == "Burglary":
        doc += f"I was {random.choice(['walking my dog', 'coming home from work', 'taking out the trash', 'checking my mail'])} when I noticed "
        doc += f"{random.choice(['someone breaking a window', 'a person forcing open a door', 'suspicious activity near the house', 'someone running from the property'])}. "
        doc += f"The person was {random.choice(['wearing dark clothing', 'wearing a hoodie', 'dressed in all black', 'wearing a mask'])}. "
    elif crime_type == "Assault":
        doc += f"I saw {random.choice(['a physical altercation', 'someone being attacked', 'a fight break out', 'someone getting hit'])}. "
        doc += f"The attacker was {random.choice(['much larger than the victim', 'about the same size', 'clearly aggressive', 'trying to get away'])}. "
    elif crime_type == "Robbery":
        doc += f"I witnessed {random.choice(['someone being robbed', 'a person demanding money', 'a theft in progress', 'someone being threatened'])}. "
        doc += f"The suspect appeared {random.choice(['armed', 'aggressive', 'nervous', 'calm and collected'])}. "
    
    # Vehicle description if available
    if vehicle:
        doc += f"I also noticed a vehicle - it looked like a {vehicle.color} {vehicle.make} {vehicle.model}. "
        if vehicle.license_plate:
            doc += f"I think the license plate started with {vehicle.license_plate[:3]}, but I'm not sure about the rest. "
    
    # Weather impact on observation
    if "Clear" in weather:
        doc += f"The weather was clear, so I had a good view. "
    elif "Rain" in weather or "Fog" in weather:
        doc += f"The {weather.lower()} made it harder to see clearly. "
    
    # Suspect description - use actual suspect physical description
    doc += f"\n\nSUSPECT DESCRIPTION:\n"
    doc += f"- Approximate age: {suspect.age} years old (give or take 5 years)\n"
    doc += f"- Gender: {suspect.gender.title() if suspect.gender else random.choice(['Male', 'Female', 'Couldn\'t tell'])}\n"
    if suspect.height:
        doc += f"- Height: {suspect.height}\n"
    else:
        doc += f"- Height: {random.choice(['Short (under 5\'6\")', 'Average (5\'6\"-5\'10\")', 'Tall (over 6\')'])}\n"
    if suspect.build:
        doc += f"- Build: {suspect.build.title()}\n"
    else:
        doc += f"- Build: {random.choice(['Slim', 'Average', 'Stocky', 'Athletic', 'Heavy'])}\n"
    if suspect.hair_color:
        doc += f"- Hair color: {suspect.hair_color.title()}\n"
    if suspect.eye_color:
        doc += f"- Eye color: {suspect.eye_color.title()}\n"
    if suspect.facial_hair and suspect.facial_hair != "none":
        doc += f"- Facial hair: {suspect.facial_hair.title()}\n"
    doc += f"- Clothing: {random.choice(['Dark hoodie and jeans', 'All black clothing', 'Casual street clothes', 'Work clothes'])}\n"
    
    # Reliability-based confidence
    if witness.reliability_score > 80:
        doc += f"\nI'm very confident in my description. I got a clear look at the person. "
    elif witness.reliability_score > 60:
        doc += f"\nI'm fairly confident, but some details might be off. "
    else:
        doc += f"\nI'm not completely sure about all the details. It happened fast. "
    
    doc += f"\n\nI am willing to testify in court if necessary.\n"
    doc += f"\nWitness Signature: ___________________________\n"
    doc += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
    doc += f"{'='*60}\n"
    
    return doc
def generate_cctv_log(location: str, subject_desc: str, vehicle_desc: str, activity: str, weather: str) -> str:
    """Generate comprehensive CCTV surveillance log with messy, detailed entries."""
    log_date = datetime.now()
    camera_system = f"{fake.company()} Security DVR System v{random.randint(3, 8)}.{random.randint(0, 9)}"

    # Generate multiple log entries with timestamps
    entries = []
    base_time = log_date.replace(hour=random.randint(18, 23), minute=random.randint(0, 59))

    # System boot and initialization
    entries.append(f"{(base_time - timedelta(minutes=45)).strftime('%H:%M:%S')} | SYSTEM | DVR System initialized - Firmware v2.1.4")
    entries.append(f"{(base_time - timedelta(minutes=44)).strftime('%H:%M:%S')} | CAMERA-01 | Camera online - Resolution: 1920x1080@30fps")
    entries.append(f"{(base_time - timedelta(minutes=44)).strftime('%H:%M:%S')} | CAMERA-02 | Camera online - Resolution: 1920x1080@30fps")
    entries.append(f"{(base_time - timedelta(minutes=44)).strftime('%H:%M:%S')} | CAMERA-03 | Camera online - Night vision activated")
    entries.append(f"{(base_time - timedelta(minutes=43)).strftime('%H:%M:%S')} | STORAGE | Disk array check passed - 95% capacity available")

    # Motion detection and activity
    for i in range(random.randint(8, 15)):
        time_offset = timedelta(minutes=random.randint(0, 40))
        entry_time = base_time - time_offset

        if i == 0:  # Main activity
            entries.append(f"{entry_time.strftime('%H:%M:%S')} | CAMERA-02 | MOTION DETECTED | Zone: {location}")
            entries.append(f"{(entry_time + timedelta(seconds=2)).strftime('%H:%M:%S')} | CAMERA-02 | VIDEO RECORDING | Duration: Continuous")
            entries.append(f"{(entry_time + timedelta(seconds=5)).strftime('%H:%M:%S')} | CAMERA-02 | SUBJECT IDENTIFIED | {subject_desc}")
            if vehicle_desc:
                entries.append(f"{(entry_time + timedelta(seconds=8)).strftime('%H:%M:%S')} | CAMERA-02 | VEHICLE DETECTED | {vehicle_desc}")
        elif i < 4:  # Additional activity
            activities = [
                f"Subject movement detected - {activity}",
                f"Vehicle approaching intersection",
                f"Person loitering near entrance",
                f"Traffic violation observed",
                f"Emergency vehicle response",
                f"Delivery vehicle at loading dock",
                f"Maintenance crew on site",
                f"Customer entering premises"
            ]
            entries.append(f"{entry_time.strftime('%H:%M:%S')} | CAMERA-{random.randint(1,4):02d} | ACTIVITY | {random.choice(activities)}")
        else:  # System/status messages
            system_msgs = [
                "Disk space check - OK",
                "Network connectivity verified",
                "Motion sensitivity calibration",
                "Auto-backup completed",
                "System temperature: 72°F",
                "Video compression ratio: 25:1",
                "Bandwidth usage: 45 Mbps",
                "Storage I/O: 120 MB/s",
                "CPU usage: 35%",
                "Memory usage: 68%"
            ]
            entries.append(f"{entry_time.strftime('%H:%M:%S')} | SYSTEM | STATUS | {random.choice(system_msgs)}")

    # Sort entries by time
    entries.sort()

    report = f"""--- CLOSED CIRCUIT TELEVISION (CCTV) SURVEILLANCE LOG ---

{fake.company().upper()} SECURITY SYSTEM LOG
Location: {location}
Date: {log_date.strftime('%B %d, %Y')}
System: {camera_system}
Operator: Security Analyst {fake.last_name()}

================================================================================
CAMERA SYSTEM CONFIGURATION
================================================================================

PRIMARY CAMERAS:
- Camera 01: Front entrance - 4MP, 2.8mm lens, IR illumination
- Camera 02: Parking lot - 4MP, 6mm lens, Auto-tracking enabled
- Camera 03: Side alley - 2MP, Varifocal 2.7-12mm, Night vision
- Camera 04: Loading dock - 4MP, 180° wide angle, Motion detection

RECORDING PARAMETERS:
- Resolution: 1920x1080 (1080p)
- Frame Rate: 30 FPS
- Compression: H.265
- Retention: 90 days
- Storage: 8TB RAID-5 array
- Backup: Daily to cloud storage

MOTION DETECTION SETTINGS:
- Sensitivity: Medium (Threshold: 15%)
- Minimum object size: 50 pixels
- Detection zones: 8 active zones
- Night mode: Automatic IR switching
- Weather compensation: {weather} conditions active

================================================================================
ACTIVITY LOG - {len(entries)} EVENTS RECORDED
================================================================================

TIMESTAMP | SOURCE | TYPE | DESCRIPTION
----------|--------|------|-------------
{chr(10).join(entries)}

================================================================================
INCIDENT TIMELINE RECONSTRUCTION
================================================================================

PRIMARY INCIDENT SEQUENCE:
1. {base_time.strftime('%H:%M:%S')} - Initial motion detection in Zone B
2. {(base_time + timedelta(seconds=3)).strftime('%H:%M:%S')} - Subject enters camera field of view
3. {(base_time + timedelta(seconds=12)).strftime('%H:%M:%S')} - Activity: {activity}
4. {(base_time + timedelta(seconds=45)).strftime('%H:%M:%S')} - Subject exits camera view
5. {(base_time + timedelta(seconds=120)).strftime('%H:%M:%S')} - Area clears, motion detection resets

WEATHER CONDITIONS DURING RECORDING:
- Temperature: {random.randint(45, 75)}°F
- Visibility: {random.choice(['Clear', 'Light fog', 'Overcast', 'Light rain'])}
- Wind: {random.randint(0, 15)} mph {random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])}
- Lighting: {random.choice(['Street lights active', 'Artificial lighting only', 'Mixed natural/artificial'])}

================================================================================
TECHNICAL ANALYSIS
================================================================================

VIDEO QUALITY ASSESSMENT:
- Overall clarity: {random.choice(['Excellent', 'Good', 'Fair', 'Poor'])} ({random.randint(70, 95)}% confidence)
- Lighting conditions: {random.choice(['Adequate', 'Poor', 'Excellent', 'Marginal'])}
- Subject identification: {random.choice(['Clear facial features', 'Partial identification', 'Silhouette only', 'Obstructed view'])}
- Vehicle identification: {random.choice(['Full license plate visible', 'Partial plate', 'Make/model identifiable', 'Not visible'])}

DIGITAL FORENSIC ANALYSIS:
- File format: MP4 (H.265 encoded)
- File size: {random.randint(500, 2000)} MB
- Duration: {random.randint(30, 120)} minutes
- MD5 hash: {fake.md5()}
- SHA-256 hash: {fake.sha256()}

COMPRESSION ARTIFACTS:
- Blockiness: Minimal ({random.randint(0, 3)}% affected)
- Motion blur: {random.choice(['None', 'Minimal', 'Moderate', 'Significant'])}
- Color accuracy: {random.randint(85, 98)}% fidelity
- Frame drops: {random.randint(0, 5)} frames missing

================================================================================
EVIDENTIARY VALUE ASSESSMENT
================================================================================

RELEVANCE TO INVESTIGATION:
- Subject identification: {random.choice(['Positive ID possible', 'Possible identification', 'Limited identification', 'Identification unlikely'])}
- Timeline correlation: {random.choice(['Strong correlation', 'Moderate correlation', 'Weak correlation', 'No correlation'])}
- Alibi verification: {random.choice(['Supports timeline', 'Contradicts timeline', 'Neutral', 'Insufficient data'])}

ADMISSIBILITY CONSIDERATIONS:
- Chain of custody: Maintained
- Authentication: Digital signatures verified
- Tamper detection: No anomalies detected
- Backup integrity: Verified

================================================================================
REVIEW AND VERIFICATION
================================================================================

LOG REVIEWED BY:
Primary Reviewer: Detective {fake.last_name()}
Badge #{random.randint(1000, 9999)}
Date: {log_date.strftime('%m/%d/%Y')}

Technical Verification:
Video integrity confirmed by IT Forensics
Hash values match original recording
No evidence of tampering detected

SECONDARY REVIEW:
Supervisor: Sergeant {fake.last_name()}
Date: {log_date.strftime('%m/%d/%Y')}

================================================================================
CONCLUSION
================================================================================

This CCTV log documents {len([e for e in entries if 'ACTIVITY' in e or 'MOTION' in e])} suspicious activities
and {len([e for e in entries if 'SUBJECT' in e])} subject identifications during the
review period. The footage has been preserved and is available for court presentation.

Video files archived under case #{random.randint(10000, 99999)}
Total recording time: {random.randint(4, 12)} hours
Storage location: Evidence Server - Folder: {fake.uuid4()}

================================================================================
END OF CCTV SURVEILLANCE LOG
================================================================================

ATTACHMENTS:
- Video still captures (8 images)
- Motion detection timeline
- Camera calibration logs
- System diagnostic report

CONFIDENTIAL - LAW ENFORCEMENT USE ONLY
NOT FOR PUBLIC DISCLOSURE WITHOUT COURT ORDER
================================================================================"""

    return report
def generate_corp_name() -> str: return "Corp"
def generate_case_id() -> str:
    """Generate a unique case ID."""
    return f"CASE-{random.randint(100000, 999999)}"
def generate_physical_description(age: int, gender: str) -> Dict[str, any]:
    """Generate realistic physical description based on age and gender."""
    # Height (in feet and inches)
    if gender.lower() == "male":
        height_feet = random.randint(5, 6)
        height_inches = random.randint(4, 11) if height_feet == 5 else random.randint(0, 5)
        weight = random.randint(140, 220)
    else:  # female or other
        height_feet = random.randint(5, 5)
        height_inches = random.randint(0, 8)
        weight = random.randint(100, 180)
    
    height_str = f"{height_feet}'{height_inches}\""
    
    # Hair color
    hair_colors = ["black", "brown", "blonde", "red", "gray", "white", "auburn"]
    # Older people more likely to have gray/white hair
    if age > 50:
        hair_colors.extend(["gray", "white", "gray"])
    hair_color = random.choice(hair_colors)
    
    # Eye color
    eye_colors = ["brown", "blue", "green", "hazel", "gray"]
    eye_color = random.choice(eye_colors)
    
    # Facial hair (only for males, and less likely with age)
    facial_hair = "none"
    if gender.lower() == "male":
        if age < 30:
            facial_hair = random.choice(["none", "none", "none", "beard", "mustache", "goatee"])
        elif age < 50:
            facial_hair = random.choice(["none", "none", "beard", "mustache", "goatee"])
        else:
            facial_hair = random.choice(["none", "beard", "mustache"])
    
    # Build
    builds = ["slim", "average", "stocky", "muscular", "heavy"]
    build = random.choice(builds)
    
    return {
        "height": height_str,
        "weight": weight,
        "hair_color": hair_color,
        "eye_color": eye_color,
        "facial_hair": facial_hair,
        "build": build
    }


def generate_driver_license(state: Optional[str] = None) -> Tuple[str, str]:
    """Generate a realistic driver's license number and state."""
    if not state:
        state = fake.state_abbr()
    
    # Format varies by state, but common formats:
    # Format 1: 8 digits (e.g., 12345678)
    # Format 2: 1 letter + 7 digits (e.g., A1234567)
    # Format 3: 2 letters + 6 digits (e.g., AB123456)
    
    format_type = random.choice([1, 2, 3])
    if format_type == 1:
        license_num = f"{random.randint(10000000, 99999999)}"
    elif format_type == 2:
        license_num = f"{random.choice('ABCDEFGHJKLMNPRSTUVWXYZ')}{random.randint(1000000, 9999999)}"
    else:
        license_num = f"{random.choice('ABCDEFGHJKLMNPRSTUVWXYZ')}{random.choice('ABCDEFGHJKLMNPRSTUVWXYZ')}{random.randint(100000, 999999)}"
    
    return license_num, state


def generate_person(role: Role = Role.WITNESS, min_age: int = 18, max_age: int = 80) -> Person:
    """Enhanced person generator with RPG attributes and physical descriptions."""
    age = random.randint(min_age, max_age)
    
    # Generate gender (infer from first name or random)
    first_name = fake.first_name()
    # Simple heuristic: names ending in certain letters more likely to be male
    gender = "male" if first_name.lower()[-1] in ['o', 'n', 'r', 's', 't', 'd', 'e', 'k', 'l'] else "female"
    # But add some randomness
    if random.random() < 0.3:
        gender = "male" if gender == "female" else "female"
    
    # Generate physical description
    physical = generate_physical_description(age, gender)
    
    # Generate driver's license (most adults have one)
    driver_license = ""
    driver_license_state = ""
    if age >= 16 and random.random() < 0.85:  # 85% of adults have driver's license
        driver_license, driver_license_state = generate_driver_license()
    
    # Set reliability score for witnesses
    reliability = 50  # Default
    if role == Role.WITNESS:
        if "Paranoid" in generate_personality():
            reliability = random.randint(20, 40)  # Paranoid witnesses are less reliable
        elif "Intelligent" in generate_personality():
            reliability = random.randint(70, 95)  # Intelligent witnesses are more reliable
        else:
            reliability = random.randint(40, 80)

    person = Person(
        id=fake.uuid4(),
        first_name=first_name,
        last_name=fake.last_name(),
        role=role,
        age=age,
        address=fake.address().replace('\n', ', '),
        phone_number=fake.phone_number(),
        personality=generate_personality(),
        criminal_history=generate_criminal_history(age),
        reliability_score=reliability,
        gender=gender,
        height=physical["height"],
        weight=physical["weight"],
        hair_color=physical["hair_color"],
        eye_color=physical["eye_color"],
        facial_hair=physical["facial_hair"],
        build=physical["build"],
        driver_license_number=driver_license,
        driver_license_state=driver_license_state
    )

    # Add social media handle for suspects/victims
    if role in [Role.SUSPECT, Role.VICTIM]:
        person.social_handle = generate_username(person.first_name, person.last_name)

    return person
def generate_browser_history(motive: str, crime_time: datetime) -> List[str]: return ["Search"]
def generate_autopsy_report(victim_name: str, crime_type: str, death_time: datetime) -> str: return "--- AUTOPSY ---"
def generate_weapon(owner_id: str) -> Weapon:
    """Generate a weapon for violent crimes."""
    weapon_types = ["Firearm", "Knife", "Blunt Object"]
    weapon_type = random.choice(weapon_types)

    if weapon_type == "Firearm":
        makes_models = [
            ("Glock", "19", "9mm"), ("Smith & Wesson", "M&P", "9mm"),
            ("Sig Sauer", "P320", "9mm"), ("Ruger", "SR9", "9mm"),
            ("Colt", "1911", ".45 ACP"), ("Remington", "870", "12ga")
        ]
        make, model, caliber = random.choice(makes_models)
    elif weapon_type == "Knife":
        makes_models = [
            ("Benchmade", "Adamas"), ("Spyderco", "Paramilitary 2"),
            ("Cold Steel", "Recon Tanto"), ("KA-BAR", "Fighting Knife"),
            ("Generic", "Kitchen Knife")
        ]
        make, model = random.choice(makes_models)
        caliber = None
    else:  # Blunt Object
        makes_models = [
            ("Generic", "Baseball Bat"), ("Generic", "Hammer"),
            ("Generic", "Crowbar"), ("Generic", "Tire Iron")
        ]
        make, model = random.choice(makes_models)
        caliber = None

    return Weapon(
        id=fake.uuid4(),
        type=weapon_type,
        make=make,
        model=model,
        caliber=caliber,
        serial_number=fake.random_number(digits=8, fix_len=True),
        registered_owner_id=owner_id if random.random() < 0.3 else None  # 30% chance registered
    )
def generate_social_posts(motive: str, days_range: int = 30) -> List[str]:
    """Generate realistic social media posts that may hint at motive or activity."""
    posts = []
    
    # Generate posts that might relate to the crime
    if "Financial" in motive or "Greed" in motive or "Debt" in motive:
        posts.extend([
            "Need money ASAP. Anyone know quick work?",
            "Broke af but gotta keep grinding",
            "When you need cash but jobs don't pay enough",
            "Desperate times call for desperate measures",
            "Can't pay rent this month. FML."
        ])
    
    if "Revenge" in motive or "Retaliation" in motive:
        posts.extend([
            "Some people gonna get what's coming to them",
            "Don't cross me. I don't forget.",
            "Karma's a bitch and so am I",
            "You think you can mess with me? Think again."
        ])
    
    if "Drug" in motive or "Addiction" in motive:
        posts.extend([
            "Need to score tonight",
            "Anyone got the hookup?",
            "Running low on supplies",
            "This lifestyle ain't cheap"
        ])
    
    # Add some generic posts to mix in
    generic_posts = [
        "Just another day in paradise",
        "Can't wait for the weekend",
        "Working late again",
        "Who's up?",
        "Nothing to see here",
        "Living my best life",
        "You know what I mean?",
        "That's how it goes sometimes"
    ]
    
    # Generate 5-12 posts over the time range
    num_posts = random.randint(5, 12)
    for _ in range(num_posts):
        if random.random() < 0.4 and posts:  # 40% chance of crime-related post
            posts.append(random.choice([p for p in posts if p]))
        else:
            posts.append(random.choice(generic_posts))
    
    # Add timestamps (simplified - just relative days)
    dated_posts = []
    for i, post in enumerate(posts[:num_posts]):
        days_ago = random.randint(0, days_range)
        dated_posts.append(f"[{days_ago} days ago] {post}")
    
    return dated_posts[:num_posts]
def generate_911_script(crime_type: str, address: str, caller_role: str = "Witness") -> List[Tuple[str, str]]:
    """Generate realistic 911 call transcript with detailed conversation."""
    call_time = datetime.now()

    # Base script with realistic dialogue
    script = [
        ("Caller", "911? I need help!"),
        ("Dispatch", "911, what's your emergency?"),
    ]

    if caller_role == "Victim":
        if crime_type == "Burglary":
            script.extend([
                ("Caller", f"I'm at {address}. Someone just broke into my house!"),
                ("Dispatch", f"Okay, stay calm. Are you safe right now? Can you describe what happened?"),
                ("Caller", "I was in the kitchen when I heard glass breaking. I think they're still in the house! I can hear them moving around upstairs."),
                ("Dispatch", "Alright, stay on the line with me. Police are on the way. Can you get to a safe room?"),
                ("Caller", "No, I... I think I hear footsteps coming down the stairs. Oh god, they're coming this way!"),
                ("Dispatch", "Stay calm. Help is coming. What's your name?"),
                ("Caller", "Cynthia Hernandez. Please hurry! I think they're in the living room now."),
                ("Dispatch", "Okay Cynthia, police are en route. ETA 3-4 minutes. Can you tell me if you see anyone?"),
                ("Caller", "I... I think I see a shadow moving. They're wearing dark clothes, hoodie pulled up. Male, I think. Medium build."),
                ("Dispatch", "Good, that's helpful. Stay quiet if you can. Officers are pulling up now."),
                ("Caller", "[Background: doorbell ringing, muffled voices] They're here! Police are here!"),
                ("Dispatch", "Good. Stay on the line until officers make contact. You did great."),
            ])
        elif crime_type == "Assault":
            script.extend([
                ("Caller", f"Help! I've been attacked at {address}!"),
                ("Dispatch", "Are you injured? What's your condition?"),
                ("Caller", "My face hurts, I think my nose is broken. He hit me and ran off."),
                ("Dispatch", "Okay, help is coming. Can you describe the attacker?"),
                ("Caller", "White male, 6 feet tall, wearing a black hoodie. He had tattoos on his hands."),
                ("Dispatch", "Did you know this person?"),
                ("Caller", "No, he came up from behind. I was walking home from work."),
                ("Dispatch", "Alright, stay where you are. Officers are responding."),
            ])

    elif caller_role == "Witness":
        if crime_type == "Burglary":
            script.extend([
                ("Caller", f"I just saw someone breaking into the house at {address}!"),
                ("Dispatch", "Can you describe what you saw?"),
                ("Caller", "I was walking my dog when I heard glass breaking. I looked over and saw a guy in a hoodie smashing a window with a crowbar."),
                ("Dispatch", "Which direction did they go? Are they still there?"),
                ("Caller", "They went around the back. I think they're still inside - I can see lights moving around."),
                ("Dispatch", "Don't approach the house. Police are on the way. What's your name and location?"),
                ("Caller", "I'm Scott Lewis, I'm across the street. The house belongs to Cynthia Hernandez - she's out of town."),
                ("Dispatch", "Okay Scott, stay where you are. Officers will want to talk to you."),
            ])

    # Add call metadata
    script.insert(0, ("SYSTEM", f"Call received: {call_time.strftime('%Y-%m-%d %H:%M:%S')}"))
    script.insert(1, ("SYSTEM", f"ANI: {fake.phone_number()}"))
    script.append(("SYSTEM", f"Call duration: {random.randint(45, 180)} seconds"))
    script.append(("SYSTEM", "Transferred to responding unit"))

    return script
def generate_motive(crime_type: str) -> str:
    """Generate realistic crime motivation based on crime type."""
    motives = {
        "Burglary": ["Financial desperation", "Drug addiction", "Greed", "Revenge", "Opportunistic theft"],
        "Assault": ["Revenge", "Domestic dispute", "Road rage", "Alcohol-fueled", "Gang-related"],
        "Robbery": ["Financial desperation", "Drug addiction", "Greed", "Gang initiation", "Debt collection"],
        "Homicide": ["Domestic violence", "Gang retaliation", "Robbery gone wrong", "Revenge", "Jealousy"],
        "Theft": ["Financial desperation", "Opportunistic", "Greed", "Drug addiction", "Peer pressure"],
        "Fraud": ["Greed", "Financial desperation", "Lifestyle maintenance", "Gambling debt", "Business failure"],
        "Drug Possession": ["Addiction", "Distribution", "Peer pressure", "Financial gain"],
        "Domestic Violence": ["Control", "Jealousy", "Alcohol-fueled", "History of abuse", "Power dynamic"],
        "Stalking": ["Obsession", "Rejection", "Control", "Jealousy", "Mental illness"],
        "Arson": ["Insurance fraud", "Revenge", "Mental illness", "Gang activity", "Covering evidence"]
    }
    return random.choice(motives.get(crime_type, ["Unknown", "Financial gain", "Revenge"]))
def generate_vehicle(owner_id: str, owner_address: str) -> Vehicle:
    makes_models = [
        ("Ford", "F-150"), ("Chevrolet", "Silverado"), ("Toyota", "Camry"),
        ("Honda", "Civic"), ("Nissan", "Altima"), ("BMW", "3 Series"),
        ("Mercedes-Benz", "C-Class"), ("Audi", "A4"), ("Jeep", "Wrangler"),
        ("Ford", "Explorer"), ("Chevrolet", "Tahoe"), ("GMC", "Sierra")
    ]
    make, model = random.choice(makes_models)
    colors = ["Black", "White", "Silver", "Gray", "Blue", "Red", "Green", "Brown"]

    return Vehicle(
        id=fake.uuid4(),
        make=make,
        model=model,
        color=random.choice(colors),
        year=random.randint(2015, 2024),
        license_plate=fake.license_plate(),
        vin=fake.vin(),
        owner_id=owner_id,
        registered_address=owner_address
    )
def generate_date_near(target_date: datetime, days_range: int = 2, before: bool = True) -> datetime: return target_date
def generate_file_hash(algorithm="sha256") -> str:
    """Generate realistic file hash."""
    if algorithm == "md5":
        return fake.md5()
    elif algorithm == "sha256":
        return fake.sha256()
    else:
        return fake.hexify(text="^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", upper=False)

def generate_ip() -> str:
    """Generate realistic IP address."""
    return fake.ipv4()
def generate_device(owner_id: str = None, type_force: str = None) -> DigitalDevice:
    """Generate a realistic digital device with all metadata."""
    device_type = type_force or random.choice(["Phone", "Laptop", "Tablet", "Desktop"])
    
    if device_type == "Phone":
        makes_models = [
            ("Apple", "iPhone 13"), ("Apple", "iPhone 12"), ("Samsung", "Galaxy S21"),
            ("Samsung", "Galaxy Note 20"), ("Google", "Pixel 6"), ("OnePlus", "9 Pro")
        ]
        make, model = random.choice(makes_models)
        phone_number = fake.phone_number()
        imei = fake.random_number(digits=15, fix_len=True)
    else:
        makes_models = [
            ("Apple", "MacBook Pro"), ("Dell", "XPS 15"), ("HP", "Spectre"),
            ("Lenovo", "ThinkPad"), ("Microsoft", "Surface Pro")
        ]
        make, model = random.choice(makes_models)
        phone_number = None
        imei = None
    
    mac = ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
    ip = generate_ip()
    
    return DigitalDevice(
        type=device_type,
        make=make,
        mac_address=mac,
        ip_address=ip,
        imei=imei,
        phone_number=phone_number,
        owner_id=owner_id
    )
def generate_interrogation_dialogue(archetype: str, crime_type: str) -> List[Tuple[str, str]]:
    """Generate interrogation dialogue based on personality archetype."""
    dialogues = {
        "Aggressive": [
            ("Q: Where were you on the night of the incident?", "A: What business is it of yours? I don't have to tell you anything."),
            ("Q: Did you have anything to do with this?", "A: You're wasting my time. Let me go or get me a lawyer."),
            ("Q: Tell us what happened.", "A: I already told you, I don't know anything!")
        ],
        "Deceptive": [
            ("Q: Can you account for your whereabouts?", "A: I was at home watching TV, like I always do."),
            ("Q: Did you see anything suspicious?", "A: No, everything seemed normal to me."),
            ("Q: Are you telling us the truth?", "A: Of course I am. Why would I lie to you?")
        ],
        "Paranoid": [
            ("Q: What can you tell us about what happened?", "A: I don't trust you people. What's this really about?"),
            ("Q: Did you notice anyone acting strangely?", "A: Everyone's acting strange. Are you watching me?"),
            ("Q: Just answer the question.", "A: I can't be too careful. People are out to get me.")
        ],
        "Calculating": [
            ("Q: Walk us through what you remember.", "A: I need to think about this carefully. Let me get my facts straight."),
            ("Q: What were you doing at the time?", "A: I was exactly where I said I was. I have an alibi."),
            ("Q: Are you sure about that?", "A: Absolutely certain. I plan everything meticulously.")
        ],
        "Impulsive": [
            ("Q: Tell us what you know.", "A: Look, I don't know much, but I heard some stuff..."),
            ("Q: Did you see the suspect?", "A: Maybe? I think so? I'm not really sure."),
            ("Q: Take your time and think.", "A: I don't have time for this! Just tell me what you want to know!")
        ]
    }

    # Default to neutral if archetype not found
    return dialogues.get(archetype, [
        ("Q: What can you tell us?", "A: I'm not sure what you mean."),
        ("Q: Did you witness anything?", "A: I don't recall seeing anything unusual."),
        ("Q: Is there anything else?", "A: I think that's all I know.")
    ])
def generate_username(first: str, last: str) -> str: return "user"
def generate_chat_thread(p1: str, p2: str, crime_context: str = "general", length: int = 4) -> List[Tuple[str, str]]: return [("A", "B")]
def generate_phishing_log(target_email: str, date: datetime) -> str: return "--- PHISHING ---"
def generate_pi_report(investigator_name: str, subject_name: str, date: datetime) -> str: return "--- PI REPORT ---"
def generate_dark_web_post(username: str, item_type: str, date: datetime) -> str: return "--- DARK WEB ---"
def generate_witsec_profile(witness: Person) -> str: return "--- WITSEC ---"
def generate_ci_contract(ci_name: str, handler_name: str) -> str: return "--- CI CONTRACT ---"
def generate_network_map(suspects: List[Person]) -> str: return "--- NETWORK ---"
