import inspect

from utillities.settings import Settings
from datetime import datetime


class Level:    
    DEBUG = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    DISPLAY = 4
    
def file_info():
    frame = inspect.currentframe().f_back
    filepath = frame.f_code.co_filename
    filename = filepath.split('/')[-1]
    lineno = frame.f_lineno
    return [filename, lineno]

def get_name(value):
    for name, val in vars(Level).items():
        if val == value:
            return name
    return None
    
def log_msg(msg, level, file_info: list = [None, None]):
    if level >= Settings().LOG_LEVEL:
        timestamp = datetime.now().strftime("%Y%m%d-%s")
        file = file_info[0]
        line = file_info[1]
        
        if level == Level.DISPLAY:
            print(f"{msg}")
        else:
            print(f"[{timestamp}] [{get_name(level)}] {file}.{line}: {msg}")
        
