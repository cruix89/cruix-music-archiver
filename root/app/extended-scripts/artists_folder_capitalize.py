import os

print("[cruix-music-archiver] capitalizing artists' folders... 🚀  the folders are leveling up in style! 🚀  ")

# set the music directory
music_dir = '/music'

# cycle through all items in the music directory
for item in os.listdir(music_dir):
    item_path = os.path.join(music_dir, item)

    # check if the item is a directory
    if os.path.isdir(item_path):
        # capitalize the directory name
        capitalized_name = item.title()
        capitalized_path = os.path.join(music_dir, capitalized_name)

        # rename the directory
        if item != capitalized_name:
            os.rename(item_path, capitalized_path)
            print(f'[cruix-music-archiver] capitalized: {item} to {capitalized_name}')

print("[cruix-music-archiver] artists' folders look awesome! ⚡  Like a perfectly executed game plan! ⚡  ")