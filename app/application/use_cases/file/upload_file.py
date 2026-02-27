from fastapi import UploadFile, File
import shutil
import os
from pathlib import Path

class UploadFileUseCase:
    def __init__(self):
        pass

    def execute(self, upload_dir: str, file: UploadFile = File(...)) :
        try:
            upload_path = Path(upload_dir)

            if not os.path.exists(upload_dir):
                os.mkdir(upload_dir)

            file_path = upload_path / file.filename

            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return file.filename
        except Exception as e:
            raise Exception("Error while uploading image", e)
