
import json
import SpreadsheetTools
from datetime import datetime
from collections import Counter
from datetime import datetime


class Document:

    def __init__(self):
        self.reset()

    def reset(self):
        self.current_elimination_index = 0
        self._entity_name = ''
        self._beginning_date = datetime.now()
        self._ending_date = datetime.now()
        self._accounts = []
        self._cost_centers = []
        self._entities = []
        self._trial_balance = []
        self._top_sides = []
        self._eliminations = [ # starts with one empty elimination
            {
                'entries': [],
                'description': '',
                'plug':{'Entity': '', 'Cost Center': '', 'Account': ''},
                'documentation': []
            }
        ]

    ####################################################################################
    # setter/getter methods
    ####################################################################################

    @property
    def entity_name(self) -> str:
        return self._entity_name
    
    @entity_name.setter
    def entity_name(self, new_name: str) -> None:
        if not isinstance(new_name, str):
            raise TypeError('Document.entity_name must be a string object.')
        self._entity_name = new_name
    
    @property
    def beginning_date(self) -> datetime:
        return self._beginning_date
    
    @beginning_date.setter
    def beginning_date(self, new_date: datetime) -> None:
        if not isinstance(new_date, datetime):
            raise TypeError('Document.beginning_date must be a datetime object.')
        self._beginning_date = new_date

    @property
    def ending_date(self) -> datetime:
        return self._ending_date
    
    @ending_date.setter
    def ending_date(self, new_date: datetime) -> None:
        if not isinstance(new_date, datetime):
            raise TypeError('Document.ending_date must be a datetime object.')
        self._ending_date = new_date
    
    @property
    def accounts(self) -> list[dict]:
        return self._accounts
    
    @accounts.setter
    def accounts(self, new_list: list[dict]) -> None:
        if not isinstance(new_list, list) or not all(isinstance(obj, dict) for obj in new_list):
            raise TypeError('Document.accounts must be a list[dict] object.')
        self._accounts = new_list
    
    @property
    def cost_centers(self) -> list[dict]:
        return self._cost_centers
    
    @cost_centers.setter
    def cost_centers(self, new_list: list[dict]) -> None:
        if not isinstance(new_list, list) or not all(isinstance(obj, dict) for obj in new_list):
            raise TypeError('Document.cost_centers must be a list[dict] object.')
        self._cost_centers = new_list
    
    @property
    def entities(self) -> list[dict]:
        return self._entities
    
    @entities.setter
    def entities(self, new_list: list[dict]) -> None:
        if not isinstance(new_list, list) or not all(isinstance(obj, dict) for obj in new_list):
            raise TypeError('Document.entities must be a list[dict] object.')
        self._entities = new_list
    
    @property
    def trial_balance(self) -> list[dict]:
        return self._trial_balance
    
    @trial_balance.setter
    def trial_balance(self, new_list: list[dict]) -> None:
        if not isinstance(new_list, list) or not all(isinstance(obj, dict) for obj in new_list):
            raise TypeError('Document.trial_balance must be a list[dict] object.')
        self._trial_balance = new_list
    
    @property
    def top_sides(self) -> list[dict]:
        return self._top_sides
    
    @top_sides.setter
    def top_sides(self, new_list: list[dict]) -> None:
        if not isinstance(new_list, list) or not all(isinstance(obj, dict) for obj in new_list):
            raise TypeError('Document.top_sides must be a list[dict] object.')
        self._top_sides = new_list
    
    @property
    def eliminations(self) -> list[dict]:
        return self._eliminations
    
    @eliminations.setter
    def eliminations(self, new_list: list[dict]) -> None:
        if not isinstance(new_list, list) or not all(isinstance(obj, dict) for obj in new_list):
            raise TypeError('Document.eliminations must be a list[dict] object.')
        self._eliminations = new_list
    
    @property
    def current_elimination_description(self):
        return self._eliminations[self.current_elimination_index]['description']
    
    @current_elimination_description.setter
    def current_elimination_description(self, description: str) -> None:
        if not isinstance(description, str):
            raise TypeError('Document.current_elimination_description must be a str object.')
        self._eliminations[self.current_elimination_index]['description'] = description
    
    @property
    def current_elimination_plug_entity(self):
        return self._eliminations[self.current_elimination_index]['plug']['Entity']
    
    @current_elimination_plug_entity.setter
    def current_elimination_plug_entity(self, entity: str) -> None:
        if not isinstance(entity, str):
            raise TypeError('Document.current_elimination_plug_entity must be a str object.')
        self._eliminations[self.current_elimination_index]['plug']['Entity'] = entity
    
    @property
    def current_elimination_plug_cc(self):
        return self._eliminations[self.current_elimination_index]['plug']['Cost Center']
    
    @current_elimination_plug_cc.setter
    def current_elimination_plug_cc(self, cost_ctr: str) -> None:
        if not isinstance(cost_ctr, str):
            raise TypeError('Document.current_elimination_plug_cc must be a str object.')
        self._eliminations[self.current_elimination_index]['plug']['Cost Center'] = cost_ctr
    
    @property
    def current_elimination_plug_account(self):
        return self._eliminations[self.current_elimination_index]['plug']['Account']
    
    @current_elimination_plug_account.setter
    def current_elimination_plug_account(self, account: str) -> None:
        if not isinstance(account, str):
            raise TypeError('Document.current_elimination_plug_account must be a str object.')
        self._eliminations[self.current_elimination_index]['plug']['Account'] = account
    
    @property
    def current_elimination_entries(self):
        return self._eliminations[self.current_elimination_index]['entries']
    
    @current_elimination_entries.setter
    def current_elimination_entries(self, entries: list[dict]) -> None:
        if not isinstance(entries, list) or not all(isinstance(obj, dict) for obj in entries):
            raise TypeError('Document.current_elimination_entries must be a list[dict] object.')
        self._eliminations[self.current_elimination_index]['entries'] = entries
    
    @property
    def current_elimination_docs(self):
        return self._eliminations[self.current_elimination_index]['documentation']
    
    @current_elimination_docs.setter
    def current_elimination_docs(self, docs: list[dict]) -> None:
        if not isinstance(docs, list) or not all(isinstance(obj, dict) for obj in docs):
            raise TypeError('Document.current_elimination_docs must be a list[dict] object.')
        self._eliminations[self.current_elimination_index]['documentation'] = docs
    
    def goto_next_elimination(self):
        i = self.current_elimination_index + 1
        if i >= len(self._eliminations): i = 0
        self.increment_current_elimination_index = i
    
    def goto_prev_elimination(self):
        i = self.current_elimination_index - 1
        if i < 0: i = len(self._eliminations) - 1
        self.increment_current_elimination_index = i

    ####################################################################################
    # Methods for saving and loading the document
    ####################################################################################

    def dump(self, filename: str) -> None:
        data = {
            'entity_name': self.entity_name,
            'beginning_date': datetime.strftime(self.beginning_date, '%m/%d/%Y'),
            'ending_date': datetime.strftime(self.ending_date, '%m/%d/%Y'),
            'accounts': self.accounts,
            'cost_centers': self.cost_centers,
            'entities': self.entities,
            'trial_balance': self.trial_balance,
            'eliminations': self.eliminations
        }
        if not filename.casefold().endswith('.json'.casefold()):
            filename += '.json'
        f = open(filename, 'w')
        json.dump(data, f)  # , indent=3)
        f.close()

    def load(self, filename: str) -> None:
        f = open(filename, 'r')
        data = json.load(f)
        f.close()
        self.entity_name = data['entity_name']
        self.beginning_date = datetime.strptime(data['beginning_date'], '%m/%d/%Y')
        self.ending_date = datetime.strptime(data['ending_date'], '%m/%d/%Y')
        self.entities = data['entities']
        self.cost_centers = data['cost_centers']
        self.accounts = data['accounts']
        self.top_sides = data['top_sides']
        self.eliminations = data['eliminations']

    ####################################################################################
    # Methods to perform the consolidation
    ####################################################################################

    def build_consolidation_table(self) -> list[dict]:
        output_data = []
        entities = {e['Number']: e for e in self.entities}
        costctrs = {c['Number']: c for c in self.cost_centers}
        accounts = {a['Number']: a for a in self.accounts}
        for name, table in (('Trial Balance', self.trial_balance), ('Top_Sides', self.top_sides)):
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
        if 'ROUNDING' not in set(c['Number'] for c in self.data['Cost_Centers']):
            self.data['Cost_Centers'].append({
                'Number': 'ROUNDING',
                'Name': 'Plug rounding error'
            })
        if 'ROUNDING' not in set(a['Number'] for a in self.data['Accounts']):
            self.data['Accounts'].append({
                'Number': 'ROUNDING',
                'Name': 'Plug rounding error',
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
        topsides = self._top_sides
        for adj in topsides:
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
        audit_balances('Top_Sides')

        return error_log
    