import os
import eyed3

# Caminho da pasta onde os arquivos MP3 estão armazenados
music_folder = '/music'


# Função para verificar e alterar a tag de disco
def update_tag_if_needed(file_path):
    try:
        # Carregar o arquivo MP3
        audio_file = eyed3.load(file_path)

        # Verificar se a tag de disco existe e obter o valor
        disk_tag = audio_file.tag.album_artist if audio_file.tag.album_artist else ""

        # Verificar se a tag de disco contém a palavra "na" ou está vazia
        if "na" in disk_tag.lower() or not disk_tag:
            # Se a condição for atendida, aplicar a tag "Various Songs"
            audio_file.tag.album_artist = "Various Songs"
            # Salvar as alterações
            audio_file.tag.save()
            print(f"[cruix-music-archiver] tag updated for: {file_path}")
    except Exception as e:
        print(f"[cruix-music-archiver] error to process {file_path}: {e}")


# Percorrer todos os arquivos na pasta /music
for root, dirs, files in os.walk(music_folder):
    for file in files:
        # Verificar se o arquivo é um MP3
        if file.lower().endswith('.mp3'):
            file_path = os.path.join(root, file)
            update_tag_if_needed(file_path)

print("[cruix-music-archiver] process done.")