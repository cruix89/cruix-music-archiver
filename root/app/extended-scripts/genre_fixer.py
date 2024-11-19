import os
import logging
from mutagen.id3 import ID3

def main():
    music_dir = "/music"
    logs_dir = "/config/logs"

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    logging.basicConfig(filename=os.path.join(logs_dir, "genre_fixer.log"), level=logging.DEBUG)
    print("formatting genre tags... ⚙️  aligning genres to the universal music matrix!")
    logging.debug("formatting genre tags...")

    for dirpath, _, filenames in os.walk(music_dir):
        for filename in filenames:
            if filename.lower().endswith(".mp3"):  # process .mp3 (case-insensitive)
                file_path = os.path.join(dirpath, filename)
                try:
                    audiofile = ID3(file_path)
                    genre_tag = audiofile.get('TCON')
                    if genre_tag:
                        original_genre = genre_tag.text[0]
                        formatted_genre = original_genre.lower()
                        if formatted_genre != original_genre:
                            audiofile['TCON'].text[0] = formatted_genre
                            audiofile.save()
                            logging.debug(f"genre tag formatted for file: {filename}")
                            logging.debug(f"original genre: {original_genre}")
                            logging.debug(f"formatted genre: {formatted_genre}")
                except Exception as e:
                    logging.error(f"error processing file: {filename} - {str(e)}")

    print("genre tag formatting completed... 🚀  music genres aligned for maximum playback satisfaction!")
    logging.debug("genre tag formatting completed...")

if __name__ == "__main__":
    main()