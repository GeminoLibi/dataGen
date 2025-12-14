"""
Multi-Format Document Generation System

Generates documents in various formats (PDF, DOCX, XLSX, images, audio transcripts, etc.)
to create more realistic case files with diverse file types.
"""

import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime
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


def generate_image_description(image_type: str, context: Dict = None) -> str:
    """
    Generate an image description as would be provided by vision AI to an LLM.
    Simulates how vision models describe images.
    """
    context = context or {}
    
    if image_type == "crime_scene":
        return f"""--- IMAGE DESCRIPTION (Vision AI Analysis) ---
File: {context.get('filename', 'crime_scene_photo_001.jpg')}
Format: {context.get('format', 'JPEG')}
Resolution: {random.choice(['1920x1080', '3840x2160', '2560x1440'])}
Date Captured: {context.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))}

VISUAL DESCRIPTION:
- Primary subject: {random.choice(['Crime scene', 'Evidence collection area', 'Victim location'])}
- Lighting conditions: {random.choice(['Well-lit', 'Dim lighting', 'Flash photography', 'Natural daylight'])}
- Image quality: {random.choice(['High resolution', 'Moderate quality', 'Slightly blurred', 'Clear'])}
- Color composition: {random.choice(['Full color', 'Color with flash artifacts', 'Natural colors', 'Slightly overexposed'])}
- Visible objects: {random.choice(['Evidence markers', 'Measuring tape', 'Evidence bags', 'Crime scene tape'])}
- Background: {random.choice(['Residential interior', 'Outdoor location', 'Vehicle interior', 'Commercial building'])}
- Notable features: {random.choice(['Blood spatter visible', 'Footprints in frame', 'Weapon visible', 'Multiple evidence markers'])}
- Perspective: {random.choice(['Overhead view', 'Eye level', 'Low angle', 'Wide angle'])}
- Time indicators: {random.choice(['Daylight visible', 'Night scene', 'Artificial lighting', 'Dusk/dawn'])}
- People visible: {random.choice(['None', '1-2 investigators', 'Multiple personnel', 'Victim only'])}
- Text/numbers visible: {random.choice(['Evidence markers readable', 'License plate partially visible', 'Address numbers visible', 'No readable text'])}
- Distortion/artifacts: {random.choice(['None', 'Minor lens distortion', 'Flash reflection', 'Motion blur in background'])}
- Overall assessment: {random.choice(['Clear documentation of scene', 'Good evidentiary value', 'Adequate for analysis', 'Some detail loss'])}
"""
    
    elif image_type == "cctv_still":
        return f"""--- IMAGE DESCRIPTION (Vision AI Analysis) ---
File: {context.get('filename', 'cctv_frame_001.jpg')}
Format: {context.get('format', 'JPEG')}
Resolution: {random.choice(['640x480', '1280x720', '1920x1080'])}
Timestamp: {context.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}
Camera: {context.get('camera', 'Camera 01 - Main Entrance')}

VISUAL DESCRIPTION:
- Primary subject: {random.choice(['Person walking', 'Vehicle in frame', 'Multiple individuals', 'Empty scene'])}
- Subject position: {random.choice(['Center frame', 'Left side', 'Right side', 'Background'])}
- Subject clarity: {random.choice(['Clear', 'Partially obscured', 'Silhouette', 'Blurred due to motion'])}
- Lighting: {random.choice(['Artificial lighting', 'Low light', 'Daylight', 'Infrared'])}
- Image quality: {random.choice(['Good', 'Moderate', 'Poor', 'Grainy'])}
- Color: {random.choice(['Color', 'Black and white', 'Color with low saturation', 'Infrared monochrome'])}
- Visible details: {random.choice(['Facial features partially visible', 'Clothing clearly visible', 'Vehicle details clear', 'Limited detail'])}
- Background: {random.choice(['Parking lot', 'Street', 'Building entrance', 'Indoor corridor'])}
- Time indicators: {random.choice(['Daytime', 'Night', 'Evening', 'Early morning'])}
- Motion indicators: {random.choice(['Static scene', 'Motion blur present', 'Subject in motion', 'Camera movement'])}
- Text/numbers: {random.choice(['License plate visible', 'Signage readable', 'No readable text', 'Partial text visible'])}
- Distortion: {random.choice(['Minimal', 'Wide angle distortion', 'Compression artifacts', 'Lens flare'])}
- Overall assessment: {random.choice(['Useful for identification', 'Limited identification value', 'Good for context', 'Poor quality'])}
"""
    
    elif image_type == "evidence_photo":
        return f"""--- IMAGE DESCRIPTION (Vision AI Analysis) ---
File: {context.get('filename', 'evidence_photo_001.jpg')}
Format: {context.get('format', 'JPEG')}
Resolution: {random.choice(['2048x1536', '3264x2448', '4032x3024'])}
Evidence ID: {context.get('evidence_id', 'EVID-0001')}
Date: {context.get('date', datetime.now().strftime('%Y-%m-%d'))}

VISUAL DESCRIPTION:
- Evidence type: {context.get('evidence_type', 'Physical evidence')}
- Scale reference: {random.choice(['Ruler visible', 'Evidence marker', 'No scale', 'Multiple reference points'])}
- Lighting: {random.choice(['Studio lighting', 'Flash photography', 'Natural light', 'Controlled lighting'])}
- Background: {random.choice(['White background', 'Evidence table', 'Crime scene', 'Lab setting'])}
- Image quality: {random.choice(['High resolution', 'Excellent detail', 'Good', 'Moderate'])}
- Color accuracy: {random.choice(['Accurate', 'Slightly enhanced', 'Natural', 'Calibrated'])}
- Visible features: {random.choice(['Surface texture clear', 'Damage visible', 'Markings readable', 'Details sharp'])}
- Orientation: {random.choice(['Top view', 'Side view', 'Multiple angles', 'Close-up'])}
- Focus: {random.choice(['Sharp throughout', 'Selective focus', 'Slight blur', 'Perfect focus'])}
- Artifacts: {random.choice(['None', 'Minor reflection', 'Shadow present', 'Clean image'])}
- Overall assessment: {random.choice(['Excellent documentation', 'Good for analysis', 'Adequate', 'High quality'])}
"""
    
    elif image_type == "surveillance":
        return f"""--- IMAGE DESCRIPTION (Vision AI Analysis) ---
File: {context.get('filename', 'surveillance_001.jpg')}
Format: {context.get('format', 'JPEG')}
Resolution: {random.choice(['1280x720', '1920x1080', '2560x1440'])}
Location: {context.get('location', 'Unknown')}
Time: {context.get('time', datetime.now().strftime('%H:%M'))}

VISUAL DESCRIPTION:
- Scene type: {random.choice(['Street scene', 'Building exterior', 'Parking area', 'Public space'])}
- Subject: {random.choice(['Person', 'Vehicle', 'Multiple people', 'Activity'])}
- Distance: {random.choice(['Close-up', 'Medium distance', 'Far', 'Variable'])}
- Clarity: {random.choice(['Clear', 'Moderate', 'Poor', 'Very poor'])}
- Lighting: {random.choice(['Daylight', 'Street lighting', 'Low light', 'Mixed'])}
- Weather: {random.choice(['Clear', 'Overcast', 'Rain', 'Fog'])}
- Visibility: {random.choice(['Good', 'Moderate', 'Poor', 'Limited'])}
- Motion: {random.choice(['Static', 'Motion blur', 'Clear motion', 'Multiple subjects moving'])}
- Identification value: {random.choice(['High', 'Moderate', 'Low', 'Very low'])}
- Overall assessment: {random.choice(['Useful evidence', 'Limited value', 'Context only', 'Poor quality'])}
"""
    
    else:
        return f"""--- IMAGE DESCRIPTION (Vision AI Analysis) ---
File: {context.get('filename', 'image_001.jpg')}
Format: {context.get('format', 'JPEG')}
Resolution: {random.choice(['1920x1080', '2560x1440', '3840x2160'])}

VISUAL DESCRIPTION:
- Image type: {image_type}
- Quality: {random.choice(['High', 'Moderate', 'Low'])}
- Content: {random.choice(['Documentation', 'Evidence', 'Surveillance', 'Reference'])}
- Overall assessment: {random.choice(['Clear', 'Useful', 'Limited detail', 'Adequate'])}
"""


