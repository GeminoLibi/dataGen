"""
Crime-type-specific document generators.
Each crime type has its own investigation flow and document types.
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from faker import Faker

fake = Faker()

class CrimeSpecificGenerator:
    """Generates documents specific to crime types with proper investigation flow."""
    
    def __init__(self, case, crime_type: str, crime_datetime: datetime, entities: Dict):
        self.case = case
        self.crime_type = crime_type
        self.crime_datetime = crime_datetime
        self.entities = entities
        self.investigation_chain = []  # Track investigation steps
        
    def generate_crime_specific_documents(self, complexity: str, modifiers: List[str]) -> List[str]:
        """Generate documents based on crime type with proper investigation flow."""
        documents = []
        
        # Route to crime-specific generator
        crime_lower = self.crime_type.lower()
        if "fraud" in crime_lower or "scam" in crime_lower or "phone" in crime_lower:
            documents.extend(self._generate_phone_scam_investigation(complexity, modifiers))
        elif "cybercrime" in crime_lower or "cyber" in crime_lower:
            documents.extend(self._generate_cybercrime_investigation(complexity, modifiers))
        elif "financial" in crime_lower and "fraud" not in crime_lower:
            documents.extend(self._generate_financial_crime_investigation(complexity, modifiers))
        elif "homicide" in crime_lower or "murder" in crime_lower:
            documents.extend(self._generate_homicide_investigation(complexity, modifiers))
        elif "assault" in crime_lower:
            documents.extend(self._generate_assault_investigation(complexity, modifiers))
        elif "burglary" in crime_lower or "theft" in crime_lower:
            documents.extend(self._generate_burglary_investigation(complexity, modifiers))
        elif "robbery" in crime_lower:
            documents.extend(self._generate_robbery_investigation(complexity, modifiers))
        else:
            # Default physical crime investigation
            documents.extend(self._generate_standard_physical_investigation(complexity, modifiers))
        
        return documents
    
    def _generate_phone_scam_investigation(self, complexity: str, modifiers: List[str]) -> List[str]:
        """Generate phone scam investigation with proper flow."""
        from .models import Role
        docs = []
        suspects = [p for p in self.case.persons if p.role == Role.SUSPECT]
        victims = [p for p in self.case.persons if p.role == Role.VICTIM]
        
        if not victims:
            return docs
        
        victim = victims[0]
        suspect = suspects[0] if suspects else None
        
        # Step 1: Initial Victim Report
        doc1 = f"""--- INITIAL VICTIM REPORT ---
CASE NUMBER: {self.case.id}
DATE/TIME: {self.crime_datetime.strftime('%Y-%m-%d %H:%M:%S')}
REPORTING OFFICER: {fake.name()}
BADGE #: {fake.random_number(digits=4)}

VICTIM INFORMATION:
Name: {victim.full_name}
DOB: {victim.date_of_birth.strftime('%Y-%m-%d') if hasattr(victim, 'date_of_birth') else fake.date_of_birth().strftime('%Y-%m-%d')}
Phone: {victim.phone_number}
Address: {victim.address}

INCIDENT SUMMARY:
On {self.crime_datetime.strftime('%B %d, %Y at approximately %H:%M')}, victim {victim.full_name} received a phone call from number {fake.phone_number()}. 
The caller identified themselves as {random.choice(['IRS agent', 'Microsoft support', 'Social Security Administration', 'Amazon customer service', 'Bank fraud department'])} 
and informed the victim that {random.choice(['their account was compromised', 'they owed back taxes', 'their computer was infected', 'their Social Security number was suspended', 'there was suspicious activity on their account'])}.

The caller instructed the victim to {random.choice(['provide their Social Security number', 'purchase gift cards and provide the codes', 'wire money to a specified account', 'download remote access software', 'provide bank account information'])} 
to resolve the issue. The victim complied and {random.choice(['provided personal information', 'purchased $500 in gift cards', 'wired $2,000', 'allowed remote access to their computer', 'provided bank account details'])}.

The victim realized they had been scammed when {random.choice(['the caller demanded more money', 'they contacted the actual organization', 'they noticed unauthorized transactions', 'the caller became aggressive', 'they researched the phone number online'])}.

