import pandas as pd

df = pd.read_excel("data/retail.xlsx")

print(df.head())
print(df.shape)

df.to_csv("data/retail.csv", index=False)

print("CSV creado correctamente")