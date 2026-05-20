import os
import shutil

def empty_web_content(path):
    if os.path.exists(path):
        shutil.rmtree(path)

    os.makedirs(path, exist_ok=True)

def copy_static(path_from, path_to):
    for item in os.listdir(path_from):

        item_path = os.path.join(path_from, item)
        target_path = os.path.join(path_to, item)

        if os.path.isfile(item_path):
            shutil.copy(item_path, target_path)
        else:
            os.makedirs(target_path, exist_ok=True)
            copy_static(item_path, target_path)
    