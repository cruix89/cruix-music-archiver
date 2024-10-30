import os
import eyed3
import logging

def setup_directories():
    try:
        music_directory = '/music'
        logs_directory = '/config/logs'
        lists_directory = '/app/lists'
        return music_directory, logs_directory, lists_directory
    except Exception as error:
        logging.error(f'error setting up directories: {error}\n')
        raise

def rename_file(file_path, new_file_path):
    try:
        # Converte o nome completo para letras minúsculas, mantendo a extensão original
        base, extension = os.path.splitext(new_file_path)
        new_file_name = base + extension
        os.rename(file_path, new_file_name)
    except Exception as error:
        logging.error(f'error renaming file: {error}\n')
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
                logging.info(f'file renamed: {file_path} -> {new_file_path}\n')

        for folder_name in dirs:
            old_folder_path = os.path.join(root, folder_name)
            formatted_folder_name = format_file_name(folder_name)
            new_folder_path = os.path.join(root, formatted_folder_name)
            if old_folder_path != new_folder_path:
                rename_file(old_folder_path, new_folder_path)
                logging.info(f'folder renamed: {old_folder_path} -> {new_folder_path}\n')

def update_tags_and_rename(directory, lowercase_terms):
    try:
        logging.info("formatting tags and directories...\n")
        for root, dirs, files in os.walk(directory, topdown=False):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                if is_mp3(file_name):
                    process_mp3_tags(file_path, lowercase_terms)

            rename_files_and_folders(root)

        logging.info("tags and directories formatted.\n")
    except Exception as error:
        logging.error(f'error formatting tags, files, and folders: {error}\n')
        raise

# CONFIGURE LOGGING
try:
    music_dir, logs_dir, lists_dir = setup_directories()
    log_path = os.path.join(logs_dir, 'capitalize_tags_files_and_folders.log')
    logging.basicConfig(filename=log_path, level=logging.INFO)
except Exception as e:
    print(f'error setting up logging: {e}\n')
    raise

# LOAD LIST OF TERMS TO KEEP LOWERCASE
try:
    with open(os.path.join(lists_dir, 'keep_lowercase.txt'), 'r') as f:
        lowercase_terms_list = f.read().splitlines()
except Exception as e:
    logging.error(f'error loading list of lowercase terms: {e}\n')
    raise

# NOTIFY START OF PROCESS
print("\nstarting the MP3 tag formatting and file renaming process...")

# PROCESS MUSIC DIRECTORY
try:
    update_tags_and_rename(music_dir, lowercase_terms_list)
except Exception as e:
    logging.error(f'error executing script: {e}\n')
    raise

# NOTIFY END OF PROCESS
print("MP3 tag formatting and file renaming process completed successfully.")