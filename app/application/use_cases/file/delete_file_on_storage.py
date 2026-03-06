
from app.domain.services.storage_service import StorageService

class DeleteFileOnStorageUseCase():
    def __init__(self, storage_service: StorageService):
        self.storage_service = storage_service

    def execute(self, file_name: str):
        file_exists = self.storage_service.exists(file_name)

        if not file_exists:
            return
        try:
            self.storage_service.delete(file_name)
        except Exception as e:
            raise Exception(f"Error while deleting image from storage service: {e}")
            
        