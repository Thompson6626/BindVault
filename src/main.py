from typing import Optional, Callable

from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll, Horizontal
from textual.widgets import Footer, Header, Static, ListView, ListItem, DataTable,Button, Label , Select, Input
from textual.screen import ModalScreen
from textual.containers import  Grid

import asyncio


from db import Category, KeyBind, init_db, get_categories, get_keybinds, insert_category, insert_keybind


class AddKeyBindScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Grid(
            Input(placeholder="Ctrl + C", id="keys"),
            Input(placeholder="Copy the text highlighted", id="description"),
            Select([(cat.name, cat.id) for cat in CATEGORIES], id="categories", type_to_search=True,allow_blank=False),
            Button("Add", variant="primary", id="add"),
            Button("Cancel", variant="default", id="cancel"),
            id="add_keybind_dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            keys_input = self.query_one("#keys", Input).value
            description_input = self.query_one("#description", Input).value
            category_id: Select = self.query_one("#categories", Select).value
            keybind = insert_keybind(keys_input, description_input, category_id)
            if keybind:
                KEYBINDS[keybind.category_id].append(keybind)
                self.app.keybind_grid.add_to_grid(keybind)

        self.app.pop_screen()

class AddCategoryScreen(ModalScreen):
    
    def compose(self) -> ComposeResult:
        yield Grid(
            Input(placeholder="New category", id="new_category"),
            Button("Add", variant="primary", id="add"),
            Button("Cancel", variant="default", id="cancel"),
            id="add_category_dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            category_name = self.query_one("#new_category", Input).value
            category = insert_category(category_name)
            if category:
                CATEGORIES.append(category)
                self.app.sidebar.populate_sidebar()

        self.app.pop_screen()

class QuitScreen(ModalScreen):
    """Screen with a dialog to quit."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()

class Sidebar(Vertical):
    """Sidebar widget for listing categories."""
    def __init__(self, on_category_selected: Callable[[Optional[int]], None], **kwargs):
        super().__init__(**kwargs)
        self.on_category_selected = on_category_selected
        self.list_view = ListView()

    def compose(self) -> ComposeResult:
        yield Static("📜 Archive", classes="header")
        yield self.list_view

    async def on_mount(self) -> None:
        """Populate sidebar after mount."""
        self.populate_sidebar()

    def populate_sidebar(self):
        """Fill sidebar with category items."""
        for category in CATEGORIES:
            self.list_view.append(ListItem(Static(category.name), id=f"category-{category.id}"))

    def add_sidebar(self,category: Category) :
        self.list_view.append(ListItem(Static(category.name),id=f"category-{category.id}"))

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle selection events from ListView."""
        try:
            category_id = int(event.item.id.split("-")[1])
            self.on_category_selected(category_id)
        except (IndexError, ValueError):
            self.on_category_selected(0)


class KeyBindGrid(VerticalScroll):
    """Scrollable table for displaying keybindings."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = DataTable(zebra_stripes=True)

    def compose(self) -> ComposeResult:
        yield Static("🎹 Keybindings", classes="header")
        yield self.table

    async def on_mount(self) -> None:
        """Setup the table layout."""
        self.table.add_columns("Keys", "Description")
        self.update_grid(1)  # General index

    def update_grid(self, category_id: int):
        """Refresh keybinding rows."""
        self.table.clear()
        keybinds = KEYBINDS[category_id]

        for kb in keybinds:
            self.table.add_row(kb.keys, kb.description, key=kb.id)
    def add_to_grid(self, keybind: KeyBind):
        self.table.add_row(keybind.keys,keybind.description,key=keybind.keys)


class KeyBindApp(App):
    """Main application UI class."""
    CSS = """
    Horizontal {
        height: 100%;
    }
    Sidebar {
        width: 30%;
        border: round white;
        padding: 1;
        overflow: auto;
    }
    .header {
        text-align: center;
        content-align: center middle;
        height: 3;
    }
    """

    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("q,Q", "request_quit", "Quit"),
        ("a,A", "add_keybind", "Add keybind"),
        ("x,X","add_category","Add category"),
        ("up", "move_up", "Move Up"),
        ("down", "move_down", "Move Down"),
        ("enter", "select", "Select"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        self.sidebar = Sidebar(self.update_keybinds)
        self.keybind_grid = KeyBindGrid()
        yield Horizontal(self.sidebar, self.keybind_grid)
        yield Footer()

    def update_keybinds(self, category_id: int):
        """Trigger grid update on category selection."""
        self.keybind_grid.update_grid(category_id)

    def action_request_quit(self) -> None:
        """Action to display the quit dialog."""
        self.push_screen(QuitScreen())

    def action_add_keybind(self) -> None:
        """Action to display the add keybind dialog."""
        self.push_screen(AddKeyBindScreen())

    def action_add_category(self) -> None:
        self.push_screen(AddCategoryScreen())

    def action_move_up(self) -> None:
        """Move up through the sidebar categories."""
        self.sidebar.list_view.action_cursor_up()

    def action_move_down(self) -> None:
        """Move down through the sidebar categories."""
        self.sidebar.list_view.action_cursor_down()

    def action_select(self) -> None:
        """Select a category."""
        self.sidebar.list_view.action_submit()
    


async def init():
    global CATEGORIES
    CATEGORIES = await get_categories()
    global KEYBINDS
    KEYBINDS = await get_keybinds()

if __name__ == "__main__":
    init_db()
    asyncio.run(init())
    KeyBindApp().run()