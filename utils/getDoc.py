"""
获取不同格式的文件,目前支持
    .docs .docx .pdf
"""
import os
import docx
import pdfplumber
import win32com.client

def convert_doc_to_docx(input_path, output_path):
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False  # 隐藏 Word 窗口
        doc = word.Documents.Open(input_path)
        doc.SaveAs(output_path, FileFormat=16)  # 16 表示 .docx 格式
        doc.Close()
        word.Quit()
        return output_path
    except Exception as e:
        print(f"将doc转换为docx时出错: {e}")
        return None
def get_docx_text(file_path, text=""):
    """提取.docx 文件中的文本"""
    try:
        file = docx.Document(file_path)
        for p in file.paragraphs:
            text += p.text
        return text
    except Exception as e:
        print(f"读取docx文件时出错: {e}")
        return text
class FileExtractor:
    def __init__(self):
        pass
    def get_doc_text(self, file_path, text=""):
        """提取.docs 或 .docx 文件中的文本"""
        if file_path.endswith('.docs'):
            docx_path = convert_doc_to_docx(file_path, f"{os.path.splitext(file_path)[0]}.docx")
            if docx_path:
                text = get_docx_text(docx_path, text)
        elif file_path.endswith('.docx'):
            text = get_docx_text(file_path, text)
        return text
    def get_pdf_text(self, file_path, text=""):
        """提取.pdf 文件中的文本"""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            print(f"读取pdf文件时出错: {e}")
            return text

