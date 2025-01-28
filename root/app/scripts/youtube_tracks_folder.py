import os


def rename_na_to_youtube_tracks(base_directory="/music"):
    """
    traverses all subdirectories from base_directory and renames folders named 'na' to 'youtube_tracks'.
    """
    for root, dirs, _ in os.walk(base_directory):
        for dir_name in dirs:
            if dir_name.lower() == "na":
                old_path = os.path.join(root, dir_name)
                new_path = os.path.join(root, "youtube_tracks")

                try:
                    os.rename(old_path, new_path)
                    print(f"[cruix-music-archiver] Renamed: {old_path} to {new_path}. It’s Like a Folder Evolution—Leveling Up! 📂  ⬆️")
                except Exception as e:
                    print(f"[cruix-music-archiver] Oops! Failed to Rename {old_path} to {new_path}. Something Went Wrong: {e}. 🔥  😱")


if __name__ == "__main__":
    rename_na_to_youtube_tracks()