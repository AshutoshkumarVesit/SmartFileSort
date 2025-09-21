#!/usr/bin/env python3
"""
SmartFileSort - Automated File & Data Organizer
===============================================

An intelligent file organization tool that automatically categorizes and sorts
files from a source directory into organized folders based on file types,
naming patterns, and custom rules.

Author: Vinay
Date: September 2025
Version: 1.0.0
"""

import os
import shutil
import re
import logging
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import hashlib


class FileClassifier:
    """Handles file type detection and classification logic."""
    
    def __init__(self, config_path: str = None):
        """Initialize the classifier with configuration."""
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), '..', 'config', 'rules.json')
        self.rules = self._load_classification_rules()
        
    def _load_classification_rules(self) -> Dict:
        """Load file classification rules from configuration."""
        default_rules = {
            "Documents": {
                "extensions": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
                "patterns": [
                    r"invoice.*\.(pdf|doc|docx)",
                    r"resume.*\.(pdf|doc|docx)",
                    r"report.*\.(pdf|doc|docx|txt)"
                ]
            },
            "Images": {
                "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".ico"],
                "patterns": [
                    r"screenshot.*\.(jpg|jpeg|png)",
                    r"photo.*\.(jpg|jpeg|png)",
                    r"image.*\.(jpg|jpeg|png|gif)"
                ]
            },
            "Videos": {
                "extensions": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
                "patterns": [
                    r"lecture.*\.(mp4|avi|mkv)",
                    r"tutorial.*\.(mp4|avi|mkv)",
                    r"meeting.*\.(mp4|avi|mkv)"
                ]
            },
            "Audio": {
                "extensions": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
                "patterns": [
                    r"music.*\.(mp3|wav|flac)",
                    r"audio.*\.(mp3|wav|flac)",
                    r"podcast.*\.(mp3|wav)"
                ]
            },
            "Code": {
                "extensions": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".cs", ".php", ".rb", ".go", ".rs"],
                "patterns": [
                    r"project.*\.(py|js|java|cpp)",
                    r"script.*\.(py|js|sh|bat)",
                    r".*_code\.(py|js|java|cpp)"
                ]
            },
            "Archives": {
                "extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
                "patterns": [
                    r"backup.*\.(zip|rar|tar|gz)",
                    r"archive.*\.(zip|rar|tar|gz)"
                ]
            },
            "Executables": {
                "extensions": [".exe", ".msi", ".dmg", ".deb", ".rpm", ".pkg"],
                "patterns": [
                    r"setup.*\.(exe|msi)",
                    r"installer.*\.(exe|msi|dmg)"
                ]
            }
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                # Create default config file
                os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
                with open(self.config_path, 'w') as f:
                    json.dump(default_rules, f, indent=4)
                return default_rules
        except Exception as e:
            logging.warning(f"Could not load rules config: {e}. Using defaults.")
            return default_rules
    
    def classify_file(self, filepath: str) -> str:
        """
        Classify a file based on extension and naming patterns.
        
        Args:
            filepath: Path to the file to classify
            
        Returns:
            Category name or 'Others' if no match found
        """
        filename = os.path.basename(filepath).lower()
        file_ext = os.path.splitext(filename)[1].lower()
        
        # Check each category
        for category, rules in self.rules.items():
            # Check extensions
            if file_ext in [ext.lower() for ext in rules.get("extensions", [])]:
                # Double-check with patterns if available
                patterns = rules.get("patterns", [])
                if patterns:
                    for pattern in patterns:
                        if re.search(pattern, filename, re.IGNORECASE):
                            return category
                return category
            
            # Check naming patterns
            patterns = rules.get("patterns", [])
            for pattern in patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    return category
        
        return "Others"