def generate_audio_transcript(audio_type: str, context: Dict = None) -> str:
    """Generate an audio transcript description."""
    context = context or {}
    
    if audio_type == "911_call":
        return f"""--- AUDIO TRANSCRIPT ---
File: {context.get('filename', '911_call_001.wav')}
Format: {context.get('format', 'WAV')}
Duration: {random.choice(['00:02:15', '00:03:42', '00:01:58', '00:04:12'])}
Sample Rate: {random.choice(['8000 Hz', '16000 Hz', '44100 Hz'])}
Bit Depth: {random.choice(['16-bit', '24-bit'])}
Date: {context.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}

AUDIO QUALITY:
- Clarity: {random.choice(['Clear', 'Moderate', 'Poor', 'Very poor'])}
- Background noise: {random.choice(['Minimal', 'Moderate', 'High', 'Very high'])}
- Distortion: {random.choice(['None', 'Minor', 'Moderate', 'Severe'])}
- Volume levels: {random.choice(['Consistent', 'Variable', 'Low', 'High'])}
- Speaker clarity: {random.choice(['Clear', 'Partially clear', 'Unclear', 'Very unclear'])}
- Call quality: {random.choice(['Good', 'Fair', 'Poor', 'Very poor'])}
- Dropouts: {random.choice(['None', 'Minor', 'Several', 'Many'])}
- Overall assessment: {random.choice(['Usable', 'Partially usable', 'Limited value', 'Poor quality'])}
"""
    
    elif audio_type == "wiretap":
        return f"""--- AUDIO TRANSCRIPT ---
File: {context.get('filename', 'wiretap_001.mp3')}
Format: {context.get('format', 'MP3')}
Duration: {random.choice(['00:15:32', '00:22:45', '00:18:12'])}
Bitrate: {random.choice(['128 kbps', '192 kbps', '256 kbps'])}
Date: {context.get('date', datetime.now().strftime('%Y-%m-%d'))}

AUDIO QUALITY:
- Recording quality: {random.choice(['High', 'Moderate', 'Low', 'Very low'])}
- Background noise: {random.choice(['Minimal', 'Moderate', 'High'])}
- Voice clarity: {random.choice(['Clear', 'Partially clear', 'Unclear'])}
- Multiple speakers: {random.choice(['Yes', 'No', 'Uncertain'])}
- Overlapping speech: {random.choice(['None', 'Some', 'Frequent'])}
- Distortion: {random.choice(['None', 'Minor', 'Moderate'])}
- Overall assessment: {random.choice(['Good', 'Fair', 'Poor'])}
"""
    
    else:
        return f"""--- AUDIO TRANSCRIPT ---
File: {context.get('filename', 'audio_001.wav')}
Format: {context.get('format', 'WAV')}
Duration: {random.choice(['00:05:00', '00:10:00', '00:15:00'])}
Quality: {random.choice(['Good', 'Moderate', 'Poor'])}
"""


