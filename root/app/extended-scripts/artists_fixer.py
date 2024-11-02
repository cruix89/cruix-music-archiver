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
    replacements = []
    with open(absolute_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                old, new = line.strip().split('|')
                replacements.append((old, new))
                logging.debug(f"Loaded replacement - old: '{old}', new: '{new}'")  # Log each loaded replacement
    return replacements


def update_tag(file_path, tag_class, tag_name, replacements):
    try:
        logging.debug(f"Attempting to update tag '{tag_name}' in file: '{file_path}'")
        audiofile = ID3(file_path)  # load the audio file
        current_tag = audiofile.get(tag_name)  # get the current tag

        # Check if the current tag exists and split it by '/'
        if current_tag:
            current_tag_text = current_tag.text[0]
            entries = current_tag_text.split('/')  # Split the string by '/'
            logging.debug(f"Current tag entries: {entries}")

            # Replace each entry according to the replacements list
            for i, entry in enumerate(entries):
                for old, new in replacements:
                    if entry == old:
                        entries[i] = new  # Replace the entry with the new value
                        logging.debug(f"Replaced '{old}' with '{new}' in tag '{tag_name}' for '{file_path}'")

            modified_tag_text = ' / '.join(entries)  # Join the modified entries
            logging.debug(f"Modified tag text: '{modified_tag_text}'")

            # Update tag only if it was modified
            if modified_tag_text != current_tag_text:
                audiofile[tag_name] = tag_class(encoding=3, text=modified_tag_text)
                audiofile.save()
                logging.debug(f"Updated '{tag_name}' tag in '{file_path}' to '{modified_tag_text}'")

    except FileNotFoundError as e:
        logging.error(f"Error updating tag in '{file_path}': {e}")
    except Exception as e:
        if "no ID3 header found" in str(e):
            logging.warning(f"No ID3 header found in '{file_path}'. Creating a new ID3 header.")
            audiofile = ID3()  # create a new ID3 instance
            modified_replacement_text = replacements[0][1].title()  # capitalize each word
            audiofile[tag_name] = tag_class(encoding=3, text=modified_replacement_text)
            audiofile.save(file_path)  # save the new file
            logging.debug(
                f"New ID3 header created in '{file_path}' with '{tag_name}' set to '{modified_replacement_text}'")
        else:
            logging.error(f"Error updating tag in '{file_path}': {e}")
    return None


def main():
    logging.basicConfig(filename=os.path.join(LOGS_DIR, 'artists_fixer.log'),
                        level=logging.DEBUG)

    # absolute path to the replacements file
    replacements_path = os.path.join(LISTS_DIR, 'artists.txt')
    replacements = load_replacements(replacements_path)

    logging.debug("Starting tag formatting for artist tags in files...")
    print("Formatting artist tags in files...")

    for dirpath, _, filenames in os.walk(MUSIC_DIR):
        for file_name in filenames:
            if file_name.endswith(".mp3"):
                file_path = os.path.join(dirpath, file_name)

                # update artist tag only
                update_tag(file_path, mutagen.id3.TPE1, 'TPE1', replacements)  # update artist tag

    logging.debug("Artist tags formatted successfully.")
    print("Artist tags formatted successfully.")


if __name__ == "__main__":
    main()