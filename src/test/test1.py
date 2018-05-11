# df_overview.pyのテスト

import numpy as np
import pandas as pd

import sys
sys.path.append('../')
import df_overview

df = pd.read_csv('test1.csv')

ov = df_overview.df_overview(df)
colSum = ov.cols_summary()
colSum.to_csv('test1_result.csv', index=False)
