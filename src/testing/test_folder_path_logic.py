import configparser

import pytest

from tools.folder_path_logic import load_config, load_config_and_get_section, save_config, save_key_to_config

# Should return a new config.
def test_load_config_that_does_not_exist():
    config = load_config("NotARealConfig.ini")
    assert config != None

def test_load_config_and_get_section_that_does_not_exist():
    section = load_config_and_get_section(config_path="not_a_real_config.ini", section="FakeSection")
    assert section == {}

def test_save_config_new():
    # Create a new config
    config = configparser.ConfigParser()
    # add something to it
    config["Save"] = {
        "saved" : "This should have saved."
    }
    save_config(config=config, config_path="save_test.ini")
    loaded_saved_config = load_config("save_test.ini")
    assert loaded_saved_config["Save"] != {}
    assert loaded_saved_config["Save"]["saved"] == "This should have saved."

def test_save_config_replace():
    test_save_config_new()

    replace_config = configparser.ConfigParser()
    replace_config["Replace"] = {
        "replace" : "This is the replaced data."
    }
    save_config(config=replace_config, config_path="save_test.ini")
    loaded_saved_config = load_config("save_test.ini")
    assert loaded_saved_config["Replace"] != {}
    assert loaded_saved_config["Replace"]["replace"] == "This is the replaced data."
    with pytest.raises(KeyError):
        fail = loaded_saved_config["Save"]

# Fixed or to be fixed.
# (F)Issue 1, no way of calling a section manually. Forces you to use the default section
def test_save_key_to_config():
    test_save_config_new()

    save_key_to_config(key="added", pair="This is the data", section="Add", config_path="save_test.ini")
    config = load_config("save_test.ini")
    assert config["Add"]["added"] == "This is the data"

# If needed we could test the other functions in here, but most are just slight altercations that the AI made for itself.