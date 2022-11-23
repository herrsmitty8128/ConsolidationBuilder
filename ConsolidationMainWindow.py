
import MainWindow
from PyQt5 import QtWidgets, QtCore
from Document import Document
from BaseTableModel import BaseTableModel


class ConsolidationMainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):

    def __init__(self, application: QtWidgets.QApplication):

        super().__init__()

        self.setupUi(self)
        self.application = application
        self.document_filename = None
        self.document = Document()

        self.actions = {
            'actionImportEntities': 'Entities',
            'actionImportCostCenters': 'Cost_Centers',
            'actionImportAccounts': 'Accounts',
            'actionImportTrialBalance': 'Trial_Balance',
            'actionImportAdjustments': 'Adjustments',
            'actionExportEntities': 'Entities',
            'actionExportCostCenters': 'Cost_Centers',
            'actionExportAccounts': 'Accounts',
            'actionExportTrialBalance': 'Trial_Balance',
            'actionExportAdjustments': 'Adjustments'
        }

        self.table_models = {
            'Entities': None,
            'Cost_Centers': None,
            'Accounts': None,
            'Trial_Balance': None,
            'Adjustments': None
        }

        for table_name in self.table_models:
            table = self.findChild(QtWidgets.QTableView, table_name)
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            model = BaseTableModel(table, self.document, table_name)
            self.table_models[table_name] = model
            table.setModel(model)

        self.set_non_table_data()

    def set_non_table_data(self) -> None:
        # set the entity name
        name = self.findChild(QtWidgets.QLineEdit, 'entityName')
        name.blockSignals(True)
        name.setText(self.document.get_entity_name())
        name.blockSignals(False)
        # set the beginning date
        date = self.findChild(QtWidgets.QDateEdit, 'beginningBalanceDate')
        date.blockSignals(True)
        date.setDate(QtCore.QDate.fromString(self.document.get_beginning_date(), 'M/d/yyyy'))
        date.blockSignals(False)
        # set the ending date
        date = self.findChild(QtWidgets.QDateEdit, 'endingBalanceDate')
        date.blockSignals(True)
        date.setDate(QtCore.QDate.fromString(self.document.get_ending_date(), 'M/d/yyyy'))
        date.blockSignals(False)

    ####################################################################################
    # FILE MENU
    ####################################################################################

    @QtCore.pyqtSlot()
    def new_menu_item(self):
        try:
            self.close_menu_item()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def open_menu_item(self):
        try:
            if self.document.changed():
                answer = QtWidgets.QMessageBox.question(self, 'Save File', 'Save current file before proceeding?')
                if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                    self.save_menu_item()
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='JSON Files (*.json)')
            if file:
                self.document_filename = file
                self.document.load(self.document_filename)
                self.set_non_table_data()
                for model in self.table_models.values():
                    model.layoutChanged.emit()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def save_menu_item(self):
        try:
            if not self.document_filename:
                file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='JSON Files (*.json)')
                if file:
                    if not file.casefold().endswith('.json'.casefold()):
                        file += '.json'
                    self.document_filename = file
                else:
                    return
            self.document.dump(self.document_filename)
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def save_as_menu_item(self):
        try:
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='JSON Files (*.json)')
            if file:
                if not file.casefold().endswith('.json'.casefold()):
                    file += '.json'
                self.document_filename = file
                self.save_menu_item()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def close_menu_item(self):
        try:
            if self.document.changed():
                answer = QtWidgets.QMessageBox.question(self, 'Save File', 'Save current file before proceeding?')
                if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                    self.save_menu_item()
            self.document.reset()
            self.set_non_table_data()
            for model in self.table_models.values():
                model.layoutChanged.emit()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def quit_menu_item(self):
        try:
            self.application.quit()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    ####################################################################################
    # DATA MENU
    ####################################################################################

    @QtCore.pyqtSlot()
    def import_menu_item(self):
        try:
            table_name = self.actions.get(self.sender().objectName(), None)
            if table_name is None:
                raise ValueError('Unrecognize action name.')
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='CSV Files (*.csv)')
            if file:
                response = QtWidgets.QMessageBox.question(self, 'Replace rows?', 'Would you like to replace all rows of data?')
                response = False if response == QtWidgets.QMessageBox.StandardButton.No else True
                self.document.import_table(table_name, file, response)
                self.table_models[table_name].layoutChanged.emit()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def export_menu_item(self):
        try:
            table_name = self.actions.get(self.sender().objectName(), None)
            if table_name is None:
                raise ValueError('Unrecognize action name.')
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='CSV Files (*.csv)')
            if file:
                if not file.casefold().endswith('.csv'.casefold()):
                    file += '.csv'
                self.document.export_table(table_name, file)
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    ####################################################################################
    # Consolidation Menu
    ####################################################################################

    @QtCore.pyqtSlot()
    def build_menu_item(self):
        try:
            self.document.build_consolidation()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def rollforward_menu_item(self):
        try:
            self.document.close_year()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def audit_menu_item(self):
        try:
            '''
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
            '''
            self.document.audit_data()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    ####################################################################################
    # Other Slots
    ####################################################################################

    @QtCore.pyqtSlot(str)
    def set_entity_name(self, new_name: str):
        try:
            self.document.set_entity_name(new_name)
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot(QtCore.QDate)
    def set_beginning_date(self, new_date: QtCore.QDate):
        try:
            self.document.set_beginning_date(new_date.toString('M/d/yyyy'))
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot(QtCore.QDate)
    def set_ending_date(self, new_date: QtCore.QDate):
        try:
            self.document.set_ending_date(new_date.toString('M/d/yyyy'))
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
