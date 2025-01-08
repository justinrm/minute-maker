# Transcription and Diarization Tool

A Python-based command-line tool for downloading YouTube audio, transcribing it using OpenAI's Whisper, performing speaker diarization with Pyannote, and exporting the results in structured formats. This project is designed for users seeking offline transcription and diarization without relying on external summarization APIs.

---

## Features

1. **YouTube Audio Download**  
   Automatically downloads and extracts audio from YouTube videos using `yt-dlp`.

2. **Speech-to-Text Transcription**  
   Leverages OpenAI Whisper to transcribe audio with high accuracy. Supports various model sizes (`tiny` to `large`).

3. **Speaker Diarization**  
   Identifies and separates speakers in the audio using Pyannote’s pretrained diarization models.

4. **Structured Outputs**  
   Saves transcription and diarization results in JSON and TXT formats for easy review.

5. **Customizable Settings**  
   Configure output directory, model size, and Hugging Face tokens via a `.env` file.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Example Outputs](#example-outputs)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [License](#license)

---

## Prerequisites

1. **Python 3.7 or later**  
   Ensure Python is installed on your system.

2. **pip**  
   The Python package manager to install dependencies.

3. **Hugging Face Access Token**  
   - Required for Pyannote speaker diarization.
   - Obtain a token at [Hugging Face](https://huggingface.co/).

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/justinrm/minute-maker.git
   cd minute-maker
   ```

2. **Install Dependencies**:
   Using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   Or using `setup.py`:
   ```bash
   pip install .
   ```

3. **Set Up the Environment File**:
   Create a `.env` file and configure it with your Hugging Face token and desired settings. Use the provided `template.env` for reference.

---

## Usage

Run the tool directly or via the command-line entry point.

### 1. Basic Command
Transcribe and diarize a YouTube video:
```bash
python main.py --url "<YouTube URL>" --hf-token "<Hugging Face Token>"
```

### 2. Use a Specific Whisper Model
```bash
python main.py --url "<YouTube URL>" --hf-token "<Hugging Face Token>" --model "small"
```

### 3. Change Output Directory
```bash
python main.py --url "<YouTube URL>" --hf-token "<Hugging Face Token>" --output-dir "./output"
```

### 4. Installed Command-Line Tool
If you installed the project via `setup.py`, use the `transcribe` command:
```bash
transcribe --url "<YouTube URL>" --hf-token "<Hugging Face Token>"
```

---

## Configuration

Use the `.env` file to manage environment variables:

### Example `.env` File
```dotenv
# Directory for output files (default: current directory)
OUTPUT_DIR=./output

# Hugging Face Access Token (required for Pyannote diarization)
HF_ACCESS_TOKEN=hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Whisper Model to Use (tiny, base, small, medium, large)
WHISPER_MODEL=small
```

---

## Example Outputs

### 1. JSON File
A structured transcription and diarization output:
```json
[
  {
    "speaker": "Speaker 1",
    "start": 0.0,
    "end": 5.3,
    "text": "Hello everyone, welcome to the meeting."
  },
  {
    "speaker": "Speaker 2",
    "start": 5.5,
    "end": 10.2,
    "text": "Thank you! Let's get started with today's agenda."
  }
]
```

### 2. TXT File
Human-readable transcription with diarization:
```
Speaker 1 (0.0-5.3s): Hello everyone, welcome to the meeting.
Speaker 2 (5.5-10.2s): Thank you! Let's get started with today's agenda.
```

---

## Limitations

1. **Performance on Older Hardware**:
   - Whisper’s larger models may be slow or unusable on systems without GPUs. Use smaller models (`tiny`, `small`) if needed.

2. **Long Audio Files**:
   - Processing very long videos may consume significant memory and CPU/GPU resources.

3. **Diarization Accuracy**:
   - Speaker diarization may have reduced accuracy in overlapping or noisy audio.

---

## Roadmap

Planned enhancements include:
1. **Chunked Processing**:
   - Split long audio files into smaller chunks to reduce memory usage.

2. **Summarization**:
   - Integrate offline summarization using open-source libraries (e.g., Hugging Face transformers).

3. **GUI/Front-End**:
   - Build a simple desktop or web interface for non-technical users.

4. **Cloud Deployment**:
   - Enable easy deployment on cloud platforms (e.g., AWS, Google Cloud).

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Final Notes

This tool is designed to simplify transcription and diarization workflows, especially for users on a budget or without API credits. Contributions are welcome—feel free to submit a pull request or open an issue!

Happy transcribing! 🎤
