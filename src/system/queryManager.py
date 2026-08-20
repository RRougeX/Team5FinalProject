from datetime import datetime
from pathlib import Path

from system.models import getBedrockModelQueryEngine


def create_final_report(query_engine):
    topic = input(
        "\nWhat would you like the final report to be about?\n: "
    ).strip()

    if not topic:
        print("Please enter a report topic.")
        return

    # Default prompt used to generate the report
    prompt = f"""
Create a professional cybersecurity threat-hunting report about {topic}.

Use only information supported by the provided documents.

Include:
- Executive Summary
- Malware Overview
- Technical Behaviors
- Indicators of Compromise
- MITRE ATT&CK Techniques
- Know Exploitable Vulnerabilities
- Threat-Hunting Recommendations
- Detection Recommendations
- Sources

Do not invent unsupported information.
"""

    print("\nCreating final report...")

    try:
        response = query_engine.query(prompt)

    except Exception as error:
        print(f"\nReport generation failed: {error}")
        return

    project_root = Path(__file__).resolve().parent.parent.parent
    reports_folder = project_root / "reports"

    reports_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    file_name = datetime.now().strftime(
        "final_report_%Y-%m-%d_%H-%M-%S.md"
    )

    report_path = reports_folder / file_name

    report_path.write_text(
        f"# Threat-Hunting Report: {topic}\n\n{response}",
        encoding="utf-8"
    )

    print("\n\033[1m| Final report created✅\033[0m")
    print(f"\033[1m| Saved to: {report_path}\033[0m")


def start_query_manager(index):
    # Connect the loaded RAG index to Amazon Nova
    query_engine = index.as_query_engine(
        llm=getBedrockModelQueryEngine(),
        similarity_top_k=5
    )

    print(
        "\n================================================================================"
        "\n\033[1m| I have loaded your documents. "
        "What would you like to know?\033[0m"
    )

    while True:
        query = input(
            "\nAsk a Question "
            "(Enter '2' to Create Final Report or 'back' to Return)...\n: "
        ).strip()

        if query.lower() == "back":
            print("\nReturning to the main menu.")
            return

        if query == "2":
            create_final_report(query_engine)
            continue

        if not query:
            print("\nPlease enter a question.")
            continue

        try:
            response = query_engine.query(query)
            print(f"\n\033[1m| {response}\033[0m")

        except KeyboardInterrupt:
            print("\n\nReturning to the main menu.")
            return

        except Exception as error:
            print(f"\nQuery failed: {error}")