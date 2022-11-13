
import MainWindow
import json
import csv
from PyQt5 import QtWidgets, QtCore, Qt, QtGui


class ConsolidationMainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):


    def __init__(self, application: QtWidgets.QApplication):
        super().__init__()
        self.setupUi(self)
        self.application = application
        self.create_new_document()
        self.connect_new_document()
        errors = self.findChild(QtWidgets.QTextEdit, 'errorTextEdit')
        errors.setTextColor(QtGui.QColor('black'))
        errors.append('Welcome to Consolidation Station!\nVersion 1.0\n')
    

    @QtCore.pyqtSlot()
    def document_changed(self):
        self.document_should_save = True
    

    @QtCore.pyqtSlot(str)
    def set_entity_name(self, new_name: str):
        try:
            self.document['Entity'] = new_name
            self.document_should_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    @QtCore.pyqtSlot(QtCore.QDate)
    def set_beginning_date(self, new_date: QtCore.QDate):
        try:
            self.document['Trial Balance']['Beginning Date'] = new_date.toString('M/d/yyyy')
            self.document_should_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    @QtCore.pyqtSlot(QtCore.QDate)
    def set_ending_date(self, new_date: QtCore.QDate):
        try:
            self.document['Trial Balance']['Ending Date'] = new_date.toString('M/d/yyyy')
            self.document_should_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))


    #@QtCore.pyqtSlot()
    def connect_new_document(self):
        try:
            # connect the data to the table veiw data models
            # refresh the table models
            # add the data models to the table views here...
            # tableView = self.findChild(QtWidgets.QTableView, 'invoiceLineItemsTableView')
            # tableView.setModel(InvoiceLineItem.TableModel(parent=tableView))
            pass
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    #@QtCore.pyqtSlot()
    def create_new_document(self):
        try:
            self.document = {
                'Entity': '',
                'Accounts': [],
                'Cost Centers': [],
                'Entities': [],
                'Trial Balance': {
                    'Consolidated PYE': None,
                    'Unconsolidated': None,
                    'Entries': []
                },
                'Adjustments': []
            }
            self.document_should_save = False
            self.document_filename = None
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    @QtCore.pyqtSlot()
    def new_document(self):
        try:
            self.close_document()
            self.create_new_document()
            self.connect_new_document()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    # DONE
    @QtCore.pyqtSlot()
    def open_document(self):
        try:
            self.close_document()
            self.document_filename,_ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='JSON Files (*.json)')
            f = open(self.document_filename,'r')
            self.document = json.load(f)
            f.close()
            self.document_should_save = False
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    # DONE
    @QtCore.pyqtSlot()
    def save_document(self):
        try:
            if not self.document_filename:
                self.document_filename,_ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='JSON Files (*.json)')
                if not self.document_filename.casefold().endswith('.json'.casefold()):
                    self.document_filename += '.json'
            f = open(self.document_filename,'w')
            json.dump(self.document, f, indent=3)
            f.close()
            self.document_should_save = False
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    # DONE
    @QtCore.pyqtSlot()
    def save_as_document(self):
        try:
            self.document_filename,_ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='JSON Files (*.json)')
            if not self.document_filename.casefold().endswith('.json'.casefold()):
                self.document_filename += '.json'
            self.save_document()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    # DONE
    @QtCore.pyqtSlot()
    def close_document(self):
        try:
            if self.document_should_save:
                answer = QtWidgets.QMessageBox.question(self, 'Save File', 'Save current file before closing?')
                if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                    if self.document_filename:
                        self.save_document()
                    else:
                        self.save_as_document()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    
    # DONE
    @QtCore.pyqtSlot()
    def quit_application(self):
        try:
            self.close_document()
            self.application.quit()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    @QtCore.pyqtSlot()
    def import_table(self):
        try:
            file,_ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='JSON Files (*.json)')
            # Append or replace???
            sender = self.sender().objectName()
            if sender == 'actionImportEntities':
                tablemodel = self.findChild(QtWidgets.QTableView, 'entityTableView')
            elif sender == 'actionImportCostCenters':
                pass
            elif sender == 'actionImportAccounts':
                pass
            elif sender == 'actionImportTrialBalance':
                pass
            elif sender == 'actionImportAdjustments':
                pass
            else:
                raise ValueError('Unrecognized import table')
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    @QtCore.pyqtSlot()
    def export_table(self):
        def write_to_csv(file:str, data:list) -> None:
            if len(data) > 0:
                with open(file, 'w') as f:
                    writer = csv.DictWriter(fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
        try:
            file,_ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='JSON Files (*.json)')
            sender = self.sender().objectName()
            if sender == 'actionExportEntities':
                write_to_csv(file,self.document['Entities'])
            elif sender == 'actionExportCostCenters':
                write_to_csv(file,self.document['Cost Centers'])
            elif sender == 'actionExportAccounts':
                write_to_csv(file,self.document['Accounts'])
            elif sender == 'actionExportTrialBalance':
                write_to_csv(file,self.document['Trial Balance']['Entries'])
            elif sender == 'actionExportAdjustments':
                write_to_csv(file,self.document['Adjustments'])
            else:
                raise ValueError('Unrecognized export table')
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    @QtCore.pyqtSlot()
    def build_consolidation(self):
        try:
            pass
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))