import os
import logging
from mutagen.id3 import ID3

def main():
    music_dir = "/music"
    logs_dir = "/config/logs"

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    logging.basicConfig(filename=os.path.join(logs_dir, "genre_fixer.log"), level=logging.DEBUG)
    print("\nformatting genre tags...")
    logging.debug("FORMATTING GENRE TAGS...\n")

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
                            logging.debug(f"GENRE TAG FORMATTED FOR FILE: {filename}")
                            logging.debug(f"ORIGINAL GENRE: {original_genre}")
                            logging.debug(f"FORMATTED GENRE: {formatted_genre}")
                except Exception as e:
                    logging.error(f"ERROR PROCESSING FILE: {filename} - {str(e)}")

    print("genre tag formatting completed...")
    logging.debug("GENRE TAG FORMATTING COMPLETED...\n")

if __name__ == "__main__":
    main()