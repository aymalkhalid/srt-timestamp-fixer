# SRT Timestamp Fixer - User Guide

## Overview
SRT Timestamp Fixer corrects malformed SRT subtitle timestamps. Available as:
- Desktop GUI (.exe and Python)
- Web Application (.exe and Python)
- Command Line (Python)

## How to Use

### Desktop GUI
- **Windows:** Double-click `SRT_Timestamp_Fixer_GUI.exe` or `src/launch_gui.bat`
- **Linux/macOS:** Run `src/launch_gui.sh`

### Web Application
- **Windows:** Double-click `SRT_Timestamp_Fixer_Web.exe` or `src/launch_web.bat`
- **Linux/macOS:** Run `src/launch_web.sh`
- Open browser at `http://localhost:5000`

### Command Line
```bash
python src/convert_to_srt.py -i input.srt -o output.srt
```

## What Gets Fixed
- Missing hours in timestamps
- Missing arrows in timestamp lines
- Malformed timestamp formats
- Always outputs valid SRT: `HH:MM:SS,mmm --> HH:MM:SS,mmm`

## Important Notes
- Original files are backed up as `.bak`
- UTF-8 encoding is used
- Web app supports files up to 16MB
- Executables require no Python installation

## Troubleshooting

1. **Python not found:**
   - Install Python from [python.org](https://python.org)
   - Add Python to your system PATH
2. **Module not found:**
   - Launcher scripts auto-install dependencies
   - If issues persist, run: `pip install -r requirements.txt`
3. **Executable doesn't start:**
   - Check antivirus or try running as administrator
4. **Web app doesn't open:**
   - Check port 5000, try a different browser, or check firewall

## Support
- Check this guide first
- Review the project's README.md
- Check the issue tracker on GitHub
- Create a new issue with details if needed

---

**Happy subtitle fixing!** 🎬✨
