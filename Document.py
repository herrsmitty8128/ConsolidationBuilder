
import csv
import json
import SpreadsheetTools
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

    def is_editable(self, table_name: str, col: int) -> bool:
        if table_name == 'Trial_Balance':
            return False
        if table_name == 'Adjustments':
            header = self.tables[table_name][col]
            return True if header != 'Beginning Balance' and header != 'Ending Balance' else False
        return True

    def is_enabled(self, table_name: str, col: int) -> bool:
        return True

    def is_selectable(self, table_name: str, col: int) -> bool:
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

    def remove_table_row(self, table_name: str, row: int) -> None:
        del self.data[table_name][row]

    def append_new_table_row(self, table_name: str) -> None:
        if table_name == 'Entities':
            self.data[table_name].append({'Number': '', 'Name': '', 'Group': ''})
        elif table_name == 'Cost_Centers':
            self.data[table_name].append({'Number': '', 'Name': ''})
        elif table_name == 'Accounts':
            self.data[table_name].append({'Number': '', 'Name': '', 'Level 1': '', 'Level 2': '', 'Level 3': '', 'Level 4': ''})
        elif table_name == 'Adjustments':
            self.data[table_name].append({'Entity': '', 'Cost Center': '', 'Account': '', 'Beginning Balance': 0, 'Debits': 0, 'Credits': 0, 'Ending Balance': 0, 'Description': ''})

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

    def import_table(self, table_name: str, file: str, replace: bool) -> None:

        with open(file, 'r', newline='') as f:

            reader = csv.DictReader(f)
            fieldnames = set(reader.fieldnames)
            headers = set(self.tables.get(table_name, []))

            if not headers.issubset(fieldnames):
                raise ValueError('CSV file has incorrect field names.')

            if replace:
                self.data[table_name].clear()

            for row in reader:
                r = dict()
                for header in headers:
                    if header == 'Beginning Balance':
                        r[header] = int(row[header].strip())
                    elif header == 'Debits':
                        r[header] = abs(int(row[header].strip()))
                    elif header == 'Credits':
                        r[header] = -abs(int(row[header].strip()))
                    elif header == 'Ending Balance':
                        pass  # do nothing
                    else:
                        r[header] = row[header].strip()
                if table_name == 'Trial_Balance' or table_name == 'Adjustments':
                    r['Ending Balance'] = r['Beginning Balance'] + r['Debits'] + r['Credits']
                self.data[table_name].append(r)

    def import_oracle_tb(self, file: str, replace: bool) -> None:

        with open(file, 'r', newline='') as f:

            reader = csv.DictReader(f)

            if not oracle_tb_fieldnames.issubset(set(reader.fieldnames)):
                raise ValueError('CSV file has incorrect field names.')

            if replace:
                self.data['Trial_Balance'].clear()

            entities = set(e['Number'] for e in self.data['Entities'])
            costctrs = set(c['Number'] for c in self.data['Cost_Centers'])
            accounts = set(a['Number'] for a in self.data['Accounts'])

            for row in reader:

                r = {
                    'Entity': row['PAGEBREAK_SEGMENT_VALUE'].strip(),
                    'Cost Center': row['ADDITIONAL_SEGMENT_VALUE'].strip(),
                    'Account': row['NAS_VALUE'].strip(),
                    'Beginning Balance': int(round(float(row['BEGIN_BALANCE'].strip()), 0)),
                    'Debits': abs(int(round(float(row['TOTAL_DR'].strip()), 0))),
                    'Credits': -abs(int(round(float(row['TOTAL_CR'].strip()), 0)))
                }

                r['Ending Balance'] = r['Beginning Balance'] + r['Debits'] + r['Credits']

                self.data['Trial_Balance'].append(r)

                if r['Entity'] not in entities:
                    self.data['Entities'].append({
                        'Number': r['Entity'],
                        'Name': row['PAGEBREAK_SEGMENT_DESC'].strip(),
                        'Group': ''
                    })
                    entities.add(r['Entity'])

                if r['Cost Center'] not in costctrs:
                    self.data['Cost_Centers'].append({
                        'Number': r['Cost Center'],
                        'Name': row['ADDITIONAL_SEGMENT_DESC'].strip()
                    })
                    costctrs.add(r['Cost Center'])

                if r['Account'] not in accounts:
                    self.data['Accounts'].append({
                        'Number': r['Account'],
                        'Name': row['NAS_DESC'].strip(),
                        'Level 1': '',
                        'Level 2': '',
                        'Level 3': '',
                        'Level 4': ''
                    })
                    accounts.add(r['Account'])

    def export_table(self, table_name: str, file: str) -> None:
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
        table = self.build_consolidation_table()
        if len(table) < 1:
            raise ValueError('Zero rows in the trial balance.')
        headers = [h for h in table[0].keys()]
        if update_existing:
            SpreadsheetTools.replace_table_in_existing_wb(filename, headers, table, 'CONSOLIDATION_DATA')
        else:
            SpreadsheetTools.new_wb_with_table(filename, headers, table, 'CONSOLIDATION_DATA', 'Consolidation Data')

    def plug_rounding_diff(self):
        costctrs = set(c['Number'] for c in self.data['Cost_Centers'])
        accounts = set(a['Number'] for a in self.data['Accounts'])
        if 'ROUNDING' not in costctrs:
            self.data['Cost_Centers'].append({
                'Number': 'ROUNDING',
                'Name': 'Plug rounding errror'
            })
        if 'ROUNDING' not in accounts:
            self.data['Cost_Centers'].append({
                'Number': 'ROUNDING',
                'Name': 'Plug rounding errror',
                'Level 1': '',
                'Level 2': '',
                'Level 3': '',
                'Level 4': ''
            })
        bb_counter = Counter()
        dr_counter = Counter()
        cr_counter = Counter()
        eb_counter = Counter()
        for row in self.data['Trial_Balance']:
            entity = row['Entity']
            bb_counter[entity] += row['Beginning Balance']
            dr_counter[entity] += row['Debits']
            cr_counter[entity] += row['Credits']
            eb_counter[entity] += row['Ending Balance']
        for entity in bb_counter.keys():
            x = False
            r = {
                'Entity': entity,
                'Cost Center': 'ROUNDING',
                'Account': 'ROUNDING',
                'Beginning Balance': 0,
                'Debits': 0,
                'Credits': 0,
                'Ending Balance': 0
            }
            if bb_counter[entity] != 0:
                x = True
                r['Beginning Balance'] = -bb_counter[entity]
            diff = dr_counter[entity] + cr_counter[entity]
            if diff > 0:
                x = True
                r['Credits'] = -diff
            if diff < 0:
                x = True
                r['Debits'] = -diff
            if x:
                r['Ending Balance'] = r['Beginning Balance'] + r['Debits'] + r['Credits']
                self.data['Trial_Balance'].append(r)

    def close_year(self):
        adjustments = self.data['Adjustments']
        for adj in adjustments:
            adj['Beginning Balance'] = adj['Ending Balance']
            adj['Debits'] = 0
            adj['Credits'] = 0

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
                        error_log.append(f'{k} without a value was detected on the {table_name} tab.')
            for num, cnt in counter.items():
                if cnt > 1:
                    error_log.append(f'Number {num} appears more than once on the {table_name} tab.')

        def audit_balances(table_name: str):
            table = self.data[table_name]
            '''
            for row in table:
                diff = round(row['Ending Balance'], 2) - round(row['Beginning Balance'] + row['Debits'] + row['Credits'], 2)
                if abs(diff) > 1.0:
                    error_log.append(f'Balance does not roll-forward for {row["Entity"]}-{row["Cost Center"]}-{row["Account"]} on the {table_name} list. The difference is {diff}.')
                else:
                    row['Credits'] += diff
                    diff = round(row['Ending Balance'], 2) - round(row['Beginning Balance'] + row['Debits'] + row['Credits'], 2)
                    if diff != 0.00:
                        error_log.append(f'Balance does not roll-forward for {row["Entity"]}-{row["Cost Center"]}-{row["Account"]} on the {table_name} list. The difference is {diff}.')
            '''
            # all entities numbers in the table must appear on the entities tab
            entities = set(e['Number'] for e in self.data['Entities'])
            bal_ent_nums = set(x['Entity'] for x in table)
            diff = bal_ent_nums.difference(entities)
            if len(diff) > 0:
                error_log.append(f'Entities on the trial balance, but not on the entity tab: {diff}.')

            # all cost center numbers on the table must appear on the cost centers tab
            costctrs = set(c['Number'] for c in self.data['Cost_Centers'])
            bal_cc_nums = set(x['Cost Center'] for x in table)
            diff = bal_cc_nums.difference(costctrs)
            if len(diff) > 0:
                error_log.append(f'Cost centers on the trial balance, but not on the cost center tab: {diff}.')

            # all accounts on the table must appear on the accounts tab
            accounts = set(a['Number'] for a in self.data['Accounts'])
            bal_acct_nums = set(x['Account'] for x in table)
            diff = bal_acct_nums.difference(accounts)
            if len(diff) > 0:
                error_log.append(f'Accounts on the trial balance, but not on the accounts tab: {diff}.')

            # debits must equal credits for each entity number
            bb_counter = Counter()
            dr_counter = Counter()
            cr_counter = Counter()
            eb_counter = Counter()
            for row in table:
                entity = row['Entity']
                bb_counter[entity] += row['Beginning Balance']
                dr_counter[entity] += row['Debits']
                cr_counter[entity] += row['Credits']
                eb_counter[entity] += row['Ending Balance']
            for entity in bb_counter.keys():
                if bb_counter[entity] != 0:
                    error_log.append(f'Sum of beginning balance for entity {entity} does not equal zero. The difference is {bb_counter[entity]}')
                if eb_counter[entity] != 0:
                    error_log.append(f'Sum of ending balance for entity {entity} does not equal zero. The difference is {eb_counter[entity]}')
                diff = dr_counter[entity] + cr_counter[entity]
                if diff != 0:
                    error_log.append(f'Debits do not equal credits for entity {entity}. The difference is {diff}')

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
