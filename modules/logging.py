import logging
import datetime
import coloredlogs
from pathlib import Path

STORE = Path("./data/logs")

def load():
    logger = logging.getLogger()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s (%(name)s): %(message)s")
    
    STORE.mkdir(exist_ok=True)
    CUR_TIME = datetime.datetime.now().strftime("%m %d %Y-%H:%M:%S")
    file_handler = logging.FileHandler(STORE.joinpath(CUR_TIME + ".log"))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    coloredlogs.install(level=logging.INFO,logger=logger)
