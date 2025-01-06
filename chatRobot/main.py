"""
pip install faiss-cpu
"""

from chatRobot.utils.utils import VectorstoreOperator,AnsModel,DocumentLoader
from chatRobot.models.embedding_model import get_huggingfacehubembeddings
from chatRobot.models.llm_models import get_huggingface_hub




def process(folder_path, usr_input, embedding_model_name, generate_model_name):
    loaedr = DocumentLoader()
    text = loaedr.get_text(folder_path)
    chunks = loaedr.split_to_chunks(text)
    print("开始加载嵌入模型……")
    emb_model = get_huggingfacehubembeddings(embedding_model_name)
    print("完成嵌入模型加载……")
    vo = VectorstoreOperator()
    vectorstore = vo.save_chunks_to_vectorstore(chunks,emb_model)
    print("已将向量存入数据库")
    ret_doc = vo.get_similar_embedding_from_vectorstore(usr_input, vectorstore, emb_model)#这个方法返回list[document]
    ret_chunks = [doc.page_content for doc in ret_doc]# list[str]
    question = usr_input
    info = '\n'.join(chunk for chunk in ret_chunks)
    print("开始加载llm模型……")
    llm =get_huggingface_hub(generate_model_name)
    print("llm加载完成，准备回答……")
    #使用思维链迭代回答
    am = AnsModel()
    res = am.iter_response(info=info, question=question, llm=llm)
    print(res)
    # #下面时不使用思维链
    # prompt_template = f"""
    # 假设你现在是一个机械原理的老师，请根据我给你提供的信息给出我想要的回答。
    # 信息：{info}
    # 下面，根据我的问题给出你的回答
    # 问题：{question}
    # 请给出简洁明了的答案
    # """
    # res = llm(prompt_template)
    # print("回答："+res)


if __name__ == '__main__':
    folder_path = "./docs" # 存放文件的目录
    usr_input = '包装机械办理 CE 认证需要什么？'
    # embedding_model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    # embedding_model_name = "google-bert/bert-base-chinese"
    embedding_model_name = "BAAI/bge-base-zh-v1.5"
    # generate_model_name = "uer/gpt2-chinese-cluecorpussmall"
    generate_model_name = "Qwen/Qwen2.5-Coder-32B-Instruct"
    process(folder_path, usr_input, embedding_model_name, generate_model_name)
