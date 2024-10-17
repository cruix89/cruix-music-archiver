import os
import glob
import logging

# ABSOLUTE PATH TO THE LOGS DIRECTORY (SET THE FULL PATH)
logs_directory = "/config/logs"

# CREATE LOGS DIRECTORY IF IT DOES NOT EXIST
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)

# FULL PATH TO THE LOG FILE
log_file = os.path.join(logs_directory, "logs_cleaner.log")

# CONFIGURE LOGGING
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("cleaning logs directory...")

# CHECK IF LOG DIRECTORY EXISTS
if not os.path.exists(logs_directory):
    logging.error(f"LOG DIRECTORY {logs_directory} DOES NOT EXIST.")
    raise FileNotFoundError(f"LOG DIRECTORY {logs_directory} DOES NOT EXIST.")

# FIND ALL FILES IN THE LOGS DIRECTORY
files = glob.glob(os.path.join(logs_directory, "*"))

# EXCLUDE LOG FILE FROM DELETION
files = [file for file in files if file != log_file]

# LOOP FOR FILE DELETION
for file in files:
    try:
        os.remove(file)
        logging.info(f"FILE {file} CLEANED.")
    except FileNotFoundError:
        logging.warning(f"FILE {file} NOT FOUND DURING DELETION.")
    except PermissionError:
        logging.error(f"PERMISSION DENIED WHEN TRYING TO CLEAN FILE {file}.")
    except Exception as e:
        logging.error(f"UNEXPECTED ERROR CLEANING FILE {file}: {type(e).__name__}: {e}")

# LOG FINALIZATION
logging.info("ALL FILES HAVE BEEN CLEANED.")
print("logs cleaned successfully.\n")