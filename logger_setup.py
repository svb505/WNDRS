import os
import logging
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))

log_dir = os.path.join(base_dir, "syst_comp")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "system_log.log")

log_dir1 = os.path.join(base_dir, "logs_session")
os.makedirs(log_dir1, exist_ok=True)
log_path1 = os.path.join(log_dir1, f"session_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

error_dir = os.path.join(base_dir, ".dumps")
os.makedirs(error_dir, exist_ok=True)
error_path = os.path.join(error_dir, f"dump_{datetime.now().strftime('%Y-%m-%d_%H')}.log")

system_logger = logging.getLogger("system_logger")
system_logger.setLevel(logging.DEBUG)
system_logger.propagate = False

if not system_logger.handlers:
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    system_logger.addHandler(handler)

system_logger1 = logging.getLogger("session_logger")
system_logger1.setLevel(logging.DEBUG)
system_logger1.propagate = False
if not system_logger1.handlers:
    handler = logging.FileHandler(log_path1, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    system_logger1.addHandler(handler)

error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)
error_logger.propagate = False
if not error_logger.handlers:
    handler = logging.FileHandler(error_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    error_logger.addHandler(handler)