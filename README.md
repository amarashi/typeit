# Typing Simulator

This project is a Typing Simulator GUI application built using Python and Tkinter. The application allows users to load text from a file or enter text manually, set initial and typing delays, and simulate typing the text in another window.
# Why?!

Because in some cases, you can not copy/paset text somewhere, so, you have to type a long text yourself and you are not a fast typer!

## Features

- Load text from a file or enter text manually.
- Set initial delay before typing starts.
- Set typing delay between each character.
- Simulate typing the text in another window.
- Stop typing at any time.

## Requirements

- Python 3.x
- Tkinter
- pyautogui

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/amarashi/typing-simulator.git
    cd typing-simulator
    ```

2. Install the required packages:
    ```sh
    pip install pyautogui
    ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

2. Enter the text you want to simulate typing or load a text file.
3. Set the initial delay (in seconds) before typing starts.
4. Set the typing delay (in seconds) between each character.
5. Click the "Start Typing" button and switch to your target window.

## File Explanation

### main.py

This file contains the main code for the Typing Simulator GUI application.

- **Imports**: The necessary modules are imported, including `tkinter`, `pyautogui`, `time`, and `threading`.
- **TypingSimulatorGUI Class**: This class defines the GUI and the functionality of the application.
  - `__init__(self, root)`: Initializes the GUI components, including text area, parameter inputs, buttons, and status label.
  - `load_file(self)`: Loads text from a selected file into the text area.
  - `simulate_typing(self, text, delay, initial_delay)`: Simulates typing the text with the specified delays. Shows a countdown from `initial_delay` to 0 before starting.
  - `start_typing(self)`: Starts the typing simulation in a separate thread.
  - `stop_typing_command(self)`: Stops the typing simulation.

### .gitignore

This file specifies the files and directories to be ignored by Git.

- **Byte-compiled / optimized / DLL files**: Ignores `__pycache__` and `.py[cod]` files.
- **Distribution / packaging**: Ignores `build/`, `dist/`, and `*.egg-info/` directories.
- **Unit test / coverage reports**: Ignores `.coverage` and `.pytest_cache/` files.
- **Virtual environment**: Ignores `venv/` and `.env` directories.
- **Logs**: Ignores `*.log` files.
- **IDE specific files**: Ignores `.vscode/` directory.

## License

This project is licensed under the MIT License.
