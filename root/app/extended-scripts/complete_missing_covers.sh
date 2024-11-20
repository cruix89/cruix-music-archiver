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
        log "error: directory not found: $1"
        return 1
    fi
    return 0
}

# Function to find the highest resolution image
find_best_image() {
    local image_dir="$1"
    local best_image=""
    local max_resolution=0

    # Check all supported image files
    for image in "$image_dir"/*.{jpg,jpeg,png,webp}; do
        if [[ -f "$image" ]]; then
            # Use ImageMagick's identify to get the image dimensions
            dimensions=$(identify -format "%wx%h" "$image" 2>/dev/null)
            width=$(echo "$dimensions" | cut -d'x' -f1)
            height=$(echo "$dimensions" | cut -d'x' -f2)

            if [[ -n "$width" && -n "$height" ]]; then
                resolution=$(( width * height ))
                if [[ $resolution -gt $max_resolution ]]; then
                    max_resolution=$resolution
                    best_image="$image"
                fi
            fi
        fi
    done

    echo "$best_image"
}

# Function to crop image to square, keeping the center
crop_image_to_square() {
    local image="$1"
    local destination="$2"

    # Use ImageMagick to crop the image
    dimensions=$(identify -format "%wx%h" "$image" 2>/dev/null)
    width=$(echo "$dimensions" | cut -d'x' -f1)
    height=$(echo "$dimensions" | cut -d'x' -f2)

    # Determine the size of the square (smallest dimension)
    if [[ $width -gt $height ]]; then
        crop_size=$height
    else
        crop_size=$width
    fi

    # Perform the crop using the center of the image
    convert "$image" -gravity Center -crop "${crop_size}x${crop_size}+0+0" +repage "$destination"
}

# Function to copy the source file to the destination
copy_file() {
    local source="$1"
    local destination="$2"

    if cp "$source" "$destination"; then
        log "file copied: $source TO $destination"
    else
        log "error copying: $source TO $destination"
    fi
}

# Main function to scan directories and associate images to audio files
process_directory() {
    local directory="$1"

    if ! validate_directory "$directory"; then
        return
    fi

    echo -e "[cruix-music-archiver] initiating operations in directory: $directory... ⚙️  🚀  let the music magic begin!"

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
            echo -e "🖼️  best image found: $best_image"
            for audio_file in "${audio_files[@]}"; do
                audio_name=$(basename "$audio_file" | sed 's/\.[^.]*$//')
                # if the audio file does not have a corresponding image, crop and copy the best image
                if [[ ! -f "$sub_dir/$audio_name.jpg" ]]; then
                    destination="$sub_dir/$audio_name.jpg"
                    crop_image_to_square "$best_image" "$destination"
                    echo -e "🖼️  image cropped and teleported to: $destination. ready for display in the gallery of awesomeness!"
                fi
            done
        else
            echo -e "🔍  no suitable image found in: $sub_dir. looks like the photo shoot got canceled!"
        fi
    done

    echo -e "[cruix-music-archiver] mission complete in directory: $directory 🏆  🎧"
}

# script execution
echo -e "[cruix-music-archiver] cover rescue mission engaged! 🦸‍♂️  commencing the epic quest to complete missing covers... 📀"
process_directory "$music_dir"
echo -e "[cruix-music-archiver] missing covers quest finished. 🏆  all missing covers have been restored! 📀"