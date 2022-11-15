
import MainWindow
import json
import csv
from BaseTableModel import BaseTableModel
from PyQt5 import QtWidgets, QtCore, QtGui
from collections import Counter
from TrialBalanceTableModel import TrialBalanceTableModel


class ConsolidationMainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):

    accountHeaders = ['Number', 'Name', 'Level 1', 'Level 2', 'Level 3', 'Level 4']
    entityHeaders = ['Number', 'Name', 'Group']
    costCenterHeaders = ['Number', 'Name']
    trialBalanceHeaders = ['Entity', 'Cost Center', 'Account', 'Beginning Balance', 'Debits', 'Credits', 'Ending Balance']
    adjustmentsHeaders = ['Entity', 'Cost Center', 'Account', 'Beginning Balance', 'Debits', 'Credits', 'Ending Balance', 'Description']

    def __init__(self, application: QtWidgets.QApplication):

        super().__init__()
        self.setupUi(self)
        self.application = application

        table = self.findChild(QtWidgets.QTableView, 'entityTableView')
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = BaseTableModel(ConsolidationMainWindow.entityHeaders, table)
        table.setModel(model)

        table = self.findChild(QtWidgets.QTableView, 'costCenterTableView')
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = BaseTableModel(ConsolidationMainWindow.costCenterHeaders, table)
        table.setModel(model)

        table = self.findChild(QtWidgets.QTableView, 'accountsTableView')
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = BaseTableModel(ConsolidationMainWindow.accountHeaders, table)
        table.setModel(model)

        table = self.findChild(QtWidgets.QTableView, 'trialBalanceTableView')
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = TrialBalanceTableModel(ConsolidationMainWindow.trialBalanceHeaders, table)
        table.setModel(model)

        table = self.findChild(QtWidgets.QTableView, 'adjustmentsTableView')
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = BaseTableModel(ConsolidationMainWindow.adjustmentsHeaders, table)
        table.setModel(model)

        self.create_new_document()

        self.errors = self.findChild(QtWidgets.QTextEdit, 'errorTextEdit')
        self.errors.setTextColor(QtGui.QColor('black'))
        self.errors.append('Welcome to Consolidation Station!\nVersion 1.0')

    ####################################################################################
    # FILE MENU
    ####################################################################################

    @QtCore.pyqtSlot()
    def new_document(self):
        try:
            self.close_document()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def open_document(self):
        try:
            if self.document_should_save:
                answer = QtWidgets.QMessageBox.question(self, 'Save File', 'Save current file before proceeding?')
                if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                    self.save_document()
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='JSON Files (*.json)')
            if file:
                self.document_filename = file
                f = open(self.document_filename, 'r')
                self.document = json.load(f)
                f.close()
                self.document_should_save = False
                self.connect_document()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def save_document(self):
        try:
            if not self.document_filename:
                file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='JSON Files (*.json)')
                if file:
                    if not file.casefold().endswith('.json'.casefold()):
                        file += '.json'
                    self.document_filename = file
                else:
                    return
            f = open(self.document_filename, 'w')
            json.dump(self.document, f)  # , indent=3)
            f.close()
            self.document_should_save = False
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def save_as_document(self):
        try:
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='JSON Files (*.json)')
            if file:
                if not file.casefold().endswith('.json'.casefold()):
                    file += '.json'
                self.document_filename = file
                self.save_document()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def close_document(self):
        try:
            if self.document_should_save:
                answer = QtWidgets.QMessageBox.question(self, 'Save File', 'Save current file before proceeding?')
                if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                    self.save_document()
            self.create_new_document()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

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
            self.document['Entity Name'] = new_name
            self.document_should_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot(QtCore.QDate)
    def set_beginning_date(self, new_date: QtCore.QDate):
        try:
            self.document['Beginning Balance Date'] = new_date.toString('M/d/yyyy')
            self.document_should_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot(QtCore.QDate)
    def set_ending_date(self, new_date: QtCore.QDate):
        try:
            self.document['Ending Balance Date'] = new_date.toString('M/d/yyyy')
            self.document_should_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    # connect the data to the table view data models

    def connect_document(self):
        try:
            date = self.findChild(QtWidgets.QDateEdit, 'beginningBalanceDate')
            date.blockSignals(True)
            date.setDate(QtCore.QDate.fromString(self.document['Beginning Balance Date'], 'M/d/yyyy'))
            date.blockSignals(False)
            date = self.findChild(QtWidgets.QDateEdit, 'endingBalanceDate')
            date.blockSignals(True)
            date.setDate(QtCore.QDate.fromString(self.document['Ending Balance Date'], 'M/d/yyyy'))
            date.blockSignals(False)
            self.findChild(QtWidgets.QLineEdit, 'entityName').setText(self.document['Entity Name'])
            self.findChild(QtWidgets.QTableView, 'entityTableView').model().replaceRows(self.document['Entities'])
            self.findChild(QtWidgets.QTableView, 'costCenterTableView').model().replaceRows(self.document['Cost Centers'])
            self.findChild(QtWidgets.QTableView, 'accountsTableView').model().replaceRows(self.document['Accounts'])
            self.findChild(QtWidgets.QTableView, 'trialBalanceTableView').model().replaceRows(self.document['Trial Balance'])
            self.findChild(QtWidgets.QTableView, 'adjustmentsTableView').model().replaceRows(self.document['Adjustments'])
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    def create_new_document(self):
        try:
            self.document = {
                'Entity Name': '',
                'Beginning Balance Date': '12/31/9999',
                'Ending Balance Date': '12/31/9999',
                'Accounts': [],
                'Cost Centers': [],
                'Entities': [],
                'Trial Balance': [],
                'Adjustments': []
            }
            self.document_should_save = False
            self.document_filename = None
            self.connect_document()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    ####################################################################################
    # DATA MENU
    ####################################################################################

    @QtCore.pyqtSlot()
    def import_table(self):
        try:
            def import_model_data(file, name):
                model = self.findChild(QtWidgets.QTableView, name).model()
                replace = True
                if model.rowCount() > 0:
                    response = QtWidgets.QMessageBox.question(self, 'Replace rows?', 'Would you like to replace all rows of data?')
                    if response == QtWidgets.QMessageBox.StandardButton.No:
                        replace = False
                model.importCSV(file, replace)
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='CSV Files (*.csv)')
            if file:
                sender = self.sender().objectName()
                if sender == 'actionImportEntities':
                    import_model_data(file, 'entityTableView')
                elif sender == 'actionImportCostCenters':
                    import_model_data(file, 'costCenterTableView')
                elif sender == 'actionImportAccounts':
                    import_model_data(file, 'accountsTableView')
                elif sender == 'actionImportTrialBalance':
                    import_model_data(file, 'trialBalanceTableView')
                elif sender == 'actionImportAdjustments':
                    import_model_data(file, 'adjustmentsTableView')
                else:
                    raise ValueError('Unrecognized import table')
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def export_table(self):
        try:
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='CSV Files (*.csv)')
            if file:
                if not file.casefold().endswith('.csv'.casefold()):
                    file += '.csv'
                sender = self.sender().objectName()
                if sender == 'actionExportEntities':
                    self.findChild(QtWidgets.QTableView, 'entityTableView').model().exportCSV(file)
                elif sender == 'actionExportCostCenters':
                    self.findChild(QtWidgets.QTableView, 'costCenterTableView').model().exportCSV(file)
                elif sender == 'actionExportAccounts':
                    self.findChild(QtWidgets.QTableView, 'accountsTableView').model().exportCSV(file)
                elif sender == 'actionExportTrialBalance':
                    self.findChild(QtWidgets.QTableView, 'trialBalanceTableView').model().exportCSV(file)
                elif sender == 'actionExportAdjustments':
                    self.findChild(QtWidgets.QTableView, 'adjustmentsTableView').model().exportCSV(file)
                else:
                    raise ValueError('Unrecognized export table')
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    ####################################################################################
    # CONSOLIDATION MENU
    ####################################################################################

    @QtCore.pyqtSlot()
    def build_consolidation(self):
        try:
            pass
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def close_year(self):
        pass

    @QtCore.pyqtSlot()
    def audit(self):

        def audit_list(errors: list, items: list, item_name: str):
            counter = Counter()
            for item in items:
                num = item['Number']
                if len(num) < 1:
                    errors.append(f'{item_name} without a number was detected.')
                if len(item['Name']) < 1:
                    errors.append(f'{item_name} without a name was detected.')
                counter[num] += 1
            for num, cnt in counter.items():
                if cnt > 1:
                    errors.append(f'{item_name} number {num} appears more than once on the list. Each {item_name} must have a unique number.')

        def audit_balances(errors: list, items: list, item_name: str):
            for item in items:
                diff = round(item['Ending Balance'], 2) - round(item['Beginning Balance'] + item['Debits'] + item['Credits'], 2)
                if abs(diff) > 1.0:
                    errors.append(f'Balance does not roll-forward for {item["Entity"]}-{item["Cost Center"]}-{item["Account"]} on the {item_name}. The difference is {diff}.')
                else:
                    item['Credits'] += diff
                    diff = round(item['Ending Balance'], 2) - round(item['Beginning Balance'] + item['Debits'] + item['Credits'], 2)
                    if diff != 0.00:
                        errors.append(f'Balance does not roll-forward for {item["Entity"]}-{item["Cost Center"]}-{item["Account"]} on the {item_name}. The difference is {diff}.')

            ent_nums = set(x['Number'] for x in self.document['Entities'])
            bal_ent_nums = set(x['Entity'] for x in items)
            diff = bal_ent_nums.difference(ent_nums)
            if len(diff) > 0:
                errors.append(f'Entities on the trial balance, but not on the entity tab: {diff}.')

            cc_nums = set(x['Number'] for x in self.document['Cost Centers'])
            bal_cc_nums = set(x['Cost Center'] for x in items)
            diff = bal_cc_nums.difference(cc_nums)
            if len(diff) > 0:
                errors.append(f'Cost centers on the trial balance, but not on the cost center tab: {diff}.')

            acct_nums = set(x['Number'] for x in self.document['Accounts'])
            bal_acct_nums = set(x['Account'] for x in items)
            diff = bal_acct_nums.difference(acct_nums)
            if len(diff) > 0:
                errors.append(f'Accounts on the trial balance, but not on the accounts tab: {diff}.')

        try:
            errors = []

            self.errors.append('Starting the audit process...')

            if len(self.findChild(QtWidgets.QLineEdit, 'entityName').text()) < 1:
                errors.append('Entity name is missing.')

            start_date = QtCore.QDate.fromString(self.document['Beginning Balance Date'], 'M/d/yyyy')
            end_date = QtCore.QDate.fromString(self.document['Ending Balance Date'], 'M/d/yyyy')
            if start_date >= end_date:
                errors.append('Beginning balance date is greater than or equal to the ending balance date.')

            audit_list(errors, self.document['Entities'], 'Entity')
            audit_list(errors, self.document['Cost Centers'], 'Cost center')
            audit_list(errors, self.document['Accounts'], 'Account')
            audit_balances(errors, self.document['Trial Balance'], 'Trial balance')
            audit_balances(errors, self.document['Adjustments'], 'Adjustments')

            if len(errors) > 0:
                self.errors.setTextColor(QtGui.QColor('red'))
                for err in errors:
                    self.errors.append(err)
                self.errors.append(f'{len(errors)} were detected. You must resolve these errors before you can proceed with the consolidation process.')
                self.errors.setTextColor(QtGui.QColor('black'))
                raise ValueError(f'The audit process identified {len(errors)} errors. Please check the error log below.')
            else:
                self.errors.setTextColor(QtGui.QColor('green'))
                self.errors.append('Audit completed successfully. No errors were found.')
                self.errors.setTextColor(QtGui.QColor('black'))

        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
