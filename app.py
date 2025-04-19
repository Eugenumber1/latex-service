from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from latex_service.latex_service import LatexService
import os


app = FastAPI(title="LaTeX to PDF Converter")

latex_service = LatexService()


class LaTeXBytesDocument(BaseModel):
    content: bytes
    filename: str = "document"


@app.post("/convert/bytes")
async def convert_latex_bytes_to_pdf(document: LaTeXBytesDocument):
    """Convert LaTeX content provided as bytes to PDF"""
    return await latex_service.generate_pdf(document.content, document.filename)


@app.post("/convert/file")
async def convert_latex_file_to_pdf(
    file: UploadFile = File(...), filename: str = Form("document")
):
    """Convert LaTeX content provided as a file upload to PDF"""
    content = await file.read()
    return await latex_service.generate_pdf(content, filename)


@app.get("/pdf/{job_id}")
async def get_pdf(job_id: str):
    """Retrieve a previously generated PDF by its job ID"""
    pdf_path = os.path.join("output", f"{job_id}.pdf")

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found")

    return FileResponse(
        path=pdf_path, media_type="application/pdf", filename="document.pdf"
    )


@app.post("/convert/direct")
async def convert_and_return_pdf(
    file: UploadFile = File(...), filename: str = Form("document")
):
    content = await file.read()
    job_id = await latex_service.generate_pdf(content, filename)
    pdf_path = os.path.join("output", f"{job_id}.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(
        path=pdf_path, media_type="application/pdf", filename=f"{filename}.pdf"
    )
