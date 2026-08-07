from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

query = "What is a cyber attack?"

documents = SimpleDirectoryReader('/home/team5/PROJECT/Team5FinalProject').load_data()

index = VectorStoreIndex.from_documents(documents)

response = index.query(query)

print(response)
