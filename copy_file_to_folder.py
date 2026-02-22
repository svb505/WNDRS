import os
from logtofile import log_system
import shutil

def copy_file_to_folder(source_file, target_folder,start_time_):
    log_system(f"Copy file {source_file} to {target_folder}", start_time_)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    target_file = os.path.join(target_folder, os.path.basename(source_file))

    # Копируем файл, перезаписывая, если он уже существует
    shutil.copy(source_file, target_file)