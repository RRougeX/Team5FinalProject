import json
import hashlib
from pathlib import Path
from datetime import datetime


def ingestText(inputPath: Path, outputDirectory: Path) -> Path:

    #read file
    reportText = inputPath.read_text(encoding='utf-8').strip()

    if not reportText:
        raise ValueError(f"Input file {inputPath} is empty.")

    reportID = hashlib.sha256(reportText.encode('utf-8')).hexdigest()[:16]

    #info to record
    record = {
        "reportID": reportID,
        "title": inputPath.stem.replace('_', ' ').title(),
        "sourceFile": inputPath.name,
        "date": datetime.now().isoformat(),
        "rawText": reportText,
    }

    #json structuring and directing output to the processed folder
    outputDirectory.mkdir(parents=True, exist_ok=True)
    outputPath = outputDirectory / f"{reportID}.json"

    outputPath.write_text(
        json.dumps(record, indent=2),
        encoding='utf-8',
    )

    return outputPath

if __name__ == "__main__":
    createdFile = ingestText(
        #change file name here to test
        Path("/home/team5/PROJECT/Team5FinalProject/data/raw/AR26-113A_MAR_FIRESTARTER_backdoor.pdf"),
        Path("data/processed"),
    )

    print(f"Created: {createdFile}")