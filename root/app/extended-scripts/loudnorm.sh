#!/usr/bin/with-contenv bash

# environment variable configurations
normalized_cache_dir="${normalized_cache_dir:-/config/cache}"
normalized_log_dir="${normalized_log_dir:-/config/logs}"
normalized_list_file="${normalized_list_file:-/config/loudnorm_cache.txt}"

# function to check if ffmpeg is installed
check_ffmpeg() {
    if ! command -v ffmpeg &> /dev/null; then
        echo "FFMPEG IS NOT INSTALLED OR NOT AVAILABLE IN THE PATH."
        exit 1
    fi
}

# function to load the list of normalized files
load_normalized_list() {
    if [[ ! -f "$normalized_list_file" ]]; then
        touch "$normalized_list_file"
    fi
    mapfile -t normalized_files < "$normalized_list_file"
    echo "number of normalized files: ${#normalized_files[@]}"
}

# function to save to the normalized list
save_to_normalized_list() {
    echo "$1" >> "$normalized_list_file"
}

# function to process audio file
process_file() {
    local src_file="$1"
    local log_file="$2"
    # use the same name as the source file, without fixed extension
    local output_file
    output_file="$normalized_cache_dir/$(dirname "$src_file")/$(basename "${src_file%.*}")"

    # create cache directory (with structure) if it doesn't exist
    mkdir -p "$(dirname "$output_file")"

    # FFMPEG command
    ffmpeg -y -i "$src_file" -af "loudnorm=I=-14:TP=-1:LRA=11:print_format=summary" -b:a 320k "$output_file.mp3" &>> "$log_file"

    # check if output file exists
    if [[ -f "$output_file.mp3" ]]; then
        # move the processed file before removing the source file
        if mv "$output_file.mp3" "$src_file"; then
            save_to_normalized_list "$src_file"
            rm "$src_file"
            echo "processed and moved: $src_file"
        else
            echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR MOVING FILE: $output_file.mp3 to $src_file" >> "$log_file"
        fi
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR PROCESSING FILE: $src_file" >> "$log_file"
    fi
}

# main function
main() {
    check_ffmpeg
    load_normalized_list

    local log_file="$normalized_log_dir/loudnorm.log"
    local audio_files=()
    local skipped_files=0

    # collect all audio files
    while IFS= read -r -d '' file; do
        audio_files+=("$file")
    done < <(find "/downloads" -type f \( -name "*.mp3" -o -name "*.flac" -o -name "*.wav" -o -name "*.aac" -o -name "*.m4a" -o -name "*.ogg" -o -name "*.wma" -o -name "*.alac" -o -name "*.aiff" -o -name "*.opus" -o -name "*.dsd" -o -name "*.amr" -o -name "*.ape" -o -name "*.ac3" -o -name "*.mp2" -o -name "*.wv" -o -name "*.m4b" -o -name "*.mka" -o -name "*.spx" -o -name "*.caf" -o -name "*.snd" -o -name "*.gsm" -o -name "*.tta" -o -name "*.voc" -o -name "*.w64" -o -name "*.s8" -o -name "*.u8" \) -print0)

    # print the number of audio files found
    echo "TOTAL FILES FOUND: ${#audio_files[@]}"
    echo "NORMALIZING FILES..."

    # process audio files one by one
    for src_file in "${audio_files[@]}"; do
        if ! grep -qx "$src_file" "$normalized_list_file"; then
            process_file "$src_file" "$log_file"
        else
            ((skipped_files++))
        fi
    done

    # final summary
    echo "Summary: ${#audio_files[@]} processed files, $skipped_files ignored files (already normalized)."
    echo "files normalized successfully."
}

main