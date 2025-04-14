#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory-with-m4a-files>"
    exit 1
fi

INPUT_DIR="$1"

if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: '$INPUT_DIR' is not a valid directory."
    exit 1
fi

# Process every m4a file in the directory
for m4a_file in "$INPUT_DIR"/*.m4a; do

    base_name=$(basename "$m4a_file" .m4a)

    wav_file="$INPUT_DIR/$base_name.wav"
    json_file="$INPUT_DIR/$base_name.json"

    echo "Conversion: $m4a_file → $wav_file"
    ffmpeg -y -i "$m4a_file" -ac 1 "$wav_file"

    echo "Diarization: $wav_file → $json_file"
    python diarify.py "$wav_file"

    echo "Splitting: $wav_file by speakers from $json_file into *_[ABC].wav"
    python splitify.py "$json_file"
done

echo "Conversions complete."
