import os
import logging
from mutagen.id3 import ID3
import mutagen.id3

# define absolute paths for directories
LOGS_DIR = '/config/logs'
LISTS_DIR = '/app/lists'
MUSIC_DIR = '/music'

# create directories if they do not exist
for path in [LOGS_DIR, LISTS_DIR, MUSIC_DIR]:
    if not os.path.exists(path):
        os.makedirs(path)

def load_replacements(replacements_path):
    absolute_path = os.path.abspath(replacements_path)
    with open(absolute_path, 'r', encoding='utf-8') as f:
        return [line.strip().split('|') for line in f.readlines() if line.strip()]

def update_tag(file_path, tag_class, tag_name, replacements):
    try:
        audiofile = ID3(file_path)  # load the audio file
        current_tag = audiofile.get(tag_name)  # get the current tag
        if current_tag:
            for old, new in replacements:
                if current_tag.text[0] == old:
                    logging.debug(f"replacing tag '{tag_name}' from '{old}' to '{new}' in file: {file_path}\n")
                    audiofile[tag_name] = tag_class(encoding=3, text=new)  # create a new tag instance
                    audiofile.save()  # save the changes
                    return audiofile.get(tag_name)
    except FileNotFoundError as e:
        logging.error(f"error updating tag in '{file_path}': {e}\n")
    except Exception as e:
        if "no ID3 header found" in str(e):
            logging.warning(f"no ID3 header found in '{file_path}'. creating a new ID3 header.\n")
            audiofile = ID3()  # create a new ID3 instance
            audiofile[tag_name] = tag_class(encoding=3, text=replacements[0][1])  # set the new tag
            audiofile.save(file_path)  # save the new file
        else:
            logging.error(f"Error updating tag in '{file_path}': {e}\n")
    return None

def rename_files_and_folders(music_directory, replacements):
    for dirpath, dirnames, filenames in os.walk(music_directory):
        for file_name in filenames:
            for old, new in replacements:
                if old in file_name:
                    new_file_name = file_name.replace(old, new)
                    old_path = os.path.join(dirpath, file_name)
                    new_path = os.path.join(dirpath, new_file_name)
                    if os.path.exists(old_path):
                        try:
                            os.rename(old_path, new_path)
                            logging.debug(f"renaming file '{file_name}' to '{new_file_name}'\n")
                        except FileNotFoundError as e:
                            logging.error(f"error renaming file '{file_name}': {e}\n")

        for folder_name in dirnames:
            for old, new in replacements:
                if old in folder_name:
                    new_folder_name = folder_name.replace(old, new)
                    old_path = os.path.join(dirpath, folder_name)
                    new_path = os.path.join(dirpath, new_folder_name)
                    if os.path.exists(old_path):
                        try:
                            # temporary renaming if names only differ in case
                            if old_path.lower() == new_path.lower():
                                temp_path = os.path.join(dirpath, new_folder_name + "_temp")
                                os.rename(old_path, temp_path)
                                os.rename(temp_path, new_path)
                            else:
                                os.rename(old_path, new_path)
                            logging.debug(f"renaming directory '{folder_name}' to '{new_folder_name}'\n")
                        except FileNotFoundError as e:
                            logging.error(f"error renaming directory '{folder_name}': {e}\n")

def main():
    logging.basicConfig(filename=os.path.join(LOGS_DIR, 'tags_and_folders_full_strings_fixer.log'),
                        level=logging.DEBUG)

    # absolute path to the replacements file
    replacements_path = os.path.join(LISTS_DIR, 'fixer.txt')
    replacements = load_replacements(replacements_path)

    print("[cruix-music-archiver] formatting tags, files, and folders...")
    logging.debug("formatting tags, files, and folders...")

    for dirpath, _, filenames in os.walk(MUSIC_DIR):
        for file_name in filenames:
            if file_name.endswith(".mp3"):
                file_path = os.path.join(dirpath, file_name)

                # update title, album, and album artist tags
                update_tag(file_path, mutagen.id3.TIT2, 'TIT2', replacements)  # update title tag
                update_tag(file_path, mutagen.id3.TALB, 'TALB', replacements)  # update album tag
                update_tag(file_path, mutagen.id3.TPE2, 'TPE2', replacements)  # update album artist tag

    # rename files and folders
    rename_files_and_folders(MUSIC_DIR, replacements)

    print("[cruix-music-archiver] tags, files, and folders formatted successfully.")
    logging.debug("tags, files, and folders formatted successfully.")

if __name__ == "__main__":
    main()