import os
import subprocess

# CONFIGURE ABSOLUTE PATHS
SRC_DIR = '/downloads'
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


def process_file(src_file, log_file):
    # DEFINE THE TEMPORARY OUTPUT FILE WITH THE NAME temp.mp3
    temp_file_mp3 = os.path.splitext(src_file)[0] + "_temp.mp3"

    # FFMPEG COMMAND WITH FULL PATH AND OUTPUT FILE EXTENSION
    cmd = ["ffmpeg", "-y", "-i", src_file, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=summary", "-b:a", "320k",
           temp_file_mp3]

    with open(log_file, 'a', encoding='utf-8') as f:
        try:
            subprocess.run(cmd, check=True, stdout=f, stderr=subprocess.STDOUT)
            f.write(f"\n")
        except subprocess.CalledProcessError as e:
            f.write(f"ERROR PROCESSING FILE: {str(e)}\n")
            return  # Exit early if there's an error

    # VERIFY THAT THE TEMPORARY FILE EXISTS BEFORE PROCEEDING
    if os.path.exists(temp_file_mp3):
        try:
            os.remove(src_file)  # Delete the original file
            os.rename(temp_file_mp3, src_file)  # Rename the temp file to the original name
            save_to_normalized_list(src_file)  # Save the file to the normalized list
        except OSError as e:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"ERROR RENAMING FILE: {str(e)}\n")
    else:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"TEMP FILE NOT FOUND: {temp_file_mp3}\n")


def prepare_directories():
    # ENSURE LOG AND LISTS DIRECTORIES EXIST
    os.makedirs(LOG_DIR, exist_ok=True)
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

    # Print final summary
    print(f"\nSummary: {total_files} files normalized, {skipped_files} files skipped (already normalized).")


if __name__ == "__main__":
    main()