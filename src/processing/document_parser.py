import docx
import PyPDF2


# 解析文件並提取文本內容，支援 .docx, .pdf 和 .txt 格式
def parse_document(file_path):
    """
    Parses a document and extracts the text content.
    Supports .docx, .pdf, and .txt files.
    """
    try:
        if file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            text = "\\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        elif file_path.endswith(".pdf"):
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = "\\n".join([page.extract_text() for page in reader.pages])
                return text
        elif file_path.endswith(".txt"):
            with open(file_path, "r") as f:
                text = f.read()
                return text
        else:
            return None
    except Exception as e:
        print(f"Error parsing document: {e}")
        return None
