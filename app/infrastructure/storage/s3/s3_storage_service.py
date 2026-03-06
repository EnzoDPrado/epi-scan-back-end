import boto3
import os
from botocore.exceptions import ClientError
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

    def upload(self, file_bytes: bytes, file_name: str, content_type: str) -> tuple[str, str]:

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=file_name,
            Body=file_bytes,
            ContentType=content_type,
        )

        url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_name}"

        return url

    def exists(self, file_name: str) -> bool:
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=file_name,
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise e
        
    def delete(self, file_name: str) -> None:
        self.s3_client.delete_object(
            Bucket=self.bucket_name,
            Key=file_name,
        )