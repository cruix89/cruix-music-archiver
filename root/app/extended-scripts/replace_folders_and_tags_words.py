import os
import logging
from mutagen.easyid3 import EasyID3
import re
import time

def setup_logging(log_file, logger_name):
    # configure the logger
    logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

def load_replacements(file_path):
    # load replacements from the specified file
    replacements = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if '|' in line:
                    old, new = line.strip().split('|')
                    replacements[old.lower()] = (old, new)
                else:
                    logging.warning(f'invalid line in replacements file: {line.strip()}\n')
    except FileNotFoundError:
        logging.error(f'replacements file not found: {file_path}\n')
    except Exception as e:
        logging.error(f'error loading replacements: {e}\n')
    logging.debug(f'replacements loaded: {replacements}\n')
    return replacements

def format_name(name, replacements):
    # format the name by replacing terms according to the replacements
    for old_lower, (old, new) in replacements.items():
        # use word boundaries to ensure whole words are replaced
        pattern = r'\b' + re.escape(old) + r'\b'
        name = re.sub(pattern, new, name, flags=re.IGNORECASE)
    logging.debug(f'formatted name: {name}\n')
    return name

def rename_directories_and_format_tags(directory, replacements, max_retries=99, pause=30):
    # rename directories and format tags in mp3 files
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            new_dir_name = format_name(dir_name, replacements)
            new_dir_path = os.path.join(root, new_dir_name)
            for attempt in range(max_retries):
                try:
                    os.rename(dir_path, new_dir_path)
                    logging.info(f'directory renamed: {dir_path} -> {new_dir_path}\n')
                    break
                except PermissionError as e:
                    logging.warning(f'error renaming {dir_path} -> {new_dir_path}: {e}.\nattempt {attempt + 1}/{max_retries}\n')
                    print(f"error renaming {dir_path} to {new_dir_path}: {e}\n")
                    print(f"attempt {attempt + 1}/{max_retries}. close the folder manually and wait {pause} seconds...\n")
                    time.sleep(pause)
                except Exception as e:
                    logging.error(f'error renaming {dir_path} -> {new_dir_path}: {e}\n')
                    break
            else:
                logging.error(f'failed to rename {dir_path} -> {new_dir_path} after {max_retries} attempts\n')
                print(f"failed to rename {dir_path} to {new_dir_path} after {max_retries} attempts.\ncheck permissions and try again.\n")

        for file_name in files:
            if file_name.endswith('.mp3'):
                file_path = os.path.join(root, file_name)
                try:
                    tags = EasyID3(file_path)
                    for tag in tags:
                        tags[tag] = format_name(tags[tag][0], replacements)
                    tags.save()
                    logging.info(f'tags formatted: {file_path}\n')
                except Exception as e:
                    logging.error(f'error formatting tags of file {file_path}: {e}\n')

def setup_directories():
    # absolute paths
    logs_dir = '/config/logs'
    lists_dir = '/app/lists'
    music_dir = '/downloads'

    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(lists_dir, exist_ok=True)

    return logs_dir, lists_dir, music_dir

def main():
    print("\nrunning directory and tag formatting...")

    logs_dir, lists_dir, music_dir = setup_directories()

    log_file_rename = os.path.join(logs_dir, 'replace_folders_and_tags_words_1.log')
    log_file_format = os.path.join(logs_dir, 'replace_folders_and_tags_words_2.log')
    logger_rename = setup_logging(log_file_rename, 'rename')
    logger_format = setup_logging(log_file_format, 'format')

    replacements = load_replacements(os.path.join(lists_dir, 'replace.txt'))
    if not replacements:
        logger_rename.warning("no replacements loaded. check the replacements file.\n")
        logger_format.warning("no replacements loaded. check the replacements file.\n")

    if os.path.exists(music_dir):
        rename_directories_and_format_tags(music_dir, replacements)
        print("directories and tags formatted.\n")
    else:
        logger_rename.error(f'music directory not found: {music_dir}\n')
        logger_format.error(f'music directory not found: {music_dir}\n')

    print("directory and tag formatting completed successfully.")

if __name__ == "__main__":
    main()