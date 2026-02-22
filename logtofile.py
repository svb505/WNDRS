import time
from logger_setup import system_logger,system_logger1,error_logger
from crypto_work import read_encrypted_file
import logging

SYSTEM_LEVEL = 25
logging.addLevelName(SYSTEM_LEVEL, "SYSTEM")

def log_to_file(msg, start_time_,level="info"):
    try:
        elapsed = time.time() - start_time_
    except NameError:
        elapsed = 0
    formatted_msg = f"[{elapsed:.1f}] - {msg}"

    if level == "info":
        system_logger.info(formatted_msg)
        system_logger1.info(formatted_msg)
    elif level == "warning":
        system_logger.warning(formatted_msg)
        system_logger1.warning(formatted_msg)
    elif level == "error":
        system_logger.error(formatted_msg)
        system_logger1.error(formatted_msg)
        if read_encrypted_file("syst_comp/log_set.cfg") == "0":
            error_logger.error(formatted_msg)
    else:
        system_logger.debug(formatted_msg)
        system_logger1.debug(formatted_msg)
def log_system(msg,start_time_):
    try:
        elapsed = time.time() - start_time_
    except NameError:
        elapsed = 0

    formatted_msg = f"[{elapsed:.1f}] - {msg}"
    system_logger.log(SYSTEM_LEVEL, formatted_msg)