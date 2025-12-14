#!/usr/bin/env python3
"""
Simple web interface for the Law Enforcement Case Generator CLI
"""

import os
import sys
from flask import Flask, render_template_string, request, redirect, url_for
import subprocess
import threading
import time
import json
from io import StringIO

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Law Enforcement Case Generator</title>
    <style>
        * { 
            box-sizing: border-box; 
            margin: 0;
            padding: 0;
        }
        body { 
            font-family: 'Georgia', 'Times New Roman', serif; 
            margin: 0; 
            padding: 0; 
            background: #f5f5f5;
            min-height: 100vh;
            color: #1a1a1a;
        }
        .header {
            background: linear-gradient(180deg, #003366 0%, #004080 100%);
            color: #FFD700;
            padding: 30px 0;
            border-bottom: 4px solid #FFD700;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 40px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.2em;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 8px;
            text-transform: uppercase;
            color: #FFD700;
        }
        .header .subtitle {
            font-size: 1.1em;
            color: #E6E6FA;
            font-weight: 400;
            letter-spacing: 0.5px;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            padding: 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border: 1px solid #ddd;
        }
        .content-wrapper {
            padding: 40px;
        }
        .section { 
            margin-bottom: 35px; 
            padding: 30px; 
            border: 1px solid #d0d0d0; 
            background: #fafafa;
            border-left: 5px solid #003366;
        }
        .section h2 {
            color: #003366;
            margin-top: 0;
            margin-bottom: 25px;
            font-size: 1.6em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #FFD700;
            padding-bottom: 12px;
        }
        .form-group { 
            margin-bottom: 25px; 
        }
        label { 
            display: block; 
            margin-bottom: 10px; 
            font-weight: 600;
            color: #003366;
            font-size: 1.05em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.95em;
        }
        select, input[type="text"], input[type="number"] { 
            width: 100%; 
            padding: 12px 15px; 
            border: 2px solid #ccc; 
            border-radius: 4px;
            font-size: 1em;
            font-family: 'Georgia', 'Times New Roman', serif;
            transition: border-color 0.3s;
            background: white;
            color: #1a1a1a;
        }
        select {
            color: #1a1a1a;
            background-color: white;
        }
        select option {
            color: #1a1a1a;
            background-color: white;
            padding: 8px;
        }
        select:focus, input:focus {
            outline: none;
            border-color: #003366;
            box-shadow: 0 0 0 3px rgba(0, 51, 102, 0.1);
        }
        select:focus {
            color: #1a1a1a;
            background-color: white;
        }
        .radio-group { 
            display: flex; 
            gap: 20px; 
            flex-wrap: wrap;
        }
        .radio-option { 
            display: flex; 
            align-items: center;
            padding: 12px 18px;
            background: white;
            border: 2px solid #ccc;
            border-radius: 4px;
            transition: all 0.3s;
            flex: 1;
            min-width: 200px;
        }
        .radio-option:hover {
            border-color: #003366;
            background: #f0f4f8;
        }
        .radio-option input[type="radio"]:checked + label {
            color: #003366;
            font-weight: 700;
        }
        .radio-option input[type="radio"] {
            margin-right: 10px;
            width: auto;
            accent-color: #003366;
        }
        .radio-option label {
            margin: 0;
            font-weight: 500;
            cursor: pointer;
            text-transform: none;
            letter-spacing: normal;
            font-size: 1em;
        }
        .modifiers { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 15px; 
        }
        .modifier-item { 
            display: flex; 
            align-items: flex-start;
            padding: 18px;
            background: white;
            border: 2px solid #d0d0d0;
            border-radius: 4px;
            transition: all 0.3s;
        }
        .modifier-item:hover {
            border-color: #003366;
            box-shadow: 0 2px 8px rgba(0, 51, 102, 0.15);
        }
        .modifier-item input[type="checkbox"] { 
            margin-right: 12px; 
            margin-top: 3px;
            width: auto;
            cursor: pointer;
            accent-color: #003366;
        }
        .modifier-item label {
            margin: 0;
            cursor: pointer;
            font-weight: 500;
            line-height: 1.5;
            text-transform: none;
            letter-spacing: normal;
            color: #1a1a1a;
        }
        .modifier-item small {
            display: block;
            color: #666;
            font-size: 0.85em;
            margin-top: 6px;
            font-style: italic;
        }
        .btn { 
            background: #003366;
            color: #FFD700; 
            padding: 16px 50px; 
            border: 2px solid #FFD700; 
            border-radius: 4px; 
            cursor: pointer; 
            font-size: 1.1em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            font-family: 'Georgia', 'Times New Roman', serif;
        }
        .btn:hover { 
            background: #004080;
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            transform: translateY(-2px);
        }
        .btn:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .output { 
            background: #1a1a1a; 
            color: #e0e0e0;
            padding: 20px; 
            border-radius: 4px; 
            font-family: 'Courier New', monospace; 
            white-space: pre-wrap; 
            max-height: 500px; 
            overflow-y: auto;
            font-size: 0.9em;
            line-height: 1.6;
            border: 1px solid #333;
        }
        .output::-webkit-scrollbar {
            width: 12px;
        }
        .output::-webkit-scrollbar-track {
            background: #2a2a2a;
        }
        .output::-webkit-scrollbar-thumb {
            background: #555;
            border-radius: 6px;
        }
        .output::-webkit-scrollbar-thumb:hover {
            background: #666;
        }
        .status { 
            text-align: center; 
            padding: 25px; 
            border-radius: 4px;
            margin-bottom: 30px;
            border: 2px solid;
        }
        .error { 
            color: #8B0000;
            background: #ffe6e6;
            border-color: #8B0000;
        }
        .success { 
            color: #006400;
            background: #e6ffe6;
            border-color: #006400;
        }
        .trend-section {
            background: #fffef0;
            border-left: 5px solid #FFD700;
            border: 1px solid #d0d0d0;
        }
        .trend-section h2 {
            border-bottom-color: #FFD700;
            color: #003366;
        }
        .info-box {
            background: #f0f4f8;
            border-left: 4px solid #003366;
            padding: 18px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .info-box p {
            margin: 5px 0;
            color: #003366;
            font-weight: 500;
        }
        .footer {
            background: #003366;
            color: #FFD700;
            padding: 20px;
            text-align: center;
            font-size: 0.9em;
            border-top: 2px solid #FFD700;
        }
        details {
            margin-top: 15px;
        }
        details summary {
            cursor: pointer;
            color: #003366;
            font-weight: 600;
            padding: 10px;
            background: #f0f4f8;
            border-radius: 4px;
            border: 1px solid #d0d0d0;
        }
        details summary:hover {
            background: #e0e8f0;
        }
        .file-list {
            background: #f8f8f8;
            padding: 15px;
            border-radius: 4px;
            margin-top: 10px;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>Law Enforcement Case Generator</h1>
            <p class="subtitle">Procedural Case Data Generator for AI Training & Evaluation</p>
        </div>
    </div>
    <div class="container">
        <div class="content-wrapper">

        {% if status %}
        <div class="section status">
            {% if error %}
                <h2 class="error">{{ status }}</h2>
                <p>{{ error }}</p>
            {% else %}
                <h2 class="success">{{ status }}</h2>
                {% if output %}
                <div class="output">{{ output }}</div>
                {% endif %}
            {% endif %}
        </div>
        {% endif %}

        <form method="POST">
            <div class="section">
                <h2>Case Configuration</h2>

                <div class="form-group">
                    <label for="crime_type">Crime Type:</label>
                    <select name="crime_type" id="crime_type" required>
                        <option value="">Select a crime type...</option>
                        <option value="1">Homicide</option>
                        <option value="2">Assault</option>
                        <option value="3">Robbery</option>
                        <option value="4">Burglary</option>
                        <option value="5">Theft</option>
                        <option value="6">Fraud</option>
                        <option value="7">Drug Possession</option>
                        <option value="8">Domestic Violence</option>
                        <option value="9">Stalking</option>
                        <option value="10">Arson</option>
                        <option value="11">Cybercrime</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Complexity Level:</label>
                    <div class="radio-group">
                        <div class="radio-option">
                            <input type="radio" name="complexity" value="Low" id="low" required>
                            <label for="low">Low (Basic investigation)</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" name="complexity" value="Medium" id="medium">
                            <label for="medium">Medium (Moderate detail)</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" name="complexity" value="High" id="high">
                            <label for="high">High (Comprehensive investigation)</label>
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label>Subject Status:</label>
                    <div class="radio-group">
                        <div class="radio-option">
                            <input type="radio" name="subject_status" value="Known" id="known" checked>
                            <label for="known">Known Subjects</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" name="subject_status" value="Unknown" id="unknown">
                            <label for="unknown">Unknown Subjects</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" name="subject_status" value="Partially Known" id="partial">
                            <label for="partial">Partially Known</label>
                        </div>
                    </div>
                </div>

                <div class="form-group" id="subject_clarity_group" style="display: none;">
                    <label>Subject Identification Approach:</label>
                    <select name="subject_clarity" id="subject_clarity">
                        <option value="Embedded">Embedded Solution (Traditional)</option>
                        <option value="Investigative">Investigative Challenge (Multiple Suspects)</option>
                    </select>
                    <div class="help-text">
                        <strong>Embedded:</strong> Solution is embedded in case data<br>
                        <strong>Investigative:</strong> Create multiple persons of interest for analysis
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>Investigative Modifiers</h2>
                <p>Select any additional investigative techniques to include:</p>

                <div class="modifiers">
                    <div class="modifier-item">
                        <input type="checkbox" name="modifiers" value="1" id="phone">
                        <label for="phone">Phone Data Pull<br><small>Extract phone records, texts, and call logs</small></label>
                    </div>
                    <div class="modifier-item">
                        <input type="checkbox" name="modifiers" value="2" id="ip">
                        <label for="ip">IP Logs<br><small>Network traffic analysis and IP address tracking</small></label>
                    </div>
                    <div class="modifier-item">
                        <input type="checkbox" name="modifiers" value="3" id="dns">
                        <label for="dns">DNS Records<br><small>Domain name resolution and internet history</small></label>
                    </div>
                    <div class="modifier-item">
                        <input type="checkbox" name="modifiers" value="4" id="bodycam">
                        <label for="bodycam">Body Cam<br><small>Officer body camera footage and transcripts</small></label>
                    </div>
                    <div class="modifier-item">
                        <input type="checkbox" name="modifiers" value="5" id="email">
                        <label for="email">Email Dump<br><small>Email account contents and metadata</small></label>
                    </div>
                    <div class="modifier-item">
                        <input type="checkbox" name="modifiers" value="6" id="financial">
                        <label for="financial">Financial Records<br><small>Bank statements and transaction analysis</small></label>
                    </div>
                    <div class="modifier-item">
                        <input type="checkbox" name="modifiers" value="7" id="massive_phone">
                        <label for="massive_phone">Data-Heavy Phone Dump<br><small>MASSIVE phone extraction (5K-15K records)</small></label>
                    </div>
                    <div class="modifier-item">
                        <input type="checkbox" name="modifiers" value="8" id="massive_ip">
                        <label for="massive_ip">Data-Heavy IP Logs<br><small>MASSIVE network logs (10K-50K entries)</small></label>
                    </div>
                    <div class="modifier-item">
                        <input type="checkbox" name="modifiers" value="9" id="massive_financial">
                        <label for="massive_financial">Data-Heavy Financial<br><small>MASSIVE financial records (5K-20K transactions)</small></label>
                    </div>
                    <div class="modifier-item">
                        <input type="checkbox" name="modifiers" value="10" id="junk_data">
                        <label for="junk_data">Extra Junk Data<br><small>Generate extensive irrelevant documents</small></label>
                    </div>
                    <div class="modifier-item">
                        <input type="checkbox" name="modifiers" value="11" id="random_events">
                        <label for="random_events">Random Events<br><small>Add unpredictable events (car wrecks, etc.)</small></label>
                    </div>
                </div>
            </div>

            <div class="section trend-section">
                <h2>Trend Generation (Optional)</h2>
                <div class="info-box">
                    <p><strong>Generate multiple related cases</strong> that share entities, locations, or patterns.</p>
                </div>
                
                <div class="form-group">
                    <label>Generate a Trend of Related Cases?</label>
                    <div class="radio-group">
                        <div class="radio-option">
                            <input type="radio" name="generate_trend" value="no" id="trend_no" checked onchange="toggleTrendOptions()">
                            <label for="trend_no">No (Generate single case)</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" name="generate_trend" value="yes" id="trend_yes" onchange="toggleTrendOptions()">
                            <label for="trend_yes">Yes (Generate trend)</label>
                        </div>
                    </div>
                </div>

                <div id="trend_options" style="display: none;">
                <div class="form-group">
                    <label for="trend_type">Trend Type:</label>
                    <select name="trend_type" id="trend_type">
                        <option value="Serial Offender">Serial Offender</option>
                        <option value="Organized Crime">Organized Crime</option>
                        <option value="Crime Ring">Crime Ring</option>
                        <option value="Victim Pattern">Victim Pattern</option>
                        <option value="Location Pattern">Location Pattern</option>
                        <option value="Mixed">Mixed</option>
                    </select>
                </div>
            </div>

            <div class="section">
                <h2>AI Enhancement (Optional)</h2>
                <div class="info-box">
                    <p><strong>Use AI models to enhance dialogue and narratives</strong> to make them less robotic and more realistic.</p>
                </div>
                
                <div class="form-group">
                    <label>AI Enhancement Mode:</label>
                    <div class="radio-group">
                        <div class="radio-option">
                            <input type="radio" name="ai_mode" value="none" id="ai_none" checked onchange="toggleAIOptions()">
                            <label for="ai_none">Procedural Only (Default)</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" name="ai_mode" value="anthropic" id="ai_anthropic" onchange="toggleAIOptions()">
                            <label for="ai_anthropic">Anthropic Claude</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" name="ai_mode" value="openai" id="ai_openai" onchange="toggleAIOptions()">
                            <label for="ai_openai">OpenAI GPT</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" name="ai_mode" value="gemini" id="ai_gemini" onchange="toggleAIOptions()">
                            <label for="ai_gemini">Google Gemini</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" name="ai_mode" value="xai" id="ai_xai" onchange="toggleAIOptions()">
                            <label for="ai_xai">xAI Grok</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" name="ai_mode" value="local" id="ai_local" onchange="toggleAIOptions()">
                            <label for="ai_local">Local Model (Ollama)</label>
                        </div>
                    </div>
                </div>

                <div id="ai_options" style="display: none;">
                    <div class="form-group">
                        <label for="api_key">API Key / Base URL:</label>
                        <input type="text" name="api_key" id="api_key" placeholder="Enter API key or local model URL">
                        <small style="display: block; color: #666; margin-top: 5px;">
                            For local models, enter base URL (e.g., http://localhost:11434)
                        </small>
                    </div>
                    <div class="form-group" id="local_model_name_group" style="display: none;">
                        <label for="local_model_name">Local Model Name:</label>
                        <input type="text" name="local_model_name" id="local_model_name" value="llama2" placeholder="llama2">
                    </div>
                </div>
                    <div class="form-group">
                        <label for="num_cases">Number of Related Cases:</label>
                        <input type="number" name="num_cases" id="num_cases" value="3" min="2" max="10" style="width: 150px;">
                    </div>
                    <div class="form-group">
                        <label>Trend Identification Status:</label>
                        <div class="radio-group">
                            <div class="radio-option">
                                <input type="radio" name="identification_status" value="Identified" id="identified_trend" checked>
                                <label for="identified_trend">Identified (Known links, unproven)</label>
                            </div>
                            <div class="radio-option">
                                <input type="radio" name="identification_status" value="Unidentified" id="unidentified_trend">
                                <label for="unidentified_trend">Unidentified (Hidden connections, AI discoverable)</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <button type="submit" class="btn">Generate Case</button>
            </div>
        </form>
        
        <script>
            function toggleTrendOptions() {
                const trendYes = document.getElementById('trend_yes');
                const trendOptions = document.getElementById('trend_options');
                if (trendYes.checked) {
                    trendOptions.style.display = 'block';
                } else {
                    trendOptions.style.display = 'none';
                }
            }
            
            function toggleAIOptions() {
                const aiNone = document.getElementById('ai_none');
                const aiLocal = document.getElementById('ai_local');
                const aiOptions = document.getElementById('ai_options');
                const localModelGroup = document.getElementById('local_model_name_group');
                
                if (aiNone.checked) {
                    aiOptions.style.display = 'none';
                } else {
                    aiOptions.style.display = 'block';
                    if (aiLocal.checked) {
                        localModelGroup.style.display = 'block';
                    } else {
                        localModelGroup.style.display = 'none';
                    }
                }
            }

            function toggleSubjectClarity() {
                const unknownRadio = document.getElementById('unknown');
                const subjectClarityGroup = document.getElementById('subject_clarity_group');
                if (unknownRadio.checked) {
                    subjectClarityGroup.style.display = 'block';
                } else {
                    subjectClarityGroup.style.display = 'none';
                }
            }

            // Add event listeners to subject status radios
            document.addEventListener('DOMContentLoaded', function() {
                const radios = document.querySelectorAll('input[name="subject_status"]');
                radios.forEach(radio => {
                    radio.addEventListener('change', toggleSubjectClarity);
                });
            });
        </script>

        {% if case_path %}
        <div class="section">
            <h2>Generated Case Files</h2>
            <p><strong>Case exported to:</strong> {{ case_path }}</p>
            <div class="output">
Files created:
{% for file in case_files %}
{{ file }}
{% endfor %}
            </div>
        </div>
        {% endif %}
        
        {% if case_paths %}
        <div class="section">
            <h2>Generated Trend Cases</h2>
            <p><strong>Trend ID:</strong> {{ trend_id }}</p>
            <p><strong>Total Cases:</strong> {{ case_paths|length }}</p>
            {% for case_info in case_files_list %}
            <div style="margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                <h3 style="margin-top: 0; color: #2c3e50;">{{ case_info.case_id }}</h3>
                <p><strong>Path:</strong> {{ case_info.path }}</p>
                <details>
                    <summary style="cursor: pointer; color: #3498db; font-weight: 600;">View Files ({{ case_info.files|length }})</summary>
                    <div class="output" style="margin-top: 10px; max-height: 300px;">
{% for file in case_info.files %}
{{ file }}
{% endfor %}
                    </div>
                </details>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        </div>
    </div>
    <div class="footer">
        <p>Law Enforcement Case Generator | Official Use Only</p>
    </div>
</body>
</html>
"""

def run_trend_generation(trend_type, num_cases, complexity, modifier_nums, subject_status, subject_clarity, identification_status):
    """Run trend generation process."""
    try:
        from src.trend_generator import TrendGenerator
        from src.exporter import CaseExporter
        
        modifier_options = {
            "1": "Phone data pull", "2": "IP logs", "3": "DNS records",
            "4": "Body Cam", "5": "Email Dump", "6": "Financial Records",
            "7": "Data-Heavy Phone Dump", "8": "Data-Heavy IP Logs",
            "9": "Data-Heavy Financial", "10": "Extra Junk Data",
            "11": "Random Events"
        }
        
        modifiers = []
        if modifier_nums:
            for num in modifier_nums:
                if num in modifier_options:
                    modifiers.append(modifier_options[num])
        
        trend_gen = TrendGenerator()
        cases, registry = trend_gen.generate_trend(
            trend_type=trend_type,
            num_cases=num_cases,
            base_complexity=complexity,
            base_modifiers=modifiers,
            subject_status=subject_status,
            subject_clarity=subject_clarity,
            identification_status=identification_status
        )
        
        if not cases:
            return {
                'success': False,
                'error': 'Trend generation returned no cases'
            }
        
        # Export all cases
        export_paths = []
        case_files_list = []
        for case in cases:
            case_path = CaseExporter.export(case)
            export_paths.append(case_path)
            if os.path.exists(case_path):
                files = []
                for root, dirs, files_in_dir in os.walk(case_path):
                    for file in files_in_dir:
                        rel_path = os.path.relpath(os.path.join(root, file), case_path)
                        files.append(rel_path)
                case_files_list.append({'case_id': case.id, 'path': case_path, 'files': files})
        
        # Generate summary output
        output = f"Trend Generated: {trend_type}\n"
        output += f"Trend ID: {registry.trend_id}\n"
        output += f"Total Cases: {len(cases)}\n"
        output += f"Identification Status: {identification_status}\n"
        output += f"Shared Suspects: {len(registry.shared_entities['suspects'])}\n"
        output += f"Case Relationships: {len(registry.case_relationships)}\n\n"
        output += "Cases Generated:\n"
        for i, case in enumerate(cases, 1):
            output += f"  {i}. {case.title}\n"
            output += f"     ID: {case.id}\n"
            output += f"     Documents: {len(case.documents)}\n"
            output += f"     Evidence: {len(case.evidence)}\n\n"
        
        return {
            'success': True,
            'output': output,
            'case_paths': export_paths,
            'case_files_list': case_files_list,
            'trend_id': registry.trend_id
        }
        
    except Exception as e:
        import traceback
        return {
            'success': False,
            'error': f'{str(e)}\n\n{traceback.format_exc()}'
        }

def run_case_generation(crime_type_num, complexity, modifier_nums, subject_status='Known', ai_mode='none', api_key=None, local_model_name='llama2'):
    """Run the case generation process directly using the generator."""
    try:
        # Import the generator directly
        from src.generators import CaseGenerator
        from src.exporter import CaseExporter

        # Convert inputs to generator format
        crime_types = {
            "1": "Homicide", "2": "Assault", "3": "Robbery", "4": "Burglary",
            "5": "Theft", "6": "Fraud", "7": "Drug Possession",
            "8": "Domestic Violence", "9": "Stalking", "10": "Arson",
            "11": "Cybercrime"
        }

        modifier_options = {
            "1": "Phone data pull", "2": "IP logs", "3": "DNS records",
            "4": "Body Cam", "5": "Email Dump", "6": "Financial Records",
            "7": "Data-Heavy Phone Dump", "8": "Data-Heavy IP Logs",
            "9": "Data-Heavy Financial", "10": "Extra Junk Data",
            "11": "Random Events"
        }

        crime_type = crime_types.get(crime_type_num, "Assault")

        # Convert modifier numbers to names
        modifiers = []
        if modifier_nums:
            for num in modifier_nums:
                if num in modifier_options:
                    modifiers.append(modifier_options[num])

        # Initialize AI enhancer if requested
        ai_enhancer = None
        if ai_mode and ai_mode != 'none':
            try:
                from src.ai_enhancer import AIEnhancer, debug_print
                debug_print(f"Web Interface: Initializing AI enhancer with mode='{ai_mode}'")
                
                kwargs = {}
                if ai_mode == 'local' or ai_mode == 'ollama':
                    kwargs['base_url'] = api_key if api_key else 'http://localhost:11434'
                    kwargs['model_name'] = local_model_name if local_model_name else 'llama2'
                    debug_print(f"Web Interface: Local model config - base_url={kwargs['base_url']}, model={kwargs['model_name']}")
                    ai_enhancer = AIEnhancer(model_type='local', **kwargs)
                else:
                    if not api_key:
                        debug_print(f"Web Interface: WARNING - No API key provided for {ai_mode}")
                        raise ValueError(f"API key required for {ai_mode}")
                    debug_print(f"Web Interface: API key provided (length={len(api_key)})")
                    ai_enhancer = AIEnhancer(model_type=ai_mode, api_key=api_key)
                debug_print(f"Web Interface: AI enhancer initialized successfully")
            except Exception as e:
                # Log the error but continue without AI
                import traceback
                error_msg = f"Failed to initialize AI enhancer: {type(e).__name__}: {str(e)}"
                print(f"[ERROR] {error_msg}", file=sys.stderr, flush=True)
                print(f"[ERROR] Traceback: {traceback.format_exc()}", file=sys.stderr, flush=True)
                ai_enhancer = None
        
        # Generate case directly
        generator = CaseGenerator()
        case = generator.generate_case(crime_type, complexity, modifiers, subject_status=subject_status, subject_clarity=subject_clarity)
        
        # Enhance documents with AI if available
        if ai_enhancer and case:
            from src.ai_enhancer import debug_print
            debug_print(f"Web Interface: Starting AI enhancement of {len(case.documents)} documents")
            enhanced_docs = []
            for i, doc in enumerate(case.documents, 1):
                debug_print(f"Web Interface: Enhancing document {i}/{len(case.documents)}")
                try:
                    enhanced = ai_enhancer.enhance_document(doc, crime_type)
                    enhanced_docs.append(enhanced)
                    debug_print(f"Web Interface: Document {i} enhanced successfully")
                except Exception as e:
                    debug_print(f"Web Interface: ERROR enhancing document {i} - {type(e).__name__}: {str(e)}")
                    # Use original if enhancement fails
                    enhanced_docs.append(doc)
            case.documents = enhanced_docs
            debug_print(f"Web Interface: AI enhancement complete - {len(enhanced_docs)} documents processed")
        elif ai_enhancer is None and ai_mode and ai_mode != 'none':
            print(f"[WARNING] AI mode '{ai_mode}' was requested but enhancer is None", file=sys.stderr, flush=True)

        if not case:
            return {
                'success': False,
                'error': 'Case generation returned None'
            }

        # Export the case
        case_path = CaseExporter.export(case)

        if case_path and os.path.exists(case_path):
            # Get list of generated files
            case_files = []
            for root, dirs, files in os.walk(case_path):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), case_path)
                    case_files.append(rel_path)

            # Generate summary output
            output = f"Case Generated: {case.title}\n"
            output += f"Case ID: {case.id}\n"
            output += f"Status: {case.status}\n"
            output += f"Documents: {len(case.documents)}\n"
            output += f"Evidence Items: {len(case.evidence)}\n"
            output += f"Persons Involved: {len(case.persons)}\n"
            output += f"\nCase exported to: {case_path}\n"

            return {
                'success': True,
                'output': output,
                'case_path': case_path,
                'case_files': case_files
            }

        return {
            'success': False,
            'error': 'Case export failed'
        }

    except Exception as e:
        import traceback
        return {
            'success': False,
            'error': f'{str(e)}\n\n{traceback.format_exc()}'
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Safely get form data with defaults
        try:
            crime_type = request.form.get('crime_type', '')
            complexity = request.form.get('complexity', 'Medium')
            subject_status = request.form.get('subject_status', 'Known')
            subject_clarity = request.form.get('subject_clarity', 'Embedded') if subject_status == 'Unknown' else None
            modifiers = request.form.getlist('modifiers') if hasattr(request.form, 'getlist') else []
            generate_trend = request.form.get('generate_trend', 'no')
            ai_mode = request.form.get('ai_mode', 'none')
            api_key = request.form.get('api_key', '')
            local_model_name = request.form.get('local_model_name', 'llama2')
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, 
                status='error',
                message=f'Error reading form data: {str(e)}',
                output='')
        
        if not crime_type or not complexity:
            return render_template_string(HTML_TEMPLATE,
                                        status="Error",
                                        error="Please select both crime type and complexity level.")

        # Check if trend generation is requested
        if generate_trend == 'yes':
            trend_type = request.form.get('trend_type', 'Serial Offender')
            num_cases = int(request.form.get('num_cases', 3))
            identification_status = request.form.get('identification_status', 'Identified')
            
            result = run_trend_generation(trend_type, num_cases, complexity, modifiers,
                                       subject_status, subject_clarity, identification_status)
            
            if result['success']:
                return render_template_string(HTML_TEMPLATE,
                                            status="Trend Generated Successfully",
                                            output=result['output'],
                                            case_paths=result.get('case_paths', []),
                                            case_files_list=result.get('case_files_list', []),
                                            trend_id=result.get('trend_id'))
            else:
                return render_template_string(HTML_TEMPLATE,
                                            status="Trend Generation Failed",
                                            error=result.get('error', 'Unknown error'),
                                            output=result.get('output', ''))
        else:
            # Run single case generation
            result = run_case_generation(crime_type, complexity, modifiers, subject_status, ai_mode, api_key, local_model_name)

            if result['success']:
                return render_template_string(HTML_TEMPLATE,
                                            status="Case Generated Successfully",
                                            output=result['output'],
                                            case_path=result.get('case_path'),
                                            case_files=result.get('case_files', []))
            else:
                return render_template_string(HTML_TEMPLATE,
                                            status="Generation Failed",
                                            error=result.get('error', 'Unknown error'),
                                            output=result.get('output', ''))

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    import webbrowser
    import threading
    
    print("=" * 60)
    print("Case Data Generator - Web Interface")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    print("Browser should open automatically...")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Open browser after a short delay
    def open_browser():
        import time
        time.sleep(1.5)
        try:
            webbrowser.open('http://localhost:5000')
        except Exception as e:
            print(f"Could not open browser automatically: {e}")
            print("Please navigate to http://localhost:5000 manually")
    
    # Start browser opener in background
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    except Exception as e:
        print(f"ERROR: Failed to start server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure port 5000 is not in use")
        print("2. Check firewall settings")
        print("3. Try running as administrator")
        input("\nPress Enter to exit...")

