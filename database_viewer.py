import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# DATABASE LOCATION
# ============================================================

DATABASE = "student_result_management.db"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("Student Result Management - Database Viewer")
root.geometry("1200x700")
root.minsize(900, 600)


# ============================================================
# COLORS / FONTS
# ============================================================

BG_COLOR = "#f4f6f8"
HEADER_COLOR = "#1f2937"
BUTTON_COLOR = "#2563eb"
TEXT_COLOR = "#111827"


root.configure(bg=BG_COLOR)


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def get_connection():
    return sqlite3.connect(DATABASE)


def get_tables():
    """Return all user-created tables."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tables = [row[0] for row in cursor.fetchall()]

    conn.close()

    return tables


def load_table(table_name=None):
    """Load selected database table into Treeview."""

    if not table_name:
        table_name = table_combo.get()

    if not table_name:
        return

    try:

        conn = get_connection()
        cursor = conn.cursor()

        # Get column information
        cursor.execute(f'PRAGMA table_info("{table_name}")')
        columns_info = cursor.fetchall()

        columns = [column[1] for column in columns_info]

        # Get data
        cursor.execute(f'SELECT * FROM "{table_name}"')

        rows = cursor.fetchall()

        conn.close()

        # Clear old table
        for item in tree.get_children():
            tree.delete(item)

        # Configure columns
        tree["columns"] = columns

        tree["show"] = "headings"

        for column in columns:

            tree.heading(
                column,
                text=column.upper()
            )

            tree.column(
                column,
                width=130,
                minwidth=80,
                anchor="center"
            )

        # Insert rows
        for row in rows:
            tree.insert(
                "",
                "end",
                values=row
            )

        # Update record count
        record_count_label.config(
            text=f"Total Records: {len(rows)}"
        )

        current_table_label.config(
            text=f"Showing table: {table_name}"
        )

        # Clear search
        search_entry.delete(0, tk.END)

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to load table.\n\n{e}"
        )


def refresh_tables():
    """Refresh table list."""

    tables = get_tables()

    table_combo["values"] = tables

    if tables:

        table_combo.current(0)

        load_table(tables[0])


def search_table():
    """Search records currently loaded in the selected table."""

    search_text = search_entry.get().strip().lower()

    table_name = table_combo.get()

    if not table_name:
        return

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f'PRAGMA table_info("{table_name}")')

        columns_info = cursor.fetchall()

        columns = [column[1] for column in columns_info]

        cursor.execute(f'SELECT * FROM "{table_name}"')

        rows = cursor.fetchall()

        conn.close()

        # Clear table
        for item in tree.get_children():
            tree.delete(item)

        # Search
        if search_text:

            filtered_rows = []

            for row in rows:

                row_text = " ".join(
                    str(value).lower()
                    for value in row
                )

                if search_text in row_text:
                    filtered_rows.append(row)

        else:

            filtered_rows = rows

        # Insert filtered rows
        for row in filtered_rows:

            tree.insert(
                "",
                "end",
                values=row
            )

        record_count_label.config(
            text=f"Showing: {len(filtered_rows)} / {len(rows)} records"
        )

    except Exception as e:

        messagebox.showerror(
            "Search Error",
            str(e)
        )


def clear_search():

    search_entry.delete(0, tk.END)

    load_table()


# ============================================================
# HEADER
# ============================================================

header_frame = tk.Frame(
    root,
    bg=HEADER_COLOR,
    height=80
)

header_frame.pack(
    fill="x"
)

header_frame.pack_propagate(False)


title_label = tk.Label(
    header_frame,
    text="STUDENT RESULT MANAGEMENT",
    font=("Segoe UI", 20, "bold"),
    fg="white",
    bg=HEADER_COLOR
)

title_label.pack(
    pady=(12, 0)
)


subtitle_label = tk.Label(
    header_frame,
    text="Database Management & Record Viewer",
    font=("Segoe UI", 10),
    fg="#d1d5db",
    bg=HEADER_COLOR
)

subtitle_label.pack()


# ============================================================
# CONTROL FRAME
# ============================================================

control_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

control_frame.pack(
    fill="x",
    padx=20,
    pady=15
)


# Table label

tk.Label(
    control_frame,
    text="Select Table:",
    font=("Segoe UI", 11, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(
    side="left"
)


# Table dropdown

table_combo = ttk.Combobox(
    control_frame,
    width=25,
    state="readonly",
    font=("Segoe UI", 10)
)

table_combo.pack(
    side="left",
    padx=10
)


table_combo.bind(
    "<<ComboboxSelected>>",
    lambda event: load_table()
)


# Refresh button

refresh_button = tk.Button(
    control_frame,
    text="↻ Refresh",
    command=refresh_tables,
    bg=BUTTON_COLOR,
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=15,
    pady=7,
    cursor="hand2"
)

refresh_button.pack(
    side="left",
    padx=5
)


# Search label

tk.Label(
    control_frame,
    text="Search:",
    font=("Segoe UI", 11, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(
    side="left",
    padx=(25, 5)
)


# Search box

search_entry = tk.Entry(
    control_frame,
    width=25,
    font=("Segoe UI", 10)
)

search_entry.pack(
    side="left",
    ipady=6
)


# Search button

search_button = tk.Button(
    control_frame,
    text="Search",
    command=search_table,
    bg="#059669",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=15,
    pady=7,
    cursor="hand2"
)

search_button.pack(
    side="left",
    padx=5
)


# Clear button

clear_button = tk.Button(
    control_frame,
    text="Clear",
    command=clear_search,
    bg="#6b7280",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=15,
    pady=7,
    cursor="hand2"
)

clear_button.pack(
    side="left"
)


# ============================================================
# CURRENT TABLE LABEL
# ============================================================

current_table_label = tk.Label(
    root,
    text="Showing table:",
    font=("Segoe UI", 12, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

current_table_label.pack(
    anchor="w",
    padx=20,
    pady=(0, 5)
)


# ============================================================
# DATABASE TABLE FRAME
# ============================================================

table_frame = tk.Frame(
    root,
    bg="white"
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=5
)


# ============================================================
# TREEVIEW
# ============================================================

tree = ttk.Treeview(
    table_frame,
    show="headings"
)

tree.pack(
    side="left",
    fill="both",
    expand=True
)


# Vertical scrollbar

vertical_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

vertical_scrollbar.pack(
    side="right",
    fill="y"
)


tree.configure(
    yscrollcommand=vertical_scrollbar.set
)


# Horizontal scrollbar

horizontal_scrollbar = ttk.Scrollbar(
    root,
    orient="horizontal",
    command=tree.xview
)

horizontal_scrollbar.pack(
    fill="x",
    padx=20
)


tree.configure(
    xscrollcommand=horizontal_scrollbar.set
)


# ============================================================
# STATUS BAR
# ============================================================

status_frame = tk.Frame(
    root,
    bg=HEADER_COLOR,
    height=45
)

status_frame.pack(
    fill="x",
    side="bottom"
)

status_frame.pack_propagate(False)


record_count_label = tk.Label(
    status_frame,
    text="Total Records: 0",
    font=("Segoe UI", 11, "bold"),
    fg="white",
    bg=HEADER_COLOR
)

record_count_label.pack(
    side="left",
    padx=20,
    pady=10
)


database_label = tk.Label(
    status_frame,
    text="SQLite Database Connected",
    font=("Segoe UI", 10),
    fg="#86efac",
    bg=HEADER_COLOR
)

database_label.pack(
    side="right",
    padx=20
)


# ============================================================
# LOAD DATABASE
# ============================================================

try:

    tables = get_tables()

    if tables:

        table_combo["values"] = tables

        table_combo.current(0)

        load_table(tables[0])

    else:

        messagebox.showwarning(
            "Database",
            "No tables found in the database."
        )

except Exception as e:

    messagebox.showerror(
        "Database Connection Error",
        f"Could not connect to database.\n\n{e}"
    )


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()