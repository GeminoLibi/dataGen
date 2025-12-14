"""
Multi-Format Document Generation System

Generates documents in various formats (PDF, DOCX, XLSX, images, audio transcripts, etc.)
to create more realistic case files with diverse file types.
"""

import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from faker import Faker

fake = Faker()


class FileFormat(Enum):
    """Supported file formats."""
    TXT = "txt"
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    XLSX = "xlsx"
    XLS = "xls"
    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"
    MP3 = "mp3"
    WAV = "wav"
    MP4 = "mp4"
    MOV = "mov"
    AVI = "avi"
    M4A = "m4a"
    MPEG = "mpeg"


# Format probabilities based on document type
FORMAT_PROBABILITIES = {
    "incident_report": {
        FileFormat.PDF: 0.6,
        FileFormat.DOCX: 0.3,
        FileFormat.TXT: 0.1
    },
    "memo": {
        FileFormat.DOCX: 0.7,
        FileFormat.DOC: 0.2,
        FileFormat.TXT: 0.1
    },
    "spreadsheet": {
        FileFormat.XLSX: 0.8,
        FileFormat.XLS: 0.15,
        FileFormat.TXT: 0.05  # CSV as text
    },
    "photo": {
        FileFormat.JPEG: 0.7,
        FileFormat.PNG: 0.25,
        FileFormat.GIF: 0.05
    },
    "audio": {
        FileFormat.MP3: 0.5,
        FileFormat.WAV: 0.3,
        FileFormat.M4A: 0.2
    },
    "video": {
        FileFormat.MP4: 0.6,
        FileFormat.MOV: 0.25,
        FileFormat.AVI: 0.1,
        FileFormat.MPEG: 0.05
    }
}


def generate_ransom_note() -> str:
    """Generate a realistic ransom note with handwritten characteristics."""
    # Common ransom note phrases
    phrases = [
        "We have {victim}. Do not contact police.",
        "If you want {victim} back alive, follow instructions exactly.",
        "We are watching. Do not try to find us.",
        "Place {amount} in unmarked bills.",
        "Wait for further instructions.",
        "Tell no one or {victim} dies.",
        "We know everything about you.",
        "Do not involve authorities.",
        "You have {hours} hours.",
        "Check {location} for instructions."
    ]
    
    # Generate note
    note_parts = []
    note_parts.append("RANSOM NOTE")
    note_parts.append("=" * 50)
    note_parts.append("")
    
    # Add random phrases
    num_phrases = random.randint(3, 6)
    selected_phrases = random.sample(phrases, num_phrases)
    
    for phrase in selected_phrases:
        # Add handwritten characteristics
        text = phrase.format(
            victim=random.choice(["him", "her", "them", "the package"]),
            amount=f"${random.randint(10000, 500000)}",
            hours=random.randint(24, 72),
            location=random.choice(["the park", "the bridge", "the drop point", "location A"])
        )
        
        # Add handwritten-style variations
        if random.random() < 0.3:
            text = text.upper()  # Sometimes all caps
        if random.random() < 0.2:
            text = text.lower()  # Sometimes all lowercase
        if random.random() < 0.4:
            # Add random capitalization
            words = text.split()
            text = ' '.join([w.capitalize() if random.random() < 0.3 else w for w in words])
        
        # Add spacing irregularities (handwritten characteristic)
        if random.random() < 0.3:
            text = text.replace(' ', '  ')  # Double spaces
        
        note_parts.append(text)
    
    note_parts.append("")
    note_parts.append("=" * 50)
    note_parts.append(f"[Note recovered: {datetime.now().strftime('%Y-%m-%d')}]")
    note_parts.append("[Handwriting analysis pending]")
    note_parts.append("[Forensic examination: Paper type, ink analysis, fingerprints]")
    
    return "\n".join(note_parts)


