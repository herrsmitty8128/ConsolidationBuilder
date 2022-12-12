
import csv


str_converter = lambda x : str(x)
debit_coverter = lambda x : abs(int(x))
credit_converter = lambda x : -abs(int(x))
balance_converter = lambda x: int(x)
f_debit_coverter = lambda x : abs(round(float(x),0))
f_credit_converter = lambda x : -abs(int(round(float(x),0)))
f_balance_converter = lambda x: int(round(float(x),0))


descriptors = {
    'Entities': {
        'Number': str_converter,
        'Name': str_converter,
        'Group': str_converter
    },
    'Cost_Centers': {
        'Number': str_converter,
        'Name': str_converter
    },
    'Accounts': {
        'Number': str_converter,
        'Name': str_converter,
        'Level 1': str_converter,
        'Level 2': str_converter,
        'Level 3': str_converter,
        'Level 4': str_converter
    },
    'Trial_Balance': {
        'Entity': str_converter,
        'Cost Center': str_converter,
        'Account': str_converter,
        'Beginning Balance': balance_converter,
        'Debits': debit_coverter,
        'Credits': credit_converter,
        'Ending Balance': balance_converter
    },
    'Top_Sides': {
        'Entity': str_converter,
        'Cost Center': str_converter,
        'Account': str_converter,
        'Beginning Balance': balance_converter,
        'Debits': debit_coverter,
        'Credits': credit_converter,
        'Ending Balance': balance_converter,
        'Description': str_converter
    },
    'Eliminations': {
        'Entity': str_converter,
        'Cost Center': str_converter,
        'Account': str_converter
    },
    'Documentation': {
        'Full Path or URL': str_converter
    },
    'Oracle_TB': {
        'PAGEBREAK_SEGMENT_DESC': str_converter,   # entity
        'ADDITIONAL_SEGMENT_DESC': str_converter,  # cost center
        'NAS_DESC': str_converter,                 # account
        'BEGIN_BALANCE': f_balance_converter,
        'TOTAL_DR': f_debit_coverter,
        'TOTAL_CR': f_credit_converter,
        'END_BALANCE': f_balance_converter
    }
}


def load(file_name: str, table_name: str) -> list[dict]:
    '''
    Loads a csv table from a file and serializes all the fileds.
    '''
    data = []
    desc = descriptors[table_name]
    with open(file_name, 'r', newline='') as f:
        reader = csv.DictReader(f)
        if not set(desc.keys()).issubset(set(reader.fieldnames)):
            raise ValueError('CSV file has incorrect field names.')
        for row in reader:
            data.append({n:h(row[n].strip()) for n,h in desc.items()})
    return data


def dump(file_name: str, data_table: list[dict], table_name: str) -> None:
    '''
    Writes a data table to a csv file.
    '''
    if len(data_table) > 0:
        desc = descriptors[table_name]
        with open(file_name, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[x for x in desc.keys()])
            writer.writeheader()
            writer.writerows(data_table)


def convert_oracle_tb(oracle_tb: list[dict]) -> None:
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
            row[old_key] = row.pop(new_key)
        
        
