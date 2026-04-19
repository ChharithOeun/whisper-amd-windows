---
name: Bug Report
about: Report a problem with Whisper on AMD Windows
title: "[BUG] "
labels: bug
assignees: ''

---

## Describe the Bug
A clear description of what the bug is.

## To Reproduce

```bash
# Steps to reproduce
python scripts/transcribe.py audio.mp3
```

## Expected Behavior
What should happen instead?

## Error Output
```
Paste full error message/traceback here
```

## System Information
- **GPU**: RX 5700 XT / RX 6600 XT / Other
- **Driver Version**: (from AMD Radeon Settings)
- **Python Version**: 3.10 / 3.11 / 3.12
- **Windows Build**: (from Settings → System → About)
- **Whisper Model**: tiny / base / small / medium / large

## Verification Steps Taken
- [ ] Ran `python scripts/verify_gpu.py` (paste output)
- [ ] Tested with `--device cpu` to isolate GPU issue
- [ ] Updated AMD drivers to latest version
- [ ] Checked Troubleshooting section in README

## Additional Context
Add any other context about the problem here.

## Benchmark Results
Paste output from:
```bash
python scripts/benchmark.py
```
