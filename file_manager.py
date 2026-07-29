import os
import shutil
import tkinter as tk

from tkinter import filedialog
from models import ImageFile
from image_utils import ImageProcessor

from config import (
    MAX_UPLOAD_SIZE,
    ALLOWED_EXTENSIONS
)


class FolderManager:

    def __init__(self):
        pass

    def move_files(self, rootdir, file_map, target_folders):

        for folder, files in target_folders.items():

            destination = os.path.join(rootdir, folder)
            os.makedirs(destination, exist_ok=True)

            for fname in files:

                try:
                    shutil.move(file_map[fname], destination)

                except shutil.Error as e:
                    print(f"Could not move {fname}: {e}")

    
    def build_upload(self, path, filename):

        if os.path.getsize(path) > MAX_UPLOAD_SIZE:
            content = ImageProcessor.compress(path)
        else:
            content = ImageProcessor.read(path)

        ext = filename.split(".")[-1].lower()

        return (
            ImageFile(
                filename,
                path,
                content,
                f"image/{ext}"
            )
        )
    def scan_directory(self, rootdir):

        upload_files = []
        file_map = {}

        for root, _, files in os.walk(rootdir):

            for file in files:

                ext = file.split(".")[-1].lower()

                if ext not in ALLOWED_EXTENSIONS:
                    continue

                abs_path = os.path.join(root, file)

                rel_path = os.path.relpath(abs_path, rootdir)

                file_map[rel_path] = abs_path

                upload_files.append(
                    self.build_upload(
                        abs_path,
                        rel_path,
                    )
                )

        return upload_files, file_map
    
    def displayImage(self, path:str):
        from PIL import Image
        with Image.open(path) as im:
            im.show()

    def select_files(self):

        root = tk.Tk()
        root.withdraw()

        paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.webp")
            ]
        )

        root.destroy()

        images = []
        file_map = {}
        for path in paths:

            filename = os.path.relpath(path)
            file_map[filename] = path
            images.append(
                self.build_upload(
                    path,
                    filename #can switch this to path to be able to retain the path as the id
                )
            )

        return images, file_map