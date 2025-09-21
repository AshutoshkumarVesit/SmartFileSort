#!/usr/bin/env python3
"""
Interactive Demo Setup for Interviews
=====================================

Creates a realistic demo environment for showcasing SmartFileSort
during job interviews and presentations.

Author: Ashutosh Kumar
Date: September 2025
"""

import os
import tempfile
from pathlib import Path
import time

def create_interview_demo():
    """Create a realistic demo setup for interviews."""
    
    # Create demo directory
    demo_base = os.path.join(tempfile.gettempdir(), "SmartFileSort_Interview_Demo")
    messy_folder = os.path.join(demo_base, "Messy_Downloads")
    organized_folder = os.path.join(demo_base, "Organized_Output")
    
    os.makedirs(messy_folder, exist_ok=True)
    os.makedirs(organized_folder, exist_ok=True)
    
    print("🎬 Setting up Interview Demo Environment...")
    print(f"📁 Demo Location: {demo_base}")
    print("=" * 60)
    
    # Realistic workplace files
    demo_files = [
        # Business Documents
        ("Q3_Financial_Report_2025.pdf", "PDF report content - quarterly earnings data"),
        ("Employee_Handbook_Updated.docx", "Word document - HR policies and procedures"),
        ("Invoice_WorldWideTech_Sept2025.pdf", "Invoice details and payment information"),
        ("Project_Proposal_Automation.pptx", "PowerPoint presentation content"),
        ("Budget_Analysis_2025.xlsx", "Excel spreadsheet with financial data"),
        
        # Screenshots & Images  
        ("Screenshot_Dashboard_20250921.png", "PNG screenshot of application dashboard"),
        ("Company_Logo_New.jpg", "JPEG company logo file"),
        ("Workflow_Diagram.png", "Process flow diagram image"),
        ("Team_Photo_Q3.jpg", "Team photograph from quarterly meeting"),
        
        # Development Files
        ("automation_script.py", "# Python automation script\nimport os\nprint('Automating workflows')"),
        ("database_backup.sql", "-- SQL backup script\nSELECT * FROM employees;"),
        ("website_index.html", "<!DOCTYPE html><html><head><title>Company Site</title></head></html>"),
        ("api_documentation.md", "# API Documentation\n## Endpoints\n- GET /users\n- POST /data"),
        
        # Media Files
        ("Training_Video_Python.mp4", "MP4 video content - Python training material"),
        ("Webinar_Recording_Sept21.avi", "Webinar recording about automation"),
        ("Background_Music.mp3", "MP3 audio file for presentations"),
        
        # Archives & Backups
        ("Project_Backup_Sept2025.zip", "ZIP archive of project files"),
        ("Old_Reports_Archive.rar", "RAR archive of historical reports"),
        
        # Mixed/Misc
        ("README_Instructions.txt", "Text file with setup instructions"),
        ("config_settings.json", '{"database": "localhost", "port": 5432}'),
        ("temp_download.tmp", "Temporary file content"),
    ]
    
    print("📝 Creating realistic workplace files...")
    created_count = 0
    
    for filename, content in demo_files:
        file_path = os.path.join(messy_folder, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            created_count += 1
            print(f"   ✓ {filename}")
        except Exception as e:
            print(f"   ✗ Failed: {filename} - {e}")
    
    print("=" * 60)
    print(f"🎉 Demo setup complete! Created {created_count} files.")
    print("\n📋 INTERVIEW DEMO READY:")
    print(f"   Messy Folder:     {messy_folder}")
    print(f"   Output Folder:    {organized_folder}")
    
    print("\n🎯 DEMO SCRIPT:")
    print("1. Show the messy folder with mixed file types")
    print("2. Run: python gui/gui_app.py") 
    print("3. Set source to messy folder, target to output folder")
    print("4. Enable dry-run first to preview")
    print("5. Run actual organization")
    print("6. Show organized results with perfect categorization")
    
    print("\n💡 KEY TALKING POINTS:")
    print("   • Saves hours of manual organization")
    print("   • Handles real workplace file types")  
    print("   • Provides audit trails for compliance")
    print("   • Scales to thousands of files")
    print("   • Integrates with Windows automation")
    
    return messy_folder, organized_folder


def cleanup_demo():
    """Clean up demo files after interview."""
    import shutil
    demo_base = os.path.join(tempfile.gettempdir(), "SmartFileSort_Interview_Demo")
    
    if os.path.exists(demo_base):
        try:
            shutil.rmtree(demo_base)
            print(f"✅ Demo cleanup complete: {demo_base}")
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
    else:
        print("No demo files to clean up.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="SmartFileSort Interview Demo Setup")
    parser.add_argument("--setup", action="store_true", help="Create interview demo environment")
    parser.add_argument("--cleanup", action="store_true", help="Clean up demo files")
    
    args = parser.parse_args()
    
    if args.setup:
        messy_folder, organized_folder = create_interview_demo()
        
        print(f"\n🚀 Ready for demo! Use these paths:")
        print(f"Source: {messy_folder}")
        print(f"Target: {organized_folder}")
        
    elif args.cleanup:
        cleanup_demo()
        
    else:
        print("SmartFileSort Interview Demo")
        print("Usage:")
        print("  python interview_demo.py --setup    # Create demo files")
        print("  python interview_demo.py --cleanup  # Remove demo files")
        
        # Quick setup option
        response = input("\nCreate demo environment now? (y/N): ")
        if response.lower().startswith('y'):
            create_interview_demo()