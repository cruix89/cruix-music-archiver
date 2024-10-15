import os
import shutil
import logging

# ABSOLUTE DIRECTORY PATHS
logs_dir = "/config/logs"
lists_dir = "/app/lists"
downloads_dir = "/downloads"
unofficial_albums_dir = "/config/unofficial-albums"

# CREATE NECESSARY DIRECTORIES
for directory in [logs_dir, lists_dir, downloads_dir, unofficial_albums_dir]:
    os.makedirs(directory, exist_ok=True)

# CONFIGURE LOGGING
logging.basicConfig(filename=os.path.join(logs_dir, "unofficial_albums_mover.log"), level=logging.INFO)

print("\nmoving unofficial albums...")

# READ THE FOLDER LIST FROM THE FILE
try:
    with open(os.path.join(lists_dir, "unofficial_albums.txt"), 'r', encoding='utf-8') as f:
        folders = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    logging.error("FILE unofficial_albums.txt NOT FOUND.")
    print("ERROR: FILE NOT FOUND.")
    exit(1)

# WALK THROUGH THE DOWNLOAD DIRECTORY
for root, dirs, files in os.walk(downloads_dir):
    for name in dirs:
        if name in folders:
            source = os.path.join(root, name)
            destination = os.path.join(unofficial_albums_dir, os.path.relpath(source, downloads_dir))
            try:
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                if os.path.exists(destination):
                    shutil.rmtree(destination)
                shutil.move(source, destination)
                logging.info(f'THE ALBUM {name} WAS SUCCESSFULLY MOVED TO {destination}\n')
            except Exception as e:
                logging.error(f'ERROR MOVING ALBUM {name}: {e}\n')

print("unofficial albums moved successfully.\n")