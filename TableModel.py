
import csv
import locale
from PyQt5 import QtWidgets, QtCore

locale.setlocale(locale.LC_ALL, '')
currency = lambda x : locale.format_string('%d', x, grouping=True)


class TableSignals(QtCore.QObject):
    sumDebitsChanged = QtCore.pyqtSignal(int)
    sumCreditsChanged = QtCore.pyqtSignal(int)
    sumBeginBalChanged = QtCore.pyqtSignal(int)
    sumEndBalChanged = QtCore.pyqtSignal(int)


class BaseTableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent, descriptors: dict, data: list[dict] = []):
        super().__init__(parent=parent)
        self._data_ = data
        self._fieldnames_ = [h for h in descriptors.keys()]
        self._descriptors_ = descriptors

    def setTableData(self, data: list[dict]) -> None:
        self.beginResetModel()
        self._data_ = data
        self.endResetModel()

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
                return self._descriptors_[field]['to string'](value)
            elif role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignLeft  # QtCore.Qt.AlignVCenter or QtCore.Qt.AlignRight
        return QtCore.QVariant()
    
    def setData(self, index: QtCore.QModelIndex, value: QtCore.QVariant, role: int = QtCore.Qt.EditRole) -> bool:
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                new_value = value.strip()
                if len(new_value) > 0:
                    try:
                        field = self._fieldnames_[index.column()]
                        row = index.row()
                        self._data_[row][field] = self._descriptors_[field]['to value'](new_value)
                        self.parent().horizontalHeader().resizeSections(QtWidgets.QHeaderView.ResizeToContents)
                        return True
                    except:
                        pass
        return False

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable   # QtCore.Qt.NoItemFlags

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

    def appendRow(self) -> None:
        row = len(self._data_)
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self._data_.append({n:h['default value'] for n,h in self._descriptors_.items()})
        self.endInsertRows()
        self.parent().scrollTo(self.index(row, 0))
    
    def load_csv(self, file_name: str, replace: bool) -> list[dict]:
        data = []
        if replace:
            self._data_.clear()
        with open(file_name, 'r', newline='') as f:
            reader = csv.DictReader(f)
            if not set(self._fieldnames_).issubset(set(reader.fieldnames)):
                raise ValueError('CSV file has incorrect field names.')
            for row in reader:
                self._data_.append({n:h['to value'](row[n].strip()) for n,h in self._descriptors_.items()})
        self.layoutChanged.emit()

    def dump_csv(self, file_name: str) -> None:
        if len(self._data_) > 0:
            with open(file_name, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self._fieldnames_)
                writer.writeheader()
                writer.writerows(self._data_)


class EntityTableModel(BaseTableModel):

    descriptors = {
        'Number': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Name': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Group': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent, EntityTableModel.descriptors)


class CostCenterTableModel(BaseTableModel):

    descriptors = {
        'Number': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Name': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent, CostCenterTableModel.descriptors)


class AccountTableModel(BaseTableModel):

    descriptors = {
        'Number': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Name': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Level 1': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Level 2': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Level 3': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Level 4': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent, AccountTableModel.descriptors)


class TrialBalanceTableModel(BaseTableModel):

    descriptors = {
        'Entity': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Cost Center': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Account': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Beginning Balance': {'default value': 0, 'to string': currency, 'to value': lambda x : int(x)},
        'Debits': {'default value': 0, 'to string': currency, 'to value': lambda x : abs(int(x))},
        'Credits': {'default value': 0, 'to string': currency, 'to value': lambda x : -abs(int(x))},
        'Ending Balance': {'default value': 0, 'to string': currency, 'to value': lambda x : int(x)}
    }

    def __init__(self, parent):
        super().__init__(parent, TrialBalanceTableModel.descriptors)
        self.signals = TopSidesTableModel()
    
    def sumColumn(self, fieldname: str) -> int:
        return locale.format_string('$%d', sum(x[fieldname] for x in self._data_), grouping=True)
    
    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if index.isValid():
            field = self._fieldnames_[index.column()]
            if field == 'Ending Balance':
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
            else:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        return QtCore.Qt.NoItemFlags
    
    def setTableData(self, data: list[dict]) -> None:
        super().setTableData(data)
        if not self.signalsBlocked():
            self.signals.topSidesChanged.emit(self)

    def setData(self, index: QtCore.QModelIndex, value: QtCore.QVariant, role: int = QtCore.Qt.EditRole) -> bool:
        if super().setData(index, value, role):
            if not self.signalsBlocked():
                self.signals.topSidesChanged.emit(self)
            return True
        return False

    def removeSelectedRows(self) -> bool:
        if super().removeSelectedRows():
            if not self.signalsBlocked():
                self.signals.topSidesChanged.emit(self)
            return True
        return False


class TopSidesTableModel(TrialBalanceTableModel):

    descriptors = {
        'Entity': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Cost Center': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Account': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Beginning Balance': {'default value': 0, 'to string': currency, 'to value': lambda x : int(x)},
        'Debits': {'default value': 0, 'to string': currency, 'to value': lambda x : abs(int(x))},
        'Credits': {'default value': 0, 'to string': currency, 'to value': lambda x : -abs(int(x))},
        'Ending Balance': {'default value': 0, 'to string': currency, 'to value': lambda x : int(x)},
        'Description' : {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent, TopSidesTableModel.descriptors)


class EliminationsTableModel(BaseTableModel):

    descriptors = {
        'Entity': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Cost Center': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)},
        'Account': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent, EliminationsTableModel.descriptors)


class DocumentationTableModel(BaseTableModel):

    descriptors = {
        'Full Path or URL': {'default value': '', 'to string': lambda x : str(x), 'to value': lambda x : str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent, DocumentationTableModel.descriptors)


'''
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
'''