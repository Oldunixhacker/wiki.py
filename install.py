# Import requests, pip, configparser, questionary and os
import requests
import configparser
import questionary
import os

# Define the URL to download the wiki.py file
WIKI_URL = "https://raw.githubusercontent.com/TylerMS887/wiki.py/main/src/wiki.py"

# Define the list of dependencies to install
DEPENDENCIES = ["Flask", "questionary"]

# Define the default options for the wiki server
DEFAULT_OPTIONS = {
    "title": "Wiki.py",
    "wikiViewerName": "Wiki.py"
}

# Define the path to the configuration file that stores the wiki options
CONFIG_FILE = "wikipy-options.py"

# Define the title and content of the new page to create after the setup
NEW_PAGE_TITLE = "Main Page"
NEW_PAGE_CONTENT = "Wiki.py has been installed."

# Define a function that installs the dependencies using pip
def install_dependencies():
    # Check if pip is installed
    try:
        import pip
    except ImportError:
        # Raise an exception if not
        raise Exception("pip is not installed. Please install it before running this installer.")
    # Install the dependencies using pip
    for dep in DEPENDENCIES:
        os.system("python3 -m pip install " + dep)

# Define a function that downloads the wiki.py file and saves it as a local file
def download_wiki():
    # Download the wiki.py file using requests
    response = requests.get(WIKI_URL)
    with open("wiki.py", "wb") as f:
        f.write(response.content)

# Define a function that asks the user to select a language for their wiki using questionary and updates the default options with it
def configure_wiki():
    # Ask the user to select a language for their wiki using questionary
    language = questionary.select(
        "What language do you want to use for your wiki? (In ISO code)",
        choices=["en", "es", "fr", "de", "zh", "ja", "ru", "ar", "hi", "Other"]
    ).ask()
    # If the user selects "Other", ask them to enter the ISO language code
    if language == "Other":
        language = questionary.text("Please enter the ISO language code (e.g. en, es, fr)").ask()
    # Update the default options with the selected language
    DEFAULT_OPTIONS["language"] = language

# Define a function that creates a new configuration file with the default options, imports the wiki module and creates a new page using its functions, and makes the new page the homepage by updating the wiki module's home function
def install_wiki():
    # Create a new configuration file with the default options using configparser
    config = configparser.ConfigParser()
    config["DEFAULT"] = DEFAULT_OPTIONS
    with open(CONFIG_FILE, "w") as f:
        config.write(f)
    # Import the wiki module and create a new page using its functions
    import wiki
    wiki.create_table()
    wiki.write_page(NEW_PAGE_TITLE, NEW_PAGE_CONTENT)
    # Make the new page the homepage by updating the wiki module's home function
    def home():
        return view_page(NEW_PAGE_TITLE)
    wiki.home = home

# Define a function that prints a message to indicate the successful installation and creation of the new page
def finish_wiki():
    print("Wiki.py has been installed successfully. A new page titled '{}' has been created as your homepage. You have selected '{}' as your wiki language. You can run the wiki server by typing 'python wiki.py' in your terminal.".format(NEW_PAGE_TITLE, DEFAULT_OPTIONS["language"]))

# Define a list of steps for the installer with their names and functions
STEPS = [
    {"name": "Dependencies", "function": install_dependencies},
    {"name": "Download", "function": download_wiki},
    {"name": "Configure", "function": configure_wiki},
    {"name": "Install", "function":install_wiki},
    {"name": "Finished", "function": finish_wiki}
]

# Define a variable to store the current step index
current_step = 0

# Define a loop that runs until the user exits or finishes the installer
while True:
    # Create a list of choices for the installer menu based on the current step
    choices = []
    for i, step in enumerate(STEPS):
        if i < current_step:
            # If the step is already done, mark it as done and disable it
            choices.append({"name": f"✓ {step['name']}", "disabled": True})
        elif i == current_step:
            # If the step is the current one, mark it as current and enable it
            choices.append({"name": f"{step['name']}", "enabled": True})
        else:
            # If the step is not yet done, mark it as pending and disable it
            choices.append({"name": f"… {step['name']}", "disabled": True})
    # Add an exit option to the choices
    choices.append("Cancel Installation")
    # Ask the user to select an option using questionary
    option = questionary.select(
        f"Installing Wiki.py ({current_step}/5)",
        choices=choices
    ).ask()
    # Check if the user selected an exit option
    if option == "X Cancel installation":
        # If so, break the loop
        break
    else:
        # If not, execute the function of the current step and increment the current step index
        STEPS[current_step]["function"]()
        current_step += 1
