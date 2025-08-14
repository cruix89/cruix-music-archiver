#!/usr/bin/with-contenv bash

# environment variable configurations
normalized_log_dir="${normalized_log_dir:-/config/logs}"
normalized_list_file="${normalized_list_file:-/config/loudnorm_cache.txt}"
cache_dir="/config/cache"
recycle_bin_dir="/config/recycle-bin"
failed_log_file="/config/loudnorm_failed_files_cache.txt"  # log file for failed files

# function to normalize strings: lowercase + remove accents (NEW)
normalize_string() {
    # iconv converte para ASCII removendo acentos; tr converte para minúsculas
    echo "$1" | iconv -f UTF-8 -t ASCII//TRANSLIT | tr '[:upper:]' '[:lower:]'
}

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
    # normalize existing list to lowercase and without accents (NEW)
    mapfile -t raw_files < "$normalized_list_file"
    > "$normalized_list_file"
    for f in "${raw_files[@]}"; do
        normalize_string "$f" >> "$normalized_list_file"
    done
    mapfile -t normalized_files < "$normalized_list_file"
    echo -e "[cruix-music-archiver] Number of Normalized Files In Cache: ${#normalized_files[@]}  🗄️  Cache is Grooving! 🕺"
}

# function to save to the normalized list (always lowercase to avoid case sensitivity issues)
save_to_normalized_list() {
    normalize_string "$1" >> "$normalized_list_file"  # now also removing accents (NEW)
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
        src_file=$(find "/music" -type f \( -iname "*.mp3" -o -iname "*.flac" -o -iname "*.wav" -o -iname "*.aac" -o -iname "*.m4a" -o -iname "*.ogg" -o -iname "*.wma" -o -iname "*.alac" -o -iname "*.aiff" -o -iname "*.opus" -o -iname "*.dsd" -o -iname "*.amr" -o -iname "*.ape" -o -iname "*.ac3" -o -iname "*.mp2" -o -iname "*.wv" -o -iname "*.m4b" -o -iname "*.mka" -o -iname "*.spx" -o -iname "*.caf" -o -iname "*.snd" -o -iname "*.gsm" -o -iname "*.tta" -o -iname "*.voc" -o -iname "*.w64" -o -iname "*.s8" -o -iname "*.u8" \) ! -exec grep -iq {} "$normalized_list_file" \; -print -quit)

        # if there are no more files to process, exit the loop
        if [[ -z "$src_file" ]]; then
            break
        fi

        # normalize the path to lowercase and remove accents for comparison (NEW)
        normalized_path=$(normalize_string "$src_file")

        # check if the file was skipped
        if grep -qx "$normalized_path" "$normalized_list_file"; then
            ((skipped_files++))
            echo -e "[cruix-music-archiver] Skipped: $src_file  🏃‍♂️ File Dodged the Process Like a Pro!  🏅 "
            continue
        fi

        # increment attempt count for the current file
        attempt_count["$normalized_path"]=$((attempt_count["$normalized_path"] + 1))

        # if the file has been attempted max_attempts times, move it to recycle bin
        if [[ ${attempt_count["$normalized_path"]} -gt $max_attempts ]]; then
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