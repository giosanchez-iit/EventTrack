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
from PyQt5.uic import loadUi


class AwardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Award Window")
        self.setGeometry(100, 100, 800, 600)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Award Name", "Date Awarded", "Event", "Edit/Delete"])
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStyleSheet("""font: 14pt "Gotham";""")
        self.tableWidget.verticalHeader().setDefaultSectionSize(70)
        for i in range(1, 4):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.repopulate()

    def repopulate(self, thingtoquery=None):
        self.tableWidget.clearContents()
        cc = DatabaseCRUDL()
        awards = cc.listAward()
        self.tableWidget.setRowCount(len(awards))
        for i, (award_id, award_name, date_awarded, event_id) in enumerate(awards):
            item_award_name = QTableWidgetItem(award_name)
            item_date_awarded = QTableWidgetItem(str(date_awarded))
            event_desc = cc.readEvent(event_id)[0][1]
            item_event = QTableWidgetItem(event_desc)
            edit_delete_widget = ButtonForEditDeleteAward(self, award_id, award_name, date_awarded, event_id)

            self.tableWidget.setItem(i, 0, item_award_name)
            self.tableWidget.setItem(i, 1, item_date_awarded)
            self.tableWidget.setItem(i, 2, item_event)
            self.tableWidget.setCellWidget(i, 3, edit_delete_widget)


class ButtonForEditDeleteAward(QWidget):
    def __init__(self, parent, award_id, award_name, date_awarded, event_id):
        super().__init__()
        self.parent = parent
        self.award_id = award_id
        self.award_name = award_name
        self.date_awarded = date_awarded
        self.event_id = event_id
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
        self.edit_button.clicked.connect(self.editAward)
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
        self.delete_button.clicked.connect(lambda: self.deleteAward(self.award_id))
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def editAward(self):
        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle("Edit Award")
        edit_layout = QVBoxLayout(edit_dialog)
        edit_layout.setSpacing(10)
        edit_layout.setContentsMargins(20, 20, 20, 20)

        award_name_label = QLabel("Award Name:")
        self.award_name_input = QLineEdit()
        self.award_name_input.setText(self.award_name)
        date_awarded_label = QLabel("Date Awarded:")
        self.date_awarded_input = QLineEdit()
        self.date_awarded_input.setText(str(self.date_awarded))

        edit_layout.addWidget(award_name_label)
        edit_layout.addWidget(self.award_name_input)
        edit_layout.addWidget(date_awarded_label)
        edit_layout.addWidget(self.date_awarded_input)

        confirm_button = QPushButton("Confirm")
        cancel_button = QPushButton("Cancel")

        confirm_button.clicked.connect(lambda: self.updateAward(edit_dialog))
        cancel_button.clicked.connect(edit_dialog.reject)

        edit_layout.addWidget(confirm_button)
        edit_layout.addWidget(cancel_button)

        edit_dialog.exec_()

    def updateAward(self, edit_dialog):
        new_award_name = self.award_name_input.text()
        new_date_awarded = self.date_awarded_input.text()
        cc = DatabaseCRUDL()
        cc.updateAward(self.award_id, new_award_name, new_date_awarded)
        self.parent.repopulate()
        edit_dialog.accept()

    def deleteAward(self, award_id):
        if self.show_confirmation_message('Delete', "Delete this award?"):
            cc = DatabaseCRUDL()
            cc.deleteAward(award_id)
            self.parent.repopulate()

    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg_box.exec_()
        return retval == QMessageBox.Yes

class CreateAwardDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Create Award")
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Award Name Input
        award_name_label = QLabel("Award Name:")
        self.award_name_input = QLineEdit()
        layout.addWidget(award_name_label)
        layout.addWidget(self.award_name_input)

        # Date Awarded Input
        date_awarded_label = QLabel("Date Awarded:")
        self.date_awarded_input = QLineEdit()
        layout.addWidget(date_awarded_label)
        layout.addWidget(self.date_awarded_input)

        # Event
        event_id_label = QLabel("Event:")
        self.event_id_input = QLineEdit()
        layout.addWidget(event_id_label)
        layout.addWidget(self.event_id_input)

        # Confirm and Cancel Buttons
        confirm_button = QPushButton("Create")
        cancel_button = QPushButton("Cancel")
        confirm_button.clicked.connect(self.createAward)
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(confirm_button)
        layout.addWidget(cancel_button)

    def createAward(self):
        award_name = self.award_name_input.text()
        date_awarded = self.date_awarded_input.text()
        event_id = self.event_id_input.text()
        if award_name and date_awarded:
            cc = DatabaseCRUDL()
            cc.createAward(award_name, date_awarded, event_id)
            self.parent().repopulate()
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "All fields must be filled.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AwardWindow()
    window.show()
    sys.exit(app.exec_())
