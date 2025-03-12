import os
import shutil


def merge_and_rename_na_to_youtube_tracks(base_directory="/music"):
    """
    renames folders named 'na' to 'youtube_tracks' only if they are directly inside the base_directory.
    if 'youtube_tracks' already exists, merge the contents of 'na' into it before renaming.
    """
    base_depth = base_directory.rstrip(os.sep).count(os.sep)  # count levels of the base directory

    for root, dirs, _ in os.walk(base_directory):
        current_depth = root.count(os.sep)  # count levels of the current directory

        if current_depth == base_depth + 1:  # ensure it's exactly one level below base_directory
            for dir_name in dirs:
                if dir_name.lower() == "na":
                    old_path = os.path.join(root, dir_name)
                    new_path = os.path.join(root, "youtube_tracks")

                    # if "youtube_tracks" already exists, move contents from "na" to it
                    if os.path.exists(new_path):
                        for item in os.listdir(old_path):
                            src = os.path.join(old_path, item)
                            dest = os.path.join(new_path, item)

                            # move file or merge directories (overwrite if necessary)
                            if os.path.isdir(src):
                                # move directory recursively
                                shutil.move(src, new_path)
                            else:
                                shutil.move(src, dest)  # overwrite existing file

                        os.rmdir(old_path)  # remove the now-empty "na" folder
                        print(f"[cruix-music-archiver] Merged and Removed: {old_path} -> {new_path}. 📂🔄")

                    else:
                        # rename directly if "youtube_tracks" doesn't exist
                        os.rename(old_path, new_path)
                        print(f"[cruix-music-archiver] Renamed: {old_path} To {new_path}. 📂⬆️")


if __name__ == "__main__":
    merge_and_rename_na_to_youtube_tracks()