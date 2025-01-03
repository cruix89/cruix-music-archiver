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
                # split without stripping spaces from each replacement part
                old, new = line.split('‖')
                replacements.append((old, new))
                logging.debug(f"loaded replacement - old: '{old}', new: '{new}'")  # log each loaded replacement
    return replacements


def update_tag(file_path, tag_class, tag_name, replacements):
    try:
        logging.debug(f"Attempting to update tag '{tag_name}' in file: '{file_path}'")
        audiofile = ID3(file_path)  # load the audio file
        current_tag = audiofile.get(tag_name)  # get the current tag

        # check if the current tag exists and split it by '/'
        if current_tag:
            current_tag_text = current_tag.text[0]
            entries = current_tag_text.split('/')  # split the string by '/'
            logging.debug(f"Current tag entries: {entries}")

            # replace each entry according to the replacements list
            for i, entry in enumerate(entries):
                for old, new in replacements:
                    if entry == old:
                        entries[i] = new  # Replace the entry with the new value
                        logging.debug(f"replaced '{old}' with '{new}' in tag '{tag_name}' for '{file_path}'")

            # remove empty entries resulting from replacements
            entries = [entry.strip() for entry in entries if entry.strip()]

            # remove duplicates while preserving the order
            seen = set()
            unique_entries = []
            for entry in entries:
                if entry not in seen:
                    unique_entries.append(entry)
                    seen.add(entry)
            logging.debug(f"Unique entries after removing duplicates: {unique_entries}")

            # join entries back into a single string
            modified_tag_text = ' / '.join(unique_entries) if unique_entries else ""
            logging.debug(f"final formatted tag text: '{modified_tag_text}'")

            # update tag only if it was modified
            if modified_tag_text != current_tag_text:
                audiofile[tag_name] = tag_class(encoding=3, text=modified_tag_text)
                audiofile.save()
                logging.debug(f"updated '{tag_name}' tag in '{file_path}' to '{modified_tag_text}'")

    except FileNotFoundError as e:
        logging.error(f"error updating tag in '{file_path}': {e}")
    except Exception as e:
        if "no id3 header found" in str(e):
            logging.warning(f"no id3 header found in '{file_path}'. creating a new id3 header.")
            audiofile = ID3()  # create a new id3 instance
            modified_replacement_text = replacements[0][1].title()  # capitalize each word
            audiofile[tag_name] = tag_class(encoding=3, text=modified_replacement_text)
            audiofile.save(file_path)  # save the new file
            logging.debug(
                f"new id3 header created in '{file_path}' with '{tag_name}' set to '{modified_replacement_text}'")
        else:
            logging.error(f"error updating tag in '{file_path}': {e}")
    return None


def main():
    logging.basicConfig(filename=os.path.join(LOGS_DIR, 'artists_tag_fixer.log'),
                        level=logging.DEBUG)

    # absolute path to the replacements file
    replacements_path = os.path.join(LISTS_DIR, 'artists_tag_fixer.txt')
    replacements = load_replacements(replacements_path)

    logging.debug("starting tag formatting for artist tags in files...")
    print("[cruix-music-archiver] Formatting Artists Tags in Files... 🧑‍  Polishing the Audio Gems to Perfection! 🧑‍  ")

    for dirpath, _, filenames in os.walk(MUSIC_DIR):
        for file_name in filenames:
            if file_name.endswith(".mp3"):
                file_path = os.path.join(dirpath, file_name)

                # update artist tag only
                update_tag(file_path, mutagen.id3.TPE1, 'TPE1', replacements)  # update artist tag

    logging.debug("artist tags formatted successfully.")


if __name__ == "__main__":
    main()