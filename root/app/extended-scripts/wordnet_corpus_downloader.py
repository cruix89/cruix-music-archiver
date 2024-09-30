import logging
import os
import nltk

# LOG FOLDER
log_dir = "/config/logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "nltk_install.log")

# LOGGER CONFIGURATION
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# FIXED PRINT IN TERMINAL
print("CONFIGURING NLTK CORPUS...")

# FUNCTION TO DOWNLOAD CORPUS
def download_corpora():
    logging.info("DOWNLOADING WORDNET CORPUS...")
    try:
        nltk.download('wordnet')
        logging.info("WORDNET CORPUS DOWNLOADED SUCCESSFULLY")
        print("NLTK CORPUS CONFIGURED SUCCESSFULLY")
    except Exception as e:
        logging.error(f"ERROR DOWNLOADING WORDNET: {e}")
        print("ERROR CONFIGURING NLTK CORPUS")

# DOWNLOAD WORDNET CORPUS
download_corpora()