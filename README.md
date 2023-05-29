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

## [License](LICENSE)

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

**This software is provided by the copyright holders and contributors "as is"
and any express or implied warranties, including, but not limited to, the
implied warranties of merchantability and fitness for a particular purpose are
disclaimed. In no event shall the copyright holder or contributors be liable
for any direct, indirect, incidental, special, exemplary, or consequential
damages (including, but not limited to, procurement of substitute goods or
services; loss of use, data, or profits; or business interruption) however
caused and on any theory of liability, whether in contract, strict liability,
or tort (including negligence or otherwise) arising in any way out of the use
of this software, even if advised of the possibility of such damage.**
