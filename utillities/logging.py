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

def initialize_log_file():
    timestamp = datetime.now().strftime("%Y%m%d-%s")
    with open(f"log_{timestamp}", "w", encoding="utf-8") as f:
        f.write("")
    return f"log_{timestamp}"

def get_name(value):
    for name, val in vars(Level).items():
        if val == value:
            return name
    return None
    
def log_msg(msg, level, file_info: list = [None, None]):
    timestamp = datetime.now().strftime("%Y%m%d-%s")
    file = file_info[0]
    line = file_info[1]
    
    with open(f"output/logs/{Settings().LOG_FILENAME}", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{get_name(level)}] {file}.{line}: {msg}\n")
    
    if level == Level.ERROR and not Settings().SUPPRESS_ERRORS:
        print(f"[{get_name(level)}] {file}.{line}: {msg}")

    if level >= Settings().LOG_LEVEL and not level == Level.ERROR:
        if level == Level.DISPLAY:
            print(f"{msg}")
        elif level == Level.INFO:
            print(f"[{get_name(level)}] {file}.{line}: {msg}")
        else:
            print(f"[{timestamp}] [{get_name(level)}] {file}.{line}: {msg}")
        
def log_variable(var_name, var_value, level, file_info: list = [None, None]):
    log_msg(f"[SET VARIABLE] {var_name} -> {var_value}", level , file_info)