INVESTIGATIVE ACTIONS TAKEN:
- Victim statement obtained
- Phone number documented: {fake.phone_number()}
- Website/email provided by suspect documented
- Financial transaction records requested
- Case assigned to Financial Crimes Unit

NEXT STEPS:
- Obtain phone records for victim's number
- Trace suspect phone number (likely VoIP/burner)
- Investigate any websites or email addresses provided
- Review financial transaction records
"""
        docs.append(doc1)
        self.investigation_chain.append(("Initial Report", "Victim statement obtained"))
        
        # Step 2: Phone Records Investigation (if phone data modifier)
        if "Phone data pull" in modifiers or "Data-Heavy Phone Dump" in modifiers:
            suspect_phone = fake.phone_number()
            doc2 = f"""--- PHONE RECORDS INVESTIGATION REPORT ---
CASE NUMBER: {self.case.id}
DATE: {(self.crime_datetime + timedelta(days=2)).strftime('%Y-%m-%d')}
INVESTIGATOR: Detective {fake.last_name()}
UNIT: Financial Crimes Unit

SUBJECT PHONE NUMBER: {suspect_phone}
CARRIER: {random.choice(['VoIP Provider A', 'VoIP Provider B', 'Burner Phone Service', 'Prepaid Carrier'])}
ACCOUNT TYPE: {random.choice(['Prepaid/VoIP', 'Burner phone', 'Virtual number', 'Disposable number'])}
REGISTRATION: {random.choice(['Anonymous registration', 'Fake identity', 'Stolen identity', 'No registration data available'])}

CALL LOG ANALYSIS:
Phone number {suspect_phone} was identified as the number used to contact victim {victim.full_name} on {self.crime_datetime.strftime('%Y-%m-%d')} at {self.crime_datetime.strftime('%H:%M')}.

SUBSEQUENT INVESTIGATION:
Tracing of this number revealed it is a VoIP/burner phone with minimal registration data. However, call pattern analysis identified {random.randint(3, 8)} other phone numbers that show similar calling patterns and were used to contact other potential victims during the same time period.

ASSOCIATED PHONE NUMBERS IDENTIFIED:
"""
            for i in range(random.randint(3, 8)):
                doc2 += f"- {fake.phone_number()} (Contacted {random.randint(1, 15)} numbers on {self.crime_datetime.strftime('%Y-%m-%d')})\n"
            
            doc2 += f"""
INVESTIGATIVE CONCLUSION:
The suspect phone number is part of a larger scam operation. Multiple burner/VoIP numbers are being used to contact victims. 
Pattern analysis suggests the same individual or group is operating multiple numbers.

NEXT STEPS:
- Obtain records for associated phone numbers
- Cross-reference with other scam reports
- Investigate VoIP provider for account information
- Check for website or email addresses associated with these numbers
"""
            docs.append(doc2)
            self.investigation_chain.append(("Phone Records", f"Identified {random.randint(3, 8)} associated numbers"))
        
        # Step 3: Website/DNS Investigation (if DNS modifier)
        if "DNS records" in modifiers or "IP logs" in modifiers:
            website = fake.domain_name()
            doc3 = f"""--- DNS AND WEBSITE INVESTIGATION REPORT ---
CASE NUMBER: {self.case.id}
DATE: {(self.crime_datetime + timedelta(days=3)).strftime('%Y-%m-%d')}
INVESTIGATOR: Detective {fake.last_name()}
UNIT: Cyber Crimes Unit

WEBSITE/EMAIL INVESTIGATION:
During the scam call, the suspect directed the victim to visit website: {website}
Additionally, the suspect provided email address: {fake.email()}

