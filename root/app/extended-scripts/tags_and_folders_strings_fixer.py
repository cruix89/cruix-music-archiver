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

# configure detailed logging
logging.basicConfig(
    filename=os.path.join(LOGS_DIR, 'tags_and_folders_full_strings_fixer.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def load_replacements(replacements_path):
    logging.info(f"loading replacements from: {replacements_path}")
    try:
        absolute_path = os.path.abspath(replacements_path)
        with open(absolute_path, 'r', encoding='utf-8') as f:
            replacements = [line.strip().split('|') for line in f.readlines() if line.strip()]
            logging.info(f"loaded {len(replacements)} replacement pairs.")
            return replacements
    except FileNotFoundError:
        logging.error(f"replacements file not found: {replacements_path}")
        return []
    except Exception as e:
        logging.error(f"unexpected error while loading replacements: {e}")
        return []


def update_tag(file_path, tag_class, tag_name, replacements):
    logging.debug(f"starting to process tags in file: {file_path}")
    try:
        audiofile = ID3(file_path)  # load the audio file
        current_tag = audiofile.get(tag_name)  # get the current tag
        if current_tag:
            logging.debug(f"current tag '{tag_name}' value: {current_tag.text[0]}")
            for old, new in replacements:
                if current_tag.text[0] == old:  # exact match, case-sensitive
                    logging.info(f"replacing tag '{tag_name}' from '{old}' to '{new}' in file: {file_path}")
                    audiofile[tag_name] = tag_class(encoding=3, text=new)  # create a new tag instance
                    audiofile.save()  # save the changes
                    logging.info(f"successfully updated tag '{tag_name}' in file: {file_path}")
                    return
        else:
            logging.debug(f"tag '{tag_name}' not found in file: {file_path}")
    except FileNotFoundError:
        logging.error(f"file not found: {file_path}")
    except Exception as e:
        logging.error(f"unexpected error updating tag in file '{file_path}': {e}")
    logging.debug(f"finished processing tags in file: {file_path}")


def rename_files_and_folders(music_directory, replacements):
    logging.info(f"starting to rename files and folders in directory: {music_directory}")
    for dirpath, dirnames, filenames in os.walk(music_directory):
        for file_name in filenames:
            old_path = os.path.join(dirpath, file_name)
            for old, new in replacements:
                if file_name == old:  # exact match, case-sensitive
                    new_file_name = new
                    new_path = os.path.join(dirpath, new_file_name)
                    try:
                        os.rename(old_path, new_path)
                        logging.info(f"renamed file from '{old_path}' to '{new_path}'")
                    except FileNotFoundError:
                        logging.error(f"file not found: {old_path}")
                    except Exception as e:
                        logging.error(f"error renaming file '{old_path}': {e}")

        for folder_name in dirnames:
            old_path = os.path.join(dirpath, folder_name)
            for old, new in replacements:
                if folder_name == old:  # exact match, case-sensitive
                    new_folder_name = new
                    new_path = os.path.join(dirpath, new_folder_name)
                    try:
                        if old_path.lower() == new_path.lower():
                            temp_path = os.path.join(dirpath, new_folder_name + "_temp")
                            os.rename(old_path, temp_path)
                            os.rename(temp_path, new_path)
                        else:
                            os.rename(old_path, new_path)
                        logging.info(f"renamed directory from '{old_path}' to '{new_path}'")
                    except FileNotFoundError:
                        logging.error(f"directory not found: {old_path}")
                    except Exception as e:
                        logging.error(f"error renaming directory '{old_path}': {e}")
    logging.info(f"finished renaming files and folders in directory: {music_directory}")


def main():
    logging.info("starting the tags and folders fixer process.")

    replacements_path = os.path.join(LISTS_DIR, 'fixer.txt')
    replacements = load_replacements(replacements_path)

    if not replacements:
        logging.warning("no replacements loaded. process aborted.")
        print("[cruix-music-archiver] no replacements loaded. check the replacements file.")
        return

    logging.info("starting tag updates...")
    for dirpath, _, filenames in os.walk(MUSIC_DIR):
        for file_name in filenames:
            if file_name.endswith(".mp3"):
                file_path = os.path.join(dirpath, file_name)
                update_tag(file_path, mutagen.id3.TIT2, 'TIT2', replacements)
                update_tag(file_path, mutagen.id3.TALB, 'TALB', replacements)
                update_tag(file_path, mutagen.id3.TPE2, 'TPE2', replacements)

    logging.info("starting file and folder renaming...")
    rename_files_and_folders(MUSIC_DIR, replacements)

    logging.info("tags and folders fixer process completed successfully.")
    print("[cruix-music-archiver] tags, files, and folders formatted successfully. 🎉")


if __name__ == "__main__":
    main()