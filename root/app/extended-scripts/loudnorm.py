import os
import subprocess
from tqdm import tqdm

# CONFIGURE ABSOLUTE PATHS
SRC_DIR = '/downloads'
LOG_DIR = '/config/logs'

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
            return

    # REMOVE THE ORIGINAL FILE AND RENAME THE TEMP FILE TO THE ORIGINAL NAME
    try:
        os.remove(src_file)  # Delete the original file
        os.rename(temp_file_mp3, src_file)  # Rename the temp file to the original name
    except OSError as e:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"ERROR RENAMING FILE: {str(e)}\n")


def prepare_directories():
    # ENSURE LOG DIRECTORY EXISTS
    os.makedirs(LOG_DIR, exist_ok=True)
    return SRC_DIR, LOG_DIR


def main():
    src_dir, log_dir = prepare_directories()
    log_file = os.path.join(log_dir, 'loudnorm.log')

    check_ffmpeg()

    audio_files = []

    # COLLECT ALL AUDIO FILES BEFORE STARTING PROCESSING
    for dirpath, dirnames, filenames in os.walk(src_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in audio_formats):
                src_file = os.path.join(dirpath, filename)
                audio_files.append(src_file)

    # PROCESS AUDIO FILES ONE BY ONE
    with tqdm(total=len(audio_files), desc="NORMALIZING AUDIO") as pbar:
        for src_file in audio_files:
            process_file(src_file, log_file)
            pbar.update()


if __name__ == "__main__":
    main()