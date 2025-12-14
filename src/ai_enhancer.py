"""
AI model integration for enhancing procedural generation.
Supports Anthropic, OpenAI, Gemini, xAI, and local models.
"""
import os
import sys
from typing import Optional, Dict, List
from abc import ABC, abstractmethod

# Debug flag - set to True to see AI calls
DEBUG = True

def debug_print(message: str):
    """Print debug message if DEBUG is enabled."""
    if DEBUG:
        print(f"[AI_DEBUG] {message}", file=sys.stderr, flush=True)

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
        debug_print(f"Anthropic: Enhancing text ({len(text)} chars)")
        prompt = f"""You are enhancing a law enforcement case document. Make the following text more realistic and natural while maintaining accuracy and professionalism.

Context: {context.get('crime_type', 'Unknown')} case, {context.get('document_type', 'report')}

Original text:
{text}

Enhanced text (more natural, less robotic, but still professional):"""
        
        try:
            debug_print(f"Anthropic: Calling API with model claude-3-5-sonnet-20241022")
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            result = message.content[0].text
            debug_print(f"Anthropic: Successfully enhanced ({len(result)} chars returned)")
            return result
        except Exception as e:
            debug_print(f"Anthropic: ERROR - {type(e).__name__}: {str(e)}")
            raise  # Re-raise so caller knows it failed

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
        debug_print(f"OpenAI: Enhancing text ({len(text)} chars)")
        prompt = f"""You are enhancing a law enforcement case document. Make the following text more realistic and natural while maintaining accuracy and professionalism.

Context: {context.get('crime_type', 'Unknown')} case, {context.get('document_type', 'report')}

Original text:
{text}

Enhanced text (more natural, less robotic, but still professional):"""
        
        try:
            debug_print(f"OpenAI: Calling API with model gpt-4")
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            result = response.choices[0].message.content
            debug_print(f"OpenAI: Successfully enhanced ({len(result)} chars returned)")
            return result
        except Exception as e:
            debug_print(f"OpenAI: ERROR - {type(e).__name__}: {str(e)}")
            raise  # Re-raise so caller knows it failed

class GeminiInterface(AIModelInterface):
    """Google Gemini interface."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            import google.generativeai as genai
            debug_print(f"Gemini: Configuring with API key (length: {len(api_key) if api_key else 0})")
            genai.configure(api_key=api_key)
            
            # Try different model names in order of preference
            # Note: Must use full model name with 'models/' prefix
            model_names = [
                'models/gemini-2.0-flash',  # Fast, widely available
                'models/gemini-2.5-flash',  # Latest flash model
                'models/gemini-2.5-pro',     # Latest pro model
                'models/gemini-2.0-flash-001',  # Stable version
            ]
            
            self.model = None
            last_error = None
            
            for model_name in model_names:
                try:
                    debug_print(f"Gemini: Attempting to load model '{model_name}'")
                    self.model = genai.GenerativeModel(model_name)
                    debug_print(f"Gemini: Successfully loaded model '{model_name}'")
                    break
                except Exception as e:
                    debug_print(f"Gemini: Failed to load '{model_name}': {type(e).__name__}: {str(e)}")
                    last_error = e
                    continue
            
            if self.model is None:
                raise Exception(f"Could not load any Gemini model. Last error: {last_error}")
                
        except ImportError:
            raise ImportError("google-generativeai package required. Install with: pip install google-generativeai")
    
    def enhance_text(self, text: str, context: Dict) -> str:
        """Enhance text using Gemini."""
        debug_print(f"Gemini: Enhancing text ({len(text)} chars)")
        prompt = f"""You are enhancing a law enforcement case document. Make the following text more realistic and natural while maintaining accuracy and professionalism.

Context: {context.get('crime_type', 'Unknown')} case, {context.get('document_type', 'report')}

Original text:
{text}

Enhanced text (more natural, less robotic, but still professional):"""
        
        try:
            debug_print(f"Gemini: Calling generate_content API")
            response = self.model.generate_content(prompt)
            result = response.text
            debug_print(f"Gemini: Successfully enhanced ({len(result)} chars returned)")
            return result
        except Exception as e:
            debug_print(f"Gemini: ERROR - {type(e).__name__}: {str(e)}")
            raise  # Re-raise so caller knows it failed

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
        debug_print(f"xAI: Enhancing text ({len(text)} chars)")
        prompt = f"""You are enhancing a law enforcement case document. Make the following text more realistic and natural while maintaining accuracy and professionalism.

Context: {context.get('crime_type', 'Unknown')} case, {context.get('document_type', 'report')}

