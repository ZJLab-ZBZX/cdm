# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 09:40:00 2025

@author: ZJ
"""
import os, glob, json, argparse
from modules.latex2bbox_color import latex2bbox_color
from evaluation import evaluation
from multiprocessing import Pool


def gen_color_list(num=10, gap=15):
    num += 1
    single_num = 255 // gap + 1
    max_num = single_num ** 3
    num = min(num, max_num)
    color_list = []
    for idx in range(num):
        R = idx // single_num**2
        GB = idx % single_num**2
        G = GB // single_num
        B = GB % single_num
        
        color_list.append((R*gap, G*gap, B*gap))
    return color_list[1:]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('--input', '-i', type=str, default="bugs.json")
    # parser.add_argument('--output', '-o', type=str, default=os.path.join("bugs_output", "got"))
    parser.add_argument('--input', '-i', type=str, default="test_cdm.json")
    parser.add_argument('--output', '-o', type=str, default=os.path.join("debug", "got"))
    parser.add_argument('--num_pools', '-n', type=str, default=1)
    args = parser.parse_args()


    temp_dir = os.path.join(args.output, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    total_color_list = gen_color_list(num=5800)
    with open(args.input, 'r', encoding='utf-8') as f:
        labels = json.load(f)
    img_ids = [label['img_id'] for label in labels]
    gt_texts = [label['gt'] for label in labels]
    pred_texts = [label['pred'] for label in labels]
    basenames = [img_id.replace('/', '_') for img_id in img_ids]

    myP = Pool(args.num_pools)
    for subset in ['gt', 'pred']:
        output_path = os.path.join(args.output, subset)
        os.makedirs(os.path.join(output_path, 'vis'), exist_ok=True)
        os.makedirs(os.path.join(output_path, 'bbox'), exist_ok=True)
        for i, label in enumerate(labels):
            img_id = label['img_id']
            latex = label[subset]
            basename = img_id.replace('/', '_')  
            input_arg = (latex, basename, output_path, temp_dir, total_color_list)
            myP.apply_async(latex2bbox_color, args=(input_arg,))
            #latex2bbox_color((latex, basename, output_path, temp_dir, total_color_list))
    myP.close()
    myP.join()

        
    metrics_res, metric_res_path, match_vis_dir = evaluation(args.output)
