"""
Case Analysis Module - Generates MOD-IN (Modification/Input) documents
for comprehensive case analysis including trends, subjects, and investigative summaries.
"""

from typing import List, Dict, Optional, Set, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

from .models import Case, Person, Role, Evidence, EvidenceType
from faker import Faker

fake = Faker()


class TrendAnalyzer:
    """Analyzes trends across multiple cases."""
    
    def __init__(self, cases: List[Case]):
        """
        Initialize trend analyzer.
        
        Args:
            cases: List of Case objects to analyze for trends
        """
        self.cases = cases
    
    def identify_trends(self) -> Dict[str, List[Dict]]:
        """
        Identify trends across cases.
        
        Returns:
            Dictionary with trend categories and associated cases
        """
        trends = {
            "shared_subjects": [],
            "shared_locations": [],
            "shared_vehicles": [],
            "shared_phone_numbers": [],
            "shared_emails": [],
            "similar_crime_types": [],
            "temporal_patterns": []
        }
        
        # Collect all entities
        all_subjects = {}  # name -> [cases]
        all_locations = {}  # location -> [cases]
        all_vehicles = {}  # license_plate -> [cases]
        all_phones = {}  # phone -> [cases]
        all_emails = {}  # email -> [cases]
        crime_types = defaultdict(list)  # crime_type -> [cases]
        
        for case in self.cases:
            # Subjects
            for person in case.persons:
                if person.role == Role.SUSPECT:
                    if person.full_name not in all_subjects:
                        all_subjects[person.full_name] = []
                    all_subjects[person.full_name].append(case.id)
            
            # Locations
            if case.incident_report:
                loc = case.incident_report.incident_location
                if loc not in all_locations:
                    all_locations[loc] = []
                all_locations[loc].append(case.id)
            
            # Vehicles
            for person in case.persons:
                for vehicle in person.vehicles:
                    if vehicle.license_plate not in all_vehicles:
                        all_vehicles[vehicle.license_plate] = []
                    all_vehicles[vehicle.license_plate].append(case.id)
            
            # Phone numbers
            for person in case.persons:
                if person.phone_number:
                    if person.phone_number not in all_phones:
                        all_phones[person.phone_number] = []
                    all_phones[person.phone_number].append(case.id)
            
            # Emails
            for person in case.persons:
                if person.email:
                    if person.email not in all_emails:
                        all_emails[person.email] = []
                    all_emails[person.email].append(case.id)
            
            # Crime types
            crime_types[case.crime_type].append(case.id)
        
        # Identify trends (appears in 2+ cases)
        for name, case_ids in all_subjects.items():
            if len(case_ids) > 1:
                trends["shared_subjects"].append({
                    "subject": name,
                    "cases": case_ids,
                    "count": len(case_ids)
                })
        
        for loc, case_ids in all_locations.items():
            if len(case_ids) > 1:
                trends["shared_locations"].append({
                    "location": loc,
                    "cases": case_ids,
                    "count": len(case_ids)
                })
        
        for plate, case_ids in all_vehicles.items():
            if len(case_ids) > 1:
                trends["shared_vehicles"].append({
                    "vehicle": plate,
                    "cases": case_ids,
                    "count": len(case_ids)
                })
        
        for phone, case_ids in all_phones.items():
            if len(case_ids) > 1:
                trends["shared_phone_numbers"].append({
                    "phone": phone,
                    "cases": case_ids,
                    "count": len(case_ids)
                })
        
        for email, case_ids in all_emails.items():
            if len(case_ids) > 1:
                trends["shared_emails"].append({
                    "email": email,
                    "cases": case_ids,
                    "count": len(case_ids)
                })
        
        # Similar crime types
        for crime_type, case_ids in crime_types.items():
            if len(case_ids) > 1:
                trends["similar_crime_types"].append({
                    "crime_type": crime_type,
                    "cases": case_ids,
                    "count": len(case_ids)
                })
        
        return trends
    
    def generate_trend_report(self) -> str:
        """Generate a trend analysis report."""
        trends = self.identify_trends()
        
        report = []
        report.append("=" * 80)
        report.append("TREND ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        report.append(f"**Analysis Date:** {datetime.now().strftime('%B %d, %Y')}")
        report.append(f"**Cases Analyzed:** {len(self.cases)}")
        report.append("")
        
        # Shared Subjects
        if trends["shared_subjects"]:
            report.append("# SHARED SUBJECTS")
            report.append("")
            for trend in trends["shared_subjects"]:
                report.append(f"**Subject:** {trend['subject']}")
                report.append(f"**Appears in Cases:** {', '.join(trend['cases'])} ({trend['count']} cases)")
                report.append("")
        
        # Shared Locations
        if trends["shared_locations"]:
            report.append("# SHARED LOCATIONS")
            report.append("")
            for trend in trends["shared_locations"]:
                report.append(f"**Location:** {trend['location']}")
                report.append(f"**Appears in Cases:** {', '.join(trend['cases'])} ({trend['count']} cases)")
                report.append("")
        
        # Shared Vehicles
        if trends["shared_vehicles"]:
            report.append("# SHARED VEHICLES")
            report.append("")
            for trend in trends["shared_vehicles"]:
                report.append(f"**Vehicle (License Plate):** {trend['vehicle']}")
                report.append(f"**Appears in Cases:** {', '.join(trend['cases'])} ({trend['count']} cases)")
                report.append("")
        
        # Shared Phone Numbers
        if trends["shared_phone_numbers"]:
            report.append("# SHARED PHONE NUMBERS")
            report.append("")
            for trend in trends["shared_phone_numbers"]:
                report.append(f"**Phone Number:** {trend['phone']}")
                report.append(f"**Appears in Cases:** {', '.join(trend['cases'])} ({trend['count']} cases)")
                report.append("")
        
        # Similar Crime Types
        if trends["similar_crime_types"]:
            report.append("# SIMILAR CRIME TYPES")
            report.append("")
            for trend in trends["similar_crime_types"]:
                report.append(f"**Crime Type:** {trend['crime_type']}")
                report.append(f"**Cases:** {', '.join(trend['cases'])} ({trend['count']} cases)")
                report.append("")
        
        if not any(trends.values()):
            report.append("No significant trends identified across the analyzed cases.")
            report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)


