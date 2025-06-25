# SRT Timestamp Fixer

A comprehensive toolkit for fixing malformed SRT subtitle timestamps. Available as command-line tool, desktop GUI applications, and web application.

## ✨ Features

- **Fix missing hours**: `01:30,500` → `00:01:30,500`
- **Add missing arrows**: `01:30,500  01:31,500` → `00:01:30,500 --> 00:01:31,500`
- **Standardize format**: Ensures proper `HH:MM:SS,mmm --> HH:MM:SS,mmm` format
- **Multiple interfaces**: CLI, Basic GUI, Modern GUI, and Web App
- **Safe processing**: Creates backups and preserves original files
- **Real-time preview**: See changes before applying them

## 🚀 Quick Start

### 1. Automatic Setup (Recommended)
```bash
python setup.py
```
This will guide you through installing all components and create launcher scripts.

### 2. Manual Installation
```bash
# Install optional dependencies
pip install -r requirements.txt

# Or install individual components:
pip install customtkinter Pillow  # For Modern GUI
pip install Flask                 # For Web App
```

## 📱 Available Interfaces

### 1. Command Line Interface (CLI)
```bash
python convert_to_srt.py
# or
./launch_cli.sh
```
- **Best for**: Automation, scripting, power users
- **Requirements**: Python 3.7+ (no additional packages)

### 2. Basic Desktop GUI
```bash
python srt_fixer_gui.py
# or
./launch_gui.sh
```
- **Best for**: Simple, reliable desktop interface
- **Requirements**: Python 3.7+ with tkinter (built-in)
- **Features**: File selection, progress tracking, results display

### 3. Modern Desktop GUI
```bash
python srt_fixer_modern.py
# or
./launch_modern.sh
```
- **Best for**: Beautiful, modern desktop experience
- **Requirements**: `customtkinter`, `Pillow`
- **Features**: Dark/light themes, modern styling, smooth animations

### 4. Web Application
```bash
python srt_fixer_web.py
# or
./launch_web.sh
```
Then open: http://localhost:5000

- **Best for**: Browser-based, cross-platform access
- **Requirements**: `Flask`
- **Features**: Drag & drop, live preview, responsive design

## 🔧 What It Fixes

| Issue | Before | After |
|-------|--------|--------|
| Missing hours | `01:30,500 --> 01:31,500` | `00:01:30,500 --> 00:01:31,500` |
| Missing arrow | `01:30,500  01:31,500` | `00:01:30,500 --> 00:01:31,500` |
| Single digit minutes | `1:30,500 --> 2:00,500` | `00:01:30,500 --> 00:02:00,500` |
| Mixed formats | Various inconsistent formats | Standardized SRT format |

## 📋 Usage Examples

### CLI Mode
```python
# Process input.txt and create output.srt
python convert_to_srt.py

# The script will:
# 1. Read from input.txt
# 2. Fix timestamp formatting
# 3. Create output.srt with fixed timestamps
# 4. Create backup of original file
```

### GUI Modes
1. Launch the application
2. Click "Browse" or drag & drop your SRT file
3. (Optional) Click "Preview Changes" to see what will be fixed
4. Click "Fix Timestamps" to process the file
5. Download or save the fixed file

### Web Mode
1. Start the web server: `python srt_fixer_web.py`
2. Open http://localhost:5000 in your browser
3. Drag & drop your SRT file or click to browse
4. Preview changes or directly process the file
5. Download the fixed file

## 📁 File Structure

```
srt_script/
├── convert_to_srt.py          # Core CLI script
├── srt_fixer_gui.py           # Basic desktop GUI
├── srt_fixer_modern.py        # Modern desktop GUI  
├── srt_fixer_web.py           # Web application
├── setup.py                   # Installation script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── input.txt                  # Sample input file
├── output.srt                 # Generated output file
└── launch_*.sh               # Launcher scripts (created by setup)
```

## 🛠️ Technical Details

### Core Algorithm
1. **Detection**: Find lines containing "-->" or timestamp patterns
2. **Analysis**: Check left and right timestamps for format issues
3. **Fixing**: Convert `MM:SS,mmm` to `HH:MM:SS,mmm` format
4. **Validation**: Ensure proper SRT compliance

### Supported Formats
- **Input**: `.srt`, `.txt` files with subtitle content
- **Output**: Properly formatted `.srt` files
- **Encoding**: UTF-8 (handles international characters)

### Error Handling
- Invalid file formats
- Corrupted timestamps
- Missing files
- Permission issues
- Large file processing

## 🔍 Preview Feature

All GUI and web interfaces include a preview feature that shows:
- Number of issues found
- Line numbers with problems
- Original vs. fixed timestamps
- Types of issues (missing hours, missing arrows, etc.)

## 🔒 Security & Privacy

- **Local processing**: All files processed locally on your machine
- **No data collection**: No files or data sent to external servers
- **Temporary files**: Web app automatically cleans up temporary files
- **Backup creation**: Original files preserved with automatic backups

## 🐛 Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'customtkinter'"**
```bash
pip install customtkinter Pillow
```

**"ModuleNotFoundError: No module named 'flask'"**
```bash
pip install Flask
```

**"tkinter not found" (Linux)**
```bash
# Ubuntu/Debian:
sudo apt-get install python3-tk

# CentOS/RHEL:
sudo yum install tkinter
```

**Permission denied on launcher scripts**
```bash
chmod +x launch_*.sh
```

### Performance Tips
- For large files (>1000 lines), use CLI mode for best performance
- Web mode is slower due to browser overhead but more convenient
- Modern GUI may use more memory due to advanced styling

## 📊 Supported Timestamp Formats

### Input Formats (automatically detected and fixed):
- `MM:SS,mmm --> MM:SS,mmm` (missing hours)
- `M:SS,mmm --> MM:SS,mmm` (missing hours + single digit minute)
- `MM:SS,mmm  MM:SS,mmm` (missing arrow)
- `HH:MM:SS,mmm --> MM:SS,mmm` (mixed format)

### Output Format (standardized):
- `HH:MM:SS,mmm --> HH:MM:SS,mmm`

## 🎯 Future Enhancements

- [ ] Batch processing for multiple files
- [ ] Support for other subtitle formats (VTT, ASS)
- [ ] Timestamp validation and gap detection
- [ ] Advanced timing adjustments
- [ ] Cloud deployment options
- [ ] Mobile app version

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure you have the correct Python version (3.7+)
3. Verify all dependencies are installed
4. Check file permissions and paths

---

**Happy subtitle fixing! 🎬✨**
