import json
import hashlib
from pathlib import Path
from datetime import datetime
from pypdf import PdfReader


def ingestPdf(inputPath: Path, outputDirectory: Path) -> Path:

    #page extract
    reader = PdfReader(inputPath)
    reportText = ""

    for page in reader.pages:
        reportText += (page.extract_text() or "") + "\n"

    reportText = reportText.strip()

    if not reportText:
        raise ValueError(f"PDF {inputPath} contains no readable text.")

    reportID = hashlib.sha256(
        reportText.encode("utf-8")
    ).hexdigest()[:16]

    #record info in PDF
    record = {
        "reportID": reportID,
        "title": inputPath.stem.replace("_", " ").title(),
        "sourceFile": inputPath.name,
        "date": datetime.now().isoformat(),
        "rawText": reportText,
    }

    #save
    outputDirectory.mkdir(parents=True, exist_ok=True)
    outputPath = outputDirectory / f"{reportID}.json"

    outputPath.write_text(
        json.dumps(record, indent=2),
        encoding="utf-8",
    )

    return outputPath


if __name__ == "__main__":
    projectRoot = Path(__file__).resolve().parent.parent
    #output
    createdFile = ingestPdf(
        projectRoot / "data/raw/AR26-113A_MAR_FIRESTARTER_backdoor.pdf",
        projectRoot / "data/processed",
    )

    print(f"Created: {createdFile}")