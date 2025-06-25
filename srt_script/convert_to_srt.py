#!/usr/bin/env python3
"""
SRT Timestamp Fixer

This script finds and fixes malformed SRT timestamps by:
1. Finding lines containing "-->" (timestamp lines)
2. Checking timestamps on the left and right of "-->"
3. Fixing missing hours format (MM:SS,mmm -> HH:MM:SS,mmm)
4. Ensuring proper SRT format compliance

Author: AI Assistant
Date: June 19, 2025
"""

import re
import sys
from typing import Tuple, Optional

def analyze_timestamp_format(timestamp: str) -> dict:
    """
    Analyze a timestamp string and return its format information.
    
    Args:
        timestamp (str): The timestamp string to analyze
        
    Returns:
        dict: Analysis results with format information
    """
    analysis = {
        'original': timestamp,
        'is_valid_srt': False,
        'has_hours': False,
        'format_detected': None,
        'needs_fixing': False
    }
    
    # Clean up the timestamp (remove extra spaces)
    clean_timestamp = timestamp.strip()
    analysis['cleaned'] = clean_timestamp
    
    # Pattern for full SRT format: HH:MM:SS,mmm
    full_pattern = r'^(\d{2}):(\d{2}):(\d{2}),(\d{3})$'
    
    # Pattern for missing hours: MM:SS,mmm or M:SS,mmm
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

def fix_timestamp_format(timestamp: str) -> str:
    """
    Fix a malformed timestamp by adding missing hours if needed.
    
    Args:
        timestamp (str): The timestamp to fix
        
    Returns:
        str: The corrected timestamp
    """
    clean_timestamp = timestamp.strip()
    
    # Pattern for missing hours: MM:SS,mmm or M:SS,mmm
    short_pattern = r'^(\d{1,2}):(\d{2}),(\d{3})$'
    match = re.match(short_pattern, clean_timestamp)
    
    if match:
        minutes, seconds, milliseconds = match.groups()
        # Convert to proper format: 00:MM:SS,mmm
        fixed_timestamp = f"00:{minutes:0>2}:{seconds},{milliseconds}"
        return fixed_timestamp
    
    # If it's already in correct format or unknown format, return as is
    return clean_timestamp

def find_and_analyze_timestamp_line(line: str) -> dict:
    """
    Find and analyze a timestamp line containing "-->".
    
    Args:
        line (str): The line to analyze
        
    Returns:
        dict: Analysis results for the entire line
    """
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
    
    # Check if line contains arrow
    if '-->' in line:
        result['has_arrow'] = True
        result['is_timestamp_line'] = True
        
        # Split by arrow
        parts = line.split('-->')
        if len(parts) == 2:
            left_part = parts[0].strip()
            right_part = parts[1].strip()
            
            result['left_timestamp'] = left_part
            result['right_timestamp'] = right_part
            
            # Analyze both timestamps
            result['left_analysis'] = analyze_timestamp_format(left_part)
            result['right_analysis'] = analyze_timestamp_format(right_part)
            
            # Check if fixing is needed
            if result['left_analysis']['needs_fixing'] or result['right_analysis']['needs_fixing']:
                result['needs_fixing'] = True
                
                # Fix both timestamps
                fixed_left = fix_timestamp_format(left_part)
                fixed_right = fix_timestamp_format(right_part)
                result['fixed_line'] = f"{fixed_left} --> {fixed_right}"
    
    # Check for lines with timestamps but missing arrow (like "01:00,600  01:01,600")
    elif re.search(r'\d{1,2}:\d{2},\d{3}\s+\d{1,2}:\d{2},\d{3}', line):
        result['is_timestamp_line'] = True
        result['has_arrow'] = False
        result['needs_fixing'] = True
        
        # Extract timestamps using regex
        timestamp_pattern = r'(\d{1,2}:\d{2},\d{3})\s+(\d{1,2}:\d{2},\d{3})'
        match = re.search(timestamp_pattern, line)
        if match:
            left_part, right_part = match.groups()
            result['left_timestamp'] = left_part
            result['right_timestamp'] = right_part
            
            # Analyze both timestamps
            result['left_analysis'] = analyze_timestamp_format(left_part)
            result['right_analysis'] = analyze_timestamp_format(right_part)
            
            # Fix both timestamps and add arrow
            fixed_left = fix_timestamp_format(left_part)
            fixed_right = fix_timestamp_format(right_part)
            result['fixed_line'] = f"{fixed_left} --> {fixed_right}"
    
    return result

