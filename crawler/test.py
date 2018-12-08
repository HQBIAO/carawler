# coding=utf-8
import re

import pandas as pd


def split_ref_item():
    df_reference = pd.read_csv('/Users/chenjunbiao/project/graduation_project/paper_degree_paper_with_reference.csv')
    # 创建一个空的 DataFrame
    ref_item_df = pd.DataFrame(columns=['paper_title', 'paper_id', 'ref_item'])

    for index, row in df_reference.iterrows():
        if row['id']!=18:
            continue
        ref_dict = {'paper_title': row['paper_title'], 'paper_id': row['paper_id']}
        ref_txt = row['ref_txt']
        reference_items = re.compile(u'(\\[[1-9][0-9]*\\])').split(ref_txt)
        reference_items = [item.strip().replace('\n', '') for item in reference_items[1:len(reference_items)] if
                           len(item) > 5]
        ref_dict['ref_item'] = reference_items
        sub_ref_item_df = pd.DataFrame(ref_dict)
        ref_item_df = pd.concat([ref_item_df, sub_ref_item_df])

def create_df():
    data = {'a': 8, 'b': [1, 3, 4, 5, 6]}
    print(pd.DataFrame(data))


if __name__ == '__main__':
    create_df()
