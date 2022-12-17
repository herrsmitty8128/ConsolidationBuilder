
import csv
import locale
from PyQt5 import QtWidgets, QtCore


locale.setlocale(locale.LC_ALL, '')


def currency(x): return locale.format_string('%d', x, grouping=True)


class TableSignals(QtCore.QObject):
    dataChanged = QtCore.pyqtSignal()
    sumDebitsChanged = QtCore.pyqtSignal(str)
    sumCreditsChanged = QtCore.pyqtSignal(str)
    sumBeginBalChanged = QtCore.pyqtSignal(str)
    sumEndBalChanged = QtCore.pyqtSignal(str)


class BaseTableModel(QtCore.QAbstractTableModel):

    descriptors = {
        'None': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent=parent)
        self._data_ = []
        self._descriptors_ = type(self).descriptors
        self._fieldnames_ = [h for h in self._descriptors_.keys()]

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

    def getAlignment(self, fieldname: str):
        return QtCore.Qt.AlignLeft  # QtCore.Qt.AlignLeft or QtCore.Qt.AlignVCenter or QtCore.Qt.AlignRight

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.ItemDataRole.DisplayRole) -> QtCore.QVariant:
        if index.isValid():
            field = self._fieldnames_[index.column()]
            if role == QtCore.Qt.DisplayRole:
                value = self._data_[index.row()][field]
                return self._descriptors_[field]['to string'](value)
            elif role == QtCore.Qt.TextAlignmentRole:
                return self.getAlignment(field)
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
                    except BaseException:
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
        self._data_.append({n: h['default value'] for n, h in self._descriptors_.items()})
        self.endInsertRows()
        self.parent().scrollTo(self.index(row, 0))

    def load_csv(self, file_name: str, replace: bool) -> None:
        if replace:
            self._data_.clear()
        with open(file_name, 'r', newline='') as f:
            reader = csv.DictReader(f)
            if not set(self._fieldnames_).issubset(set(reader.fieldnames)):
                raise ValueError('CSV file has incorrect field names.')
            for row in reader:
                self._data_.append({n: h['to value'](row[n].strip()) for n, h in self._descriptors_.items()})
        self.layoutChanged.emit()

    def dump_csv(self, file_name: str) -> None:
        if len(self._data_) > 0:
            with open(file_name, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self._fieldnames_)
                writer.writeheader()
                writer.writerows(self._data_)


class EntityTableModel(BaseTableModel):

    descriptors = {
        'Number': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Name': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Group': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent)


