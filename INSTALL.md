# Installation Guide

Complete step-by-step installation of Whisper + DirectML on Windows for AMD GPUs.

## Prerequisites Check

Before starting, verify:
- Windows 10 (build 19041+) or Windows 11
- AMD GPU with ≥4GB VRAM (8GB+ recommended)
- Internet connection for downloads
- Administrator access (for driver updates)

## Step 1: Update AMD Drivers

### Verify Current Driver

1. Right-click desktop → **AMD Radeon Settings** (or AMD Software)
2. Note the **Driver Version** shown
3. Go to https://www.amd.com/en/support
4. Download the latest **ADRENALIN** driver for your GPU

### Install Driver

1. Run the downloaded installer
2. Select **Express** (recommended) or Custom installation
3. Restart Windows
4. Verify: Open AMD Radeon Settings → you should see your GPU

**For Radeon RX 5700 XT**: Ensure driver version 23.5.1 or later (DirectML support improved).

## Step 2: Install Python

### Download Python 3.11 (Recommended)

1. Visit https://www.python.org/downloads/release/python-3110/
2. Download **Windows installer (64-bit)**
3. Run the installer

### Configure Installation

**IMPORTANT**: Check **"Add Python to PATH"**

Other options:
- ✓ Install for all users (recommended)
- ✓ Add python.exe to PATH (must check)
- Leave other options default

### Verify Installation

Open **Command Prompt** (Win+R → `cmd` → Enter):

```cmd
python --version
pip --version
```

Both should display version numbers (Python 3.10+).

## Step 3: Clone Repository

### Using Git

If you have Git installed:

```cmd
git clone https://github.com/ChharithOeun/whisper-amd-windows.git
cd whisper-amd-windows
```

### Without Git

1. Go to https://github.com/ChharithOeun/whisper-amd-windows
2. Click **Code** → **Download ZIP**
3. Extract to a folder (e.g., `C:\Users\YourName\Documents\whisper-amd-windows`)
4. Open Command Prompt in that folder

## Step 4: Create Virtual Environment

In Command Prompt (in the repo folder):

```cmd
python -m venv venv
```

Wait ~30 seconds for it to complete.

### Activate Virtual Environment

```cmd
venv\Scripts\activate
```

You should see `(venv)` at the start of the command prompt line.

## Step 5: Install Dependencies

**IMPORTANT: Keep virtual environment activated** (venv should be in prompt).

### Upgrade pip

```cmd
python -m pip install --upgrade pip
```

### Install Core Libraries

```cmd
pip install faster-whisper onnxruntime-directml
```

This installs:
- **faster-whisper** (~15 MB) — Optimized Whisper
- **onnxruntime-directml** (~80 MB) — DirectML GPU support
- Dependencies (numpy, etc.)

Total download: ~100–150 MB. Takes 2–5 minutes depending on internet.

### Verify Installation

```cmd
python -c "import faster_whisper; import onnxruntime; print('OK')"
```

Should output `OK`.

## Step 6: Verify GPU Detection

```cmd
python scripts/verify_gpu.py
```

### Expected Output (AMD GPU)

```
======================================================================
GPU Setup Verification Report
======================================================================
✓ Platform                     Windows 11
✓ Python Version               Python 3.11.0
✓ ONNX Runtime                 onnxruntime 1.17.0
✓ faster-whisper               faster-whisper 0.10.0
✓ AMD GPU Detected             AMD GPU found: AMD Radeon RX 5700 XT
✓ DirectML (AMD GPU Support)   DirectML available
✗ CUDA (NVIDIA GPU Support)    CUDA not in available providers

Summary:
Recommended device: DirectML (AMD GPU) - RECOMMENDED

✓ All checks passed! Setup is complete.
```

### If DirectML Not Detected

**Option A: Reinstall onnxruntime-directml**

```cmd
pip uninstall onnxruntime-directml onnxruntime -y
pip install onnxruntime-directml
```

**Option B: Update Windows**

- Check for Windows updates (Settings → Update & Security)
- Ensure DirectX 12 is available (most Windows 10+ systems have it)

**Option C: Use CPU Fallback**

For now, you can use CPU:
```cmd
python scripts/transcribe.py audio.mp3 --device cpu
```

