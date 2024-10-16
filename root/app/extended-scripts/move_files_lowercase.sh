#!/usr/bin/with-contenv bash

SOURCE_DIR="/downloads"
DEST_DIR="/config/cache"
CACHE_FILE="/config/mover_cache.txt"

# Função para normalizar os caminhos (minúsculas e underscores nos espaços)
normalize_path() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/ /_/g'
}

# Verifica se o arquivo de cache existe, se não existir cria
if [[ ! -f "$CACHE_FILE" ]]; then
    touch "$CACHE_FILE"
fi

# Função principal que executa o loop de cópia
process_files() {
    while IFS= read -r -d '' item; do
        # Verifica se o arquivo já está no cache
        if grep -qx "$item" "$CACHE_FILE"; then
            echo "Skipped: '$item' already processed."
            continue
        fi

        # Normaliza o caminho e define o caminho no diretório de destino
        relative_path="${item//$SOURCE_DIR\//}"
        normalized_path="$(normalize_path "$relative_path")"
        dest_path="$DEST_DIR/$normalized_path"

        # Cria a estrutura de diretórios capitalizada no destino
        mkdir -p "$(dirname "$dest_path")"

        # Copia o arquivo para o destino
        if cp "$item" "$dest_path"; then
            # Verifica se os arquivos têm o mesmo tamanho
            source_size=$(stat -c%s "$item")
            dest_size=$(stat -c%s "$dest_path")

            if [[ "$source_size" -eq "$dest_size" ]]; then
                echo "Successfully copied '$item' to '$dest_path'."

                # Adiciona ao arquivo de cache
                echo "$item" >> "$CACHE_FILE"

                # Remove o arquivo da origem
                rm "$item"

                # Verifica se a estrutura do caminho no destino existe na origem
                if [[ ! -d "$SOURCE_DIR/$(dirname "$relative_path")" ]]; then
                    echo "Recreating missing directory structure in source."
                    mkdir -p "$SOURCE_DIR/$(dirname "$relative_path")"
                    cp "$dest_path" "$SOURCE_DIR/$(dirname "$relative_path")/"
                else
                    # Copia de volta sem recriar diretórios
                    echo "Directory already exists, copying file back."
                    cp "$dest_path" "$SOURCE_DIR/$(dirname "$relative_path")/"
                fi

                # Verifica o tamanho novamente ao copiar de volta para downloads
                back_copy_path="$SOURCE_DIR/$(dirname "$relative_path")/$(basename "$dest_path")"
                back_copy_size=$(stat -c%s "$back_copy_path")

                if [[ "$dest_size" -eq "$back_copy_size" ]]; then
                    echo "Successfully copied back '$dest_path' to '$back_copy_path'."
                    rm "$dest_path" # Exclui o arquivo do cache
                else
                    echo "Error: File sizes do not match after copying back."
                    continue
                fi
            else
                echo "Error: File sizes do not match, skipping '$item'."
                continue
            fi
        else
            echo "Error copying '$item' to '$dest_path'."
            continue
        fi
    done < <(find "$SOURCE_DIR" -mindepth 1 -type f -print0)
}

# Executa o loop até que todos os arquivos tenham sido processados
while true; do
    process_files

    # Verifica se ainda há arquivos para processar
    remaining_files=$(find "$SOURCE_DIR" -mindepth 1 -type f | wc -l)
    if [[ "$remaining_files" -eq 0 ]]; then
        echo "All files have been processed."
        break
    fi

    sleep 1
done