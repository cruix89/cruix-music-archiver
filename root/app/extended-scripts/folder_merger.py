import os
import shutil
import re

print("merging folders...")

def normalize_folder_name(folder_name):
    """Normaliza o nome da pasta, removendo espaços, underscores e sufixos numéricos, convertendo para minúsculas."""
    normalized_name = folder_name.replace('__', '_').replace('_', ' ').lower()  # Substitui underscores por espaços
    normalized_name = re.sub(r'\s\d+$', '', normalized_name)  # Remove sufixos numéricos no final
    return normalized_name

# Define o diretório de downloads e o diretório de cache
downloads_dir = '/downloads'
cache_dir = '/config/cache'

# Cria um dicionário para armazenar pastas normalizadas encontradas
folders = {}

# Percorre as pastas no diretório de downloads
for folder in os.listdir(downloads_dir):
    folder_path = os.path.join(downloads_dir, folder)

    # Verifica se é uma pasta
    if os.path.isdir(folder_path):
        # Normaliza o nome da pasta para comparação
        normalized_folder = normalize_folder_name(folder)

        # Se a pasta normalizada já existir, mova os arquivos para a pasta existente
        if normalized_folder in folders:
            target_folder = folders[normalized_folder]
        else:
            # Se a pasta normalizada não existir, crie um novo diretório na pasta de cache
            normalized_folder_path = os.path.join(cache_dir, normalized_folder)
            os.makedirs(normalized_folder_path, exist_ok=True)
            folders[normalized_folder] = normalized_folder_path
            target_folder = normalized_folder_path

        # Mover os arquivos da pasta original para a pasta de cache
        for item in os.listdir(folder_path):
            src_path = os.path.join(folder_path, item)
            dest_path = os.path.join(target_folder, item)

            # Se o item já existe na pasta de destino, ajuste o nome para evitar conflitos
            count = 1
            base_name, ext = os.path.splitext(item)
            while os.path.exists(dest_path):
                dest_path = os.path.join(target_folder, f"{base_name}_copy_{count}{ext}")
                count += 1

            # Mova o arquivo ou diretório
            shutil.move(src_path, dest_path)

        # Remove a pasta original
        try:
            os.rmdir(folder_path)
            print(f'Removendo pasta vazia {folder_path}')
        except Exception as e:
            print(f'Erro ao remover pasta {folder_path}: {e}')

print('Processo concluído.')