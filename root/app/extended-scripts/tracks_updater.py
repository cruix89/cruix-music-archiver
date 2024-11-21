import eyed3
import os

# Directory paths
music_dir = '/music'
db_file = '/app/lists/tracks_db.txt'


def update_track_number_tag(mp3_file, track_number):
    """Updates the 'track number' tag of the MP3 file."""
    audio_file = eyed3.load(mp3_file)
    if audio_file.tag is None:
        audio_file.tag = eyed3.id3.tag.Tag(mp3_file)

    # Update the 'track number' tag
    audio_file.tag.track_set(track_number)
    audio_file.tag.save()


def find_track_number(artist, album, track):
    """Finds the track number in the tracks_db.txt file."""
    # Build the search string
    search_str = f"{artist}/{album}/{track}"

    # Read the tracks_db.txt file and search for the string
    with open(db_file, 'r', encoding='utf-8') as db:
        for line in db:
            if line.startswith(search_str):
                # If found, return the track number after the '|'
                return line.split('|')[1].strip()
    return None  # Return None if the string is not found


def process_music():
    """Iterates over the music in the /music directory and updates tags with the track number."""
    for root, dirs, files in os.walk(music_dir):
        for file in files:
            if file.endswith(".mp3"):
                mp3_file = os.path.join(root, file)
                audio_file = eyed3.load(mp3_file)

                if audio_file.tag is None:
                    continue  # Skip files without tags

                # Extract the necessary tags
                artist = audio_file.tag.artist
                album = audio_file.tag.album
                track = audio_file.tag.title

                if artist and album and track:
                    # Find the track number in the tracks_db.txt file
                    track_number = find_track_number(artist, album, track)

                    if track_number:
                        # If found, update the 'track number' tag
                        update_track_number_tag(mp3_file, track_number)
                        print(f"[cruix-music-archiver] updated {file} with track number: {track_number} 🚀  now it's officially part of the soundtrack of the galaxy!")
                    else:
                        print(f"[cruix-music-archiver] not found in db: {artist}/{album}/{track} 🤖  the database couldn't locate this track. it's in another dimension! 🤖  ")
                else:
                    print(f"[cruix-music-archiver] incomplete tags for file: {file} 🛠️  looks like this file missed its tag upgrade!")


if __name__ == '__main__':
    process_music()