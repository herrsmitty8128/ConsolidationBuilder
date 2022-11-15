
import csv
from BaseTableModel import BaseTableModel
from PyQt5 import QtCore


class TrialBalanceTableModel(BaseTableModel):

    nativeHeaders = {
        'Entity',
        'Cost Center',
        'Account',
        'Beginning Balance',
        'Debits',
        'Credits',
        'Ending Balance'
    }

    oracleHeaders = {
        # 'DATA_ACCESS_SET_NAME',
        'LEDGER_NAME_PARAM',
        'P_AMOUNT_TYPE',
        'ACCOUNTING_PERIOD_PARAM',
        'LEDGER_CURRENCY_PARAM',
        'P_CURRENCY_TYPE',
        'CURRENCY_TYPE_PARAM',
        'ENTERED_CURRENCY_PARAM',
        'RESULTING_CURRENCY',
        'P_SUM_BY',
        'SUMMARIZE_BY_PARAM',
        'BATCH_TYPE_PARAM',
        'P_BATCH_TYPE',
        'ENCUMBRANCE_TYPE_PARAM',
        'FILTER_CONDITIONS_ATT',
        'FILTER_CONDITIONS_OPT',
        'REPT_EXECUTION_DATE',
        'PAGEBREAK_SEGMENT_NAME',
        'ADDL_SEGMENT_NAME',
        'NAT_ACCT_SEGMENT_NAME',
        'ENCUMBRANCE_ACCOUNTING_FLAG',
        'LEDGER_NAME',
        'PAGEBREAK_SEGMENT_VALUE',
        'PAGEBREAK_SEGMENT_DESC',
        'ADDITIONAL_SEGMENT_VALUE',
        'ADDITIONAL_SEGMENT_DESC',
        'ACCT',
        'ACCT_DESC',
        'ACCT_TYPE',
        'NAS_VALUE',
        'NAS_DESC',
        'BEGIN_BALANCE',
        'TOTAL_DR',
        'TOTAL_CR',
        'END_BALANCE'
    }

    def __init__(self, headerNames: list[str], parent=None):
        super().__init__(headerNames, parent, TrialBalanceTableModel.nativeHeaders)

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.ItemDataRole.DisplayRole) -> QtCore.QVariant:
        if index.isValid():
            row = self._rows_[index.row()]
            header = self._headers_[index.column()]
            if role == QtCore.Qt.DisplayRole:
                if header == 'Beginning Balance' or header == 'Debits' or header == 'Credits' or header == 'Ending Balance':
                    return str(round(row[header], 2))
                else:
                    return row[header]
            elif role == QtCore.Qt.TextAlignmentRole:
                if header == 'Beginning Balance' or header == 'Debits' or header == 'Credits' or header == 'Ending Balance':
                    return QtCore.Qt.AlignRight  # | QtCore.Qt.AlignVCenter
                else:
                    return QtCore.Qt.AlignLeft
        return QtCore.QVariant()

    def setData(self, index: QtCore.QModelIndex, value: QtCore.QVariant, role: int = QtCore.Qt.EditRole) -> bool:
        if index.isValid():
            row = self._rows_[index.row()]
            header = self._headers_[index.column()]
            if role == QtCore.Qt.EditRole:
                if header == 'Beginning Balance' or header == 'Debits' or header == 'Credits' or header == 'Ending Balance':
                    row[header] = float(value)
                else:
                    row[header] = value
                return True
        return False

    def insertRow(self, row: int, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> bool:
        self.beginInsertRows(parent, row, row)
        data = {}
        for h in self._headers_:
            if h == 'Beginning Balance' or h == 'Debits' or h == 'Credits' or h == 'Ending Balance':
                data[h] == 0.0
            else:
                data[h] == ''
        self._rows_.insert(row, data)
        self.endInsertRows()
        return True

    # the trial balance is meant to be imported from Oracle
    # therefore it is not editable

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        return QtCore.Qt.ItemFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def importCSV(self, fileName: str, replace: bool) -> None:

        def importOracle(reader: csv.DictReader):
            for row in reader:
                r = {
                    'Entity': row['PAGEBREAK_SEGMENT_VALUE'].strip(),
                    'Cost Center': row['ADDITIONAL_SEGMENT_VALUE'].strip(),
                    'Account': row['NAS_VALUE'].strip(),
                    'Beginning Balance': float(row['BEGIN_BALANCE']),
                    'Debits': float(row['TOTAL_DR']),
                    'Credits': -float(row['TOTAL_CR']),
                    'Ending Balance': float(row['END_BALANCE'])
                }
                self._rows_.append(r)

        def importNative(reader: csv.DictReader):
            for row in reader:
                r = {
                    'Entity': row['Entity'].strip(),
                    'Cost Center': row['Cost Center'].strip(),
                    'Account': row['Account'].strip(),
                    'Beginning Balance': float(row['Beginning Balance']),
                    'Debits': float(row['Debits']),
                    'Credits': float(row['Credits']),
                    'Ending Balance': float(row['Ending Balance'])
                }
                self._rows_.append(r)

        with open(fileName, 'r', newline='') as f:
            reader = csv.DictReader(f)
            headerSet = set(reader.fieldnames)
            if TrialBalanceTableModel.nativeHeaders.issubset(headerSet):
                handler = importNative
            elif TrialBalanceTableModel.oracleHeaders.issubset(headerSet):
                handler = importOracle
            else:
                raise ValueError('Trial balance CSV file does not contain all required column headers.')
            self.layoutAboutToBeChanged.emit()
            if replace:
                self._rows_.clear()
            handler(reader)
            self.layoutChanged.emit()
