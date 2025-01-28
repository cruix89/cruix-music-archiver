import os
import eyed3

# path of the folder where the MP3 files are stored
music_folder = '/music'

# function to check and change album tag
def update_tag_if_needed(mp3_file_path):
    try:
        # upload the MP3 file
        audio_file = eyed3.load(mp3_file_path)

        # check if the album tag exists and get the value
        album_tag = audio_file.tag.album if audio_file.tag.album else ""

        # check if the album tag is exactly "na" or is empty
        if album_tag.strip().lower() == "na" or not album_tag:
            # if the condition is met, apply the "Youtube Tracks" tag
            audio_file.tag.album = "Youtube Tracks"
            # save changes
            audio_file.tag.save()
            print(f"[cruix-music-archiver] Tag Updated For {mp3_file_path}. It's Like a Software Patch, But For Your Music Collection! 🎧")
    except Exception as e:
        print(f"[cruix-music-archiver] Error to Process {mp3_file_path}: {e}. It's Like We Hit a '404' In the Music Universe! 🌌")


# browse all files in the /music folder
for root, dirs, files in os.walk(music_folder):
    for file in files:
        # check if the file is an MP3
        if file.lower().endswith('.mp3'):
            file_path_in_directory = os.path.join(root, file)
            update_tag_if_needed(file_path_in_directory)