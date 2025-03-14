#!/usr/bin/with-contenv bash

# environment variable configurations
normalized_log_dir="${normalized_log_dir:-/config/logs}"
normalized_list_file="${normalized_list_file:-/config/loudnorm_cache.txt}"
cache_dir="/config/cache"
recycle_bin_dir="/config/recycle-bin"
failed_log_file="/config/loudnorm_failed_files_cache.txt"  # log file for failed files

# function to check if ffmpeg is installed
check_ffmpeg() {
    if ! command -v ffmpeg &> /dev/null; then
        echo -e "FFMPEG is Not Installed. 🚫  The Force is Weak in This System, No Media Manipulation Powers!"
        exit 1
    fi
}

# function to load the list of normalized files
load_normalized_list() {
    if [[ ! -f "$normalized_list_file" ]]; then
        touch "$normalized_list_file"
    fi
    mapfile -t normalized_files < "$normalized_list_file"
    echo -e "[cruix-music-archiver] Number of Normalized Files In Cache: ${#normalized_files[@]}  🗄️  Cache is Grooving! 🕺"
}

# function to save to the normalized list
save_to_normalized_list() {
    echo "$1" >> "$normalized_list_file"
}

# function to process the audio file
process_file() {
    local src_file="$1"
    local log_file="$2"
    # declare the variable
    local output_file
    # assign the value separately, removing the original extension
    output_file="${cache_dir}/$(basename "${src_file%.*}")"

    # FFMPEG command to process the file
    ffmpeg -y -i "$src_file" -af "loudnorm=I=-14:TP=-1:LRA=11:print_format=summary" -b:a 320k "$output_file.mp3" &>> "$log_file"

    # capture the exit code of ffmpeg
    local exit_code=$?

    # check if the output file exists and if the exit code is 0
    if [[ -f "$output_file.mp3" && $exit_code -eq 0 ]]; then
        # delete the original file
        rm -f "$src_file"
        # move the normalized file to the original path with .mp3 extension
        mv "$output_file.mp3" "${src_file%.*}.mp3"

        save_to_normalized_list "${src_file%.*}.mp3"
        echo -e "[ffmpeg] Loudnorm (ReplayGain) Successfully Applied to the File: ${src_file%.*}.mp3 🎶  The Audio is Now Perfectly Balanced! ⚖️"
    else
        echo -e "[ffmpeg] $(date '+%Y-%m-%d %H:%M:%S') - Error Processing File: $src_file 💾  File Not Found... Or Did it Just Disappear Into the Void? 💾 "
    fi
}

# function to move file to recycle bin, preserving directory structure
move_to_recycle_bin() {
    local src_file="$1"
    local dest_file="${recycle_bin_dir}${src_file}"
    local dest_dir

    # create the directory structure in the recycle bin
    dest_dir=$(dirname "$dest_file")
    mkdir -p "$dest_dir"

    # copy the file to the recycle bin
    if cp "$src_file" "$dest_file"; then
        # remove the original file after copying
        rm -f "$src_file"
        echo -e "[cruix-music-archiver] Copied and Removed $src_file to Recycle Bin: $dest_file  💾  The File Has Been Deleted From the Matrix!  🌀 "
        # log the file path to loudnorm_failed_files.log
        echo -e "[cruix-music-archiver] $(date '+%Y-%m-%d %H:%M:%S') - Moved to Recycle Bin: $src_file" >> "$failed_log_file"
    else
        echo -e "[cruix-music-archiver] Failed to Copy $src_file to Recycle Bin: $dest_file 💾  Transfer Failed — The File Has Gone Rogue! 💾"
    fi
}

# main function
main() {
    check_ffmpeg
    load_normalized_list

    local log_file="$normalized_log_dir/loudnorm.log"
    local skipped_files=0
    local max_attempts=999
    declare -A attempt_count  # associative array to track attempts for each file

    # ensure the cache directory exists
    if [[ ! -d "$cache_dir" ]]; then
        mkdir -p "$cache_dir"
        echo -e "[cruix-music-archiver] Created Cache Directory: $cache_dir ✨  The Cache is Ready for Action! ✨"
    fi

    # ensure the recycle bin directory exists
    if [[ ! -d "$recycle_bin_dir" ]]; then
        mkdir -p "$recycle_bin_dir"
        echo -e "[cruix-music-archiver] Created Recycle Bin Directory: $recycle_bin_dir ♻️  Ready to Catch Some Strays! ♻️"
    fi

    while true; do
        # collect an rough audio file
        local src_file
        src_file=$(find "/music" -type f \( -name "*.mp3" -o -name "*.flac" -o -name "*.wav" -o -name "*.aac" -o -name "*.m4a" -o -name "*.ogg" -o -name "*.wma" -o -name "*.alac" -o -name "*.aiff" -o -name "*.opus" -o -name "*.dsd" -o -name "*.amr" -o -name "*.ape" -o -name "*.ac3" -o -name "*.mp2" -o -name "*.wv" -o -name "*.m4b" -o -name "*.mka" -o -name "*.spx" -o -name "*.caf" -o -name "*.snd" -o -name "*.gsm" -o -name "*.tta" -o -name "*.voc" -o -name "*.w64" -o -name "*.s8" -o -name "*.u8" \) ! -exec grep -qx {} "$normalized_list_file" \; -print -quit)

        # if there are no more files to process, exit the loop
        if [[ -z "$src_file" ]]; then
            break
        fi

        # check if the file was skipped
        if grep -qx "$src_file" "$normalized_list_file"; then
            ((skipped_files++))
            echo -e "[cruix-music-archiver] Skipped: $src_file  🏃‍♂️ File Dodged the Process Like a Pro!  🏅 "
            continue
        fi

        # increment attempt count for the current file
        attempt_count["$src_file"]=$((attempt_count["$src_file"] + 1))

        # if the file has been attempted max_attempts times, move it to recycle bin
        if [[ ${attempt_count["$src_file"]} -gt $max_attempts ]]; then
            echo -e "[cruix-music-archiver] Moving $src_file to The Recycle Bin After $max_attempts Failed Attempts. 💾  🚮  Game Over, File! 💾  🚮"
            move_to_recycle_bin "$src_file"
            continue
        fi

        # process the file
        process_file "$src_file" "$log_file"
    done

    # final summary
    echo -e "[cruix-music-archiver] All Files Have Been Processed and Normalized Successfully! ✅  The Library is In Harmony! 🕊️ "
}

main