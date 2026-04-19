# Project Structure

Complete directory and file organization for `whisper-amd-windows`.

```
whisper-amd-windows/
├── .github/                          # GitHub-specific files
│   ├── workflows/
│   │   ├── ci.yml                   # CI/CD — tests on Windows/macOS/Linux × Python 3.10-3.12
│   │   └── changelog.yml            # Auto-changelog on commits to main
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md            # Bug report template
│       └── feature_request.md       # Feature request template
│
├── scripts/                          # Utility scripts
│   ├── transcribe.py                # Main transcription script (DirectML + CPU)
│   ├── benchmark.py                 # Performance benchmarking tool
│   ├── verify_gpu.py                # GPU setup verification
│   └── README.md                    # Scripts documentation
│
├── .gitignore                       # Git ignore patterns
├── CHANGELOG.md                     # Version history and updates
├── CONTRIBUTING.md                  # Contributing guidelines
├── INSTALL.md                       # Step-by-step installation guide
├── LICENSE                          # MIT License
├── README.md                        # Main documentation
├── PROJECT_STRUCTURE.md             # This file
├── config.example.json              # Configuration template (advanced users)
├── requirements.txt                 # Python dependencies
├── run.bat                          # Windows quick-start batch file
├── setup.py                         # Python package setup
└── .gitattributes                   # (future) Git attributes
```

## File Descriptions

### Documentation (Root)

| File | Purpose | Audience |
|---|---|---|
| `README.md` | **Main documentation** — features, quick start, compatibility table, troubleshooting | Everyone |
| `INSTALL.md` | **Step-by-step installation** — from Python setup to first transcription | New users |
| `CONTRIBUTING.md` | **Contribution guidelines** — how to submit PRs, test requirements, code style | Contributors |
| `CHANGELOG.md` | **Version history** — changes per release, upgrade guides | Users tracking updates |
| `LICENSE` | **MIT License** — legal terms | Legal review |
| `PROJECT_STRUCTURE.md` | **This file** — project organization | Developers exploring code |

### Configuration & Setup

| File | Purpose |
|---|---|
| `requirements.txt` | Python package dependencies (faster-whisper, onnxruntime-directml) |
| `setup.py` | Python package metadata, classifiers, entry points |
| `config.example.json` | Example configuration for advanced users (not required) |
| `run.bat` | Windows batch file for convenient commands (`run.bat transcribe audio.mp3`) |
| `.gitignore` | Files to exclude from git (model cache, output files, venv) |

### GitHub Workflows

| File | Purpose | Trigger |
|---|---|---|
| `.github/workflows/ci.yml` | **Continuous Integration** — lint Python, test syntax on Windows/macOS/Linux | Push to any branch |
| `.github/workflows/changelog.yml` | **Auto-changelog** — generate release notes on commits to main | Push to main |

### Scripts (utilities/)

All production-ready Python scripts:

| File | Purpose | Output |
|---|---|---|
| `scripts/transcribe.py` | **Transcribe audio** — main user script. Auto-detects DirectML, falls back to CPU. | `.txt` + `.srt` files |
| `scripts/benchmark.py` | **Benchmark GPU** — tests model speeds, memory usage, realtime factors | Console table |
| `scripts/verify_gpu.py` | **Verify setup** — checks DirectML, GPU detection, dependencies | Pass/fail report |
| `scripts/README.md` | **Scripts documentation** — usage, arguments, examples, output | (Internal docs) |

### GitHub Issue Templates

| File | Purpose |
|---|---|
| `.github/ISSUE_TEMPLATE/bug_report.md` | Template for bug reports (auto-filled on issue creation) |
| `.github/ISSUE_TEMPLATE/feature_request.md` | Template for feature requests |

---

## Key Design Decisions

### Single-File Scripts (No Subdirectories)

- **Rationale**: Easier for users to discover and run
- **Alternative considered**: Modular package structure (rejected for simplicity)

### No Tests Directory

- **Rationale**: GitHub Actions CI validates syntax and imports
- **User testing**: Benchmark script serves as integration test
- **Future**: Unit tests can be added in `tests/` when needed

### Dual Activation Methods

