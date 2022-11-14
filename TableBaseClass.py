
import csv
from PyQt5 import QtCore

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, rowData: list[dict], headerNames: list[str], parent=None):
        super().__init__(parent)
        self._rows_ = rowData
        self._headers_ = headerNames #['Date', 'Description', 'GL String', 'Unit of Measure', 'Quantity', 'Rate', 'Amount']

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return 0 if self._rows_ == None else len(self._rows_)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self._headers_)
    
    def headerData(self, index: int, orient: QtCore.Qt.Orientation, role: int = QtCore.Qt.ItemDataRole.DisplayRole) -> QtCore.QVariant:
        if role == QtCore.Qt.DisplayRole:
            if orient == QtCore.Qt.Horizontal:
                return self._headers_[index]
            if orient == QtCore.Qt.Vertical:
                return index + 1
        return QtCore.QVariant()
    
    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.ItemDataRole.DisplayRole) -> QtCore.QVariant:
        if index.isValid():
            row = self._rows_[index.row()]
            header = self._headers_[index.column()]
            if role == QtCore.Qt.DisplayRole:
                if header == 'Amount':
                    return '$' + str(round(row[header], 2))
                else:
                    return row[header]
            elif role == QtCore.Qt.TextAlignmentRole and index.column() > 3:
                if header == 'Amount':
                    return QtCore.Qt.AlignRight # | QtCore.Qt.AlignVCenter
        return QtCore.QVariant()
    
    def setData(self, index: QtCore.QModelIndex , value: QtCore.QVariant, role: int = QtCore.Qt.EditRole) -> bool:
        if index.isValid():
            row = self._rows_[index.row()]
            header = self._headers_[index.column()]
            if role == QtCore.Qt.EditRole:
                if header == 'Amount':
                    row[header] = float(value)
                else:
                    row[header] = value
                return True
        return False
    
    def insertRow(self, row: int, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> bool:
        self.beginInsertRows(parent, row, row)
        data = {h:'' for h in self._headers_}
        self._rows_.insert(row, data)
        self.endInsertRows()
        return True
    
    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        '''
        # this section can be used instead for finer control over which columns can be edited
        if index.isValid():
            if index.column() == 6:
                return QtCore.Qt.ItemFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            return QtCore.Qt.ItemFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        return QtCore.Qt.NoItemFlags
        '''
        return QtCore.Qt.ItemFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
    
    def sort(self, col: int, order: QtCore.Qt.SortOrder = QtCore.Qt.AscendingOrder) -> None:
        self.layoutAboutToBeChanged.emit()
        field = self._headers_[col]
        self._rows_.sort(key=lambda x : x[field], reverse=order)
        self.layoutChanged.emit()
    
    def removeRow(self, row: int, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> bool:
        self.beginRemoveRows(parent, row, row)
        del self._rows_[row]
        self.endRemoveRows()
        return True
    
    ######################################################################################################
    # The following methods are not inherited from QAbstractTableModel.
    ######################################################################################################

    def importCSV(self, fileName: str, replace: bool) -> None:
        '''
        if self.insertRow(self.rowCount()):   
            index = self.index(self.rowCount() - 1, 0)
            self.setData(index, fileName)
            index = self.index(self.rowCount() - 1, 1)
            self.setData(index, fileSize)
        '''
        with open(fileName, 'r', newline='') as f:
            reader = csv.DictReader(f)
            if set(self._headers_) != set(reader.fieldnames):
                raise ValueError('CSV file does not contain all required column headers.')
            self.layoutAboutToBeChanged.emit()
            if replace: self._rows_.clear()
            for row in reader:
                self._rows_.append(dict(row))
            self.layoutChanged.emit()
    
    def replaceRows(self, rowData: list[dict]) -> None:
        self.layoutAboutToBeChanged.emit()
        self._rows_ = rowData
        self.layoutChanged.emit()