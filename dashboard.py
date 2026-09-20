import os
import sys
import sqlite3
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(
    BASE_DIR,
    "student_result_management.db"
)

LOGO_PATH = os.path.join(
    BASE_DIR,
    "logo.png"
)


# =========================================================
# COLORS
# =========================================================

NAVY = "#0B162B"
NAVY_2 = "#111D34"
NAVY_3 = "#182A52"

BLUE = "#2563EB"
BLUE_LIGHT = "#EFF6FF"

TEAL = "#14B8A6"
TEAL_LIGHT = "#ECFDF5"

ORANGE = "#F59E0B"
ORANGE_LIGHT = "#FFF7E6"

PURPLE = "#7C3AED"
PURPLE_LIGHT = "#F5F3FF"

CYAN = "#06B6D4"
CYAN_LIGHT = "#ECFEFF"

GREEN = "#10B981"
RED = "#EF4444"

WHITE = "#FFFFFF"
BG = "#F3F6FA"
BORDER = "#DCE3EC"

TEXT = "#0F172A"
TEXT_2 = "#64748B"
TEXT_3 = "#94A3B8"

# Table hover colors
TABLE_HOVER = "#E0F2FE"
TABLE_SELECTED = "#BFDBFE"
TABLE_NORMAL = "#FFFFFF"


# =========================================================
# DATABASE FUNCTIONS
# =========================================================

def get_count(table_name):

    try:

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        )

        result = cursor.fetchone()[0]

        conn.close()

        return result

    except Exception:
        return 0


