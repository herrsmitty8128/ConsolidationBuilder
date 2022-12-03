
import locale
from PyQt5 import QtWidgets, QtCore


class TableModel(QtCore.QAbstractTableModel):
    ...


class TableSignals(QtCore.QObject):
    dataChanged = QtCore.pyqtSignal(TableModel)


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent, fieldnames: list[str], data: list[dict] = []):
        super().__init__(parent=parent)
        self._data_ = data
        self._fieldnames_ = fieldnames
        self.signals = TableSignals()
        locale.setlocale(locale.LC_ALL, '')

    def setTableData(self, data: list[dict]) -> None:
        self.beginResetModel()
        self._data_ = data
        self.endResetModel()
        if not self.signalsBlocked():
            self.signals.dataChanged.emit(self)

    def sumColumn(self, fieldname: str) -> int:
        return locale.format_string('$%d', sum(x[fieldname] for x in self._data_), grouping=True)

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self._data_)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self._fieldnames_)

    def headerData(self, index: int, orient: QtCore.Qt.Orientation, role: int = QtCore.Qt.ItemDataRole.DisplayRole) -> QtCore.QVariant:
        if role == QtCore.Qt.DisplayRole:
            if orient == QtCore.Qt.Horizontal:
                return self._fieldnames_[index]
            if orient == QtCore.Qt.Vertical:
                return index + 1
        return QtCore.QVariant()

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.ItemDataRole.DisplayRole) -> QtCore.QVariant:
        if index.isValid():
            field = self._fieldnames_[index.column()]
            if role == QtCore.Qt.DisplayRole:
                value = self._data_[index.row()][field]
                if field == 'Beginning Balance' or field == 'Debits' or field == 'Credits' or field == 'Ending Balance':
                    return locale.format_string('%d', value, grouping=True)
                return value
            elif role == QtCore.Qt.TextAlignmentRole:
                if field == 'Beginning Balance' or field == 'Debits' or field == 'Credits' or field == 'Ending Balance':
                    return QtCore.Qt.AlignRight
                return QtCore.Qt.AlignLeft  # QtCore.Qt.AlignVCenter
        return QtCore.QVariant()

    def setData(self, index: QtCore.QModelIndex, value: QtCore.QVariant, role: int = QtCore.Qt.EditRole) -> bool:
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                new_value = value.strip()
                if len(value) > 0:
                    field = self._fieldnames_[index.column()]
                    row = index.row()
                    data = self._data_[row]
                    if field == 'Beginning Balance':
                        try:
                            new_value = int(new_value)
                            data[field] = new_value
                            data['Ending Balance'] = new_value + data['Debits'] + data['Credits']
                        except BaseException:
                            pass
                    elif field == 'Debits':
                        try:
                            new_value = abs(int(new_value))
                            data[field] = new_value
                            data['Ending Balance'] = data['Beginning Balance'] + new_value + data['Credits']
                        except BaseException:
                            pass
                    elif field == 'Credits':
                        try:
                            new_value = -abs(int(new_value))
                            data[field] = new_value
                            data['Ending Balance'] = data['Beginning Balance'] + data['Debits'] + new_value
                        except BaseException:
                            pass
                    elif field == 'Ending Balance':
                        data[field] = int(value)
                    else:
                        data[field] = new_value

                    self.parent().horizontalHeader().resizeSections(QtWidgets.QHeaderView.ResizeToContents)

                    if not self.signalsBlocked():
                        self.signals.dataChanged.emit(self)

                    return True
        return False

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        val = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable  # QtCore.Qt.NoItemFlags
        table_name = self.parent().objectName()
        fieldname = self._fieldnames_[index.column()]
        if table_name != 'Trial_Balance' and fieldname != 'Ending Balance':
            val = val | QtCore.Qt.ItemIsEditable
        return val

    def sort(self, col: int, order: QtCore.Qt.SortOrder = QtCore.Qt.AscendingOrder) -> None:
        self.layoutAboutToBeChanged.emit()
        fieldname = self._fieldnames_[col]
        self._data_.sort(key=lambda x: x[fieldname], reverse=order)
        self.layoutChanged.emit()

    def removeSelectedRows(self) -> bool:
        indexes = self.parent().selectionModel().selectedRows()
        for i in sorted(indexes, key=lambda x: x.row(), reverse=True):
            row = i.row()
            self.beginRemoveRows(QtCore.QModelIndex(), row, row)
            del self._data_[row]
            self.endRemoveRows()
            if not self.signalsBlocked():
                self.signals.dataChanged.emit(self)

    def appendRow(self) -> None:
        row = len(self._data_)
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        r = dict()
        for field in self._fieldnames_:
            if field == 'Beginning Balance' or field == 'Debits' or field == 'Credits' or field == 'Ending Balance':
                r[field] = 0
            else:
                r[field] = ''
        self._data_.append(r)
        self.endInsertRows()
        self.parent().scrollTo(self.index(row, 0))
