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

copy_files() {
    mkdir -p "$DEST_DIR"

    find "$SOURCE_DIR" -mindepth 1 | while read -r item; do
        # Get the basename of the current item
        base_name="$(basename "$item")"

        # Check if the current item is in the excluded folders
        if printf '%s\n' "${excluded_folders[@]}" | grep -q -x "$base_name"; then
            echo "Skipped: '$item' is in the excluded folders."
            continue
        fi

        relative_path="${item//$SOURCE_DIR\//}"
        lowercase_path="$(echo "$relative_path" | tr '[:upper:]' '[:lower:]')"
        dest_path="$DEST_DIR/$lowercase_path"

        # Check if the file is already in the cache
        if grep -qx "$item" "$CACHE_FILE"; then
            echo "Skipped: '$item' already copied."
            continue
        fi

        mkdir -p "$(dirname "$dest_path")"

        if [[ -f "$item" ]]; then
            # Copy the file and check if it was successful
            if cp "$item" "$dest_path"; then
                # Check if the file exists at the destination and compare sizes
                if [[ -f "$dest_path" ]]; then
                    original_size=$(stat -c%s "$item")
                    dest_size=$(stat -c%s "$dest_path")

                    if [[ "$original_size" -eq "$dest_size" ]]; then
                        echo "Successfully copied '$item' to '$dest_path'."
                        # Remove original file if the copy was successful and sizes match
                        rm "$item"
                        # Add the item to the cache
                        echo "$item" >> "$CACHE_FILE"
                    else
                        echo "Error: File sizes do not match. Keeping original '$item'."
                    fi
                else
                    echo "Error: File '$dest_path' does not exist after copy. Keeping original '$item'."
                fi
            else
                echo "Error copying '$item' to '$dest_path'."
            fi
        fi
    done
}

copy_files

find "$DEST_DIR" -mindepth 1 | while read -r item; do
    # Get the basename of the current item
    base_name="$(basename "$item")"

    # Check if the current item is in the excluded folders
    if printf '%s\n' "${excluded_folders[@]}" | grep -q -x "$base_name"; then
        echo "Skipped: '$item' is in the excluded folders."
        continue
    fi

    relative_path="${item//$DEST_DIR\//}"
    dest_path="$SOURCE_DIR/$relative_path"

    mkdir -p "$(dirname "$dest_path")"

    if [[ -f "$item" ]]; then
        # Check if the file is already in the cache before copying back
        if grep -qx "$item" "$CACHE_FILE"; then
            echo "Skipped: '$item' already copied back."
            continue
        fi

        # Copy the file back and check if it was successful
        if cp "$item" "$dest_path"; then
            # Check if the file exists at the source and compare sizes
            if [[ -f "$dest_path" ]]; then
                original_size=$(stat -c%s "$item")
                dest_size=$(stat -c%s "$dest_path")

                if [[ "$original_size" -eq "$dest_size" ]]; then
                    echo "Successfully copied '$item' back to '$dest_path'."
                    # Remove original file if the copy was successful and sizes match
                    rm "$item"
                    # Add the item to the cache
                    echo "$item" >> "$CACHE_FILE"
                else
                    echo "Error: File sizes do not match after copying back. Keeping original '$item'."
                fi
            else
                echo "Error: File '$dest_path' does not exist after copying back. Keeping original '$item'."
            fi
        else
            echo "Error copying '$item' back to '$dest_path'."
        fi
    fi
done