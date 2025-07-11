#!/usr/bin/env python3
"""
SRT Timestamp Fixer - Web Application

A web-based version of the SRT timestamp fixer using Flask.
This allows the application to run in any web browser and can be
easily deployed to cloud platforms.

Requirements:
- Flask (pip install Flask)

Author: SRT Timestamp Fixer Project
Date: July 9, 2025
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

if __name__ == "__main__":
    print("SRT Timestamp Fixer Web App")
    print("=" * 40)
    print("Starting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)
