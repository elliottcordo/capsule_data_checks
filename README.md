# Capsule EDW Data Quality Checks

This repository contains HAMB manifests that check Capsule EDW data qualities. 
## How to run checks of existing manifests

```python
source hamb/bin/activate
python -m hamb.module -m grp_1_missing_nk_check
python -m hamb.module -m grp_1_duplicate_nk_check 
```

## How to generate manifests from templates

There are two templates available so far:
1. missing_nk: missing natural keys compare to source
2. duplicate_nk: duplicate natural keys check

It requires a parsed `data_config.json` file that is generated from `src/tsv_parser.py` which is parsing the data dictionary.

To generate

```python
python generate_manifests.py [missing_nk|duplicate_nk] -t [pick a group number from 1~10]
```

> Some table might needs some modifications after a generation of manifests which has to be manually updated.