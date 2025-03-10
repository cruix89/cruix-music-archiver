import os


def rename_na_to_youtube_tracks(base_directory="/music"):
    """
    Renames folders named 'na' to 'youtube_tracks' only if they are directly inside the base_directory.
    """
    base_depth = base_directory.rstrip(os.sep).count(os.sep)  # count the levels of the base directory

    for root, dirs, _ in os.walk(base_directory):
        current_depth = root.count(os.sep)  # count the levels of the current directory

        if current_depth == base_depth + 1:  # ensure it is exactly one level below the base directory
            for dir_name in dirs:
                if dir_name.lower() == "na":
                    old_path = os.path.join(root, dir_name)
                    new_path = os.path.join(root, "youtube_tracks")

                    try:
                        os.rename(old_path, new_path)
                        print(f"[cruix-music-archiver] Renamed: {old_path} to {new_path}. 📂⬆️")
                    except Exception as e:
                        print(f"[cruix-music-archiver] Failed to rename {old_path}. Error: {e}. 🔥😱")


if __name__ == "__main__":
    rename_na_to_youtube_tracks()