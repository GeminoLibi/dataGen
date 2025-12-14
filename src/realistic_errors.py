"""
Realistic Error and Event Generation System

Simulates human errors, mishandling, and catastrophic events that occur
during case generation to create more realistic, messy case files.
"""

import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum


class ErrorSeverity(Enum):
    """Severity levels for errors and events."""
    MINOR = "Minor"  # Typos, formatting issues
    MODERATE = "Moderate"  # Missing pages, partial corruption
    MAJOR = "Major"  # Lost evidence, corrupted files
    CATASTROPHIC = "Catastrophic"  # Entire documents lost, evidence destroyed


class EventType(Enum):
    """Types of realistic events that can occur."""
    DOCUMENT_ERROR = "Document Error"
    EVIDENCE_MISHANDLING = "Evidence Mishandling"
    SYSTEM_FAILURE = "System Failure"
    HUMAN_ERROR = "Human Error"
    ENVIRONMENTAL = "Environmental"
    CORRUPTION = "Data Corruption"


# ========== ERROR PROBABILITY TABLES ==========

# Base probabilities for different event types (per document/evidence item)
EVENT_PROBABILITIES = {
    EventType.DOCUMENT_ERROR: {
        ErrorSeverity.MINOR: 0.15,      # 15% chance of minor errors
        ErrorSeverity.MODERATE: 0.05,    # 5% chance of moderate errors
        ErrorSeverity.MAJOR: 0.01,       # 1% chance of major errors
        ErrorSeverity.CATASTROPHIC: 0.001  # 0.1% chance of catastrophic
    },
    EventType.EVIDENCE_MISHANDLING: {
        ErrorSeverity.MINOR: 0.08,       # 8% chance
        ErrorSeverity.MODERATE: 0.03,     # 3% chance
        ErrorSeverity.MAJOR: 0.005,       # 0.5% chance
        ErrorSeverity.CATASTROPHIC: 0.0005  # 0.05% chance
    },
    EventType.SYSTEM_FAILURE: {
        ErrorSeverity.MINOR: 0.02,       # 2% chance
        ErrorSeverity.MODERATE: 0.01,     # 1% chance
        ErrorSeverity.MAJOR: 0.002,       # 0.2% chance
        ErrorSeverity.CATASTROPHIC: 0.0002  # 0.02% chance
    },
    EventType.HUMAN_ERROR: {
        ErrorSeverity.MINOR: 0.12,       # 12% chance
        ErrorSeverity.MODERATE: 0.04,    # 4% chance
        ErrorSeverity.MAJOR: 0.008,       # 0.8% chance
        ErrorSeverity.CATASTROPHIC: 0.0008  # 0.08% chance
    },
    EventType.ENVIRONMENTAL: {
        ErrorSeverity.MINOR: 0.01,       # 1% chance
        ErrorSeverity.MODERATE: 0.005,    # 0.5% chance
        ErrorSeverity.MAJOR: 0.001,       # 0.1% chance
        ErrorSeverity.CATASTROPHIC: 0.0001  # 0.01% chance
    },
    EventType.CORRUPTION: {
        ErrorSeverity.MINOR: 0.005,      # 0.5% chance
        ErrorSeverity.MODERATE: 0.002,    # 0.2% chance
        ErrorSeverity.MAJOR: 0.0005,     # 0.05% chance
        ErrorSeverity.CATASTROPHIC: 0.0001  # 0.01% chance
    }
}

# Time-based probability modifiers (events more likely at certain times)
TIME_MODIFIERS = {
    "immediate": 1.0,      # During initial incident
    "hours_after": 1.2,    # 1-6 hours after (chaos period)
    "days_after": 0.8,     # 1-3 days after
    "weeks_after": 0.5,    # 1-4 weeks after
    "months_after": 0.3    # 1+ months after
}

# Complexity modifiers (higher complexity = more errors)
COMPLEXITY_MODIFIERS = {
    "Low": 0.7,      # 30% fewer errors
    "Medium": 1.0,   # Baseline
    "High": 1.5      # 50% more errors
}


# ========== ERROR TEMPLATES ==========

