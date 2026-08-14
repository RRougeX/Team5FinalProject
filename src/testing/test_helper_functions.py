from Team5FinalProject.src.tools.helper_functions import options_printer

def test_options_printer_empty():
    user_input = options_printer([])
    assert user_input == ""

def test_options_printer_1_option():
    user_input = options_printer(["op1"],user_input="1")
    assert user_input == "1"

def test_options_printer_many_options():
    user_input = options_printer(["op1","op2","op3","op4","op5"], user_input="5")
    assert user_input == "5"

# Manully test that the program loops when you put in a invalid input.