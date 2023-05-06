# Wiki.py
A simple wiki server written in Python 3.

[Docs](https://tylerms887.github.io/wiki.py)

## Install

> **Warning**: `pip` must be installed to install Wiki.py.
`pip` is used to install neccesary dependencies and the wiki largely depends on it.
SQLite is also required, so the server can store the wiki pages.
Of course, the `questionary` module is required to show the UI for the installer
and show questions.

1. Go to your server folder, or create a new one
2. Run the following commands:
   ```shell
   curl -fsSL https://raw.githubusercontent.com/TylerMS887/wiki.py/main/install.py > install.py
   python3 install.py
   ```
3. Go through each step
4. Exit the installer, and run the following commands:
   ```shell
   rm install.py
   python3 wiki.py
   ```
