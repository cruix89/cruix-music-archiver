import os
import shutil
import logging
import requests
import re
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from pathlib import Path


def setup_directories():
    # configured directories
    music_dir = Path('/music').resolve()
    deezer_db_dir = Path('/config/deezer-db').resolve()
    log_dir = Path('/config/logs').resolve()

    # ensure directories exist
    music_dir.mkdir(parents=True, exist_ok=True)
    deezer_db_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    return music_dir, deezer_db_dir, log_dir


def main():
    # log setup
    music_dir, deezer_db_dir, log_dir = setup_directories()
    log_file = log_dir / 'missing_covers_downloader.log'
    logging.basicConfig(filename=str(log_file), level=logging.INFO)

    # check if log file is created correctly
    if not log_file.exists():
        print(f"error: unable to create log file at {log_file}. check write permissions.\n")
    else:
        print(f"log file created at: {log_file}\n")

    def validate_directory(directory):
        if not directory.is_dir():
            error = f'directory not found: {directory}'
            logging.error(error)
            print(error)
            return False
        return True

    def process_image(source, width, height):
        try:
            with Image.open(source) as img:
                img_width, img_height = img.size
            if img_width == width and img_height == height:
                return True
        except UnidentifiedImageError:
            logging.error(f'error identifying image: {source}\n')
        except Exception as e:
            logging.error(f'error processing file {source}: {e}\n')
        return False

    def find_cover_in_deezer_db(mp3_name, width, height):
        for root, _, files in os.walk(deezer_db_dir):
            txt_file = f'{mp3_name}.txt'
            if txt_file in files:
                txt_path = Path(root) / txt_file
                try:
                    with txt_path.open('r', encoding='utf-8') as f:
                        content = f.read()
                        match = re.search(r"'cover_xl':\s*'([^']+)'", content)
                        if match:
                            img_url = match.group(1)
                            logging.info(f"image URL found: {img_url}")
                            return download_and_resize_image(img_url, width, height)
                except Exception as e:
                    logging.error(f'error reading file {txt_path}: {e}\n')
                    print(f'error reading file {txt_path}: {e}\n')
        return None

    def download_and_resize_image(url, width, height):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img = img.resize((width, height))
            return img
        except requests.exceptions.RequestException as e:
            logging.error(f'error downloading image: {e}\n')
            print(f'error downloading image: {e}\n')
            return None
        except Exception as e:
            logging.error(f'error processing downloaded image: {e}\n')
            print(f'error processing downloaded image: {e}\n')
            return None

    def copy_first_image_to_lonely_mp3(directory, width=544, height=544):
        if not validate_directory(directory):
            return

        logging.info(f'beginning process in directory: {directory}\n')
        for root, _, files in os.walk(directory):
            jpg_files = [file for file in files if file.endswith('.jpg')]
            mp3_files = [file for file in files if file.endswith('.mp3')]

            for mp3_file in mp3_files:
                mp3_path = Path(mp3_file)
                mp3_name = mp3_path.stem

                if not any(jpg_file.startswith(mp3_name) for jpg_file in jpg_files):
                    for jpg_file in jpg_files:
                        source = Path(root) / jpg_file
                        if process_image(source, width, height):
                            destination = Path(root) / f'{mp3_name}.jpg'
                            shutil.copy2(source, destination)
                            logging.info(f'file copied: {source} TO {destination}\n')
                            break
                    else:
                        img = find_cover_in_deezer_db(mp3_name, width, height)
                        if img:
                            destination = Path(root) / f'{mp3_name}.jpg'
                            img.save(destination)
                            logging.info(f'cover downloaded and saved: {destination}\n')
                        else:
                            logging.error(f'unable to find or download a cover for: {mp3_name}\n')
                            print(f'unable to find or download a cover for: {mp3_name}\n')

        logging.info('process completed.\n')

    # execute main function
    copy_first_image_to_lonely_mp3(music_dir)

    print("missing covers downloaded.")


if __name__ == "__main__":
    main()