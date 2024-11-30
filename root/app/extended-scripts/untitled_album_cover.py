import os
import shutil

# absolute paths
music_directory = "/music"
default_images_directory = "/app/default-covers/untitled-album"
default_cover = os.path.join(default_images_directory, "cover.jpg")
default_folder = os.path.join(default_images_directory, "folder.jpg")


def check_and_copy_images():
    # traverse the directory structure bottom-up
    for root, dirs, files in os.walk(music_directory, topdown=False):
        # check if the current directory name is "untitled_album"
        if os.path.basename(root) == "untitled_album":
            print(
                f"[cruix-music-archiver] 'untitled_album' Detected, Applying 'untitled_album' Cover. Time to Give This Album Some Personality! 🎤  🎶 : {root} 🎤  🎶")

            # check the existence of default files
            print(f"[cruix-music-archiver] checking if {default_cover} exists: {os.path.exists(default_cover)} ✅")
            print(f"[cruix-music-archiver] checking if {default_folder} exists: {os.path.exists(default_folder)} ✅")
            print(f"[cruix-music-archiver] checking write access to {root}: {os.access(root, os.W_OK)} ✅")

            # copy the cover.jpg file, overwriting if necessary
            if os.path.exists(default_cover):
                try:
                    shutil.copy(default_cover, os.path.join(root, "cover.jpg"))
                    print(
                        f"[cruix-music-archiver] Copied: cover.jpg For {root}. Now It's Shining Like a Grammy Winner! 🏆 ✨")
                except Exception as e:
                    print(f"[cruix-music-archiver] Error Copying cover.jpg to {root}: {e}  ❌ ")

            # copy the folder.jpg file, overwriting if necessary
            if os.path.exists(default_folder):
                try:
                    shutil.copy(default_folder, os.path.join(root, "folder.jpg"))
                    print(f"[cruix-music-archiver] Copied: folder.jpg For {root}. Folder Just Got a Major Glow-Up! 💫 🎵")
                except Exception as e:
                    print(f"[cruix-music-archiver] Error Copying folder.jpg to {root}: {e}  ❌ ")


if __name__ == "__main__":
    check_and_copy_images()