def generate_image_ocr_extraction(image_type: str, context: Dict = None) -> str:
    """
    Generate OCR text extraction from images - actual useful content.
    Extracts text, license plates, addresses, etc. that would be found in images.
    """
    context = context or {}
    
    extracted_text = []
    extracted_text.append(f"--- OCR TEXT EXTRACTION ---")
    extracted_text.append(f"File: {context.get('filename', 'image_001.jpg')}")
    extracted_text.append(f"Format: {context.get('format', 'JPEG')}")
    extracted_text.append(f"Date: {context.get('date', datetime.now().strftime('%Y-%m-%d'))}")
    extracted_text.append("")
    extracted_text.append("EXTRACTED TEXT:")
    extracted_text.append("-" * 50)
    
    if image_type == "cctv_still" or image_type == "license_plate":
        # Extract license plate
        if random.random() < 0.7:  # 70% chance of readable plate
            plate = f"{random.randint(1, 9)}{random.choice(['ABC', 'DEF', 'GHI', 'JKL', 'MNO'])}{random.randint(100, 999)}"
            confidence = random.randint(85, 99)
            extracted_text.append(f"License Plate: {plate} (Confidence: {confidence}%)")
            extracted_text.append("")
        
        # Extract signage
        if random.random() < 0.5:
            signs = [
                f"STOP",
                f"SPEED LIMIT {random.randint(15, 55)}",
                f"{fake.street_name()} STREET",
                f"NO PARKING",
                f"{fake.company()} - {fake.city()}"
            ]
            extracted_text.append(f"Signage: {random.choice(signs)}")
            extracted_text.append("")
    
    elif image_type == "evidence_photo":
        # Extract serial numbers, text from evidence
        if random.random() < 0.6:
            serials = [
                f"SN: {random.randint(100000, 999999)}",
                f"Model: {random.choice(['ABC123', 'XYZ789', 'DEF456'])}",
                f"ID: {fake.uuid4()[:8].upper()}",
                f"Barcode: {random.randint(1000000000000, 9999999999999)}"
            ]
            extracted_text.append(f"Evidence Markings: {random.choice(serials)}")
            extracted_text.append("")
        
        # Extract handwritten notes
        if random.random() < 0.3:
            notes = [
                f"Found at {fake.address()}",
                f"Collected by {fake.name()}",
                f"Time: {random.randint(1, 12)}:{random.randint(0, 59):02d} {random.choice(['AM', 'PM'])}",
                f"Case #{random.randint(100000, 999999)}"
            ]
            extracted_text.append(f"Handwritten Text: {random.choice(notes)}")
            extracted_text.append("")
    
    elif image_type == "document_photo":
        # Extract text from photographed documents
        if random.random() < 0.8:
            doc_text = [
                f"Name: {fake.name()}",
                f"Address: {fake.address()}",
                f"Phone: {fake.phone_number()}",
                f"Date: {fake.date()}",
                f"Amount: ${random.randint(100, 10000)}",
                f"Account: ****{random.randint(1000, 9999)}"
            ]
            num_lines = random.randint(2, 5)
            for _ in range(num_lines):
                extracted_text.append(random.choice(doc_text))
            extracted_text.append("")
    
    # Add OCR confidence notes
    extracted_text.append("-" * 50)
    extracted_text.append(f"OCR Confidence: {random.randint(75, 98)}%")
    extracted_text.append(f"Processing Method: {random.choice(['Tesseract OCR', 'Google Vision API', 'AWS Textract', 'Azure Computer Vision'])}")
    if random.random() < 0.3:
        extracted_text.append(f"Note: Some text partially obscured or low confidence")
    
    return "\n".join(extracted_text)


