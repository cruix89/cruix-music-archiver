import os
import logging
import sys


def setup_logging( log_file ):
    log_dir = os.path.dirname(log_file)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(message)s')

# FIXED PRINT IN TERMINAL
print("\nremoving invalid characters...")

def load_invalid_characters( file_path ):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            invalid_chars = [line.encode().decode('unicode-escape').strip() for line in f if line.strip()]
        logging.info(f"INVALID CHARACTERS LOADED FROM LIST: {invalid_chars}\n")
        return invalid_chars
    except Exception as e:
        logging.error(f"ERROR LOADING INVALID CHARACTERS: {e}\n")
        return []


def sanitize_name( name, invalid_chars ):
    original_name = name
    # REPLACE SPACES WITH "_"
    name = name.replace(' ', '_')
    logging.debug(f"REPLACING SPACES WITH '_' IN '{original_name}'\n")
    # REPLACE "-" WITH "_"
    name = name.replace('-', '_')
    logging.debug(f"REPLACING '-' WITH '_' IN '{original_name}'\n")
    # REPLACE "," WITH "_"
    name = name.replace(',', '_')
    logging.debug(f"REPLACING ',' WITH '_' IN '{original_name}'\n")
    for char in invalid_chars:
        if char in name:
            logging.debug(f"REPLACING '{char}' IN '{original_name}'\n")
        name = name.replace(char, "_")
    logging.info(f"STANDARDIZING '{original_name}' TO '{name}'\n")
    return name


def rename_item( path, old_name, new_name ):
    try:
        os.rename(os.path.join(path, old_name), os.path.join(path, new_name))
        logging.info(f"RENAMED {old_name} TO {new_name}\n")
    except Exception as e:
        logging.error(f"ERROR RENAMING {old_name}: {e}\n")


def rename_files_and_dirs( path, invalid_chars ):
    logging.info("REMOVING INVALID CHARACTERS...\n")
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
        logging.info("NO INVALID CHARACTERS FOUND.\n")
    logging.info("INVALID CHARACTERS REMOVED.\n")


def main( download_path, lists_path ):
    invalid_chars_file = os.path.join(lists_path, 'invalid_characters.txt')

    if not os.path.exists(download_path):
        logging.error(f"DOWNLOAD DIRECTORY DOES NOT EXIST: {download_path}\n")
        sys.exit(1)

    if not os.path.exists(lists_path):
        logging.error(f"LISTS DIRECTORY DOES NOT EXIST: {lists_path}\n")
        sys.exit(1)

    invalid_chars = load_invalid_characters(invalid_chars_file)
    rename_files_and_dirs(download_path, invalid_chars)

# FIXED PRINT IN TERMINAL
print("invalid characters removed successfully...\n")

if __name__ == "__main__":

    global_music_path = "/music"
    global_lists_path = "/app/lists"
    log_path_absolute = "/config/logs/music_invalid_characters_remover.log"

    setup_logging(log_path_absolute)
    main(global_music_path, global_lists_path)