import os
import shutil


def rec_copy_files(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for src_name in os.listdir(src_dir):
        src_path = os.path.join(src_dir, src_name)
        dest_path = os.path.join(dest_dir, src_name)
        if os.path.isfile(src_path):
            print(f"Copying {src_path} to {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            rec_copy_files(src_path, dest_path)
