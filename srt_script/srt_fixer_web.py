#!/usr/bin/env python3
"""
SRT Timestamp Fixer - Web Application

A web-based version of the SRT timestamp fixer using Flask.
This allows the application to run in any web browser and can be
easily deployed to cloud platforms.

Requirements:
- Flask (pip install Flask)

Author: AI Assistant
Date: June 24, 2025
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import os
import re
import tempfile
import shutil
from pathlib import Path
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

class SRTProcessor:
    """Core SRT processing logic."""
    
    @staticmethod
    def analyze_timestamp_format(timestamp: str) -> dict:
        """Analyze timestamp format."""
        analysis = {
            'original': timestamp,
            'is_valid_srt': False,
            'has_hours': False,
            'format_detected': None,
            'needs_fixing': False
        }
        
        clean_timestamp = timestamp.strip()
        analysis['cleaned'] = clean_timestamp
        
        full_pattern = r'^(\d{2}):(\d{2}):(\d{2}),(\d{3})$'
        short_pattern = r'^(\d{1,2}):(\d{2}),(\d{3})$'
        
        if re.match(full_pattern, clean_timestamp):
            analysis['is_valid_srt'] = True
            analysis['has_hours'] = True
            analysis['format_detected'] = 'HH:MM:SS,mmm'
            analysis['needs_fixing'] = False
        elif re.match(short_pattern, clean_timestamp):
            analysis['has_hours'] = False
            analysis['format_detected'] = 'MM:SS,mmm'
            analysis['needs_fixing'] = True
        else:
            analysis['format_detected'] = 'unknown'
            analysis['needs_fixing'] = True
        
        return analysis
    
    @staticmethod
    def fix_timestamp_format(timestamp: str) -> str:
        """Fix timestamp format."""
        clean_timestamp = timestamp.strip()
        short_pattern = r'^(\d{1,2}):(\d{2}),(\d{3})$'
        match = re.match(short_pattern, clean_timestamp)
        
        if match:
            minutes, seconds, milliseconds = match.groups()
            fixed_timestamp = f"00:{minutes:0>2}:{seconds},{milliseconds}"
            return fixed_timestamp
        
        return clean_timestamp
    
    def find_and_analyze_timestamp_line(self, line: str) -> dict:
        """Analyze timestamp line."""
        result = {
            'original_line': line,
            'is_timestamp_line': False,
            'has_arrow': False,
            'left_timestamp': None,
            'right_timestamp': None,
            'left_analysis': None,
            'right_analysis': None,
            'needs_fixing': False,
            'fixed_line': None
        }
        
        if '-->' in line:
            result['has_arrow'] = True
            result['is_timestamp_line'] = True
            
            parts = line.split('-->')
            if len(parts) == 2:
                left_part = parts[0].strip()
                right_part = parts[1].strip()
                
                result['left_timestamp'] = left_part
                result['right_timestamp'] = right_part
                
                result['left_analysis'] = self.analyze_timestamp_format(left_part)
                result['right_analysis'] = self.analyze_timestamp_format(right_part)
                
                if result['left_analysis']['needs_fixing'] or result['right_analysis']['needs_fixing']:
                    result['needs_fixing'] = True
                    fixed_left = self.fix_timestamp_format(left_part)
                    fixed_right = self.fix_timestamp_format(right_part)
                    result['fixed_line'] = f"{fixed_left} --> {fixed_right}"
        
        elif re.search(r'\d{1,2}:\d{2},\d{3}\s+\d{1,2}:\d{2},\d{3}', line):
            result['is_timestamp_line'] = True
            result['has_arrow'] = False
            result['needs_fixing'] = True
            
            timestamp_pattern = r'(\d{1,2}:\d{2},\d{3})\s+(\d{1,2}:\d{2},\d{3})'
            match = re.search(timestamp_pattern, line)
            if match:
                left_part, right_part = match.groups()
                result['left_timestamp'] = left_part
                result['right_timestamp'] = right_part
                
                result['left_analysis'] = self.analyze_timestamp_format(left_part)
                result['right_analysis'] = self.analyze_timestamp_format(right_part)
                
                fixed_left = self.fix_timestamp_format(left_part)
                fixed_right = self.fix_timestamp_format(right_part)
                result['fixed_line'] = f"{fixed_left} --> {fixed_right}"
        
        return result
    
    def process_srt_file(self, input_file: str, output_file: str) -> dict:
        """Process SRT file and return statistics."""
        stats = {
            'total_lines': 0,
            'timestamp_lines_found': 0,
            'timestamp_lines_fixed': 0,
            'issues_found': [],
            'fixes_applied': []
        }
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        
        stats['total_lines'] = len(lines)
        processed_lines = []
        
        for line_num, line in enumerate(lines, 1):
            analysis = self.find_and_analyze_timestamp_line(line.rstrip('\n\r'))
            
            if analysis['is_timestamp_line']:
                stats['timestamp_lines_found'] += 1
                
                if analysis['needs_fixing']:
                    stats['timestamp_lines_fixed'] += 1
                    
                    issue_desc = f"Line {line_num}: '{analysis['original_line'].strip()}'"
                    if not analysis['has_arrow']:
                        issue_desc += " (missing arrow)"
                    if analysis['left_analysis'] and analysis['left_analysis']['needs_fixing']:
                        issue_desc += f" (left: {analysis['left_analysis']['format_detected']})"
                    if analysis['right_analysis'] and analysis['right_analysis']['needs_fixing']:
                        issue_desc += f" (right: {analysis['right_analysis']['format_detected']})"
                    
                    stats['issues_found'].append(issue_desc)
                    processed_lines.append(analysis['fixed_line'] + '\n')
                else:
                    processed_lines.append(line)
            else:
                processed_lines.append(line)
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(processed_lines)
        
        return stats

# Global processor instance
processor = SRTProcessor()

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing."""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())[:8]
            input_filename = f"{unique_id}_{filename}"
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
            file.save(input_path)
            
            # Generate output filename
            name, ext = os.path.splitext(filename)
            output_filename = f"{unique_id}_{name}_fixed{ext}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            # Process the file
            stats = processor.process_srt_file(input_path, output_path)
            
            # Clean up input file
            os.remove(input_path)
            
            return render_template('results.html', 
                                 stats=stats, 
                                 output_filename=output_filename,
                                 original_filename=filename)
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload SRT or TXT files.')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    """Download processed file."""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            flash('File not found')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}')
        return redirect(url_for('index'))

