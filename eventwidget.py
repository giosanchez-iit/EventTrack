import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QTableWidget,
    QVBoxLayout,
    QHeaderView,
    QTableWidgetItem,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QDialog,
    QLabel,
    QHBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from db_crudl import DatabaseCRUDL


class EventWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Event Window")
        self.setGeometry(100, 100, 800, 600)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Description", "Start Date", "End Date", "Location", "Edit/Delete"])
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStyleSheet("""font: 14pt "Gotham";""")
        self.tableWidget.verticalHeader().setDefaultSectionSize(70)
        for i in range(1, 5):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.repopulate()

    def repopulate(self, thingtoquery=None):
        self.tableWidget.clearContents()
        cc = DatabaseCRUDL()
        events = cc.listEvent()
        self.tableWidget.setRowCount(len(events))
        for i, (event_id, description, date_start, date_end, location) in enumerate(events):
            item_description = QTableWidgetItem(description)
            item_date_start = QTableWidgetItem(str(date_start))
            item_date_end = QTableWidgetItem(str(date_end))
            item_location = QTableWidgetItem(location)
            edit_delete_widget = ButtonForEditDeleteEvent(event_id, description, date_start, date_end, location, self)

            self.tableWidget.setItem(i, 0, item_description)
            self.tableWidget.setItem(i, 1, item_date_start)
            self.tableWidget.setItem(i, 2, item_date_end)
            self.tableWidget.setItem(i, 3, item_location)
            self.tableWidget.setCellWidget(i, 4, edit_delete_widget)


class ButtonForEditDeleteEvent(QWidget):
    def __init__(self, event_id, description, date_start, date_end, location, parent_window):
        super().__init__()
        self.event_id = event_id
        self.description = description
        self.date_start = date_start
        self.date_end = date_end
        self.location = location
        self.parent_window = parent_window  # Store the reference to the parent window
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        
        # Edit Button
        self.edit_button = QPushButton(None)
        self.edit_button.setFixedSize(60, 60)
        self.edit_button.setText(None)
        self.edit_button.setStyleSheet("""
            QPushButton {
                qproperty-icon: url(" "); 
                qproperty-iconSize: 16px 16px; 
                background-image: url("src/edit_off.png"); 
                background-repeat: no-repeat;
            }
            QPushButton:hover {
                background-image: url("src/edit_on.png"); 
                background-repeat: no-repeat;
            }
        """)
        self.edit_button.clicked.connect(self.editEvent)
        layout.addWidget(self.edit_button)

        # Delete Button
        self.delete_button = QPushButton(None)
        self.delete_button.setFixedSize(60, 60)
        self.delete_button.setText(None)
        self.delete_button.setStyleSheet("""
            QPushButton {
                qproperty-icon: url(" "); 
                qproperty-iconSize: 16px 16px; 
                background-image: url("src/delete_off.png");
                background-repeat: no-repeat;
            }
            QPushButton:hover {
                background-image: url("src/delete_on.png");
                background-repeat: no-repeat;
            }
        """)
        self.delete_button.clicked.connect(lambda: self.deleteEvent(self.event_id))
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def editEvent(self):
        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle("Edit Event")
        edit_layout = QVBoxLayout(edit_dialog)
        edit_layout.setSpacing(10)
        edit_layout.setContentsMargins(20, 20, 20, 20)

        description_label = QLabel("Description:")
        description_input = QLineEdit()
        description_input.setText(self.description)
        date_start_label = QLabel("Start Date:")
        date_start_input = QLineEdit()
        date_start_input.setText(str(self.date_start))
        date_end_label = QLabel("End Date:")
        date_end_input = QLineEdit()
        date_end_input.setText(str(self.date_end))
        location_label = QLabel("Location:")
        location_input = QLineEdit()
        location_input.setText(self.location)

        edit_layout.addWidget(description_label)
        edit_layout.addWidget(description_input)
        edit_layout.addWidget(date_start_label)
        edit_layout.addWidget(date_start_input)
        edit_layout.addWidget(date_end_label)
        edit_layout.addWidget(date_end_input)
        edit_layout.addWidget(location_label)
        edit_layout.addWidget(location_input)

        confirm_button = QPushButton("Confirm")
        cancel_button = QPushButton("Cancel")

        confirm_button.clicked.connect(lambda: self.updateEvent(description_input.text(), date_start_input.text(), date_end_input.text(), location_input.text()))
        cancel_button.clicked.connect(edit_dialog.reject)

        edit_layout.addWidget(confirm_button)
        edit_layout.addWidget(cancel_button)

        edit_dialog.exec_()

    def updateEvent(self, description, date_start, date_end, location):
        cc = DatabaseCRUDL()
        cc.updateEvent(self.event_id, description, date_start, date_end, location)

        event_window = self.parent_window
        event_window.repopulate() 
        
    def deleteEvent(self, event_id):
        if self.show_confirmation_message('Delete', "Delete this event?"):
            cc = DatabaseCRUDL()
            cc.deleteEvent(event_id)
            self.parent_window.repopulate()

    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg_box.exec_()
        return retval == QMessageBox.Yes

class CreateEventDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Create Event")
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Description Input
        description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        layout.addWidget(description_label)
        layout.addWidget(self.description_input)

        # Start Date Input
        start_date_label = QLabel("Start Date:")
        self.start_date_input = QLineEdit()
        layout.addWidget(start_date_label)
        layout.addWidget(self.start_date_input)

        # End Date Input
        end_date_label = QLabel("End Date:")
        self.end_date_input = QLineEdit()
        layout.addWidget(end_date_label)
        layout.addWidget(self.end_date_input)

        # Location Input
        location_label = QLabel("Location:")
        self.location_input = QLineEdit()
        layout.addWidget(location_label)
        layout.addWidget(self.location_input)

        # Confirm and Cancel Buttons
        confirm_button = QPushButton("Create")
        cancel_button = QPushButton("Cancel")
        confirm_button.clicked.connect(self.createEvent)
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(confirm_button)
        layout.addWidget(cancel_button)

    def createEvent(self):
        description = self.description_input.text()
        start_date = self.start_date_input.text()
        end_date = self.end_date_input.text()
        location = self.location_input.text()
        if description and start_date and end_date and location:
            cc = DatabaseCRUDL()
            cc.createEvent(description, start_date, end_date, location)
            self.parent().repopulate()
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "All fields must be filled.")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EventWindow()
    window.show()
    sys.exit(app.exec_())
