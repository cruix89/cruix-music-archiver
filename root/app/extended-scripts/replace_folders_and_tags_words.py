import os
import logging
from mutagen.easyid3 import EasyID3
import re
import time
from pathlib import Path
from typing import Dict, Tuple  # Removed Optional


def setup_logging(log_file: Path, logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(str(log_file))  # Convert to string for FileHandler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def load_replacements(file_path: Path) -> Dict[str, Tuple[str, str]]:
    replacements = {}
    try:
        with file_path.open('r', encoding='utf-8') as file:
            for line in file:
                if '|' in line:
                    old, new = line.strip().split('|')
                    replacements[old.lower()] = (old, new)
                else:
                    logging.warning(f'Invalid line in replacements file: {line.strip()}')
    except FileNotFoundError:
        logging.error(f'Replacements file not found: {file_path}')
    except Exception as e:
        logging.error(f'Error loading replacements: {e}')
    logging.debug(f'Replacements loaded: {replacements}')
    return replacements


def format_name(name: str, replacements: Dict[str, Tuple[str, str]]) -> str:
    name = name.replace('_', ' ')
    for old_lower, (old, new) in replacements.items():
        pattern = r'\b' + re.escape(old) + r'\b'
        name = re.sub(pattern, new, name, flags=re.IGNORECASE)
    name = name.replace(' ', '_')
    logging.debug(f'Formatted name: {name}')
    return name


def rename_directories_and_format_tags(directory: Path, replacements: Dict[str, Tuple[str, str]], max_retries: int = 99, pause: int = 30):
    for root, dirs, files in os.walk(str(directory)):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            new_dir_name = format_name(dir_name, replacements)
            new_dir_path = dir_path.parent / new_dir_name

            logging.debug(f'Attempting to rename directory: {dir_path} to {new_dir_path}')
            if new_dir_name != dir_name:
                for attempt in range(max_retries):
                    try:
                        os.rename(dir_path, new_dir_path)
                        logging.info(f'Directory renamed: {dir_path} -> {new_dir_path}')
                        break
                    except PermissionError as e:
                        logging.warning(f'Error renaming {dir_path} -> {new_dir_path}: {e}. Attempt {attempt + 1}/{max_retries}')
                        time.sleep(pause)
                    except Exception as e:
                        logging.error(f'Error renaming {dir_path} -> {new_dir_path}: {e}')
                        break
                else:
                    logging.error(f'Failed to rename {dir_path} -> {new_dir_path} after {max_retries} attempts')
            else:
                logging.debug(f'No change in directory name for: {dir_path}')

        for file_name in files:
            if file_name.endswith('.mp3'):
                file_path = Path(root) / file_name
                try:
                    tags = EasyID3(file_path)
                    for tag in tags:
                        tags[tag] = format_name(tags[tag][0], replacements)
                    tags.save()
                    logging.info(f'Tags formatted: {file_path}')
                except Exception as e:
                    logging.error(f'Error formatting tags of file {file_path}: {e}')


def setup_directories() -> Tuple[Path, Path, Path]:
    logs_dir = Path('/config/logs')
    lists_dir = Path('/app/lists')
    music_dir = Path('/downloads')

    logs_dir.mkdir(parents=True, exist_ok=True)
    lists_dir.mkdir(parents=True, exist_ok=True)

    return logs_dir, lists_dir, music_dir


def main():
    print("Running directory and tag formatting...")

    logs_dir, lists_dir, music_dir = setup_directories()

    log_file_rename = logs_dir / 'replace_folders_and_tags_words_1.log'
    log_file_format = logs_dir / 'replace_folders_and_tags_words_2.log'
    logger_rename = setup_logging(log_file_rename, 'rename')
    logger_format = setup_logging(log_file_format, 'format')

    replacements = load_replacements(lists_dir / 'replace.txt')
    if not replacements:
        logger_rename.warning("No replacements loaded. Check the replacements file.")
        logger_format.warning("No replacements loaded. Check the replacements file.")
        return

    if music_dir.exists():
        rename_directories_and_format_tags(music_dir, replacements)
        print("\nDirectories and tags formatted.")
    else:
        logger_rename.error(f'Music directory not found: {music_dir}')
        logger_format.error(f'Music directory not found: {music_dir}')
        return

    print("Directory and tag formatting completed successfully.")


if __name__ == "__main__":
    main()