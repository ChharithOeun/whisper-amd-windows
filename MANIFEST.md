# Repository Manifest

Complete file listing and description for `whisper-amd-windows` v1.0.0.

**Generated**: April 19, 2026
**Repository**: https://github.com/ChharithOeun/whisper-amd-windows

---

## File Listing (19 files, 112KB)

### Root Documentation (6 files)

```
README.md                    650+ lines  Main documentation, quick start, compatibility table
INSTALL.md                   450+ lines  Step-by-step Windows installation guide
CONTRIBUTING.md              250+ lines  Contribution guidelines and code standards
PROJECT_STRUCTURE.md         300+ lines  Repository organization and design decisions
CHANGELOG.md                 100+ lines  Version history and release notes
LICENSE                       20 lines  MIT License, Copyright 2026 Chharith Oeun
```

### Configuration Files (4 files)

```
requirements.txt              ~20 lines  Python package dependencies
setup.py                      ~60 lines  Python package metadata and console scripts
config.example.json           ~30 lines  Example configuration for advanced users
.gitignore                    ~40 lines  Git ignore patterns (venv, cache, models)
```

### Utilities & Scripts (4 files)

```
run.bat                       ~40 lines  Windows batch script for quick commands
scripts/README.md            ~200 lines  Script usage documentation
scripts/transcribe.py        ~280 lines  Main transcription script (DirectML + CPU)
scripts/benchmark.py         ~320 lines  GPU performance benchmarking tool
scripts/verify_gpu.py        ~220 lines  GPU setup verification utility
```

### GitHub Configuration (5 files)

```
.github/workflows/ci.yml       ~60 lines  CI/CD — multi-platform testing (Win/Mac/Linux)
.github/workflows/changelog.yml ~50 lines  Auto-changelog generation on commits
.github/ISSUE_TEMPLATE/bug_report.md      Bug report template with checklist
.github/ISSUE_TEMPLATE/feature_request.md Feature request template
.gitattributes                (future)   Git attributes for line endings
```

### Index & Documentation (1 file)

```
MANIFEST.md                 (this file)  Complete file listing
```

---

## Installation Footprint

| Component | Size | Time |
|---|---|---|
| Repository clone | 112KB | <1 minute |
| Python venv creation | ~300MB | 1-2 minutes |
| Dependencies install | ~150MB | 2-5 minutes |
| First model download | 140MB (base) | 1-3 minutes |
| **Total initial setup** | ~650MB | 5-10 minutes |

Model downloads (optional, on-demand):
- `tiny` — 39MB
- `base` — 140MB
- `small` — 466MB
- `medium` — 1.5GB
- `large` — 2.9GB

---

## File Purposes

### README.md (650+ lines)
**What it covers:**
- Project overview and AMD GPU benefits
- GPU compatibility matrix (RDNA1/2/3/4, Vega, Polaris)
- Three installation methods (A: DirectML, B: ROCm, C: CPU)
- Step-by-step Method A setup
- Real benchmark data from RX 5700 XT
- Proof of concept with speed metrics (8x realtime)
- Troubleshooting section (6+ common issues)
- Model recommendations by VRAM
- Related repositories link
- Contributing and support

**Who reads it:**
- First-time users (quick overview)
- Existing users (troubleshooting)
- Contributors (project scope)

### INSTALL.md (450+ lines)
**What it covers:**
- Driver update with version checking
- Python 3.11 installation
- Repository cloning (with git-free alternative)
- Virtual environment setup
- Dependency installation with breakdown
- GPU detection verification with expected output
- Test transcription with sample output
- Benchmarking guide
- Detailed troubleshooting for each step

**Who reads it:**
- New Windows users
- First-time Python users
- Troubleshooting

### CONTRIBUTING.md (250+ lines)
**What it covers:**
- Issue reporting templates
- Testing requirements before PR
- Python code style guidelines
- Commit message format
- PR submission process
- Types of contributions (bug fix, feature, optimization, documentation)
- Recognition and credit

