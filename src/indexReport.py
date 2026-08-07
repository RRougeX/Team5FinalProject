import hashlib
import argparse
from pathlib import Path
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

def CreateReportID(report: Path) -> str:
    reportBytes = report.read_bytes()
    return hashlib.sha256(reportBytes).hexdigest()[:16]

def loadAndChunkReport(reportPath: Path, sourceOrganization: str):
    if not reportPath.exists():
        raise FileNotFoundError(f"Report not found {reportPath}")

    #ID file
    reportID = CreateReportID(reportPath)

    #load pdf through indexer (extract so python can read it)
    documents = SimpleDirectoryReader(input_files=[str(reportPath)]).load_data()
    print(f"Documents loaded: {len(documents)}")

    #add information that we will use for ChromaDB later
    for document in documents:
       document.metadata.update({
            "reportID": reportID,
            "title": reportPath.stem.replace("_", " ").title(),
            "sourceFile": reportPath.name,
            "sourceOrganization": sourceOrganization,
        })

    #split in chunks
    splitter = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=50,
    )

    chunks = splitter.get_nodes_from_documents(documents)
    print(f"Chunks created: {len(chunks)}")

    return reportID, documents, chunks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load and chunk a report.")
    parser.add_argument("reportPath", type=Path, help="Path to the report file.")
    parser.add_argument("sourceOrganization", type=str, help="Source organization of the report.")

    args = parser.parse_args()

    reportID, documents, chunks = loadAndChunkReport(args.reportPath, args.sourceOrganization)

    print(f"Report ID: {reportID}")
    print(f"Number of documents loaded: {len(documents)}")
    print(f"Number of chunks created: {len(chunks)}")

    # #testing
    # if chunks:     
    #     print("\nFirst Chunks:")
    #     print(chunks[0].text)
    #     print("\nFirst Chunks metadata:")
    #     print(chunks[0].metadata)
    # else:
    #     print("No chunks were created.")

