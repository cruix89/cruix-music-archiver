import os
import eyed3
import logging
from datetime import datetime

def setup_directories():
    """set up the log's directory."""
    # define the absolute path for the logs directory
    logs_dir = '/config/logs'

    # create logs directory if it doesn't exist
    os.makedirs(logs_dir, exist_ok=True)

    return logs_dir

def update_release_year(path):
    """update the release year tag in MP3 files."""
    print("[cruix-music-archiver] formatting release year of mp3 files...")

    # Set up logging
    logs_dir = setup_directories()
    logging.basicConfig(filename=os.path.join(logs_dir, 'release_year_update.log'), level=logging.INFO)

    # get the current year
    current_year = datetime.now().year

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.mp3'):
                full_path = os.path.join(root, file)
                audio = eyed3.load(full_path)

                if audio.tag:
                    if audio.tag.recording_date and audio.tag.recording_date.year:
                        year = str(audio.tag.recording_date.year)
                    else:
                        year = str(current_year)

                    # update the recording date tag
                    audio.tag.recording_date = eyed3.core.Date(int(year[:4]))
                    audio.tag.save()

                    # log the update
                    logging.info(f'formatting year tag to {year[:4]} for file {full_path}')

    print("[cruix-music-archiver] release year formatted successfully.")

if __name__ == "__main__":
    # define the absolute path to the music directory
    music_directory = '/music'
    update_release_year(music_directory)