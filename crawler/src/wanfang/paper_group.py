# coding=utf-8
# date:下午4:34
# author:chenjunbiao
import pandas as pd
from pathlib import Path
import shutil


def get_paper_type_map():
    paper_type_map = {}
    reference_df = pd.read_csv(str(
        Path.home().joinpath('paper_C_D_reference_formatted.csv')))
    for index, row in reference_df.iterrows():
        paper_type_map[row['title']] = row['type']
    return paper_type_map


def group_paper(paper_dir, title_type_map):
    paper_path = Path(paper_dir)
    for a in paper_path.iterdir():
        if not a.is_dir():
            continue
        print('========================')
        for b in a.iterdir():
            # if not b.is_dir():
            #     continue
            print(b.stem)


if __name__ == '__main__':
    paper_type_map = get_paper_type_map()
    d_path = Path.home().joinpath('d_ref')
    c_path = Path.home().joinpath('c_ref')
    j_path = Path.home().joinpath('j_ref')
    if not d_path.exists():
        d_path.mkdir()
    if not c_path.exists():
        c_path.mkdir()
    if not j_path.exists():
        j_path.mkdir()

    paper_path = Path.home().joinpath('cnki')
    for a in paper_path.iterdir():
        d_paper_path = d_path.joinpath(a.stem)
        c_paper_path = c_path.joinpath(a.stem)
        j_paper_path = j_path.joinpath(a.stem)
        if not d_paper_path.exists():
            d_paper_path.mkdir()
        if not c_paper_path.exists():
            c_paper_path.mkdir()
        if not j_paper_path.exists():
            j_paper_path.mkdir()

        for b in a.iterdir():
            print(b.stem)
            paper_type = paper_type_map[b.stem]
            if paper_type == 'D':
                shutil.move(str(b), str(d_paper_path))
            if paper_type == 'C':
                shutil.move(str(b), str(c_paper_path))
            if paper_type == 'J':
                shutil.move(str(b), str(j_paper_path))
