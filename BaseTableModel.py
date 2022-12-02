

from PyQt5 import QtWidgets, QtCore

class BaseTableModel(QtCore.QAbstractTableModel): ...

class TableSignals(QtCore.QObject):
    dataChanged = QtCore.pyqtSignal(BaseTableModel)

class BaseTableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent, document, table_name):
        super().__init__(parent=parent)
        self.document = document
        self.table_name = table_name
        self.signals = TableSignals()

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return self.document.row_count(self.table_name)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return self.document.column_count(self.table_name)

    def headerData(self, index: int, orient: QtCore.Qt.Orientation, role: int = QtCore.Qt.ItemDataRole.DisplayRole) -> QtCore.QVariant:
        if role == QtCore.Qt.DisplayRole:
            if orient == QtCore.Qt.Horizontal:
                return self.document.column_header(self.table_name, index)
            if orient == QtCore.Qt.Vertical:
                return index + 1
        return QtCore.QVariant()

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.ItemDataRole.DisplayRole) -> QtCore.QVariant:
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return self.document.get_table_data(self.table_name, index.row(), index.column())
            elif role == QtCore.Qt.TextAlignmentRole:
                a = self.document.get_alignment(self.table_name, index.column())
                if a > 0:
                    return QtCore.Qt.AlignRight
                if a < 0:
                    return QtCore.Qt.AlignLeft
                return QtCore.Qt.AlignVCenter
        return QtCore.QVariant()

    def setData(self, index: QtCore.QModelIndex, value: QtCore.QVariant, role: int = QtCore.Qt.EditRole) -> bool:
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                value = value.strip()
                if len(value) > 0:
                    self.document.set_table_data(self.table_name, index.row(), index.column(), value)
                    self.parent().horizontalHeader().resizeSections(QtWidgets.QHeaderView.ResizeToContents)
                    if not self.signalsBlocked():
                        self.signals.dataChanged.emit(self)
                return True
        return False

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        val = QtCore.Qt.NoItemFlags
        if self.document.is_editable(self.table_name, index.column()):
            val = val | QtCore.Qt.ItemIsEditable
        if self.document.is_enabled(self.table_name, index.column()):
            val = val | QtCore.Qt.ItemIsEnabled
        if self.document.is_selectable(self.table_name, index.column()):
            val = val | QtCore.Qt.ItemIsSelectable
        return val

    def sort(self, col: int, order: QtCore.Qt.SortOrder = QtCore.Qt.AscendingOrder) -> None:
        self.layoutAboutToBeChanged.emit()
        self.document.sort_table(self.table_name, col, order)
        self.layoutChanged.emit()

    def remove_selected_rows(self) -> bool:
        indexes = self.parent().selectionModel().selectedRows()
        for i in sorted(indexes, key=lambda x: x.row(), reverse=True):
            row = i.row()
            self.beginRemoveRows(QtCore.QModelIndex(), row, row)
            self.document.remove_table_row(self.table_name, row)
            self.endRemoveRows()
            if not self.signalsBlocked():
                self.signals.dataChanged.emit(self)

    def append_new_table_row(self) -> None:
        table = self.table_name
        row = self.document.row_count(table)
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.document.append_new_table_row(table)
        self.endInsertRows()
        self.parent().scrollTo(self.index(row, 0))
