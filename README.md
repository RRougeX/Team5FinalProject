# Team 5 Malware RAG

A Python-based Retrieval-Augmented Generation (RAG) system that helps cybersecurity analysts search malware intelligence reports and generate structured threat-hunting reports.

The application processes approved malware documents, retrieves evidence relevant to an analyst's question, and provides that evidence to Amazon Nova through AWS Bedrock. This grounds generated responses in the supplied source material instead of relying only on the model's general training data.

## Features

- Loads malware intelligence reports from a user-selected folder
- Splits documents into smaller searchable chunks with LlamaIndex
- Generates embeddings locally with `BAAI/bge-small-en-v1.5`
- Stores chunks, vectors, and metadata persistently in ChromaDB
- Retrieves the five most relevant chunks for each analyst query
- Generates responses with Amazon Nova through AWS Bedrock
- Creates structured threat-hunting reports in Markdown format
- Allows existing embedding data to be reused without reprocessing the source documents
- Provides built-in AWS credential entry and validation

## How It Works

1. Malware reports are loaded and divided into text chunks.
2. The local BGE model converts each chunk into a numerical embedding.
3. ChromaDB stores the embeddings, source text, and metadata.
4. An analyst enters a question or requests a final report.
5. ChromaDB retrieves the chunks most closely related to the request.
6. Amazon Nova uses the retrieved evidence to generate the response.

## Technology Stack

| Component | Purpose |
| --- | --- |
| Python | Coordinates the application and RAG pipeline |
| LlamaIndex | Loads documents, creates chunks, and connects retrieval components |
| BGE Small EN v1.5 | Generates embeddings locally on the CPU |
| ChromaDB | Stores and retrieves persistent vector data |
| Amazon Nova Pro | Generates answers and threat-hunting reports |
| AWS Bedrock | Provides managed access to Amazon Nova |
| Boto3 | Validates and manages the AWS connection |

## Requirements

- Python 3.14
- Git
- Internet access for the initial BGE model download and AWS Bedrock requests
- AWS credentials with access to Amazon Bedrock and `amazon.nova-pro-v1:0`

Pluralsight AWS Sandbox credentials are temporary and may need to be replaced between sessions. A valid AWS identity does not automatically guarantee permission to invoke Amazon Nova.

## Quick Start

Clone the repository:

```bash
git clone https://github.com/RRougeX/Team5FinalProject.git
cd Team5FinalProject
```

### Windows

Create a virtual environment and install the dependencies:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the application:

```powershell
.\.venv\Scripts\python.exe src\main.py
```

### Linux

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start the application:

```bash
python src/main.py
```

## Usage

When the application starts, select one of the following options:

1. **Change AWS Bedrock AI keys** — enter or replace the AWS access key, secret key, and region.
2. **Load or create embedding data and run a model** — load an existing ChromaDB knowledge base or create one from source documents.
3. **Exit** — close the application.

After the documents and models are loaded, the user can:

- Ask questions about the supplied malware reports.
- Enter `2` to create a final threat-hunting report.
- Enter `back` to return to the main menu.

Generated reports are saved as timestamped Markdown files in the `reports` folder.

## Project Structure

```text
Team5FinalProject/
|-- data/
|   |-- raw/                    # Source malware reports
|   `-- processed/              # Persistent ChromaDB data
|-- reports/                    # Generated threat-hunting reports
|-- src/
|   |-- main.py                 # Application entry point
|   |-- system/
|   |   |-- indexReport.py      # Document loading and chunking
|   |   |-- models.py           # BGE and Amazon Nova configuration
|   |   |-- chromaDB.py         # Vector database creation and loading
|   |   `-- queryManager.py     # Questions and report generation
|   |-- tools/                  # Menus, paths, logging, and AWS key tools
|   `-- testing/                # Automated tests
|-- requirements.txt
|-- pytest.ini
|-- DEPLOYMENT_DOCUMENTATION.md
`-- README.md
```

## Testing

Run the automated tests from the project root:

```bash
python -m pytest src/testing
```

Verify installed dependency compatibility with:

```bash
python -m pip check
```

## Security Considerations

- Never commit or share `config.ini` or active AWS credentials.
- Keep `.venv`, local ChromaDB data, and other generated files out of version control when appropriate.
- Treat embedding databases as sensitive when their source documents contain restricted information.
- Use only trusted malware reports and documents as source material.
- Review AI-generated answers and reports before using them for security decisions.

## Documentation

See the [Deployment Documentation](./Team5DeploymentDocumentation.pdf) for detailed installation instructions, configuration guidance, method-by-method explanations, usage screenshots, troubleshooting, and deployment verification.

The README intentionally provides only the project overview and standard operating workflow. Detailed source-code methods are maintained in the deployment documentation to avoid duplicating information in multiple locations.

## Important Notes

- The BGE model downloads automatically during its first use and is cached for future sessions.
- Creating embeddings may take several minutes depending on the number and size of the documents.
- Loading existing embedding data avoids processing the same reports again.
- Access to Nova Pro depends on the policies of the active AWS account or sandbox.
- Responses are limited to the information available in the retrieved document context and may not contain every detail from every source report.

## Project Team

Developed by Team 5 as a cybersecurity RAG and threat-hunting project.
