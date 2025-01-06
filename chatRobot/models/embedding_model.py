from langchain.embeddings import HuggingFaceEmbeddings
def get_huggingfacehubembeddings(model_name):
    return HuggingFaceEmbeddings(model_name=model_name)