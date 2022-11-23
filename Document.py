
import csv
import json
from collections import Counter
from datetime import datetime

oracle_tb_fieldnames = {
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

    ####################################################################################
    # Methods to read and write to and from json file format
    ####################################################################################

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

    ####################################################################################
    # Methods for interfacing with the underlying data
    ####################################################################################

    def changed(self) -> bool:
        return self.changed_since_last_save

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
        if table_name == 'Trial_Balance':
            return False
        if table_name == 'Adjustments':
            header = self.tables[table_name][col]
            return True if header != 'Beginning Balance' and header != 'Ending Balance' else False
        return True

    def is_enabled(self, table_name: str, row: int, col: int) -> bool:
        return True

    def is_selectable(self, table_name: str, row: int, col: int) -> bool:
        return True

    def get_alignment(self, table_name: str, col: int) -> int:
        header = self.tables[table_name][col]
        if header == 'Beginning Balance' or header == 'Debits' or header == 'Credits' or header == 'Ending Balance':
            return 1
        return -1

    def sort_table(self, table_name: str, col: int, order: bool) -> None:
        col = self.tables[table_name][col]
        self.data[table_name].sort(key=lambda x: x[col], reverse=order)

    def get_table_data(self, table_name: str, row: int, col: int) -> str:
        col = self.tables[table_name][col]
        return str(self.data[table_name][row][col])

    def set_table_data(self, table_name: str, row: int, col: int, value: any) -> None:
        col = self.tables[table_name][col]
        if col == 'Beginning Balance' or col == 'Debits' or col == 'Credits':
            r = self.data[table_name][row]
            v = r[col]
            if col == 'Debits':
                try:
                    v = abs(int(value))
                except BaseException:
                    pass
            elif col == 'Credits':
                try:
                    v = -abs(int(value))
                except BaseException:
                    pass
            else:
                try:
                    v = int(value)
                except BaseException:
                    pass
            r[col] = v
            r['Ending Balance'] = r['Beginning Balance'] + r['Debits'] + r['Credits']
        elif col == 'Ending Balance':
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
    # Methods for importing and exporting tables
    ####################################################################################

    def import_table(self, table_name: str, file: str, replace: bool):

        def ent_handler(csv_row: dict) -> dict:
            return {
                'Name': csv_row['Name'].strip(),
                'Number': csv_row['Number'].strip(),
                'Group': csv_row['Group'].strip()
            }

        def cc_handler(csv_row: dict) -> dict:
            return {
                'Name': csv_row['Name'].strip(),
                'Number': csv_row['Number'].strip()
            }

        def acc_handler(csv_row: dict) -> dict:
            return {
                'Name': csv_row['Name'].strip(),
                'Number': csv_row['Number'].strip(),
                'Level 1': csv_row['Level 1'].strip(),
                'Level 2': csv_row['Level 2'].strip(),
                'Level 3': csv_row['Level 3'].strip(),
                'Level 4': csv_row['Level 4'].strip()
            }

        def adj_handler(csv_row: dict) -> dict:
            return {
                'Entity': csv_row['Entity'].strip(),
                'Cost Center': csv_row['Cost Center'].strip(),
                'Account': csv_row['Account'].strip(),
                'Beginning Balance': int(csv_row['Beginning Balance'].strip()),
                'Debits': int(csv_row['Debits'].strip()),
                'Credits': int(csv_row['Credits'].strip()),
                'Ending Balance': int(csv_row['Ending Balance'].strip()),
                'Description': csv_row['Description'].strip()
            }

        def tb_handler(csv_row: dict) -> dict:
            return {
                'Entity': csv_row['Entity'].strip(),
                'Cost Center': csv_row['Cost Center'].strip(),
                'Account': csv_row['Account'].strip(),
                'Beginning Balance': int(csv_row['Beginning Balance'].strip()),
                'Debits': int(csv_row['Debits'].strip()),
                'Credits': int(csv_row['Credits'].strip()),
                'Ending Balance': int(csv_row['Ending Balance'].strip())
            }

        def orc_handler(csv_row: dict) -> dict:
            r = {
                'Entity': csv_row['PAGEBREAK_SEGMENT_VALUE'].strip(),
                'Cost Center': csv_row['ADDITIONAL_SEGMENT_VALUE'].strip(),
                'Account': csv_row['NAS_VALUE'].strip(),
                'Beginning Balance': int(round(float(csv_row['BEGIN_BALANCE'].strip()), 0)),
                'Debits': int(round(float(csv_row['TOTAL_DR'].strip()), 0)),
                'Credits': int(round(-float(csv_row['TOTAL_CR'].strip()), 0))
            }
            r['Ending Balance'] = r['Beginning Balance'] + r['Debits'] + r['Credits']
            return r

        with open(file, 'r', newline='') as f:

            reader = csv.DictReader(f)
            fieldnames = set(reader.fieldnames)
            headers = set(self.tables.get(table_name, []))

            if table_name == 'Entities':
                handler = ent_handler
            elif table_name == 'Cost_Centers':
                handler = cc_handler
            elif table_name == 'Accounts':
                handler = acc_handler
            elif table_name == 'Adjustments':
                handler = adj_handler
            elif table_name == 'Trial_Balance':
                if not headers.issubset(fieldnames):
                    headers = oracle_tb_fieldnames
                    handler = orc_handler
                else:
                    handler = tb_handler
            else:
                raise ValueError('Unrecognized table name.')

            if not headers.issubset(fieldnames):
                raise ValueError('CSV file has incorrect field names.')

            if replace:
                self.data[table_name].clear()

            for row in reader:
                self.data[table_name].append(handler(row))

    def export_table(self, table_name: str, file: str):
        headers = self.tables.get(table_name, None)
        if headers is None:
            raise ValueError('CSV file does not have the correct field names.')
        with open(file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.data[table_name])

    ####################################################################################
    # Methods to perform the consolidation
    ####################################################################################

    def build_consolidation_table(self) -> list[dict]:
        output_data = []
        entities = {e['Number']: e for e in self.data['Entities']}
        costctrs = {c['Number']: c for c in self.data['Cost_Centers']}
        accounts = {a['Number']: a for a in self.data['Accounts']}
        for name, table in (('Trial Balance', self.data['Trial_Balance']), ('Adjustments', self.data['Adjustments'])):
            for row in table:
                entity = entities[row['Entity']]
                costctr = costctrs[row['Cost Center']]
                account = accounts[row['Account']]
                output_data.append({
                    'Type': name,
                    'Entity Number': entity['Number'],
                    'Entity Name': entity['Name'],
                    'Cost Ctr Number': costctr['Number'],
                    'Cost Ctr Name': costctr['Name'],
                    'Account Number': account['Number'],
                    'Account Name': account['Name'],
                    'Group': entity['Group'],
                    'Level 1': account['Level 1'],
                    'Level 2': account['Level 2'],
                    'Level 3': account['Level 3'],
                    'Level 4': account['Level 4'],
                    'Beginning Balance': row['Beginning Balance'],
                    'Debits': row['Debits'],
                    'Credits': row['Credits'],
                    'Ending Balance': row['Ending Balance']
                })
        return output_data

    def write_to_workbook(self, filename: str, update_existing: bool) -> None:
        import SpreadsheetTools
        table = self.build_consolidation_table()
        if len(table) < 1:
            raise ValueError('Zero rows in the trial balance.')
        headers = [h for h in table[0].keys()]
        if update_existing:
            SpreadsheetTools.replace_table_in_existing_wb(filename, headers, table, 'CONSOLIDATION_DATA')
        else:
            SpreadsheetTools.new_wb_with_table(filename, headers, table, 'CONSOLIDATION_DATA', 'Consolidation Data')

    def close_year(self):
        pass

    def audit_data(self) -> list:
        '''
        Writes error descriptions to the error log and returns the number of errors.
        '''
        error_log = []

        def audit_list(table_name: str):
            counter = Counter()
            table = self.data[table_name]
            for row in table:
                num = row['Number']
                counter[num] += 1
                for k, v in row.items():
                    if len(v) < 1:
                        error_log.append(f'{k} without a value was detected on the {table_name}.')
            for num, cnt in counter.items():
                if cnt > 1:
                    error_log.append(f'Number {num} appears more than once on the {table_name} list.')

        def audit_balances(table_name: str):
            table = self.data[table_name]
            for row in table:
                diff = round(row['Ending Balance'], 2) - round(row['Beginning Balance'] + row['Debits'] + row['Credits'], 2)
                if abs(diff) > 1.0:
                    error_log.append(f'Balance does not roll-forward for {row["Entity"]}-{row["Cost Center"]}-{row["Account"]} on the {table_name} list. The difference is {diff}.')
                else:
                    row['Credits'] += diff
                    diff = round(row['Ending Balance'], 2) - round(row['Beginning Balance'] + row['Debits'] + row['Credits'], 2)
                    if diff != 0.00:
                        error_log.append(f'Balance does not roll-forward for {row["Entity"]}-{row["Cost Center"]}-{row["Account"]} on the {table_name} list. The difference is {diff}.')

            ent_nums = set(x['Number'] for x in self.data['Entities'])
            bal_ent_nums = set(x['Entity'] for x in table)
            diff = bal_ent_nums.difference(ent_nums)
            if len(diff) > 0:
                error_log.append(f'Entities on the trial balance, but not on the entity tab: {diff}.')

            cc_nums = set(x['Number'] for x in self.data['Cost_Centers'])
            bal_cc_nums = set(x['Cost Center'] for x in table)
            diff = bal_cc_nums.difference(cc_nums)
            if len(diff) > 0:
                error_log.append(f'Cost centers on the trial balance, but not on the cost center tab: {diff}.')

            acct_nums = set(x['Number'] for x in self.data['Accounts'])
            bal_acct_nums = set(x['Account'] for x in table)
            diff = bal_acct_nums.difference(acct_nums)
            if len(diff) > 0:
                error_log.append(f'Accounts on the trial balance, but not on the accounts tab: {diff}.')

            # need to verify that debits == credits by company

        if len(self.data['Entity Name']) < 1:
            error_log.append('Entity name is missing.')

        start_date = datetime.strptime(self.data['Beginning Balance Date'], '%m/%d/%Y')
        end_date = datetime.strptime(self.data['Ending Balance Date'], '%m/%d/%Y')
        if start_date >= end_date:
            error_log.append('Beginning balance date is greater than or equal to the ending balance date.')

        audit_list('Entities')
        audit_list('Cost_Centers')
        audit_list('Accounts')
        audit_balances('Trial_Balance')
        audit_balances('Adjustments')

        return error_log
