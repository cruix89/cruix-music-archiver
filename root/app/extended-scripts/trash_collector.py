import os
import shutil
import logging

# ROOT DIRECTORY TO START THE SEARCH
root_dir = os.path.abspath('/downloads')

# NEW DESTINATION DIRECTORY
dest_dir = os.path.abspath('/config/recycle-bin')

# LOG DIRECTORY
log_dir = os.path.abspath('/config/logs')
os.makedirs(log_dir, exist_ok=True)

# CONFIGURE LOGGING
log_file = os.path.join(log_dir, 'trash_collector.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("\nrecycling files without a corresponding audio file...")

# SUPPORTED AUDIO FORMATS
audio_formats = (
    '.mp3', '.flac', '.wav', '.aac', '.m4a', '.ogg', '.wma', '.alac',
    '.aiff', '.opus', '.dsd', '.amr', '.ape', '.ac3', '.mp2', '.wv',
    '.m4b', '.mka', '.spx', '.caf', '.snd', '.gsm', '.tta', '.voc',
    '.w64', '.s8', '.u8'
)

# EXCLUDED FOLDERS
excluded_folders = {'.stfolder', '.stversions', '.thumbnails'}

# WALK THROUGH THE ROOT DIRECTORY
total_files = 0
moved_files = 0
skipped_files = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    # Filter out excluded folders
    dirnames[:] = [d for d in dirnames if d not in excluded_folders]

    # Create a set of audio files found in the directory
    audio_files = {os.path.splitext(f)[0] for f in filenames if f.lower().endswith(audio_formats)}

    # FOR EACH FILE IN THE DIRECTORY
    for filename in filenames:
        # DEFINE THE FULL PATH FOR THE FILE
        src_path = os.path.join(dirpath, filename)
        total_files += 1

        # CHECK IF THERE IS A CORRESPONDING AUDIO FILE
        if os.path.splitext(filename)[0] not in audio_files:
            # DEFINE THE DESTINATION PATH HERE
            dest_path = os.path.join(dest_dir, os.path.relpath(dirpath, root_dir), filename)

            # TRY TO MOVE THE FILE
            try:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.move(src_path, dest_path)
                moved_files += 1
                logging.info(f'FILE MOVED FROM {src_path} TO {dest_path}\n')
            except Exception as e:
                logging.error(f'FAILED TO MOVE FILE FROM {src_path} TO {dest_path}: {e}\n')
        else:
            skipped_files += 1
            logging.info(f'THE FILE {src_path} WAS SKIPPED BECAUSE A CORRESPONDING AUDIO FILE WAS FOUND\n')

# LOG FINAL SUMMARY
logging.info(
    f'THE OPERATION WAS SUCCESSFULLY COMPLETED. TOTAL FILES PROCESSED: {total_files}, RECYCLED: {moved_files}, SKIPPED: {skipped_files}\n')

# PRINT FINAL SUMMARY TO TERMINAL
print(f"files recycled successfully.\nTotal files processed: {total_files}, Recycled: {moved_files}, Skipped: {skipped_files}")