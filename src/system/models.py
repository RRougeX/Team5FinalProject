from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv
from llama_index.llms.bedrock_converse import BedrockConverse

from importlib.resources import path

from Team5FinalProject.src.tools.folder_path_logic import load_config_and_get_section


def getEmbeddingModel():

    return HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5",
        device="cpu"
    )

def getBedrockModelQueryEngine():
        model = "amazon.nova-pro-v1:0"
        print(f"Using Bedrock model: {model}")

        # The way we are handling keys could be dangerous depending on how things are packaged.
        config = load_config_and_get_section(section="AWS")

        # Bedrock () throws it's own exceptions on bad input. If something is missed though, we will need to add a check.
        llm = BedrockConverse(
        model=model,
        #profile_name=profile_name,
        temperature=0.0,
        max_tokens=8_000,
        aws_access_key_id=config.get("access_key_id"),
        aws_secret_access_key=config.get("secret_access_key"),
        region_name=config.get("region"),)

        return llm

def get_embedding_llm_print():
    print("Loading embedding model...")
    embedding_llm = getEmbeddingModel()
    print(embedding_llm.model_name + " loaded✅")
    return embedding_llm


#https://developers.llamaindex.ai/python/framework/integrations/llm/bedrock/

# SCRAPPED DUE TO NOT HAVING THE ABILITY TO USE IT!!! (our sandbox does not include this service.)
# def getBedrockModelEmbed():
#         load_dotenv()  # Load environment variables from .env file

#         model = os.getenv("BEDROCK_MODEL")
#         profile_name = os.getenv("AWS_PROFILE_NAME")

#         print(f"Using Bedrock model: {model}")

#         # Bedrock () throws it's own exceptions on bad input. If something is missed though, we will need to add a check.
#         llm = BedrockConverse(
#         model=model,
#         #profile_name=profile_name,
#         temperature=0.0,
#         max_tokens=8_000,
#         aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#         aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
#         region_name=os.getenv("REGION_NAME"),)

#         return llm