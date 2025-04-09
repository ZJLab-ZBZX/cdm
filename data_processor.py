# -*- coding: utf-8 -*-
"""
@Time: 2025/3/25 13:42
@Auth: Liu Ji
"""

import json
import re
import os

def replace_newlines_in_specific_fields(
        json_file_path,
        output_file_path,
        target_fields
):
    """
    读取 JSON 文件，仅替换指定字段中的 `\n`（当 `\n` 后不是字母时）。

    参数:
        json_file_path (str): 输入 JSON 文件路径。
        output_file_path (str): 输出 JSON 文件路径。
        target_fields (list): 需要处理的字段名列表（如 ["description", "text"]）。
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    def process(obj, current_key=None):
        if isinstance(obj, dict):
            return {
                k: process(v, k)  # 传递当前字段名给递归调用
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [process(item, current_key) for item in obj]
        elif isinstance(obj, str):
            # 仅当当前字段在 target_fields 中时，才处理 `\n`
            if current_key in target_fields:
                return re.sub(r'(?<!\\)[\n\r]', '', obj)
                # return re.sub(r'\n(?![a-zA-Z])', '', obj)
            else:
                return obj
        else:
            return obj

    processed_data = process(data)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)


# 示例用法
input_json_path = os.path.join(os.getcwd() + r'\test_got_cdm.json')
output_json_path = os.path.join(os.getcwd() + r'\test_newlines_cdm.json')
fields_to_process = ["gt", "pred"]  # 指定要处理的字段

replace_newlines_in_specific_fields(
    input_json_path,
    output_json_path,
    fields_to_process
)