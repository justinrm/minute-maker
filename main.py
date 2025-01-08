import os
import subprocess
import argparse
import whisper
from pyannote.audio import Pipeline
import json
import sys


def download_audio(youtube_url, audio_path="audio.mp3"):
    """Download audio from YouTube using yt-dlp and convert to MP3."""
    try:
        print("[INFO] Downloading audio from YouTube...")
        subprocess.run(
            ["yt-dlp", "-x", "--audio-format", "mp3", "-o", audio_path, youtube_url],
            check=True,
        )
        print(f"[INFO] Audio downloaded and saved as {audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to download audio: {e}")
        sys.exit(1)


def transcribe_audio(audio_path, model_name="large"):
    """Transcribe audio using Whisper."""
    print("[INFO] Transcribing audio with Whisper...")
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    print("[INFO] Transcription completed.")
    return result


def diarize_audio(audio_path, hf_token):
    """Perform speaker diarization using Pyannote."""
    print("[INFO] Running speaker diarization...")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization", use_auth_token=hf_token
    )
    diarization = pipeline(audio_path)
    print("[INFO] Diarization completed.")
    return diarization


def merge_transcription_and_diarization(transcription, diarization):
    """Combine Whisper transcription with Pyannote diarization results."""
    print("[INFO] Merging transcription with speaker diarization...")
    diarization_segments = [
        {"start": turn.start, "end": turn.end, "speaker": speaker}
        for turn, _, speaker in diarization.itertracks(yield_label=True)
    ]

    annotated_transcription = []
    for segment in transcription["segments"]:
        start, end, text = segment["start"], segment["end"], segment["text"]
        speaker = "Unknown"
        for dia in diarization_segments:
            if dia["start"] <= start < dia["end"]:
                speaker = dia["speaker"]
                break
        annotated_transcription.append({"speaker": speaker, "start": start, "end": end, "text": text})

    print("[INFO] Merging completed.")
    return annotated_transcription


def save_to_file(data, file_path, file_format="txt"):
    """Save annotated transcription to a file."""
    print(f"[INFO] Saving output to {file_path}...")
    if file_format == "json":
        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)
    else:  # Default to TXT format
        with open(file_path, "w") as file:
            for entry in data:
                file.write(f"{entry['speaker']} ({entry['start']:.2f}-{entry['end']:.2f}s): {entry['text']}\n")
    print(f"[INFO] Output saved to {file_path}")


def main():
    parser = argparse.ArgumentParser(description="Transcribe and annotate meeting videos.")
    parser.add_argument("--url", type=str, help="YouTube video URL", required=True)
    parser.add_argument("--model", type=str, default="large", help="Whisper model size")
    parser.add_argument("--output-dir", type=str, default=".", help="Output directory")
    parser.add_argument("--hf-token", type=str, required=True, help="Hugging Face access token")
    args = parser.parse_args()

    audio_path = os.path.join(args.output_dir, "meeting_audio.mp3")

    # Step 1: Download and extract audio
    download_audio(args.url, audio_path)

    # Step 2: Transcribe audio
    transcription = transcribe_audio(audio_path, args.model)

    # Step 3: Perform speaker diarization
    diarization = diarize_audio(audio_path, args.hf_token)

    # Step 4: Merge transcription and diarization
    annotated_transcription = merge_transcription_and_diarization(transcription, diarization)

    # Step 5: Save outputs
    save_to_file(transcription, os.path.join(args.output_dir, "transcription.json"), file_format="json")
    save_to_file(annotated_transcription, os.path.join(args.output_dir, "annotated_transcription.txt"), file_format="txt")

    # Cleanup temporary audio file
    os.remove(audio_path)
    print("[INFO] Temporary audio file removed.")


if __name__ == "__main__":
    main()

