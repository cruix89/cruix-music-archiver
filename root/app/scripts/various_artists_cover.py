import os
import shutil

# absolute paths
music_directory = "/music"
default_images_directory = "/app/default-covers/various-artists"
default_cover = os.path.join(default_images_directory, "cover.jpg")
default_folder = os.path.join(default_images_directory, "folder.jpg")

def check_and_copy_images():
    # traverse only subdirectories of /music
    for root, dirs, files in os.walk(music_directory):
        # ignore the /music root directory
        if root == music_directory:
            continue

        # check if the cover.jpg or folder.jpg files exist in the current subdirectory
        has_cover = "cover.jpg" in files
        has_folder = "folder.jpg" in files

        # if both are missing, copy the default images
        if not has_cover and not has_folder:
            print(f"[cruix-music-archiver] Artist Not Found in Database, Applying 'Various Artists' Cover. Who Needs a Solo Artist Anyway? 🎤  🎶 : {root} 🎤  🎶")
            if os.path.exists(default_cover):
                shutil.copy(default_cover, os.path.join(root, "cover.jpg"))
                print(f"[cruix-music-archiver] Copied: cover.jpg For {root}. The Cover is Now as Legendary as the Album! 📀  ✨")
            if os.path.exists(default_folder):
                shutil.copy(default_folder, os.path.join(root, "folder.jpg"))
                print(f"[cruix-music-archiver] Copied: folder.jpg For {root}. Folder's Looking Sharper Than a Jedi's Lightsaber! ⚔️  💫")

if __name__ == "__main__":
    check_and_copy_images()