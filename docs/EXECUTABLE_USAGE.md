# SRT Fixer - Executable Usage Guide

## 📥 Quick Download & Run

1. **Download**: Click on `SRT_TIMESTAMP_FIXER.exe` in this repository
2. **Save**: Choose a location on your computer (Desktop recommended)
3. **Run**: Double-click the downloaded file

## 🚨 Security Warning (Normal)

When you first run the executable, Windows may show a security warning:

```
Windows protected your PC
Microsoft Defender SmartScreen prevented an unrecognized app from starting.
```

**This is normal!** Follow these steps:
1. Click **"More info"**
2. Click **"Run anyway"**

The executable is safe and contains no malware. This warning appears because the executable is not digitally signed by Microsoft.

## 🖥️ Using the Application

### Step 1: Launch
- Double-click `SRT_TIMESTAMP_FIXER.exe`
- The GUI window will open

### Step 2: Select Your File
- Click **"Browse"** button
- Navigate to your SRT file (or text file with subtitles)
- Select the file and click **"Open"**

### Step 3: Preview (Optional)
- Click **"Preview Changes"** to see what will be fixed
- Review the changes in the preview window

### Step 4: Fix Timestamps
- Click **"Fix Timestamps"** to process the file
- The fixed file will be saved as `output.srt` in the same directory
- Original file is automatically backed up

### Step 5: Done!
- Your fixed SRT file is ready to use
- The application will show a success message with the file location

## 🔧 Common Issues

### "App can't run on your PC"
- You're likely on a 32-bit system or older Windows version
- The executable requires Windows 7+ (64-bit)
- Use the Python version instead

### Antivirus Software Blocking
- Some antivirus software may flag the executable as suspicious
- Add `srt_fixer_gui.exe` to your antivirus whitelist/exceptions
- This is a false positive common with PyInstaller executables

### Slow Performance
- Large files (>1000 lines) may take a few seconds to process
- This is normal - the executable includes the entire Python runtime

## 💡 Tips

- **File Types**: Works with `.srt`, `.txt`, and other text files containing subtitles
- **Backup**: Your original file is always preserved (renamed with `.backup` extension)
- **Output**: Fixed file is saved as `output.srt` in the same folder as your input file
- **Encoding**: Handles international characters and special symbols correctly

## 🆘 Need Help?

If the executable doesn't work for you:
1. Check the main [README.md](README.md) for alternative installation methods
2. Try the Python version for more flexibility
3. The web version works on any platform with a browser

---

**Happy subtitle fixing! 🎬✨**
