from pypdf import PdfReader
import io

class PDFService:
    def extract_text(self, file_content: bytes) -> str:
        try:
            reader = PdfReader(io.BytesIO(file_content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to parse PDF: {str(e)}")

pdf_service = PDFService()
