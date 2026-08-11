from pathlib import Path
from llama_index.core import Settings, VectorStoreIndex
#from bedrockEmbed import getBedrockModel
from bedrockQueryEngine import getBedrockModelQueryEngine
from indexReport import loadAndChunkReports, loadAndChunkReport
from ModelEmbed import getEmbeddingModel
from tools.title import header
from tools.logCleanup import cleanLogs
from tools.folderPathLogic import get_folder_path, list_files_recursive

cleanLogs()

projectRoot = Path(__file__).resolve().parent.parent
def userInput():
    filePath = Path(input("Enter report path: ").strip())
    source = input("Enter source organization: ").strip()
    return filePath, source

def get_index(folder):
    report_paths = [Path(p) for p in list_files_recursive(folder)]
    reportIDs, allDocuments, chunks = loadAndChunkReports(report_paths, "")

    print("Loading model...")
    llm = getEmbeddingModel()
    # Becomes our new global, which means things like VectorStoreIndex will use this LLM for embedding creation.
    #Settings.embed_model = llm
    print(llm.model_name + " loaded✅")

    # Use VectorStoreIndex to create a index directly from chunks
    print("Creating embeddings...")
    # Passing in model to function instead of using global variable.
    index = VectorStoreIndex(chunks, embed_model=llm, show_progress=True)
    print("Report successfully indexed✅")

    # print (f"Report ID: {reportID}")
    print(f"Report IDs: {reportIDs}")
    #print(f"Total stored chunks: {collection.count()}")

    return index

if __name__ == "__main__":
    # Split up for testing purposes (test case creation)
    print((header())) #super awesome cool title
    folder_path = get_folder_path()
    index = get_index(folder_path)

    # We need to pass in the bedrock model as the query engine.
    query_engine = index.as_query_engine(llm=getBedrockModelQueryEngine())
    print("=====================================================================================================================================================================================================\n")

    # We need to make a new def that handles querys and loops the query engine so that we don't clear the embeddings every time we ask a new question. (We want to keep the context of the report in memory for the session.)
    query = input("What would you like to ask about for the document you selected: ")
    response = query_engine.query(query)
    print(f"\nResponse: {response}")