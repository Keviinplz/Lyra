
import pandas as pd
df: pd.DataFrame = pd.read_csv('bla.csv')
df.drop('C', axis=1)
df.head()
