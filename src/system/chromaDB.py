import os
from pathlib import Path
import chromadb
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from system.indexReport import loadAndChunkReports
from tools.folder_path_logic import get_folder_path, list_files_recursive
from system.models import get_embedding_llm_print
from datetime import datetime
from pathlib import Path

def getChromaCollection():
    projectRoot = Path(__file__).resolve().parent.parent
    databasePath = projectRoot / "storage" / "chroma"

    databasePath.mkdir(parents=True, exist_ok=True)

    # Open the persistent local database
    chromaClient = chromadb.PersistentClient(
        path=str(databasePath)
    )

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


# -------------------------------------------------------------------------------------------

def init_RAG_to_chromaDB(path = "storage/chroma"):
    projectRoot = Path(__file__).resolve().parent.parent
    databasePath = projectRoot / path

    db = chromadb.PersistentClient(path=str(databasePath))
    collection = db.get_or_create_collection(name="malware_chunks")
    vector_store = ChromaVectorStore(chroma_collection=collection)
    return vector_store

def save_RAG_to_chromaDB(chunks, embedding_model, path="storage/chroma"):
    vector_store = init_RAG_to_chromaDB(path)

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    # Raffaele Bug fix, now stores the chunks that indexReport.py already created not processing teh full documents anymore
    index = VectorStoreIndex(
        nodes=chunks,
        storage_context=storage_context,
        embed_model=embedding_model,
        show_progress=True
    )

    return index
def load_RAG_from_chromaDB(llm, path = "storage/chroma"):
    vector_store = init_RAG_to_chromaDB(path)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=llm, show_progress=True)
    return index

# --- MAIN ---

def load_embedding_data():
    folder = get_folder_path(key = "last_used_embedding_path", prompt_text="Please enter the folder path where your embedding data is stored: ")

    if folder is None:
        print("Failed to load embedding data. Valid folder not given.")
        return None

    path = Path(folder)

    with os.scandir(path) as it:
        if not any(it):
            print("Failed to load embedding data. Folder is empty.")
            return None

    embedding_llm = get_embedding_llm_print()

    # Don't know what will happen if you try to pull from a bad path right now. Worth testing and fixing.
    index = load_RAG_from_chromaDB(embedding_llm, path=folder)
    return index

def create_embedding_data():
    rag_folder = get_folder_path(
        key="last_used_embedding_path",
        prompt_text=(
            "Please enter the folder path where you want to store your new embedding data: "
        ),
        prompt_for_new_folder=True
    )

    if rag_folder == None:
        return None

    documents_folder = get_folder_path(
        key="last_used_documents_path",
        prompt_text=(
            "Please enter the folder path where your documents are stored: "
        ),
        prompt_for_new_folder=False
    )

    if documents_folder == None:
        return None

    report_paths = [
        Path(path)
        for path in list_files_recursive(documents_folder)
    ]

    reportIDs, allDocuments, chunks = loadAndChunkReports(
        report_paths,
        ""
    )

    if reportIDs == None:
        print("Failed to load and chunk given Reports.\nReturning to options page...")
        return None

    embedding_llm = get_embedding_llm_print()

    index = save_RAG_to_chromaDB(
        chunks,
        embedding_llm,
        path=rag_folder
    )

    return index
