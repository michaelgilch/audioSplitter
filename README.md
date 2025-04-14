# audio_tools

Various audio tools for diarization, splitting, etc for podcasts.

## Environment Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## process_recordings.sh

Wrapper script to perform conversions, diarizations, and splitting of multiple files in a given directory.

```bash
Usage: ./process_recordings.sh directory-with-m4a-files/

Performs full conversion, diarization, and splitting of all m4a files in the given directory.

positional arguments
  directory-with-m4a-files  Directory containing some number of m4a files to process
```

## diarify.py

Performs speaker diarization of a wav file using AssemblyAI API.

```bash
usage: diarify.py [-h] audio_file

Performs Speaker Diarization of an audio file using AssemblyAI

positional arguments:
  audio_file  Path to audio file to process

options:
  -h, --help  show this help message and exit
```

## splitify.py

Splits audio file into multiple tracks, 1 for each speaker, based on diarify.py results.

```bash
usage: splitify.py [-h] json_file

Create speaker tracks from diarized transcript

positional arguments:
  json_file   Path to JSON file with diarization results

options:
  -h, --help  show this help message and exit
```

## bash-one-liners

To convert m4a to wav:
```bash
ffmpeg -i input.m4a output.wav
```

Mix Stereo to Mono and convert m4a to wav:
```bash
ffmpeg -i input.m4a -ac 1 output.wav
```

