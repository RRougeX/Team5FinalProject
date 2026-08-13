from system.models import getBedrockModelQueryEngine


def start_query_manager(index):
    # Connect the loaded RAG index to Amazon Nova
    query_engine = index.as_query_engine(
        llm=getBedrockModelQueryEngine(),
        similarity_top_k=5
    )

  
    print(
        "\n========================================"
        "\n\033[1m| I have loaded your documents. "
        "What would you like to know?\033[0m"
    )

    while True:
        query = input(
            "\nAsk a Question (Enter 'back' to Return): "
        ).strip()

        if query.lower() == "back":
            print("\nReturning to the main menu.")
            return

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