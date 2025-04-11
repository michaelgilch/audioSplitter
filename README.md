# audio_tools

Various audio tools for diarization, splitting, etc for podcasts.

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
usage: splitify.py [-h] audio_file json_file

Create speaker tracks from diarized transcript

positional arguments:
  audio_file  Path to audio file (e.g., podcast.m4a)
  json_file   Path to JSON file with diarization results

options:
  -h, --help  show this help message and exit
```
