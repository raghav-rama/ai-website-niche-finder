import logging
import datetime
import os

# remove any existing log handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

now = datetime.datetime.now()
dt = now.strftime("T%H-%M-%S-D%Y-%m-%d")
# store logs in logs folder
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)  # create logs directory if it doesn't exist
log_file = os.path.join(log_dir, f"debug-{dt}.log")
handler = logging.FileHandler(log_file, mode="w")
handler.setLevel(logging.DEBUG)


# https://stackoverflow.com/questions/533048/how-to-log-source-file-name-and-line-number-in-python
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(pathname)s - %(filename)s - %(lineno)d - %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)


def getLogger():
    return logger