def generate_audio_transcript(audio_type: str, context: Dict = None) -> str:
    """Generate actual audio transcript content."""
    context = context or {}
    
    if audio_type == "911_call":
        # Generate actual 911 call transcript
        transcript = []
        transcript.append(f"--- 911 CALL TRANSCRIPT ---")
        transcript.append(f"File: {context.get('filename', '911_call_001.wav')}")
        transcript.append(f"Format: {context.get('format', 'WAV')}")
        transcript.append(f"Duration: {random.choice(['00:02:15', '00:03:42', '00:01:58', '00:04:12'])}")
        transcript.append(f"Date: {context.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}")
        transcript.append("")
        transcript.append("TRANSCRIPT:")
        transcript.append("=" * 60)
        
        # Generate dialogue
        dispatcher_phrases = [
            "911, what's your emergency?",
            "Can you tell me what happened?",
            "Where are you located?",
            "Is anyone injured?",
            "Stay on the line, help is on the way.",
            "Can you describe what you see?",
            "Are you safe right now?"
        ]
        
        caller_phrases = [
            "I need help!",
            "There's been an accident!",
            "Someone broke into my house!",
            "I saw something suspicious!",
            "Please hurry!",
            f"I'm at {fake.address()}",
            "I don't know what to do!",
            "They're still here!",
            "I'm scared!"
        ]
        
        # Generate conversation
        num_exchanges = random.randint(4, 8)
        for i in range(num_exchanges):
            if i % 2 == 0:
                transcript.append(f"DISPATCHER: {random.choice(dispatcher_phrases)}")
            else:
                transcript.append(f"CALLER: {random.choice(caller_phrases)}")
        
        transcript.append("=" * 60)
        transcript.append(f"Quality Notes: {random.choice(['Clear audio', 'Some background noise', 'Caller emotional', 'Good quality'])}")
        
        return "\n".join(transcript)
    
    elif audio_type == "wiretap":
        # Generate actual wiretap transcript
        transcript = []
        transcript.append(f"--- WIRETAP TRANSCRIPT ---")
        transcript.append(f"File: {context.get('filename', 'wiretap_001.mp3')}")
        transcript.append(f"Date: {context.get('date', datetime.now().strftime('%Y-%m-%d'))}")
        transcript.append(f"Duration: {random.choice(['00:15:32', '00:22:45', '00:18:12'])}")
        transcript.append("")
        transcript.append("TRANSCRIPT:")
        transcript.append("=" * 60)
        
        # Generate conversation snippets
        speaker1_phrases = [
            f"Meet me at {fake.address()}",
            f"The amount is ${random.randint(1000, 50000)}",
            "Don't say anything over the phone",
            "We'll handle it tonight",
            "Everything is set up",
            "No one can know about this"
        ]
        
        speaker2_phrases = [
            "Understood",
            "I'll be there",
            "What about the other thing?",
            "Are you sure about this?",
            "I don't like this",
            "Fine, whatever you say"
        ]
        
        num_exchanges = random.randint(6, 12)
        for i in range(num_exchanges):
            speaker = "SPEAKER 1" if i % 2 == 0 else "SPEAKER 2"
            phrases = speaker1_phrases if i % 2 == 0 else speaker2_phrases
            transcript.append(f"{speaker}: {random.choice(phrases)}")
        
        transcript.append("=" * 60)
        transcript.append(f"Note: {random.choice(['Multiple speakers identified', 'Background noise present', 'Some portions unclear', 'Good quality recording'])}")
        
        return "\n".join(transcript)
    
    else:
        return f"""--- AUDIO TRANSCRIPT ---
File: {context.get('filename', 'audio_001.wav')}
Format: {context.get('format', 'WAV')}
Duration: {random.choice(['00:05:00', '00:10:00', '00:15:00'])}

[Transcript content unavailable]
"""


