import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from db_crudl import CRUDL, Constituent, Award, Event, Committee
from mysql.connector import Error

class CreateConstituentDialog(QDialog):
    closed = pyqtSignal()  # Signal to emit when the dialog is closed
    
    def __init__(self, parent=None, name=None, comm_code=None, constituent_id=None):
        super(CreateConstituentDialog, self).__init__(parent)
        self.setWindowTitle("Create Constituent")
        self.constituent_id = constituent_id  # Store the constituent_id if provided
        
        layout = QVBoxLayout()
        
        self.name_edit = QLineEdit()
        self.name_edit.setText(name)
        
        self.start_date_edit = QLineEdit()  # Assuming start_date is a simple string input
        self.contact_info_edit = QLineEdit()  # Assuming contact_info is a simple string input
        
        self.comm_code_combo = QComboBox()
        self.comm_code_combo.addItem(None, None)  # Add None as an option
        cc = CRUDL()
        comms = cc.list('committee')
        comms = {row[1] for row in comms}
        self.comm_code_combo.addItems(comms)  # Example range, adjust as needed
        if comm_code is None:
            self.comm_code_combo.setCurrentIndex(-1)
        
        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Start Date"))
        layout.addWidget(self.start_date_edit)
        layout.addWidget(QLabel("Contact Info"))
        layout.addWidget(self.contact_info_edit)
        layout.addWidget(QLabel("Committee Code"))
        layout.addWidget(self.comm_code_combo)
        
        buttons_layout = QHBoxLayout()
        create_button = QPushButton("Create")
        create_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(create_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
    
    def get_values(self):
        name = self.name_edit.text()
        start_date = self.start_date_edit.text()
        contact_info = self.contact_info_edit.text()
        comm_code = self.comm_code_combo.currentText()
        return {
            "name": name,
            "start_date": start_date,
            "contact_info": contact_info,
            "comm_code": comm_code
        }
    
    def accept(self):
        values = self.get_values()
        name = values["name"]
        start_date = values["start_date"]
        contact_info = values["contact_info"]
        comm_code = values["comm_code"]
        
        if not name or not start_date or not contact_info or not comm_code:
            QMessageBox.warning(self, "Invalid Input", "Please fill in all fields.")
            return
        
        crudl = CRUDL()
        constituent = Constituent(start_date=start_date, contact_info=contact_info, constituent_name=name, comm_code=comm_code)
        crudl.create("Constituent", constituent)
        
        QMessageBox.information(self, "Success", "Constituent created successfully.")
        self.close()
    
    def closeEvent(self, event):
        self.closed.emit()  # Emit the signal
        super().closeEvent(event)  # Call the base class implementation

class UpdateAwardDialog(QDialog):
    closed = pyqtSignal() 
    def __init__(self, award_id, parent=None, dateawarded=None, awardname=None):
        super(UpdateAwardDialog, self).__init__(parent)
        self.setWindowTitle(f"Update Award {award_id}")
        layout = QVBoxLayout()
        
        self.award_name_edit = QLineEdit()
        self.event_combo = QComboBox()
        self.load_events_into_combo()  # You'll need to implement this method to load events
        
        layout.addWidget(QLabel("Award Name"))
        layout.addWidget(self.award_name_edit)
        layout.addWidget(QLabel("Event"))
        layout.addWidget(self.event_combo)
        
        buttons_layout = QHBoxLayout()
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(update_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def load_events_into_combo(self):
        # Placeholder for loading events into the combo box
        pass

    def get_values(self):
        award_name = self.award_name_edit.text()
        event_id = self.event_combo.currentData()
        return {"award_name": award_name, "event_id": event_id}

    def accept(self):
        values = self.get_values()
        award_name = values["award_name"]
        event_id = values["event_id"]

        if not award_name or not event_id:
            QMessageBox.warning(self, "Invalid Input", "Please enter an award name and event.")
            return

        crudl = CRUDL()
        award = Award(date_awarded="", award_name=award_name)
        crudl.update("Award", award, "award_id", event_id)

        QMessageBox.information(self, "Success", "Award updated successfully.")
        self.close()
        
    def closeEvent(self, event):
        self.closed.emit()  # Emit the signal
        super().closeEvent(event)

class CreateEventDialog(QDialog):
    closed = pyqtSignal() 
    def __init__(self, parent=None):
        super(CreateEventDialog, self).__init__(parent)
        self.setWindowTitle("Create Event")
        layout = QVBoxLayout()
        
        self.date_start_edit = QLineEdit()
        self.date_end_edit = QLineEdit()
        self.location_edit = QLineEdit()
        self.description_edit = QLineEdit()
        
        layout.addWidget(QLabel("Date Start"))
        layout.addWidget(self.date_start_edit)
        layout.addWidget(QLabel("Date End"))
        layout.addWidget(self.date_end_edit)
        layout.addWidget(QLabel("Location"))
        layout.addWidget(self.location_edit)
        layout.addWidget(QLabel("Description"))
        layout.addWidget(self.description_edit)
        
        buttons_layout = QHBoxLayout()
        create_button = QPushButton("Create")
        create_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(create_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def get_values(self):
        date_start = self.date_start_edit.text()
        date_end = self.date_end_edit.text()
        location = self.location_edit.text()
        description = self.description_edit.text()
        return {"date_start": date_start, "date_end": date_end, "location": location, "description": description}

    def accept(self):
        values = self.get_values()
        date_start = values["date_start"]
        date_end = values["date_end"]
        location = values["location"]
        description = values["description"]

        if not date_start or not date_end or not location or not description:
            QMessageBox.warning(self, "Invalid Input", "Please fill in all fields.")
            return

        crudl = CRUDL()
        event = Event(date_start=date_start, date_end=date_end, location=location, description=description)
        crudl.create("Event", event)

        QMessageBox.information(self, "Success", "Event created successfully.")
        self.close()
        
    def closeEvent(self, event):
        self.closed.emit()  # Emit the signal
        super().closeEvent(event)

class CreateCommitteeDialog(QDialog):
    closed = pyqtSignal() 
    def __init__(self, parent=None, name_id = None, name_edit=None):
        super(CreateCommitteeDialog, self).__init__(parent)
        self.setWindowTitle("Create Committee")
        layout = QVBoxLayout()
        self.isEditMode = True
        self.nameId = name_id
        self.nameEdit = name_edit
        
        if name_edit is None:
            self.isEditMode = False
            
        self.comm_name_edit = QLineEdit()
        self.comm_name_edit.setText(name_edit)
        
        layout.addWidget(QLabel("Committee Name"))
        layout.addWidget(self.comm_name_edit)
        
        buttons_layout = QHBoxLayout()
        
        create_button = QPushButton("Update") if self.isEditMode else QPushButton("Create") 
        create_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(create_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def accept(self):
        cc = CRUDL()
        if not self.comm_name_edit.text():
            QMessageBox.warning(self, "Invalid Input", "Please fill in all fields.")
            return
        query = f"""UPDATE Committee SET Comm_name="{self.comm_name_edit.text()}" WHERE comm_code={self.nameId};"""
        cc.executeQuery(query)
        QMessageBox.information(self, "Success", "Committee edited successfully.")
        self.close()
    
    def closeEvent(self, event):
        self.closed.emit()  # Emit the signal
        super().closeEvent(event)