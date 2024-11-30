import os
import shutil

# initial message
print("[cruix-music-archiver] Starting Disambiguation Process...  🧩  The Mission Begins to Sort Out the Chaos!  🔄  ")

# absolute path to the configuration file
config_file_path = "/app/lists/artist_disambiguator.txt"

def move_files_based_on_list(file_path):
    """
    reads a list in the format 'source|destination' and moves files from the source folder to the destination folder.

    :param file_path: path to the .txt file containing the source and destination information
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        for line in lines:
            # ignore empty lines or comments
            if not line.strip() or line.startswith("#"):
                continue

            # divide the line by the delimiter '|'
            try:
                origin, destination = map(str.strip, line.split("|"))
            except ValueError:
                print(f"[cruix-music-archiver] Invalid Format In: {line.strip()} ⚠️  Something’s Not Quite Right In This File! ⚠️ ")
                continue

            # check if the source folder exists
            if not os.path.exists(origin):
                continue

            # create the destination folder if it does not exist
            os.makedirs(destination, exist_ok=True)

            # iterate over the files in the source folder
            for filename in os.listdir(origin):
                src_file = os.path.join(origin, filename)
                dst_file = os.path.join(destination, filename)

                if os.path.isfile(src_file):
                    # move the file to the destination
                    shutil.move(src_file, dst_file)
                    print(f"[cruix-music-archiver] Disambiguated: {src_file} to {dst_file}  🛠️ Transformation Complete — Clarity Achieved! 🛠️ ")

    except Exception as e:
        print(f"[cruix-music-archiver] Error Processing the List: {e} ⚠️  The List Fought Back — Mission Failed!  ⚠️  ")


# execute the script
if __name__ == "__main__":
    move_files_based_on_list(config_file_path)