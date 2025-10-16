# Ulauncher GNOME Window Switcher

A fast and intelligent Ulauncher extension for switching to open windows across your desktop, leveraging fuzzy searching for quick access, even with very long window titles.

# Features

- Intelligent Fuzzy Search: Uses advanced fuzzy matching (rapidfuzz python library) to prioritize results based on a weighted key: WM_CLASS have more attention that window TITLE.

- Real-Time Window Data: Retrieves a complete list of open windows, including their titles and classes, via the D-Bus (GNOME Window Calls extension).

- Seamless Switching: Select an item to instantly focus and switch to that window.

- Dynamic Icons: Uses the WM_CLASS to provide appropriate application icons from your system's icon theme.

# Installation

Follow the standard procedure for adding Ulauncher extensions.

1. Open Ulauncher Preferences

   Open Ulauncher and go to **Extensions**.

2. Add the Extension URL

   Click Add Extension and paste the GitHub URL:[https://github.com/rafaelmelom-dev/ulauncher-gnome-window-switcher](https://github.com/rafaelmelom-dev/ulauncher-gnome-window-switcher)

3. Check Dependencies (If needed) This extension relies on Python packages for fuzzy matching and interacting with the window manager. Is used:
   - **pydbus**: Used for communicating with D-BUS - [https://pypi.org/project/pydbus/](https://pypi.org/project/pydbus/)
   - **rapidfuzz**: Used for matching a query, exclusively for search a window - [https://pypi.org/project/RapidFuzz/](https://pypi.org/project/RapidFuzz/)
   - **Window Calls (GNOME extension)**: This extension exposes windows to dbus interface, turning easy the task of listing windows - [https://extensions.gnome.org/extension/4724/window-calls/](https://extensions.gnome.org/extension/4724/window-calls/)

# Usage

The extension is triggered using its assigned keyword (default is **ws**).

1. Type the Keyword: Open Ulauncher (Ctrl+Space or whatever your hotkey is) and type the keyword: ws for default

2. Search: Start typing the name of the window you want to switch to (e.g., ws term or ws code).

3. Select: Press Enter on the desired window to activate it and close the Ulauncher window.

# Development

If you are contributing or debugging, you can run the extension in development mode to see verbose logging:

1. Stop running Ulauncher: `pkill ulauncher`

2. Run in development mode: `ulauncher --no-extensions --dev -v`
   (Your verbose logs, including the sorted windows information, will appear here.)

Key Files

`main.py`: Contains the core logic for querying windows and applying the weighted priority sort key.

`README.md`: This document.License

This project is licensed under the MIT License - see the LICENSE file for details.

Created by rafaelmelom-dev
