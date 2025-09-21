#!/usr/bin/env python3
"""
SmartFileSort Demo Setup
========================

Creates sample files for testing and demonstrating the SmartFileSort tool.
This script generates various file types with different naming patterns
to showcase the organization capabilities.

Author: Vinay
Date: September 2025
"""

import os
import tempfile
from pathlib import Path
from datetime import datetime


def create_demo_files(demo_dir: str):
    """
    Create sample files for demonstration.
    
    Args:
        demo_dir: Directory to create demo files in
    """
    demo_path = Path(demo_dir)
    demo_path.mkdir(parents=True, exist_ok=True)
    
    # Sample file contents and names
    demo_files = [
        # Documents
        ("invoice_2025_march.pdf", "Sample PDF invoice content"),
        ("resume_john_doe.docx", "Sample resume document"),
        ("project_report.txt", "Sample project report content"),
        ("financial_statement.xlsx", "Sample spreadsheet data"),
        ("contract_agreement.pdf", "Sample contract content"),
        
        # Images
        ("screenshot_desktop.png", "PNG image data"),
        ("photo_vacation_2025.jpg", "JPEG image data"),
        ("logo_company.svg", "SVG vector image"),
        ("wallpaper_mountains.jpg", "Background image data"),
        ("diagram_flowchart.png", "Technical diagram"),
        
        # Videos
        ("lecture_python_basics.mp4", "Video lecture content"),
        ("tutorial_excel_advanced.avi", "Tutorial video data"),
        ("meeting_recording_20250921.mkv", "Meeting recording"),
        ("movie_sample_clip.mp4", "Sample movie clip"),
        
        # Audio
        ("music_classical_symphony.mp3", "Audio music file"),
        ("podcast_tech_talk.wav", "Podcast audio content"),
        ("voice_memo_ideas.m4a", "Voice recording"),
        ("audio_sample_test.flac", "High quality audio"),
        
        # Code
        ("project_main.py", "# Python main application\nprint('Hello World!')"),
        ("website_index.html", "<!DOCTYPE html><html><head><title>Test</title></head></html>"),
        ("styles_main.css", "body { margin: 0; padding: 20px; }"),
        ("script_automation.js", "// JavaScript automation script\nconsole.log('Running');"),
        ("database_query.sql", "-- Sample SQL query\nSELECT * FROM users;"),
        
        # Archives
        ("backup_project_files.zip", "ZIP archive content"),
        ("archive_old_documents.rar", "RAR archive content"),
        ("export_data_2025.tar.gz", "Compressed archive"),
        ("package_software.7z", "7zip archive content"),
        
        # Executables
        ("setup_software_installer.exe", "Windows executable"),
        ("install_package.msi", "Windows installer"),
        ("update_application.exe", "Application updater"),
        
        # Books
        ("ebook_python_guide.epub", "Electronic book content"),
        ("manual_user_guide.pdf", "User manual content"),
        ("book_programming_101.mobi", "Programming book"),
        
        # Fonts
        ("font_arial_custom.ttf", "TrueType font data"),
        ("typeface_modern.otf", "OpenType font data"),
        
        # Mixed/Others
        ("data_export.csv", "Sample,CSV,Data\n1,2,3\n4,5,6"),
        ("config_settings.json", '{"setting": "value", "enabled": true}'),
        ("readme_instructions.md", "# Sample Markdown\nThis is a demo file."),
        ("unknown_file.xyz", "Unknown file type content"),
        ("temp_file.tmp", "Temporary file content"),
    ]
    
    print(f"Creating {len(demo_files)} demo files in {demo_dir}...")
    
    created_files = []
    for filename, content in demo_files:
        file_path = demo_path / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            created_files.append(str(file_path))
            print(f"✓ Created: {filename}")
        except Exception as e:
            print(f"✗ Failed to create {filename}: {e}")
    
    print(f"\nDemo setup complete! Created {len(created_files)} files.")
    print(f"Demo directory: {demo_dir}")
    
    return created_files


def run_demo_organization(source_dir: str, target_dir: str, dry_run: bool = True):
    """
    Run a demo organization to show how the tool works.
    
    Args:
        source_dir: Directory with demo files
        target_dir: Directory to organize files into
        dry_run: Whether to run in preview mode
    """
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
    
    try:
        from smartfilesort import FileOrganizer
        
        print(f"\n{'='*60}")
        print("DEMO: SmartFileSort Organization")
        print(f"{'='*60}")
        print(f"Source: {source_dir}")
        print(f"Target: {target_dir}")
        print(f"Mode: {'DRY RUN (Preview)' if dry_run else 'LIVE (Files will be moved)'}")
        print(f"{'='*60}")
        
        # Create organizer
        organizer = FileOrganizer(source_dir, target_dir)
        
        # Run organization
        success_count, fail_count = organizer.organize_files(dry_run=dry_run)
        
        print(f"\n{'='*60}")
        print("DEMO RESULTS")
        print(f"{'='*60}")
        
        if dry_run:
            print(f"Files that would be organized: {success_count + fail_count}")
            print("This was a preview - no files were actually moved.")
        else:
            print(f"Successfully organized: {success_count} files")
            print(f"Failed to organize: {fail_count} files")
        
        print(f"Check the logs directory for detailed operation logs.")
        
        return success_count, fail_count
        
    except ImportError as e:
        print(f"Error: Could not import SmartFileSort module: {e}")
        print("Make sure you're running this from the project root directory.")
        return 0, 0
    except Exception as e:
        print(f"Error during demo: {e}")
        return 0, 0


