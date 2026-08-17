import sys
from tools.aws_key_manager import enter_new_keys, is_AWS_config_credentials_valid
from tools.title import header
from system.chromaDB import load_embedding_data, create_embedding_data
from tools.log_cleanup import cleanLogs
from tools.helper_functions import options_printer
from system.queryManager import start_query_manager

def load_or_create_embedding_data():
    user_input = options_printer(["Load existing embedding data", "Create new embedding data", "Back"])

    match user_input:
        case "1":
            print("Loading existing embedding data.")
            return load_embedding_data()

        case "2":
            print("Creating new embedding data.")
            return create_embedding_data()

        case "3":
            return None

def awsKeyCheck():
    user_input = options_printer(["Enter new keys", "Check if keys are valid", "Back (keep using current keys)"], "Pluralsight Sandbox Keys")

    match user_input:
        case "1":
            enter_new_keys()
        case "2":
            valid = is_AWS_config_credentials_valid()
            print(f"Keys are {'Valid' if valid else 'Invalid'}")
        case "3":
            return

#########################################################################################################

def main():
    cleanLogs()
    print(header())
    print("Welcome to Team 5 Malware RAG!")
    while True:
        user_input = options_printer(["Change AWS bedrock AI keys","Load or create embedding data and run a model","Exit"],"Select a option.")
        # Option 1
        match user_input:
            case "1":
                awsKeyCheck()
            case "2":
                # Check if AWS Keys are valid before continuing.
                if not is_AWS_config_credentials_valid():
                    print("Please fix your AWS keys in option 1.")
                    continue
                index = load_or_create_embedding_data()
                if index == None:
                    continue
                start_query_manager(index)
            case "3":
                print("Bye!")
                sys.exit(0)

#Run MAIN.PY
if __name__ == "__main__":
    main()