from setuptools import setup, find_packages

setup(
    name="transcription_diarization_tool",
    version="1.0.0",
    description="A tool for transcribing, diarizing, and annotating audio from YouTube videos.",
    author="Your Name",
    author_email="your_email@example.com",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=[
        "whisper==1.0",
        "pyannote.audio==2.1.1",
        "yt-dlp==2023.01.06",
        "torch>=1.12.0",
        "torchaudio>=0.12.0",
    ],
    entry_points={
        "console_scripts": [
            "transcribe=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