(This will be slow but confirms the rest of the setup works.)

## Step 7: Test Transcription

### Get Sample Audio

Create a test audio file or use an existing MP3/WAV from your computer.

Example with a 30-second test:
```cmd
python scripts/transcribe.py C:\path\to\your\audio.mp3 --model base
```

### Expected Output

```
Loading Whisper model 'base'...
Device: directml
Transcribing: audio.mp3

Transcription complete!
Audio duration: 30.5s
Processing time: 1.8s
Speed: 17.0x realtime
Detected language: en
Saved: C:\path\to\your\audio.txt
Saved: C:\path\to\your\audio.srt
```

### Check Results

Look for two new files:
- `audio.txt` — Plain text transcript
- `audio.srt` — Subtitles with timestamps (open in a text editor)

## Step 8: Benchmark Your GPU (Optional)

See real-world performance on your hardware:

```cmd
python scripts/benchmark.py
```

Runs transcription tests on multiple model sizes. Takes 5–10 minutes.

### Sample Output

```
============================================================
Whisper Benchmark Results — Device: DIRECTML
============================================================
Model        Size (MB)    Load (s)     Inference (s)   Speed            Memory (MB)
----
tiny         39           0.45         1.32            45.5x            210.2
base         140          0.62         1.68            17.9x            412.1
small        466          1.15         4.95            12.1x            1205.3
medium       1500         2.10         7.53            8.0x             2340.1
============================================================

Summary:
  Average speed: 20.9x realtime
  Fastest model: tiny at 45.5x realtime
  Most capable: medium at 8.0x realtime

Recommendations:
  ✓ Excellent GPU acceleration detected — use larger models (medium/large)
```

## Troubleshooting

### "venv not recognized"

**Problem**: Virtual environment not activated.

**Fix**: Run this in the repo folder:
```cmd
venv\Scripts\activate
```

### "No module named 'faster_whisper'"

**Problem**: Dependencies not installed or venv not activated.

**Fix**:
1. Activate venv: `venv\Scripts\activate`
2. Reinstall: `pip install faster-whisper onnxruntime-directml`

### "DirectML not available"

**Problem**: DirectML provider not detected.

**Fix**:
1. Update AMD driver to latest
2. Reinstall: `pip uninstall onnxruntime-directml && pip install onnxruntime-directml`
3. Restart Windows
4. Run `python scripts/verify_gpu.py` again

### Transcription is very slow

**Problem**: Using CPU instead of GPU.

**Fix**: Check benchmark results:
```cmd
python scripts/benchmark.py
```

If showing "CPU" instead of "DirectML", go back to troubleshooting DirectML.

### Out of Memory Error

**Problem**: GPU VRAM full with large model.

**Fix**: Use smaller model:
```cmd
python scripts/transcribe.py audio.mp3 --model small
```

Or enable memory optimization:
```cmd
python scripts/transcribe.py audio.mp3 --compute-type int8
```

## Next Steps

### Batch Transcription

Transcribe multiple files:
```cmd
for %f in (*.mp3) do python scripts/transcribe.py "%f"
```

### Customize Model

Whisper models by accuracy/speed:
- `tiny` — 45x faster, lower accuracy
- `base` — 18x faster, good for English
- `small` — 12x faster, better multilingual
- `medium` — 8x faster, high accuracy ← recommended
- `large` — 4x faster, highest accuracy (2.9GB VRAM needed)

```cmd
python scripts/transcribe.py audio.mp3 --model large
```

### Transcribe Non-English Audio

Specify language code (ISO-639-1):
```cmd
python scripts/transcribe.py audio_spanish.mp3 --language es
python scripts/transcribe.py audio_french.mp3 --language fr
```

Or let Whisper auto-detect:
```cmd
python scripts/transcribe.py audio_unknown.mp3
```

## Getting Help

- **Setup issues**: See README → Troubleshooting
- **Feature requests**: GitHub Issues
- **GPU testing results**: Share your benchmark output!

## Uninstall

To completely remove:

```cmd
cd ..
rmdir /s whisper-amd-windows
```

The installation is portable — just delete the folder.

---

**Ready?** Start transcribing:
```cmd
python scripts/transcribe.py audio.mp3
```
