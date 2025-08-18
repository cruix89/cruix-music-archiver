import eyed3
from eyed3.id3 import Tag
import os
import logging

# configure logging
log_file = '/config/logs/album_updater.log'
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# directory paths
music_dir = '/music'
db_file = '/app/lists/album_db.txt'


def update_album_tag(mp3_file, new_album):
    """Updates the 'album' tag of the mp3 file."""
    audio_file = eyed3.load(mp3_file)
    if audio_file.tag is None:
        audio_file.tag = eyed3.id3.tag.Tag()
        audio_file.tag.file_info = eyed3.id3.FileInfo(mp3_file)

    # update the 'album' tag
    audio_file.tag.album = new_album
    audio_file.tag.save()


def find_album_replacement(album_artist, album, track):
    """Finds the new album name in the album_db.txt file."""
    search_str = f"{album_artist}/{album}/{track}"

    with open(db_file, 'r', encoding='utf-8') as db:
        for line in db:
            db_entry, new_album = line.strip().split('‖', 1)
            if db_entry == search_str:
                return new_album.strip()
    return None


def process_music():
    """Iterates over the music in the /music directory and updates the album tag if found in the DB."""
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
                    new_album = find_album_replacement(album_artist, album, track)

                    if new_album:
                        update_album_tag(mp3_file, new_album)
                        message = (
                            f"[cruix-music-archiver] Album Tag Updated: {file} -> '{new_album}' 🚀 "
                            " Now This Track Belongs to a New Dimension of Sound! 🌌"
                        )
                        logging.info(message)
                        print(message)
                    else:
                        message = (
                            f"[cruix-music-archiver] Not Found in DB: {album_artist}/{album}/{track} 🤖 "
                            " The Database Couldn't Find a New Album for This Track. Still Floating in Space! 🌌"
                        )
                        logging.warning(message)
                        # print(message)
                else:
                    message = (
                        f"[cruix-music-archiver] Incomplete Tags For File: {file} 🛠️ "
                        " This Track Is Missing Its Metadata Passport! 🛠️"
                    )
                    logging.error(message)
                    # print(message)


if __name__ == '__main__':
    process_music()