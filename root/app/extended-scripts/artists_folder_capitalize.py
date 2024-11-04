import os

# Define o diretório de música
music_dir = '/music'

# Percorre todos os itens no diretório de música
for item in os.listdir(music_dir):
    item_path = os.path.join(music_dir, item)

    # Verifica se o item é um diretório
    if os.path.isdir(item_path):
        # Capitaliza o nome do diretório
        capitalized_name = item.title()
        capitalized_path = os.path.join(music_dir, capitalized_name)

        # Renomeia o diretório
        if item != capitalized_name:  # Evita renomeações desnecessárias
            os.rename(item_path, capitalized_path)
            print(f'renamed: {item} -> {capitalized_name}')