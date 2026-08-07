from pathlib import Path

from llama_index.core import Settings, VectorStoreIndex
from bedrockEmbed import getBedrockModel
from indexReport import loadAndChunkReport

projectRoot = Path(__file__).resolve().parent.parent

def userInput():

    filePath = Path(input("Enter report path: ").strip())
    source = input("Enter source organization: ").strip()
    return filePath, source

def get_index(filePath, source):
    reportID, documents, chunks = loadAndChunkReport(
        filePath,
        source
    )

    print("Loading Bedrock model...")
    llm = getBedrockModel()
    # Becomes our new global, which means things like VectorStoreIndex will use this LLM for embedding creation.
    #Settings.embed_model = llm
    print("Bedrock model loaded.")

    # Use VectorStoreIndex to create a index directly from chunks
    print("Creating embeddings...")
    index = VectorStoreIndex(chunks, embed_model=llm)
    print("\nReport successfully indexed.")

    print(f"Report ID: {reportID}")
    #print(f"Total stored chunks: {collection.count()}")

if __name__ == "__main__":
    # Split up for testing purposes (test case creation)
    filePath, source = userInput()
    index = get_index(filePath, source)

    #Testing if query works.
    index.query("What is the report about?")