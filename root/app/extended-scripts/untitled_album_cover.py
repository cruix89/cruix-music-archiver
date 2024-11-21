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
                f"[cruix-music-archiver] 'untitled_album' detected, applying 'untitled_album' cover. time to give this album some personality! 🎤 🎶 : {root} 🎤 🎶")

            # verifica a existência dos arquivos padrão
            print(f"[cruix-music-archiver] checking if {default_cover} exists: {os.path.exists(default_cover)} ✅")
            print(f"[cruix-music-archiver] checking if {default_folder} exists: {os.path.exists(default_folder)} ✅")
            print(f"[cruix-music-archiver] checking write access to {root}: {os.access(root, os.W_OK)} ✅")

            # copia o arquivo cover.jpg, sobrescrevendo se necessário
            if os.path.exists(default_cover):
                try:
                    shutil.copy(default_cover, os.path.join(root, "cover.jpg"))
                    print(
                        f"[cruix-music-archiver] copied: cover.jpg for {root}. now it's shining like a Grammy winner! 🏆 ✨")
                except Exception as e:
                    print(f"[cruix-music-archiver] error copying cover.jpg to {root}: {e}")

            # copia o arquivo folder.jpg, sobrescrevendo se necessário
            if os.path.exists(default_folder):
                try:
                    shutil.copy(default_folder, os.path.join(root, "folder.jpg"))
                    print(f"[cruix-music-archiver] copied: folder.jpg for {root}. folder just got a major glow-up! 💫 🎵")
                except Exception as e:
                    print(f"[cruix-music-archiver] error copying folder.jpg to {root}: {e}")


if __name__ == "__main__":
    check_and_copy_images()