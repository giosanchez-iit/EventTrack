import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit
from PyQt5.uic import loadUi
import subprocess

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/login_window.ui', self)
        self.setWindowTitle("Login")


        self.prompt.setVisible(False)
        self.PasswordLineEdit.setEchoMode(QLineEdit.Password)

        self.pushButton.clicked.connect(self.login)
        
        self.UsernameLineEdit.setToolTip('Enter Username')
        self.PasswordLineEdit.setToolTip('Enter Password')
        self.pushButton.setToolTip('View Details')

    def login(self):
        username = self.UsernameLineEdit.text()
        password = self.PasswordLineEdit.text()

        if username == "admin" and password == "password":
            subprocess.Popen(["python", "main_page.py"])
            self.close()
        else:
            # Make the prompt visible if the login fails
            self.prompt.setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
