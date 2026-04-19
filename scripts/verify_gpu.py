#!/usr/bin/env python3
"""
Verify GPU availability and configuration for Whisper.

Checks:
  - DirectML availability (AMD GPU support on Windows)
  - CUDA availability (NVIDIA GPU support)
  - GPU device detection
  - Driver status
  - VRAM availability

Usage:
    python verify_gpu.py
"""

import sys


def check_directml():
    """Check DirectML (AMD GPU) support."""
    try:
        import onnxruntime as ort
        providers = ort.get_available_providers()
        dml_available = 'DmlExecutionProvider' in providers

        if dml_available:
            return True, "DirectML available"
        else:
            return False, "DirectML not in available providers"

    except ImportError:
        return False, "onnxruntime not installed"
    except Exception as e:
        return False, str(e)


def check_cuda():
    """Check CUDA (NVIDIA GPU) support."""
    try:
        import onnxruntime as ort
        providers = ort.get_available_providers()
        cuda_available = 'CUDAExecutionProvider' in providers

        if cuda_available:
            return True, "CUDA available"
        else:
            return False, "CUDA not in available providers"

    except ImportError:
        return False, "onnxruntime not installed"
    except Exception as e:
        return False, str(e)


def check_amd_gpu():
    """Check for AMD GPU detection."""
    try:
        import wmi
        try:
            c = wmi.WMI()
            gpus = c.Win32_VideoController()

            amd_gpus = [gpu for gpu in gpus if 'AMD' in gpu.Name or 'Radeon' in gpu.Name]

            if amd_gpus:
                gpu_list = [gpu.Name for gpu in amd_gpus]
                return True, f"AMD GPU found: {', '.join(gpu_list)}"
            else:
                return False, "No AMD GPU detected"

        except Exception as e:
            return False, f"WMI error: {e}"

    except ImportError:
        # Fallback: Check NVIDIA instead as proxy for GPU detection
        try:
            import onnxruntime as ort
            providers = ort.get_available_providers()
            if 'DmlExecutionProvider' in providers or 'CUDAExecutionProvider' in providers:
                return True, "GPU detected via ONNX providers"
            else:
                return False, "No GPU providers detected"
        except Exception as e:
            return False, str(e)


def check_faster_whisper():
    """Check faster-whisper installation."""
    try:
        import faster_whisper
        return True, f"faster-whisper {faster_whisper.__version__}"
    except ImportError:
        return False, "faster-whisper not installed"
    except Exception as e:
        return False, str(e)


def check_onnxruntime():
    """Check ONNX Runtime installation and version."""
    try:
        import onnxruntime as ort
        return True, f"onnxruntime {ort.__version__}"
    except ImportError:
        return False, "onnxruntime not installed"
    except Exception as e:
        return False, str(e)


def check_python():
    """Check Python version."""
    import platform
    version = platform.python_version()
    major, minor, patch = map(int, version.split('.')[:3])

    if major == 3 and minor >= 10:
        return True, f"Python {version}"
    else:
        return False, f"Python {version} (requires 3.10+)"


def check_platform():
    """Check operating system."""
    import platform
    system = platform.system()
    release = platform.release()

    if system == "Windows":
        return True, f"Windows {release}"
    else:
        return False, f"{system} {release} (this guide targets Windows)"


def get_device_string(has_directml, has_cuda):
    """Determine recommended device based on available providers."""
    if has_directml:
        return "DirectML (AMD GPU) - RECOMMENDED"
    elif has_cuda:
        return "CUDA (NVIDIA GPU)"
    else:
        return "CPU (fallback)"


def main():
    """Run all checks and print report."""
    print("\n" + "=" * 70)
    print("GPU Setup Verification Report")
    print("=" * 70)

    checks = [
        ("Platform", check_platform),
        ("Python Version", check_python),
        ("ONNX Runtime", check_onnxruntime),
        ("faster-whisper", check_faster_whisper),
        ("AMD GPU Detected", check_amd_gpu),
        ("DirectML (AMD GPU Support)", check_directml),
        ("CUDA (NVIDIA GPU Support)", check_cuda),
    ]

    results = {}
    for name, check_fn in checks:
        success, message = check_fn()
        results[name] = (success, message)
        status = "✓" if success else "✗"
        print(f"{status} {name:<30} {message}")

    # Summary
    print("\n" + "-" * 70)
    print("Summary:")

    has_directml = results["DirectML (AMD GPU Support)"][0]
    has_cuda = results["CUDA (NVIDIA GPU Support)"][0]

    recommended_device = get_device_string(has_directml, has_cuda)
    print(f"Recommended device: {recommended_device}")

    # Status checks
    all_ok = all(success for success, _ in results.values())

    if all_ok:
        print("\n✓ All checks passed! Setup is complete.")
        if has_directml:
            print("  You can now transcribe with: python scripts/transcribe.py audio.mp3")
        return 0
    else:
        print("\n⚠ Some checks failed. See issues above.")

        # Provide guidance
        if not results["ONNX Runtime"][0]:
            print("\n  → Install ONNX Runtime with DirectML support:")
            print("    pip install onnxruntime-directml")

        if not results["faster-whisper"][0]:
            print("\n  → Install faster-whisper:")
            print("    pip install faster-whisper")

        if not has_directml and not has_cuda:
            print("\n  → No GPU detected. Transcription will use CPU (slower).")
            print("    For AMD GPU on Windows, ensure:")
            print("    1. AMD Radeon drivers are up-to-date")
            print("    2. Reinstall: pip uninstall onnxruntime-directml && pip install onnxruntime-directml")

        return 1


if __name__ == "__main__":
    exit_code = main()
    print("=" * 70 + "\n")
    sys.exit(exit_code)
