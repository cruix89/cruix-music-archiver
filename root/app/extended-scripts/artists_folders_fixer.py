import os
import logging
import re  # Importação para uso de expressões regulares

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
        # Create a list of replacements, each as a tuple (old, new)
        return [line.strip().split('|') for line in f.readlines() if line.strip()]


def rename_direct_folders(music_directory, replacements):
    try:
        for folder_name in os.listdir(music_directory):
            folder_path = os.path.join(music_directory, folder_name)
            if os.path.isdir(folder_path):
                for old, new in replacements:
                    if old in folder_name:
                        # Use regex for precise substitution
                        pattern = re.escape(old)  # Ensure the pattern is treated literally
                        new_folder_name = re.sub(pattern, new, folder_name)
                        new_folder_path = os.path.join(music_directory, new_folder_name)
                        if os.path.exists(folder_path):
                            try:
                                # Temporary renaming if names only differ in case
                                if folder_path.lower() == new_folder_path.lower():
                                    temp_path = os.path.join(music_directory, new_folder_name + "_temp")
                                    os.rename(folder_path, temp_path)
                                    os.rename(temp_path, new_folder_path)
                                else:
                                    os.rename(folder_path, new_folder_path)
                                print(f"[cruix-music-archiver] renaming directory '{folder_name}' to '{new_folder_name}' ♻️")
                            except FileNotFoundError as e:
                                logging.error(f"error renaming directory '{folder_name}': {e}")
    except Exception as e:
        logging.error(f"error in renaming folders in '{music_directory}': {e}")


def main():
    logging.basicConfig(filename=os.path.join(LOGS_DIR, 'artists_folder_fixer.log'),
                        level=logging.DEBUG)

    # absolute path to the replacements file
    replacements_path = os.path.join(LISTS_DIR, 'artists_folders_fixer.txt')
    replacements = load_replacements(replacements_path)

    # Count the number of lines (replacements) in the file
    num_replacements = len(replacements)

    print(f"[cruix-music-archiver] fixing artists' folders... 🔧  time to tidy up and make everything look perfect! 🔧  ")
    logging.debug("fixing artists folders...")

    # Execute the entire renaming process the same number of times as the number of replacements
    for i in range(num_replacements):
        print(f"[cruix-music-archiver] executing renaming process {i + 1} of {num_replacements}... 🔧 ")
        logging.debug(f"executing renaming process {i + 1} of {num_replacements}...")

        # Apply all replacements each time
        rename_direct_folders(MUSIC_DIR, replacements)

    print("[cruix-music-archiver] artists' folders fixed successfully! ⚡  mission accomplished, folders upgraded! ⚡  ")
    logging.debug("artists folders fixed successfully.")


if __name__ == "__main__":
    main()