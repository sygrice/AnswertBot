import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import pdfplumber
from langchain.schema import Document
from .getDoc import FileExtractor
"""
    1.文档加载器
"""
class DocumentLoader():
    def __init__(self):
        pass
    def get_text(self, folder_path):
        """提取文件夹中内容"""
        file_extractor = FileExtractor()
        text = ""
        for path, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".pdf"):
                    print("getting pdf")
                    text += file_extractor.get_pdf_text(f"{folder_path}/{file}")
                elif file.endswith(".docs") or file.endswith(".docx"):
                    print("getting docs")
                    text += file_extractor.get_doc_text(f"{folder_path}/{file}")
        return text
    def extract_one_pdf_text(self, file_path):
        """只提取单个pdf"""
        text = ""
        with pdfplumber.open(file_path) as f:
            for page in f.pages:
                text += page.extract_text()
        return text
    def split_to_chunks(self, text):
        text_split = CharacterTextSplitter(
            separator="\n",
            chunk_size=500,
            chunk_overlap=80,
            length_function=len
        )
        chunks = text_split.split_text(text)
        return chunks
"""
    2.向量数据库操作
"""
class VectorstoreOperator():
    def __init__(self):
        pass
    def save_chunks_to_vectorstore(self, chunks, embedding_model):# chunks是list[str]，embedding_model是嵌入模型
        doc = []
        for chunk in chunks:
            doc.append(Document(chunk))
        vectorstore = FAISS.from_documents(documents=doc,embedding=embedding_model)
        return vectorstore
    def get_similar_embedding_from_vectorstore(self, query_text,vectorstore,embedding_model):
        query_embedding = embedding_model.embed_query(query_text)
        result = vectorstore.similarity_search_by_vector(query_embedding)
        return result

"""
    3.提示词模板
"""
# 根据query进行相似度搜索，query_text是str
def origin_prompts(info, question, llm):
    prompt = f"""
    你是一个机械原理专家，以下是与问题相关的信息：
    信息：{info}
    问题：{question}
    请按照以下步骤回答：
    1. 列出解决问题的主要步骤。
    2. 对每个步骤进行简要解释。
    3. 汇总步骤并生成最终答案。
    """
    res_steps = llm(prompt)
    return res_steps
class AnsModel():
    def __init__(self):
        pass
    def iter_response(self, info,question,llm,iteration = 2):# 通过反复迭代，得出最终答案
        for i in range(iteration):
            res_steps = origin_prompts(info,question,llm)
            prompt=f"""
            基于以下推理过程，请生成比之前更完整、更精准的答案：
            推理过程：{res_steps}
            问题：{question}
            答案：
            """
            ans = llm(prompt)
            # print("*********************************************************")
            # print(f"第{i+1}轮迭代的回答：{ans}")
            # print("*********************************************************")
            info += f'\n补充信息：{ans}'
            i+=1
        return ans