import os
import shutil
import logging

# root directory to start the search
root_dir = os.path.abspath('/music')

# new destination directory
dest_dir = os.path.abspath('/config/recycle-bin')

# log directory
log_dir = os.path.abspath('/config/logs')
os.makedirs(log_dir, exist_ok=True)

# configure logging
log_file = os.path.join(log_dir, 'trash_collector.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("[cruix-music-archiver] Trash Collector Eliminating Stray Files... ♻️  Bringing Order to the Music Universe! 🌌", flush=True)

# supported audio formats
audio_formats = (
    '.mp3', '.flac', '.wav', '.aac', '.m4a', '.ogg', '.wma', '.alac',
    '.aiff', '.opus', '.dsd', '.amr', '.ape', '.ac3', '.mp2', '.wv',
    '.m4b', '.mka', '.spx', '.caf', '.snd', '.gsm', '.tta', '.voc',
    '.w64', '.s8', '.u8'
)

# excluded folders
excluded_folders = {'.stfolder', '.stversions', '.thumbnails'}

# walk through the root directory
total_files = 0
moved_files = 0
skipped_files = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    # filter out excluded folders
    dirnames[:] = [d for d in dirnames if d not in excluded_folders]

    # create a set of audio files found in the directory
    audio_files = {os.path.splitext(f)[0] for f in filenames if f.lower().endswith(audio_formats)}

    # for each file in the directory
    for filename in filenames:
        # define the full path for the file
        src_path = os.path.join(dirpath, filename)
        total_files += 1

        # check if there is a corresponding audio file
        if os.path.splitext(filename)[0] not in audio_files:
            # define the destination path here
            dest_path = os.path.join(dest_dir, os.path.relpath(dirpath, root_dir), filename)

            # try to move the file
            try:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.move(src_path, dest_path)
                moved_files += 1
                logging.info(f'file moved from {src_path} to {dest_path}')
            except Exception as e:
                logging.error(f'failed to move file from {src_path} to {dest_path}: {e}')
        else:
            skipped_files += 1
            logging.info(f'[cruix-music-archiver] The File {src_path} Was Skipped Because a Corresponding Audio File Was Found')

# log final summary
logging.info(f'[cruix-music-archiver] the operation was successfully completed. total files processed: {total_files}, recycled: {moved_files}, skipped: {skipped_files}')

# print final summary to terminal
print("[cruix-music-archiver] Files Recycled Successfully! ♻️  Clean and Green! 🌱")
print(f"[cruix-music-archiver] Total Files Processed: {total_files}, Recycled: {moved_files}, Skipped: {skipped_files}. 🎮  Efficiency Level: 100%! 🚀")