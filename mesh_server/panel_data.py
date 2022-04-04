import pandas as pd
import numpy as np
rng = pd.date_range('1/1/2014',periods=100,freq='D')

# 乱数でデータフレームを作っていく、インデックスは ABCD とする
df1 = pd.DataFrame(np.random.randn(100, 4), index = rng, columns = ['A','B','C','D'])
df2 = pd.DataFrame(np.random.randn(100, 4), index = rng, columns = ['A','B','C','D'])
df3 = pd.DataFrame(np.random.randn(100, 4), index = rng, columns = ['A','B','C','D'])

# これらデータフレームをまとめて Panel オブジェクトをつくる
pf = pd.Panel({'df1':df1,'df2':df2,'df3':df3})

print(pf)