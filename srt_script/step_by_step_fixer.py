#!/usr/bin/env python3
"""
SRT Timestamp Fixer - Step by Step Implementation

This script demonstrates the logic step by step:
1. Find lines containing "-->"
2. Check timestamps on left and right of "-->"
3. Fix missing hours format (MM:SS,mmm -> HH:MM:SS,mmm)
4. Handle missing arrows
"""

import re

def step1_find_arrow_lines(content):
    """Step 1: Find all lines containing '-->'"""
    print("STEP 1: Finding lines with '-->' arrows")
    print("=" * 50)
    
    lines = content.split('\n')
    arrow_lines = []
    
    for i, line in enumerate(lines):
        if '-->' in line:
            arrow_lines.append((i + 1, line.strip()))
            print(f"Line {i + 1}: {line.strip()}")
    
    print(f"\nFound {len(arrow_lines)} lines with arrows")
    return arrow_lines

def step2_analyze_timestamps(arrow_lines):
    """Step 2: Analyze each timestamp on left and right of '-->'"""
    print("\nSTEP 2: Analyzing timestamps")
    print("=" * 50)
    
    analyzed_lines = []
    
    for line_num, line in arrow_lines:
        print(f"\nAnalyzing Line {line_num}: '{line}'")
        
        # Split by arrow
        if '-->' in line:
            left_part, right_part = line.split('-->')
            left_timestamp = left_part.strip()
            right_timestamp = right_part.strip()
            
            print(f"  Left timestamp:  '{left_timestamp}'")
            print(f"  Right timestamp: '{right_timestamp}'")
            
            # Analyze left timestamp
            left_analysis = analyze_single_timestamp(left_timestamp)
            right_analysis = analyze_single_timestamp(right_timestamp)
            
            print(f"  Left analysis:  {left_analysis}")
            print(f"  Right analysis: {right_analysis}")
            
            analyzed_lines.append({
                'line_num': line_num,
                'original': line,
                'left_timestamp': left_timestamp,
                'right_timestamp': right_timestamp,
                'left_analysis': left_analysis,
                'right_analysis': right_analysis
            })
    
    return analyzed_lines

def analyze_single_timestamp(timestamp):
    """Analyze a single timestamp and determine its format"""
    timestamp = timestamp.strip()
    
    # Pattern for full SRT format: HH:MM:SS,mmm
    full_pattern = r'^(\d{2}):(\d{2}):(\d{2}),(\d{3})$'
    
    # Pattern for missing hours: MM:SS,mmm or M:SS,mmm  
    short_pattern = r'^(\d{1,2}):(\d{2}),(\d{3})$'
    
    if re.match(full_pattern, timestamp):
        return {
            'format': 'HH:MM:SS,mmm',
            'valid': True,
            'needs_fixing': False,
            'has_hours': True
        }
    elif re.match(short_pattern, timestamp):
        return {
            'format': 'MM:SS,mmm', 
            'valid': False,
            'needs_fixing': True,
            'has_hours': False
        }
    else:
        return {
            'format': 'unknown',
            'valid': False,
            'needs_fixing': True,
            'has_hours': False
        }

def step3_fix_timestamps(analyzed_lines):
    """Step 3: Fix malformed timestamps"""
    print("\nSTEP 3: Fixing malformed timestamps")
    print("=" * 50)
    
    fixed_lines = []
    
    for item in analyzed_lines:
        print(f"\nFixing Line {item['line_num']}")
        print(f"  Original: '{item['original']}'")
        
        # Fix left timestamp if needed
        if item['left_analysis']['needs_fixing']:
            fixed_left = fix_single_timestamp(item['left_timestamp'])
            print(f"  Left fixed: '{item['left_timestamp']}' -> '{fixed_left}'")
        else:
            fixed_left = item['left_timestamp']
            print(f"  Left OK: '{fixed_left}'")
        
        # Fix right timestamp if needed
        if item['right_analysis']['needs_fixing']:
            fixed_right = fix_single_timestamp(item['right_timestamp'])
            print(f"  Right fixed: '{item['right_timestamp']}' -> '{fixed_right}'")
        else:
            fixed_right = item['right_timestamp']
            print(f"  Right OK: '{fixed_right}'")
        
        # Create fixed line
        fixed_line = f"{fixed_left} --> {fixed_right}"
        print(f"  Final: '{fixed_line}'")
        
        fixed_lines.append({
            'line_num': item['line_num'],
            'original': item['original'],
            'fixed': fixed_line
        })
    
    return fixed_lines

def fix_single_timestamp(timestamp):
    """Fix a single timestamp by adding missing hours"""
    timestamp = timestamp.strip()
    
    # Pattern for missing hours: MM:SS,mmm or M:SS,mmm
    short_pattern = r'^(\d{1,2}):(\d{2}),(\d{3})$'
    match = re.match(short_pattern, timestamp)
    
    if match:
        minutes, seconds, milliseconds = match.groups()
        # Convert to proper format: 00:MM:SS,mmm
        fixed_timestamp = f"00:{minutes:0>2}:{seconds},{milliseconds}"
        return fixed_timestamp
    
    return timestamp

def step4_apply_fixes(content, fixed_lines):
    """Step 4: Apply fixes to the content"""
    print("\nSTEP 4: Applying fixes to content")
    print("=" * 50)
    
    lines = content.split('\n')
    
    # Apply fixes
    for fix in fixed_lines:
        line_index = fix['line_num'] - 1  # Convert to 0-based index
        if line_index < len(lines):
            old_line = lines[line_index].strip()
            if old_line == fix['original']:
                lines[line_index] = fix['fixed']
                print(f"Line {fix['line_num']}: Applied fix")
            else:
                print(f"Line {fix['line_num']}: WARNING - Line content doesn't match expected")
    
    return '\n'.join(lines)

def main():
    """Main function to demonstrate the step-by-step process"""
    print("SRT Timestamp Fixer - Step by Step")
    print("=" * 60)
    
    # Read the input file
    try:
        with open('input.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"Read input file: {len(content)} characters")
    except FileNotFoundError:
        print("Error: input.txt not found")
        return
    
    # Step 1: Find arrow lines
    arrow_lines = step1_find_arrow_lines(content)
    
    # Step 2: Analyze timestamps
    analyzed_lines = step2_analyze_timestamps(arrow_lines)
    
    # Step 3: Fix timestamps
    fixed_lines = step3_fix_timestamps(analyzed_lines)
    
    # Step 4: Apply fixes
    fixed_content = step4_apply_fixes(content, fixed_lines)
    
    # Write output
    with open('output_fixed.srt', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"\nFixed content written to: output_fixed.srt")
    
    # Show summary
    print(f"\nSUMMARY:")
    print(f"Lines processed: {len(arrow_lines)}")
    print(f"Lines fixed: {len([f for f in fixed_lines if f['original'] != f['fixed']])}")

if __name__ == "__main__":
    main()
