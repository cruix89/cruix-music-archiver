import os
import eyed3
import logging
import shutil


def setup_directories():
    try:
        music_directory = '/music'
        logs_directory = '/config/logs'
        lists_directory = '/app/lists'
        cache_directory = '/config/cache'
        return music_directory, logs_directory, lists_directory, cache_directory
    except Exception as error:
        logging.error(f'error setting up directories: {error}')
        raise


def rename_file(file_path, new_file_path):
    try:
        base, extension = os.path.splitext(new_file_path)
        new_file_name = base + extension

        counter = 1
        while os.path.exists(new_file_name):
            new_file_name = f"{base}_copy{counter}{extension}"
            counter += 1

        os.rename(file_path, new_file_name)
    except Exception as error:
        logging.error(f'error renaming file: {error}')
        raise


def is_mp3(file_name):
    return file_name.lower().endswith('.mp3')


def capitalize_words(text, lowercase_terms):
    words = text.split()
    formatted_words = []
    for i, word in enumerate(words):
        if word.startswith('(') and len(word) > 1:
            formatted_word = '(' + word[1:].capitalize()
            formatted_words.append(formatted_word)
        elif i == 0 or words[i - 1].endswith('(') or word.lower() not in lowercase_terms:
            formatted_words.append(word.capitalize())
        else:
            formatted_words.append(word.lower())
    return ' '.join(formatted_words)


def format_name(name, lowercase_terms):
    if name:
        return capitalize_words(name, lowercase_terms)
    return name


def format_file_name(name):
    if name:
        return name.lower()
    return name


def process_mp3_tags(file_path, lowercase_terms):
    audiofile = eyed3.load(file_path)
    if audiofile is None or audiofile.tag is None:
        return

    audiofile.tag.title = format_name(audiofile.tag.title, lowercase_terms)
    audiofile.tag.album = format_name(audiofile.tag.album, lowercase_terms)
    audiofile.tag.artist = format_name(audiofile.tag.artist, lowercase_terms)
    if audiofile.tag.album_artist:
        audiofile.tag.album_artist = format_name(audiofile.tag.album_artist, lowercase_terms)
    audiofile.tag.save()


def rename_files_and_folders(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            new_file_name = format_file_name(file_name)
            new_file_path = os.path.join(root, new_file_name)
            if file_path != new_file_path:
                rename_file(file_path, new_file_path)
                logging.info(f'file renamed: {file_path} -> {new_file_path}')

        for folder_name in dirs:
            old_folder_path = os.path.join(root, folder_name)
            formatted_folder_name = format_file_name(folder_name)
            new_folder_path = os.path.join(root, formatted_folder_name)
            if old_folder_path != new_folder_path:
                rename_file(old_folder_path, new_folder_path)
                logging.info(f'folder renamed: {old_folder_path} -> {new_folder_path}')


def merge_folders_with_cache(base_directory, cache_directory='/config/cache'):
    try:
        logging.info("merging duplicate folders using cache...")

        # Dicionário para mapear diretórios com nomes iguais, considerando o sufixo '_copy'
        folder_map = {}

        # Identificando pastas duplicadas
        for root, dirs, _ in os.walk(base_directory, topdown=False):
            for folder_name in dirs:
                base_name = folder_name.split('_copy')[0]  # Remover sufixo '_copy' para comparar
                folder_map.setdefault(base_name, []).append(os.path.join(root, folder_name))

        # Para cada grupo de pastas duplicadas, cria o diretório único no cache e move o conteúdo
        for base_name, folder_group in folder_map.items():
            if len(folder_group) > 1:
                # Criar diretório único no cache
                target_cache_folder = os.path.join(cache_directory, base_name)

                if not os.path.exists(target_cache_folder):
                    os.makedirs(target_cache_folder)

                for folder_path in folder_group:
                    for item in os.listdir(folder_path):
                        source_path = os.path.join(folder_path, item)
                        target_path = os.path.join(target_cache_folder, item)

                        # Se o destino já existir, substituir o arquivo ou mesclar as pastas
                        if os.path.exists(target_path):
                            if os.path.isfile(source_path):
                                os.remove(target_path)  # Remove o arquivo existente
                                shutil.move(source_path, target_path)
                            elif os.path.isdir(source_path):
                                merge_folders_with_cache(source_path, target_cache_folder)
                        else:
                            shutil.move(source_path, target_path)

                    # Remover o diretório original após mover seu conteúdo
                    os.rmdir(folder_path)

                # Mover a pasta mesclada de volta para o diretório de origem
                final_target_folder = os.path.join(base_directory, base_name)
                if os.path.exists(final_target_folder):
                    shutil.rmtree(final_target_folder)  # Remover se já existir
                shutil.move(target_cache_folder, final_target_folder)

        logging.info("duplicate folders merged successfully using cache.")
    except Exception as error:
        logging.error(f"error merging folders using cache: {error}")
        raise


def update_tags_and_rename(directory, lowercase_terms):
    try:
        logging.info("formatting tags and directories...")
        for root, dirs, files in os.walk(directory, topdown=False):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                if is_mp3(file_name):
                    process_mp3_tags(file_path, lowercase_terms)

            rename_files_and_folders(root)

        logging.info("tags and directories formatted.")
    except Exception as error:
        logging.error(f'error formatting tags, files, and folders: {error}')
        raise


# CONFIGURE LOGGING
try:
    music_dir, logs_dir, lists_dir, cache_dir = setup_directories()
    log_path = os.path.join(logs_dir, 'capitalize_tags_files_and_folders.log')
    logging.basicConfig(filename=log_path, level=logging.INFO)
except Exception as e:
    print(f'[cruix-music-archiver] error setting up logging: 😱  oh no! something went horribly wrong — {e}')
    raise

# LOAD LIST OF TERMS TO KEEP LOWERCASE
try:
    with open(os.path.join(lists_dir, 'keep_lowercase.txt'), 'r') as f:
        lowercase_terms_list = f.read().splitlines()
except Exception as e:
    logging.error(f'error loading list of lowercase terms: {e}')
    raise

# NOTIFY START OF PROCESS
print("[cruix-music-archiver] starting the mp3 tag formatting and file renaming process... 🎶  💥  let the transformation begin!")

# PROCESS MUSIC DIRECTORY
try:
    update_tags_and_rename(music_dir, lowercase_terms_list)
    merge_folders_with_cache(music_dir, cache_dir)  # Merge folders using cache
except Exception as e:
    logging.error(f'error executing script: {e}')
    raise

# NOTIFY END OF PROCESS
print("[cruix-music-archiver] mp3 tag formatting and file renaming process completed successfully... 🎉  your files are now perfectly organized and ready to shine!")