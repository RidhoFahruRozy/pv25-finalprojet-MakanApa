def get_stylesheet(theme="light"):
    light = """
    QMainWindow {
        background-color: #f9f9f9;
    }

    QLineEdit, QTableWidget {
        background-color: #ffffff;
        color: #202020;
        border: 1px solid #cccccc;
        border-radius: 6px;
        padding: 6px;
        font-size: 14px;
    }

    QPushButton {
        background-color: #0078d7;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #005a9e;
    }

    QTableWidget {
        gridline-color: #dddddd;
        alternate-background-color: #f3f3f3;
        font-size: 13px;
    }

    QHeaderView::section {
        background-color: #eeeeee;
        color: #333333;
        font-weight: bold;
        padding: 6px;
        border: 1px solid #cccccc;
    }

    QStatusBar {
        background: #eaeaea;
        color: #202020;
        font-size: 12px;
        padding-left: 10px;
    }

    QMenuBar {
        background-color: #f4f4f4;
        color: #202020;
    }

    QMenuBar::item:selected {
        background: #d0d0d0;
    }

    QMenu {
        background-color: #ffffff;
        color: #202020;
        border: 1px solid #cccccc;
    }

    QMenu::item:selected {
        background-color: #d6ebff;
    }
    QMessageBox {
        background-color: #ffffff;
        color: #202020;
        font-size: 14px;
    }

    QMessageBox QLabel {
        color: #202020;
        border: none;
    }

    QMessageBox QPushButton {
        background-color: #0078d7;
        color: white;
        padding: 6px 12px;
        border: none;
        border-radius: 6px;
        min-width: 80px;
    }

    QMessageBox QPushButton:hover {
        background-color: #005a9e;
    }
    """

    dark = """
    QMainWindow {
        background-color: #121212;
    }

    QLineEdit, QTextEdit, QTableWidget, QLabel {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #444444;
        border-radius: 6px;
        padding: 6px;
        font-size: 14px;
    }

    QPushButton {
        background-color: #3a8ee6;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #1e5aa8;
    }

    QTableWidget {
        gridline-color: #444;
        alternate-background-color: #1a1a1a;
        font-size: 13px;
    }

    QHeaderView::section {
        background-color: #2e2e2e;
        color: #ffffff;
        font-weight: bold;
        padding: 6px;
        border: 1px solid #444;
    }

    QStatusBar {
        background: #1e1e1e;
        color: #aaaaaa;
        font-size: 12px;
        padding-left: 10px;
    }

    QMenuBar {
        background-color: #1f1f1f;
        color: #dddddd;
    }

    QMenuBar::item:selected {
        background: #333333;
    }

    QMenu {
        background-color: #2b2b2b;
        color: #dddddd;
        border: 1px solid #444;
    }

    QMenu::item:selected {
        background-color: #3a8ee6;
        color: #ffffff;
    }
    QMessageBox {
        background-color: #ffffff;
        color: #ffffff;
        font-size: 14px;
    }

    QMessageBox QLabel {
        background-color: #ffffff;
        color: #202020;
        border: none;
    }

    QMessageBox QPushButton {
        background-color: #0078d7;
        color: white;
        padding: 6px 12px;
        border: none;
        border-radius: 6px;
        min-width: 80px;
    }

    QMessageBox QPushButton:hover {
        background-color: #005a9e;
    }
    """


    return dark if theme == "dark" else light
