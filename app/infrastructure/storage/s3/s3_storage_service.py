import boto3
import uuid
import os

from app.application.utils.file_utils import generate_file_name
from app.domain.services.storage_service import StorageService

class S3StorageService(StorageService):
    def __init__(self):
        self.bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
        self.region = os.getenv("AWS_REGION", "us-east-1")

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=self.region
        )

    def upload(self, file_bytes: bytes, file_name: str, content_type: str) -> str:
        unique_file_name = generate_file_name(file_name)

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=unique_file_name,
            Body=file_bytes,
            ContentType=content_type,
        )

        url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{unique_file_name}"

        return url

    def delete(self, file_name: str) -> None:
        self.s3_client.delete_object(
            Bucket=self.bucket_name,
            Key=file_name,
        )