import os
import shutil
import glob
from typing import Optional

# define absolute paths for directories
LOGS_DIR: str = '/config/logs'
LISTS_DIR: str = '/app/lists'
MUSIC_DIR: str = '/music'

# create directories if they do not exist
for directory_path in (LOGS_DIR, LISTS_DIR, MUSIC_DIR):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

# initial message
print("[cruix-music-archiver] Starting Disambiguation Process...  🧩  The Mission Begins to Sort Out the Chaos!  🔄  ")

# absolute path to the configuration file
config_file_path: str = os.path.join(LISTS_DIR, 'artist_disambiguator.txt')


def find_case_insensitive(target_path: str) -> Optional[str]:
    """
    searches for a path on disk in a case-insensitive manner.
    returns the actual path if found, otherwise returns None.
    """
    path_parts: list[str] = target_path.strip(os.sep).split(os.sep)
    current_directory: str = os.sep

    for part in path_parts:
        if not os.path.isdir(current_directory):
            return None
        dir_items: list[str] = os.listdir(current_directory)
        matches: list[str] = [item for item in dir_items if item.lower() == part.lower()]
        if not matches:
            return None
        current_directory = os.path.join(current_directory, matches[0])

    return current_directory


def move_files_based_on_list(list_file_path: str) -> None:
    """
    Reads a list in the format 'relative_source‖relative_destination' and moves files or folders
    from the source to the destination under MUSIC_DIR.
    """
    try:
        with open(list_file_path, "r", encoding="utf-8") as file:
            lines: list[str] = file.readlines()

        for line in lines:
            # ignore empty lines or comments
            if not line.strip() or line.strip().startswith("#"):
                continue

            try:
                rel_origin, rel_destination = map(str.strip, line.split("‖"))
            except ValueError:
                print(f"[cruix-music-archiver] Invalid Format In: {line.strip()} ⚠️  Something’s Not Quite Right In This File! ⚠️ ")
                continue

            # force full paths under MUSIC_DIR
            origin_path: str = os.path.join(MUSIC_DIR, rel_origin)
            destination_path: str = os.path.join(MUSIC_DIR, rel_destination)

            # search the path in a case-insensitive way
            origin_real_path: Optional[str] = find_case_insensitive(origin_path)

            # if it ends with .* (any extension)
            if origin_path.endswith(".*"):
                base_no_ext_path: str = origin_path[:-2]  # remove ".*"
                base_real_path: Optional[str] = find_case_insensitive(base_no_ext_path)
                if base_real_path:
                    glob_pattern: str = base_real_path + ".*"
                    matched_files: list[str] = glob.glob(glob_pattern)
                    if not matched_files:
                        print(f"[cruix-music-archiver] No Files Found Matching: {origin_path} ⚠️  Skipping.")
                        continue
                    os.makedirs(destination_path, exist_ok=True)
                    for matched_file in matched_files:
                        matched_file_path: str = str(matched_file)
                        try:
                            shutil.move(matched_file_path, os.path.join(destination_path, os.path.basename(matched_file_path)))
                            print(f"[cruix-music-archiver] Disambiguated: {matched_file_path} to {destination_path}  🛠️  File Moved Successfully!")
                        except Exception as e:
                            print(f"[cruix-music-archiver] Error Moving File {matched_file_path}: {e}  ⚠️  ")
                    continue
                else:
                    print(f"[cruix-music-archiver] Source Not Found: {origin_path} ⚠️  Skipping.")
                    continue

            # se não for caso com ".*"
            if origin_real_path is None:
                print(f"[cruix-music-archiver] Source Not Found: {origin_path} ⚠️  Skipping.")
                continue

            os.makedirs(destination_path, exist_ok=True)

            # if source is a file
            if os.path.isfile(origin_real_path):
                filename: str = os.path.basename(origin_real_path)
                dst_file_path: str = os.path.join(destination_path, filename)
                try:
                    shutil.move(origin_real_path, dst_file_path)
                    print(f"[cruix-music-archiver] Disambiguated: {origin_real_path} to {dst_file_path}  🛠️  File Moved Successfully!")
                except Exception as e:
                    print(f"[cruix-music-archiver] Error Moving File {origin_real_path}: {e}  ⚠️  ")

            # if source is a directory
            elif os.path.isdir(origin_real_path):
                dir_items: list[str] = os.listdir(origin_real_path)
                for filename in dir_items:
                    src_file_path: str = os.path.join(origin_real_path, filename)
                    dst_file_path: str = os.path.join(destination_path, filename)
                    if os.path.isfile(src_file_path):
                        try:
                            shutil.move(src_file_path, dst_file_path)
                            print(f"[cruix-music-archiver] Disambiguated: {src_file_path} to {dst_file_path}  🛠️  File Moved Successfully!")
                        except Exception as e:
                            print(f"[cruix-music-archiver] Error Moving File {src_file_path}: {e}  ⚠️  ")

    except Exception as e:
        print(f"[cruix-music-archiver] Error Processing the List: {e} ⚠️ The List Fought Back — Mission Failed! ⚠️ ")


# execute the script
if __name__ == "__main__":
    move_files_based_on_list(config_file_path)