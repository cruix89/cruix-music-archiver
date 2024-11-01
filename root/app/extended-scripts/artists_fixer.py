import os
import logging
from mutagen.id3 import ID3
import mutagen.id3

# Define absolute paths for directories
LOGS_DIR = '/config/logs'
LISTS_DIR = '/app/lists'
MUSIC_DIR = '/music'

# Create directories if they do not exist
for path in [LOGS_DIR, LISTS_DIR, MUSIC_DIR]:
    if not os.path.exists(path):
        os.makedirs(path)

def load_characters(characters_path):
    absolute_path = os.path.abspath(characters_path)
    characters = []
    with open(absolute_path, 'r', encoding='utf-8') as f:
        for line in f:
            char = line.strip()  # Read single character from each line
            if char:  # Ensure it's not empty
                characters.append(char)
                logging.debug(f"Loaded character for removal: '{char}'")  # Log each loaded character
    return characters

def remove_characters_from_artist_tag(file_path, tag_class, tag_name, characters):
    try:
        logging.debug(f"Attempting to update artist tag in file: '{file_path}'")
        audiofile = ID3(file_path)  # Load the audio file
        current_tag = audiofile.get(tag_name)  # Get the current artist tag (TPE1)

        # Check if the artist tag exists
        if current_tag:
            current_tag_text = current_tag.text[0]
            logging.debug(f"Current artist tag text before removal: '{current_tag_text}'")

            # Remove specified characters from the current artist tag text
            for char in characters:
                current_tag_text = current_tag_text.replace(char, '')  # Remove the character

            current_tag_text = current_tag_text.strip()  # Strip any leading/trailing whitespace
            logging.debug(f"Modified artist tag text after removal: '{current_tag_text}'")

            # Update the artist tag only if it was modified
            if current_tag_text:
                audiofile[tag_name] = tag_class(encoding=3, text=current_tag_text)
                audiofile.save()
                logging.debug(f"Updated artist tag in '{file_path}' to '{current_tag_text}'")

    except FileNotFoundError as e:
        logging.error(f"Error updating artist tag in '{file_path}': {e}")
    except Exception as e:
        logging.error(f"Error updating artist tag in '{file_path}': {e}")

def main():
    logging.basicConfig(filename=os.path.join(LOGS_DIR, 'artists_fixer.log'),
                        level=logging.DEBUG)

    # Absolute path to the characters file
    characters_path = os.path.join(LISTS_DIR, 'characters.txt')  # Updated to reflect new file
    characters = load_characters(characters_path)

    logging.debug("Starting character removal for artist tags in files...")
    print("Removing specified characters from artist tags in files...")

    for dirpath, _, filenames in os.walk(MUSIC_DIR):
        for file_name in filenames:
            if file_name.endswith(".mp3"):
                file_path = os.path.join(dirpath, file_name)

                # Remove characters from artist tag only
                remove_characters_from_artist_tag(file_path, mutagen.id3.TPE1, 'TPE1', characters)

    logging.debug("Character removal from artist tags completed successfully.")
    print("Character removal from artist tags completed successfully.")

if __name__ == "__main__":
    main()