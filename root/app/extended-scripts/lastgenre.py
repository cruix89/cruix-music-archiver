import os
import pylast
import logging
import mutagen.id3
from mutagen import File

# define absolute paths directly
log_dir = "/config/logs"
lists_dir = "/app/lists"
music_dir = "/downloads"
log_file = os.path.join(log_dir, 'lastgenre.log')


def setup_directories():
    os.makedirs(log_dir, exist_ok=True)


def read_artist_list():
    artist_list = {}
    list_path = os.path.join(lists_dir, "genres.txt")
    if os.path.exists(list_path):
        with open(list_path, "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 2:
                    artist, genre = parts
                    artist_list[artist] = genre
    return artist_list


def save_artist_list(artist_list):
    list_path = os.path.join(lists_dir, "genres.txt")
    with open(list_path, "w") as file:
        for artist, genre in artist_list.items():
            file.write(f"{artist}|{genre}\n")


def main():
    setup_directories()

    logging.basicConfig(filename=log_file, filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    api_key = "ca2a69dad0b07e99c2e7517b4354f54c"
    api_secret = "6f815b76ff0790c0fe172d372a6a5740"

    if not api_key or not api_secret:
        logging.critical('API keys for Last.fm not configured.\n')
        return

    network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
    genre_cache = {}

    artist_list = read_artist_list()

    def get_genre_tags(artist_name):
        if artist_name in artist_list:
            return artist_list[artist_name]

        if artist_name in genre_cache:
            return genre_cache[artist_name]

        try:
            artist = network.get_artist(artist_name)
            if not artist:
                logging.warning(f'Artist not found: {artist_name}\n')
                return None

            top_tag = artist.get_top_tags(limit=1)
            genre_tag = top_tag[0].item.get_name() if top_tag else None

            if genre_tag:
                logging.info(f'Genre {genre_tag} found for artist {artist_name}\n')
            else:
                logging.warning(f'No genre found for artist {artist_name}\n')

            genre_cache[artist_name] = genre_tag
            return genre_tag
        except pylast.WSError as e:
            logging.error(f'Error retrieving genre tag for artist {artist_name}: {str(e)}\n')
            return None

    def process_directory(dir_path):
        # Count .mp3 files
        total_files = sum(len([file for file in files if file.endswith(".mp3")]) for _, _, files in os.walk(dir_path))
        print(f"Total MP3 files found: {total_files}")

        processed_files = 0
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".mp3"):
                    file_path = os.path.join(root, file)
                    processed_files += 1
                    print(f"Processing file {processed_files}/{total_files}: {file_path}")
                    logging.info(f'Processing file: {file_path}\n')

                    audio = File(file_path)
                    artist_frame = audio.get("TPE2")
                    if artist_frame:
                        artist_name = artist_frame.text[0]
                        logging.info(f'Artist found: {artist_name}\n')
                        genre_tag = get_genre_tags(artist_name)
                        if genre_tag:
                            audio["TCON"] = mutagen.id3.TCON(encoding=3, text=genre_tag)  # Using TCON from mutagen.id3
                            audio.save()
                            print(f"Genre '{genre_tag}' added to {file_path}")
                            logging.info(f'Genre {genre_tag} added to file {file_path}\n')
                            artist_list[artist_name] = genre_tag
                            save_artist_list(artist_list)
                        else:
                            logging.warning(f'No genre found for artist {artist_name}, file: {file_path}\n')
                            print(f"No genre found for {file_path}")
                    else:
                        logging.warning(f'No artist tag found in file: {file_path}\n')
                        print(f"No artist tag found in {file_path}")

    process_directory(music_dir)


if __name__ == "__main__":
    main()