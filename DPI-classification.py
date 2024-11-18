import pandas as pd

# DPI is LSOA 2011 data
# first map to LSOA 2021.
# then look up OA from LSOA (many to 1) 
# then decode the name of the groups
DPI_FILE='./DPI_noramlized-python.csv'
LSOA11_TO_21_MAPPING="./LSOA_(2011)_to_LSOA_(2021)_to_Local_Authority_District_(2022)_Lookup_for_England_and_Wales.csv"
LSOA21_TO_OA_MAPPING="./PCD_OA21_LSOA21_MSOA21_LAD_MAY23_UK_LU.csv"
OA_CLASSIFICATION="./oac21ew.csv"
CLASS_CODE_NAME="./classification_codes_and_names.csv"
URBAN_RURAL_CLASSIFICATION_2011="./Rural_Urban_Classification_(2011)_of_Lower_Layer_Super_Output_Areas_in_England_and_Wales.csv"

print("--- reading DPI file")
df1 = pd.read_csv(DPI_FILE,encoding='ISO-8859-1') 
print(df1)
df2 = pd.read_csv(LSOA11_TO_21_MAPPING,encoding='ISO-8859-1') 
df2.rename(columns={df2.columns[0]: 'LSOA11CD'}, inplace=True)


print(df2)
print("--- Map 2011 LSOA to 2021 LSOA")
df2=df2[['LSOA11CD', 'LSOA21CD']]
# Map 2011 LSOA to 2021 LSOA
merged_df = pd.merge(df1, df2, left_on='LSOAcode', right_on='LSOA11CD')


print("--- Map 2021 LSOA to 2021 OA")
df3 = pd.read_csv(LSOA21_TO_OA_MAPPING,encoding='ISO-8859-1') 
df3=df3[['oa21cd','lsoa21cd']]
# Map 2021 LSOA to 2021 OA 
#result_df = merged_df.drop(columns=['D'], errors='ignore')  # Use errors='ignore' to avoid errors if 'D' doesn't exist

merged_df = pd.merge(merged_df,df3, left_on='LSOA21CD', right_on='lsoa21cd')

print(merged_df)
print("--- Map 2021 OA classification at OA level")

df4 = pd.read_csv(OA_CLASSIFICATION)
df4=df4[['oa21cd','subgroup']]
# Map 2021 OA classification at OA level
merged_df = pd.merge(merged_df,df4, left_on='oa21cd', right_on='oa21cd')

print(merged_df)
print("--- Map classification code to get the  names")

df5=pd.read_csv(CLASS_CODE_NAME)
df5=df5[['Classification Code','Classification Name']]
# map the classification code to get the classification names
merged_df = pd.merge(merged_df,df5, left_on='subgroup', right_on='Classification Code')

print(merged_df)

merged_df=merged_df[['LSOA11CD','Region','Local Authority name','Score','score_normalized','LSOA21CD','oa21cd','Classification Name']]

print("--- Map urban/rural classification")

# map the urban/rural classification (latest data is as of 2011)
df6=pd.read_csv(URBAN_RURAL_CLASSIFICATION_2011)
df6=df6[['LSOA11CD','RUC11']]
# map the classification code to get the classification names
merged_df = pd.merge(merged_df,df6, left_on='LSOA11CD', right_on='LSOA11CD')

merged_df.rename(columns={'RUC11': 'Urban Rural Classification'}, inplace=True)


# Write the resulting DataFrame into a new CSV
merged_df.to_csv('complete_list.csv', index=False)  # Replace 'result.csv' with your desired output file name


mean = merged_df['score_normalized'].mean()
std_dev = merged_df['score_normalized'].std()

### Interquartile Range (IQR):
### Calculate the IQR (Q3 - Q1) and define lower scores as those below Q1 - 1.5 * IQR. 
Q1 = merged_df['score_normalized'].quantile(0.25)
Q3 = merged_df['score_normalized'].quantile(0.75)
IQR = Q3 - Q1
lower_threshold = Q1 - 1.5 * IQR
lower_scores = merged_df[merged_df['score_normalized'] < lower_threshold]

urban_lower_scores = lower_scores[lower_scores['Urban Rural Classification'].str.contains('Urban', case=False, na=False)]
rural_lower_scores = lower_scores[lower_scores['Urban Rural Classification'].str.contains('Rural', case=False, na=False)]

#merged_df['z_score'] = (merged_df['score_normalized'] - mean) / std_dev
#lower_scores = merged_df[merged_df['z_score'] < -1]

urban_lower_scores.to_csv('urban_focus_area.csv')
rural_lower_scores.to_csv('rural_focus_area.csv')
#print(merged_df['z_score'])



print("Data processing complete. Result saved.")