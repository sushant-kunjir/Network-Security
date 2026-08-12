from datetime import datetime
import logging
import os

log_file=f'{datetime.now().strftime('%m-%d-%y %H-%M-%S')}'
logs_path=os.path.join(os.getcwd(),'logs',log_file)
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path,log_file)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s-%(levelname)s %(message)s",
    level=logging.INFO
)