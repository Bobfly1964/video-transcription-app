import boto3
import json
from typing import Dict, Any
from app.core.config import settings

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            endpoint_url=settings.s3_endpoint
        )
        self.bucket = settings.s3_bucket

    def upload_json(self, data: Dict[str, Any], key: str) -> bool:
        """Upload JSON data to S3"""
        try:
            json_data = json.dumps(data, ensure_ascii=False)
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=json_data,
                ContentType='application/json'
            )
            return True
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return False

    def download_json(self, key: str) -> Dict[str, Any]:
        """Download JSON data from S3"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=key)
            json_data = response['Body'].read().decode('utf-8')
            return json.loads(json_data)
        except Exception as e:
            print(f"Error downloading from S3: {e}")
            return {}

    def delete_object(self, key: str) -> bool:
        """Delete object from S3"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=key)
            return True
        except Exception as e:
            print(f"Error deleting from S3: {e}")
            return False 