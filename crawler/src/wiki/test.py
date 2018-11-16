# _*_ coding:utf-8 _*_

import pandas as pd

if __name__ == '__main__':
    with open("figure_relation.csv") as f:
        lines = f.readlines()
    hh = []
    for line in lines:
        line_array = line.strip().split(',')
        hh.append([line_array[0], line_array[1]])
    df = pd.DataFrame(hh)
    # df = pd.read_csv("figure_relation.csv")
    df.to_excel("figure_relation.xlsx")
