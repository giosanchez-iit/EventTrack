import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt5.QtCore import QRect, QMetaObject
from PyQt5.uic import loadUi
from constituentwidget import ConstituentWindow, CreateConstituentDialog
from committeewidget import CommitteeWindow, CreateCommitteeDialog
from awardwidget import AwardWindow, CreateAwardDialog
from eventwidget import EventWindow, CreateEventDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.mode = 'constituent'
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet("""
                           QTableWidget {
                                border: none;
                                font: 14pt "SF Pro Display";
                            }

                            QHeaderView::section {
                                padding: 4px;
                                border: none;
                                font: 14pt "Gotham";
                            }

                            QTableWidget::item {
                                border: none;
                                padding-left: 5px;
                                padding-right: 5px;
                                font: 14pt "SF Pro Display";
                            }
                           """)
        layout = QHBoxLayout(central_widget)

        # SIDEBAR
        self.sidebar = QWidget()
        loadUi('ui/side_bar.ui', self.sidebar)

        # Add the sidebar to the layout
        layout.addWidget(self.sidebar)
        layout.setSpacing(0)

        # VBOX FOR TOP BAR, SEARCH BAR, AND CONSTITUENT WINDOW
        vbox = QVBoxLayout()
        vbox.setSpacing(0)

        # Load and add top_bar.ui
        self.top_bar = QWidget()
        loadUi('ui/top_bar.ui', self.top_bar)
        vbox.addWidget(self.top_bar)
        awards_button = QPushButton()
        committees_button = QPushButton()
        constituents_button = QPushButton()
        events_button = QPushButton()
        awards_button = self.top_bar.findChild(QPushButton, 'awards_button')
        committees_button = self.top_bar.findChild(QPushButton, 'committees_button')
        constituents_button = self.top_bar.findChild(QPushButton, 'constituents_button')
        events_button = self.top_bar.findChild(QPushButton, 'events_button')
        awards_button.clicked.connect(self.settableaward)
        committees_button.clicked.connect(self.settablecommittee)
        constituents_button.clicked.connect(self.settableconstituent)
        events_button.clicked.connect(self.settableevent)
        
        # Load and add search_bar.ui
        search_bar = QWidget()
        loadUi('ui/search_bar.ui', search_bar)
        search_bar_line_edit = QLineEdit()
        search_bar_line_edit = search_bar.findChild(QLineEdit, 'lineEdit')
        #vbox.addWidget(search_bar)

        self.table = ConstituentWindow()
        vbox.addWidget(self.table)
        self.table2 = CommitteeWindow()
        vbox.addWidget(self.table2)
        self.table2.hide()
        self.table3 = AwardWindow()
        vbox.addWidget(self.table3)
        self.table3.hide()
        self.table4 = EventWindow()
        vbox.addWidget(self.table4)
        self.table4.hide()

        table_view = QWidget()
        loadUi('ui/bottom_bar.ui', table_view)
        create_button = QPushButton()
        create_button = table_view.findChild(QPushButton, 'createNew')
        create_button.clicked.connect(self.createNew)
        vbox.addWidget(table_view)

        # Add the vbox to the layout
        layout.addLayout(vbox)

        self.setWindowTitle('Main Window')
        
        # FUNCTIONALITY
        search_bar_line_edit.textChanged.connect(lambda: self.table.repopulate(search_bar_line_edit.text()))
    
    def createNew(self):
        if self.mode == 'constituent':
            create_constituent_dialog = CreateConstituentDialog(self.table)
            create_constituent_dialog.exec_()
        elif self.mode == 'committee':
            create_committee_dialog = CreateCommitteeDialog(self.table2)
            create_committee_dialog.exec_()
        elif self.mode == 'award':
            create_award_dialog = CreateAwardDialog(self.table3)
            create_award_dialog.exec_()
        elif self.mode == 'event':
            create_event_dialog = CreateEventDialog(self.table4)
            create_event_dialog.exec_()
            

    def settableconstituent(self):
        self.mode = 'constituent'
        self.table.show()
        self.table2.hide()
        self.table3.hide()
        self.table4.hide()
    def settablecommittee(self):
        self.mode = 'committee'
        self.table.hide()
        self.table2.show()
        self.table3.hide()
        self.table4.hide()
    def settableaward(self):
        self.mode = 'award'
        self.table.hide()
        self.table2.hide()
        self.table3.show()
        self.table4.hide()
    def settableevent(self):
        self.mode = 'event'
        self.table.hide()
        self.table2.hide()
        self.table3.hide()
        self.table4.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())