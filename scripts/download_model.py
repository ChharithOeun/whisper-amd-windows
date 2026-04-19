#!/usr/bin/env python3
"""
Download Whisper models from HuggingFace Hub.

Automatically caches models in the faster-whisper model directory.
Supports all standard Whisper models (tiny, base, small, medium, large-v2, large-v3).

Usage:
    python download_model.py
    python download_model.py --model large-v3
    python download_model.py --all
"""

import argparse
import sys

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    print("ERROR: huggingface-hub not installed.")
    print("Install with: pip install huggingface-hub")
    sys.exit(1)

try:
    from faster_whisper import WhisperModel
except ImportError:
    print("ERROR: faster-whisper not installed.")
    print("Install with: pip install faster-whisper")
    sys.exit(1)


def get_model_cache_dir():
    """
    Get the cache directory where Whisper models are stored.

    Returns:
        str: Path to model cache directory
    """
    import os
    from pathlib import Path

    # faster-whisper uses HF_HOME or defaults to ~/.cache/huggingface
    hf_home = os.environ.get('HF_HOME')
    if hf_home:
        return str(Path(hf_home) / 'hub')
    else:
        return str(Path.home() / '.cache' / 'huggingface' / 'hub')


def download_model(model_name):
    """
    Download a Whisper model.

    Args:
        model_name (str): Model size (tiny, base, small, medium, large-v2, large-v3)

    Returns:
        bool: True if successful, False otherwise
    """
    print(f"Downloading '{model_name}' model...")
    try:
        model = WhisperModel(model_name, device='cpu')
        print(f"✓ Model '{model_name}' downloaded successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to download '{model_name}': {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download Whisper models from HuggingFace.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python download_model.py
  python download_model.py --model large-v3
  python download_model.py --all
        """,
    )

    parser.add_argument(
        "--model",
        default="small",
        choices=["tiny", "base", "small", "medium", "large-v2", "large-v3"],
        help="Whisper model to download (default: small)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Download all models (tiny, base, small, medium, large-v2, large-v3)",
    )

    args = parser.parse_args()

    cache_dir = get_model_cache_dir()
    print(f"\nModel cache location: {cache_dir}\n")

    if args.all:
        models = ["tiny", "base", "small", "medium", "large-v2", "large-v3"]
        print(f"Downloading all {len(models)} models...")
        print("-" * 50)

        results = []
        for model in models:
            success = download_model(model)
            results.append((model, success))

        print("-" * 50)
        successful = sum(1 for _, success in results if success)
        print(f"\nDownloaded {successful}/{len(models)} models successfully")

        if successful < len(models):
            sys.exit(1)
    else:
        success = download_model(args.model)
        if not success:
            sys.exit(1)

    print(f"\nAll models cached at: {cache_dir}")


if __name__ == "__main__":
    main()
