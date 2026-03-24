#!/usr/bin/env python3
"""Modern dark themed GUI scientific calculator with PySide6."""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from calculator_scientific import EvaluationError, evaluate_expression


DARK_STYLE = """
QWidget {
    background-color: #101218;
    color: #e6e8ef;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 14px;
}
QLineEdit#display {
    background: #171b24;
    border: 1px solid #2a3040;
    border-radius: 12px;
    font-size: 30px;
    font-weight: 700;
    padding: 18px;
    color: #f6f8ff;
}
QLabel#hint {
    color: #8e97ad;
    font-size: 12px;
}
QPushButton {
    background: #1a1f2b;
    border: 1px solid #2a3144;
    border-radius: 12px;
    min-height: 44px;
    font-weight: 600;
}
QPushButton:hover {
    background: #242b3b;
}
QPushButton:pressed {
    background: #2d3650;
}
QPushButton[role="action"] {
    background: #5135e1;
    border: 1px solid #6f56ef;
}
QPushButton[role="action"]:hover {
    background: #6149ec;
}
QPushButton[role="danger"] {
    background: #5a2030;
    border: 1px solid #7d3147;
}
QListWidget {
    background: #141925;
    border: 1px solid #262f44;
    border-radius: 10px;
    padding: 8px;
}
QListWidget::item {
    padding: 6px;
    border-bottom: 1px solid #20283a;
}
QListWidget::item:selected {
    background: #2a3551;
    border-radius: 6px;
}
QFrame#card {
    background: #0f131d;
    border: 1px solid #262e42;
    border-radius: 14px;
}
"""


class ScientificCalculatorWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Scientific Calculator • PySide6")
        self.resize(1024, 680)

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(14)

        calculator_card = QFrame()
        calculator_card.setObjectName("card")
        calc_layout = QVBoxLayout(calculator_card)
        calc_layout.setContentsMargins(18, 18, 18, 18)
        calc_layout.setSpacing(10)

        title = QLabel("Scientific Calculator")
        title_font = QFont()
        title_font.setPointSize(17)
        title_font.setBold(True)
        title.setFont(title_font)
        calc_layout.addWidget(title)

        self.hint = QLabel("Shortcut: Enter hitung • Backspace hapus • Esc clear")
        self.hint.setObjectName("hint")
        calc_layout.addWidget(self.hint)

        self.display = QLineEdit()
        self.display.setObjectName("display")
        self.display.setPlaceholderText("Contoh: sin(pi/2) + sqrt(25)")
        self.display.returnPressed.connect(self.calculate)
        calc_layout.addWidget(self.display)

        grid = QGridLayout()
        grid.setSpacing(8)
        calc_layout.addLayout(grid)

        buttons = [
            ["sin(", "cos(", "tan(", "log(", "sqrt(", "(", ")", "⌫"],
            ["7", "8", "9", "/", "**", "pi", "e", "C"],
            ["4", "5", "6", "*", "%", "tau", "//", "±"],
            ["1", "2", "3", "-", "exp(", "abs(", "round(", "="],
            ["0", ".", "+", "factorial(", "log10(", "asin(", "acos(", "atan("],
        ]

        for row, cols in enumerate(buttons):
            for col, text in enumerate(cols):
                btn = QPushButton(text)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                if text == "=":
                    btn.setProperty("role", "action")
                if text == "C":
                    btn.setProperty("role", "danger")
                btn.clicked.connect(lambda _checked=False, t=text: self.handle_button(t))
                grid.addWidget(btn, row, col)

        root.addWidget(calculator_card, stretch=3)

        side_card = QFrame()
        side_card.setObjectName("card")
        side_layout = QVBoxLayout(side_card)
        side_layout.setContentsMargins(14, 14, 14, 14)
        side_layout.setSpacing(10)

        side_layout.addWidget(QLabel("Riwayat Perhitungan"))
        self.history = QListWidget()
        self.history.itemDoubleClicked.connect(self.reuse_history)
        side_layout.addWidget(self.history, stretch=1)

        clear_history_btn = QPushButton("Clear History")
        clear_history_btn.clicked.connect(self.history.clear)
        side_layout.addWidget(clear_history_btn)

        guide = QLabel(
            "Tips:\n"
            "• Double click item riwayat untuk pakai ulang ekspresi\n"
            "• Gunakan tombol fungsi untuk meminimalkan typo\n"
            "• Tekan Esc untuk reset input"
        )
        guide.setWordWrap(True)
        guide.setObjectName("hint")
        side_layout.addWidget(guide)

        root.addWidget(side_card, stretch=2)

        self._create_menu()
        self._bind_shortcuts()

    def _create_menu(self) -> None:
        copy_action = QAction("Copy Result", self)
        copy_action.setShortcut(QKeySequence("Ctrl+C"))
        copy_action.triggered.connect(self.copy_display)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence("Ctrl+V"))
        paste_action.triggered.connect(self.paste_display)

        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)

        menu = self.menuBar().addMenu("Tools")
        menu.addAction(copy_action)
        menu.addAction(paste_action)
        menu.addSeparator()
        menu.addAction(help_action)

    def _bind_shortcuts(self) -> None:
        QShortcut(QKeySequence(Qt.Key_Escape), self, activated=self.clear_display)

    def handle_button(self, label: str) -> None:
        if label == "=":
            self.calculate()
        elif label == "C":
            self.clear_display()
        elif label == "⌫":
            self.display.backspace()
        elif label == "±":
            text = self.display.text().strip()
            if text.startswith("-"):
                self.display.setText(text[1:])
            elif text:
                self.display.setText(f"-{text}")
        else:
            self.display.insert(label)
        self.display.setFocus()

    def calculate(self) -> None:
        expression = self.display.text().strip()
        if not expression:
            return

        try:
            result = evaluate_expression(expression)
        except EvaluationError as exc:
            QMessageBox.warning(self, "Calculation Error", str(exc))
            return

        rendered = f"{result:g}"
        self.history.insertItem(0, QListWidgetItem(f"{expression} = {rendered}"))
        self.display.setText(rendered)

    def clear_display(self) -> None:
        self.display.clear()
        self.display.setFocus()

    def reuse_history(self, item: QListWidgetItem) -> None:
        text = item.text()
        if "=" in text:
            expression = text.split("=", maxsplit=1)[0].strip()
            self.display.setText(expression)
            self.display.setFocus()

    def copy_display(self) -> None:
        QApplication.clipboard().setText(self.display.text())

    def paste_display(self) -> None:
        self.display.insert(QApplication.clipboard().text())

    def show_help(self) -> None:
        QMessageBox.information(
            self,
            "Help",
            "Masukkan ekspresi matematika lalu tekan Enter atau '='.\n"
            "Fungsi yang didukung: trigonometri, log, sqrt, exp, factorial, abs, round.\n"
            "Konstanta: pi, e, tau.",
        )


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    window = ScientificCalculatorWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
