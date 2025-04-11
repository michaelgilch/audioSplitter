import argparse
import json
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

base_name = os.path.splitext(os.path.basename(args.audio_file))[0]
output_file = f"{base_name}.json"

config = aai.TranscriptionConfig(
	speaker_labels=True,
	speakers_expected=3,
)

try:
	transcriber = aai.Transcriber()
	transcript = transcriber.transcribe(args.audio_file, config)

	transcript_dict = {
		"id": transcript.id,
		# "status": transcript.status,
		"text": transcript.text,
		"audio_duration": transcript.audio_duration,
	}
	
	# # Manually serialize words if they exist
	# if hasattr(transcript, 'words') and transcript.words:
	# 	transcript_dict["words"] = []
	# 	for word in transcript.words:
	# 		word_dict = {
	# 			"text": word.text,
	# 			"start": word.start,
	# 			"end": word.end,
	# 			"confidence": word.confidence
	# 		}
			
	# 		# Add speaker if available
	# 		if hasattr(word, 'speaker') and word.speaker:
	# 			word_dict["speaker"] = word.speaker
							
	# 			transcript_dict["words"].append(word_dict)
	
	# Manually serialize utterances if they exist
	if hasattr(transcript, 'utterances') and transcript.utterances:
		transcript_dict["utterances"] = []
		for utterance in transcript.utterances:
			utterance_dict = {
				"text": utterance.text,
				"start": utterance.start,
				"end": utterance.end
			}
					
			# Add speaker if available
			if hasattr(utterance, 'speaker') and utterance.speaker:
				utterance_dict["speaker"] = utterance.speaker
								
			transcript_dict["utterances"].append(utterance_dict)
	
	with open(output_file, "w", encoding="utf-8") as f:
		json.dump(transcript_dict, f, indent=2, ensure_ascii=False)

	# for utterance in transcript.utterances:
	# 	print(f"<SPEAKER>{utterance.speaker},<START>{utterance.start},<END>{utterance.end},<TEXT>{utterance.text}")
except Exception as e:
	print(f"Error during transcription: {e}")
	sys.exit(1)