class FileOrganizer:
    """Main file organization logic and operations."""
    
    def __init__(self, source_dir: str, target_dir: str, config_path: str = None):
        """
        Initialize the file organizer.
        
        Args:
            source_dir: Directory to organize files from
            target_dir: Base directory to organize files into
            config_path: Path to configuration file
        """
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.classifier = FileClassifier(config_path)
        self.logger = self._setup_logging()
        self.moved_files = []
        self.failed_files = []
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logger = logging.getLogger("SmartFileSort")
        logger.setLevel(logging.INFO)
        
        # File handler
        log_file = log_dir / f"file_sort_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _get_file_hash(self, filepath: str) -> str:
        """Calculate MD5 hash of a file for duplicate detection."""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.warning(f"Could not calculate hash for {filepath}: {e}")
            return ""
    
    def _handle_duplicate(self, source_file: Path, target_file: Path) -> Path:
        """
        Handle duplicate files by renaming.
        
        Args:
            source_file: Original file path
            target_file: Target file path that already exists
            
        Returns:
            New target path with unique name
        """
        counter = 1
        file_stem = target_file.stem
        file_suffix = target_file.suffix
        parent_dir = target_file.parent
        
        while True:
            new_name = f"{file_stem}({counter}){file_suffix}"
            new_target = parent_dir / new_name
            
            if not new_target.exists():
                return new_target
            
            # Check if files are actually identical
            if self._get_file_hash(str(source_file)) == self._get_file_hash(str(new_target)):
                self.logger.info(f"Identical file found, skipping: {source_file}")
                return None
            
            counter += 1
            if counter > 100:  # Safety limit
                raise Exception(f"Too many duplicates for {source_file}")
    
    def _move_file(self, source_path: Path, category: str) -> bool:
        """
        Move a file to the appropriate category folder.
        
        Args:
            source_path: Path to the source file
            category: Target category folder name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create target directory
            target_dir = self.target_dir / category
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Determine target file path
            target_path = target_dir / source_path.name
            
            # Handle duplicates
            if target_path.exists():
                target_path = self._handle_duplicate(source_path, target_path)
                if target_path is None:  # File is identical, skip
                    return True
            
            # Move the file
            shutil.move(str(source_path), str(target_path))
            
            self.moved_files.append({
                'timestamp': datetime.now().isoformat(),
                'source': str(source_path),
                'target': str(target_path),
                'category': category,
                'status': 'Success'
            })
            
            self.logger.info(f"Moved: {source_path} → {target_path}")
            return True
            
        except Exception as e:
            self.failed_files.append({
                'timestamp': datetime.now().isoformat(),
                'source': str(source_path),
                'target': '',
                'category': category,
                'status': f'Failed: {str(e)}'
            })
            
            self.logger.error(f"Failed to move {source_path}: {e}")
            return False
    
    def organize_files(self, dry_run: bool = False) -> Tuple[int, int]:
        """
        Organize all files in the source directory.
        
        Args:
            dry_run: If True, only log what would be done without actually moving files
            
        Returns:
            Tuple of (successful_moves, failed_moves)
        """
        if not self.source_dir.exists():
            self.logger.error(f"Source directory does not exist: {self.source_dir}")
            return 0, 0
        
        self.logger.info(f"Starting file organization from {self.source_dir}")
        if dry_run:
            self.logger.info("DRY RUN MODE - No files will be moved")
        
        files_to_process = []
        
        # Collect all files to process
        for item in self.source_dir.iterdir():
            if item.is_file():
                files_to_process.append(item)
        
        self.logger.info(f"Found {len(files_to_process)} files to process")
        
        # Process each file
        for file_path in files_to_process:
            category = self.classifier.classify_file(str(file_path))
            self.logger.info(f"Classified {file_path.name} as {category}")
            
            if not dry_run:
                self._move_file(file_path, category)
            else:
                # Just log what would happen
                target_dir = self.target_dir / category
                target_path = target_dir / file_path.name
                self.logger.info(f"Would move: {file_path} → {target_path}")
        
        successful = len(self.moved_files)
        failed = len(self.failed_files)
        
        # Save operation log
        if not dry_run:
            self._save_operation_log()
        
        self.logger.info(f"Organization complete. Success: {successful}, Failed: {failed}")
        return successful, failed
    
    def _save_operation_log(self):
        """Save operation log to CSV file."""
        log_dir = Path(__file__).parent.parent / "logs"
        log_file = log_dir / f"operations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        all_operations = self.moved_files + self.failed_files
        
        if all_operations:
            with open(log_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['timestamp', 'source', 'target', 'category', 'status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_operations)
            
            self.logger.info(f"Operation log saved to: {log_file}")


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="SmartFileSort - Automated File Organizer")
    parser.add_argument("source", help="Source directory to organize")
    parser.add_argument("target", help="Target directory for organized files")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without moving files")
    parser.add_argument("--config", help="Path to configuration file")
    
    args = parser.parse_args()
    
    # Create organizer and run
    organizer = FileOrganizer(args.source, args.target, args.config)
    success_count, fail_count = organizer.organize_files(dry_run=args.dry_run)
    
    print(f"\n=== SmartFileSort Complete ===")
    print(f"Successfully processed: {success_count} files")
    print(f"Failed to process: {fail_count} files")
    
    if fail_count > 0:
        print(f"Check logs for details on failed operations")


if __name__ == "__main__":
    main()