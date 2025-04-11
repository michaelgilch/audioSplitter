import argparse
import os
import sys
import assemblyai as aai

parser = argparse.ArgumentParser(description="Transcribe an audio file using AssemblyAI")
parser.add_argument("audio_file", help="Path to audio file to transcribe")
args = parser.parse_args()

if not os.path.isfile(args.audio_file):
	print(f"Error: File '{args.audio_file}' not found.")
	sys.exit(1)

try:
	with open("assemblyai_api_key.txt", "r") as file:
		assemblyai_api_key = file.read().strip()
	if not assemblyai_api_key:
		raise ValueError("API key is empty")
except Exception as e:
	print(f"Error reading API key: {e}")
	sys.exit(1)

aai.settings.api_key = assemblyai_api_key

try:
	transcriber = aai.Transcriber()
	transcript = transcriber.transcribe(args.audio_file)
	print(transcript.text)
except Exception as e:
	print(f"Error during transcription: {e}")
	sys.exit(1)