#!/usr/bin/env python3
"""
SRT Timestamp Fixer - Modern Desktop App with CustomTkinter

A modern, beautiful desktop application using CustomTkinter for fixing SRT timestamps.
Features dark/light themes, modern UI components, and smooth animations.

Requirements:
- customtkinter (pip install customtkinter)
- Pillow (pip install Pillow)

Author: AI Assistant
Date: June 24, 2025
"""

try:
    import customtkinter as ctk
    from tkinter import filedialog, messagebox
    import tkinter as tk
except ImportError as e:
    print("CustomTkinter not found. Install with: pip install customtkinter")
    print(f"Error details: {e}")
    exit(1)

import re
import os
import shutil
from pathlib import Path
import threading
from typing import Dict, List

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class ModernSRTFixerGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.setup_window()
        self.create_widgets()
        self.input_file = None
        self.output_file = None
        
    def setup_window(self):
        """Set up the main window properties."""
        self.root.title("SRT Timestamp Fixer")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        
        # Center window
        self.center_window()
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = 900
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        
        # Title section
        self.create_title_section(main_frame)
        
        # File selection section
        self.create_file_selection_section(main_frame)
        
        # Options section
        self.create_options_section(main_frame)
        
        # Action buttons section
        self.create_action_section(main_frame)
        
        # Results section
        self.create_results_section(main_frame)
        
    def create_title_section(self, parent):
        """Create the title section with theme toggle."""
        title_frame = ctk.CTkFrame(parent, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(1, weight=1)
        
        # Main title
        title_label = ctk.CTkLabel(title_frame, text="SRT Timestamp Fixer", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(title_frame, 
                                     text="Fix malformed timestamps in SRT subtitle files",
                                     font=ctk.CTkFont(size=14),
                                     text_color=("gray60", "gray40"))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Theme toggle
        self.theme_switch = ctk.CTkSwitch(title_frame, text="Dark Mode", 
                                         command=self.toggle_theme,
                                         font=ctk.CTkFont(size=12))
        self.theme_switch.grid(row=2, column=1, sticky="e", pady=5)
        self.theme_switch.select()  # Start in dark mode
        
    def create_file_selection_section(self, parent):
        """Create the file selection section."""
        file_frame = ctk.CTkFrame(parent)
        file_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        file_frame.grid_columnconfigure(1, weight=1)
        
        # Section title
        ctk.CTkLabel(file_frame, text="File Selection", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, columnspan=3, pady=(15, 10), sticky="w", padx=15)
        
        # Input file
        ctk.CTkLabel(file_frame, text="Input File:").grid(
            row=1, column=0, sticky="w", padx=15, pady=5)
        
        self.input_entry = ctk.CTkEntry(file_frame, placeholder_text="Select SRT file to fix...")
        self.input_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        self.input_browse_btn = ctk.CTkButton(file_frame, text="Browse", width=100,
                                             command=self.browse_input_file)
        self.input_browse_btn.grid(row=1, column=2, padx=(0, 15), pady=5)
        
        # Output file
        ctk.CTkLabel(file_frame, text="Output File:").grid(
            row=2, column=0, sticky="w", padx=15, pady=5)
        
        self.output_entry = ctk.CTkEntry(file_frame, placeholder_text="Output file will be auto-generated...")
        self.output_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        self.output_browse_btn = ctk.CTkButton(file_frame, text="Browse", width=100,
                                              command=self.browse_output_file)
        self.output_browse_btn.grid(row=2, column=2, padx=(0, 15), pady=(5, 15))
        
    def create_options_section(self, parent):
        """Create the options section."""
        options_frame = ctk.CTkFrame(parent)
        options_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        # Section title
        ctk.CTkLabel(options_frame, text="Options", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(15, 10), sticky="w", padx=15)
        
        # Create backup option
        self.create_backup_var = ctk.BooleanVar(value=True)
        self.backup_check = ctk.CTkCheckBox(options_frame, text="Create backup of original file",
                                           variable=self.create_backup_var)
        self.backup_check.grid(row=1, column=0, sticky="w", padx=15, pady=5)
        
        # Auto-fill output filename option
        self.auto_output_var = ctk.BooleanVar(value=True)
        self.auto_check = ctk.CTkCheckBox(options_frame, text="Auto-generate output filename",
                                         variable=self.auto_output_var,
                                         command=self.on_auto_output_changed)
        self.auto_check.grid(row=2, column=0, sticky="w", padx=15, pady=(5, 15))
        
    def create_action_section(self, parent):
        """Create the action buttons and progress section."""
        action_frame = ctk.CTkFrame(parent)
        action_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        action_frame.grid_columnconfigure(0, weight=1)
        
        # Buttons container
        button_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        button_frame.grid(row=0, column=0, pady=15)
        
        self.process_btn = ctk.CTkButton(button_frame, text="🔧 Fix Timestamps", 
                                        command=self.start_processing,
                                        font=ctk.CTkFont(size=14, weight="bold"),
                                        height=40, width=150)
        self.process_btn.grid(row=0, column=0, padx=10)
        
        self.preview_btn = ctk.CTkButton(button_frame, text="👁 Preview Changes", 
                                        command=self.preview_changes,
                                        font=ctk.CTkFont(size=14),
                                        height=40, width=150,
                                        fg_color="transparent",
                                        border_width=2)
        self.preview_btn.grid(row=0, column=1, padx=10)
        
        self.clear_btn = ctk.CTkButton(button_frame, text="🗑 Clear", 
                                      command=self.clear_all,
                                      font=ctk.CTkFont(size=14),
                                      height=40, width=100,
                                      fg_color="transparent",
                                      border_width=2,
                                      text_color=("gray60", "gray40"))
        self.clear_btn.grid(row=0, column=2, padx=10)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(action_frame, width=400, height=20)
        self.progress_bar.grid(row=1, column=0, pady=(10, 5))
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(action_frame, text="Ready to process SRT files",
                                        font=ctk.CTkFont(size=12))
        self.status_label.grid(row=2, column=0, pady=(5, 15))
        
    def create_results_section(self, parent):
        """Create the results display section."""
        results_frame = ctk.CTkFrame(parent)
        results_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=(10, 20))
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        # Section title
        ctk.CTkLabel(results_frame, text="Processing Results", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, pady=(15, 10), sticky="w", padx=15)
        
        # Results text area
        self.results_text = ctk.CTkTextbox(results_frame, wrap="word", 
                                          font=ctk.CTkFont(family="Consolas", size=12))
        self.results_text.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
            
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
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)
            self.input_file = filename
            
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
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)
            self.output_file = filename
            
    def auto_generate_output_filename(self):
        """Auto-generate output filename based on input filename."""
        if self.input_file:
            input_path = Path(self.input_file)
            output_name = f"{input_path.stem}_fixed{input_path.suffix}"
            output_path = input_path.parent / output_name
            
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, str(output_path))
            self.output_file = str(output_path)
            
    def on_auto_output_changed(self):
        """Handle auto-output option change."""
        if self.auto_output_var.get() and self.input_file:
            self.auto_generate_output_filename()
            
    def clear_all(self):
        """Clear all fields and reset the interface."""
        self.input_entry.delete(0, tk.END)
        self.output_entry.delete(0, tk.END)
        self.input_file = None
        self.output_file = None
        self.results_text.delete("1.0", tk.END)
        self.progress_bar.set(0)
        self.status_label.configure(text="Ready to process SRT files")
        
    def validate_inputs(self) -> bool:
        """Validate user inputs before processing."""
        self.input_file = self.input_entry.get().strip()
        self.output_file = self.output_entry.get().strip()
        
        if not self.input_file or not os.path.exists(self.input_file):
            messagebox.showerror("Error", "Please select a valid input file.")
            return False
            
        if not self.output_file:
            messagebox.showerror("Error", "Please specify an output file.")
            return False
            
        return True
        
    def preview_changes(self):
        """Preview the changes that would be made."""
        if not self.validate_inputs():
            return
            
        try:
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert("1.0", "🔍 Analyzing file for timestamp issues...\n\n")
            self.root.update()
            
            issues = self.analyze_file_for_issues(self.input_file)
            
            if issues:
                self.results_text.insert(tk.END, f"📋 Found {len(issues)} timestamp issues:\n\n")
                for i, issue in enumerate(issues[:15], 1):
                    self.results_text.insert(tk.END, f"{i:2d}. {issue}\n")
                if len(issues) > 15:
                    self.results_text.insert(tk.END, f"    ... and {len(issues) - 15} more issues\n")
            else:
                self.results_text.insert(tk.END, "✅ No timestamp formatting issues found!\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview changes: {str(e)}")
            
    def start_processing(self):
        """Start the processing in a separate thread."""
        if not self.validate_inputs():
            return
            
        # Disable buttons during processing
        self.process_btn.configure(state="disabled")
        self.preview_btn.configure(state="disabled")
        
        # Start processing thread
        thread = threading.Thread(target=self.process_file_threaded)
        thread.daemon = True
        thread.start()
        
    def process_file_threaded(self):
        """Process the file in a separate thread."""
        try:
            self.update_status("🔧 Processing file...")
            self.update_progress(0.1)
            
            # Create backup if requested
            if self.create_backup_var.get():
                backup_path = f"{self.input_file}.backup"
                shutil.copy2(self.input_file, backup_path)
                self.update_status(f"💾 Created backup: {os.path.basename(backup_path)}")
                self.update_progress(0.2)
            
            # Process the file
            stats = self.process_srt_file(self.input_file, self.output_file)
            self.update_progress(0.9)
            
            # Update UI with results
            self.root.after(0, self.display_results, stats)
            self.update_progress(1.0)
            self.update_status("✅ Processing completed successfully!")
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed: {str(e)}"))
            self.update_status("❌ Processing failed!")
        finally:
            # Re-enable buttons
            self.root.after(0, lambda: self.process_btn.configure(state="normal"))
            self.root.after(0, lambda: self.preview_btn.configure(state="normal"))
            
    def update_status(self, message):
        """Update status message from any thread."""
        self.root.after(0, lambda: self.status_label.configure(text=message))
        
    def update_progress(self, value):
        """Update progress bar from any thread."""
        self.root.after(0, lambda: self.progress_bar.set(value))
        
    def display_results(self, stats):
        """Display processing results."""
        self.results_text.delete("1.0", tk.END)
        
        if stats:
            self.results_text.insert("1.0", "📊 Processing Results:\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")
            self.results_text.insert(tk.END, f"📄 Total lines processed: {stats['total_lines']}\n")
            self.results_text.insert(tk.END, f"⏱️  Timestamp lines found: {stats['timestamp_lines_found']}\n")
            self.results_text.insert(tk.END, f"🔧 Timestamp lines fixed: {stats['timestamp_lines_fixed']}\n\n")
            
            if stats['issues_found']:
                self.results_text.insert(tk.END, "🔍 Issues found and fixed:\n")
                self.results_text.insert(tk.END, "-" * 40 + "\n")
                for issue in stats['issues_found'][:10]:
                    self.results_text.insert(tk.END, f"• {issue}\n")
                if len(stats['issues_found']) > 10:
                    self.results_text.insert(tk.END, f"• ... and {len(stats['issues_found']) - 10} more\n")
                    
                self.results_text.insert(tk.END, f"\n✅ Output file created: {os.path.basename(self.output_file)}\n")
            else:
                self.results_text.insert(tk.END, "✅ No issues found. File was already properly formatted.\n")
        else:
            self.results_text.insert(tk.END, "❌ Processing failed!\n")
    
    # Include all the SRT processing methods from the original script
    def analyze_timestamp_format(self, timestamp: str) -> dict:
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
    
    def fix_timestamp_format(self, timestamp: str) -> str:
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
    
    def analyze_file_for_issues(self, input_file: str) -> List[str]:
        """Analyze file and return list of issues."""
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
        """Process SRT file and fix timestamps."""
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
            # Update progress
            if line_num % 50 == 0:
                progress = 0.2 + (line_num / len(lines)) * 0.7
                self.update_progress(progress)
            
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
    
    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Main function to start the modern GUI application."""
    app = ModernSRTFixerGUI()
    app.run()


if __name__ == "__main__":
    main()
