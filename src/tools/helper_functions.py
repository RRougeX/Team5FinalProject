
def options_printer(options_text = ["!!!NO OPTIONS INPUTED!!!"], question = "What would you like to do?", user_input=""):
    """
    Takes in a list of string which will be the options the user can select from. These options will be numerically assigned in order starting from 1.
    Returns a users input.
    """

    if len(options_text) <= 0:
        return ""

    options = []

    print(f"\n{question}")
    for i, option in enumerate(options_text, start=1):
        print(f"{i}. {option}")
        options.append(str(i))

    choices_str = {', '.join(options)}

    # This line is just for making testing automatable.
    if user_input != "":
        return user_input

    while True:
        user_input = input(
                f"Enter your choice: {choices_str}\n: "
            ).strip()

        if user_input not in options:
            print(f"Invalid choice. Please enter a valid option number: {choices_str}")
            continue

        return user_input