#!/usr/bin/with-contenv bash

# Absolute directories for logs and downloads
log_dir='/config/logs'
music_dir='/music'

# Ensure the log directory exists
mkdir -p "$log_dir"

# Log file
log_file="$log_dir/complete_missing_covers.log"

# List of supported audio formats
ffmpeg_supported_audio_formats=(
    ".mp3" ".flac" ".wav" ".aac" ".m4a" ".ogg" ".wma" ".alac" ".aiff"
    ".opus" ".dsd" ".amr" ".ape" ".ac3" ".mp2" ".wv" ".m4b" ".mka"
    ".spx" ".caf" ".snd" ".gsm" ".tta" ".voc" ".w64" ".s8" ".u8"
)

# Function to log messages
log() {
    echo "$1" | tee -a "$log_file"
}

# Function to validate directory
validate_directory() {
    if [[ ! -d "$1" ]]; then
        log "ERROR: DIRECTORY NOT FOUND: $1"
        return 1
    fi
    return 0
}

# Function to find the closest image to 544x544
find_best_image() {
    local image_dir="$1"
    local best_image=""
    local best_diff=99999

    # Check all supported image files
    for image in "$image_dir"/*.{jpg,jpeg,png,webp}; do
        if [[ -f "$image" ]]; then
            # Use ImageMagick's identify to get the image dimensions
            dimensions=$(identify -format "%wx%h" "$image" 2>/dev/null)
            width=$(echo "$dimensions" | cut -d'x' -f1)
            height=$(echo "$dimensions" | cut -d'x' -f2)

            if [[ -n "$width" && -n "$height" ]]; then
                diff=$(( (width - 544) ** 2 + (height - 544) ** 2 ))
                if [[ $diff -lt $best_diff ]]; then
                    best_diff=$diff
                    best_image="$image"
                fi
            fi
        fi
    done

    echo "$best_image"
}

# Function to copy the source file to the destination
copy_file() {
    local source="$1"
    local destination="$2"

    if cp "$source" "$destination"; then
        log "FILE COPIED: $source TO $destination"
    else
        log "ERROR COPYING: $source TO $destination"
    fi
}

# Main function to scan directories and associate images to audio files
process_directory() {
    local directory="$1"

    if ! validate_directory "$directory"; then
        return
    fi

    log "starting process in directory: $directory"

    find "$directory" -type d | while read -r sub_dir; do
        # Search for images and audio files in the current subdirectory
        audio_files=()

        # Using mapfile to avoid splitting issues
        for audio_ext in "${ffmpeg_supported_audio_formats[@]}"; do
            mapfile -t temp_audio_files < <(find "$sub_dir" -maxdepth 1 -type f -name "*$audio_ext")
            audio_files+=("${temp_audio_files[@]}")  # Add to audio_files array
        done

        # If no audio files are found, skip the directory
        if [[ ${#audio_files[@]} -eq 0 ]]; then
            continue
        fi

        # Search for the best image in the directory
        best_image=$(find_best_image "$sub_dir")

        if [[ -n "$best_image" ]]; then
            log ""
            log "best image found: $best_image"
            log ""
            for audio_file in "${audio_files[@]}"; do
                audio_name=$(basename "$audio_file" | sed 's/\.[^.]*$//')
                # if the audio file does not have a corresponding image, copy the best image
                if [[ ! -f "$sub_dir/$audio_name.jpg" ]]; then
                    destination="$sub_dir/$audio_name.jpg"
                    copy_file "$best_image" "$destination"
                fi
            done
        else
            log "no suitable image found in: $sub_dir"
        fi
    done

    log "process completed in directory: $directory"
}

# script execution
log ""
log "starting missing covers completion..."
process_directory "$music_dir"
log "missing covers completion finished."