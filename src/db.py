from collections import defaultdict
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

APP_NAME = "HotKeyVault"
CONFIG_DIR = Path.home() / ".config" / APP_NAME
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = CONFIG_DIR / "keybindings.db"

@dataclass
class KeyBind:
    id: int
    keys: str
    description: str
    category_id: Optional[int]

@dataclass
class Category:
    id: int
    name: str

def init_db() -> None:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS keybinds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keys TEXT UNIQUE NOT NULL,
            description TEXT,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES category (id) ON DELETE SET NULL
        );""")

        cursor.execute("""
        INSERT OR IGNORE INTO category (name) VALUES (?)
        """, ("General",))

        conn.commit()

async def get_categories() -> List[Category]:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM category")
        results = cursor.fetchall()
        return [Category(id,name) for (id,name) in results]

async def get_keybinds() -> Dict[int,List[KeyBind]]:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.cursor()

        query = """
        SELECT id, keys, description, COALESCE(category_id, -1) AS category_id
        FROM keybinds
        """

        cursor.execute(query)

        results = cursor.fetchall()
        by_category_id = defaultdict(list)

        for id, keys,description, category_id in results:
            by_category_id[category_id].append(KeyBind(id,keys, description, category_id))

        return by_category_id


def insert_keybind(keys: str, description: str, category_id: int) -> Optional[KeyBind]:
    try:
        new_keybind = None
        with closing(sqlite3.connect(DB_PATH)) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO keybinds (keys, description,category_id) VALUES (?, ?, ?) RETURNING id,keys,description,category_id", (keys, description, category_id))
            inserted_row = cursor.fetchone()
            new_keybind = KeyBind(*inserted_row)
            conn.commit()
        return new_keybind
    except sqlite3.IntegrityError as e:
        print(f"Database error: {e}")
        return new_keybind

def insert_category(name: str) -> Optional[Category]:
    """Inserts a new category and returns the created category if successful."""
    try:
        new_category = None
        with closing(sqlite3.connect(DB_PATH)) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO category (name) VALUES (?) RETURNING id, name", (name,))
            inserted_row = cursor.fetchone()
            new_category = Category(*inserted_row)
            conn.commit()
        return new_category
    except sqlite3.IntegrityError as e:
        print(f"Database error: {e}")
        return new_category