**Who reads it:**
- Contributors
- Bug reporters
- Feature requesters

### PROJECT_STRUCTURE.md (300+ lines)
**What it covers:**
- Directory tree visualization
- File-by-file descriptions
- Design decisions and rationales
- Development workflow
- Platform support matrix
- Security considerations
- Future expansion plans

**Who reads it:**
- Developers exploring code
- Contributors planning changes
- Maintainers

### scripts/README.md (200+ lines)
**What it covers:**
- transcribe.py usage with examples
- benchmark.py output interpretation
- verify_gpu.py output reference
- Quick reference for common tasks
- Batch processing examples
- Memory optimization tips

**Who reads it:**
- Script users
- Advanced users

### CHANGELOG.md (100+ lines)
**What it covers:**
- Version 1.0.0 release notes
- Features added
- Testing performed
- Tested GPU models
- Planned features for future releases
- Upgrade guide

**Who reads it:**
- Users checking what's new
- Contributors understanding changes

### LICENSE (20 lines)
MIT License — legal terms for open-source use

**Who reads it:**
- Legal review
- Commercial use verification

### requirements.txt (~20 lines)
Python packages needed:
- `faster-whisper>=0.9.0` — Optimized Whisper
- `onnxruntime-directml>=1.17.0` — AMD GPU support
- `onnx>=1.14.0` — Optional, for optimization
- `numpy>=1.21.0` — Numeric operations

### setup.py (~60 lines)
Python package configuration:
- Package metadata (name, version, author)
- Dependencies from requirements.txt
- Console script entry points
- Python version requirement (3.10+)
- Classifiers for PyPI

### scripts/transcribe.py (~280 lines)
**Core features:**
- Auto-device detection (DirectML → CUDA → CPU)
- 5 model sizes (tiny to large)
- 5+ audio formats (MP3, WAV, M4A, FLAC, OGG, WMA)
- Compute type selection (float16, float32, int8)
- Output formats (TXT, SRT)
- Progress reporting with speed metrics
- Full error handling

**Entry point for users**

### scripts/benchmark.py (~320 lines)
**Core features:**
- Synthetic audio generation for reproducible testing
- Tests all 5 model sizes
- Reports: load time, inference time, speed (x realtime), VRAM usage
- Device detection with fallback
- Performance recommendations
- Human-readable output table

**For hardware validation and selection**

### scripts/verify_gpu.py (~220 lines)
**Core features:**
- Checks Python version (3.10+)
- Verifies ONNX Runtime
- Detects DirectML provider
- Checks AMD GPU hardware
- Tests faster-whisper
- Provides troubleshooting guidance
- Cross-platform compatibility checks

**For setup verification and troubleshooting**

### run.bat (~40 lines)
Windows batch script for convenience:
- `run.bat install` — Install dependencies
- `run.bat verify` — Run GPU verification
- `run.bat transcribe FILE` — Transcribe audio
- `run.bat benchmark` — Benchmark hardware

### .github/workflows/ci.yml (~60 lines)
GitHub Actions CI/CD:
- Runs on Ubuntu, Windows, macOS
- Tests Python 3.10, 3.11, 3.12 (9 combinations)
- Linting with flake8
- Syntax validation
- Security checks with bandit
- Triggered on push and PR

### .github/workflows/changelog.yml (~50 lines)
Auto-changelog workflow:
- Triggered on push to main
- Reads latest commit
- Generates CHANGELOG entry
- Commits changelog update

### .github/ISSUE_TEMPLATE/bug_report.md
Structured bug report template:
- Description field
- Steps to reproduce
- Expected vs actual behavior
- System info (GPU, driver, Python, Windows)
- Verification checklist
- Benchmark output section

### .github/ISSUE_TEMPLATE/feature_request.md
Structured feature request template:
- Problem description
- Proposed solution
- Alternative approaches
- Testing confirmation

