"""S3 client"""
from typing import TYPE_CHECKING

import boto3
from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile
from fastapi.logger import logger
from starlette import status

if TYPE_CHECKING:
    from botocore.client import BaseClient


class S3Client:
    """Client for S3"""

    def __init__(
        self: "S3Client",
        access_key_id: str,
        secret_access_key: str,
        region: str,
    ) -> None:  # pragma: no cover
        """Init S3 client"""
        self.credentials = {
            "aws_access_key_id": access_key_id,
            "aws_secret_access_key": secret_access_key,
            "region_name": region,
        }

    def get_file_from_bucket(
        self: "S3Client",
        key: str,
        bucket: str,
    ) -> tuple:  # pragma: no cover
        """
        Get file from S3 bucket

        Args:
            key (str): file key
            bucket (str): bucket name

        Returns:
            tuple: file data and content type
        """
        s3: BaseClient = boto3.client("s3", **self.credentials)
        try:
            obj = s3.get_object(Bucket=bucket, Key=key)
            data = obj["Body"].read()
            content_type = obj["ContentType"]
        except ClientError as err:
            logger.error(err)
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Couldn't get file from S3 bucket",
            ) from err
        else:
            return data, content_type

    def get_presigned_url(
        self: "S3Client",
        key: str,
        bucket: str,
    ) -> str:  # pragma: no cover
        """
        Get presigned URL for file in S3 bucket

        Args:
            key (str): file key
            bucket (str): bucket name

        Returns:
            str: presigned URL
        """
        s3: BaseClient = boto3.client("s3", **self.credentials)
        try:
            return s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=600,  # 10 minutes
            )
        except ClientError as err:
            logger.error(err)
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Couldn't get file URL from S3 bucket",
            ) from err

    def upload_file_to_bucket(
        self: "S3Client",
        file: UploadFile,
        dest_file: str,
        bucket_name: str,
    ) -> None:  # pragma: no cover
        """
        Upload file to S3 bucket

        Args:
            file (UploadFile): file to upload
            dest_file (str): destination file name
            bucket_name (str): bucket name

        Returns:
            None

        Raises:
            HTTPException: If file upload fails
        """
        s3_client = boto3.client("s3", **self.credentials)

        try:
            s3_client.upload_fileobj(
                file.file,
                bucket_name,
                dest_file,
                ExtraArgs={"ContentType": file.content_type},
            )
        except S3UploadFailedError as exc:
            logger.error(exc)
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Couldn't upload file to S3 bucket",
            ) from exc

    def upload_content_to_bucket(
        self: "S3Client",
        content: bytes,
        dest_file: str,
        bucket_name: str,
    ) -> None:  # pragma: no cover
        """
        Upload content to S3 bucket

        Args:
            content: file content
            dest_file: destination file name
            bucket_name: bucket name

        Returns:
            None
        """
        s3_client: boto3.client = boto3.client("s3", **self.credentials)

        try:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=dest_file,
                Body=content,
                ContentType="application/pdf",
            )
        except S3UploadFailedError as exc:
            logger.error(exc)
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Couldn't upload file to S3 bucket",
            ) from exc
