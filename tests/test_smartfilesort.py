#!/usr/bin/env python3
"""
SmartFileSort Unit Tests
========================

Unit tests for the SmartFileSort file organization system.

Author: Vinay
Date: September 2025
"""

import unittest
import tempfile
import os
import sys
import shutil
from pathlib import Path
import json

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from smartfilesort import FileClassifier, FileOrganizer
except ImportError:
    print("Warning: Could not import smartfilesort modules. Make sure to run tests from the project root.")
    FileClassifier = None
    FileOrganizer = None


class TestFileClassifier(unittest.TestCase):
    """Test cases for the FileClassifier class."""
    
    def setUp(self):
        """Set up test fixtures."""
        if FileClassifier is None:
            self.skipTest("FileClassifier not available")
        
        self.classifier = FileClassifier()
    
    def test_classify_documents(self):
        """Test document classification."""
        test_cases = [
            ("invoice_2025.pdf", "Documents"),
            ("resume.docx", "Documents"),
            ("report.txt", "Documents"),
            ("data.xlsx", "Documents"),
            ("presentation.pptx", "Documents"),
        ]
        
        for filename, expected_category in test_cases:
            with self.subTest(filename=filename):
                result = self.classifier.classify_file(filename)
                self.assertEqual(result, expected_category)
    
    def test_classify_images(self):
        """Test image classification."""
        test_cases = [
            ("photo.jpg", "Images"),
            ("screenshot.png", "Images"),
            ("diagram.gif", "Images"),
            ("logo.svg", "Images"),
            ("wallpaper.bmp", "Images"),
        ]
        
        for filename, expected_category in test_cases:
            with self.subTest(filename=filename):
                result = self.classifier.classify_file(filename)
                self.assertEqual(result, expected_category)
    
    def test_classify_code(self):
        """Test code file classification."""
        test_cases = [
            ("main.py", "Code"),
            ("app.js", "Code"),
            ("index.html", "Code"),
            ("style.css", "Code"),
            ("Program.java", "Code"),
        ]
        
        for filename, expected_category in test_cases:
            with self.subTest(filename=filename):
                result = self.classifier.classify_file(filename)
                self.assertEqual(result, expected_category)
    
    def test_classify_archives(self):
        """Test archive file classification."""
        test_cases = [
            ("backup.zip", "Archives"),
            ("files.rar", "Archives"),
            ("data.tar.gz", "Archives"),
            ("package.7z", "Archives"),
        ]
        
        for filename, expected_category in test_cases:
            with self.subTest(filename=filename):
                result = self.classifier.classify_file(filename)
                self.assertEqual(result, expected_category)
    
    def test_classify_unknown(self):
        """Test unknown file classification."""
        test_cases = [
            ("unknown.xyz", "Others"),
            ("mystery", "Others"),
            ("file.unknown", "Others"),
        ]
        
        for filename, expected_category in test_cases:
            with self.subTest(filename=filename):
                result = self.classifier.classify_file(filename)
                self.assertEqual(result, expected_category)
    
    def test_pattern_matching(self):
        """Test pattern-based classification."""
        test_cases = [
            ("invoice_march_2025.pdf", "Documents"),
            ("screenshot_desktop.png", "Images"),
            ("project_main.py", "Code"),
            ("backup_files.zip", "Archives"),
        ]
        
        for filename, expected_category in test_cases:
            with self.subTest(filename=filename):
                result = self.classifier.classify_file(filename)
                self.assertEqual(result, expected_category)


