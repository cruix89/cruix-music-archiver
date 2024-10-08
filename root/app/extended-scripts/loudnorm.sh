#!/usr/bin/with-contenv bash

# Configurações de variáveis de ambiente
normalized_lockfile=${normalized_lockfile:-false}
normalized_debug=${normalized_debug:-false}
normalized_interval=${normalized_interval:-false}
normalized_cache_dir=${normalized_cache_dir:-"/config/cache"}
normalized_log_dir=${normalized_log_dir:-"/config/logs"}
normalized_list_file=${normalized_list_file:-"/config/loudnorm_cache.txt"}

if $normalized_debug; then normalized_args_verbose=true; else normalized_args_verbose=false; fi

# Função para verificar se ffmpeg está instalado
check_ffmpeg() {
    if ! command -v ffmpeg &> /dev/null; then
        echo "FFMPEG NÃO ESTÁ INSTALADO OU NÃO ESTÁ DISPONÍVEL NO CAMINHO."
        exit 1
    fi
}

# Função para carregar a lista de arquivos normalizados
load_normalized_list() {
    if [[ ! -f $normalized_list_file ]]; then
        touch $normalized_list_file
    fi
    mapfile -t normalized_files < $normalized_list_file
}

# Função para salvar na lista de normalizados
save_to_normalized_list() {
    echo "$1" >> $normalized_list_file
}

# Função para processar arquivo de áudio
process_file() {
    local src_file="$1"
    local log_file="$2"
    local output_file_mp3="$normalized_cache_dir/$(basename "${src_file%.*}.mp3")"

    # Criar diretório de cache se não existir
    mkdir -p "$normalized_cache_dir"

    # Comando FFMPEG
    ffmpeg -y -i "$src_file" -af "loudnorm=I=-14:TP=-1:LRA=11:print_format=summary" -b:a 320k "$output_file_mp3" &>> "$log_file"

    # Verificar se o arquivo de saída existe
    if [[ -f "$output_file_mp3" ]]; then
        save_to_normalized_list "$src_file"

        # Remover arquivo de origem
        rm "$src_file"

        # Mover arquivo do cache para o local original
        mv "$output_file_mp3" "$src_file"
        echo "Processado e movido: $src_file"
    else
        echo "ERRO AO PROCESSAR O ARQUIVO: $src_file" >> "$log_file"
    fi
}

# Função principal
main() {
    check_ffmpeg
    load_normalized_list

    local log_file="$normalized_log_dir/loudnorm.log"
    local audio_files=()
    local skipped_files=0

    # Coletar todos os arquivos de áudio
    while IFS= read -r -d '' file; do
        audio_files+=("$file")
    done < <(find "/downloads" -type f \( -name "*.mp3" -o -name "*.flac" -o -name "*.wav" -o -name "*.aac" -o -name "*.m4a" -o -name "*.ogg" -o -name "*.wma" -o -name "*.alac" -o -name "*.aiff" -o -name "*.opus" -o -name "*.dsd" -o -name "*.amr" -o -name "*.ape" -o -name "*.ac3" -o -name "*.mp2" -o -name "*.wv" -o -name "*.m4b" -o -name "*.mka" -o -name "*.spx" -o -name "*.caf" -o -name "*.snd" -o -name "*.gsm" -o -name "*.tta" -o -name "*.voc" -o -name "*.w64" -o -name "*.s8" -o -name "*.u8" \) -print0)

    # Processar arquivos de áudio um a um
    for src_file in "${audio_files[@]}"; do
        if ! grep -qx "$src_file" "$normalized_list_file"; then
            process_file "$src_file" "$log_file"
        else
            ((skipped_files++))
        fi
    done

    # Resumo final
    echo "Resumo: ${#audio_files[@]} arquivos processados, $skipped_files arquivos ignorados (já normalizados)."
}

main