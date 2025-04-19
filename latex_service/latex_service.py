import subprocess
import os
import uuid
import tempfile
import shutil
import logging

logger = logging.getLogger(__name__)


class CompilationException(Exception):
    pass


class GenerationException(Exception):
    pass


class LatexService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def generate_pdf(self, content: bytes, filename: str) -> str:
        job_id = filename + "_" + str(uuid.uuid4())
        temporary_directory, temporary_file = self.create_temp_file_and_dir(filename)
        try:
            with open(temporary_file, "wb+") as file:
                file.write(content)

            pdf_path = await self.call_pdflatex(
                temporary_directory=temporary_directory,
                temporary_file=temporary_file,
                filename=filename,
            )
            self.prepare_output(pdf_path=pdf_path, filename=job_id)
            return job_id
        finally:
            shutil.rmtree(temporary_directory)

    def create_temp_file_and_dir(self, filename: str) -> tuple[str, str]:
        temporary_directory = tempfile.mkdtemp()
        temporary_file = os.path.join(temporary_directory, f"{filename}.tex")
        return temporary_directory, temporary_file

    async def call_pdflatex(
        self, temporary_directory: str, temporary_file: str, filename: str
    ) -> str:
        result = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-output-directory",
                temporary_directory,
                temporary_file,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            self.logger.error(f"Latex compilation failed: {result}")
            self.logger.error(f"LaTeX compilation failed: {result.stderr}")
            raise CompilationException

        pdf_path = os.path.join(temporary_directory, f"{filename}.pdf")
        if not os.path.exists(pdf_path):
            self.logger.error("PDF file was not generated")
            raise GenerationException
        return pdf_path

    def prepare_output(self, pdf_path: str, filename: str) -> None:
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        pdf_output_path = os.path.join(output_dir, f"{filename}.pdf")
        shutil.copy(pdf_path, pdf_output_path)
