import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QTableWidget,
    QVBoxLayout,
    QHeaderView,
    QTableWidgetItem,
    QPushButton,
    QMessageBox
)

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from db_crudl import DatabaseCRUDL

from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QLabel

class EditCommitteeDialog(QDialog):
    def __init__(self, committee_id, committee_name, parent=None):
        super().__init__(parent)
        self.committee_id = committee_id
        self.committee_name = committee_name
        self.setWindowTitle("Edit Committee Name")

        layout = QVBoxLayout(self)
        self.name_edit = QLineEdit(self)
        self.name_edit.setText(committee_name)
        layout.addWidget(QLabel("New Committee Name:"))
        layout.addWidget(self.name_edit)

        confirm_button = QPushButton("Confirm", self)
        confirm_button.clicked.connect(self.accept)
        layout.addWidget(confirm_button)

    def accept(self):
        if self.name_edit.text().strip():
            self.parent().editCommittee(self.committee_id, self.name_edit.text())
        else:
            QMessageBox.warning(self, "Warning", "Committee name cannot be blank.")
            self.reject()
            
class ButtonForEditCommittee(QWidget):
    def __init__(self, committee_id, committee_name):
        super().__init__()
        self.committee_id = committee_id
        self.committee_name = committee_name
        self.layout = QVBoxLayout(self)
        self.button = QPushButton(None)
        self.button.setFixedSize(60, 60)
        self.button.setText(None)
        self.button.clicked.connect(lambda: self.showEditDialog())
        self.button.setStyleSheet("""
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
        self.layout.addWidget(self.button)
        self.layout.setStretchFactor(self.button, 1)
        
    def showEditDialog(self):
        dialog = EditCommitteeDialog(self.committee_id, self.committee_name, self)
        dialog.exec_()
        
    def editCommittee(self, committee_id, new_name):
        if self.show_confirmation_message('Update', f"Update committee name from '{self.committee_name}' to '{new_name}'?"):
            cc = DatabaseCRUDL()
            cc.updateCommittee(committee_id, new_name)
            self.committee_name = new_name  # Update the local state

    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg_box.exec_()
        return retval == QMessageBox.Yes


class ButtonForDeleteCommittee(QWidget):
    def __init__(self, committee_id, committee_name):
        super().__init__()
        self.committee_name = committee_name
        self.layout = QVBoxLayout(self)
        self.button = QPushButton(None)
        self.button.setFixedSize(60, 60)
        self.button.setText(None)
        self.button.clicked.connect(lambda: self.deleteCommittee(committee_id))
        self.button.setStyleSheet("""
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
        self.layout.addWidget(self.button)
        self.layout.setStretchFactor(self.button, 1)
        
    def deleteCommittee(self, committee_id):
        if self.show_confirmation_message('Delete', f"Delete committee {self.committee_name}?"):
            cc = DatabaseCRUDL()
            cc.deleteCommittee(committee_id)

    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg_box.exec_()
        return retval == QMessageBox.Yes

class CommitteeWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle("Committee Window")
        self.setGeometry(100, 100, 800, 600)

        # Create table widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3) 
        self.tableWidget.setHorizontalHeaderLabels(["Committee Name", "Edit", "Delete"])
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStyleSheet("""font: 14pt "Gotham";""")
        self.tableWidget.verticalHeader().setDefaultSectionSize(70)
        for i in range(1, 3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        
        # Create layout and add table widget
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.repopulate()

    def repopulate(self, thingtoquery=None):
        self.tableWidget.clearContents()  
        cc = DatabaseCRUDL()
        committees = cc.listCommitteeForTable(thingtoquery)
        self.tableWidget.setRowCount(len(committees)) 
        
        for i, (committee_id, committee_name) in enumerate(committees):
            item_name = QTableWidgetItem(committee_name)
            self.tableWidget.setItem(i, 0, item_name) 
            
            # Now set the cell widgets for the buttons
            edit_button = ButtonForEditCommittee(committee_id, committee_name)
            delete_button = ButtonForDeleteCommittee(committee_id, committee_name)
            self.tableWidget.setCellWidget(i, 1, edit_button)
            self.tableWidget.setCellWidget(i, 2, delete_button)
