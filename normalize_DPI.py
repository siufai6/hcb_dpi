import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from util import normalize_to_range

# normaliz DPI data to range 0-10

data = pd.read_csv("./digitalpropensityindexlsoasv3.csv")

data['score_normalized'] = normalize_to_range(data.Score)

# Round the normalized scores to 2 decimal places
data['score_normalized'] = data['score_normalized'].round(2)

# If you want to overwrite the original 'score' column instead, use:
# df['score'] = df['score_normalized']
# df = df.drop('score_normalized', axis=1)

# Print the first few rows to verify
print(data.head())

data.to_csv("./noramlized.csv")