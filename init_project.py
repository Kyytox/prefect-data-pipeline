import json
import os
from cookiecutter.main import cookiecutter


def get_line_for_insert(content_pyproj):
    """
    Get the line number for inserting dependencies in pyproject.toml.

    Args:
        content_pyproj (str): Content of the pyproject.toml file.

    Returns:
        int: Line number for inserting dependencies.
    """
    # Find the dependencies section and first empty line after it
    start_index = content_pyproj.find("[tool.pixi.dependencies]")

    if start_index != -1:

        # Get substring starting from the section
        section_content = content_pyproj[start_index:]

        # Find first empty line using splitlines()
        lines = section_content.splitlines()

        for i, line in enumerate(lines):
            if line.strip() == "":
                insert_position = start_index + sum(len(l) + 1 for l in lines[:i])
                break
    else:
        print("Dependencies section not found in pyproject.toml")

    return insert_position


def update_pyproject_toml(content_pyproj, insert_position, select_libs):
    """
    Update the pyproject.toml file with the selected dependencies.
    """
    # Insert the selected dependencies at the insert position
    if insert_position:
        new_pyproject = (
            content_pyproj[:insert_position]
            + "\n".join([f"{lib}" for lib in select_libs])
            + "\n"
            + content_pyproj[insert_position:]
        )
        print("Dependencies inserted successfully.")
    else:
        print("Insert position not found, skipping insertion.")

    return new_pyproject


def get_version_libs(select_libs, json_libs):
    """
    Get the version of the librarys from the json file.

    Args:
        select_libs (list): List of selected libraries.
        json_libs (dict): Dictionary containing library dependencies.

    Returns:
        list: List of libraries with their versions.
    """
    new_libs = []

    for lib in select_libs:
        if lib in json_libs["dependencies"]:
            version = json_libs["dependencies"][lib]
            new_libs.append(version)
        else:
            print(f"Library {lib} not found in dependencies.json")

    return new_libs


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

    print("")
    print("============================================")
    print("          Create a new project")
    print("============================================")

    # get os path
    PATH = os.path.dirname(os.path.abspath(__file__))

    # get templates choice
    dict_templates = json.loads(open(os.path.join(PATH, "templates.json"), "r").read())

    # get list of libs
    json_libs = json.loads(open(os.path.join(PATH, "dependencies.json"), "r").read())

    # Choose between the templates
    print("")
    print("Choose a template:")
    print("")

    for template in dict_templates:
        print(
            f"  \033[1;35m{template['id']}.\033[00m\033[1;33m{template['name']} \033[00m"
        )
        print(f"  ---------------------------")
        print(f"  Description:")
        print(f"    {template['description']}")
        print("")
        print(f"  Dependencies:")
        print(f"    {template['dependencies']}")
        print("")

    # get response
    num_template = input("Enter the number of the template you want to use: ")
    print("")

    # check response
    num_template = check_response_template(num_template, dict_templates)

    # get the selected template where id = num_template
    selected_template = get_selected_template(dict_templates, num_template)

    # get the dependencies from the selected template
    select_libs = selected_template["dependencies"]

    # get version of the selected libraries
    select_libs = get_version_libs(select_libs, json_libs)

    # launch the cookiecutter command
    print("")
    print("Configure the project: ")
    print("")
    NEW_PATH = cookiecutter(
        PATH,
        output_dir=os.path.dirname(PATH),
    )

    # Read pyproject.toml
    with open(os.path.join(NEW_PATH, "pyproject.toml"), "r") as f:
        content_pyproj = f.read()

    # Get the line number for inserting dependencies
    insert_position = get_line_for_insert(content_pyproj)

    # Update pyproject.toml with the selected dependencies
    new_pyproject = update_pyproject_toml(content_pyproj, insert_position, select_libs)

    # Write the modified content back to pyproject.toml
    with open(os.path.join(NEW_PATH, "pyproject.toml"), "w") as f:
        f.write(new_pyproject)

    print("")
    print("================================================")
    print(f"        Project - {NEW_PATH.split('/')[-1]} - Created.")
    print(f"        {NEW_PATH}")
    print("================================================")
