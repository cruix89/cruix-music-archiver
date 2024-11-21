import os
import eyed3
import requests
import logging

# print in terminal
print("[cruix-music-archiver] downloading music database... 🚀  initiating data stream from the audio archives! 🚀  ", flush=True)

def setup_directories():
    # absolute directories
    base_dir = '/music'
    db_dir = '/config/dz-db'
    log_dir = '/config/logs'

    # create directories if they do not exist
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(db_dir, exist_ok=True)

    return base_dir, db_dir, log_dir


def count_mp3_files(base_dir):
    total_files = 0
    for _, _, files in os.walk(base_dir):
        total_files += sum(1 for file in files if file.endswith('.mp3'))
    return total_files


def main():
    # logging configuration
    base_dir, db_dir, log_dir = setup_directories()
    logging.basicConfig(filename=os.path.join(log_dir, 'dz_db_downloader.log'), level=logging.INFO)

    # file count to track progress
    total_files = count_mp3_files(base_dir)
    logging.info(f"starting to process {total_files} files.")

    # for each subdirectory and file in the base directory
    for dirpath, dirnames, filenames in os.walk(base_dir):
        for filename in filenames:

            # if the file is a mp3
            if filename.endswith('.mp3'):

                # full file path
                full_path = os.path.join(dirpath, filename)

                # load mp3 tags
                audiofile = eyed3.load(full_path)
                if audiofile is None or audiofile.tag is None:
                    logging.warning(f"file {filename} does not contain valid id3 tags.")
                    continue

                track_name = audiofile.tag.title
                album_name = audiofile.tag.album
                artist_name = audiofile.tag.artist

                # make request to dz api
                try:
                    response = requests.get(
                        f'https://api.deezer.com/search?q=track:"{track_name}" album:"{album_name}" artist:"{artist_name}"&limit=1')
                    response.raise_for_status()  # raises exception for http error status codes
                    data = response.json()
                except requests.exceptions.RequestException as e:
                    logging.error(f"http request error: {e}")
                    continue  # skip to next file
                except requests.exceptions.JSONDecodeError as e:
                    logging.error(f"json decoding error: {e}")
                    continue  # skip to next file

                # corresponding text file path in db directory
                relative_path = os.path.relpath(full_path, base_dir)
                txt_path = os.path.join(db_dir, os.path.splitext(relative_path)[0] + '.txt')

                # create subdirectories if necessary
                os.makedirs(os.path.dirname(txt_path), exist_ok=True)

                # write data to text file
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(str(data))

                # log action
                logging.info(f"file {filename} processed. data saved to {txt_path}.")

    logging.info("processing completed.")
    print("[cruix-music-archiver] music database updated... 🚀  synchronization complete — the library is now in perfect harmony! 🚀  ")


if __name__ == "__main__":
    main()