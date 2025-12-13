# Building the Case Generator Executable

## Prerequisites

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Building for Windows

1. Run the build script:
   ```bash
   build.bat
   ```

   Or manually:
   ```bash
   pyinstaller build_executable.spec
   ```

2. The executable will be in the `dist` folder as `CaseGenerator.exe`

## Building for Linux

1. Make the build script executable:
   ```bash
   chmod +x build.sh
   ```

2. Run the build script:
   ```bash
   ./build.sh
   ```

   Or manually:
   ```bash
   pyinstaller build_executable.spec
   ```

3. The executable will be in the `dist` folder as `CaseGenerator`

## Running the Executable

### Windows
Double-click `CaseGenerator.exe` or run from command line:
```bash
dist\CaseGenerator.exe
```

### Linux
```bash
./dist/CaseGenerator
```

The web interface will start on `http://localhost:5000`

## Notes

- The executable includes all dependencies and can run on systems without Python installed
- Generated cases will be saved in a `cases` folder in the same directory as the executable
- The first run may take a moment to start as it extracts bundled files

