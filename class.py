import pandas as pd

data = {
    "Name":['Echezona', 'Blessing', 'Jennifer'],
    "score":[80, 45, 72],
}

dp = pd.DataFrame(data)
dp_head = dp.head()
dp_shape = dp.shape
dp_desc = dp.describe()

print(dp)
print(dp_head)
print(dp_shape)
print(dp_desc)