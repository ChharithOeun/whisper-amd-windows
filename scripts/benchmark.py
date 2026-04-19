#!/usr/bin/env python3
"""
Benchmark Whisper model inference speed on current GPU/CPU.

Tests each model size and reports:
  - Model size (MB)
  - Device (DirectML, CUDA, CPU)
  - Speed (x realtime)
  - VRAM/RAM used (GB)
  - Time for 60s audio

Usage:
    python benchmark.py
    python benchmark.py --device cpu
    python benchmark.py --duration 120
"""

import argparse
import io
import os
import sys
import time
import tracemalloc
from pathlib import Path

import numpy as np

try:
    from faster_whisper import WhisperModel
except ImportError:
    print("ERROR: faster-whisper not installed.")
    print("Install with: pip install faster-whisper")
    sys.exit(1)


def detect_device():
    """Detect available device: DirectML (AMD), CUDA (NVIDIA), or CPU."""
    try:
        import onnxruntime as ort
        providers = ort.get_available_providers()

        if 'DmlExecutionProvider' in providers:
            return 'directml'
        elif 'CUDAExecutionProvider' in providers:
            return 'cuda'
    except ImportError:
        pass
    except Exception as e:
        print(f"WARNING: Could not detect GPU: {e}")

    return 'cpu'


def get_model_size_mb(model_name):
    """Get approximate model size in MB."""
    sizes = {
        "tiny": 39,
        "base": 140,
        "small": 466,
        "medium": 1500,
        "large": 2900,
    }
    return sizes.get(model_name, 0)


def create_test_audio(duration_seconds, sample_rate=16000):
    """
    Create a synthetic test audio signal.

    Args:
        duration_seconds (int): Duration of test audio
        sample_rate (int): Sample rate in Hz

    Returns:
        bytes: Audio data as WAV bytes
    """
    # Generate 1 kHz sine wave
    frames = int(duration_seconds * sample_rate)
    t = np.arange(frames) / sample_rate
    signal = np.sin(2 * np.pi * 1000 * t) * 0.3  # 1 kHz at 30% amplitude

    # Create simple WAV header (44.1 kHz, mono, 16-bit)
    # This is a minimal WAV that faster-whisper can read
    import wave
    import io as io_module

    audio_buffer = io_module.BytesIO()
    with wave.open(audio_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        audio_data = (signal * 32767).astype(np.int16).tobytes()
        wav_file.writeframes(audio_data)

    return audio_buffer.getvalue()


def benchmark_model(model_name, device, duration_seconds=60):
    """
    Benchmark a Whisper model.

    Args:
        model_name (str): Model size (tiny, base, small, medium, large)
        device (str): Device (directml, cuda, cpu)
        duration_seconds (int): Duration of test audio to transcribe

    Returns:
        dict: Benchmark results
    """
    print(f"\n  Testing {model_name}...", end=" ", flush=True)

    try:
        # Start memory tracking
        tracemalloc.start()
        mem_before = tracemalloc.get_traced_memory()[0] / 1024 / 1024  # MB

        # Load model
        load_start = time.time()
        model = WhisperModel(model_name, device=device, compute_type="float16" if device != "cpu" else "float32")
        load_time = time.time() - load_start

        # Create test audio
        test_audio = create_test_audio(duration_seconds)

        # Transcribe
        infer_start = time.time()
        segments, info = model.transcribe(io.BytesIO(test_audio))
        _ = list(segments)  # Consume generator
        infer_time = time.time() - infer_start

        # Memory after
        mem_after = tracemalloc.get_traced_memory()[0] / 1024 / 1024  # MB
        tracemalloc.stop()

        mem_used = max(0, mem_after - mem_before)
        speed = duration_seconds / infer_time if infer_time > 0 else 0

        print(f"✓")

        return {
            "model": model_name,
            "device": device,
            "model_size_mb": get_model_size_mb(model_name),
            "load_time_s": load_time,
            "inference_time_s": infer_time,
            "speed_x_realtime": speed,
            "memory_used_mb": mem_used,
            "duration_s": duration_seconds,
        }

    except Exception as e:
        print(f"✗ ({e})")
        return None


def print_results(results, device):
    """Print benchmark results in table format."""
    print("\n" + "=" * 90)
    print(f"Whisper Benchmark Results — Device: {device.upper()}")
    print("=" * 90)
    print(f"{'Model':<12} {'Size (MB)':<12} {'Load (s)':<12} {'Inference (s)':<15} {'Speed':<15} {'Memory (MB)':<12}")
    print("-" * 90)

    for result in results:
        if result is None:
            continue
        print(
            f"{result['model']:<12} "
            f"{result['model_size_mb']:<12} "
            f"{result['load_time_s']:<12.2f} "
            f"{result['inference_time_s']:<15.2f} "
            f"{result['speed_x_realtime']:<15.1f}x "
            f"{result['memory_used_mb']:<12.1f}"
        )

    print("=" * 90)

    # Summary
    valid_results = [r for r in results if r is not None]
    if valid_results:
        avg_speed = np.mean([r['speed_x_realtime'] for r in valid_results])
        best = max(valid_results, key=lambda x: x['speed_x_realtime'])
        slowest = min(valid_results, key=lambda x: x['speed_x_realtime'])

        print(f"\nSummary:")
        print(f"  Average speed: {avg_speed:.1f}x realtime")
        print(f"  Fastest model: {best['model']} at {best['speed_x_realtime']:.1f}x realtime")
        print(f"  Most capable: {slowest['model']} at {slowest['speed_x_realtime']:.1f}x realtime")
        print()

        print("Recommendations:")
        if avg_speed > 10:
            print("  ✓ Excellent GPU acceleration detected — use larger models (medium/large)")
        elif avg_speed > 5:
            print("  ✓ Good GPU acceleration — medium model recommended")
        elif avg_speed > 1:
            print("  ⚠ Moderate speedup — small model recommended for real-time use")
        else:
            print("  ⚠ Limited acceleration — consider CPU with smaller models")


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark Whisper models on available hardware.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python benchmark.py
  python benchmark.py --device cpu
  python benchmark.py --duration 120
        """,
    )

    parser.add_argument(
        "--device",
        default="auto",
        choices=["auto", "directml", "cuda", "cpu"],
        help="Device to benchmark (default: auto-detect)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Duration of test audio in seconds (default: 60)",
    )
    parser.add_argument(
        "--models",
        default="tiny,base,small,medium",
        help="Comma-separated models to test (default: tiny,base,small,medium)",
    )

    args = parser.parse_args()

    device = args.device if args.device != "auto" else detect_device()
    models = [m.strip() for m in args.models.split(",")]

    print(f"\nWhisper Benchmark")
    print(f"Device: {device.upper()}")
    print(f"Test audio duration: {args.duration}s")
    print(f"Models: {', '.join(models)}")
    print(f"\nRunning benchmarks...")

    results = []
    for model in models:
        result = benchmark_model(model, device, args.duration)
        results.append(result)

    print_results(results, device)

    # Return non-zero if no results
    if not any(r is not None for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