def show_classification_preview(demo_dir: str):
    """
    Show how files would be classified without moving them.
    
    Args:
        demo_dir: Directory containing demo files
    """
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
    
    try:
        from smartfilesort import FileClassifier
        
        print(f"\n{'='*60}")
        print("CLASSIFICATION PREVIEW")
        print(f"{'='*60}")
        
        classifier = FileClassifier()
        demo_path = Path(demo_dir)
        
        # Group files by category
        categories = {}
        for file_path in demo_path.glob('*'):
            if file_path.is_file():
                category = classifier.classify_file(str(file_path))
                if category not in categories:
                    categories[category] = []
                categories[category].append(file_path.name)
        
        # Display results
        total_files = 0
        for category, files in sorted(categories.items()):
            print(f"\n📁 {category.upper()} ({len(files)} files):")
            for file in sorted(files):
                print(f"   • {file}")
            total_files += len(files)
        
        print(f"\n{'='*60}")
        print(f"Total files: {total_files} in {len(categories)} categories")
        print(f"{'='*60}")
        
    except ImportError as e:
        print(f"Error: Could not import SmartFileSort module: {e}")
    except Exception as e:
        print(f"Error during classification: {e}")


def cleanup_demo(demo_dir: str):
    """
    Clean up demo files.
    
    Args:
        demo_dir: Directory to clean up
    """
    import shutil
    
    demo_path = Path(demo_dir)
    if demo_path.exists():
        try:
            shutil.rmtree(demo_path)
            print(f"✓ Cleaned up demo directory: {demo_dir}")
        except Exception as e:
            print(f"✗ Error cleaning up {demo_dir}: {e}")
    else:
        print(f"Demo directory doesn't exist: {demo_dir}")


def main():
    """Main demo script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="SmartFileSort Demo Setup and Testing")
    parser.add_argument("--demo-dir", default=None, help="Demo files directory (default: temp directory)")
    parser.add_argument("--target-dir", default=None, help="Target organization directory (default: temp directory)")
    parser.add_argument("--create-files", action="store_true", help="Create demo files")
    parser.add_argument("--preview", action="store_true", help="Show classification preview")
    parser.add_argument("--run-demo", action="store_true", help="Run demo organization (dry run)")
    parser.add_argument("--run-live", action="store_true", help="Run demo organization (live - actually move files)")
    parser.add_argument("--cleanup", action="store_true", help="Clean up demo files")
    parser.add_argument("--full-demo", action="store_true", help="Run complete demo (create, preview, organize, cleanup)")
    
    args = parser.parse_args()
    
    # Set default directories
    if args.demo_dir is None:
        args.demo_dir = os.path.join(tempfile.gettempdir(), "SmartFileSort_Demo")
    
    if args.target_dir is None:
        args.target_dir = os.path.join(tempfile.gettempdir(), "SmartFileSort_Organized")
    
    print("SmartFileSort Demo Setup")
    print("=" * 40)
    print(f"Demo files directory: {args.demo_dir}")
    print(f"Target directory: {args.target_dir}")
    print("=" * 40)
    
    # Run full demo
    if args.full_demo:
        print("\n🚀 Running FULL DEMO...")
        create_demo_files(args.demo_dir)
        show_classification_preview(args.demo_dir)
        run_demo_organization(args.demo_dir, args.target_dir, dry_run=True)
        
        response = input("\nWould you like to run the actual organization (files will be moved)? (y/N): ")
        if response.lower().startswith('y'):
            run_demo_organization(args.demo_dir, args.target_dir, dry_run=False)
        
        response = input("\nWould you like to clean up demo files? (y/N): ")
        if response.lower().startswith('y'):
            cleanup_demo(args.demo_dir)
            cleanup_demo(args.target_dir)
        
        return
    
    # Individual actions
    if args.create_files:
        create_demo_files(args.demo_dir)
    
    if args.preview:
        show_classification_preview(args.demo_dir)
    
    if args.run_demo:
        run_demo_organization(args.demo_dir, args.target_dir, dry_run=True)
    
    if args.run_live:
        print("\n⚠️  WARNING: This will actually move files!")
        response = input("Are you sure you want to continue? (y/N): ")
        if response.lower().startswith('y'):
            run_demo_organization(args.demo_dir, args.target_dir, dry_run=False)
        else:
            print("Live demo cancelled.")
    
    if args.cleanup:
        cleanup_demo(args.demo_dir)
        cleanup_demo(args.target_dir)
    
    if not any([args.create_files, args.preview, args.run_demo, args.run_live, args.cleanup, args.full_demo]):
        print("\nNo action specified. Use --help to see available options.")
        print("Quick start: python demo_setup.py --full-demo")


if __name__ == "__main__":
    main()