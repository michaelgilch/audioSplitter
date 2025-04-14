import os
import json
import numpy as np
import soundfile as sf
import argparse

parser = argparse.ArgumentParser(description="Create speaker tracks from diarized transcript")
parser.add_argument("json_file", help="Path to JSON file with diarization results")
args = parser.parse_args()

json_path = os.path.abspath(args.json_file)
base_name = os.path.splitext(os.path.basename(json_path))[0]  # e.g., "interview"
dir_path = os.path.dirname(json_path)
wav_path = os.path.join(dir_path, base_name + ".wav")

if not os.path.isfile(wav_path):
    print(f"Error: Expected WAV file not found: {wav_path}")
    exit(1)

print(f"Loading diarization data from {args.json_file}")
with open(json_path, 'r') as f:
  result = json.load(f)
		
print(f"Loading audio from {wav_path}")
data, samplerate = sf.read(wav_path)
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
	output_path = os.path.join(dir_path, f"{base_name}_{speaker}.wav")
	print(f"Exporting to {output_path}")
	sf.write(output_path, silent_track, samplerate)
