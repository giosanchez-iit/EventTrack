import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.uic import loadUi
import db_connector 

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet("""background-color:white;""")
        layout = QHBoxLayout(central_widget)

        #------------------------------------------------------------------------------------------------------------------
        #   SIDEBAR
        #------------------------------------------------------------------------------------------------------------------
        # Add Side Bar to Main Window
        self.sidebar = QWidget()
        loadUi('ui/side_bar.ui', self.sidebar)

        # Add the sidebar to the layout
        layout.addWidget(self.sidebar)
        layout.setSpacing(0)
        # Connect the logout button signal to a slot
        self.sidebar.findChild(QPushButton, 'logout_button').clicked.connect(self.logout)
        
        #------------------------------------------------------------------------------------------------------------------
        #   VBOX FOR TOP BAR, SEARCH BAR, AND TABLE VIEW
        #------------------------------------------------------------------------------------------------------------------
        vbox = QVBoxLayout()
        vbox.setSpacing(0)

        # Load and add top_bar.ui
        top_bar = QWidget()
        loadUi('ui/top_bar.ui', top_bar)
        vbox.addWidget(top_bar)

        # Load and add search_bar.ui
        search_bar = QWidget()
        loadUi('ui/search_bar.ui', search_bar)
        vbox.addWidget(search_bar)

        # Load and add table_view.ui
        table_view = QWidget()
        loadUi('ui/table_view.ui', table_view)
        vbox.addWidget(table_view)

        # Load and add bottom_bar.ui
        bottom_bar = QWidget()
        loadUi('ui/bottom_bar.ui', bottom_bar)
        vbox.addWidget(bottom_bar)
        
        # Add the vbox to the layout
        layout.addLayout(vbox)

        self.setWindowTitle('Main Window with Sidebar and Spacer')

    def logout(self):
        print("Logout button clicked!")
        # Here you can add the logic for logging out

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
