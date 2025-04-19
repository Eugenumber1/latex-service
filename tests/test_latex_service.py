from latex_service.latex_service import LatexService
import os
import pytest
import asyncio


@pytest.mark.asyncio
async def test_pdf_generation():
    service = LatexService()
    with open("test_files/temp.tex", "rb") as latex_file:
        file_contents = latex_file.read()
        job_id = await service.generate_pdf(file_contents, "document")
    assert job_id != None
    assert os.path.exists(f"output/document.pdf")


# @pytest.mark.asyncio
# async def test_call_pdflatex():
#     service = LatexService()
#     with open("test_files/temp.tex", "rb") as latex_file:
#         content = latex_file.read()
#         temp_file, temp_dir = service.create_temp_file_and_dir("document")
#         with open(temp_file, "wb") as f:
#             f.write(content)
#         pdf_path = await service.call_pdflatex(temp_dir, temp_file, "document")
#     assert os.path.exists(pdf_path)
