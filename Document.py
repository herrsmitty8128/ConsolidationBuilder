
import csv
import json


class Document:

    def __init__(self):

        self.tables = {
            'Entities': ['Number', 'Name', 'Group'],
            'Cost_Centers': ['Number', 'Name'],
            'Accounts': ['Number', 'Name', 'Level 1', 'Level 2', 'Level 3', 'Level 4'],
            'Trial_Balance': ['Entity', 'Cost Center', 'Account', 'Beginning Balance', 'Debits', 'Credits', 'Ending Balance'],
            'Adjustments': ['Entity', 'Cost Center', 'Account', 'Beginning Balance', 'Debits', 'Credits', 'Ending Balance', 'Description']
        }

        self.reset()

    def dump(self, filename: str) -> None:
        if not filename.casefold().endswith('.json'.casefold()):
            filename += '.json'
        f = open(filename, 'w')
        json.dump(self.data, f)  # , indent=3)
        f.close()
        self.changed_since_last_save = False

    def load(self, filename: str) -> None:
        f = open(filename, 'r')
        self.data = json.load(f)
        f.close()
        self.changed_since_last_save = False

    def changed(self) -> bool:
        return self.changed_since_last_save

    ####################################################################################
    # CUSTOM METHODS AND SLOTS
    ####################################################################################

    def set_entity_name(self, new_name: str):
        self.data['Entity Name'] = new_name
        self.changed_since_last_save = True

    def get_entity_name(self) -> None:
        return self.data['Entity Name']

    def set_beginning_date(self, new_date: str):
        self.data['Beginning Balance Date'] = new_date
        self.changed_since_last_save = True

    def get_beginning_date(self) -> str:
        return self.data['Beginning Balance Date']

    def set_ending_date(self, new_date: str):
        self.data['Ending Balance Date'] = new_date
        self.changed_since_last_save = True

    def get_ending_date(self) -> None:
        return self.data['Ending Balance Date']

    def column_count(self, table_name: str) -> None:
        return len(self.tables[table_name])

    def row_count(self, table_name: str) -> None:
        return len(self.data[table_name])

    def column_header(self, table_name: str, col: int) -> str:
        return self.tables[table_name][col]

    def is_editable(self, table_name: str, row: int, col: int) -> bool:
        return True

    def is_enabled(self, table_name: str, row: int, col: int) -> bool:
        return True

    def is_selectable(self, table_name: str, row: int, col: int) -> bool:
        return True

    def sort_table(self, table_name: str, col: int, order: bool) -> None:
        col = self.tables[table_name][col]
        self.data[table_name].sort(key=lambda x: x[col], reverse=order)

    def get_table_data(self, table_name: str, row: int, col: int) -> str:
        col = self.tables[table_name][col]
        return str(self.data[table_name][row][col])

    def set_table_data(self, table_name: str, row: int, col: int, value: any) -> None:
        col = self.tables[table_name][col]
        if col == 'Beginning Balance' or col == 'Debits' or col == 'Credits' or col == 'Ending Balance':
            self.data[table_name][row][col] = int(value)
        else:
            self.data[table_name][row][col] = value
        self.changed_since_last_save = True

    def reset(self):
        self.data = {
            'Entity Name': '',
            'Beginning Balance Date': '12/31/9999',
            'Ending Balance Date': '12/31/9999',
            'Accounts': [],
            'Cost_Centers': [],
            'Entities': [],
            'Trial_Balance': [],
            'Adjustments': []
        }
        self.changed_since_last_save = False

    ####################################################################################
    # DATA MENU
    ####################################################################################

    def import_table(self, table_name: str, file: str, replace: bool):
        if table_name not in self.tables:
            raise ValueError('Unrecognized import table')
        headers = set(self.tables[table_name]['HeaderNames'])
        model = self.tables[table_name]['TableModel']
        reader = csv.DictReader(file)
        if not headers.issubset(reader.fieldnames):
            pass

    def export_table(self, table_name: str, file: str):
        pass

    ####################################################################################
    # CONSOLIDATION MENU
    ####################################################################################

    def build_consolidation(self):
        try:
            pass
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))

    def close_year(self):
        pass

    def audit_data(self):

        def audit_list(errors: list, items: list, item_name: str):
            counter = Counter()
            for item in items:
                num = item['Number']
                if len(num) < 1:
                    errors.append(f'{item_name} without a number was detected.')
                if len(item['Name']) < 1:
                    errors.append(f'{item_name} without a name was detected.')
                counter[num] += 1
            for num, cnt in counter.items():
                if cnt > 1:
                    errors.append(f'{item_name} number {num} appears more than once on the list. Each {item_name} must have a unique number.')

        def audit_balances(errors: list, items: list, item_name: str):
            for item in items:
                diff = round(item['Ending Balance'], 2) - round(item['Beginning Balance'] + item['Debits'] + item['Credits'], 2)
                if abs(diff) > 1.0:
                    errors.append(f'Balance does not roll-forward for {item["Entity"]}-{item["Cost Center"]}-{item["Account"]} on the {item_name}. The difference is {diff}.')
                else:
                    item['Credits'] += diff
                    diff = round(item['Ending Balance'], 2) - round(item['Beginning Balance'] + item['Debits'] + item['Credits'], 2)
                    if diff != 0.00:
                        errors.append(f'Balance does not roll-forward for {item["Entity"]}-{item["Cost Center"]}-{item["Account"]} on the {item_name}. The difference is {diff}.')

            ent_nums = set(x['Number'] for x in self.data['Entities'])
            bal_ent_nums = set(x['Entity'] for x in items)
            diff = bal_ent_nums.difference(ent_nums)
            if len(diff) > 0:
                errors.append(f'Entities on the trial balance, but not on the entity tab: {diff}.')

            cc_nums = set(x['Number'] for x in self.data['Cost Centers'])
            bal_cc_nums = set(x['Cost Center'] for x in items)
            diff = bal_cc_nums.difference(cc_nums)
            if len(diff) > 0:
                errors.append(f'Cost centers on the trial balance, but not on the cost center tab: {diff}.')

            acct_nums = set(x['Number'] for x in self.data['Accounts'])
            bal_acct_nums = set(x['Account'] for x in items)
            diff = bal_acct_nums.difference(acct_nums)
            if len(diff) > 0:
                errors.append(f'Accounts on the trial balance, but not on the accounts tab: {diff}.')

        try:
            errors = []

            self.errors.append('Starting the audit process...')

            if len(self.master.findChild(QtWidgets.QLineEdit, 'entityName').text()) < 1:
                errors.append('Entity name is missing.')

            start_date = QtCore.QDate.fromString(self.data['Beginning Balance Date'], 'M/d/yyyy')
            end_date = QtCore.QDate.fromString(self.data['Ending Balance Date'], 'M/d/yyyy')
            if start_date >= end_date:
                errors.append('Beginning balance date is greater than or equal to the ending balance date.')

            audit_list(errors, self.data['Entities'], 'Entity')
            audit_list(errors, self.data['Cost Centers'], 'Cost center')
            audit_list(errors, self.data['Accounts'], 'Account')
            audit_balances(errors, self.data['Trial Balance'], 'Trial balance')
            audit_balances(errors, self.data['Adjustments'], 'Adjustments')

            if len(errors) > 0:
                self.errors.setTextColor(QtGui.QColor('red'))
                for err in errors:
                    self.errors.append(err)
                self.errors.append(f'{len(errors)} were detected. You must resolve these errors before you can proceed with the consolidation process.')
                self.errors.setTextColor(QtGui.QColor('black'))
                raise ValueError(f'The audit process identified {len(errors)} errors. Please check the error log below.')
            else:
                self.errors.setTextColor(QtGui.QColor('green'))
                self.errors.append('Audit completed successfully. No errors were found.')
                self.errors.setTextColor(QtGui.QColor('black'))

        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error', str(err))
