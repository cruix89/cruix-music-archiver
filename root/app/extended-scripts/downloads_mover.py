import os
import shutil
import re

print("[cruix-music-archiver] initiating folder migration... ⚡  moving data from /downloads to the mystical /music library... 📚", flush=True)

def normalize_folder_name(folder_name):
    """normalizes the folder name, removing spaces, underscores and numeric suffixes, converting it to lowercase."""
    normalized_name = folder_name.replace('__', '_').replace('_', ' ').lower()  # replace underscores with spaces
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
            print(f'[cruix-music-archiver] moved: {src_path} to {dest_path}  💻', flush=True)

        # remove the original folder
        try:
            os.rmdir(folder_path)
            print(f"[cruix-music-archiver] removing empty folder {folder_path}... 🧹  clearing out the ghost towns! 🧹  ")
        except Exception as e:
            print(f"[cruix-music-archiver] error removing folder {folder_path}: {e}... ⚠️  the folder resisted deletion — perhaps it holds ancient secrets?")

print('[cruix-music-archiver] move completed successfully... 🏆  the files have been safely transferred through the space-time continuum! 🌌')