DOCUMENT_ERRORS = {
    ErrorSeverity.MINOR: [
        "Typo in date: {date} should be {correct_date}",
        "Missing page number on page {page}",
        "Inconsistent formatting in section {section}",
        "Spelling error: '{word}' should be '{correct_word}'",
        "Duplicate entry on line {line}",
        "Incorrect badge number: {badge} (should be {correct_badge})",
        "Missing punctuation in witness statement",
        "Illegible handwriting in margin notes",
        "Coffee stain obscuring partial text",
        "Crossed-out text with correction written above"
    ],
    ErrorSeverity.MODERATE: [
        "Pages {start}-{end} missing from document",
        "Partial water damage - approximately 30% of document illegible",
        "Scan quality poor - text recognition errors in {section}",
        "Document misfiled - found in wrong case folder",
        "Redacted section {section} - original text partially visible",
        "Photocopy quality degraded - some text unreadable",
        "Document timestamp incorrect - actual date {actual_date}",
        "Missing signature on page {page}",
        "Duplicate document with conflicting information",
        "Document partially torn - missing corner section"
    ],
    ErrorSeverity.MAJOR: [
        "CRITICAL: Document {doc_id} lost during transfer - last seen {date}",
        "Approximately 50% of document illegible after {event}",
        "Document corrupted - unable to recover {section}",
        "Evidence chain of custody broken - document location unknown",
        "Document destroyed in {event} - backup unavailable",
        "Entire section {section} missing - suspected misfiling",
        "Document partially destroyed - only {percentage}% recoverable",
        "CRITICAL ERROR: Wrong case number assigned - document belongs to {other_case}",
        "Document damaged beyond repair - attempting reconstruction",
        "Multiple pages out of order - original sequence unknown"
    ],
    ErrorSeverity.CATASTROPHIC: [
        "CATASTROPHIC: Entire document lost - no backup available",
        "CRITICAL: Document completely destroyed in {event}",
        "CATASTROPHIC: Evidence chain broken - document never recovered",
        "CRITICAL ERROR: Document permanently lost - last backup {date}",
        "CATASTROPHIC: Document corrupted beyond recovery - {percentage}% lost",
        "CRITICAL: Document destroyed in fire/flood - no recovery possible",
        "CATASTROPHIC: Entire case file section lost - {items} items missing",
        "CRITICAL ERROR: Document shredded by mistake - reconstruction impossible"
    ]
}

EVIDENCE_ERRORS = {
    ErrorSeverity.MINOR: [
        "Evidence tag partially torn - ID number unclear",
        "Evidence bag seal broken - contents verified intact",
        "Minor contamination during collection",
        "Evidence location logged incorrectly - corrected to {location}",
        "Evidence photo out of focus - retake required",
        "Evidence tag missing date - estimated from context",
        "Evidence bag label smudged - ID partially illegible"
    ],
    ErrorSeverity.MODERATE: [
        "Evidence {evidence_id} temporarily misplaced - located {days} days later",
        "Evidence chain of custody gap - {hours} hours unaccounted",
        "Evidence bag damaged - contents partially exposed",
        "Evidence photo missing - attempting to locate",
        "Evidence tag lost - ID reconstructed from records",
        "Evidence stored in wrong location - relocated after {days} days",
        "Evidence partially contaminated - {percentage}% compromised"
    ],
    ErrorSeverity.MAJOR: [
        "CRITICAL: Evidence {evidence_id} lost - last seen {date}",
        "Evidence chain of custody broken - evidence location unknown",
        "Evidence {evidence_id} destroyed in {event}",
        "CRITICAL ERROR: Evidence misplaced - located {days} days later, integrity questionable",
        "Evidence bag compromised - contents contaminated",
        "Evidence {evidence_id} lost during transfer - never recovered",
        "CRITICAL: Evidence stored incorrectly - degradation suspected",
        "Evidence chain broken - {hours} hours unaccounted, integrity compromised"
    ],
    ErrorSeverity.CATASTROPHIC: [
        "CATASTROPHIC: Evidence {evidence_id} permanently lost - no recovery possible",
        "CRITICAL: Evidence destroyed in {event} - case impact severe",
        "CATASTROPHIC: Evidence chain completely broken - evidence never recovered",
        "CRITICAL ERROR: Evidence {evidence_id} destroyed beyond recovery",
        "CATASTROPHIC: Multiple evidence items lost - {count} items missing",
        "CRITICAL: Evidence permanently lost - case compromised"
    ]
}

