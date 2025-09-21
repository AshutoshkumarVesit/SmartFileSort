# 🚀 SmartFileSort - Automated File & Data Organizer

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/platform-windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![GitHub stars](https://img.shields.io/github/stars/AshutoshkumarVesit/SmartFileSort.svg)](https://github.com/AshutoshkumarVesit/SmartFileSort/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/AshutoshkumarVesit/SmartFileSort.svg)](https://github.com/AshutoshkumarVesit/SmartFileSort/network)
[![GitHub issues](https://img.shields.io/github/issues/AshutoshkumarVesit/SmartFileSort.svg)](https://github.com/AshutoshkumarVesit/SmartFileSort/issues)

An intelligent automation tool that **automatically organizes unstructured files** from cluttered directories into categorized folders. Perfect for organizing Downloads folders, shared drives, and any messy file collections!

![SmartFileSort Demo](https://via.placeholder.com/800x400/2E3440/88C0D0?text=SmartFileSort+Demo+Coming+Soon)

> 💡 **Perfect for demonstrating automation skills in job interviews and portfolio projects!**

## 🎯 Features

- **🧠 Intelligent Classification**: Automatically categorizes files by extension and naming patterns
- **📁 Smart Organization**: Sorts files into logical folders (Documents, Images, Code, etc.)
- **🔍 Duplicate Handling**: Detects and handles duplicate files intelligently
- **📊 Comprehensive Logging**: Tracks every operation with detailed CSV logs
- **⚡ Automation Ready**: Windows Task Scheduler integration for hands-free operation
- **🖥️ User-Friendly GUI**: Easy-to-use graphical interface
- **🛡️ Safe Preview Mode**: Dry-run capability to preview changes before execution
- **⚙️ Fully Configurable**: Customizable rules and settings via JSON files
- **🚀 Zero Dependencies**: Uses only Python standard library
- **📱 Cross-Interface**: Command-line, GUI, and automation interfaces

## 📸 Screenshots

| GUI Interface | File Organization | Automation Setup |
|---------------|-------------------|------------------|
| ![GUI](https://via.placeholder.com/250x200/4C566A/88C0D0?text=GUI+Interface) | ![Organization](https://via.placeholder.com/250x200/4C566A/A3BE8C?text=File+Organization) | ![Automation](https://via.placeholder.com/250x200/4C566A/EBCB8B?text=Task+Scheduler) |

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Automation Setup](#-automation-setup)
- [GUI Usage](#-gui-usage)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ⚡ Quick Start

### 🎬 One-Click Demo
```bash
# Clone the repository
git clone https://github.com/AshutoshkumarVesit/SmartFileSort.git
cd SmartFileSort

# Run instant demo
QUICK_START.bat
```

### 🖥️ GUI Application
```bash
python gui/gui_app.py
```

### 🤖 Setup Automation
Right-click `scripts/setup_scheduler.ps1` → "Run with PowerShell" (as Administrator)

![Quick Start Demo](https://via.placeholder.com/600x100/5E81AC/D8DEE9?text=Quick+Start+Demo+GIF+Coming+Soon)

## 🛠️ Installation

### Prerequisites

- **Python 3.7+** (Download from [python.org](https://www.python.org/downloads/))
- **Windows 10/11** (for Task Scheduler automation)

### Setup

1. **Download/Clone the project**:
   ```bash
   git clone https://github.com/yourusername/SmartFileSort.git
   cd SmartFileSort
   ```

2. **No additional dependencies required** - uses only Python standard library!

3. **Test the installation**:
   ```bash
   python src/smartfilesort.py --help
   ```

## 📖 Usage

### Command Line Interface

**Basic usage:**
```bash
python src/smartfilesort.py "C:\Users\YourName\Downloads" "C:\Users\YourName\Documents\OrganizedFiles"
```

**Preview mode (recommended first run):**
```bash
python src/smartfilesort.py "C:\Users\YourName\Downloads" "C:\Users\YourName\Documents\OrganizedFiles" --dry-run
```

**With custom configuration:**
```bash
python src/smartfilesort.py "C:\Users\YourName\Downloads" "C:\Users\YourName\Documents\OrganizedFiles" --config config/custom_rules.json
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `source` | Source directory to organize (required) |
| `target` | Target directory for organized files (required) |
| `--dry-run` | Preview mode - shows what would be moved without actually moving files |
| `--config` | Path to custom configuration file |

## ⚙️ Configuration

### File Classification Rules (`config/rules.json`)

Customize how files are categorized by editing the rules file:

```json
{
    "Documents": {
        "extensions": [".pdf", ".doc", ".docx", ".txt", ".xlsx"],
        "patterns": [
            "invoice.*\\.(pdf|doc|docx)",
            "resume.*\\.(pdf|doc|docx)",
            "report.*\\.(pdf|doc|docx|txt)"
        ]
    },
    "Images": {
        "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "patterns": [
            "screenshot.*\\.(jpg|jpeg|png)",
            "photo.*\\.(jpg|jpeg|png)"
        ]
    }
}
```

### Application Settings (`config/settings.json`)

Global application behavior settings:

```json
{
    "general": {
        "source_directory": "C:\\Users\\%USERNAME%\\Downloads",
        "target_directory": "C:\\Users\\%USERNAME%\\Documents\\OrganizedFiles",
        "dry_run": false,
        "ignore_hidden_files": true
    },
    "behavior": {
        "handle_duplicates": "rename",
        "max_duplicate_counter": 100
    }
}
```

## 🤖 Automation Setup

### Windows Task Scheduler Setup

**Option 1: Automatic Setup (Recommended)**
1. Right-click `scripts/setup_scheduler.ps1`
2. Select "Run with PowerShell"
3. Choose "Yes" when prompted for Administrator access
4. Follow the prompts

**Option 2: Manual Setup**
1. Open Task Scheduler (`taskschd.msc`)
2. Create Basic Task
3. Set trigger (e.g., daily at startup)
4. Set action to run `scripts/run_organizer.bat`

### Removing Automation
Run `scripts/remove_scheduler.ps1` as Administrator to remove the scheduled task.

## 🖥️ GUI Usage

Launch the graphical interface:
```bash
python gui/gui_app.py
```

### GUI Features

- **📁 Directory Selection**: Easy browse buttons for source/target directories
- **🔍 Preview Mode**: See what files would be organized before running
- **📊 Live Logs**: Real-time operation feedback
- **⚙️ Settings**: Quick access to configuration files
- **📈 Progress Tracking**: Visual progress bars and status updates

### GUI Tabs

1. **File Organizer**: Main operation interface
2. **View Logs**: Browse operation history and logs
3. **Settings**: Access configuration files
4. **About**: Project information and help

## 📊 Examples

### Before Organization
```
Downloads/
├── invoice_2025.pdf
├── screenshot1.png
├── project_code.py
├── lecture_video.mp4
├── resume.docx
├── music_song.mp3
└── backup_files.zip
```

### After Organization
```
OrganizedFiles/
├── Documents/
│   ├── invoice_2025.pdf
│   └── resume.docx
├── Images/
│   └── screenshot1.png
├── Code/
│   └── project_code.py
├── Videos/
│   └── lecture_video.mp4
├── Audio/
│   └── music_song.mp3
└── Archives/
    └── backup_files.zip
```

### Operation Log (`logs/operations_YYYYMMDD_HHMMSS.csv`)
```csv
timestamp,source,target,category,status
2025-09-21 22:05:12,Downloads/invoice.pdf,Documents/invoice.pdf,Documents,Success
2025-09-21 22:05:13,Downloads/code.py,Code/project_code.py,Code,Success
2025-09-21 22:05:14,Downloads/photo.jpg,Images/screenshot1.png,Images,Success
```

## 🔧 Troubleshooting

### Common Issues

**1. "Permission Denied" Error**
- **Cause**: File is locked or in use
- **Solution**: Close applications using the file, or run as Administrator

**2. "Source directory not found"**
- **Cause**: Invalid directory path
- **Solution**: Check the path exists and is accessible

**3. "Import module not found" (GUI)**
- **Cause**: Running GUI from wrong directory
- **Solution**: Run from project root directory or use `cd SmartFileSort` first

**4. Scheduled task not running**
- **Cause**: Insufficient permissions or wrong paths
- **Solution**: Re-run `setup_scheduler.ps1` as Administrator

### Debug Mode

Enable detailed logging by setting log level to DEBUG in the configuration.

### Log Files Location

- **Operation logs**: `logs/operations_YYYYMMDD_HHMMSS.csv`
- **Application logs**: `logs/file_sort_YYYYMMDD_HHMMSS.log`
- **Scheduler logs**: `logs/scheduler_run.log`

## 🎯 Use Cases

- **Personal**: Organize Downloads folder automatically
- **Business**: Clean up shared network drives
- **Development**: Organize project files and downloads
- **Media Management**: Sort photos, videos, and audio files
- **Document Management**: Organize invoices, reports, and paperwork

## 🔮 Advanced Features

### Custom File Categories

Add new categories by editing `config/rules.json`:

```json
"Presentations": {
    "extensions": [".ppt", ".pptx", ".key"],
    "patterns": ["presentation.*\\.(ppt|pptx)", "slides.*\\.(ppt|pptx)"]
}
```

### Email Notifications (Future Enhancement)

Configure email alerts in `config/settings.json` when organization completes.

### Machine Learning Classification (Future Enhancement)

Upgrade to semantic file classification using content analysis.

## 📝 Project Structure

```
SmartFileSort/
├── src/
│   └── smartfilesort.py          # Main application logic
├── gui/
│   └── gui_app.py               # Tkinter GUI interface
├── config/
│   ├── rules.json               # File classification rules
│   └── settings.json            # Application settings
├── scripts/
│   ├── run_organizer.bat        # Automation batch script
│   ├── setup_scheduler.ps1      # Task scheduler setup
│   └── remove_scheduler.ps1     # Task scheduler removal
├── logs/                        # Generated log files
├── tests/                       # Test files and demos
└── README.md                    # This file
```

## 🚀 Why SmartFileSort?

Perfect for demonstrating **automation and scripting skills** for:
- **Job Applications**: Shows real-world problem solving
- **Portfolio Projects**: Demonstrates Python, automation, and GUI development
- **Daily Productivity**: Actually useful tool for file management
- **Learning**: Great example of modular Python project structure

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Email**: [Your email address]
- **Documentation**: This README and inline code comments

---

**Created by Ashutosh Kumar • September 2025**  
*Automated File Organization Made Simple* 🚀

---

## 🌟 Star This Project!

If this project helped you, please ⭐ star it on GitHub and share it with others!

[![GitHub stars](https://img.shields.io/github/stars/AshutoshkumarVesit/SmartFileSort.svg?style=social&label=Star)](https://github.com/AshutoshkumarVesit/SmartFileSort)
[![GitHub forks](https://img.shields.io/github/forks/AshutoshkumarVesit/SmartFileSort.svg?style=social&label=Fork)](https://github.com/AshutoshkumarVesit/SmartFileSort/fork)