@app.route('/preview', methods=['POST'])
def preview_changes():
    """Preview changes without processing."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})
    
    file = request.files['file']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'})
    
    try:
        # Read file content
        content = file.read().decode('utf-8')
        lines = content.splitlines()
        
        issues = []
        for line_num, line in enumerate(lines, 1):
            analysis = processor.find_and_analyze_timestamp_line(line)
            
            if analysis['is_timestamp_line'] and analysis['needs_fixing']:
                issue = {
                    'line_number': line_num,
                    'original': analysis['original_line'].strip(),
                    'fixed': analysis['fixed_line'],
                    'issues': []
                }
                
                if not analysis['has_arrow']:
                    issue['issues'].append('missing arrow')
                if analysis['left_analysis'] and analysis['left_analysis']['needs_fixing']:
                    issue['issues'].append(f"left: {analysis['left_analysis']['format_detected']}")
                if analysis['right_analysis'] and analysis['right_analysis']['needs_fixing']:
                    issue['issues'].append(f"right: {analysis['right_analysis']['format_detected']}")
                
                issues.append(issue)
        
        return jsonify({
            'issues_count': len(issues),
            'issues': issues[:20]  # Limit to first 20 for preview
        })
        
    except Exception as e:
        return jsonify({'error': f'Error analyzing file: {str(e)}'})

def allowed_file(filename):
    """Check if file type is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'srt', 'txt'}