class TestFileOrganizer(unittest.TestCase):
    """Test cases for the FileOrganizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        if FileOrganizer is None:
            self.skipTest("FileOrganizer not available")
        
        # Create temporary directories
        self.temp_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.temp_dir, "source")
        self.target_dir = os.path.join(self.temp_dir, "target")
        
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.target_dir, exist_ok=True)
        
        # Create test files
        self.test_files = [
            "document.pdf",
            "photo.jpg",
            "script.py",
            "archive.zip",
            "music.mp3",
        ]
        
        for filename in self.test_files:
            file_path = os.path.join(self.source_dir, filename)
            with open(file_path, 'w') as f:
                f.write("test content")
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_dry_run_organization(self):
        """Test dry run mode."""
        organizer = FileOrganizer(self.source_dir, self.target_dir)
        success_count, fail_count = organizer.organize_files(dry_run=True)
        
        # In dry run, files should still exist in source
        for filename in self.test_files:
            source_file = os.path.join(self.source_dir, filename)
            self.assertTrue(os.path.exists(source_file), f"{filename} should still exist in source")
        
        # Target directory should be empty (except for created subdirs)
        target_files = []
        for root, dirs, files in os.walk(self.target_dir):
            target_files.extend(files)
        self.assertEqual(len(target_files), 0, "No files should be moved in dry run")
    
    def test_actual_organization(self):
        """Test actual file organization."""
        organizer = FileOrganizer(self.source_dir, self.target_dir)
        success_count, fail_count = organizer.organize_files(dry_run=False)
        
        # Files should be moved from source
        remaining_files = os.listdir(self.source_dir)
        self.assertEqual(len(remaining_files), 0, "All files should be moved from source")
        
        # Files should exist in target categories
        expected_locations = {
            "document.pdf": "Documents",
            "photo.jpg": "Images",
            "script.py": "Code",
            "archive.zip": "Archives",
            "music.mp3": "Audio",
        }
        
        for filename, category in expected_locations.items():
            target_file = os.path.join(self.target_dir, category, filename)
            self.assertTrue(os.path.exists(target_file), 
                          f"{filename} should exist in {category} folder")
    
    def test_duplicate_handling(self):
        """Test duplicate file handling."""
        # Create a file in target first
        target_subdir = os.path.join(self.target_dir, "Documents")
        os.makedirs(target_subdir, exist_ok=True)
        existing_file = os.path.join(target_subdir, "document.pdf")
        with open(existing_file, 'w') as f:
            f.write("existing content")
        
        # Run organizer
        organizer = FileOrganizer(self.source_dir, self.target_dir)
        success_count, fail_count = organizer.organize_files(dry_run=False)
        
        # Should have both original and renamed file
        self.assertTrue(os.path.exists(existing_file), "Original file should exist")
        
        renamed_file = os.path.join(target_subdir, "document(1).pdf")
        self.assertTrue(os.path.exists(renamed_file), "Renamed file should exist")


class TestConfigurationLoading(unittest.TestCase):
    """Test configuration file loading."""
    
    def setUp(self):
        """Set up test fixtures."""
        if FileClassifier is None:
            self.skipTest("FileClassifier not available")
        
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_rules.json")
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_custom_config_loading(self):
        """Test loading custom configuration."""
        # Create custom config
        custom_rules = {
            "TestCategory": {
                "extensions": [".test"],
                "patterns": ["test.*\\.test"]
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(custom_rules, f)
        
        # Load classifier with custom config
        classifier = FileClassifier(self.config_file)
        
        # Test custom classification
        result = classifier.classify_file("test_file.test")
        self.assertEqual(result, "TestCategory")
    
    def test_default_config_fallback(self):
        """Test fallback to default configuration."""
        # Use non-existent config file
        classifier = FileClassifier("/non/existent/config.json")
        
        # Should still work with defaults
        result = classifier.classify_file("document.pdf")
        self.assertEqual(result, "Documents")


def run_tests():
    """Run all unit tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestFileClassifier))
    suite.addTests(loader.loadTestsFromTestCase(TestFileOrganizer))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigurationLoading))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("SmartFileSort Unit Tests")
    print("=" * 40)
    
    if FileClassifier is None or FileOrganizer is None:
        print("Error: Could not import SmartFileSort modules.")
        print("Make sure to run tests from the project root directory.")
        sys.exit(1)
    
    success = run_tests()
    
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)