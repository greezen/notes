import pandas as pd
import csv

df = pd.read_csv("tmp/data.csv")
# 行转列
res = df.pivot_table(index=['regionid','kind'], columns='m', values='cn')
res.to_csv('tmp/res.csv')