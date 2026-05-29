import asyncio
import os
import tempfile
import uuid

from jinja2 import Template
from weasyprint import HTML
from src.utils.S3Storage import S3Storage
from src.config import Settings

class Renderer:

    @staticmethod
    async def render(template: str, data: dict, filename: str | None = None, bucket_name: str | None = None) -> str:
        if filename is None:
            filename = f"{uuid.uuid4()}.pdf"
        if '.' not in filename:
            filename += ".pdf"
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        resource_path = os.path.join(base_path, "resource")
        resource_path_url = resource_path.replace("\\", "/")
        resource_path_url = f"file:///{resource_path_url}"

        data['resource_path'] = resource_path_url
        
        html_content = Template(template).render(**data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f: 
            f.write(html_content)
            temp_path = f.name

        HTML(f'file://{temp_path}').write_pdf(filename)
        os.unlink(temp_path)

        settings = Settings()
        endpoint_url = f"{settings.S3_URL}"
        bucket_name = bucket_name or settings.BUCKET_NAME

        storage = S3Storage(
            endpoint_url=endpoint_url,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            bucket_name=bucket_name
        )

        try:
            await storage.connect()
            await storage.upload_file(filename, filename)
            file_url = await storage.generate_presigned_url(
                filename,
                expiration=99999999999
            )
            return file_url
        except Exception as e:
            print(f"Error with S3 work! {e}")
            raise

