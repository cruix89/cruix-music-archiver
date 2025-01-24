import os
import eyed3
import requests
import logging

# print in terminal
print("[cruix-music-archiver] Downloading Music Database... 🚀  Initiating Data Stream From the Audio Archives! 🚀  ", flush=True)

def setup_directories():
    # absolute directories
    base_dir = '/music'
    db_dir = '/config/dz-db'
    log_dir = '/config/logs'

    # create directories if they do not exist
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(db_dir, exist_ok=True)

    return base_dir, db_dir, log_dir

def count_mp3_files(base_dir):
    total_files = 0
    for _, _, files in os.walk(base_dir):
        total_files += sum(1 for file in files if file.endswith('.mp3'))
    return total_files

def remove_empty_files(db_dir):
    # iterate over all .txt files in db_dir
    for dirpath, _, filenames in os.walk(db_dir):
        for filename in filenames:
            if filename.endswith('.txt'):
                txt_path = os.path.join(dirpath, filename)
                try:
                    # read the content of the file
                    with open(txt_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # if the content matches the specified value, delete the file
                    if content.strip() == "{'data': [], 'total': 0}":
                        os.remove(txt_path)
                        logging.info(f"file {txt_path} had empty data and was deleted.")
                except Exception as e:
                    logging.error(f"error while processing file {txt_path}: {e}")

def main():
    # logging configuration
    base_dir, db_dir, log_dir = setup_directories()
    logging.basicConfig(filename=os.path.join(log_dir, 'dz_db_downloader.log'), level=logging.INFO)

    # file count to track progress
    total_files = count_mp3_files(base_dir)
    logging.info(f"starting to process {total_files} files.")

    # for each subdirectory and file in the base directory
    for dirpath, dirnames, filenames in os.walk(base_dir):
        for filename in filenames:

            # if the file is a mp3
            if filename.endswith('.mp3'):

                # full file path
                full_path = os.path.join(dirpath, filename)

                # corresponding text file path in db directory
                relative_path = os.path.relpath(full_path, base_dir)
                txt_path = os.path.join(db_dir, os.path.splitext(relative_path)[0] + '.txt')

                # check if the text file already exists
                if os.path.exists(txt_path):
                    logging.info(f"file {filename} already processed. skipping.")
                    continue

                # load mp3 tags
                audiofile = eyed3.load(full_path)
                if audiofile is None or audiofile.tag is None:
                    logging.warning(f"file {filename} does not contain valid id3 tags.")
                    continue

                album_artist = audiofile.tag.album_artist  # busca o artista do álbum
                album_name = audiofile.tag.album
                track_name = audiofile.tag.title

                # fallback caso album_artist não esteja preenchido
                if not album_artist:
                    album_artist = audiofile.tag.artist

                # prepare API query string
                query_string = f'artist:"{album_artist}" album:"{album_name}" track:"{track_name}"'
                logging.info(f"api query string for file {filename}: {query_string}")

                # make request to dz api with the new order: album artist -> album -> track
                try:
                    response = requests.get(
                        f'https://api.deezer.com/search?q={query_string}&limit=1'
                    )
                    response.raise_for_status()  # raises exception for http error status codes
                    data = response.json()

                    # log success
                    logging.info(f"api responded successfully for file {filename}. data received.")
                except requests.exceptions.RequestException as e:
                    logging.error(f"http request error for file {filename}: {e}")
                    continue  # skip to next file
                except requests.exceptions.JSONDecodeError as e:
                    logging.error(f"json decoding error for file {filename}: {e}")
                    continue  # skip to next file

                # create subdirectories if necessary
                os.makedirs(os.path.dirname(txt_path), exist_ok=True)

                # write data to text file
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(str(data))

                # log action
                logging.info(f"file {filename} processed. data saved to {txt_path}.")

    # process completed
    logging.info("processing completed.")

    # check and remove empty files
    remove_empty_files(db_dir)

if __name__ == "__main__":
    main()