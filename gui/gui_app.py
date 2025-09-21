#!/usr/bin/env python3
"""
SmartFileSort GUI - Graphical User Interface
===========================================

A Tkinter-based GUI for the SmartFileSort file organizer tool.
Provides easy access to file organization, configuration, and log viewing.

Author: Vinay
Date: September 2025
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import threading
from pathlib import Path
import json
import csv
from datetime import datetime

# Add the src directory to the path to import our main module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from smartfilesort import FileOrganizer


class SmartFileSortGUI:
    """Main GUI application class."""
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("SmartFileSort - Automated File Organizer")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Variables
        self.source_dir = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.target_dir = tk.StringVar(value=os.path.expanduser("~/Documents/OrganizedFiles"))
        self.dry_run = tk.BooleanVar(value=True)
        self.is_running = False
        
        self.setup_ui()
        self.load_last_settings()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Main tab
        self.setup_main_tab(notebook)
        
        # Logs tab
        self.setup_logs_tab(notebook)
        
        # Settings tab
        self.setup_settings_tab(notebook)
        
        # About tab
        self.setup_about_tab(notebook)
    
    def setup_main_tab(self, notebook):
        """Set up the main operation tab."""
        main_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text="File Organizer")
        
        # Title
        title_label = ttk.Label(main_frame, text="SmartFileSort", font=("Arial", 16, "bold"))
        title_label.pack(pady=(10, 20))
        
        # Directory selection frame
        dir_frame = ttk.LabelFrame(main_frame, text="Directory Settings", padding=10)
        dir_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Source directory
        ttk.Label(dir_frame, text="Source Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        source_entry = ttk.Entry(dir_frame, textvariable=self.source_dir, width=50)
        source_entry.grid(row=0, column=1, padx=(10, 5), pady=5, sticky=tk.EW)
        ttk.Button(dir_frame, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)
        
        # Target directory
        ttk.Label(dir_frame, text="Target Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        target_entry = ttk.Entry(dir_frame, textvariable=self.target_dir, width=50)
        target_entry.grid(row=1, column=1, padx=(10, 5), pady=5, sticky=tk.EW)
        ttk.Button(dir_frame, text="Browse", command=self.browse_target).grid(row=1, column=2, padx=5, pady=5)
        
        dir_frame.grid_columnconfigure(1, weight=1)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Checkbutton(options_frame, text="Dry Run (Preview only - don't move files)", 
                       variable=self.dry_run).pack(anchor=tk.W)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        self.run_button = ttk.Button(button_frame, text="Organize Files", 
                                   command=self.run_organizer, style="Accent.TButton")
        self.run_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Preview Classification", 
                  command=self.preview_classification).pack(side=tk.LEFT, padx=(0, 10))
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding=10)
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, text="Ready to organize files...")
        self.status_label.pack(anchor=tk.W)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(progress_frame, height=10, width=70)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
    
    def setup_logs_tab(self, notebook):
        """Set up the logs viewing tab."""
        logs_frame = ttk.Frame(notebook)
        notebook.add(logs_frame, text="View Logs")
        
        # Controls frame
        controls_frame = ttk.Frame(logs_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(controls_frame, text="Refresh Logs", 
                  command=self.refresh_logs).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="Open Logs Folder", 
                  command=self.open_logs_folder).pack(side=tk.LEFT)
        
        # Logs display
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=25, width=80)
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.refresh_logs()
    
    def setup_settings_tab(self, notebook):
        """Set up the settings configuration tab."""
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="Settings")
        
        # Create scrollable frame
        canvas = tk.Canvas(settings_frame)
        scrollbar = ttk.Scrollbar(settings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # File type rules
        rules_frame = ttk.LabelFrame(scrollable_frame, text="File Classification Rules", padding=10)
        rules_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(rules_frame, text="Click to edit classification rules:").pack(anchor=tk.W)
        ttk.Button(rules_frame, text="Edit Rules File", 
                  command=self.edit_rules_file).pack(anchor=tk.W, pady=5)
        
        # Settings info
        info_frame = ttk.LabelFrame(scrollable_frame, text="Configuration Files", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
        ttk.Label(info_frame, text=f"Rules file: {os.path.join(config_dir, 'rules.json')}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Settings file: {os.path.join(config_dir, 'settings.json')}").pack(anchor=tk.W)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_about_tab(self, notebook):
        """Set up the about/help tab."""
        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text="About")
        
        # Title
        title_label = ttk.Label(about_frame, text="SmartFileSort", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)
        
        # Version info
        version_label = ttk.Label(about_frame, text="Version 1.0.0", font=("Arial", 12))
        version_label.pack()
        
        # Description
        desc_text = """
