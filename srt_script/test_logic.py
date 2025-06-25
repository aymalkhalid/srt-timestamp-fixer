#!/usr/bin/env python3

import re

def analyze_timestamp_format(timestamp: str) -> dict:
    """Analyze a timestamp string and return its format information."""
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
    """Fix a malformed timestamp by adding missing hours if needed."""
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

# Test the functions
if __name__ == "__main__":
    test_cases = [
        '01:00,900',
        '01:01,800', 
        '01:02,200',
        '00:01:00,500',
        '1:30,500'
    ]
    
    print("Testing timestamp analysis and fixing:")
    print("=" * 50)
    
    for ts in test_cases:
        analysis = analyze_timestamp_format(ts)
        fixed = fix_timestamp_format(ts)
        print(f"Input: '{ts}'")
        print(f"  Format: {analysis['format_detected']}")
        print(f"  Needs fixing: {analysis['needs_fixing']}")
        print(f"  Fixed: '{fixed}'")
        print()
