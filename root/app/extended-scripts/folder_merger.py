import os
import shutil
import re

def normalize_folder_name(folder_name):
    """Normaliza o nome da pasta, removendo espaços, underscores e sufixos numéricos."""
    # Remove espaços e underscores, converte para minúsculas
    normalized_name = folder_name.replace(' ', '').replace('_', '').lower()
    # Remove sufixos no padrão "_número" (ex: "_1", "_2", etc.)
    normalized_name = re.sub(r'(_\d+)$', '', normalized_name)
    return normalized_name

# Define o diretório de downloads
downloads_dir = '/downloads'

# Cria um dicionário para armazenar pastas encontradas
folders = {}

# Percorre as pastas no diretório de downloads
for folder in os.listdir(downloads_dir):
    # Define o caminho completo da pasta
    folder_path = os.path.join(downloads_dir, folder)

    # Verifica se é uma pasta
    if os.path.isdir(folder_path):
        # Normaliza o nome da pasta para comparação
        normalized_folder = normalize_folder_name(folder)

        # Adiciona a pasta se ainda não existir no dicionário
        if normalized_folder not in folders:
            folders[normalized_folder] = folder_path
        else:
            # Se uma pasta com o mesmo nome normalizado já existir,
            # move o conteúdo da pasta atual para a pasta existente
            target_folder = folders[normalized_folder]

            # Certifique-se de que o diretório de destino existe
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            for item in os.listdir(folder_path):
                src_path = os.path.join(folder_path, item)
                dest_path = os.path.join(target_folder, item)

                # Se o item já existe na pasta de destino, ajuste o nome para evitar conflitos
                if os.path.exists(dest_path):
                    base_name, ext = os.path.splitext(item)
                    dest_path = os.path.join(target_folder, f"{base_name}_copy{ext}")

                # Mova o item para a pasta de destino, sobrescrevendo se necessário
                try:
                    if os.path.isdir(src_path):
                        shutil.move(src_path, dest_path)
                    else:
                        shutil.copy2(src_path, dest_path)  # Usa copy2 para manter os metadados
                    print(f'Movendo {src_path} para {dest_path}')
                except Exception as e:
                    print(f'Erro ao mover {src_path}: {e}')

            # Após mover o conteúdo, pode-se remover a pasta original vazia
            try:
                os.rmdir(folder_path)
                print(f'Removendo pasta vazia {folder_path}')
            except Exception as e:
                print(f'Erro ao remover pasta {folder_path}: {e}')

print('Processo concluído.')