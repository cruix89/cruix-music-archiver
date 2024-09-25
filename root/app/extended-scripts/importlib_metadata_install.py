import subprocess
import os
import logging

# LOGS DIRECTORY
log_dir = '/config/logs'

# CHECK IF THE LOG DIRECTORY EXISTS AND CREATE IT IF IT DOESN'T
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# DEFINE LOG FILE DIRECTORY
log_file = os.path.join(log_dir, 'importlib_metadata_install.log')

# LOGGER CONFIGURATION
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# FUNCTION TO CHECK IF THE PIP COMMAND IS AVAILABLE
def check_pip():
    try:
        subprocess.check_call(['pip', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# CHECK IF THE PIP COMMAND IS AVAILABLE
if not check_pip():
    logging.error("PIP COMMAND NOT FOUND. MAKE SURE PYTHON AND PIP ARE INSTALLED CORRECTLY.")
    exit(1)

# FIXED MESSAGE ON THE TERMINAL
print("INSTALLING IMPORTLIB METADATA LIBRARY...")

try:
    with open(log_file, 'a+') as f:
        logging.info('INSTALLING IMPORTLIB METADATA LIBRARY...')
        subprocess.check_call(['pip', 'install', 'importlib_metadata'], stdout=f, stderr=subprocess.STDOUT)
        logging.info('IMPORTLIB METADATA LIBRARY INSTALLED SUCCESSFULLY.')
except subprocess.CalledProcessError as e:
    logging.error(f'AN ERROR OCCURRED WHILE INSTALLING IMPORTLIB_METADATA: {e}')
    print(f'AN ERROR OCCURRED WHILE INSTALLING IMPORTLIB_METADATA: {e}')
else:
    print('IMPORTLIB METADATA LIBRARY INSTALLED SUCCESSFULLY.')