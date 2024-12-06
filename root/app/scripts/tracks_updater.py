import eyed3
import os
import logging

# configure logging
log_file = '/config/logs/track_updater.log'
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# directory paths
music_dir = '/music'
db_file = '/app/lists/tracks_db.txt'


def update_track_number_tag(mp3_file, track_number):
    """updates the 'track number' tag of the mp3 file."""
    audio_file = eyed3.load(mp3_file)
    if audio_file.tag is None:
        audio_file.tag = eyed3.id3.tag.Tag()
        audio_file.tag.file_info = eyed3.id3.FileInfo(mp3_file)

    # update the 'track number' tag
    audio_file.tag.track_num = int(track_number)
    audio_file.tag.save()


def find_track_number(artist, album, track):
    """finds the track number in the tracks_db.txt file."""
    # build the search string
    search_str = f"{artist}/{album}/{track}"

    # read the tracks_db.txt file and search for the exact match
    with open(db_file, 'r', encoding='utf-8') as db:
        for line in db:
            # split line into parts
            db_entry, track_number = line.strip().split('|', 1)
            if db_entry == search_str:  # ensure exact match
                return track_number.strip()
    return None  # return None if the string is not found


def process_music():
    """iterates over the music in the /music directory and updates tags with the track number."""
    for root, dirs, files in os.walk(music_dir):
        for file in files:
            if file.endswith(".mp3"):
                mp3_file = os.path.join(root, file)
                audio_file = eyed3.load(mp3_file)

                if audio_file.tag is None:
                    continue  # skip files without tags

                # extract the necessary tags
                artist = audio_file.tag.artist
                album = audio_file.tag.album
                track = audio_file.tag.title

                if artist and album and track:
                    # find the track number in the tracks_db.txt file
                    track_number = find_track_number(artist, album, track)

                    if track_number:
                        # if found, update the 'track number' tag
                        update_track_number_tag(mp3_file, track_number)
                        message = (
                            f"[cruix-music-archiver] Updated {file} With Track Number: {track_number} 🚀 "
                            "Now It's Officially Part of the Soundtrack of the Galaxy! 🌌"
                        )
                        logging.info(message)
                        print(message)
                    else:
                        message = (
                            f"[cruix-music-archiver] Not Found in DB: {artist}/{album}/{track} 🤖 "
                            "The Database Couldn't Locate This Track. It's in Another Dimension! 🤖"
                        )
                        logging.warning(message)
                        print(message)
                else:
                    message = (
                        f"[cruix-music-archiver] Incomplete Tags For File: {file} 🛠️ "
                        "Looks Like This File Missed Its Tag Upgrade! 🛠️"
                    )
                    logging.error(message)
                    print(message)


if __name__ == '__main__':
    process_music()