import csv
import re
import json

def parse_datasheet():
    output = {}
    grp_0 = ['dim_market', 'dim_facility']  # grp_0 not in the data sheet

    with open(f"src/data_sheet.tsv", newline='') as data_sheet:
        reader = csv.DictReader(data_sheet, delimiter='\t')

        for row in reader:
            table_id = row['Target Table']  # considering this: dim_address (billing) etc
            tokens = re.split(r'\s(?=\([\w ]+\))', row['Target Table'])
            if len(tokens) > 2:
                raise Exception(f"Target table {row['Target Table']} is not in parsing format.")
            target_table, address_type = tokens[0], tokens[1] if len(tokens) == 2 else ''

            grp = f'grp_0' if target_table in grp_0 else f"grp_{row['grp']}"

            output[grp] = output.get(grp, {})
            if table_id not in output[grp]:
                output[grp][table_id] = {
                    'table_id': table_id,
                    'target_dimension': target_table,
                    'target_natural_keys': [],
                    'source_natural_keys': [],
                    'source_table': '',
                    'source_timestamp': '',
                    'dim_type': 'dimension',
                    'grp': 0 if target_table in grp_0 else int(row['grp'])
                }

            target_attribute = row['Target Attribute']
            target_key = row['Target Key']
            source_table = row['Source Table']
            source_column = row['Source Column']
            target_foreign_tbl = row['Target Comments']
            target_type = row['Type']

            # grab the first table if many were specified for one column
            source_table = source_table.split(',')[0]

            if re.match(r'\w+\.\w+', source_table):
                tokens = source_table.split('.')

                if len(tokens) != 2:
                    raise Exception(f'Source table {source_table} is not like schema.table format. ')

            if target_key.lower() == 'natural key': # cannot combine with Type2 as config-type table has to be defined
                output[grp][table_id]['target_natural_keys'].append(target_attribute)
                output[grp][table_id]['source_natural_keys'].append(source_column)
                output[grp][table_id]['source_table'] = source_table

            if target_key == 'Event Timestamp':
                output[grp][table_id]['source_timestamp'] = source_column
    
            if target_type.lower() == 'fact':
                output[grp][table_id]['dim_type'] = target_type.lower()

    return output


if __name__ == '__main__':
    
    with open('data_config.json', 'w') as f:
        json.dump(parse_datasheet(), f, indent=4)