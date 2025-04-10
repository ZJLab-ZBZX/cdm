#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/3/24 9:57
@Author  : wang binghua
@FileName: wbh_data_process.py
@Software: PyCharm
"""

import json
import os

baseline_path = os.path.join(os.getcwd() + r'\test_newlines_cdm.json')
print(baseline_path)
result_path = os.path.join(os.getcwd() + r'\newKatex_output\got\metrics_res.json')
print(result_path)

with open(baseline_path, 'r', encoding='utf-8') as file:
    baseline_data = json.load(file)

baseline_cases = []
for item in baseline_data:
    img_id = item['img_id']
    img_id_parts = img_id.split('debug/')
    baseline_cases.append(img_id_parts[1])

with open(result_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
    details = data['details']

not_result_cases = []
result_cases = []
for key, value in details.items():
   result_case_id_all = key.split('debug_')
   result_case_id = result_case_id_all[1]
   result_cases.append(result_case_id)
   recall = value['recall']
   precision = value['precision']
   F1_score = value['F1_score']

   if recall==0 or precision==0 or F1_score==0:
       not_result_cases.append(result_case_id)

differences = list(set(baseline_cases).difference(set(result_cases)))
no_cases = not_result_cases + differences
file_path = 'new_katex_bugs.json'


domains_to_match = no_cases



filtered_data = [
    item for item in baseline_data
    if any(domain in item.get('img_id', '') for domain in domains_to_match)
]

with open(file_path, 'w') as file:
    json.dump(filtered_data, file, indent=4)


