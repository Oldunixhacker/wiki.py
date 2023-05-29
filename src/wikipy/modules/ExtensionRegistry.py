#!/usr/bin/python3
# Extension registry script containing utilities for extensions.

if __name__ != "Wikipy":
  def raiseIncompatibleImportError():
    print("This script is a module that can only be imported by the wiki software. See README.md for more information.")
    raise ImportError
  raiseIncompatibleImportError()

class WikiPyExtensionException(Exception):
    pass

import os

def wpyLoadExtension(extension):
  """Loads an extension's scripts.

  Args:
    extension: The name of the extension to load.

  Returns:
    None.
  """

  # Get the path to the extension.
  extension_path = os.path.join(wikipy, "extensions", extension)

  # Open the extension file.
  with open(extension_path + "/pyExtScript.py", "r") as f:
    source = f.read()

  # Execute the extension file.
  try:
    exec(source)
  except:
    raise WikiPyExtensionException("Failed to load extension. (Did you run softwareUpdate.py?)")
def wpyLoadSkin(skin):
  """Loads a skin's scripts.

  Args:
    skin: The name of the skin to load.

  Returns:
    None.
  """

  # Get the path to the skin.
  skin_path = os.path.join(wikipy, "skins", skin)

  # Open the extension file.
  with open(skin_path + "/pySkinScript.py", "r") as f:
    source = f.read()

  # Execute the extension file.
  try:
    exec(source)
  except:
    print("Failed to import skin, ignoring")