Original text:
{text}

Enhanced text (more natural, less robotic, but still professional):"""
        
        try:
            debug_print(f"xAI: Calling API with model grok-beta")
            response = self.client.chat.completions.create(
                model="grok-beta",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            result = response.choices[0].message.content
            debug_print(f"xAI: Successfully enhanced ({len(result)} chars returned)")
            return result
        except Exception as e:
            debug_print(f"xAI: ERROR - {type(e).__name__}: {str(e)}")
            raise  # Re-raise so caller knows it failed

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
        debug_print(f"Local ({self.model_name}): Enhancing text ({len(text)} chars)")
        prompt = f"""You are enhancing a law enforcement case document. Make the following text more realistic and natural while maintaining accuracy and professionalism.

Context: {context.get('crime_type', 'Unknown')} case, {context.get('document_type', 'report')}

Original text:
{text}

Enhanced text (more natural, less robotic, but still professional):"""
        
        try:
            url = f"{self.base_url}/api/generate"
            debug_print(f"Local: Calling {url} with model {self.model_name}")
            response = self.requests.post(
                url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120  # 2 minute timeout for local models
            )
            if response.status_code == 200:
                result = response.json().get("response", text)
                debug_print(f"Local: Successfully enhanced ({len(result)} chars returned)")
                return result
            else:
                debug_print(f"Local: ERROR - HTTP {response.status_code}: {response.text}")
                raise Exception(f"Local model returned status {response.status_code}")
        except Exception as e:
            debug_print(f"Local: ERROR - {type(e).__name__}: {str(e)}")
            raise  # Re-raise so caller knows it failed

class AIEnhancer:
    """Main AI enhancement interface."""
    
    def __init__(self, model_type: str = "none", api_key: Optional[str] = None, **kwargs):
        self.model_type = model_type.lower()
        self.model: Optional[AIModelInterface] = None
        
        debug_print(f"AIEnhancer: Initializing with model_type='{model_type}', api_key provided={api_key is not None}")
        
        if model_type.lower() == "anthropic":
            if not api_key:
                raise ValueError("API key required for Anthropic")
            debug_print("AIEnhancer: Creating AnthropicInterface")
            self.model = AnthropicInterface(api_key)
        elif model_type.lower() == "openai":
            if not api_key:
                raise ValueError("API key required for OpenAI")
            debug_print("AIEnhancer: Creating OpenAIInterface")
            self.model = OpenAIInterface(api_key)
        elif model_type.lower() == "gemini":
            if not api_key:
                raise ValueError("API key required for Gemini")
            debug_print("AIEnhancer: Creating GeminiInterface")
            self.model = GeminiInterface(api_key)
        elif model_type.lower() == "xai":
            if not api_key:
                raise ValueError("API key required for xAI")
            debug_print("AIEnhancer: Creating XAIInterface")
            self.model = XAIInterface(api_key)
        elif model_type.lower() == "local":
            base_url = kwargs.get("base_url", "http://localhost:11434")
            model_name = kwargs.get("model_name", "llama2")
            debug_print(f"AIEnhancer: Creating LocalModelInterface (base_url={base_url}, model={model_name})")
            self.model = LocalModelInterface(base_url, model_name)
        else:
            debug_print(f"AIEnhancer: No model initialized (model_type='{model_type}')")
    
    def enhance_document(self, document: str, crime_type: str, document_type: str = "report") -> str:
        """Enhance a document with AI if model is available."""
        if not self.model or self.model_type == "none":
            debug_print("AIEnhancer: No model available, skipping enhancement")
            return document
        
        debug_print(f"AIEnhancer: Enhancing document (type={document_type}, length={len(document)} chars)")
        
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
                
                debug_print(f"AIEnhancer: Document has header, enhancing content portion ({len(content)} chars)")
                # Enhance content but keep header
                enhanced_content = self.model.enhance_text(content, context)
                result = header + "---" + enhanced_content if header else enhanced_content
                debug_print(f"AIEnhancer: Document enhanced successfully (result length={len(result)} chars)")
                return result
            else:
                debug_print(f"AIEnhancer: Enhancing entire document")
                result = self.model.enhance_text(document, context)
                debug_print(f"AIEnhancer: Document enhanced successfully (result length={len(result)} chars)")
                return result
        except Exception as e:
            # Log error but return original
            debug_print(f"AIEnhancer: ERROR during enhancement - {type(e).__name__}: {str(e)}")
            debug_print(f"AIEnhancer: Returning original document due to error")
            return document

