import os
import shutil

# Mensagem inicial
print("[cruix-music-archiver] starting disambiguation process... ⚡  the mission begins to sort out the chaos! ⚡  ")

# caminho absoluto para o arquivo de configuração
config_file_path = "/app/lists/artist_disambiguator.txt"  # Substitua pelo caminho do seu arquivo .txt

def move_files_based_on_list(file_path):
    """
    lê uma lista no formato 'origem|destino' e move os arquivos da pasta de origem para a pasta de destino.

    :param file_path: caminho para o arquivo .txt contendo as informações de origem e destino
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        for line in lines:
            # Ignora linhas vazias ou comentários
            if not line.strip() or line.startswith("#"):
                continue

            # Divide a linha pelo delimitador '|'
            try:
                origin, destination = map(str.strip, line.split("|"))
            except ValueError:
                print(f"[cruix-music-archiver] invalid format in: {line.strip()} ⚠️  something’s not quite right in this file!")
                continue

            # Verifica se a pasta de origem existe
            if not os.path.exists(origin):
                continue

            # Cria a pasta de destino, se não existir
            os.makedirs(destination, exist_ok=True)

            # Itera sobre os arquivos na pasta de origem
            for filename in os.listdir(origin):
                src_file = os.path.join(origin, filename)
                dst_file = os.path.join(destination, filename)

                if os.path.isfile(src_file):
                    # Move o arquivo para o destino
                    shutil.move(src_file, dst_file)
                    print(f"[cruix-music-archiver] disambiguated: {src_file} to {dst_file} 🛠️  transformation complete — clarity achieved!")

    except Exception as e:
        print(f"[cruix-music-archiver] error processing the list: {e} 💥  the list fought back — mission failed!")


# Executa o script
if __name__ == "__main__":
    move_files_based_on_list(config_file_path)