def get_database_tables():

    try:

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
        """)

        tables = cursor.fetchall()

        conn.close()

        return len(tables)

    except Exception:
        return 0


def get_recent_students():

    try:

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT roll, name, Course
            FROM student
            ORDER BY roll DESC
            LIMIT 8
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    except Exception:
        return []


# =========================================================
# MAIN APPLICATION
# =========================================================

class SRM:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Result Lab | Student Result Management System"
        )

        try:
            self.root.state("zoomed")
        except:
            self.root.geometry("1400x850")

        self.root.minsize(
            1100,
            700
        )

        self.root.configure(
            bg=BG
        )

        self.setup_styles()

        self.create_header()

        self.create_body()

        self.refresh_dashboard()

        self.update_clock()

        self.root.bind(
            "<Configure>",
            self.on_resize
        )


    # =====================================================
    # STYLES
    # =====================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass


        # -----------------------------
        # TABLE
        # -----------------------------

        style.configure(
            "Treeview",
            background=TABLE_NORMAL,
            foreground=TEXT,
            fieldbackground=TABLE_NORMAL,
            rowheight=43,
            borderwidth=0,
            font=(
                "Segoe UI",
                10
            )
        )


        style.configure(
            "Treeview.Heading",
            background=NAVY,
            foreground=WHITE,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            padding=11,
            relief="flat"
        )


        style.map(
            "Treeview",
            background=[
                (
                    "selected",
                    TABLE_SELECTED
                )
            ],
            foreground=[
                (
                    "selected",
                    TEXT
                )
            ]
        )


    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        self.header = tk.Frame(
            self.root,
            bg=NAVY,
            height=125
        )

        self.header.pack(
            side="top",
            fill="x"
        )

        self.header.pack_propagate(False)


        # =================================================
        # LOGO
        # =================================================

        self.logo_frame = tk.Frame(
            self.header,
            bg=NAVY
        )

        self.logo_frame.pack(
            side="left",
            padx=(28, 12),
            pady=14
        )


        self.logo_image = None


        if os.path.exists(LOGO_PATH):

            try:

                from PIL import Image, ImageTk

                image = Image.open(
                    LOGO_PATH
                )

                image.thumbnail(
                    (82, 82)
                )

                self.logo_image = ImageTk.PhotoImage(
                    image
                )

                logo_label = tk.Label(
                    self.logo_frame,
                    image=self.logo_image,
                    bg=NAVY,
                    bd=0
                )

                logo_label.pack()

                logo_label.bind(
                    "<Button-1>",
                    lambda e: self.logo_clicked()
                )

            except:

                self.create_fallback_logo()

        else:

            self.create_fallback_logo()


        # =================================================
        # TITLE
        # =================================================

        title_frame = tk.Frame(
            self.header,
            bg=NAVY
        )

        title_frame.pack(
            side="left",
            pady=20
        )


        tk.Label(
            title_frame,
            text="RESULT LAB",
            font=(
                "Segoe UI",
                28,
                "bold"
            ),
            fg=WHITE,
            bg=NAVY
        ).pack(
            anchor="w"
        )


        tk.Label(
            title_frame,
            text="Student Result Management System",
            font=(
                "Segoe UI",
                11
            ),
            fg="#9FB2D0",
            bg=NAVY
        ).pack(
            anchor="w",
            pady=(4, 0)
        )


        # =================================================
        # RIGHT HEADER
        # =================================================

        right_header = tk.Frame(
            self.header,
            bg=NAVY
        )

        right_header.pack(
            side="right",
            padx=30,
            pady=25
        )


        self.clock_label = tk.Label(
            right_header,
            text="",
            font=(
                "Segoe UI",
                10
            ),
            fg="#9FB2D0",
            bg=NAVY
        )

        self.clock_label.pack(
            anchor="e",
            pady=(0, 8)
        )


        # =================================================
        # ADMIN BUTTON
        # =================================================

        self.admin_button = tk.Frame(
            right_header,
            bg=NAVY_3,
            cursor="hand2"
        )

        self.admin_button.pack(
            anchor="e"
        )


        admin_dot = tk.Label(
            self.admin_button,
            text="●",
            font=(
                "Segoe UI",
                10
            ),
            fg=GREEN,
            bg=NAVY_3
        )

        admin_dot.pack(
            side="left",
            padx=(15, 5),
            pady=12
        )


        admin_text = tk.Label(
            self.admin_button,
            text="ADMIN",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            fg=WHITE,
            bg=NAVY_3
        )

        admin_text.pack(
            side="left",
            padx=(0, 16),
            pady=12
        )


        for widget in [
            self.admin_button,
            admin_dot,
            admin_text
        ]:

            widget.bind(
                "<Button-1>",
                lambda e: self.open_admin_panel()
            )

            widget.bind(
                "<Enter>",
                lambda e: self.admin_hover(True)
            )

            widget.bind(
                "<Leave>",
                lambda e: self.admin_hover(False)
            )


    def admin_hover(self, active):

        color = (
            "#203466"
            if active
            else NAVY_3
        )

        self.admin_button.config(
            bg=color
        )

        for widget in self.admin_button.winfo_children():

            widget.config(
                bg=color
            )


    # =====================================================
    # FALLBACK LOGO
    # =====================================================

    def create_fallback_logo(self):

        canvas = tk.Canvas(
            self.logo_frame,
            width=75,
            height=75,
            bg=NAVY,
            highlightthickness=0
        )

        canvas.pack()

        canvas.create_oval(
            5,
            5,
            70,
            70,
            outline=CYAN,
            width=3
        )

        canvas.create_oval(
            12,
            12,
            63,
            63,
            outline=BLUE,
            width=2
        )

        canvas.create_text(
            37,
            37,
            text="R",
            font=(
                "Segoe UI",
                26,
                "bold"
            ),
            fill=WHITE
        )

        canvas.bind(
            "<Button-1>",
            lambda e: self.logo_clicked()
        )


    def logo_clicked(self):

        messagebox.showinfo(
            "RESULT LAB",
            "Student Result Management System\n\n"
            "Academic Management Dashboard\n\n"
            "Version 1.0"
        )


    # =====================================================
    # BODY
    # =====================================================

    def create_body(self):

        self.body = tk.Frame(
            self.root,
            bg=BG
        )

        self.body.pack(
            fill="both",
            expand=True
        )


        # =================================================
        # SIDEBAR
        # =================================================

        self.sidebar = tk.Frame(
            self.body,
            bg=NAVY,
            width=265
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        self.create_sidebar()


        # =================================================
        # MAIN SCROLL AREA
        # =================================================

        self.main_container = tk.Frame(
            self.body,
            bg=BG
        )

        self.main_container.pack(
            side="left",
            fill="both",
            expand=True
        )


        self.canvas = tk.Canvas(
            self.main_container,
            bg=BG,
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            self.main_container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scroll_frame = tk.Frame(
            self.canvas,
            bg=BG
        )


        self.scroll_window = self.canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor="nw"
        )


        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )


        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )


        self.scroll_frame.bind(
            "<Configure>",
            lambda e:
            self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )


        self.canvas.bind(
            "<Configure>",
            self.resize_scroll_frame
        )


        self.canvas.bind_all(
            "<MouseWheel>",
            self.mousewheel
        )


        self.create_dashboard()


    # =====================================================
    # SIDEBAR
    # =====================================================

    def create_sidebar(self):

        # -------------------------------------------------
        # CONTROL
        # -------------------------------------------------

        top = tk.Frame(
            self.sidebar,
            bg=NAVY
        )

        top.pack(
            fill="x",
            padx=22,
            pady=(28, 20)
        )


        tk.Label(
            top,
            text="CONTROL",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg="#7186A8",
            bg=NAVY
        ).pack(
            anchor="w"
        )


        # FIXED MANAGEMENT PANEL
        # It now fits inside the sidebar.

        tk.Label(
            top,
            text="Management Panel",
            font=(
                "Segoe UI",
                18,
                "bold"
            ),
            fg=WHITE,
            bg=NAVY,
            anchor="w",
            justify="left"
        ).pack(
            anchor="w",
            pady=(10, 0)
        )


        # -------------------------------------------------
        # MAIN MENU
        # -------------------------------------------------

        tk.Label(
            self.sidebar,
            text="MAIN MENU",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg="#7186A8",
            bg=NAVY
        ).pack(
            anchor="w",
            padx=30,
            pady=(3, 10)
        )


        self.sidebar_button(
            "⌂   Dashboard",
            self.refresh_dashboard,
            active=True
        )


        self.sidebar_button(
            "▣   Courses",
            self.add_course
        )


        self.sidebar_button(
            "♙   Students",
            self.add_student
        )


        self.sidebar_button(
            "▤   Examinations",
            self.add_examrecord
        )


        self.sidebar_button(
            "▥   Add Marks",
            self.add_result
        )


        self.sidebar_button(
            "▤   Student Reports",
            self.show_report
        )


        self.sidebar_button(
            "▦   Course Reports",
            self.course_report
        )


        # -------------------------------------------------
        # SMART TOOLS
        # -------------------------------------------------

        tk.Label(
            self.sidebar,
            text="SMART TOOLS",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg="#7186A8",
            bg=NAVY
        ).pack(
            anchor="w",
            padx=30,
            pady=(22, 10)
        )


        self.sidebar_button(
            "✦   AI Assistant",
            self.open_ai_chatbot,
            special=True
        )


        self.sidebar_button(
            "▣   View Database",
            self.open_database,
            special=True
        )


        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        bottom = tk.Frame(
            self.sidebar,
            bg=NAVY_2
        )

        bottom.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=15
        )


        tk.Label(
            bottom,
            text="SYSTEM STATUS",
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg="#7186A8",
            bg=NAVY_2
        ).pack(
            anchor="w",
            padx=12,
            pady=(10, 3)
        )


        tk.Label(
            bottom,
            text="●  System Online",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg="#34D399",
            bg=NAVY_2
        ).pack(
            anchor="w",
            padx=12,
            pady=(0, 10)
        )


    # =====================================================
    # SIDEBAR BUTTON
    # =====================================================

    def sidebar_button(
        self,
        text,
        command,
        active=False,
        special=False
    ):

        if active:
            normal_bg = "#1B2B63"
        elif special:
            normal_bg = "#24194D"
        else:
            normal_bg = NAVY


        frame = tk.Frame(
            self.sidebar,
            bg=normal_bg,
            cursor="hand2"
        )

        frame.pack(
            fill="x",
            padx=14,
            pady=3
        )


        label = tk.Label(
            frame,
            text=text,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            fg=(
                "#67E8F9"
                if special
                else "#E5E7EB"
            ),
            bg=normal_bg,
            anchor="w"
        )

        label.pack(
            fill="x",
            padx=18,
            pady=12
        )


        def enter(event):

            if special:
                hover_bg = "#35226F"
            else:
                hover_bg = "#1B315D"

            frame.config(
                bg=hover_bg
            )

            label.config(
                bg=hover_bg
            )


        def leave(event):

            frame.config(
                bg=normal_bg
            )

            label.config(
                bg=normal_bg
            )


        for widget in [
            frame,
            label
        ]:

            widget.bind(
                "<Button-1>",
                lambda e: command()
            )

            widget.bind(
                "<Enter>",
                enter
            )

            widget.bind(
                "<Leave>",
                leave
            )


        return frame


    # =====================================================
    # DASHBOARD
    # =====================================================

    def create_dashboard(self):

        self.content = tk.Frame(
            self.scroll_frame,
            bg=BG
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=24
        )


        # =================================================
        # PAGE HEADER
        # =================================================

        heading = tk.Frame(
            self.content,
            bg=BG
        )

        heading.pack(
            fill="x",
            pady=(0, 20)
        )


        title_box = tk.Frame(
            heading,
            bg=BG
        )

        title_box.pack(
            side="left"
        )


        tk.Label(
            title_box,
            text="Dashboard Overview",
            font=(
                "Segoe UI",
                28,
                "bold"
            ),
            fg=TEXT,
            bg=BG
        ).pack(
            anchor="w"
        )


        tk.Label(
            title_box,
            text="Monitor and manage your complete academic system",
            font=(
                "Segoe UI",
                11
            ),
            fg=TEXT_2,
            bg=BG
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


        tk.Button(
            heading,
            text="⟳  Refresh",
            command=self.refresh_dashboard,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            bg=WHITE,
            fg="#334155",
            activebackground="#E2E8F0",
            relief="flat",
            bd=0,
            padx=20,
            pady=11,
            cursor="hand2"
        ).pack(
            side="right"
        )


        # =================================================
        # STATISTICS
        # =================================================

        self.stats_frame = tk.Frame(
            self.content,
            bg=BG
        )

        self.stats_frame.pack(
            fill="x",
            pady=(0, 20)
        )


        self.student_card = self.create_stat_card(
            self.stats_frame,
            "TOTAL STUDENTS",
            "Student Records",
            BLUE,
            BLUE_LIGHT
        )


        self.course_card = self.create_stat_card(
            self.stats_frame,
            "TOTAL COURSES",
            "Available Courses",
            TEAL,
            TEAL_LIGHT
        )


        self.exam_card = self.create_stat_card(
            self.stats_frame,
            "EXAM RECORDS",
            "Examination Data",
            ORANGE,
            ORANGE_LIGHT
        )


        self.result_card = self.create_stat_card(
            self.stats_frame,
            "RESULT RECORDS",
            "Published Results",
            PURPLE,
            PURPLE_LIGHT
        )


        # =================================================
        # LOWER AREA
        # =================================================

        self.lower = tk.Frame(
            self.content,
            bg=BG
        )

        self.lower.pack(
            fill="x"
        )


        # =================================================
        # ACADEMIC MANAGEMENT
        # =================================================

        self.academic = tk.Frame(
            self.lower,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.academic.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )


        tk.Label(
            self.academic,
            text="Academic Management",
            font=(
                "Segoe UI",
                21,
                "bold"
            ),
            fg=TEXT,
            bg=WHITE
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 3)
        )


        tk.Label(
            self.academic,
            text="Quick access to your most-used management tools",
            font=(
                "Segoe UI",
                10
            ),
            fg=TEXT_2,
            bg=WHITE
        ).pack(
            anchor="w",
            padx=30
        )


        # =================================================
        # ACTION CARDS
        # =================================================

        self.action_grid = tk.Frame(
            self.academic,
            bg=WHITE
        )

        self.action_grid.pack(
            fill="x",
            padx=25,
            pady=16
        )


        self.action_card(
            self.action_grid,
            "+",
            "Add Student",
            "Create record",
            BLUE_LIGHT,
            BLUE,
            self.add_student
        )


        self.action_card(
            self.action_grid,
            "+",
            "Add Marks",
            "Enter marks",
            TEAL_LIGHT,
            TEAL,
            self.add_result
        )


        self.action_card(
            self.action_grid,
            "▤",
            "Reports",
            "View reports",
            PURPLE_LIGHT,
            PURPLE,
            self.show_report
        )


        self.action_card(
            self.action_grid,
            "✦",
            "AI Assistant",
            "Smart help",
            CYAN_LIGHT,
            CYAN,
            self.open_ai_chatbot
        )


        # =================================================
        # FEATURES
        # =================================================

        tk.Label(
            self.academic,
            text="SYSTEM FEATURES",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=TEXT_2,
            bg=WHITE
        ).pack(
            anchor="w",
            padx=30,
            pady=(5, 10)
        )


        features = [
            ("✓", "Student information management", GREEN),
            ("✓", "Course and examination management", BLUE),
            ("✓", "Marks and result processing", PURPLE),
            ("✓", "Reports and database management", ORANGE)
        ]


        for icon, text, color in features:

            row = tk.Frame(
                self.academic,
                bg=WHITE
            )

            row.pack(
                fill="x",
                padx=30,
                pady=4
            )


            tk.Label(
                row,
                text=icon,
                font=(
                    "Segoe UI",
                    11,
                    "bold"
                ),
                fg=color,
                bg=WHITE
            ).pack(
                side="left",
                padx=(0, 12)
            )


            tk.Label(
                row,
                text=text,
                font=(
                    "Segoe UI",
                    10
                ),
                fg="#475569",
                bg=WHITE
            ).pack(
                side="left"
            )


        # =================================================
        # DATABASE CENTER
        # =================================================

        self.database_panel = tk.Frame(
            self.lower,
            bg=NAVY,
            width=370
        )

        self.database_panel.pack(
            side="right",
            fill="both",
            padx=(10, 0)
        )

        self.database_panel.pack_propagate(False)


        tk.Label(
            self.database_panel,
            text="DATABASE CENTER",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg="#67E8F9",
            bg=NAVY
        ).pack(
            anchor="w",
            padx=28,
            pady=(25, 0)
        )


        tk.Label(
            self.database_panel,
            text="Your Data Hub",
            font=(
                "Segoe UI",
                22,
                "bold"
            ),
            fg=WHITE,
            bg=NAVY
        ).pack(
            anchor="w",
            padx=28,
            pady=(8, 0)
        )


        tk.Label(
            self.database_panel,
            text="Inspect and manage your SQLite records.",
            font=(
                "Segoe UI",
                9
            ),
            fg="#9FB2D0",
            bg=NAVY
        ).pack(
            anchor="w",
            padx=28,
            pady=(5, 18)
        )


        # =================================================
        # DATABASE INFO
        # =================================================

        self.db_info = tk.Frame(
            self.database_panel,
            bg="#182A52",
            height=50
        )

        self.db_info.pack(
            fill="x",
            padx=24
        )

        self.db_info.pack_propagate(False)


        self.db_table_label = tk.Label(
            self.db_info,
            text="Tables     0",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            fg="#D7E4FA",
            bg="#182A52"
        )

        self.db_table_label.pack(
            side="left",
            padx=15
        )


        tk.Label(
            self.db_info,
            text="● Connected",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg="#34D399",
            bg="#182A52"
        ).pack(
            side="right",
            padx=15
        )


        # =================================================
        # DATABASE BUTTON
        # =================================================

        tk.Button(
            self.database_panel,
            text="OPEN DATABASE  →",
            command=self.open_database,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            fg=WHITE,
            bg="#2DD4BF",
            activebackground="#14B8A6",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=11
        ).pack(
            fill="x",
            padx=24,
            pady=(13, 10)
        )


        # =================================================
        # AI ASSISTANT
        # =================================================

        ai_box = tk.Frame(
            self.database_panel,
            bg="#2A1D55"
        )

        ai_box.pack(
            fill="x",
            padx=24,
            pady=(4, 18)
        )


        tk.Label(
            ai_box,
            text="✦  AI ASSISTANT",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg="#C4B5FD",
            bg="#2A1D55"
        ).pack(
            anchor="w",
            padx=17,
            pady=(14, 3)
        )


        tk.Label(
            ai_box,
            text="Smart academic help",
            font=(
                "Segoe UI",
                13,
                "bold"
            ),
            fg=WHITE,
            bg="#2A1D55"
        ).pack(
            anchor="w",
            padx=17
        )


        tk.Label(
            ai_box,
            text=(
                "Ask questions about students,\n"
                "results, courses and records."
            ),
            font=(
                "Segoe UI",
                9
            ),
            fg="#C4BDD9",
            bg="#2A1D55",
            justify="left"
        ).pack(
            anchor="w",
            padx=17,
            pady=(5, 10)
        )


        # FIX:
        # Proper button height and text area.

        ai_button = tk.Button(
            ai_box,
            text="OPEN AI ASSISTANT",
            command=self.open_ai_chatbot,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=WHITE,
            bg=PURPLE,
            activebackground="#6D28D9",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            height=1,
            pady=9
        )

        ai_button.pack(
            fill="x",
            padx=14,
            pady=(0, 14)
        )


        # =================================================
        # RECENT STUDENTS
        # =================================================

        recent_box = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        recent_box.pack(
            fill="x",
            pady=(20, 0)
        )


        recent_header = tk.Frame(
            recent_box,
            bg=WHITE
        )

        recent_header.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )


        tk.Label(
            recent_header,
            text="Recent Students",
            font=(
                "Segoe UI",
                17,
                "bold"
            ),
            fg=TEXT,
            bg=WHITE
        ).pack(
            side="left"
        )


        tk.Label(
            recent_header,
            text="Latest records",
            font=(
                "Segoe UI",
                9
            ),
            fg=TEXT_2,
            bg=WHITE
        ).pack(
            side="left",
            padx=12
        )


        # =================================================
        # TABLE
        # =================================================

        table_frame = tk.Frame(
            recent_box,
            bg=WHITE
        )

        table_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        self.student_table = ttk.Treeview(
            table_frame,
            columns=(
                "roll",
                "name",
                "course"
            ),
            show="headings",
            height=6
        )


        self.student_table.heading(
            "roll",
            text="ROLL NO."
        )

        self.student_table.heading(
            "name",
            text="STUDENT NAME"
        )

        self.student_table.heading(
            "course",
            text="COURSE"
        )


        self.student_table.column(
            "roll",
            width=170,
            minwidth=120,
            anchor="center"
        )

        self.student_table.column(
            "name",
            width=350,
            minwidth=200,
            anchor="w"
        )

        self.student_table.column(
            "course",
            width=350,
            minwidth=200,
            anchor="w"
        )


        self.student_table.pack(
            fill="x"
        )


        # =================================================
        # TABLE HOVER SYSTEM
        # =================================================

        self.student_table.tag_configure(
            "normal",
            background=TABLE_NORMAL,
            foreground=TEXT
        )


        self.student_table.tag_configure(
            "hover",
            background=TABLE_HOVER,
            foreground=TEXT
        )


        self.student_table.tag_configure(
            "selected_row",
            background=TABLE_SELECTED,
            foreground=TEXT
        )


        self.hover_item = None


        self.student_table.bind(
            "<Motion>",
            self.table_hover
        )


        self.student_table.bind(
            "<Leave>",
            self.table_leave
        )


        self.student_table.bind(
            "<ButtonRelease-1>",
            self.table_click
        )


    # =====================================================
    # STAT CARD
    # =====================================================

    def create_stat_card(
        self,
        parent,
        title,
        subtitle,
        color,
        light
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )


        tk.Frame(
            card,
            bg=color,
            height=5
        ).pack(
            fill="x"
        )


        body = tk.Frame(
            card,
            bg=WHITE
        )

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=14
        )


        tk.Label(
            body,
            text="●",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            fg=color,
            bg=light,
            padx=7,
            pady=4
        ).pack(
            anchor="w"
        )


        value = tk.Label(
            body,
            text="0",
            font=(
                "Segoe UI",
                28,
                "bold"
            ),
            fg=TEXT,
            bg=WHITE
        )

        value.pack(
            anchor="w",
            pady=(10, 1)
        )


        tk.Label(
            body,
            text=title,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=TEXT,
            bg=WHITE
        ).pack(
            anchor="w"
        )


        tk.Label(
            body,
            text=subtitle,
            font=(
                "Segoe UI",
                9
            ),
            fg=TEXT_2,
            bg=WHITE
        ).pack(
            anchor="w",
            pady=(3, 0)
        )


        return {
            "card": card,
            "value": value
        }


    # =====================================================
    # ACTION CARD
    # =====================================================

    def action_card(
        self,
        parent,
        icon,
        title,
        subtitle,
        bg,
        color,
        command
    ):

        card = tk.Frame(
            parent,
            bg=bg,
            cursor="hand2"
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )


        tk.Label(
            card,
            text=icon,
            font=(
                "Segoe UI",
                18,
                "bold"
            ),
            fg=color,
            bg=bg
        ).pack(
            anchor="w",
            padx=17,
            pady=(12, 1)
        )


        tk.Label(
            card,
            text=title,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            fg=TEXT,
            bg=bg
        ).pack(
            anchor="w",
            padx=17
        )


        tk.Label(
            card,
            text=subtitle,
            font=(
                "Segoe UI",
                8
            ),
            fg=TEXT_2,
            bg=bg
        ).pack(
            anchor="w",
            padx=17,
            pady=(3, 12)
        )


        for widget in card.winfo_children():

            widget.bind(
                "<Button-1>",
                lambda e: command()
            )

            widget.bind(
                "<Enter>",
                lambda e, c=card, b=bg:
                c.config(
                    bg="#E5E7EB"
                )
            )

            widget.bind(
                "<Leave>",
                lambda e, c=card, b=bg:
                c.config(
                    bg=b
                )
            )


        card.bind(
            "<Button-1>",
            lambda e: command()
        )


    # =====================================================
    # TABLE HOVER
    # =====================================================

    def table_hover(self, event):

        item = self.student_table.identify_row(
            event.y
        )


        # Remove old hover

        if self.hover_item:

            current_tags = list(
                self.student_table.item(
                    self.hover_item,
                    "tags"
                )
            )

            current_tags = [
                tag
                for tag in current_tags
                if tag != "hover"
            ]

            if "selected_row" not in current_tags:

                current_tags.append(
                    "normal"
                )

            self.student_table.item(
                self.hover_item,
                tags=current_tags
            )


        # Apply new hover

        if item:

            self.hover_item = item

            current_tags = list(
                self.student_table.item(
                    item,
                    "tags"
                )
            )

            current_tags = [
                tag
                for tag in current_tags
                if tag not in [
                    "normal",
                    "hover"
                ]
            ]

            current_tags.append(
                "hover"
            )

            self.student_table.item(
                item,
                tags=current_tags
            )

        else:

            self.hover_item = None


    def table_leave(self, event):

        if self.hover_item:

            current_tags = list(
                self.student_table.item(
                    self.hover_item,
                    "tags"
                )
            )

            current_tags = [
                tag
                for tag in current_tags
                if tag != "hover"
            ]

            current_tags.append(
                "normal"
            )

            self.student_table.item(
                self.hover_item,
                tags=current_tags
            )

            self.hover_item = None


    def table_click(self, event):

        item = self.student_table.identify_row(
            event.y
        )

        if item:

            for row in self.student_table.get_children():

                self.student_table.item(
                    row,
                    tags=("normal",)
                )


            self.student_table.item(
                item,
                tags=("selected_row",)
            )


    # =====================================================
    # ADMIN PANEL
    # =====================================================

    def open_admin_panel(self):

        admin = tk.Toplevel(
            self.root
        )

        admin.title(
            "Admin Control Center"
        )

        admin.geometry(
            "650x560"
        )

        admin.minsize(
            550,
            500
        )

        admin.configure(
            bg=BG
        )


        # HEADER

        header = tk.Frame(
            admin,
            bg=NAVY,
            height=105
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)


        tk.Label(
            header,
            text="ADMIN CONTROL CENTER",
            font=(
                "Segoe UI",
                20,
                "bold"
            ),
            fg=WHITE,
            bg=NAVY
        ).pack(
            anchor="w",
            padx=30,
            pady=(22, 3)
        )


        tk.Label(
            header,
            text="Manage your Result Lab system",
            font=(
                "Segoe UI",
                10
            ),
            fg="#9FB2D0",
            bg=NAVY
        ).pack(
            anchor="w",
            padx=30
        )


        # CONTENT

        content = tk.Frame(
            admin,
            bg=BG
        )

        content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )


        # PROFILE

        profile = tk.Frame(
            content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        profile.pack(
            fill="x",
            pady=(0, 15)
        )


        tk.Label(
            profile,
            text="●",
            font=(
                "Segoe UI",
                25,
                "bold"
            ),
            fg=GREEN,
            bg=WHITE
        ).pack(
            side="left",
            padx=20,
            pady=15
        )


        ptext = tk.Frame(
            profile,
            bg=WHITE
        )

        ptext.pack(
            side="left",
            pady=15
        )


        tk.Label(
            ptext,
            text="Administrator",
            font=(
                "Segoe UI",
                13,
                "bold"
            ),
            fg=TEXT,
            bg=WHITE
        ).pack(
            anchor="w"
        )


        tk.Label(
            ptext,
            text="System administrator • Online",
            font=(
                "Segoe UI",
                9
            ),
            fg=TEXT_2,
            bg=WHITE
        ).pack(
            anchor="w"
        )


        # OPTIONS

        options = tk.Frame(
            content,
            bg=BG
        )

        options.pack(
            fill="both",
            expand=True
        )


        self.admin_option(
            options,
            "Database Management",
            "Open and inspect all SQLite tables",
            self.open_database,
            BLUE
        )


        self.admin_option(
            options,
            "Refresh Dashboard",
            "Reload latest academic statistics",
            self.refresh_dashboard,
            TEAL
        )


        self.admin_option(
            options,
            "AI Assistant",
            "Open the future-ready AI assistant",
            self.open_ai_chatbot,
            PURPLE
        )


        self.admin_option(
            options,
            "System Information",
            "View application and database information",
            self.show_system_info,
            ORANGE
        )


    def admin_option(
        self,
        parent,
        title,
        subtitle,
        command,
        color
    ):

        box = tk.Frame(
            parent,
            bg=WHITE,
            cursor="hand2",
            highlightbackground=BORDER,
            highlightthickness=1
        )

        box.pack(
            fill="x",
            pady=5
        )


        tk.Label(
            box,
            text="◆",
            font=(
                "Segoe UI",
                12
            ),
            fg=color,
            bg=WHITE
        ).pack(
            side="left",
            padx=(18, 12),
            pady=15
        )


        text_box = tk.Frame(
            box,
            bg=WHITE
        )

        text_box.pack(
            side="left",
            pady=10
        )


        title_label = tk.Label(
            text_box,
            text=title,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            fg=TEXT,
            bg=WHITE
        )

        title_label.pack(
            anchor="w"
        )


        sub_label = tk.Label(
            text_box,
            text=subtitle,
            font=(
                "Segoe UI",
                8
            ),
            fg=TEXT_2,
            bg=WHITE
        )

        sub_label.pack(
            anchor="w",
            pady=(2, 0)
        )


        for widget in [
            box,
            text_box,
            title_label,
            sub_label
        ]:

            widget.bind(
                "<Button-1>",
                lambda e: command()
            )


    # =====================================================
    # SYSTEM INFORMATION
    # =====================================================

    def show_system_info(self):

        messagebox.showinfo(
            "System Information",
            "RESULT LAB\n\n"
            "Database: SQLite\n"
            f"Tables: {get_database_tables()}\n\n"
            f"Students: {get_count('student')}\n"
            f"Courses: {get_count('course')}\n"
            f"Exam Records: {get_count('examrecord')}\n"
            f"Result Records: {get_count('result')}\n\n"
            "Status: Online"
        )


    # =====================================================
    # AI ASSISTANT
    # =====================================================

    def open_ai_chatbot(self):

        chat = tk.Toplevel(
            self.root
        )

        chat.title(
            "Result Lab AI Assistant"
        )

        chat.geometry(
            "600x650"
        )

        chat.minsize(
            500,
            550
        )

        chat.configure(
            bg=BG
        )


        # HEADER

        header = tk.Frame(
            chat,
            bg=NAVY,
            height=100
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)


        tk.Label(
            header,
            text="✦  AI ASSISTANT",
            font=(
                "Segoe UI",
                18,
                "bold"
            ),
            fg=WHITE,
            bg=NAVY
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 3)
        )


        tk.Label(
            header,
            text="Smart academic assistance",
            font=(
                "Segoe UI",
                9
            ),
            fg="#9FB2D0",
            bg=NAVY
        ).pack(
            anchor="w",
            padx=25
        )


        # CHAT

        chat_box = tk.Text(
            chat,
            bg=WHITE,
            fg=TEXT,
            font=(
                "Segoe UI",
                10
            ),
            relief="flat",
            bd=0,
            wrap="word",
            padx=15,
            pady=15
        )

        chat_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        chat_box.insert(
            "end",
            "AI Assistant\n\n"
            "Hello! I am the Result Lab AI Assistant.\n\n"
            "I can be connected with your database and AI API "
            "in the next development stage.\n\n"
            "Possible features:\n"
            "• Search students\n"
            "• Analyze results\n"
            "• Find course information\n"
            "• Search examination records\n"
            "• Generate academic insights\n"
            "• Answer database questions\n\n"
        )


        chat_box.config(
            state="disabled"
        )


        # INPUT

        bottom = tk.Frame(
            chat,
            bg=BG
        )

        bottom.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        entry = tk.Entry(
            bottom,
            font=(
                "Segoe UI",
                10
            ),
            relief="solid",
            bd=1
        )

        entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10
        )


        def send_message():

            question = entry.get().strip()

            if not question:
                return


            chat_box.config(
                state="normal"
            )


            chat_box.insert(
                "end",
                f"\nYou: {question}\n"
            )


            chat_box.insert(
                "end",
                "\nAI: This AI interface is ready. "
                "The real AI/database connection can be "
                "added in the next stage.\n"
            )


            chat_box.config(
                state="disabled"
            )


            chat_box.see(
                "end"
            )


            entry.delete(
                0,
                "end"
            )


        tk.Button(
            bottom,
            text="SEND",
            command=send_message,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=WHITE,
            bg=PURPLE,
            activebackground="#6D28D9",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(
            side="right",
            padx=(10, 0)
        )


        entry.bind(
            "<Return>",
            lambda e: send_message()
        )


    # =====================================================
    # REFRESH
    # =====================================================

    def refresh_dashboard(self):

        students = get_count(
            "student"
        )

        courses = get_count(
            "course"
        )

        exams = get_count(
            "examrecord"
        )

        results = get_count(
            "result"
        )


        self.student_card["value"].config(
            text=str(students)
        )

        self.course_card["value"].config(
            text=str(courses)
        )

        self.exam_card["value"].config(
            text=str(exams)
        )

        self.result_card["value"].config(
            text=str(results)
        )


        self.db_table_label.config(
            text=f"Tables     {get_database_tables()}"
        )


        self.refresh_recent_students()


    # =====================================================
    # RECENT STUDENTS
    # =====================================================

    def refresh_recent_students(self):

        for item in self.student_table.get_children():

            self.student_table.delete(
                item
            )


        students = get_recent_students()


        for student in students:

            self.student_table.insert(
                "",
                "end",
                values=(
                    student[0],
                    student[1],
                    student[2]
                ),
                tags=("normal",)
            )


    # =====================================================
    # DATABASE
    # =====================================================

    def open_database(self):

        database_viewer = os.path.join(
            BASE_DIR,
            "database_viewer.py"
        )


        if not os.path.exists(
            database_viewer
        ):

            messagebox.showerror(
                "Database Viewer",
                "database_viewer.py was not found."
            )

            return


        try:

            subprocess.Popen(
                [
                    sys.executable,
                    database_viewer
                ],
                cwd=BASE_DIR
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


    # =====================================================
    # EXISTING MODULES
    # =====================================================

    def add_course(self):

        try:

            from course_details import courseClass

            window = tk.Toplevel(
                self.root
            )

            courseClass(window)

        except Exception as e:

            messagebox.showerror(
                "Courses",
                str(e)
            )


    def add_student(self):

        try:

            from student import studentClass

            window = tk.Toplevel(
                self.root
            )

            studentClass(window)

        except Exception as e:

            messagebox.showerror(
                "Students",
                str(e)
            )


    def add_examrecord(self):

        try:

            from exam_record import examClass

            window = tk.Toplevel(
                self.root
            )

            examClass(window)

        except Exception as e:

            messagebox.showerror(
                "Examinations",
                str(e)
            )


    def add_result(self):

        try:

            from result import resultClass

            window = tk.Toplevel(
                self.root
            )

            resultClass(window)

        except Exception as e:

            messagebox.showerror(
                "Marks",
                str(e)
            )


    def show_report(self):

        try:

            from final_report import reportClass

            window = tk.Toplevel(
                self.root
            )

            reportClass(window)

        except Exception as e:

            messagebox.showerror(
                "Reports",
                str(e)
            )


    def course_report(self):

        try:

            from course_report import creportClass

            window = tk.Toplevel(
                self.root
            )

            creportClass(window)

        except Exception as e:

            messagebox.showerror(
                "Course Reports",
                str(e)
            )


    # =====================================================
    # RESPONSIVE
    # =====================================================

    def resize_scroll_frame(self, event):

        self.canvas.itemconfig(
            self.scroll_window,
            width=event.width
        )


    def on_resize(self, event):

        # Tkinter automatically expands the
        # main content area.
        pass


    def mousewheel(self, event):

        try:

            self.canvas.yview_scroll(
                int(
                    -1 *
                    (event.delta / 120)
                ),
                "units"
            )

        except:
            pass


    # =====================================================
    # CLOCK
    # =====================================================

    def update_clock(self):

        now = datetime.now()

        self.clock_label.config(
            text=now.strftime(
                "%d %b %Y  •  %I:%M %p"
            )
        )

        self.root.after(
            1000,
            self.update_clock
        )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    try:

        from create_db import create_db

        create_db()

    except Exception as e:

        print(
            "Database initialization:",
            e
        )


    root = tk.Tk()

    app = SRM(
        root
    )

    root.mainloop()