def process_srt_file(input_file: str, output_file: str) -> dict:
    """
    Process an SRT file and fix timestamp formatting issues.
    
    Args:
        input_file (str): Path to input SRT file
        output_file (str): Path to output SRT file
        
    Returns:
        dict: Processing statistics
    """
    stats = {
        'total_lines': 0,
        'timestamp_lines_found': 0,
        'timestamp_lines_fixed': 0,
        'issues_found': [],
        'fixes_applied': []
    }
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        
        stats['total_lines'] = len(lines)
        processed_lines = []
        
        for line_num, line in enumerate(lines, 1):
            # Analyze the line
            analysis = find_and_analyze_timestamp_line(line.rstrip('\n\r'))
            
            if analysis['is_timestamp_line']:
                stats['timestamp_lines_found'] += 1
                
                if analysis['needs_fixing']:
                    stats['timestamp_lines_fixed'] += 1
                    
                    # Record the issue
                    issue_desc = f"Line {line_num}: '{analysis['original_line'].strip()}'"
                    if not analysis['has_arrow']:
                        issue_desc += " (missing arrow)"
                    if analysis['left_analysis'] and analysis['left_analysis']['needs_fixing']:
                        issue_desc += f" (left timestamp: {analysis['left_analysis']['format_detected']})"
                    if analysis['right_analysis'] and analysis['right_analysis']['needs_fixing']:
                        issue_desc += f" (right timestamp: {analysis['right_analysis']['format_detected']})"
                    
                    stats['issues_found'].append(issue_desc)
                    
                    # Record the fix
                    fix_desc = f"Line {line_num}: Fixed to '{analysis['fixed_line']}'"
                    stats['fixes_applied'].append(fix_desc)
                    
                    # Use the fixed line
                    processed_lines.append(analysis['fixed_line'] + '\n')
                else:
                    # Line is fine, keep as is
                    processed_lines.append(line)
            else:
                # Not a timestamp line, keep as is
                processed_lines.append(line)
        
        # Write the processed file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(processed_lines)
        
        return stats
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

def main():
    """Main function to fix SRT timestamp formatting issues."""
    
    print("SRT Timestamp Fixer")
    print("=" * 50)
    print()
    
    # Process the input file and create a fixed output
    input_file = "input.txt"
    output_file = "output.srt"
    backup_file = "input_backup.txt"
    
    try:
        # Create backup of input
        import shutil
        shutil.copy2(input_file, backup_file)
        print(f"Created backup: {backup_file}")
        
        # Process the file
        stats = process_srt_file(input_file, output_file)
        
        if stats:
            print(f"\nProcessing Results:")
            print(f"Total lines processed: {stats['total_lines']}")
            print(f"Timestamp lines found: {stats['timestamp_lines_found']}")
            print(f"Timestamp lines fixed: {stats['timestamp_lines_fixed']}")
            
            if stats['issues_found']:
                print(f"\nIssues found and fixed:")
                for issue in stats['issues_found'][:10]:  # Show first 10
                    print(f"  {issue}")
                if len(stats['issues_found']) > 10:
                    print(f"  ... and {len(stats['issues_found']) - 10} more")
            
            print(f"\nFixed SRT file created: {output_file}")
        else:
            print("Failed to process the file.")
            
    except FileNotFoundError:
        print(f"Error: {input_file} not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
