"""
AI model integration for enhancing procedural generation.
Supports Anthropic, OpenAI, Gemini, xAI, and local models.
"""
import os
from typing import Optional, Dict, List
from abc import ABC, abstractmethod

class AIModelInterface(ABC):
    """Abstract base class for AI model interfaces."""
    
    @abstractmethod
    def enhance_text(self, text: str, context: Dict) -> str:
        """Enhance procedural text with AI."""
        pass

class AnthropicInterface(AIModelInterface):
    """Anthropic Claude interface."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("anthropic package required. Install with: pip install anthropic")
    
    def enhance_text(self, text: str, context: Dict) -> str:
        """Enhance text using Claude."""
        prompt = f"""You are enhancing a law enforcement case document. Make the following text more realistic and natural while maintaining accuracy and professionalism.

Context: {context.get('crime_type', 'Unknown')} case, {context.get('document_type', 'report')}

Original text:
{text}

Enhanced text (more natural, less robotic, but still professional):"""
        
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return text  # Fallback to original on error

class OpenAIInterface(AIModelInterface):
    """OpenAI GPT interface."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")
    
    def enhance_text(self, text: str, context: Dict) -> str:
        """Enhance text using GPT."""
        prompt = f"""You are enhancing a law enforcement case document. Make the following text more realistic and natural while maintaining accuracy and professionalism.

Context: {context.get('crime_type', 'Unknown')} case, {context.get('document_type', 'report')}

Original text:
{text}

Enhanced text (more natural, less robotic, but still professional):"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return text  # Fallback to original on error

class GeminiInterface(AIModelInterface):
    """Google Gemini interface."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except ImportError:
            raise ImportError("google-generativeai package required. Install with: pip install google-generativeai")
    
    def enhance_text(self, text: str, context: Dict) -> str:
        """Enhance text using Gemini."""
        prompt = f"""You are enhancing a law enforcement case document. Make the following text more realistic and natural while maintaining accuracy and professionalism.

Context: {context.get('crime_type', 'Unknown')} case, {context.get('document_type', 'report')}

Original text:
{text}

Enhanced text (more natural, less robotic, but still professional):"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return text  # Fallback to original on error

class XAIInterface(AIModelInterface):
    """xAI Grok interface."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            from xai import Client
            self.client = Client(api_key=api_key)
        except ImportError:
            raise ImportError("xai package required. Install with: pip install xai")
    
    def enhance_text(self, text: str, context: Dict) -> str:
        """Enhance text using Grok."""
        prompt = f"""You are enhancing a law enforcement case document. Make the following text more realistic and natural while maintaining accuracy and professionalism.

Context: {context.get('crime_type', 'Unknown')} case, {context.get('document_type', 'report')}

Original text:
{text}

Enhanced text (more natural, less robotic, but still professional):"""
        
        try:
            response = self.client.chat.completions.create(
                model="grok-beta",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return text  # Fallback to original on error

class LocalModelInterface(AIModelInterface):
    """Local model interface (Ollama, etc.)."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model_name: str = "llama2"):
        self.base_url = base_url
        self.model_name = model_name
        try:
            import requests
            self.requests = requests
        except ImportError:
            raise ImportError("requests package required. Install with: pip install requests")
    
    def enhance_text(self, text: str, context: Dict) -> str:
        """Enhance text using local model."""
        prompt = f"""You are enhancing a law enforcement case document. Make the following text more realistic and natural while maintaining accuracy and professionalism.

Context: {context.get('crime_type', 'Unknown')} case, {context.get('document_type', 'report')}

Original text:
{text}

Enhanced text (more natural, less robotic, but still professional):"""
        
        try:
            response = self.requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                }
            )
            if response.status_code == 200:
                return response.json().get("response", text)
            return text
        except Exception as e:
            return text  # Fallback to original on error

class AIEnhancer:
    """Main AI enhancement interface."""
    
    def __init__(self, model_type: str = "none", api_key: Optional[str] = None, **kwargs):
        self.model_type = model_type.lower()
        self.model: Optional[AIModelInterface] = None
        
        if model_type.lower() == "anthropic" and api_key:
            self.model = AnthropicInterface(api_key)
        elif model_type.lower() == "openai" and api_key:
            self.model = OpenAIInterface(api_key)
        elif model_type.lower() == "gemini" and api_key:
            self.model = GeminiInterface(api_key)
        elif model_type.lower() == "xai" and api_key:
            self.model = XAIInterface(api_key)
        elif model_type.lower() == "local":
            base_url = kwargs.get("base_url", "http://localhost:11434")
            model_name = kwargs.get("model_name", "llama2")
            self.model = LocalModelInterface(base_url, model_name)
    
    def enhance_document(self, document: str, crime_type: str, document_type: str = "report") -> str:
        """Enhance a document with AI if model is available."""
        if not self.model or self.model_type == "none":
            return document
        
        context = {
            "crime_type": crime_type,
            "document_type": document_type
        }
        
        try:
            # Only enhance narrative/text portions, not structured data
            if "---" in document:
                parts = document.split("---")
                header = parts[0] if len(parts) > 0 else ""
                content = "---".join(parts[1:]) if len(parts) > 1 else document
                
                # Enhance content but keep header
                enhanced_content = self.model.enhance_text(content, context)
                return header + "---" + enhanced_content if header else enhanced_content
            else:
                return self.model.enhance_text(document, context)
        except Exception as e:
            # On error, return original
            return document

