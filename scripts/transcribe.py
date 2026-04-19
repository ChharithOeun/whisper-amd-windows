#!/usr/bin/env python3
"""
Transcribe audio files using Whisper on AMD GPU (DirectML) or CPU fallback.

Automatically detects DirectML GPU availability and falls back to CPU if needed.
Supports MP3, WAV, M4A, FLAC, OGG, WMA audio formats.

Usage:
    python transcribe.py path/to/audio.mp3
    python transcribe.py path/to/audio.wav --model large
    python transcribe.py path/to/audio.mp3 --device cpu --language en

Output:
    - {basename}.txt  : Plain text transcript
    - {basename}.srt  : SRT subtitle file with timestamps
"""

import argparse
import os
import sys
import time
from pathlib import Path

try:
    from faster_whisper import WhisperModel
except ImportError:
    print("ERROR: faster-whisper not installed.")
    print("Install with: pip install faster-whisper onnxruntime-directml")
    sys.exit(1)


def detect_device():
    """
    Detect available device: DirectML (AMD GPU), CUDA, or CPU.

    Returns:
        str: Device name ('directml', 'cuda', or 'cpu')
    """
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


def format_srt_timestamp(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def transcribe_audio(
    audio_path,
    model_name="base",
    device="auto",
    language=None,
    compute_type="float16",
):
    """
    Transcribe audio file using Whisper.

    Args:
        audio_path (str): Path to audio file
        model_name (str): Whisper model size (tiny, base, small, medium, large)
        device (str): Device ('auto', 'directml', 'cuda', 'cpu')
        language (str): ISO-639-1 language code (e.g., 'en', 'es'), or None for auto-detect
        compute_type (str): Computation type ('float16' for GPU, 'int8' for reduced memory)

    Returns:
        dict: Transcription result with segments
    """
    audio_path = Path(audio_path)

    if not audio_path.exists():
        print(f"ERROR: Audio file not found: {audio_path}")
        sys.exit(1)

    # Detect device
    if device == "auto":
        device = detect_device()

    print(f"Loading Whisper model '{model_name}'...")
    print(f"Device: {device}")

    # Initialize model
    model = WhisperModel(model_name, device=device, compute_type=compute_type)

    print(f"Transcribing: {audio_path.name}")
    start_time = time.time()

    # Transcribe
    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=5 if device != 'cpu' else 1,
    )

    # Convert to list to allow multiple iterations
    segments = list(segments)
    elapsed = time.time() - start_time

    # Audio duration from info
    audio_duration = info.duration

    # Calculate speed (realtime factor)
    if audio_duration > 0:
        speed = audio_duration / elapsed
        print(f"\nTranscription complete!")
        print(f"Audio duration: {audio_duration:.1f}s")
        print(f"Processing time: {elapsed:.1f}s")
        print(f"Speed: {speed:.1f}x realtime")
    else:
        print(f"\nTranscription complete in {elapsed:.1f}s")

    print(f"Detected language: {info.language}")

    return segments, audio_duration


def save_transcript(segments, audio_path, output_format="both"):
    """
    Save transcription to files.

    Args:
        segments: Whisper segments
        audio_path (Path): Original audio file path
        output_format (str): 'txt', 'srt', or 'both'
    """
    audio_path = Path(audio_path)
    basename = audio_path.stem

    txt_path = audio_path.parent / f"{basename}.txt"
    srt_path = audio_path.parent / f"{basename}.srt"

    if output_format in ("txt", "both"):
        with open(txt_path, "w", encoding="utf-8") as f:
            for segment in segments:
                f.write(segment.text + " ")
            f.write("\n")
        print(f"Saved: {txt_path}")

    if output_format in ("srt", "both"):
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments, 1):
                start = format_srt_timestamp(segment.start)
                end = format_srt_timestamp(segment.end)
                text = segment.text.strip()

                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")
        print(f"Saved: {srt_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio using Whisper on AMD GPU or CPU.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python transcribe.py podcast.mp3
  python transcribe.py speech.wav --model medium --language en
  python transcribe.py meeting.m4a --device cpu --compute-type int8
        """,
    )

    parser.add_argument("audio_path", help="Path to audio file (MP3, WAV, M4A, FLAC, OGG, WMA)")
    parser.add_argument(
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base)",
    )
    parser.add_argument(
        "--device",
        default="auto",
        choices=["auto", "directml", "cuda", "cpu"],
        help="Device to use (default: auto-detect)",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Language code (e.g., en, es, fr). Auto-detect if not specified.",
    )
    parser.add_argument(
        "--compute-type",
        default="float16",
        choices=["float16", "float32", "int8"],
        help="Compute type (default: float16 for GPU, use int8 for lower memory)",
    )
    parser.add_argument(
        "--format",
        default="both",
        choices=["txt", "srt", "both"],
        help="Output format (default: both)",
    )

    args = parser.parse_args()

    try:
        segments, duration = transcribe_audio(
            args.audio_path,
            model_name=args.model,
            device=args.device,
            language=args.language,
            compute_type=args.compute_type,
        )

        save_transcript(segments, args.audio_path, output_format=args.format)

        print("\n✓ Transcription successful!")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
