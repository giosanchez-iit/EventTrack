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
    QHBoxLayout,
    QComboBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from db_crudl import DatabaseCRUDL
from PyQt5.uic import loadUi


class ButtonForDeleteConstituentEvent(QWidget):
    def __init__(self, member_id, event_id, name, event_desc):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.button = QPushButton(None)
        self.button.setFixedSize(60, 60)
        self.button.setText(None)
        self.button.clicked.connect(lambda: self.deleteEvent(member_id, event_id, name, event_desc))
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

    def deleteEvent(self, member_id, event_id, name, event_desc):
        if self.show_confirmation_message('Delete', f"Delete {name} - {event_desc}?"):
            cc = DatabaseCRUDL()
            cc.deleteConstituentEvent(member_id, event_id)

    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg_box.exec_()
        return retval == QMessageBox.Yes

class ButtonForEventsConstituents(QWidget):
    def __init__(self, member_id, parent=None):
        super().__init__(parent)
        self.member_id = member_id
        self.parent_window = parent
        self.event_window = None  # Initialize event_window to None
        self.layout = QVBoxLayout(self)
        self.button = QPushButton(None)
        self.button.setFixedSize(60, 60)
        self.button.setText(None)
        self.button.clicked.connect(self.displayEvents)
        self.button.setStyleSheet("""
                                  QPushButton {
                                        qproperty-icon: url(" ");
                                        qproperty-iconSize: 16px 16px;
                                        background-image: url("src/event_off.png");
                                        background-repeat: no-repeat;
                                    }

                                    QPushButton:hover {
                                        background-image: url("src/event_on.png");
                                        background-repeat: no-repeat;
                                    }
                                  """)
        self.layout.addWidget(self.button)
        self.layout.setStretchFactor(self.button, 1)

    def displayEvents(self):
        if not self.event_window or not self.event_window.isVisible():
            self.event_window = ConstituentEventWindow(self.member_id, self.parent_window)
            self.event_window.show()
        
class ButtonForAwardsConstituents(QWidget):
    def __init__(self, member_id, parent=None):
        super().__init__(parent)
        self.member_id = member_id
        self.parent_window = parent
        self.layout = QVBoxLayout(self)
        self.button = QPushButton(None)
        self.button.setFixedSize(60, 60)
        self.button.setText(None)
        self.button.clicked.connect(lambda: self.displayAwards())
        self.button.setStyleSheet("""
                                  QPushButton {
                                        qproperty-icon: url(" "); 
                                        qproperty-iconSize: 16px 16px; 
                                        background-image: url("src/award_off.png");
                                        background-repeat: no-repeat;
                                    }

                                    QPushButton:hover {
                                        background-image: url("src/award_on.png");
                                        background-repeat: no-repeat;
                                    }
                                  """)
        self.layout.addWidget(self.button)
        self.layout.setStretchFactor(self.button, 1)
        
    def displayAwards(self):
        award_window = ConstituentAwardWindow(self.member_id, self.parent_window)
        award_window.show()

