# KeyBind TUI Application

## Overview

This is a Text User Interface (TUI) application that allows users to manage keybindings and categories. The application enables users to add new keybindings, categorize them, and navigate through them in a structured manner. The TUI interface uses `textual` to build interactive and easy-to-navigate screens.

## Features

- **Add Keybinds**: Users can add new keybindings by specifying the keys, description, and category.
- **Category Management**: Users can select a category to filter keybindings by category.
- **Scrollable Grid**: A scrollable table is available to display the keybindings, making navigation seamless.
- **Keybinding Display**: The keybindings are displayed with their associated keys and descriptions.
- **Quit Dialog**: The application provides a quit dialog to confirm whether users want to exit the application.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Thompson6626/BindVault.git
    cd BindVault
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python app/main.py
    ```

## Usage

1. **Navigating Keybinds**: Use the arrow keys to scroll through the list of keybindings in the grid.
2. **Adding a Keybind**: Press `a` to add a new keybind. A dialog will appear where you can enter the keybinding, description, and select the category.
3. **Category Selection**: Navigate through the categories in the sidebar. The keybind grid will automatically update to display keybindings related to the selected category.
4. **Quit the Application**: Press `q` to quit the application, a confirmation dialog will appear asking if you're sure you want to quit.

## Screenshots

_(Add screenshots here once your app is visually complete.)_

## TODO

### Features to Implement:

- **Update Keybind**: Add functionality to update an existing keybind's keys, description, or category.
- **Delete Keybind**: Implement a method to delete an existing keybind from the list.
- **Update Category**: Implement functionality to update an existing category's name.
- **Delete Category**: Allow users to delete categories, with the appropriate handling of associated keybindings.
- **Search Functionality**: Allow users to search for keybindings and categories more easily.
- **Pagination**: Add pagination to handle a large number of keybindings for better performance.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push to your forked repository.
5. Create a pull request with a description of your changes.