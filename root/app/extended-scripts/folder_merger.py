import os
import shutil


def normalize_folder_name(folder_name):
    """Normaliza o nome da pasta, removendo espaços e underscores."""
    return folder_name.replace(' ', '').replace('_', '').lower()


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

        if normalized_folder in folders:
            # Se uma pasta com o mesmo nome (normalizado) já existir,
            # move o conteúdo da pasta atual para a pasta existente
            target_folder = folders[normalized_folder]
            for item in os.listdir(folder_path):
                src_path = os.path.join(folder_path, item)
                dest_path = os.path.join(target_folder, item)

                # Mova o item para a pasta de destino, sobrescrevendo se necessário
                try:
                    if os.path.isdir(src_path):
                        shutil.move(src_path, dest_path)
                    else:
                        shutil.copy2(src_path, dest_path)  # Usa copy2 para manter os metadados
                    print(f'Movendo {src_path} para {dest_path}')
                except Exception as e:
                    print(f'Erro ao mover {src_path}: {e}')
        else:
            # Armazena o caminho da pasta original no dicionário
            folders[normalized_folder] = folder_path

print('Processo concluído.')