SYSTEM_ERRORS = {
    ErrorSeverity.MINOR: [
        "System backup delayed - last backup {hours} hours ago",
        "Temporary network outage during upload",
        "File sync error - manual intervention required",
        "Database query timeout - retry successful"
    ],
    ErrorSeverity.MODERATE: [
        "System crash during document generation - partial data loss",
        "Database corruption detected - recovery in progress",
        "File server outage - {hours} hours of data potentially lost",
        "Backup system failure - last successful backup {days} days ago",
        "Network partition - some documents not synced"
    ],
    ErrorSeverity.MAJOR: [
        "CRITICAL: System failure - {percentage}% of data lost",
        "Database corruption - {items} records unrecoverable",
        "File server crash - {hours} hours of work lost",
        "CRITICAL ERROR: Backup system failure - no backups for {days} days",
        "System compromise suspected - data integrity verification required"
    ],
    ErrorSeverity.CATASTROPHIC: [
        "CATASTROPHIC: Complete system failure - data recovery impossible",
        "CRITICAL: Ransomware attack - {percentage}% of data encrypted",
        "CATASTROPHIC: Data center failure - {items} cases affected",
        "CRITICAL ERROR: Complete data loss - no backups available"
    ]
}

ENVIRONMENTAL_EVENTS = {
    ErrorSeverity.MINOR: [
        "Power outage - documents saved before shutdown",
        "Water leak in storage area - documents moved safely",
        "Temperature fluctuation - some documents slightly damaged"
    ],
    ErrorSeverity.MODERATE: [
        "Flood damage - approximately {percentage}% of documents affected",
        "Fire suppression system activated - water damage to documents",
        "HVAC failure - documents exposed to extreme conditions",
        "Water pipe burst - {items} documents damaged"
    ],
    ErrorSeverity.MAJOR: [
        "CRITICAL: Fire damage - {percentage}% of documents destroyed",
        "Flood damage - {items} documents lost",
        "CRITICAL: Structural damage - documents inaccessible",
        "Environmental disaster - {percentage}% of case files affected"
    ],
    ErrorSeverity.CATASTROPHIC: [
        "CATASTROPHIC: Fire destroyed entire storage area - {items} cases lost",
        "CRITICAL: Flood destroyed evidence storage - recovery impossible",
        "CATASTROPHIC: Natural disaster - entire case file destroyed"
    ]
}


# ========== EVENT TIMING LOGIC ==========

def get_time_category(incident_date: datetime, current_date: datetime) -> str:
    """Determine time category for probability modifier."""
    delta = current_date - incident_date
    
    if delta.total_seconds() < 3600:  # Less than 1 hour
        return "immediate"
    elif delta.total_seconds() < 21600:  # Less than 6 hours
        return "hours_after"
    elif delta.days < 3:
        return "days_after"
    elif delta.days < 28:
        return "weeks_after"
    else:
        return "months_after"


def roll_for_event(event_type: EventType, severity: ErrorSeverity, 
                   incident_date: datetime, current_date: datetime,
                   complexity: str = "Medium") -> bool:
    """
    Roll for a specific event based on probability tables.
    
    Returns True if event occurs, False otherwise.
    """
    base_prob = EVENT_PROBABILITIES[event_type][severity]
    time_cat = get_time_category(incident_date, current_date)
    time_mod = TIME_MODIFIERS.get(time_cat, 1.0)
    complexity_mod = COMPLEXITY_MODIFIERS.get(complexity, 1.0)
    
    final_prob = base_prob * time_mod * complexity_mod
    
    return random.random() < final_prob


