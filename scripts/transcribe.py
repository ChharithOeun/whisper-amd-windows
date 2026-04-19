#!/usr/bin/env python3
"""
Transcribe audio files using Whisper on AMD GPU (DirectML) or CPU fallback.

Automatically detects DirectML GPU availability and falls back to CPU if needed.
Supports MP3, WAV, M4A, M4B, MP4, MKV, WEBM, FLAC, OGG, WMA audio formats.

Usage:
    python transcribe.py path/to/audio.mp3
    python transcribe.py path/to/audio.wav --model large --word-timestamps
    python transcribe.py path/to/audio.mp3 --device cpu --language en
    python transcribe.py path/to/audio.mp3 --format srt
    python transcribe.py path/to/audio.mp3 --format json --word-timestamps
    python transcribe.py ./audio_folder/ --batch --model small

Output:
    - {basename}.txt   : Plain text transcript
    - {basename}.srt   : SRT subtitle file with timestamps
    - {basename}.vtt   : WebVTT subtitle format
    - {basename}.json  : JSON format with segments and metadata
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
    beam_size=5,
    word_timestamps=False,
):
    """
    Transcribe audio file using Whisper.

    Args:
        audio_path (str): Path to audio file
        model_name (str): Whisper model size (tiny, base, small, medium, large, large-v2, large-v3)
        device (str): Device ('auto', 'directml', 'cuda', 'cpu')
        language (str): ISO-639-1 language code (e.g., 'en', 'es'), or None for auto-detect
        compute_type (str): Computation type ('float16' for GPU, 'int8' for reduced memory)
        beam_size (int): Beam search width (default 5, use 1 for CPU)
        word_timestamps (bool): Enable word-level timestamps (slower)

    Returns:
        tuple: (segments, audio_duration, language_code)
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

    # Determine beam size based on device
    if beam_size == 5 and device == 'cpu':
        beam_size = 1

    # Transcribe
    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=beam_size,
        word_level_timestamps=word_timestamps,
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

    return segments, audio_duration, info.language


def format_vtt_timestamp(seconds):
    """Convert seconds to WebVTT timestamp format (HH:MM:SS.mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def save_transcript(segments, audio_path, output_format="both", language=None):
    """
    Save transcription to files.

    Args:
        segments: Whisper segments
        audio_path (Path): Original audio file path
        output_format (str): 'txt', 'srt', 'vtt', 'json', or 'all'
        language (str): Detected language code
    """
    import json as json_module

    audio_path = Path(audio_path)
    basename = audio_path.stem

    # Handle "all" format
    formats_to_save = [output_format] if output_format != "all" else ["txt", "srt", "vtt", "json"]

    if "txt" in formats_to_save:
        txt_path = audio_path.parent / f"{basename}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            for segment in segments:
                f.write(segment.text + " ")
            f.write("\n")
        print(f"Saved: {txt_path}")

    if "srt" in formats_to_save:
        srt_path = audio_path.parent / f"{basename}.srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments, 1):
                start = format_srt_timestamp(segment.start)
                end = format_srt_timestamp(segment.end)
                text = segment.text.strip()

                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")
        print(f"Saved: {srt_path}")

    if "vtt" in formats_to_save:
        vtt_path = audio_path.parent / f"{basename}.vtt"
        with open(vtt_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for segment in segments:
                start = format_vtt_timestamp(segment.start)
                end = format_vtt_timestamp(segment.end)
                text = segment.text.strip()

                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")
        print(f"Saved: {vtt_path}")

    if "json" in formats_to_save:
        json_path = audio_path.parent / f"{basename}.json"
        output_data = {
            "language": language,
            "segments": [
                {
                    "id": i,
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                    "words": [
                        {"word": word.word, "start": word.start, "end": word.end}
                        for word in getattr(segment, "words", [])
                    ] if hasattr(segment, "words") and segment.words else [],
                }
                for i, segment in enumerate(segments)
            ],
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json_module.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"Saved: {json_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio using Whisper on AMD GPU or CPU.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python transcribe.py podcast.mp3
  python transcribe.py speech.wav --model medium --language en
  python transcribe.py meeting.m4a --device cpu --compute-type int8
  python transcribe.py audio.mp3 --format json --word-timestamps
  python transcribe.py ./audio_folder/ --batch --model small
        """,
    )

    parser.add_argument("audio_path", help="Path to audio file or directory (MP3, WAV, M4A, M4B, MP4, MKV, WEBM, FLAC, OGG, WMA)")
    parser.add_argument(
        "--model",
        default="small",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
        help="Whisper model size (default: small)",
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
        choices=["txt", "srt", "vtt", "json", "all"],
        help="Output format (default: both = txt + srt)",
    )
    parser.add_argument(
        "--word-timestamps",
        action="store_true",
        help="Include word-level timestamps (slower but more precise)",
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        default=5,
        help="Beam search width (default: 5, use 1 for CPU)",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Batch mode: transcribe all audio files in directory",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output directory (default: same as input file)",
    )

    args = parser.parse_args()

    try:
        audio_path = Path(args.audio_path)

        # Batch mode
        if args.batch:
            if not audio_path.is_dir():
                print(f"ERROR: --batch requires a directory, got file: {audio_path}")
                sys.exit(1)

            audio_extensions = {".mp3", ".wav", ".m4a", ".m4b", ".mp4", ".mkv", ".webm", ".flac", ".ogg", ".wma"}
            audio_files = [f for f in audio_path.rglob("*") if f.suffix.lower() in audio_extensions]

            if not audio_files:
                print(f"No audio files found in {audio_path}")
                sys.exit(0)

            print(f"Found {len(audio_files)} audio files. Processing...")
            print("-" * 50)

            for i, file in enumerate(audio_files, 1):
                print(f"\n[{i}/{len(audio_files)}] Transcribing: {file.name}")
                try:
                    segments, duration, language = transcribe_audio(
                        str(file),
                        model_name=args.model,
                        device=args.device,
                        language=args.language,
                        compute_type=args.compute_type,
                        beam_size=args.beam_size,
                        word_timestamps=args.word_timestamps,
                    )

                    output_dir = Path(args.output) if args.output else file.parent
                    output_dir.mkdir(parents=True, exist_ok=True)

                    save_transcript(segments, file, output_format=args.format, language=language)
                except Exception as e:
                    print(f"ERROR: {e}", file=sys.stderr)
                    continue

            print("\n" + "-" * 50)
            print("✓ Batch transcription complete!")

        # Single file mode
        else:
            segments, duration, language = transcribe_audio(
                str(audio_path),
                model_name=args.model,
                device=args.device,
                language=args.language,
                compute_type=args.compute_type,
                beam_size=args.beam_size,
                word_timestamps=args.word_timestamps,
            )

            output_dir = Path(args.output) if args.output else audio_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)

            save_transcript(segments, audio_path, output_format=args.format, language=language)

            print("\n✓ Transcription successful!")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
