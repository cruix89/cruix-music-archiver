import os
import re
import requests
import logging
from PIL import Image
from io import BytesIO


def setup_directories():
    # define absolute paths for directories
    music_dir = "/music"
    dz_db_dir = "/config/dz-db"
    log_dir = "/config/logs"

    # ensure that directories exist
    os.makedirs(music_dir, exist_ok=True)
    os.makedirs(dz_db_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    return music_dir, dz_db_dir, log_dir


def main():
    print("[cruix-music-archiver] Setting Up Plex Artist Image...  📺  Preparing the Artist’s Image For Ultimate Streaming Power! 📡 ")

    # logging setup
    music_dir, dz_db_dir, log_dir = setup_directories()
    logging.basicConfig(filename=os.path.join(log_dir, 'plex_artist_downloader.log'), level=logging.DEBUG)

    logging.debug(f"music_dir: {music_dir}")
    logging.debug(f"dz_db_dir: {dz_db_dir}")
    logging.debug(f"log_dir: {log_dir}")

    if not os.path.exists(music_dir):
        logging.error(f"the music directory '{music_dir}' does not exist.")
        return

    for folder in os.listdir(music_dir):
        search_dir = os.path.join(dz_db_dir, folder)
        logging.debug(f"searching in directory: {search_dir}")

        if os.path.exists(search_dir):
            url_counts = {}  # dictionary to store URLs and their counts

            for root, dirs, files in os.walk(search_dir):
                logging.debug(f"checking files in: {root}")

                for file in files:
                    if file.endswith(".txt"):
                        file_path = os.path.join(root, file)
                        logging.debug(f"reading file: {file_path}")

                        with open(file_path, 'r') as f:
                            content = f.read()
                            match = re.search(r"'picture_xl':\s*'([^']+)'", content)
                            if match:
                                img_url = match.group(1)
                                logging.debug(f"image url found: {img_url}")
                                url_counts[img_url] = url_counts.get(img_url, 0) + 1

            # after reading all .txt files, check if any results were obtained
            if url_counts:
                # select the URL that repeats the most times
                most_common_url = max(url_counts, key=url_counts.get)
                logging.debug(f"Most common image url: {most_common_url} with count: {url_counts[most_common_url]}")

                try:
                    response = requests.get(most_common_url, timeout=10)
                    response.raise_for_status()
                    img = Image.open(BytesIO(response.content))
                    img = img.resize((1280, 1280))
                    img.save(os.path.join(music_dir, folder, "cover.jpg"))
                    logging.info(f'artist image downloaded and saved for {folder}')
                except requests.exceptions.RequestException as e:
                    logging.error(f'error downloading image from {most_common_url} for {folder}: {str(e)}')
                except Exception as e:
                    logging.error(f'error processing image for {folder}: {str(e)}')
            else:
                logging.debug(f"No valid image url found in {search_dir}")

    # the loop continues for all directories inside music_dir


if __name__ == "__main__":
    main()