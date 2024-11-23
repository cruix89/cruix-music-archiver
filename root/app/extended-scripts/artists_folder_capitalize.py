import os

print("[cruix-music-archiver] capitalizing artists' folders... 🚀  the folders are leveling up in style! 🚀  ")

# set the music directory
music_dir = '/music'

# cycle through all items in the music directory
for item in os.listdir(music_dir):
    item_path = os.path.join(music_dir, item)

    # check if the item is a directory
    if os.path.isdir(item_path):
        # replace underscores with spaces and capitalize the directory name
        cleaned_name = item.replace('_', ' ').title()
        cleaned_path = os.path.join(music_dir, cleaned_name)

        # rename the directory
        if item != cleaned_name:
            os.rename(item_path, cleaned_path)
            print(f'[cruix-music-archiver] renamed: {item} to {cleaned_name} ✅')

print("[cruix-music-archiver] artists' folders look awesome! ⚡  Like a perfectly executed game plan! ⚡  ")