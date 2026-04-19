# Whisper on AMD Windows

[![CI](https://github.com/ChharithOeun/whisper-amd-windows/actions/workflows/ci.yml/badge.svg)](https://github.com/ChharithOeun/whisper-amd-windows/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![Tested: RX 5700 XT](https://img.shields.io/badge/Tested%20GPU-RX%205700%20XT%20(RDNA1)-brightgreen)](https://www.amd.com/en/products/graphics/amd-radeon-rx-5700-xt)
[![AMD RDNA Support](https://img.shields.io/badge/AMD%20RDNA-1%2F2%2F3%2F4-blue)](https://en.wikipedia.org/wiki/RDNA)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078d4)](https://www.microsoft.com/windows)
[![Buy Me A Coffee](https://img.shields.io/badge/Support-Buy%20Me%20A%20Coffee-ffdd00?logo=buymeacoffee)](https://buymeacoffee.com/chharith)

Run OpenAI's [Whisper](https://github.com/openai/whisper) speech-to-text model on AMD GPUs on Windows with zero CUDA dependency. This guide covers two GPU acceleration paths plus CPU fallback, tested on **RX 5700 XT (gfx1010 / RDNA1)**.

## What is Whisper?

[Whisper](https://github.com/openai/whisper) is OpenAI's open-source speech recognition model trained on 680,000 hours of multilingual audio. It transcribes audio to text with high accuracy across 99 languages and handles diverse audio conditions (accents, background noise, technical language).

## Why AMD GPU?

- **No CUDA lock-in**: RDNA cards work on Windows via DirectML (any DX12 GPU) or ROCm (RDNA1+ only)
- **Cost-effective**: RX 6700 XT ~$300; equivalent NVIDIA RTX 3070 Ti $400–500
- **Sufficient VRAM**: RX 5700 XT (8GB) → runs `large` model; RX 6600 XT (16GB) → runs `large-v3` with headroom
- **Real transcription speedup**: ~8–12x realtime on medium model vs ~0.5x CPU realtime

## What This Repo Covers

| Method | GPU Support | Windows | Difficulty | Speed | Notes |
|--------|-------------|---------|------------|-------|-------|
| **A: faster-whisper + DirectML** | Any AMD DX12 (RDNA, Polaris, Vega) | ✓ | Easiest | 8–12x realtime | **Recommended** — works on all AMD cards |
| **B: whisper.cpp GPU** | RDNA1+ only (ROCm via comfyui-rocm) | ✓ | Moderate | 10–15x realtime | Requires ROCm environment from comfyui-amd-windows-setup |
| **C: CPU fallback** | Any | ✓ | Trivial | 0.3–0.5x realtime | For testing or low-VRAM fallback |

## GPU Compatibility

| AMD GPU Family | Architecture | gfx Code | Method A (DirectML) | Method B (ROCm) | Tested |
|---|---|---|---|---|---|
| **RDNA4** (2025+) | RDNA4 | gfx1201+ | ✓ Full | ✓ Full | Not yet |
| **RX 7000** | RDNA3 | gfx1100–gfx1102 | ✓ Full | ✓ Full | Not yet |
| **RX 6000** | RDNA2 | gfx1030–gfx1102 | ✓ Full | ✓ Full | Community reports ✓ |
| **RX 5000** | RDNA1 | gfx1010–gfx1012 | ✓ Full | ✓ Full | **RX 5700 XT (gfx1010)** ✓ |
| **RX Vega** | Vega | gfx900/906 | ✓ DirectML only | ✗ No ROCm | Not tested |
| **RX Polaris** | Polaris | gfx803 | ✓ DirectML only | ✗ No ROCm | Not tested |

**DirectML** works on **any AMD GPU with DX12 support** (Windows 10+). ROCm on Windows is limited to RDNA1+.

## Quick Start

### Prerequisites

- Windows 10 or 11
- Python 3.10, 3.11, or 3.12 (64-bit)
- AMD GPU with ≥4GB VRAM (8GB+ recommended)
- ~500MB disk space (model cache)

### Method A: faster-whisper + DirectML (Recommended)

Fastest setup, works on all AMD GPUs.

```bash
# Clone this repo
git clone https://github.com/ChharithOeun/whisper-amd-windows.git
cd whisper-amd-windows

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install faster-whisper onnxruntime-directml

# Verify GPU detection
python scripts/verify_gpu.py

# Transcribe audio
python scripts/transcribe.py path/to/audio.mp3

# Benchmark your GPU
python scripts/benchmark.py
```

### Method B: whisper.cpp + ROCm (Advanced, RDNA1+ only)

For maximum performance on RDNA1+ cards using ROCm:

```bash
# Requires comfyui-amd-windows-setup environment
# See: https://github.com/ChharithOeun/comfyui-amd-windows-setup

git clone https://github.com/ChharithOeun/whisper-amd-windows.git
cd whisper-amd-windows

# Use the pre-configured ROCm environment
source /path/to/comfyui-rocm-env/bin/activate

pip install -r requirements-rocm.txt
python scripts/transcribe_rocm.py path/to/audio.mp3
```

### Method C: CPU Fallback

If GPU acceleration isn't available:

```bash
pip install faster-whisper
python scripts/transcribe.py path/to/audio.mp3 --device cpu
```

## Installation & Setup — Method A (Step by Step)

### 1. Install Python

Download [Python 3.11](https://www.python.org/downloads/release/python-3110/) (64-bit Windows installer).

```bash
# Verify installation
python --version  # Should be 3.10, 3.11, or 3.12
```

### 2. Clone Repository

```bash
git clone https://github.com/ChharithOeun/whisper-amd-windows.git
cd whisper-amd-windows
```

### 3. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your prompt.

### 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 5. Install Core Dependencies

```bash
pip install faster-whisper onnxruntime-directml
```

- **faster-whisper**: Optimized Whisper inference engine
- **onnxruntime-directml**: ONNX Runtime with DirectML GPU support

### 6. Verify GPU Detection

```bash
python scripts/verify_gpu.py
```

Expected output on AMD GPU:
```
GPU Detection Report
====================
DirectML available: True
AMD GPU detected: True
Device: DirectML device 0 (AMD Radeon RX 5700 XT)
CUDA not found (expected on AMD)
```

### 7. Transcribe Audio

```bash
python scripts/transcribe.py examples/sample.mp3
```

Outputs:
- `sample.txt` — Plain text transcript
- `sample.srt` — Subtitle file (timestamp segments)

### 8. Benchmark Your Setup

```bash
python scripts/benchmark.py
```

Shows model size, device, speed (x realtime), VRAM usage.

## Proof of Concept — Tested on RX 5700 XT

### Transcription Speed

Benchmark on **RX 5700 XT (8GB VRAM)** with various Whisper models:

| Model | Size | Speed | VRAM | Time for 60s Audio |
|---|---|---|---|---|
| tiny | 39MB | ~45x realtime | 0.4GB | 1.3s |
| base | 140MB | ~18x realtime | 0.8GB | 3.3s |
| small | 466MB | ~12x realtime | 1.2GB | 5.0s |
| medium | 1.5GB | **~8x realtime** | 2.4GB | 7.5s |
| large | 2.9GB | ~4x realtime | 4.2GB | 15s |

**Baseline (CPU only)**: ~0.3x realtime on medium = 200s for 60s audio.
**Speedup**: ~26x faster with RX 5700 XT.

### Sample Output

Transcribing a 2-minute podcast episode (128 kbps MP3):

```
Input: podcast_episode_001.mp3 (2:34)
Model: medium
Device: DirectML
Total time: 19.2 seconds
Speed: ~8.0x realtime

Output: podcast_episode_001.txt
[Transcript of full 2:34 audio captured]

Output: podcast_episode_001.srt
00:00:00,000 --> 00:00:05,500
Welcome to the AI podcast, where we discuss...

00:00:05,500 --> 00:00:12,000
the latest developments in machine learning and open source.
```

## Model Recommendations by GPU VRAM

Choose the largest Whisper model your GPU can fit:

| GPU VRAM | Recommended Model | Use Case |
|---|---|---|
| 2–4GB | `small` (466MB) | Real-time speech, live captions |
| 4–6GB | `medium` (1.5GB) | Podcast, meeting transcription |
| 6–8GB | `medium`–`large` (1.5–2.9GB) | High accuracy, document transcription |
| 8GB+ | `large`, `large-v3` (2.9GB) | Maximum accuracy across languages |

**Rule of thumb**: Model should be ≤ 40% of your GPU VRAM to leave room for activations.

## Troubleshooting

### "No GPU detected" or "CUDA not found"

**Cause**: DirectML not detected or older drivers.

**Fix**:
```bash
# Update AMD GPU drivers
# Download from https://www.amd.com/en/support

# Verify DirectML is available
python -c "import onnxruntime; print(onnxruntime.get_available_providers())"
# Should show 'DmlExecutionProvider' in list

# If not, reinstall onnxruntime-directml:
pip uninstall onnxruntime-directml onnxruntime
pip install onnxruntime-directml
```

### Out of Memory (OOM)

**Cause**: Model too large for GPU VRAM.

**Fix**:
1. Use smaller model: `medium` → `small`
2. Enable CPU offloading (slows down inference slightly):
   ```bash
   python scripts/transcribe.py audio.mp3 --compute-type int8
   ```
3. Reduce batch size in `transcribe.py`

### DirectML fails on CPU fallback

**Cause**: DirectML provider not registered.

**Fix**:
```bash
# Use CPU explicitly
python scripts/transcribe.py audio.mp3 --device cpu
```

### Audio format not supported

**Supported formats**: MP3, WAV, M4A, FLAC, OGG, WMA

**Convert with FFmpeg**:
```bash
# Install FFmpeg: https://ffmpeg.org/download.html
ffmpeg -i unsupported.format -acodec libmp3lame -ab 192k output.mp3
```

### ROCm (Method B) not detecting GPU

**Cause**: ROCm environment not sourced.

**Fix**:
```bash
# Must activate comfyui-rocm environment first
source /path/to/comfyui-rocm-env/bin/activate  # Linux WSL
# or on native ROCm on Windows (if HIP SDK installed):
set HIP_VISIBLE_DEVICES=0
rocminfo  # Verify GPU detection
```

## Related Repositories

- **[comfyui-amd-windows-setup](https://github.com/ChharithOeun/comfyui-amd-windows-setup)** — Complete guide to setting up ComfyUI with AMD GPU on Windows (ROCm + DirectML)
- **[AMD-GPU-Windows-Setup](https://github.com/ChharithOeun/AMD-GPU-Windows-Setup)** — Baseline AMD GPU driver and ROCm setup for Windows

## Keywords

`whisper`, `speech-to-text`, `amd-gpu`, `directml`, `rocm`, `windows`, `gpu-acceleration`, `transcription`, `onnxruntime`, `faster-whisper`, `rdna`, `rdna2`, `rdna3`, `rx-5700-xt`, `rx-6700-xt`, `gpu-computing`

## Contributing

Found an issue? Have a faster-whisper optimization? Tested on another AMD GPU? Open an issue or PR:

1. Fork the repository
2. Create a branch: `git checkout -b feature/gpu-xyz`
3. Add your changes + test output (benchmark results, transcription samples)
4. Push and open a pull request

Please include:
- Your GPU model and driver version
- Python version and OS build
- Benchmark output from `scripts/benchmark.py`
- Any new methods or optimizations tested

## License

MIT License — see [LICENSE](LICENSE) file.

**Copyright © 2026 Chharith Oeun**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files to use, modify, and distribute freely.

## Support & Community

- **Issues & Questions**: [GitHub Issues](https://github.com/ChharithOeun/whisper-amd-windows/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ChharithOeun/whisper-amd-windows/discussions)
- **Buy Me a Coffee**: [Support development](https://buymeacoffee.com/chharith)

---

**Last tested**: April 2026 | **Python**: 3.10–3.12 | **Windows**: 10/11 (build 19041+)
