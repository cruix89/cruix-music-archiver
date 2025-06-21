import os
import shutil

# define absolute paths for directories
LOGS_DIR = '/config/logs'
LISTS_DIR = '/app/lists'
MUSIC_DIR = '/music'

# create directories if they do not exist
for path in [LOGS_DIR, LISTS_DIR, MUSIC_DIR]:
    if not os.path.exists(path):
        os.makedirs(path)

# initial message
print("[cruix-music-archiver] Starting Disambiguation Process...  🧩  The Mission Begins to Sort Out the Chaos!  🔄  ")

# absolute path to the configuration file
config_file_path = os.path.join(LISTS_DIR, 'artist_disambiguator.txt')

def move_files_based_on_list(file_path):
    """
    reads a list in the format 'relative_source‖relative_destination' and moves files or folders from the source to the destination under MUSIC_DIR.

    :param file_path: path to the .txt file containing the source and destination information
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        for line in lines:
            # ignore empty lines or comments
            if not line.strip() or line.startswith("#"):
                continue

            # divide the line by the delimiter '‖'
            try:
                rel_origin, rel_destination = map(str.strip, line.split("‖"))
            except ValueError:
                print(f"[cruix-music-archiver] Invalid Format In: {line.strip()} ⚠️  Something’s Not Quite Right In This File! ⚠️ ")
                continue

            # force full paths under MUSIC_DIR
            origin = os.path.join(MUSIC_DIR, rel_origin)
            destination = os.path.join(MUSIC_DIR, rel_destination)

            # check if the source exists
            if not os.path.exists(origin):
                print(f"[cruix-music-archiver] Source Not Found: {origin} ⚠️  Skipping.")
                continue

            # create the destination folder if it does not exist
            os.makedirs(destination, exist_ok=True)

            # if source is a file
            if os.path.isfile(origin):
                filename = os.path.basename(origin)
                dst_file = os.path.join(destination, filename)
                try:
                    shutil.move(origin, dst_file)
                    print(f"[cruix-music-archiver] Disambiguated: {origin} to {dst_file}  🛠️  File Moved Successfully!")
                except Exception as e:
                    print(f"[cruix-music-archiver] Error Moving File {origin}: {e}  ⚠️  ")

            # if source is a directory
            elif os.path.isdir(origin):
                for filename in os.listdir(origin):
                    src_file = os.path.join(origin, filename)
                    dst_file = os.path.join(destination, filename)

                    if os.path.isfile(src_file):
                        try:
                            shutil.move(src_file, dst_file)
                            print(f"[cruix-music-archiver] Disambiguated: {src_file} to {dst_file}  🛠️  File Moved Successfully!")
                        except Exception as e:
                            print(f"[cruix-music-archiver] Error Moving File {src_file}: {e}  ⚠️  ")

    except Exception as e:
        print(f"[cruix-music-archiver] Error Processing the List: {e} ⚠️ The List Fought Back — Mission Failed! ⚠️ ")

# execute the script
if __name__ == "__main__":
    move_files_based_on_list(config_file_path)