def generate_error_message(event_type: EventType, severity: ErrorSeverity,
                          context: Dict = None) -> str:
    """Generate a realistic error message based on event type and severity."""
    context = context or {}
    
    if event_type == EventType.DOCUMENT_ERROR:
        templates = DOCUMENT_ERRORS[severity]
    elif event_type == EventType.EVIDENCE_MISHANDLING:
        templates = EVIDENCE_ERRORS[severity]
    elif event_type == EventType.SYSTEM_FAILURE:
        templates = SYSTEM_ERRORS[severity]
    elif event_type == EventType.ENVIRONMENTAL:
        templates = ENVIRONMENTAL_EVENTS[severity]
    else:
        templates = DOCUMENT_ERRORS[severity]  # Default fallback
    
    template = random.choice(templates)
    
    # Fill in template variables
    try:
        return template.format(**context)
    except KeyError:
        # If context missing, use template as-is or with defaults
        defaults = {
            'date': 'unknown',
            'page': random.randint(1, 10),
            'section': 'unknown',
            'word': 'unknown',
            'badge': 'unknown',
            'line': random.randint(1, 50),
            'percentage': random.randint(20, 80),
            'items': random.randint(1, 10),
            'hours': random.randint(1, 24),
            'days': random.randint(1, 7),
            'event': random.choice(['accident', 'incident', 'system failure', 'human error']),
            'evidence_id': f"EVID-{random.randint(1000, 9999)}",
            'doc_id': f"DOC-{random.randint(1000, 9999)}",
            'other_case': f"CASE-{random.randint(100000, 999999)}",
            'location': 'unknown',
            'count': random.randint(2, 5)
        }
        defaults.update(context)
        return template.format(**defaults)


