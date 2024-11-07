import os
import re
import requests
import logging
from PIL import Image
from io import BytesIO


def setup_directories():
    # define absolute paths for directories
    music_dir = "/music"
    deezer_db_dir = "/config/deezer-db"
    log_dir = "/config/logs"

    # ensure that directories exist
    os.makedirs(music_dir, exist_ok=True)
    os.makedirs(deezer_db_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    return music_dir, deezer_db_dir, log_dir


def main():
    print("\nsetting up poweramp artist image...")

    # logging setup
    music_dir, deezer_db_dir, log_dir = setup_directories()
    logging.basicConfig(filename=os.path.join(log_dir, 'poweramp_artist_downloader.log'), level=logging.DEBUG)

    logging.debug(f"music_dir: {music_dir}\n")
    logging.debug(f"deezer_db_dir: {deezer_db_dir}\n")
    logging.debug(f"log_dir: {log_dir}\n")

    if not os.path.exists(music_dir):
        logging.error(f"the music directory '{music_dir}' does not exist.\n")
        return

    for folder in os.listdir(music_dir):
        search_dir = os.path.join(deezer_db_dir, folder)
        logging.debug(f"searching in directory: {search_dir}\n")

        if os.path.exists(search_dir):
            for root, dirs, files in os.walk(search_dir):
                logging.debug(f"checking files in: {root}\n")

                for file in files:
                    if file.endswith(".txt"):
                        file_path = os.path.join(root, file)
                        logging.debug(f"reading file: {file_path}\n")

                        with open(file_path, 'r') as f:
                            content = f.read()
                            match = re.search(r"'picture_xl':\s*'([^']+)'", content)
                            if match:
                                img_url = match.group(1)
                                logging.debug(f"image url found: {img_url}\n")

                                try:
                                    response = requests.get(img_url, timeout=10)
                                    response.raise_for_status()
                                    img = Image.open(BytesIO(response.content))
                                    img = img.resize((1280, 1280))
                                    img.save(os.path.join(music_dir, folder, "cover.jpg"))
                                    logging.info(f'artist image downloaded and saved for {folder}\n')
                                    break
                                except requests.exceptions.RequestException as e:
                                    logging.error(f'error downloading image from {img_url} for {folder}: {str(e)}\n')
                                except Exception as e:
                                    logging.error(f'error processing image for {folder}: {str(e)}\n')
                else:
                    continue
                break

    print("poweramp artist image set up successfully.\n")


if __name__ == "__main__":
    main()