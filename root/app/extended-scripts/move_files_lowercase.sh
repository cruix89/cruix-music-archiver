#!/usr/bin/with-contenv bash

SOURCE_DIR="/downloads"
DEST_DIR="/config/cache"
CACHE_FILE="/config/mover_cache.txt"

# Define the excluded folders
excluded_folders=('.stfolder' '.stversions' '.thumbnails')

# Create the cache file if it doesn't exist
if [[ ! -f "$CACHE_FILE" ]]; then
    touch "$CACHE_FILE"
fi

normalize_path() {
    # Convert the path to lowercase and replace spaces with underscores
    echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/ /_/g'
}

copy_files() {
    mkdir -p "$DEST_DIR"

    find "$SOURCE_DIR" -mindepth 1 | while read -r item; do
        # Check if the current item's path starts with any of the excluded folders
        for excluded in "${excluded_folders[@]}"; do
            if [[ "$item" == "$SOURCE_DIR/$excluded"* ]]; then
                echo "Skipped: '$item' is in the excluded folders."
                continue 2
            fi
        done

        # Normalize the path to lowercase and underscores
        relative_path="${item//$SOURCE_DIR\//}"
        normalized_path="$(normalize_path "$relative_path")"
        dest_path="$DEST_DIR/$normalized_path"

        # Check if the file is already in the cache
        if grep -qx "$item" "$CACHE_FILE"; then
            echo "Skipped: '$item' already copied."
            continue
        fi

        # Check if a directory with a normalized name already exists
        if [[ -d "$dest_path" || -f "$dest_path" ]]; then
            echo "Merging: '$item' into existing directory '$dest_path'."
        fi

        mkdir -p "$(dirname "$dest_path")"

        if [[ -f "$item" ]]; then
            # Move the file and check if it was successful
            if mv "$item" "$dest_path"; then
                # Add the item to the cache
                echo "$item" >> "$CACHE_FILE"
                echo "Successfully moved '$item' to '$dest_path'."
            else
                echo "Error moving '$item' to '$dest_path'."
            fi
        elif [[ -d "$item" ]]; then
            # Merge directories if it's a folder
            if mv "$item"/* "$dest_path"/ 2>/dev/null; then
                echo "Successfully merged directory '$item' into '$dest_path'."
                rmdir "$item" 2>/dev/null # Remove the directory if it's empty
            else
                echo "Error merging directory '$item' into '$dest_path'."
            fi
        fi
    done
}

copy_files