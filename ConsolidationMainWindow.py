import MainWindow
from PyQt5 import QtWidgets, QtCore


class ConsolidationMainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):


    def __init__(self, application: QtWidgets.QApplication):
        super().__init__()
        self.setupUi(self)
        self.application = application
        self.new_document()
        # add the data models to the table views here...
        #tableView = self.findChild(QtWidgets.QTableView, 'invoiceLineItemsTableView')
        #tableView.setModel(InvoiceLineItem.TableModel(parent=tableView))
    

    @QtCore.pyqtSlot()
    def connect_data(self):
        try:
            # connect the data to the table veiw data models
            # refresh the table models
            pass
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    @QtCore.pyqtSlot()
    def new_document(self):
        try:
            print('new_document')
            self.filename = None
            self.document = {
                'Entity': '',
                'Accounts': [],
                'Cost Centers': [],
                'Entities': [],
                'Trial Balance': {},
                'Adjustments': []
            }
            self.connect_data()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    @QtCore.pyqtSlot()
    def open_document(self):
        try:
            print('open_document')
            pass
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    @QtCore.pyqtSlot()
    def save_document(self):
        try:
            print('save_document')
            pass
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))


    @QtCore.pyqtSlot()
    def save_as_document(self):
        try:
            print('save_as_document')
            pass
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    @QtCore.pyqtSlot()
    def close_document(self):
        try:
            print('close_document')
            pass
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    @QtCore.pyqtSlot()
    def quit_application(self):
        try:
            self.application.quit()
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    
    
    @QtCore.pyqtSlot()
    def build_consolidation(self):
        try:
            pass
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))