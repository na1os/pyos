# pyos

# TerminalOS

A simulated command-line operating system written in Python. This project provides an interactive terminal interface that handles user authentication, a persistent flat-file system via JSON, and a functional command shell.

## Features
* **Boot Sequence:** Animated boot sequence featuring a customized ASCII logo.
* **Authentication:** Basic login system with username and masked password input.
* **File Manager:** Allows users to create, edit (using a lightweight inline editor with vi-like shortcuts), view, and delete files.
* **Shell:** A custom command shell (tsh) supporting standard operations (ls, cat, clear, matrix, save, exit).
* **State Persistence:** Automatically saves files and user configuration to `tos_state.json`.

## Getting Started
1. Ensure you have Python 3.x installed.
2. Download the `main.py` file.
3. Run the script from your terminal:
   ```bash
   python main.py
