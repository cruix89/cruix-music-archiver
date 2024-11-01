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

        # process each substring separated by '/' in the tag
        if current_tag:
            modified_segments = []
            for segment in current_tag.text[0].split('/'):
                segment = segment.strip()

                # apply replacements for each segment
                for old, new in replacements:
                    if segment == old:
                        logging.debug(f"replacing segment '{segment}' with '{new}' in file: {file_path}\n")
                        segment = new
                        break
                modified_segments.append(segment)

            # join modified segments with '/'
            modified_tag_text = '/'.join(modified_segments)
            audiofile[tag_name] = tag_class(encoding=3, text=modified_tag_text)
            audiofile.save()

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


def main():
    logging.basicConfig(filename=os.path.join(LOGS_DIR, 'artists_fixer.log'),
                        level=logging.DEBUG)

    # absolute path to the replacements file
    replacements_path = os.path.join(LISTS_DIR, 'artists.txt')
    replacements = load_replacements(replacements_path)

    print("formatting artist tags in files...")
    logging.debug("formatting artist tags in files...")

    for dirpath, _, filenames in os.walk(MUSIC_DIR):
        for file_name in filenames:
            if file_name.endswith(".mp3"):
                file_path = os.path.join(dirpath, file_name)

                # update artist tag only
                update_tag(file_path, mutagen.id3.TPE1, 'TPE1', replacements)  # update artist tag

    print("artist tags formatted successfully.\n")
    logging.debug("artist tags formatted successfully.")


if __name__ == "__main__":
    main()