DNS RECORDS ANALYSIS:
Domain: {website}
Registrar: {fake.company()}
Registration Date: {(self.crime_datetime - timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d')}
Registrant: {random.choice(['Privacy Protection Service', 'Anonymous Registration', 'Fake Identity', 'Stolen Identity'])}
WHOIS Data: Minimal/Privacy Protected

IP ADDRESSES ASSOCIATED WITH DOMAIN:
"""
            ips = []
            for i in range(random.randint(2, 5)):
                ip = fake.ipv4()
                ips.append(ip)
                doc3 += f"- {ip} (Active from {(self.crime_datetime - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')} to {self.crime_datetime.strftime('%Y-%m-%d')})\n"
            
            doc3 += f"""
IP LOG ANALYSIS:
One of the identified IP addresses ({ips[0]}) was traced to a residential internet service provider account.
Subsequent investigation of this IP address revealed usage logs showing connection patterns consistent with scam operations.

RESIDENTIAL IP IDENTIFIED: {ips[0]}
ISP: {fake.company()} Internet Services
ACCOUNT HOLDER: {fake.name()} (Possible suspect or compromised account)
LOCATION: {fake.address()}

USAGE LOG ANALYSIS:
Analysis of connection logs for IP {ips[0]} shows:
- Multiple connections to the scam website {website}
- Connections to VoIP services used for scam calls
- Pattern of activity during scam call times
- {random.randint(50, 200)} connections to various scam-related domains

INVESTIGATIVE CONCLUSION:
The residential IP address {ips[0]} is likely associated with the suspect or a compromised account being used for scam operations.
The connection logs provide evidence linking the suspect to the scam website and VoIP services.

NEXT STEPS:
- Obtain subscriber information for IP {ips[0]} from ISP
- Request search warrant for residence associated with IP
- Cross-reference with phone number investigation
- Coordinate with local jurisdiction for suspect identification
"""
            docs.append(doc3)
            self.investigation_chain.append(("DNS/IP Investigation", f"Identified residential IP: {ips[0]}"))
        
        # Step 4: Follow-up Investigation Report
        doc4 = f"""--- FOLLOW-UP INVESTIGATION REPORT ---
CASE NUMBER: {self.case.id}
DATE: {(self.crime_datetime + timedelta(days=5)).strftime('%Y-%m-%d')}
INVESTIGATOR: Detective {fake.last_name()}
UNIT: Financial Crimes Unit

INVESTIGATION SUMMARY:
This case involves a phone scam operation targeting victims through {random.choice(['IRS impersonation', 'tech support fraud', 'Social Security scam', 'bank fraud alert', 'Amazon refund scam'])}.

INVESTIGATION CHAIN:
"""
        for step, detail in self.investigation_chain:
            doc4 += f"- {step}: {detail}\n"
        
        doc4 += f"""
CURRENT STATUS:
- Victim statement obtained and documented
- Phone records analysis completed
- DNS and IP investigation completed
- Residential IP address identified
- Subscriber information requested from ISP
- Search warrant application in progress

SUSPECT INFORMATION:
At this time, suspect identity is {random.choice(['unknown', 'partially identified', 'under investigation'])}.
The investigation has identified technical indicators linking the scam operation to specific IP addresses and phone numbers.

RECOMMENDED ACTIONS:
- Execute search warrant for residence associated with IP address
- Interview account holder/subscriber
- Seize digital devices for forensic analysis
- Continue monitoring associated phone numbers
- Coordinate with other jurisdictions for similar cases
"""
        docs.append(doc4)
        
        return docs
    
    def _generate_cybercrime_investigation(self, complexity: str, modifiers: List[str]) -> List[str]:
        """Generate cybercrime investigation documents."""
        # This is already handled well, but we can enhance it
        return []
    
    def _generate_financial_crime_investigation(self, complexity: str, modifiers: List[str]) -> List[str]:
        """Generate financial crime investigation documents."""
        return []
    
    def _generate_homicide_investigation(self, complexity: str, modifiers: List[str]) -> List[str]:
        """Generate homicide investigation with physical evidence focus."""
        docs = []
        # Homicide should have: scene investigation, autopsy, ballistics, DNA, witness interviews
        # NOT phone scam documents
        return docs
    
    def _generate_assault_investigation(self, complexity: str, modifiers: List[str]) -> List[str]:
        """Generate assault investigation documents."""
        return []
    
    def _generate_burglary_investigation(self, complexity: str, modifiers: List[str]) -> List[str]:
        """Generate burglary investigation with physical evidence."""
        docs = []
        # Burglary should have: scene investigation, fingerprints, tool marks, CCTV, NOT phone scam docs
        return docs
    
    def _generate_robbery_investigation(self, complexity: str, modifiers: List[str]) -> List[str]:
        """Generate robbery investigation documents."""
        return []
    
    def _generate_standard_physical_investigation(self, complexity: str, modifiers: List[str]) -> List[str]:
        """Generate standard physical crime investigation."""
        return []

