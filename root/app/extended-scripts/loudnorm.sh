#!/usr/bin/with-contenv bash

# Environment variable configurations
normalized_log_dir="${normalized_log_dir:-/config/logs}"
normalized_list_file="${normalized_list_file:-/config/loudnorm_cache.txt}"
cache_dir="/config/cache"

# Function to check if ffmpeg is installed
check_ffmpeg() {
    if ! command -v ffmpeg &> /dev/null; then
        echo "FFMPEG IS NOT INSTALLED OR NOT AVAILABLE IN THE PATH."
        exit 1
    fi
}

# Function to load the list of normalized files
load_normalized_list() {
    if [[ ! -f "$normalized_list_file" ]]; then
        touch "$normalized_list_file"
    fi
    mapfile -t normalized_files < "$normalized_list_file"
    echo -e "\nNumber of normalized files: ${#normalized_files[@]}"
}

# Function to save to the normalized list
save_to_normalized_list() {
    echo "$1" >> "$normalized_list_file"
}

# Function to process the audio file
process_file() {
    local src_file="$1"
    local log_file="$2"
    # Declare the variable
    local output_file
    # Assign the value separately, removing the original extension
    output_file="${cache_dir}/$(basename "${src_file%.*}")"

    # FFMPEG command to process the file
    ffmpeg -y -i "$src_file" -af "loudnorm=I=-14:TP=-1:LRA=11:print_format=summary" -b:a 320k "$output_file.mp3" &>> "$log_file"

    # Capture the exit code of ffmpeg
    local exit_code=$?

    # Check if the output file exists and if the exit code is 0
    if [[ -f "$output_file.mp3" && $exit_code -eq 0 ]]; then
        # Delete the original file
        rm -f "$src_file"
        # Move the normalized file to the original path with .mp3 extension
        mv "$output_file.mp3" "${src_file%.*}.mp3"

        save_to_normalized_list "${src_file%.*}.mp3"
        echo "Processed and replaced: ${src_file%.*}.mp3"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR PROCESSING FILE: $src_file" >> "$log_file"
    fi
}

# Main function
main() {
    check_ffmpeg
    load_normalized_list

    local log_file="$normalized_log_dir/loudnorm.log"
    local skipped_files=0

    # Ensure the cache directory exists
    if [[ ! -d "$cache_dir" ]]; then
        mkdir -p "$cache_dir"
        echo "Created cache directory: $cache_dir"
    fi

    while true; do
        # Collect an unnormalized audio file
        local src_file
        src_file=$(find "/downloads" -type f \( -name "*.mp3" -o -name "*.flac" -o -name "*.wav" -o -name "*.aac" -o -name "*.m4a" -o -name "*.ogg" -o -name "*.wma" -o -name "*.alac" -o -name "*.aiff" -o -name "*.opus" -o -name "*.dsd" -o -name "*.amr" -o -name "*.ape" -o -name "*.ac3" -o -name "*.mp2" -o -name "*.wv" -o -name "*.m4b" -o -name "*.mka" -o -name "*.spx" -o -name "*.caf" -o -name "*.snd" -o -name "*.gsm" -o -name "*.tta" -o -name "*.voc" -o -name "*.w64" -o -name "*.s8" -o -name "*.u8" \) ! -exec grep -qx {} "$normalized_list_file" \; -print -quit)

        # If there are no more files to process, exit the loop
        if [[ -z "$src_file" ]]; then
            break
        fi

        # Check if the file was skipped
        if grep -qx "$src_file" "$normalized_list_file"; then
            ((skipped_files++))
            echo "Skipped: $src_file"
            continue
        fi

        process_file "$src_file" "$log_file"
    done

    # Final summary
    echo "All files have been processed and normalized successfully."
    echo "Total skipped files: $skipped_files"
}

main