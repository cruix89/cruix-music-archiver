import logging
import os
import nltk

# log folder
log_dir = "/config/logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "nltk_install.log")

# logger configuration
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# fixed print in terminal
print("configuring NLTK corpus...")

# function to download corpus
def download_corpora():
    logging.info("downloading WORDNET CORPUS...")
    try:
        nltk.download('wordnet')
        logging.info("WORDNET CORPUS downloaded successfully")
        print("NLTK corpus configured successfully")
    except Exception as e:
        logging.error(f"error downloading WORDNET: {e}")
        print("error configuring NLTK corpus")

# download WORDNET CORPUS
download_corpora()