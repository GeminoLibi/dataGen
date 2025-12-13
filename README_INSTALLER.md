# Installation Guide

## Option 1: Standalone Executable (Simple)

If someone just receives `CaseGenerator.exe`:

1. **Double-click** `CaseGenerator.exe`
2. A console window will open showing server status
3. Your browser should automatically open to `http://localhost:5000`
4. If browser doesn't open, manually navigate to `http://localhost:5000`

**Requirements:**
- Windows 10 or later
- No Python installation needed (everything is bundled)
- No additional dependencies required

**Note:** The executable is self-contained (~60MB) and includes all dependencies.

## Option 2: Installer Package (Recommended for Distribution)

### Creating the Installer

1. **Build the executable:**
   ```bash
   build.bat
   ```

2. **Create installer** (requires Inno Setup):
   ```bash
   create_installer.bat
   ```
   
   Or do both at once:
   ```bash
   build_and_install.bat
   ```

3. **Distribute:** `installer\CaseDataGenerator-Setup.exe`

### Installing from Installer

1. Run `CaseDataGenerator-Setup.exe`
2. Follow the installation wizard
3. Choose installation location (default: `C:\Program Files\CaseDataGenerator`)
4. Optionally create desktop shortcut
5. Launch from Start Menu or desktop icon

### Installing Inno Setup (for creating installers)

1. Download from: https://jrsoftware.org/isinfo.php
2. Install Inno Setup
3. Add to PATH (or run `create_installer.bat` from Inno Setup directory)

## Option 3: Python Source (For Developers)

1. Install Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python web_interface.py
   ```
   or
   ```bash
   python main.py
   ```

## Troubleshooting

### Executable Won't Launch

1. **Check console window:** The exe now shows a console window with error messages
2. **Check port 5000:** Make sure nothing else is using port 5000
3. **Firewall:** Windows Firewall may block the application
4. **Antivirus:** Some antivirus software may flag PyInstaller executables

### Browser Doesn't Open

- Manually navigate to: `http://localhost:5000`
- Check the console window for error messages
- Try a different browser

### Port Already in Use

- Close other applications using port 5000
- Or modify `web_interface.py` to use a different port

## Testing the Executable

Run `test_exe.bat` to test the executable with automatic browser opening.

## Distribution

### What to Send

**Option A: Just the EXE**
- Send `dist\CaseGenerator.exe` (~60MB)
- User double-clicks to run
- No installation needed

**Option B: Installer**
- Send `installer\CaseDataGenerator-Setup.exe`
- Professional installation experience
- Can create shortcuts and Start Menu entries

### File Sizes

- `CaseGenerator.exe`: ~60MB (standalone, no dependencies)
- `CaseDataGenerator-Setup.exe`: ~45MB (compressed installer)

## Security Notes

- The executable is unsigned (Windows may show a warning)
- For production distribution, consider code signing
- Antivirus software may flag PyInstaller executables (false positive)

