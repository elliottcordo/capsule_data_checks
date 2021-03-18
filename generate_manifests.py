from typing import List, Dict
import json 
import argparse

template_manifest = """{dim_table}_{check_item}:
    label: "{dim_table}_{check_item}"
    type: "sql_comp_list"
    conn_a: "capsule-dw"
    script_a: >
{sql}
    conn_b: "capsule-dw"
    script_b: "select 1 where 1=0;"
    pct_diff: False
    warning_threshold: 1
    failure_threshold: 10

"""

missing_nk = """
        with source as (
            select distinct {source_nk} as source_nk
            from {source_table}
            where {source_timestamp} < dateadd(HOUR, -3, convert_timezone('EST', getdate()))
        ), dim as (
            select distinct {dim_nk} as dim_nk
            from capsule_dw.{dim_table}
        )
        select source.*
        from source
        left join dim on source_nk=dim_nk
        where source_nk is not null and dim_nk is null;
"""

duplicate_nk = """
        select {dim_nk}, count(*)
        from capsule_dw.v_{dim_table}
        group by 1 having count(*)>1 order by 1 desc;
"""

def combine(natural_keys: List):
    if len(natural_keys) == 1:
        return natural_keys[0]

    return '||'.join([f"coalesce({nk}::text, '')" for nk in natural_keys])

def generate_manifest(check_item, group_id):
    with open('data_config.json') as f:
        config = json.load(f)

    sql_template = globals()[check_item]

    manifest = ''
    for grp, tables in config.items():
        if grp != f'grp_{group_id}':
            continue
        for table, values in tables.items():
            target_table = values['target_dimension']
            target_natural_keys = values['target_natural_keys']
            source_natural_keys = values['source_natural_keys']
            source_table = values['source_table']
            source_timestamp = values['source_timestamp']

            source_timestamp = source_timestamp.replace('max of ', '')

            if values['target_dimension'] in ('dim_address', 'dim_contact_type'):
                continue

            sql = sql_template.format(
                source_table=source_table,
                dim_table=target_table,
                source_nk=combine(source_natural_keys),
                dim_nk=combine(target_natural_keys),
                source_timestamp=source_timestamp
            )

            manifest += template_manifest.format(
                dim_table=target_table,
                check_item=check_item,
                sql=sql
                )

        with open(f'manifests/{grp}_{check_item}_check.yaml', 'w') as f:
            f.write(manifest)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='To generate manifests from templates.')
    parser.add_argument('template', help='Templates available to use: missing_nk, duplicate_nk')
    parser.add_argument('-g', '--group', type=int, help='Pick a single domain to work on, from 1 to 10.')

    args = parser.parse_args()

    generate_manifest(args.template, args.group)