# Create templates directory and files
def create_templates():
    """Create HTML templates for the web app."""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Base template
    base_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}SRT Timestamp Fixer{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .drag-area {
            border: 2px dashed #ccc;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .drag-area.dragover {
            border-color: #007bff;
            background-color: #f8f9fa;
        }
        .footer {
            margin-top: 50px;
            padding: 20px 0;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
    
    <footer class="footer text-center text-muted">
        <div class="container">
            <small>SRT Timestamp Fixer - Convert malformed timestamps to proper SRT format</small>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>'''
    
    # Index template
    index_template = '''{% extends "base.html" %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h1 class="card-title mb-0">
                    <i class="fas fa-wrench"></i> SRT Timestamp Fixer
                </h1>
                <small>Fix malformed timestamps in SRT subtitle files</small>
            </div>
            <div class="card-body">
                {% with messages = get_flashed_messages() %}
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-warning alert-dismissible fade show" role="alert">
                                {{ message }}
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}
                
                <form action="/upload" method="post" enctype="multipart/form-data" id="uploadForm">
                    <div class="drag-area mb-3" id="dragArea">
                        <i class="fas fa-cloud-upload-alt fa-3x text-muted mb-3"></i>
                        <h5>Drag & Drop your SRT file here</h5>
                        <p class="text-muted">or click to browse</p>
                        <input type="file" name="file" accept=".srt,.txt" required class="d-none" id="fileInput">
                        <button type="button" class="btn btn-outline-primary" onclick="document.getElementById('fileInput').click()">
                            <i class="fas fa-folder-open"></i> Browse Files
                        </button>
                    </div>
                    
                    <div class="file-info d-none mb-3" id="fileInfo">
                        <div class="alert alert-info">
                            <i class="fas fa-file"></i> Selected: <span id="fileName"></span>
                            <small class="d-block text-muted">Size: <span id="fileSize"></span></small>
                        </div>
                    </div>
                    
                    <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                        <button type="button" class="btn btn-outline-secondary" id="previewBtn" disabled>
                            <i class="fas fa-eye"></i> Preview Changes
                        </button>
                        <button type="submit" class="btn btn-primary" id="submitBtn" disabled>
                            <i class="fas fa-magic"></i> Fix Timestamps
                        </button>
                    </div>
                </form>
                
                <div class="preview-results mt-4 d-none" id="previewResults">
                    <h5><i class="fas fa-search"></i> Preview Results</h5>
                    <div id="previewContent"></div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-question-circle"></i> What does this fix?</h5>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success"></i> Missing hours: <code>01:30,500</code> → <code>00:01:30,500</code></li>
                            <li><i class="fas fa-check text-success"></i> Missing arrows: <code>01:30,500  01:31,500</code> → <code>00:01:30,500 --> 00:01:31,500</code></li>
                            <li><i class="fas fa-check text-success"></i> Inconsistent formatting</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-shield-alt"></i> Safe & Secure</h5>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success"></i> Files processed locally</li>
                            <li><i class="fas fa-check text-success"></i> No data stored on server</li>
                            <li><i class="fas fa-check text-success"></i> Temporary files auto-deleted</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const dragArea = document.getElementById('dragArea');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const submitBtn = document.getElementById('submitBtn');
    const previewBtn = document.getElementById('previewBtn');
    const previewResults = document.getElementById('previewResults');
    const previewContent = document.getElementById('previewContent');
    
    // Drag and drop handlers
    dragArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        dragArea.classList.add('dragover');
    });
    
    dragArea.addEventListener('dragleave', () => {
        dragArea.classList.remove('dragover');
    });
    
    dragArea.addEventListener('drop', (e) => {
        e.preventDefault();
        dragArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect();
        }
    });
    
    fileInput.addEventListener('change', handleFileSelect);
    
    function handleFileSelect() {
        const file = fileInput.files[0];
        if (file) {
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            fileInfo.classList.remove('d-none');
            submitBtn.disabled = false;
            previewBtn.disabled = false;
        }
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Preview functionality
    previewBtn.addEventListener('click', function() {
        const file = fileInput.files[0];
        if (!file) return;
        
        const formData = new FormData();
        formData.append('file', file);
        
        previewBtn.disabled = true;
        previewBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        
        fetch('/preview', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            previewContent.innerHTML = generatePreviewHTML(data);
            previewResults.classList.remove('d-none');
        })
        .catch(error => {
            alert('Error: ' + error.message);
        })
        .finally(() => {
            previewBtn.disabled = false;
            previewBtn.innerHTML = '<i class="fas fa-eye"></i> Preview Changes';
        });
    });
    
    function generatePreviewHTML(data) {
        if (data.issues_count === 0) {
            return '<div class="alert alert-success"><i class="fas fa-check-circle"></i> No issues found! Your file is already properly formatted.</div>';
        }
        
        let html = `<div class="alert alert-info"><i class="fas fa-info-circle"></i> Found ${data.issues_count} timestamp issues that will be fixed:</div>`;
        html += '<div class="table-responsive"><table class="table table-sm"><thead><tr><th>Line</th><th>Original</th><th>Fixed</th><th>Issues</th></tr></thead><tbody>';
        
        data.issues.forEach(issue => {
            html += `<tr>
                <td>${issue.line_number}</td>
                <td><code>${issue.original}</code></td>
                <td><code class="text-success">${issue.fixed}</code></td>
                <td><small class="text-muted">${issue.issues.join(', ')}</small></td>
            </tr>`;
        });
        
        html += '</tbody></table></div>';
        
        if (data.issues_count > 20) {
            html += `<p><small class="text-muted">... and ${data.issues_count - 20} more issues</small></p>`;
        }
        
        return html;
    }
});
</script>
{% endblock %}'''

    # Results template
    results_template = '''{% extends "base.html" %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card shadow">
            <div class="card-header bg-success text-white">
                <h2 class="card-title mb-0">
                    <i class="fas fa-check-circle"></i> Processing Complete!
                </h2>
            </div>
            <div class="card-body">
                <div class="row mb-4">
                    <div class="col-md-3 text-center">
                        <div class="bg-light p-3 rounded">
                            <h3 class="text-primary">{{ stats.total_lines }}</h3>
                            <small class="text-muted">Total Lines</small>
                        </div>
                    </div>
                    <div class="col-md-3 text-center">
                        <div class="bg-light p-3 rounded">
                            <h3 class="text-info">{{ stats.timestamp_lines_found }}</h3>
                            <small class="text-muted">Timestamp Lines</small>
                        </div>
                    </div>
                    <div class="col-md-3 text-center">
                        <div class="bg-light p-3 rounded">
                            <h3 class="text-success">{{ stats.timestamp_lines_fixed }}</h3>
                            <small class="text-muted">Lines Fixed</small>
                        </div>
                    </div>
                    <div class="col-md-3 text-center">
                        <div class="bg-light p-3 rounded">
                            <h3 class="text-warning">{{ stats.issues_found|length }}</h3>
                            <small class="text-muted">Issues Found</small>
                        </div>
                    </div>
                </div>
                
                {% if stats.issues_found %}
                <div class="mb-4">
                    <h5><i class="fas fa-list"></i> Issues Fixed:</h5>
                    <div class="table-responsive">
                        <table class="table table-striped table-sm">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for issue in stats.issues_found[:10] %}
                                <tr>
                                    <td>{{ loop.index }}</td>
                                    <td><code>{{ issue }}</code></td>
                                </tr>
                                {% endfor %}
                                {% if stats.issues_found|length > 10 %}
                                <tr>
                                    <td colspan="2" class="text-muted text-center">
                                        ... and {{ stats.issues_found|length - 10 }} more issues
                                    </td>
                                </tr>
                                {% endif %}
                            </tbody>
                        </table>
                    </div>
                </div>
                {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> No issues were found in your file. It was already properly formatted!
                </div>
                {% endif %}
                
                <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                    <a href="/download/{{ output_filename }}" class="btn btn-success btn-lg">
                        <i class="fas fa-download"></i> Download Fixed File
                    </a>
                    <a href="/" class="btn btn-outline-primary">
                        <i class="fas fa-plus"></i> Process Another File
                    </a>
                </div>
                
                <div class="mt-3 text-center">
                    <small class="text-muted">
                        Original file: {{ original_filename }}<br>
                        Fixed file will be automatically deleted after download
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    # Write templates
    with open(os.path.join(templates_dir, 'base.html'), 'w') as f:
        f.write(base_template)
    
    with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
        f.write(index_template)
        
    with open(os.path.join(templates_dir, 'results.html'), 'w') as f:
        f.write(results_template)

if __name__ == "__main__":
    # Create templates on first run
    create_templates()
    
    print("SRT Timestamp Fixer Web App")
    print("=" * 40)
    print("Starting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
