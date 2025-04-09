#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/3/24 9:57
@Author  : wang binghua
@FileName: cdm_output_post_data_process.py
@Software: PyCharm
"""

import json
import os


def get_baseline_cases_list(baseline_path):
    with open(baseline_path, 'r', encoding='utf-8') as file:
        baseline_data = json.load(file)

    baseline_cases = []
    for item in baseline_data:
        img_id = item['img_id']
        img_id_parts = img_id.split('debug/')
        baseline_cases.append(img_id_parts[1])
    return baseline_data, baseline_cases


def get_no_result_cases(result_path, baseline_cases):
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
    no_cases_list = not_result_cases + differences
    return no_cases_list


def filter_enter_by_replace(file_path,result_file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    for item in data:
        gt = item['gt']
        pred = item['pred']
        new_gt = gt.replace('\n', '')
        new_pred = pred.replace('\n', '')
        item['gt'] = new_gt
        item['pred'] = new_pred
    with open(result_file_path, 'w', encoding='utf-8') as file:
        # 将修改后的 baseline_data 以 JSON 格式写入文件
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    baseline_path = os.path.join(os.getcwd() + r'\test_got_cdm11_filter.json')
    print(baseline_path)
    cdm_output_path = os.path.join(os.getcwd() + r'\cdm_output\test_got_cdm11_filter0407\metrics_res.json')
    print(cdm_output_path)
    no_result_file_path = os.path.join(os.getcwd() + r'\no_result_output0407.json')
    #定义文件路径
    # 存储符合条件的 item
    matched_items = []
    baseline_data, baseline_cases = get_baseline_cases_list(baseline_path)
    cdm_no_output_case_list = get_no_result_cases(cdm_output_path, baseline_cases)
    for item in baseline_data:
        img_id = item['img_id']
        img_id_parts = img_id.split('debug/')
        gt = item['gt']
        pred = item['pred']
        if img_id_parts[1] in cdm_no_output_case_list:
            matched_items.append(item)

    with open(no_result_file_path, 'w', encoding='utf-8') as file:
        # 将修改后的 baseline_data 以 JSON 格式写入文件
        json.dump(matched_items, file, ensure_ascii=False, indent=4)