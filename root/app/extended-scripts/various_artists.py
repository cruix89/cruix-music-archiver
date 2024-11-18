import os
import shutil

# caminhos absolutos
music_directory = "/music"
default_images_directory = "/app/various-artists"
default_cover = os.path.join(default_images_directory, "cover.jpg")
default_folder = os.path.join(default_images_directory, "folder.jpg")

def check_and_copy_images():
    # percorre apenas os subdiretórios de /music
    for root, dirs, files in os.walk(music_directory):
        # ignora o diretório raiz /music
        if root == music_directory:
            continue

        # verifica se os arquivos cover.jpg ou folder.jpg existem no subdiretório atual
        has_cover = "cover.jpg" in files
        has_folder = "folder.jpg" in files

        # se ambos estiverem ausentes, copia as imagens padrão
        if not has_cover and not has_folder:
            print(f"[cruix-music-archiver] artist not found in database, applying various artists cover : {root}")
            if os.path.exists(default_cover):
                shutil.copy(default_cover, os.path.join(root, "cover.jpg"))
                print(f"[cruix-music-archiver] copied: cover.jpg for {root}")
            if os.path.exists(default_folder):
                shutil.copy(default_folder, os.path.join(root, "folder.jpg"))
                print(f"[cruix-music-archiver] copied: folder.jpg for {root}")

if __name__ == "__main__":
    check_and_copy_images()