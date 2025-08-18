import os

print("[cruix-music-archiver] Capitalizing Artists Folders...  🔠  The Folders Are Leveling Up In Style!  🚀  ")

# set the music directory
music_dir = '/music'

def next_available_name(directory: str, base_name: str) -> str:
    """
    Retorna um nome disponível dentro de 'directory'.
    Se 'base_name' já existir, tenta 'base_name copy1', 'base_name copy2', etc.
    """
    candidate = base_name
    candidate_path = os.path.join(directory, candidate)

    if not os.path.exists(candidate_path):
        return candidate

    n = 1
    while True:
        candidate = f"{base_name} copy{n}"
        candidate_path = os.path.join(directory, candidate)
        if not os.path.exists(candidate_path):
            return candidate
        n += 1

# cycle through all items in the music directory
for item in os.listdir(music_dir):
    item_path = os.path.join(music_dir, item)

    # check if the item is a directory
    if os.path.isdir(item_path):
        # replace underscores with spaces and capitalize the directory name
        cleaned_base = item.replace('_', ' ').title()

        # only proceed if there will be a change
        if item != cleaned_base:
            # resolve duplicate target names by appending copyN if needed
            final_name = next_available_name(music_dir, cleaned_base)
            final_path = os.path.join(music_dir, final_name)

            # rename the directory
            os.rename(item_path, final_path)

            # logging
            if final_name == cleaned_base:
                print(f"[cruix-music-archiver] Renamed: {item} to {final_name} ✅")
            else:
                print(f"[cruix-music-archiver] Renamed: {item} to {final_name} (duplicate resolved) ✅")

print("[cruix-music-archiver] Artists Folders Look Awesome!  😎   Like a Perfectly Executed Game Plan!  🏆   ")