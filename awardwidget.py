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
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

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
            edit_delete_widget = ButtonForEditDeleteAward(award_id, award_name, date_awarded, event_id)

            self.tableWidget.setItem(i, 0, item_award_name)
            self.tableWidget.setItem(i, 1, item_date_awarded)
            self.tableWidget.setItem(i, 2, item_event)
            self.tableWidget.setCellWidget(i, 3, edit_delete_widget)

class ButtonForEditDeleteAward(QWidget):
    def __init__(self, award_id, award_name, date_awarded, event_id):
        super().__init__()
        self.award_id = award_id
        self.award_name = award_name
        self.date_awarded = date_awarded
        self.event_id = event_id
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)

        self.edit_button.clicked.connect(self.editAward)
        self.delete_button.clicked.connect(lambda: self.deleteAward(self.award_id))

    def editAward(self):
        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle("Edit Award")
        edit_layout = QVBoxLayout(edit_dialog)
        edit_layout.setSpacing(10)
        edit_layout.setContentsMargins(20, 20, 20, 20)

        award_name_label = QLabel("Award Name:")
        award_name_input = QLineEdit()
        award_name_input.setText(self.award_name)
        date_awarded_label = QLabel("Date Awarded:")
        date_awarded_input = QLineEdit()
        date_awarded_input.setText(str(self.date_awarded))

        edit_layout.addWidget(award_name_label)
        edit_layout.addWidget(award_name_input)
        edit_layout.addWidget(date_awarded_label)
        edit_layout.addWidget(date_awarded_input)

        confirm_button = QPushButton("Confirm")
        cancel_button = QPushButton("Cancel")

        confirm_button.clicked.connect(lambda: self.updateAward(award_name_input.text(), date_awarded_input.text()))
        cancel_button.clicked.connect(edit_dialog.reject)

        edit_layout.addWidget(confirm_button)
        edit_layout.addWidget(cancel_button)

        edit_dialog.show()

    def updateAward(self, award_name, date_awarded):
        cc = DatabaseCRUDL()
        cc.updateAward(self.award_id, award_name, date_awarded)

    def deleteAward(self, award_id):
        if self.show_confirmation_message('Delete', "Delete this award?"):
            cc = DatabaseCRUDL()
            cc.deleteAward(award_id)

    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg_box.exec_()
        return retval == QMessageBox.Yes