class CostCenterTableModel(BaseTableModel):

    descriptors = {
        'Number': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Name': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent)


class AccountTableModel(BaseTableModel):

    descriptors = {
        'Number': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Name': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Level 1': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Level 2': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Level 3': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Level 4': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent)


class TrialBalanceTableModel(BaseTableModel):

    descriptors = {
        'Entity': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Cost Center': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Account': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Beginning Balance': {'default value': 0, 'to string': currency, 'to value': lambda x: int(x)},
        'Debits': {'default value': 0, 'to string': currency, 'to value': lambda x: abs(int(x))},
        'Credits': {'default value': 0, 'to string': currency, 'to value': lambda x: -abs(int(x))},
        'Ending Balance': {'default value': 0, 'to string': currency, 'to value': lambda x: int(x)}
    }

    oracle_tb = {
        'PAGEBREAK_SEGMENT_DESC': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'ADDITIONAL_SEGMENT_DESC': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'NAS_DESC': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'BEGIN_BALANCE': {'default value': 0, 'to string': currency, 'to value': lambda x: int(round(float(x), 0))},
        'TOTAL_DR': {'default value': 0, 'to string': currency, 'to value': lambda x: abs(int(round(float(x), 0)))},
        'TOTAL_CR': {'default value': 0, 'to string': currency, 'to value': lambda x: -abs(int(round(float(x), 0)))},
        'END_BALANCE': {'default value': 0, 'to string': currency, 'to value': lambda x: int(round(float(x), 0))}
    }

    def __init__(self, parent):
        super().__init__(parent)
        self.signals = TableSignals()

    def sumColumn(self, fieldname: str) -> int:
        return locale.format_string('$%d', sum(x[fieldname] for x in self._data_), grouping=True)

    def getAlignment(self, fieldname: str):
        if fieldname == 'Beginning Balance' or fieldname == 'Debits' or fieldname == 'Credits' or fieldname == 'Ending Balance':
            return QtCore.Qt.AlignRight
        return QtCore.Qt.AlignLeft  # QtCore.Qt.AlignLeft or QtCore.Qt.AlignVCenter or QtCore.Qt.AlignRight

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
            self.signals.sumBeginBalChanged.emit(self.sumColumn('Beginning Balance'))
            self.signals.sumDebitsChanged.emit(self.sumColumn('Debits'))
            self.signals.sumCreditsChanged.emit(self.sumColumn('Credits'))
            self.signals.sumEndBalChanged.emit(self.sumColumn('Ending Balance'))

    def setData(self, index: QtCore.QModelIndex, value: QtCore.QVariant, role: int = QtCore.Qt.EditRole) -> bool:
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                new_value = value.strip()
                if len(new_value) > 0:
                    try:
                        field = self._fieldnames_[index.column()]
                        row = index.row()
                        data = self._data_[row]
                        new_value = self._descriptors_[field]['to value'](new_value)
                        if field == 'Beginning Balance':
                            data[field] = new_value
                            data['Ending Balance'] = new_value + data['Debits'] + data['Credits']
                            self.signals.sumBeginBalChanged.emit(self.sumColumn('Beginning Balance'))
                            self.signals.sumEndBalChanged.emit(self.sumColumn('Ending Balance'))
                        elif field == 'Debits':
                            data[field] = new_value
                            data['Ending Balance'] = data['Beginning Balance'] + new_value + data['Credits']
                            self.signals.sumDebitsChanged.emit(self.sumColumn('Debits'))
                            self.signals.sumEndBalChanged.emit(self.sumColumn('Ending Balance'))
                        elif field == 'Credits':
                            data[field] = new_value
                            data['Ending Balance'] = data['Beginning Balance'] + data['Debits'] + new_value
                            self.signals.sumCreditsChanged.emit(self.sumColumn('Credits'))
                            self.signals.sumEndBalChanged.emit(self.sumColumn('Ending Balance'))
                        elif field == 'Ending Balance':
                            pass
                        else:
                            data[field] = new_value
                        self.parent().horizontalHeader().resizeSections(QtWidgets.QHeaderView.ResizeToContents)
                    except BaseException:
                        pass

                    if not self.signalsBlocked():
                        self.signals.dataChanged.emit()
                        #self.signals.sumBeginBalChanged.emit(self.sumColumn('Beginning Balance'))
                        # self.signals.sumDebitsChanged.emit(self.sumColumn('Debits'))
                        # self.signals.sumCreditsChanged.emit(self.sumColumn('Credits'))
                        #self.signals.sumEndBalChanged.emit(self.sumColumn('Ending Balance'))

                    return True
        return False

    def removeSelectedRows(self) -> bool:
        if super().removeSelectedRows():
            if not self.signalsBlocked():
                self.signals.sumBeginBalChanged.emit(self.sumColumn('Beginning Balance'))
                self.signals.sumDebitsChanged.emit(self.sumColumn('Debits'))
                self.signals.sumCreditsChanged.emit(self.sumColumn('Credits'))
                self.signals.sumEndBalChanged.emit(self.sumColumn('Ending Balance'))
            return True
        return False

    def load_csv(self, file_name: str, replace: bool) -> None:
        super().load_csv(file_name, replace)
        if not self.signalsBlocked():
            self.signals.sumBeginBalChanged.emit(self.sumColumn('Beginning Balance'))
            self.signals.sumDebitsChanged.emit(self.sumColumn('Debits'))
            self.signals.sumCreditsChanged.emit(self.sumColumn('Credits'))
            self.signals.sumEndBalChanged.emit(self.sumColumn('Ending Balance'))

    def import_oracle_tb(self, file_name: str, replace: bool) -> None:
        if replace:
            self._data_.clear()
        data = []
        with open(file_name, 'r', newline='') as f:
            reader = csv.DictReader(f)
            desc = type(self).oracle_tb
            if not set(desc.keys()).issubset(set(reader.fieldnames)):
                raise ValueError('CSV file has incorrect field names.')
            for row in reader:
                data.append({n: h['to value'](row[n].strip()) for n, h in desc.items()})
        self.convert_oracle_tb(data)
        self._data_.extend(data)
        self.layoutChanged.emit()
        if not self.signalsBlocked():
            self.signals.sumBeginBalChanged.emit(self.sumColumn('Beginning Balance'))
            self.signals.sumDebitsChanged.emit(self.sumColumn('Debits'))
            self.signals.sumCreditsChanged.emit(self.sumColumn('Credits'))
            self.signals.sumEndBalChanged.emit(self.sumColumn('Ending Balance'))

    def convert_oracle_tb(self, oracle_tb: list[dict]) -> None:
        '''
        Converts all the fieldnames in an oracle trial balance to useable names.
        '''
        field_crosswalk = {
            'PAGEBREAK_SEGMENT_DESC': 'Entity',
            'ADDITIONAL_SEGMENT_DESC': 'Cost Center',
            'NAS_DESC': 'Account',
            'BEGIN_BALANCE': 'Beginning Balance',
            'TOTAL_DR': 'Debits',
            'TOTAL_CR': 'Credits',
            'END_BALANCE': 'Ending Balance'
        }
        fields = set(x for x in field_crosswalk.keys())
        for row in oracle_tb:
            if set(row.keys()) != fields:
                raise KeyError(f'Not all rows in the Oracle trial balance contain the correct fields: {row}')
            for old_key, new_key in field_crosswalk.items():
                row[new_key] = row.pop(old_key)


class TopSidesTableModel(TrialBalanceTableModel):

    descriptors = {
        'Entity': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Cost Center': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Account': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Beginning Balance': {'default value': 0, 'to string': currency, 'to value': lambda x: int(x)},
        'Debits': {'default value': 0, 'to string': currency, 'to value': lambda x: abs(int(x))},
        'Credits': {'default value': 0, 'to string': currency, 'to value': lambda x: -abs(int(x))},
        'Ending Balance': {'default value': 0, 'to string': currency, 'to value': lambda x: int(x)},
        'Description': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent)


class EliminationsTableModel(BaseTableModel):

    descriptors = {
        'Entity': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Cost Center': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Account': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent)


class DocumentationTableModel(BaseTableModel):

    descriptors = {
        'Full Path or URL': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent)


class NCIDocumentationTableModel(BaseTableModel):

    descriptors = {
        'Full Path or URL': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent)

class NCIPercentsTableModel(BaseTableModel):

    descriptors = {
        'Enitity': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'NCI Percent': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)},
        'Description': {'default value': '', 'to string': lambda x: str(x), 'to value': lambda x: str(x)}
    }

    def __init__(self, parent):
        super().__init__(parent)