class CaseAnalyzer:
    """Analyzes generated cases and produces comprehensive MOD-IN reports."""
    
    def __init__(self, case: Case, detective_name: Optional[str] = None, badge_number: Optional[int] = None):
        """
        Initialize case analyzer.
        
        Args:
            case: The Case object to analyze
            detective_name: Name of detective preparing the report
            badge_number: Badge number of detective
        """
        self.case = case
        self.detective_name = detective_name or f"Detective {fake.last_name()}"
        self.badge_number = badge_number or fake.random_number(digits=4)
        self.analysis_date = datetime.now()
    
    def generate_mod_in(self) -> str:
        """Generate a comprehensive MOD-IN case analysis document."""
        doc = []
        
        # Header
        doc.append("=" * 80)
        doc.append("MOD-IN: CASE ANALYSIS REPORT")
        doc.append("=" * 80)
        doc.append("")
        
        # Overview Section
        doc.append("# OVERVIEW")
        doc.append("")
        doc.append(f"**Case Number:** {self.case.id}")
        doc.append(f"**Detective:** {self.detective_name}")
        doc.append(f"**Badge Number:** #{self.badge_number}")
        doc.append(f"**Date of Analysis:** {self.analysis_date.strftime('%B %d, %Y')}")
        doc.append(f"**Crime Type:** {self.case.crime_type}")
        doc.append(f"**Complexity:** {self.case.complexity}")
        doc.append(f"**Status:** {self.case.status}")
        doc.append(f"**Date Opened:** {self.case.date_opened.strftime('%B %d, %Y')}")
        if self.case.incident_report:
            doc.append(f"**Incident Date:** {self.case.incident_report.incident_date.strftime('%B %d, %Y at %H:%M')}")
        doc.append("")
        
        # Executive Summary
        doc.append("# EXECUTIVE SUMMARY")
        doc.append("")
        doc.append(self._generate_executive_summary())
        doc.append("")
        
        # Case Overview
        doc.append("# CASE OVERVIEW")
        doc.append("")
        doc.append(self._generate_case_overview())
        doc.append("")
        
        # Subjects of Investigation
        doc.append("# SUBJECTS OF INVESTIGATION")
        doc.append("")
        doc.append(self._generate_subjects_section())
        doc.append("")
        
        # Attachments and Physical Evidence
        doc.append("# ATTACHMENTS AND PHYSICAL EVIDENCE")
        doc.append("")
        doc.append(self._generate_evidence_section())
        doc.append("")
        
        # Timeline
        doc.append("# TIMELINE")
        doc.append("")
        doc.append(self._generate_timeline())
        doc.append("")
        
        # Investigative Activities Summary
        doc.append("# INVESTIGATIVE ACTIVITIES SUMMARY")
        doc.append("")
        doc.append(self._generate_investigative_activities())
        doc.append("")
        
        # Recommended Next Steps
        doc.append("# RECOMMENDED NEXT STEPS")
        doc.append("")
        doc.append(self._generate_next_steps())
        doc.append("")
        
        # Working Theory
        doc.append("# WORKING THEORY")
        doc.append("")
        doc.append(self._generate_working_theory())
        doc.append("")
        
        # Footer
        doc.append("=" * 80)
        doc.append(f"Report Prepared By: {self.detective_name}, Badge #{self.badge_number}")
        doc.append(f"Date: {self.analysis_date.strftime('%B %d, %Y at %H:%M')}")
        doc.append("=" * 80)
        
        return "\n".join(doc)
    
    def _generate_executive_summary(self) -> str:
        """Generate executive summary of the case."""
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        victims = [p for p in self.case.persons if p.role == Role.VICTIM]
        
        summary = f"I conducted a comprehensive analysis of {self.case.id}, a {self.case.complexity.lower()}-complexity "
        summary += f"{self.case.crime_type.lower()} investigation. "
        
        if self.case.incident_report:
            incident_date = self.case.incident_report.incident_date.strftime('%B %d, %Y')
            location = self.case.incident_report.incident_location
            summary += f"The incident occurred on {incident_date} at {location}. "
        
        if suspects:
            summary += f"I identified {len(suspects)} subject(s) of investigation: "
            summary += ", ".join([s.full_name for s in suspects]) + ". "
        
        if victims:
            summary += f"The case involves {len(victims)} victim(s): "
            summary += ", ".join([v.full_name for v in victims]) + ". "
        
        summary += f"I collected and reviewed {len(self.case.evidence)} evidence items and {len(self.case.documents)} "
        summary += "investigative documents. "
        
        # Key findings
        key_evidence = [e for e in self.case.evidence if e.type in [EvidenceType.FORENSIC, EvidenceType.DIGITAL, EvidenceType.BALLISTIC]]
        if key_evidence:
            summary += f"Key evidence includes {len(key_evidence)} forensic/digital/ballistic items. "
        
        # Status
        if self.case.status == "OPEN":
            summary += "The investigation remains active with multiple leads being pursued."
        else:
            summary += f"The case status is currently {self.case.status}."
        
        return summary
    
    def _generate_case_overview(self) -> str:
        """Generate detailed case overview."""
        overview = []
        
        # Narrative
        if self.case.incident_report and self.case.incident_report.narrative:
            overview.append("## Narrative")
            overview.append("")
            overview.append(self.case.incident_report.narrative)
            overview.append("")
        
        # Crime Details
        overview.append("## Crime Details")
        overview.append("")
        overview.append(f"**Type:** {self.case.crime_type}")
        overview.append(f"**Complexity:** {self.case.complexity}")
        overview.append(f"**Date Opened:** {self.case.date_opened.strftime('%B %d, %Y')}")
        
        if self.case.incident_report:
            overview.append(f"**Incident Date:** {self.case.incident_report.incident_date.strftime('%B %d, %Y at %H:%M')}")
            overview.append(f"**Location:** {self.case.incident_report.incident_location}")
            if self.case.incident_report.latitude and self.case.incident_report.longitude:
                overview.append(f"**Coordinates:** {self.case.incident_report.latitude}, {self.case.incident_report.longitude}")
            if self.case.incident_report.weather_condition:
                overview.append(f"**Weather Conditions:** {self.case.incident_report.weather_condition}")
        
        overview.append("")
        
        # Modifiers
        if self.case.modifiers:
            overview.append("## Investigation Modifiers")
            overview.append("")
            for modifier in self.case.modifiers:
                overview.append(f"- {modifier}")
            overview.append("")
        
        # Reporting Officer
        if self.case.reporting_officer:
            overview.append("## Initial Responding Officer")
            overview.append("")
            overview.append(f"**Officer:** {self.case.reporting_officer.full_name}")
            overview.append(f"**Phone:** {self.case.reporting_officer.phone_number}")
            overview.append("")
        
        return "\n".join(overview)
    
    def _generate_subjects_section(self) -> str:
        """Generate subjects of investigation section."""
        subjects = []
        
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        victims = [p for p in self.case.persons if p.role == Role.VICTIM]
        witnesses = [p for p in self.case.persons if p.role == Role.WITNESS]
        
        # Suspects
        if suspects:
            subjects.append("## Suspects")
            subjects.append("")
            for i, suspect in enumerate(suspects, 1):
                subjects.append(f"### Subject {i}: {suspect.full_name}")
                subjects.append("")
                subjects.append(f"**Age:** {suspect.age}")
                subjects.append(f"**Gender:** {suspect.gender.title() if suspect.gender else 'Unknown'}")
                subjects.append(f"**Address:** {suspect.address}")
                subjects.append(f"**Phone:** {suspect.phone_number}")
                if suspect.email:
                    subjects.append(f"**Email:** {suspect.email}")
                
                # Physical Description
                subjects.append("**Physical Description:**")
                if suspect.height:
                    subjects.append(f"  - Height: {suspect.height}")
                if suspect.weight > 0:
                    subjects.append(f"  - Weight: {suspect.weight} lbs")
                if suspect.build:
                    subjects.append(f"  - Build: {suspect.build}")
                if suspect.hair_color:
                    subjects.append(f"  - Hair Color: {suspect.hair_color.title()}")
                if suspect.eye_color:
                    subjects.append(f"  - Eye Color: {suspect.eye_color.title()}")
                if suspect.facial_hair and suspect.facial_hair != "none":
                    subjects.append(f"  - Facial Hair: {suspect.facial_hair.title()}")
                if not any([suspect.height, suspect.weight, suspect.build, suspect.hair_color, suspect.eye_color]):
                    subjects.append(f"  - {suspect.physical_description}")
                subjects.append("")
                
                # Driver's License
                if suspect.driver_license_number:
                    subjects.append("**Driver's License Information:**")
                    subjects.append(f"  - License Number: {suspect.driver_license_number}")
                    subjects.append(f"  - State: {suspect.driver_license_state}")
                    subjects.append("")
                
                if suspect.motive:
                    subjects.append(f"**Motive:** {suspect.motive}")
                if suspect.criminal_history:
                    subjects.append(f"**Criminal History:** {', '.join(suspect.criminal_history)}")
                if suspect.aliases:
                    subjects.append(f"**Known Aliases:** {', '.join(suspect.aliases)}")
                if suspect.vehicles:
                    vehicle_list = []
                    for v in suspect.vehicles:
                        vehicle_str = f'{v.year} {v.make} {v.model} ({v.license_plate})'
                        # Add owner info if available
                        if v.owner_id:
                            owner = next((p for p in self.case.persons if p.id == v.owner_id), None)
                            if owner:
                                vehicle_str += f" - Registered to: {owner.full_name}"
                        vehicle_list.append(vehicle_str)
                    subjects.append(f"**Vehicles:** {', '.join(vehicle_list)}")
                if suspect.devices:
                    phone_devices = [d for d in suspect.devices if d.phone_number]
                    if phone_devices:
                        subjects.append(f"**Phone Numbers:** {', '.join([d.phone_number for d in phone_devices])}")
                subjects.append("")
        
        # Victims
        if victims:
            subjects.append("## Victims")
            subjects.append("")
            for i, victim in enumerate(victims, 1):
                subjects.append(f"### Victim {i}: {victim.full_name}")
                subjects.append("")
                subjects.append(f"**Age:** {victim.age}")
                subjects.append(f"**Gender:** {victim.gender.title() if victim.gender else 'Unknown'}")
                subjects.append(f"**Address:** {victim.address}")
                subjects.append(f"**Phone:** {victim.phone_number}")
                if victim.email:
                    subjects.append(f"**Email:** {victim.email}")
                
                # Physical Description
                subjects.append("**Physical Description:**")
                if victim.height:
                    subjects.append(f"  - Height: {victim.height}")
                if victim.weight > 0:
                    subjects.append(f"  - Weight: {victim.weight} lbs")
                if victim.build:
                    subjects.append(f"  - Build: {victim.build}")
                if victim.hair_color:
                    subjects.append(f"  - Hair Color: {victim.hair_color.title()}")
                if victim.eye_color:
                    subjects.append(f"  - Eye Color: {victim.eye_color.title()}")
                if victim.facial_hair and victim.facial_hair != "none":
                    subjects.append(f"  - Facial Hair: {victim.facial_hair.title()}")
                if not any([victim.height, victim.weight, victim.build, victim.hair_color, victim.eye_color]):
                    subjects.append(f"  - {victim.physical_description}")
                subjects.append("")
                
                # Driver's License
                if victim.driver_license_number:
                    subjects.append("**Driver's License Information:**")
                    subjects.append(f"  - License Number: {victim.driver_license_number}")
                    subjects.append(f"  - State: {victim.driver_license_state}")
                    subjects.append("")
                
                subjects.append("")
        
        # Witnesses
        if witnesses:
            subjects.append("## Witnesses")
            subjects.append("")
            for i, witness in enumerate(witnesses, 1):
                subjects.append(f"### Witness {i}: {witness.full_name}")
                subjects.append("")
                subjects.append(f"**Age:** {witness.age}")
                subjects.append(f"**Gender:** {witness.gender.title() if witness.gender else 'Unknown'}")
                subjects.append(f"**Address:** {witness.address}")
                subjects.append(f"**Phone:** {witness.phone_number}")
                subjects.append(f"**Reliability Score:** {witness.reliability_score}/100")
                
                # Physical Description (if available)
                if witness.height or witness.weight or witness.build or witness.hair_color or witness.eye_color:
                    subjects.append("**Physical Description:**")
                    if witness.height:
                        subjects.append(f"  - Height: {witness.height}")
                    if witness.weight > 0:
                        subjects.append(f"  - Weight: {witness.weight} lbs")
                    if witness.build:
                        subjects.append(f"  - Build: {witness.build}")
                    if witness.hair_color:
                        subjects.append(f"  - Hair Color: {witness.hair_color.title()}")
                    if witness.eye_color:
                        subjects.append(f"  - Eye Color: {witness.eye_color.title()}")
                    subjects.append("")
                
                subjects.append("")
        
        if not subjects:
            return "No subjects identified at this time."
        
        return "\n".join(subjects)
    
    def _generate_evidence_section(self) -> str:
        """Generate evidence and attachments section."""
        evidence_list = []
        
        if not self.case.evidence:
            return "No physical evidence collected at this time."
        
        # Group by type
        evidence_by_type = defaultdict(list)
        for ev in self.case.evidence:
            evidence_by_type[ev.type.value].append(ev)
        
        for ev_type, items in sorted(evidence_by_type.items()):
            evidence_list.append(f"## {ev_type} Evidence")
            evidence_list.append("")
            
            for i, ev in enumerate(items, 1):
                evidence_list.append(f"### Item {i}: {ev.description}")
                evidence_list.append("")
                evidence_list.append(f"**Evidence ID:** {ev.id}")
                evidence_list.append(f"**Collected By:** {ev.collected_by}")
                evidence_list.append(f"**Collection Date:** {ev.collected_at.strftime('%B %d, %Y at %H:%M')}")
                evidence_list.append(f"**Location Found:** {ev.location_found}")
                
                if ev.chain_of_custody:
                    evidence_list.append("**Chain of Custody:**")
                    for entry in ev.chain_of_custody:
                        evidence_list.append(f"  - {entry}")
                
                if ev.metadata:
                    evidence_list.append("**Metadata:**")
                    for key, value in ev.metadata.items():
                        evidence_list.append(f"  - {key}: {value}")
                
                evidence_list.append("")
        
        # Document attachments
        evidence_list.append("## Document Attachments")
        evidence_list.append("")
        evidence_list.append(f"I reviewed {len(self.case.documents)} investigative documents, including:")
        evidence_list.append("")
        
        # Categorize documents
        doc_categories = {
            "Initial Reports": ["911", "CAD", "INCIDENT_REPORT", "INITIAL_VICTIM_REPORT"],
            "Search Warrants": ["SEARCH_WARRANT", "AFFIDAVIT", "WARRANT_RETURN"],
            "Forensic Reports": ["FINGERPRINT", "BALLISTIC", "DNA", "FORENSIC"],
            "Digital Evidence": ["PHONE", "IP", "DNS", "EMAIL", "BROWSER", "SOCIAL"],
            "Financial Records": ["BANK", "FINANCIAL"],
            "Surveillance": ["CCTV", "ALPR", "EDR", "INFOTAINMENT"],
            "Witness Statements": ["WITNESS", "INTERVIEW"],
            "Other Documents": []
        }
        
        for category, keywords in doc_categories.items():
            matching_docs = []
            for doc in self.case.documents:
                doc_upper = doc.upper()
                if any(keyword in doc_upper for keyword in keywords):
                    matching_docs.append(doc)
                elif category == "Other Documents" and not any(kw in doc_upper for kw in 
                    ["911", "CAD", "INCIDENT", "WARRANT", "FINGERPRINT", "BALLISTIC", "DNA", 
                     "PHONE", "IP", "DNS", "EMAIL", "BANK", "CCTV", "ALPR", "WITNESS"]):
                    matching_docs.append(doc)
            
            if matching_docs:
                evidence_list.append(f"**{category}:** {len(matching_docs)} document(s)")
        
        evidence_list.append("")
        
        return "\n".join(evidence_list)
    
    def _generate_timeline(self) -> str:
        """Generate chronological timeline."""
        timeline = []
        
        if not self.case.incident_report:
            return "Timeline information not available."
        
        incident_date = self.case.incident_report.incident_date
        
        timeline.append("## Key Events")
        timeline.append("")
        
        # Incident
        timeline.append(f"**{incident_date.strftime('%B %d, %Y at %H:%M')}** - Incident occurred")
        timeline.append(f"  - Location: {self.case.incident_report.incident_location}")
        timeline.append(f"  - Type: {self.case.crime_type}")
        timeline.append("")
        
        # Estimated 911 call (typically 0-30 min after)
        estimated_911 = incident_date + timedelta(minutes=15)
        timeline.append(f"**{estimated_911.strftime('%H:%M')}** - 911 call received")
        timeline.append("  - Source: Incident Report, CAD Log")
        timeline.append("")
        
        # Response
        estimated_response = estimated_911 + timedelta(minutes=5)
        timeline.append(f"**{estimated_response.strftime('%H:%M')}** - Officers arrived on scene")
        timeline.append("  - Source: CAD Log")
        timeline.append("")
        
        # Evidence collection
        if self.case.evidence:
            collection_start = min(ev.collected_at for ev in self.case.evidence)
            timeline.append(f"**{collection_start.strftime('%B %d, %Y at %H:%M')}** - Evidence collection initiated")
            timeline.append(f"  - {len(self.case.evidence)} items collected")
        timeline.append("  - Source: Evidence Collection Log")
        timeline.append("")
        
        # Search warrants
        warrant_docs = [d for d in self.case.documents if "SEARCH_WARRANT" in d.upper() and "AFFIDAVIT" in d.upper()]
        if warrant_docs:
            # Estimate warrant time (typically 4-48 hours after incident)
            warrant_time = incident_date + timedelta(hours=12)
            timeline.append(f"**{warrant_time.strftime('%B %d, %Y at %H:%M')}** - Search warrant(s) executed")
            timeline.append(f"  - {len(warrant_docs)} warrant(s) obtained")
            timeline.append("  - Source: Search Warrant Affidavits")
            timeline.append("")
        
        # Case opened
        timeline.append(f"**{self.case.date_opened.strftime('%B %d, %Y')}** - Case file opened")
        timeline.append(f"  - Case ID: {self.case.id}")
        timeline.append("")
        
        return "\n".join(timeline)
    
    def _generate_investigative_activities(self) -> str:
        """Generate summary of investigative activities."""
        activities = []
        
        activities.append("I conducted the following investigative activities:")
        activities.append("")
        
        # Document review
        activities.append("## Document Review")
        activities.append("")
        activities.append(f"I reviewed {len(self.case.documents)} investigative documents, including:")
        activities.append("")
        
        doc_types = {
            "Initial Reports": ["911", "CAD", "INCIDENT_REPORT"],
            "Search Warrants": ["SEARCH_WARRANT", "AFFIDAVIT"],
            "Forensic Analysis": ["FINGERPRINT", "BALLISTIC", "DNA", "FORENSIC"],
            "Digital Forensics": ["PHONE", "IP", "DNS", "EMAIL", "BROWSER"],
            "Financial Investigation": ["BANK", "FINANCIAL"],
            "Surveillance Review": ["CCTV", "ALPR", "EDR"]
        }
        
        for category, keywords in doc_types.items():
            count = sum(1 for doc in self.case.documents 
                       if any(kw in doc.upper() for kw in keywords))
            if count > 0:
                activities.append(f"- {category}: Reviewed {count} document(s)")
        
        activities.append("")
        
        # Evidence collection
        if self.case.evidence:
            activities.append("## Evidence Collection")
            activities.append("")
            activities.append(f"I documented {len(self.case.evidence)} evidence items:")
            activities.append("")
            
            evidence_by_type = defaultdict(int)
            for ev in self.case.evidence:
                evidence_by_type[ev.type.value] += 1
            
            for ev_type, count in sorted(evidence_by_type.items()):
                activities.append(f"- {ev_type}: {count} item(s)")
            
            activities.append("")
        
        # Subject identification
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        if suspects:
            activities.append("## Subject Identification")
            activities.append("")
            activities.append(f"I identified {len(suspects)} subject(s) of investigation:")
            for suspect in suspects:
                activities.append(f"- {suspect.full_name} (Age {suspect.age}, {suspect.address})")
            activities.append("")
        
        # Follow-up actions
        activities.append("## Follow-Up Actions Taken")
        activities.append("")
        
        if any("SEARCH_WARRANT" in d.upper() for d in self.case.documents):
            activities.append("- Executed search warrant(s) at subject location(s)")
        
        if any("PHONE" in d.upper() or "IP" in d.upper() for d in self.case.documents):
            activities.append("- Conducted digital forensics analysis (phone records, IP logs)")
        
        if any("BANK" in d.upper() or "FINANCIAL" in d.upper() for d in self.case.documents):
            activities.append("- Reviewed financial records and transaction history")
        
        if any("CCTV" in d.upper() or "ALPR" in d.upper() for d in self.case.documents):
            activities.append("- Reviewed surveillance footage and ALPR data")
        
        activities.append("")
        
        return "\n".join(activities)
    
    def _generate_next_steps(self) -> str:
        """Generate recommended next steps."""
        steps = []
        
        steps.append("Based on my analysis, I recommend the following investigative actions:")
        steps.append("")
        
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        victims = [p for p in self.case.persons if p.role == Role.VICTIM]
        
        # Subject interviews
        if suspects:
            steps.append("## Subject Interviews")
            steps.append("")
            for suspect in suspects:
                steps.append(f"- Conduct formal interview with {suspect.full_name}")
                steps.append(f"  - Address: {suspect.address}")
                steps.append(f"  - Focus: Establish alibi, motive, and timeline")
            steps.append("")
        
        # Victim follow-up
        if victims:
            steps.append("## Victim Follow-Up")
            steps.append("")
            for victim in victims:
                steps.append(f"- Follow-up interview with {victim.full_name}")
                steps.append(f"  - Obtain detailed statement and timeline")
            steps.append("")
        
        # Evidence analysis
        forensic_evidence = [e for e in self.case.evidence if e.type in [EvidenceType.FORENSIC, EvidenceType.BALLISTIC]]
        if forensic_evidence:
            steps.append("## Forensic Analysis")
            steps.append("")
            steps.append("- Submit physical evidence to crime lab for analysis")
            steps.append("- Request expedited processing for priority items")
            steps.append("")
        
        # Digital forensics
        digital_evidence = [e for e in self.case.evidence if e.type == EvidenceType.DIGITAL]
        if digital_evidence:
            steps.append("## Digital Forensics")
            steps.append("")
            steps.append("- Complete comprehensive digital device analysis")
            steps.append("- Review all phone records, IP logs, and communication data")
            steps.append("- Identify additional associates and communication patterns")
            steps.append("")
        
        # Financial investigation
        if any("BANK" in d.upper() or "FINANCIAL" in d.upper() for d in self.case.documents):
            steps.append("## Financial Investigation")
            steps.append("")
            steps.append("- Subpoena additional financial records if needed")
            steps.append("- Analyze transaction patterns and identify suspicious activity")
            steps.append("")
        
        # Surveillance
        if any("CCTV" in d.upper() or "ALPR" in d.upper() for d in self.case.documents):
            steps.append("## Surveillance Review")
            steps.append("")
            steps.append("- Review all available surveillance footage")
            steps.append("- Identify vehicle movements and subject locations")
            steps.append("")
        
        # Case coordination
        steps.append("## Case Coordination")
        steps.append("")
        steps.append("- Coordinate with prosecutor's office for charging decisions")
        steps.append("- Update case management system with latest findings")
        steps.append("- Schedule case review meeting with supervisor")
        steps.append("")
        
        return "\n".join(steps)
    
    def _generate_working_theory(self) -> str:
        """Generate working theory of the case."""
        theory = []
        
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        victims = [p for p in self.case.persons if p.role == Role.VICTIM]
        
        theory.append("## Current Working Theory")
        theory.append("")
        
        if not suspects:
            theory.append("No subjects have been identified at this time. The investigation is focused on ")
            theory.append("identifying potential suspects through evidence analysis and witness statements.")
            return "\n".join(theory)
        
        # Build theory based on available information
        primary_suspect = suspects[0]
        
        theory.append(f"Based on my review of the evidence and investigative documents, I believe that ")
        theory.append(f"{primary_suspect.full_name} is the primary subject in this {self.case.crime_type.lower()} case. ")
        
        if primary_suspect.motive:
            theory.append(f"The subject's motive appears to be {primary_suspect.motive.lower()}. ")
        
        # Evidence supporting theory
        supporting_evidence = []
        if any("FINGERPRINT" in d.upper() for d in self.case.documents):
            supporting_evidence.append("fingerprint evidence")
        if any("BALLISTIC" in d.upper() for d in self.case.documents):
            supporting_evidence.append("ballistic analysis")
        if any("PHONE" in d.upper() for d in self.case.documents):
            supporting_evidence.append("phone records")
        if any("CCTV" in d.upper() for d in self.case.documents):
            supporting_evidence.append("surveillance footage")
        
        if supporting_evidence:
            theory.append(f"Evidence supporting this theory includes {', '.join(supporting_evidence)}. ")
        
        # Method of operation
        if self.case.incident_report and self.case.incident_report.narrative:
            theory.append("The method of operation suggests ")
            if "weapon" in self.case.incident_report.narrative.lower():
                theory.append("the use of a weapon. ")
            elif "vehicle" in self.case.incident_report.narrative.lower():
                theory.append("involvement of a vehicle. ")
            else:
                theory.append("a calculated approach to the crime. ")
        
        # Additional subjects
        if len(suspects) > 1:
            theory.append(f"Additionally, {len(suspects) - 1} other subject(s) may be involved: ")
            theory.append(", ".join([s.full_name for s in suspects[1:]]) + ". ")
        
        theory.append("")
        theory.append("## Confidence Level")
        theory.append("")
        
        # Determine confidence based on evidence
        evidence_count = len(self.case.evidence)
        doc_count = len(self.case.documents)
        
        if evidence_count > 5 and doc_count > 15:
            confidence = "High"
            theory.append("I have **high confidence** in this working theory based on the volume and quality ")
            theory.append("of evidence collected.")
        elif evidence_count > 2 and doc_count > 10:
            confidence = "Moderate"
            theory.append("I have **moderate confidence** in this working theory. Additional investigation ")
            theory.append("is needed to strengthen the case.")
        else:
            confidence = "Low"
            theory.append("I have **low confidence** in this working theory. The investigation is still ")
            theory.append("in early stages and requires additional evidence collection.")
        
        theory.append("")
        theory.append("## Alternative Theories")
        theory.append("")
        theory.append("I am also considering the following alternative explanations:")
        theory.append("")
        theory.append("- The incident may have involved additional unknown subjects")
        theory.append("- There may be mitigating circumstances not yet discovered")
        theory.append("- The evidence may point to a different sequence of events than initially believed")
        theory.append("")
        
        return "\n".join(theory)


def generate_mod_in_for_case(case: Case, detective_name: Optional[str] = None, 
                             badge_number: Optional[int] = None) -> str:
    """
    Generate a MOD-IN case analysis document for a given case.
    
    Args:
        case: The Case object to analyze
        detective_name: Optional detective name
        badge_number: Optional badge number
    
    Returns:
        Formatted MOD-IN document as string
    """
    analyzer = CaseAnalyzer(case, detective_name, badge_number)
    return analyzer.generate_mod_in()


def generate_trend_analysis(cases: List[Case]) -> str:
    """
    Generate a trend analysis report for multiple cases.
    
    Args:
        cases: List of Case objects to analyze
    
    Returns:
        Formatted trend analysis report as string
    """
    analyzer = TrendAnalyzer(cases)
    return analyzer.generate_trend_report()

