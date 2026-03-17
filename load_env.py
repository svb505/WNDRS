import os
import sys
from dotenv import load_dotenv
from logtofile import log_to_file

def load_env():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    env_path = os.path.join(base_path, ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        log_to_file(f"[!] .env not found: {env_path}",level = "error", start_time_ = 0.0)


