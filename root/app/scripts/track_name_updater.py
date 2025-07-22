import eyed3
from eyed3.id3 import Tag
import os
import logging

# configure logging
log_file = '/config/logs/track_name_updater.log'
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# directory paths
music_dir = '/music'
db_file = '/app/lists/track_name_db.txt'


def update_track_tag(mp3_file, new_title):
    """Updates the 'title' tag of the mp3 file."""
    audio_file = eyed3.load(mp3_file)
    if audio_file.tag is None:
        audio_file.tag = eyed3.id3.tag.Tag()
        audio_file.tag.file_info = eyed3.id3.FileInfo(mp3_file)

    # update the 'title' tag
    audio_file.tag.title = new_title
    audio_file.tag.save()


def find_track_replacement(album_artist, album, track):
    """Finds the new track title in the db_file."""
    search_str = f"{album_artist}/{album}/{track}"

    with open(db_file, 'r', encoding='utf-8') as db:
        for line in db:
            db_entry, new_title = line.strip().split('‖', 1)
            if db_entry == search_str:
                return new_title.strip()
    return None


def process_music():
    """Iterates over the music in the /music directory and updates the track title if found in the DB."""
    for root, dirs, files in os.walk(music_dir):
        for file in files:
            if file.endswith(".mp3"):
                mp3_file = os.path.join(root, file)
                audio_file = eyed3.load(mp3_file)

                if audio_file.tag is None:
                    continue  # skip files without tags

                album_artist = audio_file.tag.album_artist
                album = audio_file.tag.album
                track = audio_file.tag.title

                if album_artist and album and track:
                    new_title = find_track_replacement(album_artist, album, track)

                    if new_title:
                        update_track_tag(mp3_file, new_title)
                        message = (
                            f"[cruix-music-archiver] Track Title Updated: {file} -> '{new_title}' 🚀 "
                            " This Song Just Got a New Identity in the Sound Multiverse! 🌌"
                        )
                        logging.info(message)
                        print(message)
                    else:
                        message = (
                            f"[cruix-music-archiver] Not Found in DB: {album_artist}/{album}/{track} 🤖 "
                            " This Track Couldn't Find Its New Name. Still Echoing in the Void! 🌌"
                        )
                        logging.warning(message)
                        print(message)
                else:
                    message = (
                        f"[cruix-music-archiver] Incomplete Tags For File: {file} 🛠️ "
                        " This Track Is Missing Its Metadata Passport! 🛠️"
                    )
                    logging.error(message)
                    print(message)


if __name__ == '__main__':
    process_music()