class RealisticErrorGenerator:
    """Generates realistic errors and events during case generation."""
    
    def __init__(self, incident_date: datetime, complexity: str = "Medium"):
        self.incident_date = incident_date
        self.complexity = complexity
        self.events_log: List[Dict] = []
        self.affected_items: Dict[str, List[str]] = {
            'documents': [],
            'evidence': [],
            'persons': []
        }
    
    def check_document_error(self, doc_id: str, doc_type: str, 
                            current_date: datetime) -> Optional[str]:
        """
        Check if a document error occurs.
        Returns error message if error occurs, None otherwise.
        """
        # Roll for different severity levels (most likely to least)
        for severity in [ErrorSeverity.MINOR, ErrorSeverity.MODERATE, 
                         ErrorSeverity.MAJOR, ErrorSeverity.CATASTROPHIC]:
            if roll_for_event(EventType.DOCUMENT_ERROR, severity, 
                            self.incident_date, current_date, self.complexity):
                context = {
                    'doc_id': doc_id,
                    'doc_type': doc_type,
                    'date': current_date.strftime('%Y-%m-%d'),
                    'page': random.randint(1, 20),
                    'section': random.choice(['Section A', 'Section B', 'Narrative', 'Evidence']),
                    'percentage': random.randint(20, 80),
                    'event': random.choice(['accident', 'system crash', 'water damage', 'fire'])
                }
                error_msg = generate_error_message(
                    EventType.DOCUMENT_ERROR, severity, context
                )
                self.events_log.append({
                    'type': EventType.DOCUMENT_ERROR,
                    'severity': severity,
                    'item': doc_id,
                    'message': error_msg,
                    'timestamp': current_date
                })
                self.affected_items['documents'].append(doc_id)
                return error_msg
        return None
    
    def check_evidence_error(self, evidence_id: str, evidence_type: str,
                            current_date: datetime) -> Optional[str]:
        """
        Check if an evidence mishandling error occurs.
        Returns error message if error occurs, None otherwise.
        """
        for severity in [ErrorSeverity.MINOR, ErrorSeverity.MODERATE,
                         ErrorSeverity.MAJOR, ErrorSeverity.CATASTROPHIC]:
            if roll_for_event(EventType.EVIDENCE_MISHANDLING, severity,
                            self.incident_date, current_date, self.complexity):
                context = {
                    'evidence_id': evidence_id,
                    'evidence_type': evidence_type,
                    'date': current_date.strftime('%Y-%m-%d'),
                    'days': random.randint(1, 14),
                    'hours': random.randint(1, 48),
                    'percentage': random.randint(10, 50),
                    'event': random.choice(['accident', 'mishandling', 'storage error', 'transfer error']),
                    'location': 'unknown',
                    'count': random.randint(2, 5)
                }
                error_msg = generate_error_message(
                    EventType.EVIDENCE_MISHANDLING, severity, context
                )
                self.events_log.append({
                    'type': EventType.EVIDENCE_MISHANDLING,
                    'severity': severity,
                    'item': evidence_id,
                    'message': error_msg,
                    'timestamp': current_date
                })
                self.affected_items['evidence'].append(evidence_id)
                return error_msg
        return None
    
    def check_system_error(self, current_date: datetime) -> Optional[str]:
        """Check if a system error occurs."""
        for severity in [ErrorSeverity.MINOR, ErrorSeverity.MODERATE,
                         ErrorSeverity.MAJOR, ErrorSeverity.CATASTROPHIC]:
            if roll_for_event(EventType.SYSTEM_FAILURE, severity,
                            self.incident_date, current_date, self.complexity):
                context = {
                    'hours': random.randint(1, 72),
                    'days': random.randint(1, 7),
                    'percentage': random.randint(10, 90),
                    'items': random.randint(1, 50)
                }
                error_msg = generate_error_message(
                    EventType.SYSTEM_FAILURE, severity, context
                )
                self.events_log.append({
                    'type': EventType.SYSTEM_FAILURE,
                    'severity': severity,
                    'message': error_msg,
                    'timestamp': current_date
                })
                return error_msg
        return None
    
    def check_environmental_event(self, current_date: datetime) -> Optional[str]:
        """Check if an environmental event occurs."""
        for severity in [ErrorSeverity.MINOR, ErrorSeverity.MODERATE,
                         ErrorSeverity.MAJOR, ErrorSeverity.CATASTROPHIC]:
            if roll_for_event(EventType.ENVIRONMENTAL, severity,
                            self.incident_date, current_date, self.complexity):
                context = {
                    'percentage': random.randint(20, 80),
                    'items': random.randint(1, 20),
                    'event': random.choice(['fire', 'flood', 'water leak', 'power outage'])
                }
                error_msg = generate_error_message(
                    EventType.ENVIRONMENTAL, severity, context
                )
                self.events_log.append({
                    'type': EventType.ENVIRONMENTAL,
                    'severity': severity,
                    'message': error_msg,
                    'timestamp': current_date
                })
                return error_msg
        return None
    
    def apply_error_to_document(self, document: str, error_msg: str, 
                                severity: ErrorSeverity) -> str:
        """
        Apply error effects to a document string.
        Modifies the document based on error severity.
        """
        if severity == ErrorSeverity.MINOR:
            # Add typos, formatting issues
            lines = document.split('\n')
            if lines and random.random() < 0.3:
                # Add a typo
                line_idx = random.randint(0, min(10, len(lines) - 1))
                lines[line_idx] = lines[line_idx].replace('the', 'teh', 1)
            return '\n'.join(lines)
        
        elif severity == ErrorSeverity.MODERATE:
            # Remove sections, add corruption markers
            lines = document.split('\n')
            if len(lines) > 20:
                # Remove random section
                start = random.randint(5, len(lines) - 10)
                end = start + random.randint(3, 8)
                lines.insert(start, f"\n[NOTE: {error_msg}]\n")
                lines.insert(start + 1, "[SECTION PARTIALLY ILLEGIBLE]")
            return '\n'.join(lines)
        
        elif severity == ErrorSeverity.MAJOR:
            # Significant corruption
            lines = document.split('\n')
            if len(lines) > 10:
                # Mark large sections as corrupted
                start = random.randint(2, len(lines) - 5)
                end = min(start + len(lines) // 3, len(lines))
                lines.insert(start, f"\n[CRITICAL ERROR: {error_msg}]\n")
                lines.insert(start + 1, "[APPROXIMATELY 50% OF FOLLOWING SECTION ILLEGIBLE]")
            return '\n'.join(lines)
        
        elif severity == ErrorSeverity.CATASTROPHIC:
            # Document mostly lost
            return f"[CATASTROPHIC ERROR: {error_msg}]\n\n[ORIGINAL DOCUMENT LOST - RECONSTRUCTION ATTEMPT]\n\n{document[:len(document)//4]}...[REMAINDER LOST]"
        
        return document
    
    def get_events_summary(self) -> str:
        """Generate a summary of all events that occurred."""
        if not self.events_log:
            return ""
        
        summary = "\n=== REALISTIC ERRORS AND EVENTS LOG ===\n\n"
        for event in self.events_log:
            summary += f"[{event['timestamp'].strftime('%Y-%m-%d %H:%M')}] "
            summary += f"{event['severity'].value} {event['type'].value}: "
            summary += f"{event['message']}\n"
        
        return summary