def generate_video_transcript(video_type: str, context: Dict = None) -> str:
    """Generate actual video transcript/analysis."""
    context = context or {}
    
    if video_type == "cctv":
        transcript = []
        transcript.append(f"--- CCTV VIDEO ANALYSIS ---")
        transcript.append(f"File: {context.get('filename', 'cctv_001.mp4')}")
        transcript.append(f"Duration: {random.choice(['00:34:15', '01:12:43', '00:45:22'])}")
        transcript.append(f"Date: {context.get('date', datetime.now().strftime('%Y-%m-%d'))}")
        transcript.append("")
        transcript.append("TIMELINE OF EVENTS:")
        transcript.append("=" * 60)
        
        # Generate timeline events
        times = []
        base_time = datetime.strptime(context.get('date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
        for i in range(random.randint(3, 8)):
            minutes = random.randint(0, 59)
            hours = random.randint(8, 22)
            times.append(f"{hours:02d}:{minutes:02d}")
        
        events = [
            "Person enters frame from left",
            "Vehicle stops in parking lot",
            "Subject exits vehicle",
            "Subject approaches building entrance",
            "Subject enters building",
            "Subject exits building",
            "Subject returns to vehicle",
            "Vehicle departs scene",
            "Multiple individuals visible",
            "Suspicious activity observed",
            "Subject loiters near entrance",
            "Subject makes phone call"
        ]
        
        for time in sorted(set(times))[:random.randint(3, 6)]:
            transcript.append(f"{time} - {random.choice(events)}")
        
        transcript.append("")
        transcript.append("KEY OBSERVATIONS:")
        transcript.append("-" * 60)
        observations = [
            f"License plate visible: {random.randint(1, 9)}{random.choice(['ABC', 'DEF', 'GHI'])}{random.randint(100, 999)}",
            f"Subject appears to be {random.choice(['male', 'female'])}, approximately {random.randint(20, 60)} years old",
            f"Vehicle: {random.choice(['Sedan', 'SUV', 'Truck', 'Van'])} - {random.choice(['Black', 'White', 'Silver', 'Blue'])}",
            f"Subject wearing {random.choice(['dark clothing', 'hoodie', 'jacket', 'casual attire'])}",
            f"Duration at location: {random.randint(2, 15)} minutes"
        ]
        
        for obs in random.sample(observations, random.randint(2, 4)):
            transcript.append(f"- {obs}")
        
        transcript.append("=" * 60)
        
        return "\n".join(transcript)
    
    elif video_type == "body_cam":
        transcript = []
        transcript.append(f"--- BODY CAMERA FOOTAGE TRANSCRIPT ---")
        transcript.append(f"File: {context.get('filename', 'bodycam_001.mp4')}")
        transcript.append(f"Officer: {context.get('officer', 'Unknown')}")
        transcript.append(f"Date: {context.get('date', datetime.now().strftime('%Y-%m-%d'))}")
        transcript.append("")
        transcript.append("TRANSCRIPT:")
        transcript.append("=" * 60)
        
        officer_phrases = [
            "This is Officer {name}, responding to call",
            "Show me your hands!",
            "Stay where you are!",
            "Put your hands behind your back",
            "You're under arrest",
            "Do you understand your rights?",
            "What's going on here?",
            "Backup requested"
        ]
        
        subject_phrases = [
            "I didn't do anything!",
            "What's this about?",
            "I have rights!",
            "You can't do this!",
            "I want a lawyer",
            "I'm not resisting",
            "This is a mistake"
        ]
        
        num_exchanges = random.randint(5, 10)
        for i in range(num_exchanges):
            if i % 2 == 0:
                transcript.append(f"OFFICER: {random.choice(officer_phrases).format(name=context.get('officer', 'Unknown').split()[0])}")
            else:
                transcript.append(f"SUBJECT: {random.choice(subject_phrases)}")
        
        transcript.append("=" * 60)
        
        return "\n".join(transcript)
    
    else:
        return f"""--- VIDEO ANALYSIS ---
File: {context.get('filename', 'video_001.mp4')}
[Video analysis unavailable]
"""


def generate_spreadsheet_data(data_type: str, context: Dict = None) -> str:
    """Generate actual spreadsheet/CSV data."""
    context = context or {}
    
    if data_type == "financial":
        # Generate financial transaction data
        data = []
        data.append("--- FINANCIAL RECORDS (CSV DATA) ---")
        data.append(f"File: {context.get('filename', 'financial_data_001.xlsx')}")
        data.append(f"Format: {context.get('format', 'XLSX')}")
        data.append("")
        data.append("Date,Description,Amount,Account,Category,Balance")
        data.append("-" * 80)
        
        # Generate transaction rows
        num_transactions = random.randint(20, 100)
        balance = random.randint(1000, 50000)
        
        for i in range(num_transactions):
            date = (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
            descriptions = [
                f"ATM WITHDRAWAL - {fake.city()}",
                f"PURCHASE - {fake.company()}",
                f"TRANSFER TO {fake.name()}",
                f"DEPOSIT - CHECK #{random.randint(1000, 9999)}",
                f"ONLINE PAYMENT - {fake.company()}",
                f"CASH DEPOSIT",
                f"FEE - {random.choice(['MONTHLY', 'OVERDRAFT', 'WIRE'])}"
            ]
            amount = random.randint(-5000, 3000)
            balance += amount
            account = f"****{random.randint(1000, 9999)}"
            category = random.choice(['ATM', 'PURCHASE', 'TRANSFER', 'DEPOSIT', 'FEE'])
            
            data.append(f"{date},{random.choice(descriptions)},{amount:.2f},{account},{category},{balance:.2f}")
        
        return "\n".join(data)
    
    elif data_type == "evidence_log":
        # Generate evidence log spreadsheet
        data = []
        data.append("--- EVIDENCE LOG (CSV DATA) ---")
        data.append(f"File: {context.get('filename', 'evidence_log_001.xlsx')}")
        data.append("")
        data.append("Evidence ID,Type,Description,Location Found,Date Collected,Collected By,Status,Storage Location")
        data.append("-" * 100)
        
        # Generate evidence rows
        evidence_types = ['Physical', 'Digital', 'Document', 'Biological', 'Firearm', 'Drug', 'Vehicle']
        locations = [fake.address() for _ in range(5)]
        officers = [fake.name() for _ in range(3)]
        statuses = ['In Storage', 'At Lab', 'Returned', 'Destroyed']
        storage = ['Evidence Room A', 'Evidence Room B', 'Lab Storage', 'Secure Vault']
        
        num_items = random.randint(10, 50)
        for i in range(num_items):
            evid_id = f"EVID-{random.randint(1000, 9999)}"
            evid_type = random.choice(evidence_types)
            description = random.choice([
                f"{random.choice(['Item', 'Substance', 'Device', 'Document'])} recovered from scene",
                f"Evidence collected during search",
                f"Item seized from suspect"
            ])
            location = random.choice(locations)
            date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
            officer = random.choice(officers)
            status = random.choice(statuses)
            storage_loc = random.choice(storage)
            
            data.append(f"{evid_id},{evid_type},{description},{location},{date},{officer},{status},{storage_loc}")
        
        return "\n".join(data)
    
    elif data_type == "phone_records":
        # Generate phone call records
        data = []
        data.append("--- PHONE RECORDS (CSV DATA) ---")
        data.append(f"File: {context.get('filename', 'phone_records_001.xlsx')}")
        data.append("")
        data.append("Date,Time,Duration,From Number,To Number,Call Type,Location")
        data.append("-" * 100)
        
        num_calls = random.randint(50, 200)
        for i in range(num_calls):
            date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
            time = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
            duration = random.randint(10, 3600)  # seconds
            from_num = f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"
            to_num = f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"
            call_type = random.choice(['Voice', 'Text', 'Data'])
            location = f"{fake.city()}, {fake.state_abbr()}"
            
            data.append(f"{date},{time},{duration},{from_num},{to_num},{call_type},{location}")
        
        return "\n".join(data)
    
    else:
        return f"""--- SPREADSHEET DATA ---
File: {context.get('filename', 'data_001.xlsx')}
[Data unavailable]
"""


class MultiFormatGenerator:
    """Generates documents in various formats."""
    
    def __init__(self, case_id: str):
        self.case_id = case_id
        self.file_counter = 1
    
    def generate_document(self, doc_type: str, content: str, 
                          preferred_format: Optional[FileFormat] = None) -> Dict:
        """
        Generate a document with format metadata.
        Returns dict with content, format, filename, and metadata.
        """
        # Determine format
        if preferred_format:
            file_format = preferred_format
        elif doc_type in FORMAT_PROBABILITIES:
            formats = list(FORMAT_PROBABILITIES[doc_type].keys())
            weights = list(FORMAT_PROBABILITIES[doc_type].values())
            file_format = random.choices(formats, weights=weights)[0]
        else:
            file_format = FileFormat.TXT
        
        # Generate filename
        filename = self._generate_filename(doc_type, file_format)
        
        # Add format-specific metadata
        metadata = self._generate_metadata(file_format, doc_type)
        
        return {
            'content': content,
            'format': file_format.value,
            'filename': filename,
            'metadata': metadata,
            'doc_type': doc_type
        }
    
    def _generate_filename(self, doc_type: str, file_format: FileFormat) -> str:
        """Generate a realistic filename."""
        prefix_map = {
            'incident_report': 'INCIDENT_REPORT',
            'memo': 'MEMO',
            'spreadsheet': 'DATA',
            'photo': 'PHOTO',
            'audio': 'AUDIO',
            'video': 'VIDEO',
            'ransom_note': 'RANSOM_NOTE'
        }
        
        prefix = prefix_map.get(doc_type, 'DOC')
        return f"{prefix}_{self.file_counter:03d}.{file_format.value}"
    
    def _generate_metadata(self, file_format: FileFormat, doc_type: str) -> Dict:
        """Generate format-specific metadata."""
        metadata = {
            'format': file_format.value,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'case_id': self.case_id
        }
        
        if file_format in [FileFormat.JPEG, FileFormat.PNG, FileFormat.GIF]:
            metadata.update({
                'resolution': random.choice(['1920x1080', '2560x1440', '3840x2160']),
                'color_depth': random.choice(['24-bit', '32-bit']),
                'compression': random.choice(['JPEG', 'PNG', 'Lossless'])
            })
        elif file_format in [FileFormat.MP3, FileFormat.WAV, FileFormat.M4A]:
            metadata.update({
                'duration': f"{random.randint(1, 30)}:{random.randint(0, 59):02d}",
                'bitrate': random.choice(['128 kbps', '192 kbps', '256 kbps', '320 kbps']),
                'sample_rate': random.choice(['44100 Hz', '48000 Hz'])
            })
        elif file_format in [FileFormat.MP4, FileFormat.MOV, FileFormat.AVI]:
            metadata.update({
                'duration': f"{random.randint(5, 60)}:{random.randint(0, 59):02d}",
                'resolution': random.choice(['1280x720', '1920x1080', '3840x2160']),
                'frame_rate': random.choice(['24 fps', '30 fps', '60 fps']),
                'codec': random.choice(['H.264', 'H.265', 'MPEG-4'])
            })
        elif file_format in [FileFormat.XLSX, FileFormat.XLS]:
            metadata.update({
                'sheets': random.randint(1, 5),
                'rows': random.randint(100, 10000),
                'columns': random.randint(5, 20)
            })
        elif file_format == FileFormat.PDF:
            metadata.update({
                'pages': random.randint(1, 50),
                'version': random.choice(['1.4', '1.5', '1.7'])
            })
        
        return metadata
    
    def generate_ransom_note_document(self) -> Dict:
        """Generate a ransom note document."""
        content = generate_ransom_note()
        return self.generate_document('ransom_note', content, FileFormat.TXT)
    
    def generate_image_ocr_document(self, image_type: str, 
                                    context: Dict = None) -> Dict:
        """Generate OCR text extraction from images (only when useful)."""
        context = context or {}
        context['filename'] = self._generate_filename('photo', FileFormat.JPEG)
        # Only generate OCR for images that would have extractable text
        if image_type in ['cctv_still', 'license_plate', 'evidence_photo', 'document_photo']:
            content = generate_image_ocr_extraction(image_type, context)
            return self.generate_document('photo', content, FileFormat.TXT)
        return None  # Skip useless image descriptions
    
    def generate_audio_transcript_document(self, audio_type: str,
                                          context: Dict = None) -> Dict:
        """Generate an audio transcript document."""
        context = context or {}
        context['filename'] = self._generate_filename('audio', FileFormat.WAV)
        content = generate_audio_transcript(audio_type, context)
        return self.generate_document('audio', content, FileFormat.TXT)
    
    def generate_video_transcript_document(self, video_type: str,
                                          context: Dict = None) -> Dict:
        """Generate a video transcript document."""
        context = context or {}
        context['filename'] = self._generate_filename('video', FileFormat.MP4)
        content = generate_video_transcript(video_type, context)
        return self.generate_document('video', content, FileFormat.TXT)
    
    def generate_spreadsheet_data_document(self, data_type: str, context: Dict = None) -> Dict:
        """Generate actual spreadsheet/CSV data."""
        context = context or {}
        context['filename'] = self._generate_filename('spreadsheet', FileFormat.XLSX)
        content = generate_spreadsheet_data(data_type, context)
        return self.generate_document('spreadsheet', content, FileFormat.TXT)

