import os
import eyed3
import logging
from eyed3.id3 import ID3_V2_4

# define the paths for logs and music directories
logs_dir = '/config/logs'
music_dir = '/downloads'

# create logging directory if it doesn't exist
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# set up logging
log_file = os.path.join(logs_dir, 'replace_folders_and_tags_accents.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Logger is set up successfully.")

def format_name(name, substitutions_list):
    formatted_name = name
    for source, target in substitutions_list:
        formatted_name = formatted_name.replace(source, target)
    return formatted_name

def rename_file(old_path, new_path):
    if old_path != new_path:
        try:
            os.rename(old_path, new_path)
            logging.info(f'Formatted file: {old_path} -> {new_path}')
        except Exception as e:
            logging.error(f'Error renaming file: {old_path} -> {new_path}: {e}')

def rename_image(old_path, new_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    for ext in image_extensions:
        old_image_path = old_path.replace('.mp3', ext)
        new_image_path = new_path.replace('.mp3', ext)
        if os.path.exists(old_image_path) and old_image_path != new_image_path:
            rename_file(old_image_path, new_image_path)

def change_tags_and_rename_file(substitutions_list):
    for root, dirs, files in os.walk(music_dir):
        for file_name in files:
            if file_name.endswith('.mp3'):
                file_path = os.path.join(root, file_name)
                try:
                    logging.info(f'Trying to load file: {file_path}')
                    audiofile = eyed3.load(file_path)
                    if audiofile.tag is not None:
                        logging.info(f'Loaded tags for file: {file_path}')
                        changes_made = False

                        if audiofile.tag.title:
                            new_title = format_name(audiofile.tag.title, substitutions_list)
                            if new_title != audiofile.tag.title:
                                audiofile.tag.title = new_title
                                changes_made = True
                                logging.info(f'Title changed: {audiofile.tag.title} -> {new_title}')
                        if audiofile.tag.album:
                            new_album = format_name(audiofile.tag.album, substitutions_list)
                            if new_album != audiofile.tag.album:
                                audiofile.tag.album = new_album
                                changes_made = True
                                logging.info(f'Album changed: {audiofile.tag.album} -> {new_album}')
                        if audiofile.tag.artist:
                            new_artist = format_name(audiofile.tag.artist, substitutions_list)
                            if new_artist != audiofile.tag.artist:
                                audiofile.tag.artist = new_artist
                                changes_made = True
                                logging.info(f'Artist changed: {audiofile.tag.artist} -> {new_artist}')
                        if audiofile.tag.album_artist:
                            new_album_artist = format_name(audiofile.tag.album_artist, substitutions_list)
                            if new_album_artist != audiofile.tag.album_artist:
                                audiofile.tag.album_artist = new_album_artist
                                changes_made = True
                                logging.info(f'Album artist changed: {audiofile.tag.album_artist} -> {new_album_artist}')
                        if audiofile.tag.genre and audiofile.tag.genre.name:
                            new_genre = format_name(audiofile.tag.genre.name, substitutions_list)
                            if new_genre != audiofile.tag.genre.name:
                                audiofile.tag.genre = new_genre
                                changes_made = True
                                logging.info(f'Genre changed: {audiofile.tag.genre.name} -> {new_genre}')

                        if changes_made:
                            audiofile.tag.save(version=ID3_V2_4)

                        new_file_name = format_name(file_name, substitutions_list)
                        new_file_path = os.path.join(root, new_file_name)
                        rename_file(file_path, new_file_path)
                        rename_image(file_path, new_file_path)
                    else:
                        logging.warning(f'No tag found in file: {file_path}')
                except Exception as e:
                    logging.error(f'Error formatting file {file_path}: {e}')

def rename_directories(directory, substitutions_list):
    for root, dirs, _ in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if os.path.exists(dir_path):
                new_dir_name = format_name(dir_name, substitutions_list)
                new_dir_path = os.path.join(root, new_dir_name)
                if dir_path != new_dir_path:
                    try:
                        os.rename(dir_path, new_dir_path)
                        logging.info(f'Formatted directory: {dir_path} -> {new_dir_path}')
                    except Exception as e:
                        logging.error(f'Error renaming directory {dir_path}: {e}')

# list of substitutions for accents
accent_substitutions = [("É", "é"), ("Á", "á"), ("À", "à"), ("Ó", "ó")]

# process mp3 files and their tags
change_tags_and_rename_file(accent_substitutions)

# process directories
if os.path.exists(music_dir):
    logging.info(f'Music directory found: {music_dir}')
    rename_directories(music_dir, accent_substitutions)
else:
    logging.error(f'The directory {music_dir} does not exist.')

print("\nAccents formatted successfully.")