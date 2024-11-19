import os
import eyed3

# Caminho da pasta onde os arquivos MP3 estão armazenados
music_folder = '/music'


# Função para verificar e alterar a tag de álbum
def update_tag_if_needed(mp3_file_path):
    try:
        # Carregar o arquivo MP3
        audio_file = eyed3.load(mp3_file_path)

        # Verificar se a tag de álbum existe e obter o valor
        album_tag = audio_file.tag.album if audio_file.tag.album else ""

        # Verificar se a tag de álbum contém a palavra "na" ou está vazia
        if "na" in album_tag.lower() or not album_tag:
            # Se a condição for atendida, aplicar a tag "Various Songs"
            audio_file.tag.album = "Various Songs"
            # Salvar as alterações
            audio_file.tag.save()
            print(f"[cruix-music-archiver] 🛠️  tag updated for {mp3_file_path}. it's like a software patch, but for your music collection! 🎧")
    except Exception as e:
        print(f"[cruix-music-archiver] 🚨  error to process {mp3_file_path}: {e}. it's like we hit a '404' in the music universe! 🌌")


# Percorrer todos os arquivos na pasta /music
for root, dirs, files in os.walk(music_folder):
    for file in files:
        # Verificar se o arquivo é um MP3
        if file.lower().endswith('.mp3'):
            file_path_in_directory = os.path.join(root, file)
            update_tag_if_needed(file_path_in_directory)

print("[cruix-music-archiver] ✅  process done! like a true hero in the digital world! 🦸‍♂️")