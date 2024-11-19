import os
import shutil
import logging

# absolute directory paths
logs_dir = "/config/logs"
lists_dir = "/app/lists"
music_dir = "/music"
unofficial_albums_dir = "/config/unofficial-albums"

# create necessary directories
for directory in [logs_dir, lists_dir, music_dir, unofficial_albums_dir]:
    os.makedirs(directory, exist_ok=True)

# configure logging
logging.basicConfig(filename=os.path.join(logs_dir, "unofficial_albums_mover.log"), level=logging.INFO)

print("[cruix-music-archiver] moving unofficial albums to /config/unofficial-albums... 🚀  warp drive engaged, albums are in transit!")

# read the folder list from the file
try:
    with open(os.path.join(lists_dir, "unofficial_albums.txt"), 'r', encoding='utf-8') as f:
        folders = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    logging.error("file unofficial_albums.txt not found.")
    print("error: file not found... the file has vanished into the digital black hole! 🌌")
    exit(1)

# walk through the download directory
for root, dirs, files in os.walk(music_dir):
    for name in dirs:
        if name in folders:
            source = os.path.join(root, name)
            destination = os.path.join(unofficial_albums_dir, os.path.relpath(source, music_dir))
            try:
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                if os.path.exists(destination):
                    shutil.rmtree(destination)
                shutil.move(source, destination)
                logging.info(f'the album {name} was successfully moved to {destination}')
            except Exception as e:
                logging.error(f'error moving album {name}: {e}')

print("[cruix-music-archiver] unofficial albums moved to the hidden vault...  mission accomplished! 🏆  🚀")