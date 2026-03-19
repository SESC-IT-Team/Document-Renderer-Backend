# src/main.py
from fastapi import FastAPI
from pydantic import BaseModel

from src.config import Settings
from src.tasks import generate_certificate_task

app = FastAPI()
settings = Settings()


class CertificateRequest(BaseModel):
    template_content: str
    data: dict
    filename: str | None = None


@app.post("/generate")
async def generate_certificate(req: CertificateRequest):
    task = await generate_certificate_task.kiq(
        req.template_content,
        req.data,
        req.filename,
    )
    return {"task_id": task.task_id}