class ButtonForEditConstituents(QWidget):
    def __init__(self, member_id, parent_window):
        super().__init__()
        self.member_id = member_id
        self.parent_window = parent_window
        self.layout = QVBoxLayout(self)
        self.button = QPushButton(None)
        self.button.setFixedSize(60, 60)
        self.button.setText(None)
        self.button.clicked.connect(lambda: self.editMember(member_id))
        self.button.setStyleSheet("""
                                  QPushButton {
                                        qproperty-icon: url(" "); 
                                        qproperty-iconSize: 16px 16px; 
                                        background-image: url("src/edit_off.png"); /* Ensure you have an edit_off.png */
                                        background-repeat: no-repeat;
                                    }

                                    QPushButton:hover {
                                        background-image: url("src/edit_on.png"); /* Ensure you have an edit_on.png */
                                        background-repeat: no-repeat;
                                    }
                                  """)
        self.layout.addWidget(self.button)
        self.layout.setStretchFactor(self.button, 1)
        
    def editMember(self, member_id):
        # Open a dialog for editing member details
        cc = DatabaseCRUDL()
        info = cc.listConstituentForTable(constituent_id=member_id)[0]
        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle("Edit Member")
        edit_layout = QVBoxLayout(edit_dialog)
        edit_layout.setSpacing(10)
        edit_layout.setContentsMargins(20, 20, 20, 20)

        # Assuming you have fields like name, contact info, etc., in your database
        name_label = QLabel("Name:")
        name_input = QLineEdit()
        name_input.setText(info[1])
        contact_info_label = QLabel("Contact Info:")
        contact_info_input = QLineEdit()
        contact_info_input.setText(info[2])
        committee_label = QLabel("Committee:")
        committee_input = CommitteeComboBox()
        
        # Set the current selection of the CommitteeComboBox to the committee of the member
        for i in range(committee_input.count()):
            if committee_input.itemText(i) == info[4]:
                committee_input.setCurrentIndex(i)
                break

        edit_layout.addWidget(name_label)
        edit_layout.addWidget(name_input)
        edit_layout.addWidget(contact_info_label)
        edit_layout.addWidget(contact_info_input)
        edit_layout.addWidget(committee_label)
        edit_layout.addWidget(committee_input)

        confirm_button = QPushButton("Confirm")
        cancel_button = QPushButton("Cancel")

        confirm_button.clicked.connect(lambda: self.updateMember(member_id, name_input.text(), contact_info_input.text(), committee_input.selectedCommitteeCode()))
        cancel_button.clicked.connect(edit_dialog.reject)

        edit_layout.addWidget(confirm_button)
        edit_layout.addWidget(cancel_button)

        edit_dialog.exec_()

    def updateMember(self, member_id, name, contact_info, committee_code):
        cc = DatabaseCRUDL()
        cc.updateConstituent(member_id, name, contact_info, committee_code)
        self.parent_window.repopulate()  # Call repopulate method here

class ButtonForDeleteConstituents(QWidget):
    def __init__(self, member_id, parent_window):
        super().__init__()
        self.member_id = member_id
        self.parent_window = parent_window
        self.layout = QVBoxLayout(self)
        self.button = QPushButton(None)
        self.button.setFixedSize(60, 60)
        self.button.setText(None)
        self.button.clicked.connect(lambda: self.deleteMember(member_id))
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
        
    def deleteMember(self, member_id):
        if self.show_confirmation_message('Delete', f"Delete this member?"):
            cc = DatabaseCRUDL()
            cc.deleteConstituent(member_id)
            self.parent_window.repopulate()
            
    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg_box.exec_()
        return retval == QMessageBox.Yes
    
class ButtonForDeleteConstituentAward(QWidget):
    def __init__(self, member_id, award_id, name, award):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.button = QPushButton(None)
        self.button.setFixedSize(60, 60)
        self.button.setText(None)
        self.button.clicked.connect(lambda: self.deleteMember(member_id, award_id, name, award))
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
        
    def deleteMember(self, member_id, award_id, name, award):
        if self.show_confirmation_message('Delete', f"Delete {name} - {award}?"):
            cc = DatabaseCRUDL()
            cc.deleteConstituentAward(member_id, award_id)
            
    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg_box.exec_()
        return retval == QMessageBox.Yes

class ButtonForDeleteConstituentEvent(QWidget):
    def __init__(self, member_id, event_id, name, event_desc):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.button = QPushButton(None)
        self.button.setFixedSize(60, 60)
        self.button.setText(None)
        self.button.clicked.connect(lambda: self.deleteEvent(member_id, event_id, name, event_desc))
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

    def deleteEvent(self, member_id, event_id, name, event_desc):
        if self.show_confirmation_message('Delete', f"Delete {name} - {event_desc}?"):
            cc = DatabaseCRUDL()
            cc.deleteConstituentEvent(member_id, event_id)

    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg_box.exec_()
        return retval == QMessageBox.Yes
    
class ConstituentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle("Constituent Window")
        self.setGeometry(100, 100, 800, 600)

        # Create table widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(8) 
        self.tableWidget.setHorizontalHeaderLabels(["Member Name", "Contact Information", "Date Joined", "Committee", "View\nEvents", "View\nAwards", "Edit", "Delete"])
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStyleSheet("""font: 14pt "Gotham";""")
        self.tableWidget.verticalHeader().setDefaultSectionSize(70)
        for i in range(1,7):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        
        # Create layout and add table widget
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.repopulate()

    def repopulate(self, thingtoquery=None):
        self.tableWidget.clearContents()
        cc = DatabaseCRUDL()
        constis = cc.listConstituentForTable(thingtoquery)
        self.tableWidget.setRowCount(len(constis))
        for i, (memberid, name, contactinfo, datejoined, comm) in enumerate(constis):
            item_name = QTableWidgetItem(name)
            item_ci = QTableWidgetItem(contactinfo)
            item_dj = QTableWidgetItem(str(datejoined))
            item_cm = QTableWidgetItem(comm)    
            ve_widget = ButtonForEventsConstituents(memberid)
            va_widget = ButtonForAwardsConstituents(memberid, self)
            edit_button = ButtonForEditConstituents(memberid, self)
            delete_button = ButtonForDeleteConstituents(memberid, self)
    
            self.tableWidget.setItem(i, 0, item_name)
            self.tableWidget.setItem(i, 1, item_ci)
            self.tableWidget.setItem(i, 2, item_dj)
            self.tableWidget.setItem(i, 3, item_cm)
            self.tableWidget.setCellWidget(i, 4, ve_widget)
            self.tableWidget.setCellWidget(i, 5, va_widget)
            self.tableWidget.setCellWidget(i, 6, edit_button)
            self.tableWidget.setCellWidget(i, 7, delete_button)
            
class ConstituentAwardWindow(QDialog):
    def __init__(self, constituent_id, parent=None):
        super().__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.constituent_id = constituent_id
        cc = DatabaseCRUDL()
        self.constituent_name = cc.readConstituent(constituent_id)[0][1]
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"{self.constituent_name} - Award Window")
        self.setGeometry(100, 100, 800, 600)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Awards", "Delete"])
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStyleSheet("""font: 14pt "Gotham";""")
        self.tableWidget.verticalHeader().setDefaultSectionSize(70)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        search_bar = QWidget()
        loadUi('ui/search_bar.ui', search_bar)
        search_bar_line_edit = QLineEdit()
        search_bar_line_edit = search_bar.findChild(QLineEdit, 'lineEdit')

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.repopulate(self.constituent_id)

        search_bar_line_edit.textChanged.connect(lambda _: self.repopulate(self.constituent_id, search_bar_line_edit.text()))

        # Button to add a new award
        self.add_award_button = QPushButton("Add Award")
        self.add_award_button.clicked.connect(lambda _: self.openAddAwardDialog(constituentid=self.constituent_id))

        layout.addWidget(self.add_award_button)

    def repopulate(self, constid=None, thingtoquery=None):
        self.tableWidget.clearContents()
        cc = DatabaseCRUDL()
        constar = cc.listConstituentAwardForTable(constituentid=constid, thingtoquery=thingtoquery)
        self.tableWidget.setRowCount(len(constar))
        for i, (constid, awardid, consname, awardname, desc) in enumerate(constar):
            item_award = QTableWidgetItem(f"{desc}\n{awardname}")
            delete_button = ButtonForDeleteConstituentAward(constid, awardid, consname, awardname)
            self.tableWidget.setItem(i, 0, item_award)
            self.tableWidget.setCellWidget(i, 1, delete_button)

    def openAddAwardDialog(self, constituentid):
        add_award_dialog = AddAwardDialog(self.constituent_id, self)
        if add_award_dialog.exec_() == QDialog.Accepted:
            self.repopulate(self.constituent_id)
            
class AddAwardDialog(QDialog):
    def __init__(self, constituentid, parent=None):
        super().__init__(parent)
        self.initUI()
        self.constituentid = constituentid

    def initUI(self):
        self.setWindowTitle("Add Award")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.award_label = QLabel("Select Award:")
        self.award_combo = AwardComboBox()
        
        
        layout.addWidget(self.award_label)
        layout.addWidget(self.award_combo)

        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(lambda _: self.confirmAddAward(self.constituentid, self.award_combo.selectedCommitteeCode()))
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def confirmAddAward(self, constituentid, awardid):
        selected_award = self.award_combo.currentText()
        if selected_award:
            cc = DatabaseCRUDL()
            cc.createConstituentAward(constituent_id=constituentid, award_id=awardid)
            self.parent().repopulate()
            self.accept()
        else:
            QMessageBox.warning(self, "Input Error", "Please select an award.")
            
class ConstituentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Constituent Window")
        self.setGeometry(100, 100, 800, 600)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(["Member Name", "Contact Information", "Date Joined", "Committee", "View\nEvents", "View\nAwards", "Edit", "Delete"])
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStyleSheet("""font: 14pt "Gotham";""")
        self.tableWidget.verticalHeader().setDefaultSectionSize(70)
        for i in range(1, 7):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        
        self.setLayout(layout)
        self.repopulate()

    def repopulate(self, thingtoquery=None):
        self.tableWidget.clearContents()
        cc = DatabaseCRUDL()
        constis = cc.listConstituentForTable(thingtoquery)
        self.tableWidget.setRowCount(len(constis))
        for i, (memberid, name, contactinfo, datejoined, comm) in enumerate(constis):
            item_name = QTableWidgetItem(name)
            item_ci = QTableWidgetItem(contactinfo)
            item_dj = QTableWidgetItem(str(datejoined))
            item_cm = QTableWidgetItem(comm)    
            ve_widget = ButtonForEventsConstituents(memberid)
            va_widget = ButtonForAwardsConstituents(memberid, self)
            edit_button = ButtonForEditConstituents(memberid, self)
            delete_button = ButtonForDeleteConstituents(memberid, self)
    
            self.tableWidget.setItem(i, 0, item_name)
            self.tableWidget.setItem(i, 1, item_ci)
            self.tableWidget.setItem(i, 2, item_dj)
            self.tableWidget.setItem(i, 3, item_cm)
            self.tableWidget.setCellWidget(i, 4, ve_widget)
            self.tableWidget.setCellWidget(i, 5, va_widget)
            self.tableWidget.setCellWidget(i, 6, edit_button)
            self.tableWidget.setCellWidget(i, 7, delete_button)

    def openCreateConstituentDialog(self):
        create_dialog = CreateConstituentDialog(self)
        if create_dialog.exec_() == QDialog.Accepted:
            self.repopulate()

class CommitteeComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.addItem('None')  # Add a default option
        self.committees_mapping = {}  # Dictionary to store the mapping between name and code
        cc = DatabaseCRUDL()
        self.committees = cc.executeQueryWithReturn("SELECT comm_code, comm_name FROM committee ORDER BY comm_name")
        for comm_code, comm_name in self.committees:
            self.committees_mapping[comm_name] = comm_code  # Store the mapping
            self.addItem(comm_name)  # Add only the name to the combo box

    def selectedCommitteeCode(self):
        committee_name = self.currentText()  # Get the selected committee name
        return self.committees_mapping.get(committee_name)  # Get the associated code

class AwardComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.committees_mapping = {}  
        cc = DatabaseCRUDL()
        self.awards = cc.executeQueryWithReturn("SELECT award_id, award_name FROM award ORDER BY award_name")
        for award_id, award_name in self.awards:
            self.committees_mapping[award_name] = award_id 
            self.addItem(award_name)  
            
    def selectedCommitteeCode(self):
        award_name = self.currentText()  
        return self.committees_mapping.get(award_name) 
    
class CreateConstituentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Create Constituent")
        self.setGeometry(100, 100, 400, 300)
        
        # Layout for the dialog
        layout = QVBoxLayout()
        
        # Labels and input fields
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        self.contact_info_label = QLabel("Contact Info:")
        self.contact_info_input = QLineEdit()

        self.date_joined_label = QLabel("Date Joined:")
        self.date_joined_input = QLineEdit()

        self.committee_label = QLabel("Committee:")
        self.committee_input = CommitteeComboBox()  # Use the custom combo box
        layout.addWidget(self.committee_label)
        layout.addWidget(self.committee_input)

        # Add widgets to the layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(self.contact_info_label)
        layout.addWidget(self.contact_info_input)

        layout.addWidget(self.date_joined_label)
        layout.addWidget(self.date_joined_input)
        
        # Confirm and cancel buttons
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.saveConstituent)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        # Add buttons to the layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # Set the layout for the dialog
        self.setLayout(layout)
        
    def saveConstituent(self):
        name = self.name_input.text()
        contact_info = self.contact_info_input.text()
        date_joined = self.date_joined_input.text()
        comm_code = self.committee_input.selectedCommitteeCode()  # Get the selected committee code
        
        if not name or not contact_info or not date_joined:
            QMessageBox.warning(self, "Input Error", "Fields must be filled")
            return
        cc = DatabaseCRUDL()
        cc.createConstituent(name, contact_info, date_joined, comm_code)
        
        QMessageBox.information(self, "Success", "Constituent created successfully")
        self.parent().repopulate()
        self.accept()


class ConstituentEventWindow(QDialog):
    def __init__(self, constituent_id, parent=None):
        super().__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.constituent_id = constituent_id
        cc = DatabaseCRUDL()
        self.constituent_name = cc.readConstituent(constituent_id)[0][1]
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"{self.constituent_name}-Event Window")
        self.setGeometry(100, 100, 800, 600)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Events", "Delete"])
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStyleSheet("""font: 14pt "Gotham";""")
        self.tableWidget.verticalHeader().setDefaultSectionSize(70)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        search_bar = QWidget()
        loadUi('ui/search_bar.ui', search_bar)
        search_bar_line_edit = QLineEdit()
        search_bar_line_edit = search_bar.findChild(QLineEdit, 'lineEdit')

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        # Add button for adding event
        self.add_event_button = QPushButton("Add Event")
        self.add_event_button.clicked.connect(self.openAddEventDialog)
        layout.addWidget(self.add_event_button)

        self.setLayout(layout)

        self.repopulate(self.constituent_id)

        search_bar_line_edit.textChanged.connect(lambda _: self.repopulate(self.constituent_id, search_bar_line_edit.text()))

    def repopulate(self, constid=None, thingtoquery=None):
        self.tableWidget.clearContents()
        cc = DatabaseCRUDL()
        const_events = cc.listConstituentEventForTable(constituentid=self.constituent_id, thingtoquery=thingtoquery)
        self.tableWidget.setRowCount(len(const_events))
        for i, (event_id, const_id, event_desc, const_name) in enumerate(const_events):
            item_event = QTableWidgetItem(event_desc)
            delete_button = ButtonForDeleteConstituentEvent(const_id, event_id, const_name, event_desc)
            self.tableWidget.setItem(i, 0, item_event)
            self.tableWidget.setCellWidget(i, 1, delete_button)

    def openAddEventDialog(self):
        add_event_dialog = AddEventDialog(self.constituent_id, self)
        if add_event_dialog.exec_() == QDialog.Accepted:
            self.repopulate()


class AddEventDialog(QDialog):
    def __init__(self, constituent_id, parent=None):
        super().__init__(parent)
        self.initUI()
        self.constituent_id = constituent_id

    def initUI(self):
        self.setWindowTitle("Add Event")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.event_label = QLabel("Select Event:")
        self.event_combo = EventComboBox()

        layout.addWidget(self.event_label)
        layout.addWidget(self.event_combo)

        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(lambda _: self.confirmAddEvent(self.constituent_id, self.event_combo.selectedEventId()))
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def confirmAddEvent(self, constituent_id, event_id):
        selected_event = self.event_combo.currentText()
        if selected_event:
            cc = DatabaseCRUDL()
            cc.createConstituentEvent(constituent_id=constituent_id, event_id=event_id)
            self.parent().repopulate()
            self.accept()
        else:
            QMessageBox.warning(self, "Input Error", "Please select an event.")

class EventComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.events_mapping = {}
        cc = DatabaseCRUDL()
        self.events = cc.executeQueryWithReturn("SELECT event_id, description FROM event ORDER BY description")
        for event_id, event_description in self.events:
            self.events_mapping[event_description] = event_id
            self.addItem(event_description)

    def selectedEventId(self):
        event_description = self.currentText()
        return self.events_mapping.get(event_description)
