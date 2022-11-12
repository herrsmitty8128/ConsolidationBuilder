import MainWindow
from PyQt5 import QtWidgets, QtCore



class ConsolidationMainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):


    def __init__(self, application):
        super().__init__()
        self.setupUi(self)
        self.application = application
        #tableView = self.findChild(QtWidgets.QTableView, 'invoiceLineItemsTableView')
        #tableView.setModel(InvoiceLineItem.TableModel(parent=tableView))
    