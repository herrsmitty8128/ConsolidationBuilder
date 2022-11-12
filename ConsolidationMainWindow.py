import MainWindow
from PyQt5 import QtWidgets, QtCore



class ConsolidationMainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):


    def __init__(self, application):
        super().__init__()
        self.setupUi(self)
        self.application = application
        self.new_data()
        # add the data models to the table views here...
        #tableView = self.findChild(QtWidgets.QTableView, 'invoiceLineItemsTableView')
        #tableView.setModel(InvoiceLineItem.TableModel(parent=tableView))
    

    @QtCore.pyqtSlot()
    def connect_data(self):
        try:
            # connect the data to the table veiw data models
            pass
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
    

    @QtCore.pyqtSlot()
    def new_data(self):
        try:
            self.datafile = None
            self.data = {
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