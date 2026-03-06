from fastapi import UploadFile, File
import shutil
import os
from pathlib import Path
from PIL import Image
from io import BytesIO

from app.application.utils.file_utils import generate_file_name
from app.domain.exceptions.business_rule_exception import BusinessRuleException

class UploadFileOnLocalUseCase:
    def __init__(self):
        pass

    def execute(self, upload_dir: str, file_contents: bytes, file: UploadFile = File(...)):
        self._validate(file, file_contents)
        try:
            upload_path = Path(upload_dir)

            if not os.path.exists(upload_dir):
                os.mkdir(upload_dir)

            file_name = generate_file_name(file.filename)

            file_path = upload_path / file_name

            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return file_name
        except Exception as e:
            raise Exception("Error while uploading image", e)
        
    def _validate(self, file: UploadFile, file_contents: bytes) :
        self._validate_file_type(file)
        self._validate_image_resolution(file_contents)
        self._validate_image_size(file_contents)

    def _validate_file_type(self, file: UploadFile) :
        ALLOWED_TYPES = ["image/jpeg", "image/png"]

        if file.content_type not in ALLOWED_TYPES :
            raise BusinessRuleException("Formato inválido para imagem, deve ser do tipo JPEG ou PNG")

    def _validate_image_size(self, contents: bytes) :
        MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 5))
        MAX_FILE_SIZE_PB = MAX_FILE_SIZE_MB * 1024 * 1024

        if len(contents) > MAX_FILE_SIZE_PB:
            raise BusinessRuleException(f"Arquivo muito grande, o tamanho máximo é: {MAX_FILE_SIZE_MB}MB")

    def _validate_image_resolution(self, contents: bytes) :
        image = Image.open(BytesIO(contents))

        width, height = image.size

        MAX_WIDTH = int(os.getenv("IMAGE_MAX_WIDTH"))
        MAX_HEIGHT = int(os.getenv("IMAGE_MAX_HEIGHT"))

        if width > MAX_WIDTH or height > MAX_HEIGHT:
            raise BusinessRuleException(f"Resolução muito grande. Máximo permitido: {MAX_WIDTH} x {MAX_HEIGHT}")
        
        MIN_WIDTH = int(os.getenv("IMAGE_MIN_WIDTH"))
        MIN_HEIGHT = int(os.getenv("IMAGE_MIN_HEIGHT"))

        if width < MIN_WIDTH or height < MIN_HEIGHT:
            raise BusinessRuleException(f"Resolução muito pequena. Minimo permitido: {MIN_WIDTH} x {MIN_HEIGHT}")