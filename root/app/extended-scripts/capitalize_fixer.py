import os
import logging
from mutagen.easyid3 import EasyID3

def configure_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def rename_to_lowercase(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            new_dir_name = dir_name.lower()
            new_dir_path = os.path.join(root, new_dir_name)
            if dir_path != new_dir_path:
                os.rename(dir_path, new_dir_path)
                logging.info(f'directory renamed: {dir_path} -> {new_dir_path}\n')

        for file_name in files:
            file_path = os.path.join(root, file_name)
            new_file_name = file_name.lower()
            new_file_path = os.path.join(root, new_file_name)
            if file_path != new_file_path:
                os.rename(file_path, new_file_path)
                logging.info(f'file renamed: {file_path} -> {new_file_path}\n')

def format_first_letter(name):
    if not name:
        return name

    # find the first alphabetical character and capitalize it
    new_string = []
    first_letter_found = False
    for char in name:
        if not first_letter_found and char.isalpha():
            new_string.append(char.upper())
            first_letter_found = True
        else:
            new_string.append(char)
    return ''.join(new_string)

def format_mp3_tags(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.mp3'):
                file_path = os.path.join(root, file_name)
                try:
                    tags = EasyID3(file_path)
                    tags_modified = False
                    for tag in tags:
                        original_tag = tags[tag][0]
                        formatted_tag = format_first_letter(original_tag)
                        if original_tag != formatted_tag:
                            tags[tag] = formatted_tag
                            tags_modified = True
                    if tags_modified:
                        tags.save()
                        logging.info(f'tags formatted: {file_path}\n')
                except Exception as e:
                    logging.error(f'error formatting tags for file {file_path}: {e}\n')

def main():
    print("\nrunning directory and tag formatting...")

    # replace with absolute paths
    music_directory = '/music'
    logs_directory = '/config/logs'

    log_file_rename = os.path.join(logs_directory, 'capitalize_fixer.log')
    configure_logging(log_file_rename)

    if os.path.exists(music_directory):
        rename_to_lowercase(music_directory)
        format_mp3_tags(music_directory)
        print("directories and tags formatted.")
    else:
        logging.error(f'music directory not found: {music_directory}\n')

    print("directory and tag formatting successfully completed.")

if __name__ == "__main__":
    main()