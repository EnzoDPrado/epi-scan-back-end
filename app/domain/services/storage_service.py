from abc import ABC, abstractmethod


class StorageService(ABC):
    @abstractmethod
    def upload(self, file_bytes: bytes, file_name: str, content_type: str) -> str:
        pass

    @abstractmethod
    def delete(self, file_name: str) -> None:
        pass

    @abstractmethod
    def exists(self, file_name: str) -> bool:
        pass