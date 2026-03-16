import asyncio
from pathlib import Path
from typing import Union, BinaryIO, Optional
import aioboto3
from botocore.exceptions import ClientError


class S3Storage:

    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        region_name: Optional[str] = None,
    ):

        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.region_name = region_name
        self._session = aioboto3.Session()

    async def _create_bucket(self):
        async with self._session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
        ) as s3_client:
            try:
                await s3_client.create_bucket(Bucket=self.bucket_name)
            except ClientError as e:
                if e.response['Error']['Code'] in ('BucketAlreadyOwnedByYou', 'BucketAlreadyExists'):
                    pass
                else:
                    raise

    async def connect(self):
        await self._create_bucket()


    async def upload_file(
        self,
        local_path: Union[str, Path],
        object_name: Optional[str] = None,
        extra_args: Optional[dict] = None,
    ) -> bool:

        local_path = Path(local_path)
        if not local_path.is_file():
            raise FileNotFoundError(f"Файл не найден: {local_path}")

        if object_name is None:
            object_name = local_path.name

        async with self._session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
        ) as s3_client:
            try:
                await s3_client.upload_file(
                    str(local_path),
                    self.bucket_name,
                    object_name,
                    ExtraArgs=extra_args or {},
                )
                return True
            except ClientError as e:
                print(f"Ошибка при загрузке файла: {e}")
                return False

    async def upload_bytes(
        self,
        data: bytes,
        object_name: str,
        extra_args: Optional[dict] = None,
    ) -> bool:

        async with self._session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
        ) as s3_client:
            try:

                from io import BytesIO
                with BytesIO(data) as file_obj:
                    await s3_client.upload_fileobj(
                        file_obj,
                        self.bucket_name,
                        object_name,
                        ExtraArgs=extra_args or {},
                    )
                return True
            except ClientError as e:
                print(f"Ошибка при загрузке байтов: {e}")
                return False

    async def upload_fileobj(
        self,
        fileobj: BinaryIO,
        object_name: str,
        extra_args: Optional[dict] = None,
    ) -> bool:

        async with self._session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
        ) as s3_client:
            try:
                await s3_client.upload_fileobj(
                    fileobj,
                    self.bucket_name,
                    object_name,
                    ExtraArgs=extra_args or {},
                )
                return True
            except ClientError as e:
                print(f"Failed to upload: {e}")
                return False