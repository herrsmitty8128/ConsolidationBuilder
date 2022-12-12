
import MainWindow
import CsvTables
from PyQt5 import QtWidgets, QtCore, QtGui
from Document2 import Document
from TableModel import TableModel


class ConsolidationMainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):

    def __init__(self, application: QtWidgets.QApplication):

        super().__init__()

        self.setupUi(self)
        self.application = application
        self.filename = None
        self.document = Document()
        self.changed_since_last_save = False

        self.menu_actions = {
            'actionImportEntities': 'Entities',
            'actionImportCostCenters': 'Cost_Centers',
            'actionImportAccounts': 'Accounts',
            'actionImportTrialBalance': 'Trial_Balance',
            'actionImportTopSides': 'Top_Sides',
            'actionExportEntities': 'Entities',
            'actionExportCostCenters': 'Cost_Centers',
            'actionExportAccounts': 'Accounts',
            'actionExportTrialBalance': 'Trial_Balance',
            'actionExportTopSides': 'Top_Sides',
            'addEntityButton': 'Entities',
            'deleteEntityButton': 'Entities',
            'addCostCenterButton': 'Cost_Centers',
            'deleteCostCenterButton': 'Cost_Centers',
            'insertAccountButton': 'Accounts',
            'addAccountButton': 'Accounts',
            'addTopSideButton': 'Top_Sides',
            'deleteTopSideButton': 'Top_Sides'
        }

        self.set_table_model('Entities', [x for x in CsvTables.descriptors['Entities'].keys()], self.document.entities)
        self.set_table_model('Cost_Centers', [x for x in CsvTables.descriptors['Cost_Centers'].keys()], self.document.cost_centers)
        self.set_table_model('Accounts', [x for x in CsvTables.descriptors['Accounts'].keys()], self.document.accounts)
        self.set_table_model('Trial_Balance', [x for x in CsvTables.descriptors['Trial_Balance'].keys()], self.document.trial_balance)
        self.set_table_model('Top_Sides', [x for x in CsvTables.descriptors['Top_Sides'].keys()], self.document.top_sides)
        self.set_table_model('Eliminations', [x for x in CsvTables.descriptors['Eliminations'].keys()], self.document.current_elimination_entries)
        self.set_table_model('Documentation', [x for x in CsvTables.descriptors['Documentation'].keys()], self.document.current_elimination_docs)

        self.set_non_table_data()
    
    def set_table_model(self, table_name: str, headers: list[str], data: list[dict]):
        table = self.findChild(QtWidgets.QTableView, table_name)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = TableModel(table, headers, data)
        model.signals.dataChanged[TableModel].connect(self.table_data_changed)
        table.setModel(model)

    def set_table_data(self, table_name: str = None) -> None:
        if table_name is None:
            tables = self.findChildren(QtWidgets.QTableView)
            for table in tables:
                table.model().setTableData(self.document.data[table.objectName()])
        else:
            table = self.findChild(QtWidgets.QTableView, table_name)
            table.model().setTableData(self.document.data[table_name])

    def set_non_table_data(self) -> None:
        # set the entity name
        name = self.findChild(QtWidgets.QLineEdit, 'entityName')
        name.blockSignals(True)
        name.setText(self.document.entity_name)
        name.blockSignals(False)
        # set the beginning date
        date = self.findChild(QtWidgets.QDateEdit, 'beginningBalanceDate')
        date.blockSignals(True)
        date.setDate(QtCore.QDate.fromString(self.document.data['Beginning Balance Date'], 'M/d/yyyy'))
        date.blockSignals(False)
        # set the ending date
        date = self.findChild(QtWidgets.QDateEdit, 'endingBalanceDate')
        date.blockSignals(True)
        date.setDate(QtCore.QDate.fromString(self.document.data['Ending Balance Date'], 'M/d/yyyy'))
        date.setDate(QtCore.QDate(self.document.ending_date))
        date.blockSignals(False)
    
    def connect_elimination(self) -> None:
        # set current elimination description
        elim = self.findChild(QtWidgets.QTextEdit, 'Elim_Desc')
        elim.blockSignals(True)
        elim.setText(self.document.current_elimination_description)
        elim.blockSignals(False)
        # set current elimination entity
        elim = self.findChild(QtWidgets.QLineEdit, 'Elim_Plug_Entity')
        elim.blockSignals(True)
        elim.setText(self.document.current_elimination_plug_entity)
        elim.blockSignals(False)
        # set current elimination cc
        elim = self.findChild(QtWidgets.QLineEdit, 'Elim_Plug_CC')
        elim.blockSignals(True)
        elim.setText(self.document.current_elimination_plug_cc)
        elim.blockSignals(False)
        # set current elimination cc
        elim = self.findChild(QtWidgets.QLineEdit, 'Elim_Plug_Acct')
        elim.blockSignals(True)
        elim.setText(self.document.current_elimination_plug_account)
        elim.blockSignals(False)

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
            self.statusBar().showMessage('Opening file... please be patient... this could take several minutes...')
            if self.changed_since_last_save:
                answer = QtWidgets.QMessageBox.question(self, 'Save File', 'Save current file before proceeding?')
                if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                    self.save_menu_item()
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='JSON Files (*.json)')
            if file:
                self.filename = file
                self.document.load(self.filename)
                self.set_non_table_data()
                self.set_table_data()
                self.changed_since_last_save = False
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done opening file.')

    @QtCore.pyqtSlot()
    def save_menu_item(self):
        try:
            self.statusBar().showMessage('Saving current file... please be patient... this could take several minutes...')
            if not self.filename:
                file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='JSON Files (*.json)')
                if file:
                    if not file.casefold().endswith('.json'.casefold()):
                        file += '.json'
                    self.filename = file
                else:
                    return
            self.document.dump(self.filename)
            self.changed_since_last_save = False
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done saving current file.')

    @QtCore.pyqtSlot()
    def save_as_menu_item(self):
        try:
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='JSON Files (*.json)')
            if file:
                if not file.casefold().endswith('.json'.casefold()):
                    file += '.json'
                self.filename = file
                self.save_menu_item()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def close_menu_item(self):
        try:
            if self.changed_since_last_save:
                answer = QtWidgets.QMessageBox.question(self, 'Save File', 'Save current file before proceeding?')
                if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                    self.save_menu_item()
            self.document.reset()
            self.set_non_table_data()
            self.set_table_data()
            self.changed_since_last_save = False
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
            self.statusBar().showMessage('Importing CSV file...')
            table_name = self.menu_actions.get(self.sender().objectName(), None)
            if table_name is None:
                raise ValueError('Unrecognized action name.')
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='CSV Files (*.csv)')
            if file:
                response = QtWidgets.QMessageBox.question(self, 'Replace rows?', 'Would you like to replace all rows of data?')
                response = False if response == QtWidgets.QMessageBox.StandardButton.No else True
                self.document.import_table(table_name, file, response)
                self.set_table_data(table_name)
                self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done importing CSV file.')

    @QtCore.pyqtSlot()
    def import_oracle_tb(self):
        try:
            self.statusBar().showMessage('Importing Oracle TB...')
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='CSV Files (*.csv)')
            if file:
                response = QtWidgets.QMessageBox.question(self, 'Replace rows?', 'Would you like to replace all rows of data?')
                response = False if response == QtWidgets.QMessageBox.StandardButton.No else True
                self.document.import_oracle_tb(file, response)
                self.set_table_data()
                self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done importing Oracle TB.')

    @QtCore.pyqtSlot()
    def export_menu_item(self):
        try:
            self.statusBar().showMessage('Exporting to CSV file...')
            table_name = self.menu_actions.get(self.sender().objectName(), None)
            if table_name is None:
                raise ValueError('Unrecognized action name.')
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='CSV Files (*.csv)')
            if file:
                if not file.casefold().endswith('.csv'.casefold()):
                    file += '.csv'
                self.document.export_table(table_name, file)
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done exporting.')

    ####################################################################################
    # Consolidation Menu
    ####################################################################################

    @QtCore.pyqtSlot()
    def build_menu_item(self):
        try:
            self.statusBar().showMessage('Building the consolidation table...')
            update = QtWidgets.QMessageBox.question(self, 'New or update file?', 'Would you like to update an existing file?')
            update = False if update == QtWidgets.QMessageBox.StandardButton.No else True
            if update:
                file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select an existing file to update', filter='XLSX Files (*.xlsx)')
            else:
                file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a new file to create', filter='XLSX Files (*.xlsx)')
            if file:
                self.document.write_to_workbook(file, update)
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done building.')

    @QtCore.pyqtSlot()
    def rollforward_menu_item(self):
        try:
            msg = 'Closing the year will perminently roll-forward the balance on the adjustments tab. This procedure can not be undone. Are you sure you want to proceed?'
            response = QtWidgets.QMessageBox.question(self, 'Close the year?', msg)
            if response == QtWidgets.QMessageBox.StandardButton.Yes:
                self.document.close_year()
                self.set_table_data('Top_Sides')
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def audit_menu_item(self):
        try:
            self.statusBar().showMessage('Auditing the underlying data...')
            error_log = self.document.audit_data()
            if len(error_log) > 0:
                self.console.setTextColor(QtGui.QColor('red'))
                for err in error_log:
                    self.console.append(err)
                self.console.append(f'{len(error_log)} were detected. You must resolve these errors before you can proceed with the consolidation process.')
                self.console.setTextColor(QtGui.QColor('black'))
                raise ValueError(f'The audit process identified {len(error_log)} errors. Please check the error log below.')
            else:
                self.console.setTextColor(QtGui.QColor('green'))
                self.console.append('Audit completed successfully. No errors were found.')
                self.console.setTextColor(QtGui.QColor('black'))
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done auditing.')

    @QtCore.pyqtSlot()
    def rounding_diff_menu_item(self):
        try:
            msg = 'Are you sure you want to plug the rounding difference and post it to the trial balance?'
            response = QtWidgets.QMessageBox.question(self, 'Plug rounding difference?', msg)
            if response == QtWidgets.QMessageBox.StandardButton.Yes:
                self.document.plug_rounding_diff()
                self.set_table_data()
                self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    ####################################################################################
    # Table Slots
    ####################################################################################

    @QtCore.pyqtSlot()
    def insert_table_row(self):
        try:
            table_name = self.menu_actions.get(self.sender().objectName(), None)
            if table_name is None:
                raise ValueError('Unrecognized button name.')
            self.findChild(QtWidgets.QTableView, table_name).model().appendRow()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def delete_table_row(self):
        try:
            response = QtWidgets.QMessageBox.question(self, 'Confirm deletion', 'Delete all selected rows?')
            if response == QtWidgets.QMessageBox.StandardButton.Yes:
                table_name = self.menu_actions.get(self.sender().objectName(), None)
                if table_name is None:
                    raise ValueError('Unrecognized button name.')
                self.findChild(QtWidgets.QTableView, table_name).model().removeSelectedRows()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    
    @QtCore.pyqtSlot(TableModel)
    def table_data_changed(self, model: TableModel):
        if model.parent().objectName() == 'Top_Sides':
            self.totalTopSidesDebits.setText(model.sumColumn('Debits'))
            self.totalTopSidesCredits.setText(model.sumColumn('Credits'))
            self.totalTopSidesBeginning.setText(model.sumColumn('Beginning Balance'))
            self.totalTopSidesEnding.setText(model.sumColumn('Ending Balance'))
        self.changed_since_last_save = True
    
    ####################################################################################
    # Individual Field (QLineEdit, QTextEdit) Slots
    ####################################################################################

    @QtCore.pyqtSlot(str)
    def set_entity_name(self, new_name: str):
        try:
            self.document.data['Entity Name'] = new_name
            self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot(QtCore.QDate)
    def set_beginning_date(self, new_date: QtCore.QDate):
        try:
            self.document.data['Beginning Balance Date'] = new_date.toString('M/d/yyyy')
            self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot(QtCore.QDate)
    def set_ending_date(self, new_date: QtCore.QDate):
        try:
            new_date.toPyDate()
            self.document.data['Ending Balance Date'] = new_date.toString('M/d/yyyy')
            self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    
    @QtCore.pyqtSlot(str)
    def set_current_elimination_description(self, new_name: str):
        try:
            self.document.set_current_elimination_description(new_name)
            self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    
    @QtCore.pyqtSlot(str)
    def set_current_elimination_entity(self, entity: str):
        try:
            self.document.set_current_elimination_entity(entity)
            self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    
    @QtCore.pyqtSlot(str)
    def set_current_elimination_cost_center(self, cost_ctr: str):
        try:
            self.document.set_current_elimination_cost_center(cost_ctr)
            self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    
    @QtCore.pyqtSlot(str)
    def set_current_elimination_account(self, account: str):
        try:
            self.document.set_current_elimination_account(account)
            self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    
    @QtCore.pyqtSlot()
    def goto_next_elimination(self):
        i = self.document.next_elimination_index()
        self.findChild(QtWidgets.QLineEdit, 'Elim_Plug_Entity').set


    @QtCore.pyqtSlot()
    def goto_prev_elimination(self):
        pass

    @QtCore.pyqtSlot()
    def add_new_elimination(self):
        pass

    @QtCore.pyqtSlot()
    def del_current_elimination(self):
        pass
    
    ####################################################################################
    # Console Slots
    ####################################################################################

    @QtCore.pyqtSlot()
    def copy_console(self):
        try:
            clipboard = self.application.clipboard()
            clipboard.clear()
            clipboard.setText(self.console.toPlainText())
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def clear_console(self):
        try:
            self.console.clear()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    
