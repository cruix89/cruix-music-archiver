import os
import logging
import sys


def setup_logging( log_file ):
    log_dir = os.path.dirname(log_file)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(message)s')


def load_invalid_characters( file_path ):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            invalid_chars = [line.encode().decode('unicode-escape').strip() for line in f if line.strip()]
        logging.info(f"invalid characters loaded from list: {invalid_chars}")
        return invalid_chars
    except Exception as e:
        logging.error(f"error loading invalid characters: {e}")
        return []


def sanitize_name( name, invalid_chars ):
    original_name = name
    # replace spaces with "_"
    name = name.replace(' ', '_')
    logging.debug(f"replacing spaces with '_' in '{original_name}'")
    # replace "-" with "_"
    name = name.replace('-', '_')
    logging.debug(f"replacing '-' with '_' in '{original_name}'")
    # replace "," with "_"
    name = name.replace(',', '_')
    logging.debug(f"replacing ',' with '_' in '{original_name}'")
    for char in invalid_chars:
        if char in name:
            logging.debug(f"replacing '{char}' in '{original_name}'")
        name = name.replace(char, "_")
    logging.info(f"standardizing '{original_name}' TO '{name}'")
    return name


def rename_item( path, old_name, new_name ):
    try:
        os.rename(os.path.join(path, old_name), os.path.join(path, new_name))
        logging.info(f"renamed {old_name} to {new_name}")
    except Exception as e:
        logging.error(f"error renaming {old_name}: {e}")


def rename_files_and_dirs( path, invalid_chars ):
    logging.info("removing invalid characters...")
    chars_removed = False
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        for filename in filenames:
            new_filename = sanitize_name(filename, invalid_chars)
            if new_filename != filename:
                rename_item(dirpath, filename, new_filename)
                chars_removed = True
        for dirname in dirnames:
            new_dirname = sanitize_name(dirname, invalid_chars)
            if new_dirname != dirname:
                new_path = os.path.join(dirpath, new_dirname)
                i = 1
                while os.path.exists(new_path):
                    new_path = os.path.join(dirpath, f"{new_dirname}_{i}")
                    i += 1
                rename_item(dirpath, dirname, new_path)
                chars_removed = True

    if not chars_removed:
        logging.info("no invalid characters found.")
    logging.info("invalid characters removed.")


def main( download_path, lists_path ):
    invalid_chars_file = os.path.join(lists_path, 'invalid_characters.txt')

    if not os.path.exists(download_path):
        logging.error(f"download directory does not exist: {download_path}")
        sys.exit(1)

    if not os.path.exists(lists_path):
        logging.error(f"lists directory does not exist: {lists_path}")
        sys.exit(1)

    invalid_chars = load_invalid_characters(invalid_chars_file)
    rename_files_and_dirs(download_path, invalid_chars)

# fixed print in terminal
print("[cruix-music-archiver] Invalid Characters Deleted Like a Boss... ✂️  Mission Successful! 😎 ")

if __name__ == "__main__":

    global_music_path = "/music"
    global_lists_path = "/app/lists"
    log_path_absolute = "/config/logs/music_invalid_characters_remover.log"

    setup_logging(log_path_absolute)
    main(global_music_path, global_lists_path)