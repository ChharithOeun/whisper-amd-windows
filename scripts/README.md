# Scripts

Utility scripts for Whisper on AMD Windows.

## transcribe.py

Main transcription script. Automatically detects DirectML GPU and falls back to CPU if needed.

### Usage

```bash
python transcribe.py path/to/audio.mp3
python transcribe.py audio.wav --model medium
python transcribe.py meeting.m4a --language en --device directml
```

### Arguments

| Argument | Default | Options | Description |
|---|---|---|---|
| `audio_path` | (required) | Any file | Path to audio file (MP3, WAV, M4A, FLAC, OGG, WMA) |
| `--model` | `base` | tiny, base, small, medium, large | Whisper model size |
| `--device` | `auto` | auto, directml, cuda, cpu | Device to use |
| `--language` | `None` | ISO-639-1 code | Language (auto-detect if not set) |
| `--compute-type` | `float16` | float16, float32, int8 | Precision (int8 uses less VRAM) |
| `--format` | `both` | txt, srt, both | Output format |

### Examples

**Transcribe with auto GPU detection:**
```bash
python transcribe.py podcast.mp3
```

**Transcribe large file with memory optimization:**
```bash
python transcribe.py large_meeting.wav --model medium --compute-type int8
```

**Force CPU (for testing):**
```bash
python transcribe.py audio.mp3 --device cpu
```

**Transcribe German audio:**
```bash
python transcribe.py interview_german.mp3 --language de
```

### Output

Generates two files in the same directory as input:
- `{basename}.txt` — Plain text transcript
- `{basename}.srt` — SRT subtitle file with timestamps

```
✓ Transcription successful!
Saved: podcast.txt
Saved: podcast.srt
```

---

## benchmark.py

Performance benchmarking tool. Tests each Whisper model and reports speed, memory, and device info.

### Usage

```bash
python benchmark.py
python benchmark.py --device cpu
python benchmark.py --duration 120 --models base,small,medium
```

### Arguments

| Argument | Default | Description |
|---|---|---|
| `--device` | `auto` | Device to benchmark (auto, directml, cuda, cpu) |
| `--duration` | `60` | Test audio duration in seconds |
| `--models` | `tiny,base,small,medium` | Comma-separated models to test |

### Output

Table with:
- **Model** — Whisper model size
- **Size (MB)** — Model size on disk
- **Load (s)** — Time to load model
- **Inference (s)** — Time to transcribe test audio
- **Speed** — Realtime factor (x realtime)
- **Memory (MB)** — VRAM/RAM used

### Examples

**Benchmark all models:**
```bash
python benchmark.py
```

**Benchmark only on CPU:**
```bash
python benchmark.py --device cpu
```

**Benchmark with 2-minute test audio:**
```bash
python benchmark.py --duration 120
```

### Interpreting Results

```
Whisper Benchmark Results — Device: DIRECTML
============================================================
Model        Size (MB)    Load (s)     Inference (s)   Speed            Memory (MB)
----
tiny         39           0.45         1.32            45.5x            210.2
base         140          0.62         1.68            17.9x            412.1
small        466          1.15         4.95            12.1x            1205.3
medium       1500         2.10         7.53            8.0x             2340.1

Summary:
  Average speed: 20.9x realtime
  Fastest model: tiny at 45.5x realtime
  Most capable: medium at 8.0x realtime

Recommendations:
  ✓ Excellent GPU acceleration detected — use larger models (medium/large)
```

**Speed interpretation:**
- `>30x realtime` — Excellent; can use large models
- `10–30x realtime` — Good; medium model recommended
- `5–10x realtime` — Decent; small model recommended
- `<5x realtime` — Limited; consider CPU optimization or smaller models
- `<1x realtime` — CPU only; no GPU acceleration

---

## verify_gpu.py

Setup verification utility. Checks GPU detection, driver status, dependencies, and Python version.

### Usage

```bash
python verify_gpu.py
```

### Output

Checks:
- ✓ **Platform** — Windows version
- ✓ **Python Version** — 3.10+
- ✓ **ONNX Runtime** — Required for GPU
- ✓ **faster-whisper** — Whisper engine
- ✓ **AMD GPU Detected** — GPU hardware
- ✓ **DirectML** — AMD GPU support
- ✗ **CUDA** — NVIDIA GPU support (not needed on AMD)

### Example Output

```
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
======================================================================
```

### Troubleshooting

If checks fail, run:
```bash
python verify_gpu.py
```

The script provides guidance on fixing issues.

---

## Quick Reference

### For New Users

1. **First time setup:**
   ```bash
   python verify_gpu.py      # Check setup
   python scripts/benchmark.py   # See performance
   ```

2. **Transcribe audio:**
   ```bash
   python transcribe.py audio.mp3
   ```

### For Advanced Users

1. **Batch transcription:**
   ```bash
   for file in *.mp3; do
       python transcribe.py "$file" --model medium
   done
   ```

2. **Memory-optimized transcription:**
   ```bash
   python transcribe.py large_file.wav --compute-type int8 --model medium
   ```

3. **Force CPU (for testing):**
   ```bash
   python transcribe.py audio.mp3 --device cpu --model tiny
   ```

---

## Dependencies

All scripts require:
- Python 3.10, 3.11, or 3.12
- `faster-whisper` — Optimized Whisper inference
- `onnxruntime-directml` — DirectML GPU support for AMD
- `numpy` — Numeric operations

Install with:
```bash
pip install -r ../requirements.txt
```

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Error (file not found, GPU init failed, etc.) |

---

## See Also

- [README.md](../README.md) — Full documentation
- [INSTALL.md](../INSTALL.md) — Step-by-step setup
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Contributing guidelines
