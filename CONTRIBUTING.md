# Contributing

Thank you for your interest in improving `whisper-amd-windows`! This guide outlines how to contribute effectively.

## Before You Start

- **Search existing issues** before opening a new one
- **Check the README** and troubleshooting section — your issue may be covered
- **Be specific**: Include GPU model, driver version, Python version, and error messages

## Reporting Issues

### GPU Not Detected

Include:
```bash
python scripts/verify_gpu.py  # Run and paste output
python -c "import onnxruntime; print(onnxruntime.get_available_providers())"
```

### Transcription Fails

Include:
- Error message (full traceback)
- Audio file format (MP3, WAV, etc.)
- Whisper model used (tiny, base, small, medium, large)
- Your GPU model and VRAM

```bash
python scripts/transcribe.py audio.mp3 2>&1 | tee error.log
```

## Testing Before PR

### 1. Verify GPU Detection

```bash
python scripts/verify_gpu.py
```

Should show:
- ✓ DirectML available
- ✓ AMD GPU detected (or similar)
- ✓ faster-whisper installed

### 2. Test on Sample Audio

```bash
python scripts/transcribe.py test_audio.mp3 --model base
```

Check that `.txt` and `.srt` files are generated correctly.

### 3. Benchmark Your Hardware

```bash
python scripts/benchmark.py
```

Include the results in your PR — they prove your changes work.

### 4. Check Python Code Quality

```bash
pip install flake8
flake8 scripts/
```

Fix any style issues before submitting.

## Submitting Changes

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/whisper-amd-windows.git
cd whisper-amd-windows
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Keep commits focused (one feature per commit)
- Write clear commit messages:
  ```
  Add DirectML fallback for older AMD drivers
  
  - Detect DirectML via legacy DXGI path
  - Fallback to CPU if DML provider unavailable
  - Tested on Windows 10 with RX 5700 XT
  ```

### 3. Test Thoroughly

Run the full test suite:
```bash
python -m pytest tests/  # If tests exist
python scripts/verify_gpu.py
python scripts/transcribe.py sample.mp3
python scripts/benchmark.py --models tiny,base,small
```

### 4. Document Your Changes

- Update `README.md` if adding new features
- Add troubleshooting entries if fixing common issues
- Include benchmark results in the PR description

### 5. Submit PR

Include:
- **Description**: What does this fix/add?
- **GPU tested on**: RX 5700 XT, RX 6600 XT, etc.
- **Python version**: 3.10, 3.11, 3.12
- **Windows version**: 10 / 11
- **Benchmark output**: From `python scripts/benchmark.py`
- **Before/after**: If fixing performance, show the improvement

### Example PR Description

```
**GPU Path Optimization for RDNA2 Cards**

- Detects gfx1030+ and enables RDNA2-specific optimizations
- Improves batch processing speed by ~25% on RX 6700 XT
- Tested on Windows 11, Python 3.12
- Backward compatible with RDNA1, Polaris, Vega

Benchmark (RX 6700 XT, medium model):
- Before: 5.2x realtime
- After: 6.5x realtime
```

## Types of Contributions

### GPU Model Testing

Tested on RX 5700 XT? Open an issue:
- **Title**: `Tested on [GPU Model]`
- **Content**: Benchmark results from `scripts/benchmark.py`
- **Include**: Driver version, Python version, Windows build

### Performance Optimization

Have a faster implementation? Submit a PR with:
- Before/after benchmark results
- Explanation of optimization
- Testing on multiple GPU models

### Bug Fixes

Fix a crash or error? Include:
- Root cause analysis
- Steps to reproduce
- Your GPU and driver version
- The error trace

### Documentation

Improve guides or examples? Check for:
- Accuracy (test the steps you document)
- Clarity (read as a newcomer would)
- Completeness (cover edge cases)

## Code Style

- Use **4 spaces** for indentation
- Keep lines **≤120 characters**
- Add docstrings to functions:
  ```python
  def transcribe_audio(audio_path, model_name="base"):
      """
      Transcribe audio using Whisper.

      Args:
          audio_path (str): Path to audio file
          model_name (str): Whisper model size
      
      Returns:
          dict: Transcription result
      """
  ```
- Type hints encouraged for clarity

## Questions?

- **GPU issue**: Open a GitHub issue
- **Setup problem**: Check README → Troubleshooting
- **Feature idea**: Open a discussion

## Recognition

Contributors are recognized in:
- **README** — Added to "Contributors" section (with your permission)
- **CHANGELOG** — Linked to your GitHub profile
- **Releases** — Tagged in release notes

Thank you for helping make Whisper faster on AMD!