def generate_video_description(video_type: str, context: Dict = None) -> str:
    """Generate a video description."""
    context = context or {}
    
    if video_type == "cctv":
        return f"""--- VIDEO DESCRIPTION ---
File: {context.get('filename', 'cctv_001.mp4')}
Format: {context.get('format', 'MP4')}
Resolution: {random.choice(['640x480', '1280x720', '1920x1080'])}
Duration: {random.choice(['00:34:15', '01:12:43', '00:45:22'])}
Frame Rate: {random.choice(['15 fps', '30 fps', '25 fps'])}
Codec: {random.choice(['H.264', 'H.265', 'MPEG-4'])}
Date: {context.get('date', datetime.now().strftime('%Y-%m-%d'))}

VIDEO QUALITY:
- Overall quality: {random.choice(['Good', 'Moderate', 'Poor', 'Very poor'])}
- Resolution: {random.choice(['High', 'Medium', 'Low'])}
- Frame rate: {random.choice(['Smooth', 'Slightly choppy', 'Choppy'])}
- Compression: {random.choice(['Minimal', 'Moderate', 'Heavy'])}
- Artifacts: {random.choice(['None', 'Minor', 'Moderate', 'Severe'])}
- Lighting: {random.choice(['Good', 'Moderate', 'Poor', 'Very poor'])}
- Motion blur: {random.choice(['Minimal', 'Moderate', 'High'])}
- Audio: {random.choice(['Present', 'Missing', 'Poor quality'])}
- Overall assessment: {random.choice(['Useful', 'Partially useful', 'Limited value', 'Poor'])}
"""
    
    elif video_type == "body_cam":
        return f"""--- VIDEO DESCRIPTION ---
File: {context.get('filename', 'bodycam_001.mp4')}
Format: {context.get('format', 'MP4')}
Resolution: {random.choice(['1280x720', '1920x1080'])}
Duration: {random.choice(['00:12:34', '00:18:56', '00:25:12'])}
Frame Rate: 30 fps
Codec: H.264
Officer: {context.get('officer', 'Unknown')}
Date: {context.get('date', datetime.now().strftime('%Y-%m-%d'))}

VIDEO QUALITY:
- Recording quality: {random.choice(['High', 'Good', 'Moderate'])}
- Stability: {random.choice(['Stable', 'Some movement', 'Unstable'])}
- Audio quality: {random.choice(['Clear', 'Moderate', 'Poor'])}
- Lighting: {random.choice(['Good', 'Variable', 'Poor'])}
- Field of view: {random.choice(['Wide', 'Normal', 'Narrow'])}
- Overall assessment: {random.choice(['Excellent', 'Good', 'Adequate'])}
"""
    
    else:
        return f"""--- VIDEO DESCRIPTION ---
File: {context.get('filename', 'video_001.mp4')}
Format: {context.get('format', 'MP4')}
Duration: {random.choice(['00:10:00', '00:20:00', '00:30:00'])}
Quality: {random.choice(['Good', 'Moderate', 'Poor'])}
"""


