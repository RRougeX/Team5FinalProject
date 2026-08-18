import hashlib
from pathlib import Path
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

def CreateReportID(report: Path) -> str:
    report = Path(report)
    reportBytes = report.read_bytes()
    return hashlib.sha256(reportBytes).hexdigest()[:16]

def loadAndChunkReports(listOfReportPaths: list[Path], sourceOrganization: str):
    try:
        if listOfReportPaths is None or len(listOfReportPaths) == 0:
            raise FileNotFoundError(f"List of reports is empty or None: {listOfReportPaths}")

        #ID each file
        reportIDs = []
        allDocuments = []

        for reportPath in listOfReportPaths:
            reportID = CreateReportID(reportPath)
            reportIDs.append(reportID)

            #load pdf through indexer (extract so python can read it)
            documents = SimpleDirectoryReader(input_files=[str(reportPath)]).load_data()
            print(f"Documents loaded from Report[{reportID}]: {len(documents)}")

            #add information that we will use for ChromaDB later
            for document in documents:
                document.metadata.update({
                        "reportID": reportID,
                        "title": reportPath.stem.replace("_", " ").title(),
                        "sourceFile": reportPath.name,
                        "sourceOrganization": sourceOrganization,
                    })

            allDocuments.extend(documents)

        #split in chunks
        splitter = SentenceSplitter(
            chunk_size=512,
            chunk_overlap=50,
        )

        chunks = splitter.get_nodes_from_documents(allDocuments)
        print(f"Chunks created: {len(chunks)}")

        return reportIDs, allDocuments, chunks
    except FileNotFoundError as e:
        print(e)
        return None, None, None