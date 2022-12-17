
from PyQt5 import QtWidgets, QtCore

class TableView(QtWidgets.QTableView):

    def __init__(self, parent) -> None:
        super().__init__(parent)
    
    @QtCore.pyqtSlot()
    def removeSelectedRows(self):
        try:
            answer = QtWidgets.QMessageBox.question(self, 'Are you sure?', 'Are you sure you want to permanently delete all selected rows?')
            if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                self.model().removeSelectedRows()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    
    @QtCore.pyqtSlot()
    def appendRow(self):
        try:
            self.model().appendRow()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))