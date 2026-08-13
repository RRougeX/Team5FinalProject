"""
config_manager.py

Handles a config.ini file that remembers the last-used folder path,
and provides a helper to recursively list all files inside a folder.
"""

import configparser
import os
from pathlib import Path

CONFIG_FILE = "config.ini"
SECTION = "Settings"
DEFAULT_KEY = "last_folder"

def get_config_file_path():
    return load_config()

def load_config(config_path: str = CONFIG_FILE) -> configparser.ConfigParser:
    """Load the config file, creating an empty parser if it doesn't exist."""
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
    return config

def load_config_and_get_section(config_path: str = CONFIG_FILE, section = SECTION) -> dict:
    """Calls 'load_config' and trys to load the section requeted. Returns a valid section on success, and empty {} on fail."""
    config = load_config(config_path)
    if section in config:
        return config[section]
    return {}

def save_config(config, config_path:str = CONFIG_FILE):
    """
    Make sure to load in the main config before adding new variables in saving. 
    Otherwise, you will create a new config and overwrite old data.
    """
    with open(config_path, "w") as f:
        config.write(f)

def save_key_to_config(key: str, folder_path: str, config_path: str = CONFIG_FILE) -> None:
    """
    Save the given folder path under `key` in the config file.
    Reads the existing file first so other keys aren't wiped out.
    """
    config = load_config(config_path)
    if SECTION not in config:
        config[SECTION] = {}
    config[SECTION][key] = str(folder_path)
    with open(config_path, "w") as f:
        config.write(f)


def get_saved_folder(key: str = DEFAULT_KEY, config_path: str = CONFIG_FILE) -> str | None:
    """Return the folder path saved under `key`, or None if not set."""
    config = load_config(config_path)
    if SECTION in config and key in config[SECTION]:
        return config[SECTION][key]
    return None


def prompt_for_folder(prompt_text: str = "Please enter the folder path where your documents are stored: ", prompt_for_new_folder = False) -> str:
    """Ask the user to enter a folder path, validating it exists."""
    while True:
        folder = input(prompt_text).strip()

        # Add the ability to use ./ as suffix to save the folder path relative to the current working directory
        if folder.startswith("./"):
            folder = os.path.abspath(folder)
            print("Absolute folder path:", folder)

        if os.path.isdir(folder):
            return folder
        else:
            if prompt_for_new_folder:
                out = input(f"Folder [{folder}] was not found. Create it? (y/N): ")
                if out.lower() == "y" or out.lower() == "yes":
                    os.makedirs(folder, exist_ok=True)
                    return folder
            
        try_again = input(f"'{folder}' is not a valid directory. Try again? (y/N).")
        try_again = try_again.lower()
        if try_again == "y" or try_again == "yes":
            continue
        else:
            return None


def get_folder_path(key: str = DEFAULT_KEY, config_path: str = CONFIG_FILE, prompt_text=None, prompt_for_new_folder = False) -> str:
    """
    Main entry point for startup logic, keyed so multiple folder
    "slots" (e.g. "last_folder_user_input_1", "last_folder_user_input_2")
    can be tracked independently in the same config file:
    - If no saved path exists for this key, prompt the user and save it.
    - If a saved path exists, ask whether to reuse it or enter a new one.
    Returns the folder path to use for this session.
    """

    # Simple fix for prompt text.
    if prompt_text is None:
        prompt_text = "Please enter the folder path where your documents are stored: "

    saved_folder = get_saved_folder(key, config_path)

    if not saved_folder:
        folder = prompt_for_folder(prompt_text)
        save_key_to_config(key, folder, config_path)
        return folder

    answer = input(
        f"Last used folder for '{key}' was:\n  {saved_folder}\nUse this folder again? (Y/n): "
    ).strip().lower()

    if answer in ("", "y", "yes"):
        if os.path.isdir(saved_folder):
            return saved_folder
        print("That folder no longer exists. Please choose a new one.")
        folder = prompt_for_folder(prompt_text=prompt_text, prompt_for_new_folder=prompt_for_new_folder)
    else:
        folder = prompt_for_folder(prompt_text=prompt_text, prompt_for_new_folder=prompt_for_new_folder)

    save_key_to_config(key, folder, config_path)
    return folder


def list_files_recursive(folder_path: str) -> list[Path]:
    """
    Recursively search the given folder (and all subfolders) and
    return a list of full file paths (as Path objects) for every file found.
    """
    return [
        Path(root) / filename
        for root, _dirs, files in os.walk(folder_path)
        for filename in files
    ]


if __name__ == "__main__":
    # Example: two independently-remembered folders
    folder_1 = get_folder_path("last_folder_user_input_1")
    print(f"\nUsing folder 1: {folder_1}\n")

    folder_2 = get_folder_path("last_folder_user_input_2")
    print(f"\nUsing folder 2: {folder_2}\n")

    files = list_files_recursive(folder_1)
    print(f"Found {len(files)} file(s) in folder 1:")
    for f in files:
        print(f"  {f}")