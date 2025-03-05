from langchain.llms import HuggingFaceHub

def get_huggingface_hub(model_name):
    llm_model = HuggingFaceHub(
        repo_id=model_name,
        task="text-generation"
    )
    return llm_model