- **Git clone**: Full version control, contributions, updates
- **ZIP download**: No git dependency for casual users
- **Python package**: `pip install` support via `setup.py`

### Batch File for Windows Convenience

- `run.bat` — Quick commands without typing full Python paths
- Not required, but helps Windows users
- Automatically creates/activates venv

### Comprehensive Documentation

- **README.md** — Main entry point, 80% of questions answered
- **INSTALL.md** — Step-by-step, visual guidance
- **scripts/README.md** — Usage for each script
- **CONTRIBUTING.md** — Clear path for contributors

---

## Development Workflow

### Adding a New Feature

1. **Fork & branch**: `git checkout -b feature/my-feature`
2. **Add code** to `scripts/`
3. **Update README** if user-facing
4. **Test**:
   ```bash
   python scripts/verify_gpu.py
   python scripts/transcribe.py test.mp3
   python scripts/benchmark.py
   ```
5. **Lint**: `flake8 scripts/`
6. **Commit** with clear message
7. **Open PR** with benchmark results

### Updating Dependencies

1. **Edit `requirements.txt`**
2. **Test locally**:
   ```bash
   pip install -r requirements.txt
   python scripts/verify_gpu.py
   ```
3. **Update CI** (`.github/workflows/ci.yml`) if needed
4. **Note in CHANGELOG.md**

### Releasing a New Version

1. **Update version** in `setup.py`
2. **Update CHANGELOG.md** with new version
3. **Create git tag**: `git tag v1.1.0`
4. **Push**: `git push origin main --tags`
5. **GitHub releases page** auto-creates release from tag

---

## File Size Reference

Typical repository size after cloning:

| Component | Size |
|---|---|
| `.git/` (history) | ~500KB |
| `README.md` + docs | ~200KB |
| `scripts/` (Python) | ~50KB |
| `.github/` workflows | ~20KB |
| **Total** | ~800KB |

Whisper models are downloaded on-demand:
- `tiny` — 39MB
- `base` — 140MB
- `small` — 466MB
- `medium` — 1.5GB
- `large` — 2.9GB

---

## Platform Support

| Component | Windows | Linux | macOS |
|---|---|---|---|
| Python scripts | ✓ (main) | ✓ | ✓ |
| DirectML GPU | ✓ AMD only | ✗ | ✗ |
| CPU fallback | ✓ | ✓ | ✓ |
| run.bat | ✓ (native) | ✗ (use bash) | ✗ (use bash) |
| CI testing | ✓ | ✓ | ✓ |

---

## Security Considerations

- **No credentials stored** — Scripts don't require API keys or secrets
- **Open source** — Full transparency, community audit
- **No telemetry** — Local processing, no data collection
- **MIT License** — Permissive, allows commercial use
- **Dependency scanning** — `setup.py` lists all dependencies explicitly

---

## Future Expansion

Potential additions (not in initial release):

```
whisper-amd-windows/
├── tests/                     # Unit tests (pytest)
├── examples/                  # Sample audio files
├── docs/                      # Extended documentation
│   ├── gpu-tuning.md         # Performance optimization
│   ├── rocm-setup.md         # ROCm (Method B) guide
│   └── api-reference.md      # Python API docs
├── web_ui/                    # Web interface (FastAPI)
└── docker/                    # Docker configuration
```

---

## Getting Started

### For Users
1. Read `README.md`
2. Follow `INSTALL.md`
3. Run `python scripts/transcribe.py audio.mp3`

### For Contributors
1. Read `CONTRIBUTING.md`
2. Fork the repo
3. Check `PROJECT_STRUCTURE.md` (this file) for organization
4. Make changes to `scripts/` or docs
5. Submit PR with benchmark results

### For Packagers/DevOps
1. Use `setup.py` for automated installation
2. `requirements.txt` for dependency pinning
3. `.github/workflows/ci.yml` as test reference

---

## Questions?

- **Setup issues**: See `INSTALL.md` → Troubleshooting
- **Usage questions**: See `scripts/README.md` and `README.md` → Troubleshooting
- **Contributing**: See `CONTRIBUTING.md`
- **GitHub Issues**: https://github.com/ChharithOeun/whisper-amd-windows/issues
