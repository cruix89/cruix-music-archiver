import os
import shutil
import subprocess

# CONFIGURE ABSOLUTE PATHS
SRC_DIR = '/downloads'
CACHE_DIR = '/config/cache'
LOG_DIR = '/config/logs'
LISTS_DIR = '/config'
NORMALIZED_LIST_FILE = os.path.join(LISTS_DIR, 'loudnorm_cache.txt')

# SUPPORTED AUDIO FORMATS
audio_formats = (
    '.mp3', '.flac', '.wav', '.aac', '.m4a', '.ogg', '.wma', '.alac',
    '.aiff', '.opus', '.dsd', '.amr', '.ape', '.ac3', '.mp2', '.wv',
    '.m4b', '.mka', '.spx', '.caf', '.snd', '.gsm', '.tta', '.voc',
    '.w64', '.s8', '.u8'
)

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("\nFFMPEG IS NOT INSTALLED OR NOT AVAILABLE IN THE PATH.")
        exit(1)

def load_normalized_list():
    """Load the list of already normalized files from the loudnorm_cache.txt."""
    if not os.path.exists(NORMALIZED_LIST_FILE):
        return set()  # Return an empty set if the file does not exist
    with open(NORMALIZED_LIST_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def save_to_normalized_list(file_path):
    """Append the normalized file path to loudnorm_cache.txt."""
    with open(NORMALIZED_LIST_FILE, 'a', encoding='utf-8') as f:
        f.write(file_path + '\n')

def get_cache_output_path(src_file):
    """Get the output path in the cache directory with the same directory structure."""
    relative_path = os.path.relpath(src_file, SRC_DIR)
    output_path = os.path.join(CACHE_DIR, os.path.splitext(relative_path)[0] + ".mp3")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    return output_path

def process_file(src_file, log_file):
    # DEFINE THE OUTPUT FILE IN THE CACHE DIRECTORY
    output_file_mp3 = get_cache_output_path(src_file)

    # FFMPEG COMMAND WITH FULL PATH AND OUTPUT FILE EXTENSION
    cmd = ["ffmpeg", "-y", "-i", src_file, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=summary", "-b:a", "320k",
           output_file_mp3]

    with open(log_file, 'a', encoding='utf-8') as f:
        try:
            subprocess.run(cmd, check=True, stdout=f, stderr=subprocess.STDOUT)
            f.write(f"\n")
        except subprocess.CalledProcessError as e:
            f.write(f"ERROR PROCESSING FILE: {str(e)}\n")
            return  # Exit early if there's an error

    # VERIFY THAT THE OUTPUT FILE EXISTS BEFORE PROCEEDING
    if os.path.exists(output_file_mp3):
        save_to_normalized_list(src_file)  # Save the file to the normalized list
    else:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"OUTPUT FILE NOT FOUND: {output_file_mp3}\n")

def move_files_and_cleanup():
    """Move files from cache to original location and remove source files."""
    for dirpath, dirnames, filenames in os.walk(CACHE_DIR):
        for filename in filenames:
            cache_file = os.path.join(dirpath, filename)
            # Determine the original file path in SRC_DIR
            relative_path = os.path.relpath(cache_file, CACHE_DIR)
            original_file_path = os.path.join(SRC_DIR, os.path.splitext(relative_path)[0] + ".mp3")

            # Remove the original source file first
            original_src_file = os.path.splitext(original_file_path)[0] + os.path.splitext(filename)[1]
            if os.path.exists(original_src_file):
                os.remove(original_src_file)  # Delete the original file before moving the new one

            # Move the cache file to the original location
            os.makedirs(os.path.dirname(original_file_path), exist_ok=True)
            shutil.move(cache_file, original_file_path)

def prepare_directories():
    # ENSURE LOG, CACHE AND LISTS DIRECTORIES EXIST
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(LISTS_DIR, exist_ok=True)
    return SRC_DIR, LOG_DIR, LISTS_DIR

def main():
    src_dir, log_dir, lists_dir = prepare_directories()
    log_file = os.path.join(log_dir, 'loudnorm.log')

    check_ffmpeg()

    # Load the list of already normalized files
    normalized_files = load_normalized_list()

    audio_files = []
    skipped_files = 0

    # COLLECT ALL AUDIO FILES BEFORE STARTING PROCESSING
    for dirpath, dirnames, filenames in os.walk(src_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in audio_formats):
                src_file = os.path.join(dirpath, filename)
                if src_file not in normalized_files:  # Check if the file is already normalized
                    audio_files.append(src_file)
                else:
                    skipped_files += 1  # Count skipped files

    # PROCESS AUDIO FILES ONE BY ONE
    total_files = len(audio_files)
    for idx, src_file in enumerate(audio_files, start=1):
        process_file(src_file, log_file)
        print(f"File {idx}/{total_files} processed: {src_file}")

    # MOVE FILES FROM CACHE TO ORIGINAL LOCATION AND CLEAN UP
    move_files_and_cleanup()

    # Print final summary
    print(f"\nSummary: {total_files} files processed, {skipped_files} files skipped (already normalized).")

if __name__ == "__main__":
    main()