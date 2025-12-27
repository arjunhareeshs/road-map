"""
Flask Web Application for LLM Roadmap Generator
"""
import os
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from core.generator import generate_roadmap
from renderer.flowchart import render_mermaid

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate roadmap API endpoint"""
    try:
        data = request.get_json()
        domain = data.get('domain', '').strip()
        level = data.get('level', 'Beginner').strip()
        
        if not domain:
            return jsonify({'error': 'Domain is required'}), 400
        
        # Generate roadmap
        roadmap_data = generate_roadmap(domain, level)
        
        # Generate Mermaid diagram
        mermaid_code = render_mermaid(roadmap_data)
        
        return jsonify({
            'success': True,
            'roadmap': roadmap_data,
            'mermaid': mermaid_code
        })
        
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Failed to parse LLM response: {str(e)}'}), 500
    except ValueError as e:
        return jsonify({'error': f'Validation error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'provider': os.getenv('LLM_PROVIDER', 'ollama')})


if __name__ == '__main__':
    print("🚀 Starting LLM Roadmap Generator Web App...")
    print("📍 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
