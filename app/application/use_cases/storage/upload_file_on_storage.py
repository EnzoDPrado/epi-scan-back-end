import uuid
from app.domain.services.storage_service import StorageService

class UploadFileOnStorageUseCase():

    def __init__(self, storage_service: StorageService):
        self.storage_service = storage_service

    def execute(self, file_bytes: bytes, file_name: str, content_type: str) -> str:
       try:
            return self.storage_service.upload(file_bytes, file_name, content_type)
       except Exception as e:
           raise Exception("Error while uploading file", e)
    
