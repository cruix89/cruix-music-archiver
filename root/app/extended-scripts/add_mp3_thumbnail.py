import os
import eyed3
import logging

# global variables for directories
music_directory: str = ""
logs_directory: str = ""

def add_thumbnail_to_mp3(mp3_path: str, image_path: str) -> None:
    try:
        audiofile = eyed3.load(mp3_path)
        if os.path.isfile(image_path) and os.path.getsize(image_path) > 0:
            with open(image_path, 'rb') as img:
                audiofile.tag.images.set(3, img.read(), 'image/jpeg')
            audiofile.tag.save()
            logging.info(f'image {image_path} was successfully added to MP3 file: {mp3_path}')
        else:
            logging.warning(f'image {image_path} does not exist or is empty')
    except Exception as exc:
        logging.error(f'error processing file: {mp3_path}: {str(exc)}')

def setup_directories() -> None:
    global music_directory, logs_directory
    # set absolute paths
    music_directory = '/music'
    logs_directory = '/config/logs'

def main():

    # configure directories
    setup_directories()

    # configure logging
    logging.basicConfig(
        filename=os.path.join(logs_directory, 'add_mp3_thumbnail.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(console_handler)

    success_count = 0
    failure_count = 0

    # supported image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp']

    for root, _, files in os.walk(music_directory):
        for filename in files:
            if filename.endswith('.mp3'):
                mp3_file: str = os.path.join(root, filename)
                # try to find an image file with any of the supported extensions
                image_file_found = False
                for ext in image_extensions:
                    image_file: str = os.path.join(root, filename.rsplit('.', 1)[0] + ext)
                    if os.path.isfile(image_file):
                        add_thumbnail_to_mp3(mp3_file, image_file)
                        success_count += 1
                        image_file_found = True
                        break  # exit the loop once a valid image is found
                if not image_file_found:
                    logging.warning(f'no valid image file found for {mp3_file}')
            else:
                logging.warning(f'file {os.path.join(root, filename)} is not an mp3 file')

    print(f"[cruix-music-archiver] thumbnails successfully added to {success_count} songs with {failure_count} failures.")

if __name__ == "__main__":
    main()