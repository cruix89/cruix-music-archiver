#!/usr/bin/with-contenv bash

# environment variable configurations
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
    echo -e "\nnumber of normalized files: ${#normalized_files[@]}"
}

# function to save to the normalized list
save_to_normalized_list() {
    echo "$1" >> "$normalized_list_file"
}

# function to process audio file
process_file() {
    local src_file="$1"
    local log_file="$2"
    local output_file
    # Add "_TEMP" suffix to the output file name
    output_file="$(dirname "$src_file")/$(basename "${src_file%.*}")_TEMP"

    # FFMPEG command to process the file and add "_TEMP" suffix
    ffmpeg -y -i "$src_file" -af "loudnorm=I=-14:TP=-1:LRA=11:print_format=summary" -b:a 320k "$output_file.mp3" &>> "$log_file"

    # check if output file exists
    if [[ -f "$output_file.mp3" ]]; then
        save_to_normalized_list "$src_file"
        echo "processed: $src_file"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR PROCESSING FILE: $src_file" >> "$log_file"
    fi
}

# function to clean up original files (after processing)
clean_up_original_files() {
    local target_dir="$1"
    local log_file="$2"
    # File extensions to be deleted after processing
    local extensions="flac|wav|aac|m4a|ogg|wma|alac|aiff|opus|dsd|amr|ape|ac3|mp2|wv|m4b|mka|spx|caf|snd|gsm|tta|voc|w64|s8|u8"

    echo "cleaning up original files..." >> "$log_file"
    find "$target_dir" -type f -regextype posix-extended -iregex ".*\.(${extensions})$" -exec rm -f {} \;
    echo "cleanup completed." >> "$log_file"
}

# function to rename the processed files (removing "_TEMP")
rename_processed_files() {
    local target_dir="$1"
    local log_file="$2"

    echo "renaming processed files..." >> "$log_file"
    find "$target_dir" -type f -name "*_TEMP.mp3" | while read -r temp_file; do
        local new_file="${temp_file/_TEMP/}"
        if mv "$temp_file" "$new_file"; then
            echo "renamed: $temp_file -> $new_file" >> "$log_file"
        else
            echo "failed to rename: $temp_file" >> "$log_file"
        fi
    done
    echo "renaming completed." >> "$log_file"
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
    echo "total files found: ${#audio_files[@]}"
    echo "normalizing files..."

    # process audio files one by one
    for src_file in "${audio_files[@]}"; do
        if ! grep -qx "$src_file" "$normalized_list_file"; then
            process_file "$src_file" "$log_file"
        else
            ((skipped_files++))
        fi
    done

    # clean up original files
    clean_up_original_files "/downloads" "$log_file"

    # rename processed files (remove _TEMP)
    rename_processed_files "/downloads" "$log_file"

    # final summary
    echo "summary: ${#audio_files[@]} processed files, $skipped_files ignored files (already normalized)."
    echo "files normalized successfully."
}

main