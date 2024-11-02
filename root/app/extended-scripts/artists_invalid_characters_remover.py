import os
import logging
import sys
import eyed3


def setup_logging(log_file):
    log_dir = os.path.dirname(log_file)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(message)s')


# fixed print in terminal
print("removing invalid characters from artist tags in MP3 files...")

def load_invalid_characters(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            invalid_chars = [line.encode().decode('unicode-escape').strip() for line in f if line.strip()]
        logging.info(f"invalid characters loaded from list: {invalid_chars}\n")
        return invalid_chars
    except Exception as e:
        logging.error(f"error loading invalid characters: {e}\n")
        return []


def sanitize_artist_tag(artist_name, invalid_chars):
    original_name = artist_name
    # replace spaces with "_"
    artist_name = artist_name.replace(',', '/')
    logging.debug(f"replacing ',' with '/' in artist tag '{original_name}'\n")
    # replace "-" with "_"
    artist_name = artist_name.replace(',', '/')
    logging.debug(f"replacing ',' with '/' in artist tag '{original_name}'\n")
    # replace "," with "_"
    artist_name = artist_name.replace(',', '/')
    logging.debug(f"replacing ',' with '/' in artist tag '{original_name}'\n")
    for char in invalid_chars:
        if char in artist_name:
            logging.debug(f"replacing '{char}' in artist tag '{original_name}'\n")
        artist_name = artist_name.replace(char, "_")
    logging.info(f"standardizing artist tag '{original_name}' TO '{artist_name}'\n")
    return artist_name


def update_mp3_tag(path, invalid_chars):
    if path.endswith('.mp3'):
        try:
            audiofile = eyed3.load(path)
            if audiofile is None:
                logging.warning(f"unable to load MP3 file: {path}\n")
                return

            artist_tag = audiofile.tag.artist
            if artist_tag:
                new_artist_tag = sanitize_artist_tag(artist_tag, invalid_chars)
                if new_artist_tag != artist_tag:
                    audiofile.tag.artist = new_artist_tag
                    audiofile.tag.save()
                    logging.info(f"updated artist tag in {path}\n")
                else:
                    logging.info(f"no changes needed for artist tag in {path}\n")
            else:
                logging.info(f"no artist tag found in {path}\n")
        except Exception as e:
            logging.error(f"error updating artist tag in {path}: {e}\n")


def process_mp3_tags(path, invalid_chars):
    logging.info("processing MP3 artist tags...\n")
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            update_mp3_tag(file_path, invalid_chars)
    logging.info("artist tags processed.\n")


def main(download_path, lists_path):
    invalid_chars_file = os.path.join(lists_path, 'artists_invalid_characters.txt')

    if not os.path.exists(download_path):
        logging.error(f"download directory does not exist: {download_path}\n")
        sys.exit(1)

    if not os.path.exists(lists_path):
        logging.error(f"lists directory does not exist: {lists_path}\n")
        sys.exit(1)

    invalid_chars = load_invalid_characters(invalid_chars_file)
    process_mp3_tags(download_path, invalid_chars)


# fixed print in terminal
print("artist tags updated successfully...\n")

if __name__ == "__main__":

    global_music_path = "/music"
    global_lists_path = "/app/lists"
    log_path_absolute = "/config/logs/artists_invalid_characters_remover.log"

    setup_logging(log_path_absolute)
    main(global_music_path, global_lists_path)