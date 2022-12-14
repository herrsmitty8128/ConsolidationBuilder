
import MainWindow
import json
import TableModel
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui


class ConsolidationMainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):

    def __init__(self, application: QtWidgets.QApplication):

        super().__init__()

        self.setupUi(self)
        self.application = application
        self.filename = None
        self.changed_since_last_save = False

        table = self.Entities
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = TableModel.EntityTableModel(table)
        # REMEMBER TO REMOVE THESE CONNECTIONS IN DESIGNER
        self.addCostCenterButton.clicked.connect(model.appendRow)
        self.deleteEntityButton.clicked.connect(model.removeSelectedRows)
        table.setModel(model)

        table = self.Cost_Centers
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = TableModel.CostCenterTableModel(table)
        # REMEMBER TO REMOVE THESE CONNECTIONS IN DESIGNER
        self.addEntityButton.clicked.connect(model.appendRow)
        self.deleteCostCenterButton.clicked.connect(model.removeSelectedRows)
        table.setModel(model)

        table = self.Accounts
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = TableModel.AccountTableModel(table)
        table.setModel(model)

        table = self.Trial_Balance
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = TableModel.TrialBalanceTableModel(table)
        table.setModel(model)

        table = self.Top_Sides
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = TableModel.TopSidesTableModel(table)
        model.signals.sumBeginBalChanged[str].connect(self.totalTopSidesBeginning.setText)
        model.signals.sumDebitsChanged[str].connect(self.totalTopSidesDebits.setText)
        model.signals.sumCreditsChanged[str].connect(self.totalTopSidesCredits.setText)
        model.signals.sumEndBalChanged[str].connect(self.totalTopSidesEnding.setText)
        table.setModel(model)

        table = self.Eliminations
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = TableModel.EliminationsTableModel(table)
        table.setModel(model)

        table = self.Documentation
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model = TableModel.DocumentationTableModel(table)
        table.setModel(model)

    ####################################################################################
    ####################################################################################
    # FILE MENU
    ####################################################################################
    ####################################################################################

    def build_json_data(self) -> dict:
        return {
            'Entity Name': self.entityName.text(),
            'Beginning Balance Date': datetime.strftime(self.beginningBalanceDate.date().toPyDate(), '%m/%d/%Y'),
            'Ending Balance Date': datetime.strftime(self.endingBalanceDate.date().toPyDate(), '%m/%d/%Y'),
            'Accounts': self.Accounts.model()._data_,
            'Cost_Centers': self.Cost_Centers.model()._data_,
            'Entities': self.Entities.model()._data_,
            'Trial_Balance': self.Trial_Balance.model()._data_,
            'Top_Sides': self.Top_Sides.model()._data_
        }

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
                f = open(self.filename, 'r')
                data = json.load(f)
                f.close()
                self.Entities.model().setTableData(data['Entities'])
                self.Cost_Centers.model().setTableData(data['Cost_Centers'])
                self.Accounts.model().setTableData(data['Accounts'])
                self.Trial_Balance.model().setTableData(data['Trial_Balance'])
                self.Top_Sides.model().setTableData(data['Top_Sides'])
                self.entityName.setText(data['Entity Name'])
                self.beginningBalanceDate.setDate(QtCore.QDate.fromString(data['Beginning Balance Date'], 'M/d/yyyy'))
                self.endingBalanceDate.setDate(QtCore.QDate.fromString(data['Ending Balance Date'], 'M/d/yyyy'))
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
            data = self.build_json_data()
            f = open(self.filename, 'w')
            json.dump(data, f)  # , indent=3)
            f.close()
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
            self.entityName.setText('')
            self.beginningBalanceDate.setDate(QtCore.QDate())
            self.endingBalanceDate.setDate(QtCore.QDate())
            self.Entities.model().setTableData([])
            self.Cost_Centers.model().setTableData([])
            self.Accounts.model().setTableData([])
            self.Trial_Balance.model().setTableData([])
            self.Top_Sides.model().setTableData([])
            self.Eliminations.model().setTableData([])
            self.Documentation.model().setTableData([])
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
    ####################################################################################
    # DATA MENU
    ####################################################################################
    ####################################################################################

    @QtCore.pyqtSlot()
    def import_entities_menu_item(self):
        try:
            self.statusBar().showMessage('Importing entities from CSV file...')
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='CSV Files (*.csv)')
            if file:
                response = QtWidgets.QMessageBox.question(self, 'Replace rows?', 'Would you like to replace all rows of data?')
                response = False if response == QtWidgets.QMessageBox.StandardButton.No else True
                self.Entities.model().load_csv(file, response)
                self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done importing CSV file.')

    @QtCore.pyqtSlot()
    def import_cost_centers_menu_item(self):
        try:
            self.statusBar().showMessage('Importing cost centers from CSV file...')
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='CSV Files (*.csv)')
            if file:
                response = QtWidgets.QMessageBox.question(self, 'Replace rows?', 'Would you like to replace all rows of data?')
                response = False if response == QtWidgets.QMessageBox.StandardButton.No else True
                self.Cost_Centers.model().load_csv(file, response)
                self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done importing CSV file.')

    @QtCore.pyqtSlot()
    def import_accounts_menu_item(self):
        try:
            self.statusBar().showMessage('Importing accounts from CSV file...')
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='CSV Files (*.csv)')
            if file:
                response = QtWidgets.QMessageBox.question(self, 'Replace rows?', 'Would you like to replace all rows of data?')
                response = False if response == QtWidgets.QMessageBox.StandardButton.No else True
                self.Accounts.model().load_csv(file, response)
                self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done importing CSV file.')

    @QtCore.pyqtSlot()
    def import_trial_balance_menu_item(self):
        try:
            self.statusBar().showMessage('Importing trial balance from CSV file...')
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='CSV Files (*.csv)')
            if file:
                response = QtWidgets.QMessageBox.question(self, 'Replace rows?', 'Would you like to replace all rows of data?')
                response = False if response == QtWidgets.QMessageBox.StandardButton.No else True
                self.Trial_Balance.model().load_csv(file, response)
                self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done importing CSV file.')

    @QtCore.pyqtSlot()
    def import_top_sides_menu_item(self):
        try:
            self.statusBar().showMessage('Importing top sides from CSV file...')
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='CSV Files (*.csv)')
            if file:
                response = QtWidgets.QMessageBox.question(self, 'Replace rows?', 'Would you like to replace all rows of data?')
                response = False if response == QtWidgets.QMessageBox.StandardButton.No else True
                self.Top_Sides.model().load_csv(file, response)
                self.changed_since_last_save = True
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done importing CSV file.')

    @QtCore.pyqtSlot()
    def import_oracle_tb(self):
        # try:
        self.statusBar().showMessage('Importing Oracle TB...')
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to open', filter='CSV Files (*.csv)')
        if file:
            response = QtWidgets.QMessageBox.question(self, 'Replace rows?', 'Would you like to replace all rows of data?')
            response = False if response == QtWidgets.QMessageBox.StandardButton.No else True
            self.Trial_Balance.model().import_oracle_tb(file, response)
            self.changed_since_last_save = True
        '''
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done importing Oracle TB.')
        '''

    @QtCore.pyqtSlot()
    def export_entities_menu_item(self):
        try:
            self.statusBar().showMessage('Exporting entities to CSV file...')
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='CSV Files (*.csv)')
            if file:
                if not file.casefold().endswith('.csv'.casefold()):
                    file += '.csv'
                self.Entities.model().dump_csv(file)
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done exporting.')

    @QtCore.pyqtSlot()
    def export_cost_centers_menu_item(self):
        try:
            self.statusBar().showMessage('Exporting cost centers to CSV file...')
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='CSV Files (*.csv)')
            if file:
                if not file.casefold().endswith('.csv'.casefold()):
                    file += '.csv'
                self.Cost_Centers.model().dump_csv(file)
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done exporting.')

    @QtCore.pyqtSlot()
    def export_accounts_menu_item(self):
        try:
            self.statusBar().showMessage('Exporting accounts to CSV file...')
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='CSV Files (*.csv)')
            if file:
                if not file.casefold().endswith('.csv'.casefold()):
                    file += '.csv'
                self.Accounts.model().dump_csv(file)
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done exporting.')

    @QtCore.pyqtSlot()
    def export_trial_balance_menu_item(self):
        try:
            self.statusBar().showMessage('Exporting trial balance to CSV file...')
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='CSV Files (*.csv)')
            if file:
                if not file.casefold().endswith('.csv'.casefold()):
                    file += '.csv'
                self.Trial_Balance.model().dump_csv(file)
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done exporting.')

    @QtCore.pyqtSlot()
    def export_top_sides_menu_item(self):
        try:
            self.statusBar().showMessage('Exporting top sides to CSV file...')
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a filename to save', filter='CSV Files (*.csv)')
            if file:
                if not file.casefold().endswith('.csv'.casefold()):
                    file += '.csv'
                self.Top_Sides.model().dump_csv(file)
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
        finally:
            self.statusBar().showMessage('Done exporting.')

    ####################################################################################
    ####################################################################################
    # Consolidation Menu
    ####################################################################################
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
    ####################################################################################
    # Table Slots
    ####################################################################################
    ####################################################################################

    @QtCore.pyqtSlot()
    def insert_entity_table_row(self):
        try:
            self.Entities.model().appendRow()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def insert_cost_center_table_row(self):
        try:
            self.Cost_Centers.model().appendRow()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def insert_account_table_row(self):
        try:
            self.Accounts.model().appendRow()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def insert_trial_balance_table_row(self):
        try:
            self.Trial_Balance.model().appendRow()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def insert_top_sides_table_row(self):
        try:
            self.Top_Sides.model().appendRow()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def insert_elimination_entry_table_row(self):
        try:
            self.Eliminations.model().appendRow()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def insert_elimination_doc_table_row(self):
        try:
            self.Documentation.model().appendRow()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def delete_entity_table_rows(self):
        try:
            self.Entities.model().removeSelectedRows()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def delete_cost_center_table_rows(self):
        try:
            self.Cost_Centers.model().removeSelectedRows()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def delete_account_table_rows(self):
        try:
            self.Accounts.model().removeSelectedRows()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def delete_trial_balance_table_rows(self):
        try:
            self.Trial_Balance.model().removeSelectedRows()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def delete_top_sides_table_rows(self):
        try:
            self.Top_Sides.model().removeSelectedRows()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def delete_elimination_entry_table_rows(self):
        try:
            self.Eliminations.model().removeSelectedRows()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def delete_elimination_doc_table_rows(self):
        try:
            self.Documentation.model().removeSelectedRows()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    ####################################################################################
    ####################################################################################
    # Current Elimination Slots
    ####################################################################################
    ####################################################################################

    @QtCore.pyqtSlot()
    def add_new_elimination(self):
        pass

    @QtCore.pyqtSlot()
    def del_current_elimination(self):
        pass

    @QtCore.pyqtSlot()
    def goto_next_elimination(self):
        pass

    @QtCore.pyqtSlot()
    def goto_prev_elimination(self):
        pass

    ####################################################################################
    ####################################################################################
    # Text Slots
    ####################################################################################
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

    @QtCore.pyqtSlot()
    def copy_elimination_description(self):
        try:
            clipboard = self.application.clipboard()
            clipboard.clear()
            clipboard.setText(self.Elim_Desc.toPlainText())
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def clear_elimination_description(self):
        try:
            self.Elim_Desc.clear()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    @QtCore.pyqtSlot()
    def paste_elimination_description(self):
        try:
            self.Elim_Desc.clear()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
