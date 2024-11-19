import os


def rename_na_to_various_songs(base_directory="/music"):
    """
    percorre todos os subdiretórios a partir de base_directory e renomeia pastas chamadas 'na' para 'various_songs'.
    """
    for root, dirs, _ in os.walk(base_directory):
        for dir_name in dirs:
            if dir_name.lower() == "na":
                old_path = os.path.join(root, dir_name)
                new_path = os.path.join(root, "various_songs")

                try:
                    os.rename(old_path, new_path)
                    print(f"[cruix-music-archiver] renamed: {old_path} to {new_path}. it’s like a folder evolution—leveling up! 🚀  🎮")
                except Exception as e:
                    print(f"[cruix-music-archiver] oops! failed to rename {old_path} to {new_path}. something went wrong: {e}. 🔥  😱")


if __name__ == "__main__":
    rename_na_to_various_songs()