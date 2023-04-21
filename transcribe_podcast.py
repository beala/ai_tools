# Description: Transcribe a podcast episode into text using OpenAI's Whisper API
#
# Pre-requisites:
#   1. brew install ffmpeg
#   2. pip install -r requirements.txt
#   3. Set `openai.api_key` to your OpenAI API key
import argparse
import shutil
import sys
import tempfile

import requests
from bs4 import BeautifulSoup
import os
import openai
from pydub import AudioSegment

import utils
from utils import openai_api_key, p

openai.api_key = openai_api_key()


def download_audio(url, tmp_dir):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    audio_url = soup.find("source", {"type": "audio/mpeg"})["src"]
    p("Found audio URL:", audio_url)
    audio_data = requests.get(audio_url)
    filename = os.path.join(tmp_dir, "podcast.mp3")
    p(f"Downloading audio to {filename}... ", end="", flush=True)
    with open(filename, "wb") as f:
        f.write(audio_data.content)
    p("✅")
    return filename


def break_audio_into_chunks(filename, tmp_dir, max_size_bytes=25 * 1024 * 1024):
    audio = AudioSegment.from_mp3(filename)
    chunk_length_ms = 10 * 60 * 1000  # 10 minutes
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_file = os.path.join(tmp_dir, f"chunk_{i}.mp3")
        p(f"Exporting chunk {i + 1} of {len(chunks)} to {chunk_file}... ", end="", flush=True)
        chunk.export(chunk_file, format="mp3")
        p("✅")
        if os.path.getsize(chunk_file) < max_size_bytes:
            chunk_files.append(chunk_file)
        else:
            os.remove(chunk_file)
            raise Exception("Chunk too large")
    return chunk_files


def transcribe_audio_chunks(chunk_files):
    transcript = []
    for i, chunk_file in enumerate(chunk_files):
        p(f"Transcribing chunk {i + 1} of {len(chunk_files)}...", end=" ", flush=True)
        if args.dry_run:
            chunk_transcript = {"text": "This is a test transcript"}
        else :
            with open(chunk_file, "rb") as audio_file:
                if i > 0:
                    chunk_transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt=transcript[-1])
                else:
                    chunk_transcript = openai.Audio.transcribe("whisper-1", audio_file)
        transcript += [chunk_transcript["text"]]
        p("✅")
    return transcript


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("OVERCAST_LINK", type=str,
                        help="Overcast link to podcast episode (eg https://overcast.fm/+YsPQCIdOs)")
    parser.add_argument("--output", type=str, help="Output file to write transcript to. Otherwise, prints to stdout.")
    parser.add_argument("--tmp", type=str,
                        help="Temporary directory to use for downloading and chunking audio. Defaults to a new "
                             "temporary directory.")
    parser.add_argument("--preserve", action="store_true",
                        help="Preserve temporary directory after running. Defaults to False.")
    parser.add_argument("--silent", action="store_true",
                        help="Silence all status updates. Defaults to False.")
    parser.add_argument("--dry_run", action="store_true",
                        help="Don't actually query OpenAI. Useful for debugging. Defaults to False.")
    args = parser.parse_args()

    if args.silent:
        utils.SILENT = True

    if args.tmp is None:
        tmp = tempfile.mkdtemp(prefix="podcast-transcription-")
    else:
        tmp = args.tmp

    audio_file_path = download_audio(args.OVERCAST_LINK, tmp)
    chunk_files = break_audio_into_chunks(audio_file_path, tmp)
    transcripts = transcribe_audio_chunks(chunk_files)

    if not args.preserve:
        shutil.rmtree(tmp, ignore_errors=True)

    out = " ".join(transcripts)
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
        p(f"Wrote transcript to {args.output}")
    else:
        print(out, file=sys.stdout)
