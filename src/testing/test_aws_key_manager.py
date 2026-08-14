from pytest import MonkeyPatch

from Team5FinalProject.src.tools.aws_key_manager import enter_new_keys

def test_enter_new_keys():
    responses = iter(["aaa","bbb","us-east-1"])
    MonkeyPatch.setattr("bultins.input", lambda _: next(responses))

    enter_new_keys("testing_config")

    # We need to load our keys before we can test, 
    # we need to ensure our key loading is good before we test here though.
