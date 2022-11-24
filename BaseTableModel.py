
from PyQt5 import QtWidgets, QtCore


class BaseTableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent, document, table_name):
        super().__init__(parent=parent)
        self.document = document
        self.table_name = table_name

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
                return True
        return False

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        val = 0
        if self.document.is_editable(self.table_name, index.row(), index.column()):
            val = val | QtCore.Qt.ItemIsEditable
        if self.document.is_enabled(self.table_name, index.row(), index.column()):
            val = val | QtCore.Qt.ItemIsEnabled
        if self.document.is_selectable(self.table_name, index.row(), index.column()):
            val = val | QtCore.Qt.ItemIsSelectable
        return val

    def sort(self, col: int, order: QtCore.Qt.SortOrder = QtCore.Qt.AscendingOrder) -> None:
        self.layoutAboutToBeChanged.emit()
        self.document.sort_table(self.table_name, col, order)
        self.layoutChanged.emit()

    def remove_selected_rows(self, row: int, count: int, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> bool:
        indexes = self.parent().selectionModel().selectedIndexes()
        print(indexes)
        for i in indexes:
            print(vars(i))
        for i in sorted(indexes, reverse=True):
            self.beginRemoveRows(parent, i, 0)
            self.document.remove_table_row(self.table_name, i)
            self.endRemoveRows()
