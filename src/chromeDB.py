from pathlib import Path
import chromadb
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore


def getChromaCollection():
    projectRoot = Path(__file__).resolve().parent.parent
    databasePath = projectRoot / "storage" / "chroma"

    databasePath.mkdir(parents=True, exist_ok=True)

    # Open the persistent local database
    chromaClient = chromadb.PersistentClient(
        path=str(databasePath)
    )

    #open local database
    chromaClient = chromadb.PersistentClient(path=str(databasePath))

    #Open collection from malware chunks
    collection = chromaClient.get_or_create_collection(name="malware_chunks")

    return collection

def getStorageContext(collection):

    #connected LLamaindex to ChromaDB
    vectorStore = ChromaVectorStore(chroma_collection=collection)

    storageContext = StorageContext.from_defaults(vector_store=vectorStore)

    return storageContext

def deleteExistingReport(collection, reportID: str):
    
    #delete existing report from ChromaDB
    collection.delete(where={"reportID": reportID})




