import os


def fix_folders(base_path, substitutions_file):
    """
    Renames folders in a directory based on a substitution file.
    Each substitution is applied exhaustively before moving to the next.

    :param base_path: Path to the directory containing folders to be fixed.
    :param substitutions_file: Path to the file containing substitutions in the format 'old|new'.
    """
    # Read substitutions from the file
    with open(substitutions_file, 'r') as file:
        substitutions = [line.strip().split('|') for line in file if '|' in line]

    # Get the list of folders in the base directory
    folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]

    # Iterate over each substitution pair
    for old, new in substitutions:
        changes_made = True
        while changes_made:
            changes_made = False
            for folder_name in folders:
                if old in folder_name:
                    # Generate the new folder name by replacing 'old' with 'new'
                    new_folder_name = folder_name.replace(old, new)
                    # Rename the folder if the name has changed
                    if folder_name != new_folder_name:
                        os.rename(
                            os.path.join(base_path, folder_name),
                            os.path.join(base_path, new_folder_name)
                        )
                        print(f"[cruix-music-archiver] fixed: '{folder_name}' to '{new_folder_name}' ♻️")
                        changes_made = True
            # Update the folder list to reflect renamed folders
            folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]

    print("[cruix-music-archiver] artists' folders fixed successfully! ⚡  mission accomplished, folders upgraded! ⚡")


# Example of how to use the function
if __name__ == "__main__":
    # Path to the directory containing the folders to fix
    base_path = "/music"
    # Path to the file containing the substitutions
    substitutions_file = "/app/lists/artists_folders_fixer.txt"
    # Call the function to fix folders
    fix_folders(base_path, substitutions_file)