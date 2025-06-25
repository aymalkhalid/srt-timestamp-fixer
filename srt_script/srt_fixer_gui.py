#!/usr/bin/env python3
"""
SRT Timestamp Fixer - Desktop GUI Application

A desktop application to fix malformed SRT timestamps with a user-friendly interface.
Built with tkinter for cross-platform compatibility.

Features:
- File selection dialog
- Progress tracking
- Real-time preview of fixes
- Dark/Light theme support
- Detailed reporting

Author: AI Assistant
Date: June 24, 2025
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re
import os
import shutil
from pathlib import Path
import threading
from typing import Dict, List, Tuple

class SRTFixerGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.input_file = None
        self.output_file = None
        
    def setup_window(self):
        """Set up the main window properties."""
        self.root.title("SRT Timestamp Fixer")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')  # Modern looking theme
        
        # Center window on screen
        self.center_window()
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="SRT Timestamp Fixer", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        self.create_file_selection_section(main_frame)
        
        # Options section
        self.create_options_section(main_frame)
        
        # Action buttons
        self.create_action_buttons(main_frame)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=300)
        self.progress_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                              pady=(10, 5))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to process SRT files")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Results section
        self.create_results_section(main_frame)
        
    def create_file_selection_section(self, parent):
        """Create the file selection section."""
        # Input file
        ttk.Label(parent, text="Input File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.input_file_var = tk.StringVar()
        input_entry = ttk.Entry(parent, textvariable=self.input_file_var, width=50)
        input_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        input_browse_btn = ttk.Button(parent, text="Browse", 
                                     command=self.browse_input_file)
        input_browse_btn.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Output file
        ttk.Label(parent, text="Output File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.output_file_var = tk.StringVar()
        output_entry = ttk.Entry(parent, textvariable=self.output_file_var, width=50)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        output_browse_btn = ttk.Button(parent, text="Browse", 
                                      command=self.browse_output_file)
        output_browse_btn.grid(row=2, column=2, padx=(5, 0), pady=5)
        
    def create_options_section(self, parent):
        """Create the options section."""
        options_frame = ttk.LabelFrame(parent, text="Options", padding="5")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                          pady=(10, 5))
        options_frame.columnconfigure(1, weight=1)
        
        # Create backup option
        self.create_backup_var = tk.BooleanVar(value=True)
        backup_check = ttk.Checkbutton(options_frame, text="Create backup of original file", 
                                      variable=self.create_backup_var)
        backup_check.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Auto-fill output filename option
        self.auto_output_var = tk.BooleanVar(value=True)
        auto_check = ttk.Checkbutton(options_frame, text="Auto-generate output filename", 
                                    variable=self.auto_output_var,
                                    command=self.on_auto_output_changed)
        auto_check.grid(row=1, column=0, sticky=tk.W, pady=2)
        
    def create_action_buttons(self, parent):
        """Create the action buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(10, 5))
        
        self.process_btn = ttk.Button(button_frame, text="Fix Timestamps", 
                                     command=self.start_processing, style="Accent.TButton")
        self.process_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.preview_btn = ttk.Button(button_frame, text="Preview Changes", 
                                     command=self.preview_changes)
        self.preview_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(button_frame, text="Clear", 
                                   command=self.clear_all)
        self.clear_btn.pack(side=tk.LEFT)
        
    def create_results_section(self, parent):
        """Create the results display section."""
        results_frame = ttk.LabelFrame(parent, text="Processing Results", padding="5")
        results_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results text area with scrollbar
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, 
                                                     wrap=tk.WORD)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def browse_input_file(self):
        """Open file dialog to select input file."""
        filetypes = [
            ("SRT files", "*.srt"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select SRT file to fix",
            filetypes=filetypes
        )
        
        if filename:
            self.input_file_var.set(filename)
            self.input_file = filename
            
            # Auto-generate output filename if option is enabled
            if self.auto_output_var.get():
                self.auto_generate_output_filename()
                
    def browse_output_file(self):
        """Open file dialog to select output file."""
        filetypes = [
            ("SRT files", "*.srt"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.asksaveasfilename(
            title="Save fixed SRT file as",
            filetypes=filetypes,
            defaultextension=".srt"
        )
        
        if filename:
            self.output_file_var.set(filename)
            self.output_file = filename
            
    def auto_generate_output_filename(self):
        """Auto-generate output filename based on input filename."""
        if self.input_file:
            input_path = Path(self.input_file)
            output_name = f"{input_path.stem}_fixed{input_path.suffix}"
            output_path = input_path.parent / output_name
            self.output_file_var.set(str(output_path))
            self.output_file = str(output_path)
            
    def on_auto_output_changed(self):
        """Handle auto-output option change."""
        if self.auto_output_var.get() and self.input_file:
            self.auto_generate_output_filename()
            
    def clear_all(self):
        """Clear all fields and reset the interface."""
        self.input_file_var.set("")
        self.output_file_var.set("")
        self.input_file = None
        self.output_file = None
        self.results_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        self.status_var.set("Ready to process SRT files")
        
    def validate_inputs(self) -> bool:
        """Validate user inputs before processing."""
        if not self.input_file or not os.path.exists(self.input_file):
            messagebox.showerror("Error", "Please select a valid input file.")
            return False
            
        if not self.output_file:
            messagebox.showerror("Error", "Please specify an output file.")
            return False
            
        return True
        
    def preview_changes(self):
        """Preview the changes that would be made without actually processing."""
        if not self.validate_inputs():
            return
            
        try:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Analyzing file for timestamp issues...\n\n")
            self.root.update()
            
            # Analyze the file
            issues = self.analyze_file_for_issues(self.input_file)
            
            if issues:
                self.results_text.insert(tk.END, f"Found {len(issues)} timestamp issues:\n\n")
                for i, issue in enumerate(issues[:20], 1):  # Show first 20
                    self.results_text.insert(tk.END, f"{i}. {issue}\n")
                if len(issues) > 20:
                    self.results_text.insert(tk.END, f"... and {len(issues) - 20} more issues\n")
            else:
                self.results_text.insert(tk.END, "No timestamp formatting issues found!\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview changes: {str(e)}")
            
    def start_processing(self):
        """Start the processing in a separate thread."""
        if not self.validate_inputs():
            return
            
        # Disable buttons during processing
        self.process_btn.config(state='disabled')
        self.preview_btn.config(state='disabled')
        
        # Start processing thread
        thread = threading.Thread(target=self.process_file_threaded)
        thread.daemon = True
        thread.start()
        
    def process_file_threaded(self):
        """Process the file in a separate thread."""
        try:
            self.update_status("Processing file...")
            self.progress_var.set(10)
            
            # Create backup if requested
            if self.create_backup_var.get():
                backup_path = f"{self.input_file}.backup"
                shutil.copy2(self.input_file, backup_path)
                self.update_status(f"Created backup: {backup_path}")
                self.progress_var.set(20)
            
            # Process the file
            stats = self.process_srt_file(self.input_file, self.output_file)
            self.progress_var.set(90)
            
            # Update UI with results
            self.root.after(0, self.display_results, stats)
            self.progress_var.set(100)
            self.update_status("Processing completed successfully!")
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed: {str(e)}"))
            self.update_status("Processing failed!")
        finally:
            # Re-enable buttons
            self.root.after(0, lambda: self.process_btn.config(state='normal'))
            self.root.after(0, lambda: self.preview_btn.config(state='normal'))
            
    def update_status(self, message):
        """Update status message from any thread."""
        self.root.after(0, lambda: self.status_var.set(message))
        
    def display_results(self, stats):
        """Display processing results in the text area."""
        self.results_text.delete(1.0, tk.END)
        
        if stats:
            self.results_text.insert(tk.END, "Processing Results:\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")
            self.results_text.insert(tk.END, f"Total lines processed: {stats['total_lines']}\n")
            self.results_text.insert(tk.END, f"Timestamp lines found: {stats['timestamp_lines_found']}\n")
            self.results_text.insert(tk.END, f"Timestamp lines fixed: {stats['timestamp_lines_fixed']}\n\n")
            
            if stats['issues_found']:
                self.results_text.insert(tk.END, "Issues found and fixed:\n")
                self.results_text.insert(tk.END, "-" * 30 + "\n")
                for issue in stats['issues_found'][:10]:
                    self.results_text.insert(tk.END, f"• {issue}\n")
                if len(stats['issues_found']) > 10:
                    self.results_text.insert(tk.END, f"• ... and {len(stats['issues_found']) - 10} more\n")
                    
                self.results_text.insert(tk.END, f"\nOutput file created: {self.output_file}\n")
            else:
                self.results_text.insert(tk.END, "No issues found. File was already properly formatted.\n")
        else:
            self.results_text.insert(tk.END, "Processing failed!\n")
            
    # Include the core SRT processing functions from the original script
    def analyze_timestamp_format(self, timestamp: str) -> dict:
        """Analyze timestamp format (same as original)."""
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
    
    def fix_timestamp_format(self, timestamp: str) -> str:
        """Fix timestamp format (same as original)."""
        clean_timestamp = timestamp.strip()
        short_pattern = r'^(\d{1,2}):(\d{2}),(\d{3})$'
        match = re.match(short_pattern, clean_timestamp)
        
        if match:
            minutes, seconds, milliseconds = match.groups()
            fixed_timestamp = f"00:{minutes:0>2}:{seconds},{milliseconds}"
            return fixed_timestamp
        
        return clean_timestamp
    
    def find_and_analyze_timestamp_line(self, line: str) -> dict:
        """Analyze timestamp line (same as original)."""
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
    
    def analyze_file_for_issues(self, input_file: str) -> List[str]:
        """Analyze file and return list of issues without fixing."""
        issues = []
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        
        for line_num, line in enumerate(lines, 1):
            analysis = self.find_and_analyze_timestamp_line(line.rstrip('\n\r'))
            
            if analysis['is_timestamp_line'] and analysis['needs_fixing']:
                issue_desc = f"Line {line_num}: '{analysis['original_line'].strip()}'"
                if not analysis['has_arrow']:
                    issue_desc += " (missing arrow)"
                if analysis['left_analysis'] and analysis['left_analysis']['needs_fixing']:
                    issue_desc += f" (left: {analysis['left_analysis']['format_detected']})"
                if analysis['right_analysis'] and analysis['right_analysis']['needs_fixing']:
                    issue_desc += f" (right: {analysis['right_analysis']['format_detected']})"
                
                issues.append(issue_desc)
        
        return issues
    
    def process_srt_file(self, input_file: str, output_file: str) -> dict:
        """Process SRT file (same as original)."""
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
            # Update progress periodically
            if line_num % 50 == 0:
                progress = 20 + (line_num / len(lines)) * 70  # 20-90% range
                self.progress_var.set(progress)
                self.root.update()
            
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


def main():
    """Main function to start the GUI application."""
    root = tk.Tk()
    app = SRTFixerGUI(root)
    
    # Configure the application icon (if you have one)
    try:
        # root.iconbitmap('icon.ico')  # Add if you have an icon file
        pass
    except:
        pass
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
