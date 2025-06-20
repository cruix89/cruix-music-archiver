import os
import shutil

# initial message
print("[cruix-music-archiver] Starting Disambiguation Process...  🧩  The Mission Begins to Sort Out the Chaos!  🔄  ")

# show current working directory
print(f"[cruix-music-archiver] Current Working Directory: {os.getcwd()}")

# absolute path to the configuration file
config_file_path = "/app/lists/artist_disambiguator.txt"

def move_files_based_on_list(file_path):
    """
    Reads a list in the format 'source‖destination' and moves files or directories
    from the source to the destination.

    :param file_path: path to the .txt file containing the source and destination information
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            # ignore empty lines or comments
            if not line.strip() or line.startswith("#"):
                continue

            # divide the line by the delimiter '‖'
            try:
                origin, destination = map(str.strip, line.split("‖"))
            except ValueError:
                print(f"[cruix-music-archiver] Invalid Format In: {line.strip()} ⚠️  Something’s Not Quite Right In This File! ⚠️ ")
                continue

            # log the path being checked
            print(f"[cruix-music-archiver] Checking Origin: {origin}")

            # check if the source exists
            if not os.path.exists(origin):
                print(f"[cruix-music-archiver] Source Not Found: {origin} ⚠️  Skipping... ⚠️ ")
                continue

            # check permissions (readable?)
            if not os.access(origin, os.R_OK):
                print(f"[cruix-music-archiver] No Permission to Read: {origin} ⚠️  Skipping... ⚠️ ")
                continue

            # if source is a file
            if os.path.isfile(origin):
                # ensure destination folder exists
                os.makedirs(os.path.dirname(destination), exist_ok=True)

                # move file
                shutil.move(origin, destination)
                print(f"[cruix-music-archiver] Moved File: {origin} to {destination}  🛠️ Transformation Complete — Clarity Achieved! 🛠️ ")

            # if source is a directory
            elif os.path.isdir(origin):
                # ensure destination folder exists
                os.makedirs(destination, exist_ok=True)

                # move all files inside the directory
                for filename in os.listdir(origin):
                    src_file = os.path.join(origin, filename)
                    dst_file = os.path.join(destination, filename)

                    if os.path.isfile(src_file):
                        # check permissions of each file
                        if os.access(src_file, os.R_OK):
                            shutil.move(src_file, dst_file)
                            print(f"[cruix-music-archiver] Moved File: {src_file} to {dst_file}  🛠️ Transformation Complete — Clarity Achieved! 🛠️ ")
                        else:
                            print(f"[cruix-music-archiver] No Permission to Read: {src_file} ⚠️  Skipping file... ⚠️ ")
            else:
                print(f"[cruix-music-archiver] Unknown Source Type: {origin} ⚠️  Skipping... ⚠️ ")

    except Exception as e:
        print(f"[cruix-music-archiver] Error Processing the List: {e} ⚠️  The List Fought Back — Mission Failed! ⚠️ ")

# execute the script
if __name__ == "__main__":
    move_files_based_on_list(config_file_path)