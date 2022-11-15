
import csv
from PyQt5 import QtCore


class BaseTableModel(QtCore.QAbstractTableModel):

    def __init__(self, headerNames: list[str], parent=None, rowData: list[dict] = []):
        super().__init__(parent)
        self._rows_ = rowData
        self._headers_ = headerNames

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return 0 if self._rows_ is None else len(self._rows_)

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
        try:
            if index.isValid():
                row = self._rows_[index.row()]
                header = self._headers_[index.column()]
                if role == QtCore.Qt.DisplayRole:
                    return row[header]
                elif role == QtCore.Qt.TextAlignmentRole:
                    return QtCore.Qt.AlignLeft  # QtCore.Qt.AlignRight # | QtCore.Qt.AlignVCenter
            return QtCore.QVariant()
        except Exception as err:
            print(err)

    def setData(self, index: QtCore.QModelIndex, value: QtCore.QVariant, role: int = QtCore.Qt.EditRole) -> bool:
        try:
            if index.isValid():
                row = self._rows_[index.row()]
                header = self._headers_[index.column()]
                if role == QtCore.Qt.EditRole:
                    row[header] = value
                    return True
            return False
        except Exception as err:
            print(err)

    def insertRow(self, row: int, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> bool:
        self.beginInsertRows(parent, row, row)
        data = {h: '' for h in self._headers_}
        self._rows_.insert(row, data)
        self.endInsertRows()
        return True

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        return QtCore.Qt.ItemFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def sort(self, col: int, order: QtCore.Qt.SortOrder = QtCore.Qt.AscendingOrder) -> None:
        self.layoutAboutToBeChanged.emit()
        field = self._headers_[col]
        self._rows_.sort(key=lambda x: x[field], reverse=order)
        self.layoutChanged.emit()

    def removeRow(self, row: int, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> bool:
        self.beginRemoveRows(parent, row, row)
        del self._rows_[row]
        self.endRemoveRows()
        return True

    def removeRows(self, row: int, count: int, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> bool:
        if count < 1:
            return False
        self.beginRemoveRows(parent, row, row + count - 1)
        del self._rows_[row:row + count]
        self.endRemoveRows()
        return True

    ######################################################################################################
    # The following methods are not inherited from QAbstractTableModel.
    ######################################################################################################

    def importCSV(self, fileName: str, replace: bool) -> None:
        with open(fileName, 'r', newline='') as f:
            reader = csv.DictReader(f)
            if set(self._headers_) != set(reader.fieldnames):
                raise ValueError('CSV file does not contain all required column headers.')
            self.layoutAboutToBeChanged.emit()
            if replace:
                self._rows_.clear()
            for row in reader:
                self._rows_.append(dict(row))
            self.layoutChanged.emit()

    def replaceRows(self, rowData: list[dict]) -> None:
        self.layoutAboutToBeChanged.emit()
        self._rows_ = rowData
        self.layoutChanged.emit()

    def exportCSV(self, fileName: str) -> None:
        with open(fileName, 'w', newline='') as f:
            writer = csv.DictWriter(f, self._headers_)
            writer.writeheader()
            writer.writerows(self._rows_)
