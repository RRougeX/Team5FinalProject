# from pathlib import Path
# from llama_index.core import Settings, VectorStoreIndex
# #from bedrockEmbed import getBedrockModel
# from PROJECT.Team5FinalProject.src.system.indexReport import loadAndChunkReports, loadAndChunkReport
# from PROJECT.Team5FinalProject.src.system.models import getEmbeddingModel, getBedrockModelQueryEngine
# from tools.title import header
# from tools.logCleanup import cleanLogs
# from tools.folderPathLogic import get_folder_path, list_files_recursive

# cleanLogs()

# projectRoot = Path(__file__).resolve().parent.parent

# def load_RAG_from_chromadb():
#     pass

# def get_embed_vectorstoreindex(folder):
#     report_paths = [Path(p) for p in list_files_recursive(folder)]
#     reportIDs, allDocuments, chunks = loadAndChunkReports(report_paths, "")

#     print("Loading embedding model...")
#     llm = getEmbeddingModel()
#     print(llm.model_name + " loaded✅")

#     # Use VectorStoreIndex to create a index directly from chunks
#     print("Creating embeddings...")
#     # Passing in model to function instead of using global variable.
#     index = VectorStoreIndex(chunks, embed_model=llm, show_progress=True)
#     print("Report successfully indexed✅")

#     # print (f"Report ID: {reportID}")
#     print(f"Report IDs: {reportIDs}")
#     #print(f"Total stored chunks: {collection.count()}")

#     return index

# if __name__ == "__main__":
#     # Split up for testing purposes (test case creation)
#     print((header())) #super awesome cool title
#     folder_path = get_folder_path(key = "last_folder_documents")
#     index = get_embed_vectorstoreindex(folder_path)

#     # We need to pass in the bedrock model as the query engine.
#     query_engine = index.as_query_engine(llm=getBedrockModelQueryEngine())
#     print("=====================================================================================================================================================================================================\n")
#     print("\033[1m| I have loaded your documents. What would you like to know?\033[0m") #bolded using ANSI escape

#     #loop user to ask mulitple questions for mulitple responses
#     while True:
#         query = input(
#             "\nAsk A Question (Enter 'exit' to leave): "
#         ).strip()

#         if query.lower() == 'exit':
#             print(f"\nBye!")
#             break

#         response = query_engine.query(query)
#         print(f"\n\033[1m| {response}\033[0m") #bolded using ANSI escape

        