def generate_spreadsheet_description(context: Dict = None) -> str:
    """Generate a description of spreadsheet data."""
    context = context or {}
    
    return f"""--- SPREADSHEET DATA DESCRIPTION ---
File: {context.get('filename', 'data_001.xlsx')}
Format: {context.get('format', 'XLSX')}
Sheets: {random.randint(1, 5)}
Rows: {random.randint(100, 10000)}
Columns: {random.randint(5, 20)}
Date Created: {context.get('date', datetime.now().strftime('%Y-%m-%d'))}

DATA STRUCTURE:
- Headers: {random.choice(['Present', 'Missing', 'Partial'])}
- Data types: {random.choice(['Mixed', 'Numeric', 'Text', 'Dates'])}
- Formatting: {random.choice(['Formatted', 'Plain', 'Mixed'])}
- Formulas: {random.choice(['Present', 'None', 'Some'])}
- Charts: {random.choice(['None', '1-3 charts', 'Multiple charts'])}
- Overall structure: {random.choice(['Well-organized', 'Moderate', 'Poorly organized'])}
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
    
    def generate_image_description_document(self, image_type: str, 
                                           context: Dict = None) -> Dict:
        """Generate an image description document."""
        context = context or {}
        context['filename'] = self._generate_filename('photo', FileFormat.JPEG)
        content = generate_image_description(image_type, context)
        return self.generate_document('photo', content, FileFormat.TXT)
    
    def generate_audio_transcript_document(self, audio_type: str,
                                          context: Dict = None) -> Dict:
        """Generate an audio transcript document."""
        context = context or {}
        context['filename'] = self._generate_filename('audio', FileFormat.WAV)
        content = generate_audio_transcript(audio_type, context)
        return self.generate_document('audio', content, FileFormat.TXT)
    
    def generate_video_description_document(self, video_type: str,
                                           context: Dict = None) -> Dict:
        """Generate a video description document."""
        context = context or {}
        context['filename'] = self._generate_filename('video', FileFormat.MP4)
        content = generate_video_description(video_type, context)
        return self.generate_document('video', content, FileFormat.TXT)
    
    def generate_spreadsheet_description_document(self, context: Dict = None) -> Dict:
        """Generate a spreadsheet description document."""
        context = context or {}
        context['filename'] = self._generate_filename('spreadsheet', FileFormat.XLSX)
        content = generate_spreadsheet_description(context)
        return self.generate_document('spreadsheet', content, FileFormat.TXT)

