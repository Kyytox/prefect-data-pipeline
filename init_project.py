import json
import os
from cookiecutter.main import cookiecutter


def check_response_template(num_template, dict_templates):
    """
    Check if the response is valid.

    Args:
        num_template (str): User input for template number.
        dict_templates (list): List of templates.

    Returns:
        int: Validated template number.
    """
    if not num_template.isnumeric():
        print("Invalid input. Please enter a number.")
        exit()

    num_template = int(num_template)

    if num_template < 1 or num_template >= len(dict_templates) + 1:
        print("Invalid input. Please enter a number between 1 and", len(dict_templates))
        exit()

    return num_template


def get_selected_template(dict_templates, num_template):
    """
    Get the selected template.

    Args:
        dict_templates (list): List of templates.
        num_template (int): Template number.

    Returns:
        dict: Selected template.
    """
    selected_template = next(
        (template for template in dict_templates if template["id"] == num_template),
        None,
    )

    if selected_template is None:
        print("Template not found.")
        exit()

    return selected_template


if __name__ == "__main__":

    # Colors
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    YELLOW = "\033[1;33m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    NC = "\033[0m"  # No Color

    print("")
    print(f"{BLUE}=" * 50)
    print(f"  {YELLOW}Welcome to the Prefect Data Pipeline Creator !{NC}")
    print(f"{BLUE}=" * 50)

    # get os path
    PATH = os.path.dirname(os.path.abspath(__file__))

    # get templates choice
    dict_templates = json.loads(open(os.path.join(PATH, "templates.json"), "r").read())

    # Choose between the templates
    print("")
    print("Choose a template:")
    print("")

    for template in dict_templates:
        print(f"  {PURPLE}{template['id']}.{YELLOW}{template['name']} {NC}")
        print(f"  {BLUE}-----------------{NC}")
        print(f"  {CYAN}Description :{NC} {template['description']}")
        print(f"  {CYAN}Dependencies :{NC} {template['dependencies']}")
        print("")
        print("")

    print("")
    # get response
    num_template = input("Enter the number of the template you want to use: ")
    print("")

    # check response
    num_template = check_response_template(num_template, dict_templates)

    # launch the cookiecutter command
    print("")
    print("Configure the project: ")
    print("")
    NEW_PATH = cookiecutter(
        os.path.join(PATH, f"template_{num_template}"),
        output_dir=os.path.dirname(PATH),
    )

    print("")
    print(f"{BLUE}=" * 50)
    print(f"    {YELLOW}Project - {NEW_PATH.split('/')[-1]} - Created.{NC}")
    print(f"    {YELLOW}{NEW_PATH}{NC}")
    print(f"{BLUE}=" * 50)
