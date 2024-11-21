import os
import shutil

# caminhos absolutos
music_directory = "/music"
default_images_directory = "/app/default-covers/untitled-album"
default_cover = os.path.join(default_images_directory, "cover.jpg")
default_folder = os.path.join(default_images_directory, "folder.jpg")


def check_and_copy_images():
    # percorre a estrutura de diretórios de forma bottom-up
    for root, dirs, files in os.walk(music_directory, topdown=False):
        # verifica se o nome do diretório atual é "untitled_album"
        if os.path.basename(root) == "untitled_album":
            print(
                f"[cruix-music-archiver] 'untitled_album' detected, applying 'Various Artists' cover. time to give this album some personality! 🎤 🎶 : {root}")

            # copia o arquivo cover.jpg, sobrescrevendo se necessário
            if os.path.exists(default_cover):
                shutil.copy(default_cover, os.path.join(root, "cover.jpg"))
                print(
                    f"[cruix-music-archiver] copied: cover.jpg for {root}. now it's shining like a Grammy winner! 🏆 ✨")

            # copia o arquivo folder.jpg, sobrescrevendo se necessário
            if os.path.exists(default_folder):
                shutil.copy(default_folder, os.path.join(root, "folder.jpg"))
                print(f"[cruix-music-archiver] copied: folder.jpg for {root}. folder just got a major glow-up! 💫 🎵")


if __name__ == "__main__":
    check_and_copy_images()