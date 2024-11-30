import os
import shutil
import re

print("[cruix-music-archiver] Initiating Folder Migration... 🚚  Moving Data From /downloads to the Mystical /music Library... 📚", flush=True)

def normalize_folder_name(folder_name):
    """normalizes the folder name, removing spaces and numeric suffixes, converting it to lowercase."""
    normalized_name = folder_name.lower()  # convert to lowercase
    normalized_name = re.sub(r'\s\d+$', '', normalized_name)  # remove numeric suffixes at the end
    return normalized_name

# set the download directory and cache directory
downloads_dir = '/downloads'
music_dir = '/music'

# create a dictionary to store normalized folders found
folders = {}

# cycle through folders in the downloads directory
for folder in os.listdir(downloads_dir):
    folder_path = os.path.join(downloads_dir, folder)

    # check if it is a folder
    if os.path.isdir(folder_path):
        # normalize folder name for comparison
        normalized_folder = normalize_folder_name(folder)

        # if the normalized folder already exists, move the files to the existing folder
        if normalized_folder in folders:
            target_folder = folders[normalized_folder]
        else:
            # if the normalized folder does not exist, create a new directory in the cache folder
            normalized_folder_path = os.path.join(music_dir, normalized_folder)
            os.makedirs(normalized_folder_path, exist_ok=True)
            folders[normalized_folder] = normalized_folder_path
            target_folder = normalized_folder_path

        # move files from original folder to cache folder
        for item in os.listdir(folder_path):
            src_path = os.path.join(folder_path, item)
            dest_path = os.path.join(target_folder, item)

            # if the item already exists in the destination folder, adjust the name to avoid conflicts
            count = 1
            base_name, ext = os.path.splitext(item)
            while os.path.exists(dest_path):
                dest_path = os.path.join(target_folder, f"{base_name}_copy_{count}{ext}")
                count += 1

            # move the file or directory
            shutil.move(src_path, dest_path)

            # print the path of the moved file
            print(f'[cruix-music-archiver] Moved: {src_path} To {dest_path}  💻', flush=True)

        # remove the original folder
        try:
            os.rmdir(folder_path)
            print(f"[cruix-music-archiver] Removing Empty Folder {folder_path}... 🧹  Clearing Out the Ghost Towns! 🧹  ", flush=True)
        except Exception as e:
            print(f"[cruix-music-archiver] Error Removing Folder {folder_path}: {e}... ⚠️  The Folder Resisted Deletion — Perhaps It Holds Ancient Secrets? ⚠️ ", flush=True)

print('[cruix-music-archiver] Move Completed Successfully... 🏆  The Files Have Been Safely Transferred Through the Space-Time Continuum! 🌌')