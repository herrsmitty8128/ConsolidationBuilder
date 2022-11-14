
import MainWindow
import json
import csv
from BaseTableModel import BaseTableModel
from PyQt5 import QtWidgets, QtCore, QtGui


class ConsolidationMainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):

    def __init__(self, application: QtWidgets.QApplication):
        
        super().__init__()
        self.setupUi(self)
        self.application = application

        self.create_new_document()
        #self.connect_new_document()
        
        table = self.findChild(QtWidgets.QTableView, 'entityTableView')
        model = BaseTableModel(self.document['Entities'], ['','','','',], table)
        table.setModel(model)

        table = self.findChild(QtWidgets.QTableView, 'costCenterTableView')
        model = BaseTableModel(self.document['Cost Centers'], ['','','','',], table)
        table.setModel(model)

        table = self.findChild(QtWidgets.QTableView, 'accountsTableView')
        model = BaseTableModel(self.document['Accounts'], ['','','','',], table)
        table.setModel(model)

        table = self.findChild(QtWidgets.QTableView, 'trialBalanceTableView')
        model = BaseTableModel(self.document['Trial Balance']['Entries'], ['','','','',], table)
        table.setModel(model)

        table = self.findChild(QtWidgets.QTableView, 'adjustmentsTableView')
        model = BaseTableModel(self.document['Adjustments'], ['','','','',], table)
        table.setModel(model)

        errors = self.findChild(QtWidgets.QTextEdit, 'errorTextEdit')
        errors.setTextColor(QtGui.QColor('black'))
        errors.append('Welcome to Consolidation Station!\nVersion 1.0\n')

    ####################################################################################
    # FILE MENU
    ####################################################################################

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
            self.document_filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='JSON Files (*.json)')
            f = open(self.document_filename, 'r')
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
                self.document_filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='JSON Files (*.json)')
                if not self.document_filename.casefold().endswith('.json'.casefold()):
                    self.document_filename += '.json'
            f = open(self.document_filename, 'w')
            json.dump(self.document, f, indent=3)
            f.close()
            self.document_should_save = False
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    # DONE

    @QtCore.pyqtSlot()
    def save_as_document(self):
        try:
            self.document_filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='JSON Files (*.json)')
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

    ####################################################################################
    # CUSTOM METHODS AND SLOTS
    ####################################################################################

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

    def connect_new_document(self):
        try:
            # connect the data to the table veiw data models
            self.findChild(QtWidgets.QTableView, 'entityTableView').getModel().replaceRows(self.document['Entities'])
            self.findChild(QtWidgets.QTableView, 'costCenterTableView').getModel().replaceRows(self.document['Cost Centers'])
            self.findChild(QtWidgets.QTableView, 'accountsTableView').getModel().replaceRows(self.document['Accounts'])
            self.findChild(QtWidgets.QTableView, 'trialBalanceTableView').getModel().replaceRows(self.document['Trial Balance']['Entries'])
            self.findChild(QtWidgets.QTableView, 'adjustmentsTableView').getModel().replaceRows(self.document['Adjustments'])
            pass
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

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

    ####################################################################################
    # DATA MENU
    ####################################################################################

    @QtCore.pyqtSlot()
    def import_table(self):
        try:
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='JSON Files (*.json)')
            if file:
                replace = QtWidgets.QMessageBox.question(self, 'Replace rows?', 'Would you like to replace all rows of data?')
                replace = True if replace == QtWidgets.QMessageBox.StandardButton.Yes else False
                sender = self.sender().objectName()
                if sender == 'actionImportEntities':
                    self.findChild(QtWidgets.QTableView, 'entityTableView').getModel().importCSV(file,replace)
                elif sender == 'actionImportCostCenters':
                    self.findChild(QtWidgets.QTableView, 'costCenterTableView').getModel().importCSV(file,replace)
                elif sender == 'actionImportAccounts':
                    self.findChild(QtWidgets.QTableView, 'accountsTableView').getModel().importCSV(file,replace)
                elif sender == 'actionImportTrialBalance':
                    self.findChild(QtWidgets.QTableView, 'trialBalanceTableView').getModel().importCSV(file,replace)
                elif sender == 'actionImportAdjustments':
                    self.findChild(QtWidgets.QTableView, 'adjustmentsTableView').getModel().importCSV(file,replace)
                else:
                    raise ValueError('Unrecognized import table')
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def export_table(self):
        try:
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='JSON Files (*.json)')
            if file:
                sender = self.sender().objectName()
                if sender == 'actionImportEntities':
                    self.findChild(QtWidgets.QTableView, 'entityTableView').getModel().exportCSV(file)
                elif sender == 'actionImportCostCenters':
                    self.findChild(QtWidgets.QTableView, 'costCenterTableView').getModel().exportCSV(file)
                elif sender == 'actionImportAccounts':
                    self.findChild(QtWidgets.QTableView, 'accountsTableView').getModel().exportCSV(file)
                elif sender == 'actionImportTrialBalance':
                    self.findChild(QtWidgets.QTableView, 'trialBalanceTableView').getModel().exportCSV(file)
                elif sender == 'actionImportAdjustments':
                    self.findChild(QtWidgets.QTableView, 'adjustmentsTableView').getModel().exportCSV(file)
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