Automated File & Data Organizer

SmartFileSort intelligently organizes unstructured files from a source directory 
into categorized folders based on file types and naming patterns.

Features:
• Automatic file classification by extension and name patterns
• Duplicate file handling with intelligent renaming
• Comprehensive logging and audit trails
• Configurable rules and settings
• Dry-run mode for safe preview
• Windows Task Scheduler integration
• GUI and command-line interfaces

Perfect for organizing Downloads folders, shared drives, and any cluttered directories!
        """
        
        desc_label = ttk.Label(about_frame, text=desc_text, justify=tk.LEFT, wraplength=600)
        desc_label.pack(pady=20, padx=20)
        
        # Author info
        author_label = ttk.Label(about_frame, text="Created by Vinay • September 2025", 
                                font=("Arial", 10, "italic"))
        author_label.pack(pady=10)
    
    def browse_source(self):
        """Browse for source directory."""
        directory = filedialog.askdirectory(title="Select Source Directory", 
                                          initialdir=self.source_dir.get())
        if directory:
            self.source_dir.set(directory)
    
    def browse_target(self):
        """Browse for target directory."""
        directory = filedialog.askdirectory(title="Select Target Directory", 
                                          initialdir=self.target_dir.get())
        if directory:
            self.target_dir.set(directory)
    
    def log_message(self, message):
        """Add a message to the output text area."""
        self.output_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def run_organizer(self):
        """Run the file organizer in a separate thread."""
        if self.is_running:
            messagebox.showwarning("Already Running", "File organizer is already running!")
            return
        
        source = self.source_dir.get().strip()
        target = self.target_dir.get().strip()
        
        if not source or not target:
            messagebox.showerror("Error", "Please select both source and target directories!")
            return
        
        if not os.path.exists(source):
            messagebox.showerror("Error", f"Source directory does not exist: {source}")
            return
        
        # Save settings
        self.save_settings()
        
        # Start organizer in separate thread
        thread = threading.Thread(target=self._run_organizer_thread)
        thread.daemon = True
        thread.start()
    
    def _run_organizer_thread(self):
        """Run the organizer in a separate thread."""
        self.is_running = True
        self.run_button.config(state='disabled')
        self.progress.start()
        
        try:
            self.log_message("Starting file organization...")
            self.status_label.config(text="Organizing files...")
            
            # Create organizer
            organizer = FileOrganizer(self.source_dir.get(), self.target_dir.get())
            
            # Run organization
            success_count, fail_count = organizer.organize_files(dry_run=self.dry_run.get())
            
            # Update UI
            if self.dry_run.get():
                self.log_message(f"DRY RUN completed. Found {success_count + fail_count} files to organize.")
            else:
                self.log_message(f"Organization completed! Success: {success_count}, Failed: {fail_count}")
            
            self.status_label.config(text="Organization completed successfully!")
            
            if not self.dry_run.get():
                messagebox.showinfo("Complete", 
                                  f"File organization completed!\n\nSuccessfully processed: {success_count} files\nFailed: {fail_count} files")
        
        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            self.status_label.config(text="Organization failed!")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            self.is_running = False
            self.run_button.config(state='normal')
            self.progress.stop()
    
    def preview_classification(self):
        """Preview how files would be classified."""
        source = self.source_dir.get().strip()
        
        if not source or not os.path.exists(source):
            messagebox.showerror("Error", "Please select a valid source directory!")
            return
        
        try:
            from smartfilesort import FileClassifier
            classifier = FileClassifier()
            
            self.output_text.delete(1.0, tk.END)
            self.log_message("Previewing file classification...")
            
            source_path = Path(source)
            files_found = list(source_path.glob('*'))
            files_found = [f for f in files_found if f.is_file()]
            
            if not files_found:
                self.log_message("No files found in source directory.")
                return
            
            # Group files by category
            categories = {}
            for file_path in files_found:
                category = classifier.classify_file(str(file_path))
                if category not in categories:
                    categories[category] = []
                categories[category].append(file_path.name)
            
            # Display results
            for category, files in categories.items():
                self.log_message(f"\n{category.upper()} ({len(files)} files):")
                for file in files[:10]:  # Show first 10 files
                    self.log_message(f"  • {file}")
                if len(files) > 10:
                    self.log_message(f"  ... and {len(files) - 10} more files")
            
            self.log_message(f"\nTotal: {len(files_found)} files in {len(categories)} categories")
            
        except Exception as e:
            messagebox.showerror("Error", f"Preview failed: {str(e)}")
    
    def refresh_logs(self):
        """Refresh the logs display."""
        try:
            logs_dir = Path(__file__).parent.parent / "logs"
            
            if not logs_dir.exists():
                self.logs_text.delete(1.0, tk.END)
                self.logs_text.insert(tk.END, "No logs directory found. Run the organizer first to generate logs.")
                return
            
            self.logs_text.delete(1.0, tk.END)
            
            # Get all log files
            log_files = list(logs_dir.glob("*.log")) + list(logs_dir.glob("*.csv"))
            log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            if not log_files:
                self.logs_text.insert(tk.END, "No log files found.")
                return
            
            # Show latest files
            for log_file in log_files[:5]:  # Show last 5 log files
                self.logs_text.insert(tk.END, f"\n=== {log_file.name} ===\n")
                
                try:
                    if log_file.suffix == '.csv':
                        # Display CSV in readable format
                        with open(log_file, 'r', newline='', encoding='utf-8') as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                self.logs_text.insert(tk.END, 
                                    f"{row.get('timestamp', 'N/A')} | {row.get('status', 'N/A')} | "
                                    f"{os.path.basename(row.get('source', 'N/A'))} → {row.get('category', 'N/A')}\n")
                    else:
                        # Display regular log file
                        with open(log_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Show last 20 lines
                            lines = content.split('\n')[-20:]
                            self.logs_text.insert(tk.END, '\n'.join(lines))
                    
                    self.logs_text.insert(tk.END, "\n")
                    
                except Exception as e:
                    self.logs_text.insert(tk.END, f"Error reading {log_file.name}: {e}\n")
        
        except Exception as e:
            self.logs_text.insert(tk.END, f"Error loading logs: {e}")
    
    def open_logs_folder(self):
        """Open the logs folder in file explorer."""
        logs_dir = Path(__file__).parent.parent / "logs"
        
        if logs_dir.exists():
            os.startfile(str(logs_dir))
        else:
            messagebox.showinfo("Info", "Logs directory doesn't exist yet. Run the organizer first.")
    
    def edit_rules_file(self):
        """Open the rules file for editing."""
        rules_file = Path(__file__).parent.parent / "config" / "rules.json"
        
        if rules_file.exists():
            os.startfile(str(rules_file))
        else:
            messagebox.showerror("Error", f"Rules file not found: {rules_file}")
    
    def save_settings(self):
        """Save current settings to file."""
        settings = {
            'source_dir': self.source_dir.get(),
            'target_dir': self.target_dir.get(),
            'dry_run': self.dry_run.get()
        }
        
        settings_file = Path(__file__).parent.parent / "gui_settings.json"
        
        try:
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Could not save settings: {e}")
    
    def load_last_settings(self):
        """Load the last saved settings."""
        settings_file = Path(__file__).parent.parent / "gui_settings.json"
        
        try:
            if settings_file.exists():
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                
                self.source_dir.set(settings.get('source_dir', self.source_dir.get()))
                self.target_dir.set(settings.get('target_dir', self.target_dir.get()))
                self.dry_run.set(settings.get('dry_run', True))
        except Exception as e:
            print(f"Could not load settings: {e}")


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    
    # Set the application icon (if available)
    try:
        # You can add an icon file here
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    # Create and run the application
    app = SmartFileSortGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()