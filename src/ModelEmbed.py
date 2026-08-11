from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def getEmbeddingModel():

    return HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5",
        device="cpu"
    )