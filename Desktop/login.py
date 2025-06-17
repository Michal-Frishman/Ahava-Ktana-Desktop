from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class LoginPage(QWidget):
    def __init__(self, switch_to_main_callback):
        super().__init__()
        self.switch_to_main = switch_to_main_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setFont(QFont("Segoe UI", 12))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setToolTip("Enter your username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setToolTip("Enter your password")

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Code from email")
        self.code_input.setDisabled(True)
        self.code_input.setToolTip("Enter the verification code sent to your email")

        self.send_code_btn = QPushButton("Send Code")
        self.send_code_btn.setIcon(QIcon.fromTheme("fa-solid fa-envelope"))
        self.send_code_btn.clicked.connect(self.send_code)

        self.login_btn = QPushButton("Confirm Login")
        self.login_btn.setIcon(QIcon.fromTheme("fa-solid fa-right-to-bracket"))
        self.login_btn.clicked.connect(self.confirm_login)

        for w in [self.username_input, self.password_input, self.send_code_btn,
                  self.code_input, self.login_btn]:
            layout.addWidget(w)

        self.setLayout(layout)

    def send_code(self):
        # TODO: קריאה ל-API
        self.code_input.setDisabled(False)
        QMessageBox.information(self, "Code Sent", "Code was sent to your email")

    def confirm_login(self):
        # TODO: אימות עם API
        self.switch_to_main()
