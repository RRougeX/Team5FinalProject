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
KEY = "last_folder"


def load_config(config_path: str = CONFIG_FILE) -> configparser.ConfigParser:
    """Load the config file, creating an empty parser if it doesn't exist."""
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
    return config


def save_config(folder_path: str, config_path: str = CONFIG_FILE) -> None:
    """Save the given folder path to the config file."""
    config = configparser.ConfigParser()
    config[SECTION] = {KEY: folder_path}
    with open(config_path, "w") as f:
        config.write(f)


def get_saved_folder(config_path: str = CONFIG_FILE) -> str | None:
    """Return the saved folder path, or None if not set."""
    config = load_config(config_path)
    if SECTION in config and KEY in config[SECTION]:
        return config[SECTION][KEY]
    return None


def prompt_for_folder() -> str:
    """Ask the user to enter a folder path, validating it exists."""
    while True:
        folder = input("Please enter the folder path where your documents are stored: ").strip()
        if os.path.isdir(folder):
            return folder
        print(f"'{folder}' is not a valid directory. Please try again.")


def get_folder_path(config_path: str = CONFIG_FILE) -> str:
    """
    Main entry point for startup logic:
    - If no saved path exists, prompt the user and save it.
    - If a saved path exists, ask whether to reuse it or enter a new one.
    Returns the folder path to use for this session.
    """
    saved_folder = get_saved_folder(config_path)

    if not saved_folder:
        folder = prompt_for_folder()
        save_config(folder, config_path)
        return folder

    answer = input(
        f"Last used folder was:\n  {saved_folder}\nUse this folder again? (Y/n): "
    ).strip().lower()

    if answer in ("", "y", "yes"):
        if os.path.isdir(saved_folder):
            return saved_folder
        print("That folder no longer exists. Please choose a new one.")
        folder = prompt_for_folder()
    else:
        folder = prompt_for_folder()

    save_config(folder, config_path)
    return folder


def list_files_recursive(folder_path: str) -> list[str]:
    """
    Recursively search the given folder (and all subfolders) and
    return a list of full file paths for every file found.
    """
    file_paths = []
    for root, _dirs, files in os.walk(folder_path):
        for filename in files:
            file_paths.append(os.path.join(root, filename))
    return file_paths


if __name__ == "__main__":
    folder = get_folder_path()
    print(f"\nUsing folder: {folder}\n")

    files = list_files_recursive(folder)
    print(f"Found {len(files)} file(s):")
    for f in files:
        print(f"  {f}")