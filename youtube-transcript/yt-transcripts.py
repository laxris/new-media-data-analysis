#!/usr/bin/python

import subprocess
import sys
import glob
import webvtt
import chardet
from typing import List

def convert(filename: str, auto: bool = False) -> None:
    """
    Convert WebVTT file to plain text.

    :param filename: The name of the WebVTT file.
    :param auto: Whether to automatically generate subtitles or not. Defaults to False.
    """
    vtt = webvtt.read(filename)
    transcript = ""

    lines = []
    for line in vtt:
        lines.extend(line.text.strip().splitlines())

    previous = None
    for line in lines:
        if line == previous:
            continue
        transcript += " " + line
        previous = line

    with open(filename + ".txt", "w", encoding='utf-8', errors='replace') as fh:
        fh.write(transcript)


def download_step(url: str, yt_dlp_path: str, auto: bool = False) -> None:
    """
    Download subtitles from YouTube video.

    :param url: The URL of the YouTube video.
    :param yt_dlp_path: Path to the yt-dlp executable.
    :param auto: Whether to automatically generate subtitles or not. Defaults to False.
    """
    args = [
        yt_dlp_path,
        "--write-auto-sub" if auto else "--write-sub",
        "--sub-langs=en",
        "--skip-download",
    ]

    result = subprocess.run(args + [url], capture_output=True)

    try:
        enc = chardet.detect(result.stdout)["encoding"]
    except:
        enc = "utf-8"

    if enc is None:
        enc = "utf-8"

    print(result.stdout.decode(enc))

    try:
        enc = chardet.detect(result.stderr)["encoding"]
    except:
        enc = "utf-8"

    if enc is None:
        enc = "utf-8"

    print(result.stderr.decode(enc))


def process_urls(urls: List[str], done: List[str], yt_dlp_path: str) -> None:
    """ 
    Process a list of URLs.

    :param urls: A list of URLs.
    :param done: A list of URLs that have already been processed.
    :param yt_dlp_path: Path to the yt-dlp executable.
    """
    
    error = []
    resolved = []

    for pos, url in enumerate(urls):
        print(f"{pos + 1} out of {len(urls)}")

        if url in done:
            print(f"Skipping {url}")
            continue

        print(f"Downloading {url}")
        try:
            download_step(url, yt_dlp_path, auto=True)
            resolved.append(url)
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            error.append(url)

    with open("errors.txt", "w") as fh:
        for err in error:
            fh.write(err)

    with open("resolved.txt", "w") as fh:
        for res in resolved:
            fh.write(res)

    for file in glob.glob("*.vtt"):
        print(f"Converting transcript from {file}")
        convert(file)


# This is a silly wrapper around youtube-dl to download transcripts from a list of URLs.
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: yt-transcripts.py <list of youtube-urls>")
        exit()

    print(f"running over {sys.argv[1]}")

    yt_dlp_path = "/home/chris/anaconda3/bin/yt-dlp"

    try:
        with open("resolved.txt", "r") as fh:
            done_urls = fh.readlines()
    except:
        done_urls = []

    with open(sys.argv[1], "r") as fh:
        input_urls = fh.readlines()

    process_urls(input_urls, done_urls, yt_dlp_path)