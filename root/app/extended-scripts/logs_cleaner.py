import os
import glob
import logging

# ABSOLUTE PATH TO THE LOGS DIRECTORY (SET THE FULL PATH)
logs_directory = "/config/logs"

# FULL PATH TO THE LOG FILE
log_file = os.path.join(logs_directory, "logs_cleaner.log")

# CONFIGURE LOGGING
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("CLEANING LOG DIRECTORY...")

# FIND ALL FILES IN THE LOGS DIRECTORY
files = glob.glob(os.path.join(logs_directory, "*"))

# LOOP FOR FILE DELETION
for file in files:
    try:
        os.remove(file)
        logging.info(f"FILE {file} DELETED.")
    except FileNotFoundError:
        logging.warning(f"FILE {file} NOT FOUND DURING DELETION.")
    except PermissionError:
        logging.error(f"PERMISSION DENIED WHEN TRYING TO DELETE FILE {file}.")
    except Exception as e:
        logging.error(f"ERROR DELETING FILE {file}: {e}")

# LOG FINALIZATION USING 'WITH'
with open(log_file, 'a') as log:
    log.write("ALL FILES HAVE BEEN DELETED.\n")

print("LOGS DELETED SUCCESSFULLY.")