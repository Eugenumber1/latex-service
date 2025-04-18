from latex_service.latex_service import LatexService


def test_pdf_generation():
    service = LatexService()
    with open("test_files/temp.tex", "rb") as latex_file:
        file = latex_file.read()
        job_id = service.generate_pdf(file, "document")
    assert job_id != None