### .gitignore (~40 lines)
Excludes from version control:
- Python cache (`__pycache__`, `.pyc`)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- Model cache (`.model`, whisper-*/  directories)
- Output files (`*.txt`, `*.srt`, `*.wav`, `*.mp3`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Local config (`.env`, `secrets.json`)

### config.example.json (~30 lines)
Configuration template for advanced users:
- Model selection
- Device preferences
- Output options
- Performance tuning
- Audio settings
- Logging configuration

---

## How Files Work Together

```
User reads README.md
    ↓
Follows INSTALL.md for setup
    ↓
Runs scripts/verify_gpu.py to check installation
    ↓
Runs scripts/transcribe.py to transcribe audio
    ↓
Optional: Runs scripts/benchmark.py for performance
    ↓
Has issue → Submits bug report using .github/ISSUE_TEMPLATE/bug_report.md
    ↓
Wants to contribute → Reads CONTRIBUTING.md
```

---

## File Interdependencies

```
README.md
├── References INSTALL.md for setup details
├── References scripts/README.md for script options
├── References CONTRIBUTING.md for contributing
└── References CHANGELOG.md for version info

INSTALL.md
├── Uses requirements.txt for dependencies
├── References scripts/verify_gpu.py for verification
└── References scripts/transcribe.py for first use

scripts/transcribe.py
├── Uses requirements.txt dependencies
├── Uses setup.py for packaging
└── Output documented in scripts/README.md

CI/CD (.github/workflows/)
├── Tests scripts/transcribe.py
├── Tests scripts/benchmark.py
├── Tests scripts/verify_gpu.py
└── Validates setup.py configuration
```

---

## Editing Guidelines

### Adding a Feature

1. Update `scripts/*.py` (implementation)
2. Update `scripts/README.md` (usage)
3. Update `README.md` (quick start or troubleshooting)
4. Test with `ci.yml` requirements
5. Update `CHANGELOG.md`
6. Update `CONTRIBUTING.md` if testing changes

### Updating Installation

1. Update `INSTALL.md` (step-by-step)
2. Update `requirements.txt` if dependencies change
3. Update `setup.py` version and classifiers
4. Test on actual Windows system
5. Update `README.md` quick start if needed

### Adding a New GPU Support

1. Add to compatibility table in `README.md`
2. Document in GPU compatibility matrix
3. Add benchmark data if possible
4. Update CHANGELOG.md
5. Document in troubleshooting if needed

---

## File Sizes (Actual)

```
README.md                    ~13KB
INSTALL.md                   ~18KB
CONTRIBUTING.md              ~9KB
PROJECT_STRUCTURE.md         ~12KB
CHANGELOG.md                 ~4KB
scripts/transcribe.py        ~11KB
scripts/benchmark.py         ~13KB
scripts/verify_gpu.py        ~9KB
scripts/README.md            ~8KB
setup.py                     ~2KB
requirements.txt             ~0.5KB
config.example.json          ~1KB
.github/workflows/ci.yml     ~1.5KB
.github/workflows/changelog.yml ~1KB
Other files                  ~4KB
─────────────────────
TOTAL                        ~112KB
```

---

## Maintenance Checklist

### Monthly
- [ ] Check GitHub Issues for common problems
- [ ] Update benchmark data if new hardware tested
- [ ] Verify CI/CD still passing

### Per Release
- [ ] Update version in setup.py
- [ ] Update CHANGELOG.md
- [ ] Test all scripts on Windows
- [ ] Verify CI passes on all platforms
- [ ] Create GitHub release tag

### Annually
- [ ] Review and update dependencies
- [ ] Test on latest Windows versions
- [ ] Review and update GPU compatibility table
- [ ] Update Python version support if needed

---

## Summary

This manifest documents a complete, production-ready repository with:
- 19 files (documentation, code, CI/CD, templates)
- 850+ lines of Python code
- 2000+ lines of documentation
- Complete GitHub integration
- Real benchmark data
- Cross-platform support

All files are ready for immediate GitHub publication.

---

**Last updated**: April 19, 2026
**Status**: Complete v1.0.0
