import os
import json
import numpy as np
import soundfile as sf
import argparse

parser = argparse.ArgumentParser(description="Create speaker tracks from diarized transcript")
parser.add_argument("audio_file", help="Path to audio file (e.g., podcast.m4a)")
parser.add_argument("json_file", help="Path to JSON file with diarization results")
args = parser.parse_args()

print(f"Loading diarization data from {args.json_file}")
with open(args.json_file, 'r') as f:
	result = json.load(f)
		
print(f"Loading audio from {args.audio_file}")
data, samplerate = sf.read(args.audio_file)
duration = len(data) / samplerate
		
# For each speaker, create a track with silence where they're not speaking
speakers = set(utterance["speaker"] for utterance in result["utterances"] if "speaker" in utterance)
	
for speaker in speakers:
	print(f"Processing speaker {speaker}...")
	# Create empty (silent) audio the same length as the original
	silent_track = np.zeros_like(data)
			
	# Collect utterances for this speaker
	for utterance in result["utterances"]:
		if "speaker" in utterance and utterance["speaker"] == speaker:

			# Convert timestamps from milliseconds to samples
			start_sec = utterance["start"] / 1000
			end_sec = utterance["end"] / 1000
			start_sample = int(start_sec * samplerate)
			end_sample = int(end_sec * samplerate)
							
			# Ensure we don't go out of bounds
			if end_sample > len(data):
				end_sample = len(data)
							
			# Copy this segment to the silent track
			if start_sample < len(silent_track) and start_sample < end_sample:
				silent_track[start_sample:end_sample] = data[start_sample:end_sample]
			
	# Export the track
	output_file = f"speaker_{speaker}.wav"
	print(f"Exporting to {output_file}")
	sf.write(output_file, silent_track, samplerate)
