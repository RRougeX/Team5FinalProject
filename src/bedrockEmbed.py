from importlib.resources import path
import os
from dotenv import load_dotenv
# Need to import bedrock_converse, just bedrock is legacy.
from llama_index.llms.bedrock_converse import BedrockConverse


#from indexReport.py pull def
from indexReport import loadAndChunkReport

#https://developers.llamaindex.ai/python/framework/integrations/llm/bedrock/

def getBedrockModel():
        load_dotenv()  # Load environment variables from .env file

        model = os.getenv("BEDROCK_MODEL")
        profile_name = os.getenv("AWS_PROFILE_NAME")

        print(f"Using Bedrock model: {model}")

        # Bedrock () throws it's own exceptions on bad input. If something is missed though, we will need to add a check.
        llm = BedrockConverse(
        model=model,
        #profile_name=profile_name,
        temperature=0.0,
        max_tokens=8_000,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("REGION_NAME"),)

        return llm

# We might want to set up Streaming? (stream_chat)

