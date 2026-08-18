import builtins
from unittest.mock import patch

import pytest

from tools.aws_key_manager import enter_new_keys, is_AWS_config_credentials_valid
from tools.folder_path_logic import load_config, load_config_and_get_section

# Enter keys inputs should work fine, 
# but getting pytest to allow inputs with password is being very difficult.

def test_enter_new_keys_empty_should_break():
    with pytest.raises(OSError):
        enter_new_keys()

# (F) Issue 1, enter new keys path, is not actually saving to the given path.
def test_enter_new_keys_with_test_var():
    keys = {
        "access_key_id": "aaa",
        "secret_access_key": "bbb",
        "region": "us-east-1"
    }
    enter_new_keys("aws_test_config.ini", aws_section=keys)
    config = load_config("aws_test_config.ini")
    assert config["AWS"] != None

    assert config["AWS"]["access_key_id"] == "aaa"
    assert config["AWS"]["secret_access_key"] == "bbb"
    assert config["AWS"]["region"] == "us-east-1"

# keys = {
#         "access_key_id": "aaa",
#         "secret_access_key": "bbb",
#         "region": "us-east-1"
#     }
#     enter_new_keys(config_path="aws_test_config.ini" ,aws_section=keys)
def test_is_AWS_config_credentials_valid_bad_credentials():
    test_enter_new_keys_with_test_var()
    assert is_AWS_config_credentials_valid("aws_test_config.ini") == False

# !!!THIS TEST WILL FAIL IF YOU DON'T ADD IN YOUR VALID CREDENTIALS TO A CONFIG FILE THAT MATCHES THE INPUT!!!
def test_is_AWS_config_credentials_valid_good_credentials():
    # Please add valid keys to config file. You should not have them hardcode added.
    assert is_AWS_config_credentials_valid(config_path="aws_valid_keys_for_testing.ini") == True

def test_is_AWS_config_credentials_valid_good_credentials_bad_region():
    aws = load_config_and_get_section(config_path="aws_valid_keys_for_testing.ini",section = "AWS")
    keys = {
        "access_key_id": aws.get("access_key_id"),
        "secret_access_key": aws.get("secret_access_key"),
        "region": "bad-region"
    }
    assert is_AWS_config_credentials_valid(creds=keys) == False