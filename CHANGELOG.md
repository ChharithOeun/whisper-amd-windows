# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- ROCm support guide for ComfyUI ecosystem (Method B)
- Batch transcription script
- WebUI for transcription
- Audio preprocessing utilities (noise reduction, normalization)
- Multi-language detection and per-segment language identification
- GPU memory optimization guide for <4GB VRAM cards

## [1.0.0] - 2026-04-19

### Added
- Initial release with full DirectML support (Method A)
- `transcribe.py` — Main transcription script with auto GPU detection
- `benchmark.py` — Performance benchmarking tool
- `verify_gpu.py` — GPU setup verification utility
- Comprehensive README with GPU compatibility table
- CI/CD workflows (GitHub Actions) for multi-platform testing
- MIT License
- Contributing guidelines
- Tested on RX 5700 XT (RDNA1) with benchmarks (~8x realtime on medium model)
- Support for `tiny`, `base`, `small`, `medium`, `large` models
- Output formats: TXT and SRT (subtitles with timestamps)
- CPU fallback for systems without GPU support
- Requirements pinned to compatible versions

### Documentation
- Full setup guide for Method A (faster-whisper + DirectML)
- Troubleshooting section covering common errors
- Model recommendations by VRAM
- GPU compatibility matrix for RDNA/Polaris/Vega
- Real-world performance metrics

### Testing
- Validated on Windows 10/11
- Python 3.10, 3.11, 3.12 compatibility
- DirectML detection and fallback paths
- Audio format support (MP3, WAV, M4A, FLAC, OGG, WMA)

---

## Upgrade Guide

### From Initial Setup to 1.0.0
No breaking changes. Existing installations continue to work:
```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

### Future: 1.x → 2.0
ROCm support (Method B) will be added as optional. Existing DirectML users unaffected.

---

For older releases, see [GitHub Releases](https://github.com/ChharithOeun/whisper-amd-windows/releases).
