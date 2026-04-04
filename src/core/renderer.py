import asyncio
import os
import tempfile
from jinja2 import Template
from weasyprint import HTML
from src.utils.S3Storage import S3Storage
from src.config import Settings

class Renderer:

    @staticmethod
    def render(template: str, data: dict, filename: str):
        if ('.' not in filename):
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
        endpoint_url = f"http://{settings.S3_URL}:{settings.S3_PORT}"

        storage = S3Storage(
            endpoint_url=endpoint_url,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            bucket_name=settings.BUCKET_NAME
        )

        async def upload():
            try:
                await storage.connect()
                await storage.upload_file(filename, filename)
            except Exception as e:
                print(f"Error with S3 work! {e}")
        
        asyncio.run(upload())