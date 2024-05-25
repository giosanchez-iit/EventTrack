import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy, QPushButton, QLineEdit, QTableView, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QRect, QMetaObject
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from db_crudl import CRUDL, display_awards_by_constituent_id, display_awards_for_event, display_constituents_by_award_id, display_events_and_awards_by_constituent_id, display_events_by_constituent_id, display_members_by_comm_code
from PyQt5.uic import loadUi
import subprocess
from dialogs import CreateCommitteeDialog, CreateConstituentDialog, CreateEventDialog, UpdateAwardDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet("""background-color:white;""")
        self.currentMode = 'constituent'
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
        self.top_bar = QWidget()
        loadUi('ui/top_bar.ui', self.top_bar)
        vbox.addWidget(self.top_bar)
        
        self.top_bar.findChild(QPushButton, 'awards_button').clicked.connect(lambda: self.mode_switch('award'))
        self.top_bar.findChild(QPushButton, 'committees_button').clicked.connect(lambda: self.mode_switch('committee'))
        self.top_bar.findChild(QPushButton, 'events_button').clicked.connect(lambda: self.mode_switch('event'))
        self.top_bar.findChild(QPushButton, 'constituents_button').clicked.connect(lambda: self.mode_switch('constituent'))
        
        # Load and add search_bar.ui
        search_bar = QWidget()
        loadUi('ui/search_bar.ui', search_bar)
        vbox.addWidget(search_bar)
        
        self.searchQuery = search_bar.findChild(QLineEdit, 'lineEdit')

        # Load and add table_view.ui
        table_view_widget = QWidget()
        loadUi('ui/table_view.ui', table_view_widget)
        vbox.addWidget(table_view_widget)
        self.table = QTableWidget()
        self.table = table_view_widget.findChild(QTableWidget, 'tableWidget')
        

        table_view = QWidget()
        loadUi('ui/bottom_bar.ui', table_view)
        vbox.addWidget(table_view)
        
        # Add the vbox to the layout
        layout.addLayout(vbox)

        self.setWindowTitle('Main Window with Sidebar and Spacer')
        
        self.findChild(QPushButton, 'createNew').clicked.connect(self.open_popup)
        
    def open_popup(self):
        if self.currentMode == 'constituent':
            dialog = CreateConstituentDialog(self)
            dialog.closed.connect(self.mode_switch)
            dialog.exec_()
        elif self.currentMode == 'award':
            # You'll need to pass the award_id to the UpdateAwardDialog
            award_id = 1  # Replace with the appropriate award_id
            dialog = UpdateAwardDialog(award_id, self)
            dialog.closed.connect(self.mode_switch)
            dialog.exec_()
        elif self.currentMode == 'event':
            dialog = CreateEventDialog(self)
            dialog.closed.connect(self.mode_switch)
            dialog.exec_()
        elif self.currentMode == 'committee':
            dialog = CreateCommitteeDialog(self)
            dialog.closed.connect(self.mode_switch)
            dialog.exec_()

        # Reload the table after the dialog is closed
        if self.currentMode == 'award':
            self.reloadTableWithAwards()
        elif self.currentMode == 'committee':
            self.reloadTableWithCommittees()
        elif self.currentMode == 'event':
            self.reloadTableWithEvents()
        else:  # constituents
            self.reloadTableWithConstituents()
    
    def show_message_box(self, message_text):
        app = QApplication([])  # Initialize the QApplication instance
        msg_box = QMessageBox()  # Create a QMessageBox instance
        msg_box.setWindowTitle("Information")  # Set the window title
        msg_box.setText(message_text)  # Set the message text
        msg_box.exec_()  # Show the message box
    
    def mode_switch(self, mode=None):
        self.searchQuery.clear()
        if mode:
            self.currentMode = mode
        on = """
        background-color: rgb(231, 231, 221);
        color: black;
		font: 10pt "Gotham";
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 0px;
        """
        off = """
        QPushButton {
		background-color: rgb(57, 57, 55);
        color: rgb(231, 231, 221);
		font: 10pt "Gotham";
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 0px;
        }
        QPushButton:hover {
            background-color: rgb(231, 231, 221);
            color: black;
        }
        """
        self.top_bar.findChild(QPushButton, 'awards_button').setStyleSheet(off)
        self.top_bar.findChild(QPushButton, 'committees_button').setStyleSheet(off)
        self.top_bar.findChild(QPushButton, 'events_button').setStyleSheet(off)
        self.top_bar.findChild(QPushButton, 'constituents_button').setStyleSheet(off)
        if mode == 'award':
            self.top_bar.findChild(QPushButton, 'awards_button').setStyleSheet(on)
            self.reloadTableWithAwards()
        elif mode == 'committee':
            self.top_bar.findChild(QPushButton, 'committees_button').setStyleSheet(on)
            self.reloadTableWithCommittees()
        elif mode == 'event':
            self.top_bar.findChild(QPushButton, 'events_button').setStyleSheet(on)
            self.reloadTableWithEvents()
        else: #constituents
            self.top_bar.findChild(QPushButton, 'constituents_button').setStyleSheet(on)
            self.reloadTableWithConstituents()
                  
    def logout(self):
        subprocess.Popen(["python", "login_page.py"])
        self.close()
    
    def reloadTableWithEvents(self):
        self.clearTable()
        crudl = CRUDL()
        results = crudl.list('event')
        self.table.setRowCount(len(results))
        self.table.setColumnCount(len(results[0]) + 1)  # Adjusted to match the corrected logic below
        
        for row_number, row_data in enumerate(results):
            # Fetch the event_id for the current row
            query = f"""SELECT event_id FROM event WHERE event_id = {row_data[0]} LIMIT 1;"""
            idNum = crudl.executeQuery(query)[0][0]
            
            for column_number, data in enumerate(row_data[1:], start=1):  # Start from index 1 to skip the first column
                self.table.setItem(row_number, column_number - 1, QTableWidgetItem(str(data)))  # Adjust column index
            
            # Assign the correct idNum to each button
            viewinfo_button = QPushButton("View All Awards")
            viewinfo_button.clicked.connect(lambda _, idNum=idNum: display_awards_for_event(idNum))
            self.table.setCellWidget(row_number, len(row_data) - 1, viewinfo_button)  # Adjust column index
            
            viewinfo_button = QPushButton("Delete")
            viewinfo_button.clicked.connect(lambda _, rowId=idNum: self.deleteRow(rowId, self.currentMode))
            self.table.setCellWidget(row_number, len(row_data), viewinfo_button)  # Adjust column index


            
    def reloadTableWithCommittees(self):
        self.clearTable()
        crudl = CRUDL()
        results = crudl.list('committee')
        self.table.setRowCount(len(results))
        self.table.setColumnCount(len(results[0]) + 2)
        for row_number, row_data in enumerate(results):
            # Fetch the event_id for the current row
            query = f"""SELECT comm_code FROM committee WHERE comm_code = {row_data[0]} LIMIT 1;"""
            commcode = crudl.executeQuery(query)[0][0]
            for column_number, data in enumerate(row_data[1:], start=1):  # Start from index 1 to skip the first column
                self.table.setItem(row_number, column_number - 1, QTableWidgetItem(str(data)))  # Adjust column index
            viewinfo_button = QPushButton("View All Members")
            viewinfo_button.clicked.connect(lambda _, commcode=commcode: display_members_by_comm_code(commcode))
            self.table.setCellWidget(row_number, len(row_data) - 1, viewinfo_button)  # Adjust column index
            viewinfo_buttone = QPushButton("Edit")
            viewinfo_buttone.clicked.connect(lambda _, row_data=row_data: self.openEditCommittee(name_id=row_data[0], name_edit=row_data[1]))
            self.table.setCellWidget(row_number, len(row_data), viewinfo_buttone)  # Adjust column index
            viewinfo_buttond = QPushButton("Delete")
            viewinfo_buttond.clicked.connect(lambda _, rowId=commcode: self.deleteRow(rowId, self.currentMode))
            self.table.setCellWidget(row_number, len(row_data) + 1, viewinfo_buttond)  # Adjust column index
            
    def reloadTableWithAwards(self):
        self.clearTable()
        crudl = CRUDL()
        query = """
            SELECT award.award_name, award.date_awarded, event.description
            FROM award
            LEFT JOIN event ON award.event_id = event.event_id;
        """
        results = crudl.executeQuery(query)
        self.table.setRowCount(len(results))
        self.table.setColumnCount(len(results[0]) + 2)
        
        for row_number, row_data in enumerate(results):
            # Fetch the event_id for the current row
            query = f"""select award_id from award limit 1 offset {row_number};"""
            awardid = crudl.executeQuery(query)[0][0]
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            viewinfo_button = QPushButton("View All Awardees")
            viewinfo_button.clicked.connect(lambda _, awardid=awardid: display_constituents_by_award_id(awardid))
            self.table.setCellWidget(row_number, len(row_data), viewinfo_button)
            viewinfo_buttond = QPushButton("Delete")
            viewinfo_buttond.clicked.connect(lambda _, rowId=awardid: self.deleteRow(rowId, self.currentMode))
            self.table.setCellWidget(row_number, len(row_data)+1, viewinfo_buttond)
            
    def reloadTableWithConstituents(self):
        self.clearTable()
        crudl = CRUDL()
        query = """
            SELECT
                Constituent.constituent_name,
                Constituent.contact_info,
                Constituent.start_date,
                Committee.comm_name
            FROM
                Constituent
            LEFT JOIN
                Committee ON Constituent.comm_code = Committee.comm_code
        """
        results = crudl.executeQuery(query)
        self.table.setRowCount(len(results))
        self.table.setColumnCount(len(results[0]) + 5)
        
        for row_number, row_data in enumerate(results):
            query = f"""select constituent_id from constituent limit 1 offset {row_number};"""
            constid = crudl.executeQuery(query)[0][0]
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            viewinfo_button1 = QPushButton("View Events")
            viewinfo_button1.clicked.connect(lambda _, constid=constid: display_events_by_constituent_id(constid))
            self.table.setCellWidget(row_number, len(row_data), viewinfo_button1)
            viewinfo_button2 = QPushButton("View Awards")
            self.table.setCellWidget(row_number, len(row_data)+1, viewinfo_button2)
            viewinfo_button2.clicked.connect(lambda _, constid=constid: display_awards_by_constituent_id(constid))
            viewinfo_button3 = QPushButton("View Info")
            viewinfo_button3.clicked.connect(lambda _, constid=constid: display_events_and_awards_by_constituent_id(constid))
            self.table.setCellWidget(row_number, len(row_data)+2, viewinfo_button3)
            viewinfo_buttone = QPushButton("Edit")
            self.table.setCellWidget(row_number, len(row_data)+3, viewinfo_buttone)
            viewinfo_buttond = QPushButton("Delete")
            viewinfo_buttond.clicked.connect(lambda _, rowId=constid: self.deleteRow(rowId, self.currentMode))
            self.table.setCellWidget(row_number, len(row_data)+4, viewinfo_buttond)

    def deleteRow(self, rowId, mode):
        # Prompt the user for confirmation
        reply = QMessageBox.question(self, 'Confirmation', "Are you sure you want to delete?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Perform deletion based on the current mode
            cc = CRUDL()
            if mode == 'award':
                cc.delete(mode, 'award_id', rowId)
            elif mode == 'committee':
                cc.delete(mode, 'comm_code ', rowId)
            elif mode == 'event':
                cc.delete(mode, 'event_id', rowId)
            else:  # constituents
                cc.delete(mode, 'constituent_id', rowId)
            self.mode_switch()

    def clearTable(self):
        self.table.clear()
        
    def openEditCommittee(self, name_id=None, name_edit=None):
        dialog = CreateCommitteeDialog(self, name_id=name_id, name_edit=name_edit)
        dialog.closed.connect(self.mode_switch)
        dialog.exec_()
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
