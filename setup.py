#!/usr/bin/env python3
"""Setup configuration for whisper-amd-windows."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").split("\n")
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="whisper-amd-windows",
    version="1.0.0",
    author="Chharith Oeun",
    author_email="chharith@gmail.com",
    description="Run OpenAI Whisper on AMD GPU on Windows via DirectML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChharithOeun/whisper-amd-windows",
    project_urls={
        "Bug Tracker": "https://github.com/ChharithOeun/whisper-amd-windows/issues",
        "Documentation": "https://github.com/ChharithOeun/whisper-amd-windows#readme",
        "Source Code": "https://github.com/ChharithOeun/whisper-amd-windows",
    },
    packages=find_packages(),
    py_modules=["scripts.transcribe", "scripts.benchmark", "scripts.verify_gpu"],
    python_requires=">=3.10",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
    ],
    keywords=(
        "whisper speech-to-text amd-gpu directml rdna windows "
        "transcription audio-processing gpu-acceleration"
    ),
    entry_points={
        "console_scripts": [
            "whisper-transcribe=scripts.transcribe:main",
            "whisper-benchmark=scripts.benchmark:main",
            "whisper-verify=scripts.verify_gpu:main",
        ],
    },
    zip_safe=False,
)
