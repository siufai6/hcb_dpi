This repo contains files and code to analyse Digital Propensity Index (DPI) report based on the 2021 census.  It maps the index to Output Area (OA) classification (the profile of household in the area) and also the Urban/Rural classification.

We then filter out the areas which have higher DPI and ouputs two files, one for  Urban and one for Rural.  

Notes on mapping:
1. DPI 2021 data is based on LSOA 2011.
2. The urban/rural classification is also based on LSOA 2011, so a direct mapping using LSOA code would do.
3. The OA classification is using OA of 2021, so we need to map LSOA 2011 -> LSOA 2021 -> 2021 OA to be able to get the household classification.  

This gives a whole list of DPI with urban/rural classification and also household classification.  Next, we will filter for the areas that requires help to increase their likelihood to use digitial service.  To do this, we use interquartile range (IQR) to find out low outliers that are below Q1 − 1.5 x IQR.  The results are three files:
1. complete_list.csv contains all data
2. rural_focus_area.csv contains outliners in rural area
3. urban_focus_area.csv contains outliners in urban area

For better integration with other data based on LSOA 2021, we also mapped the DPI data to use LSOA 2021.  The code is in https://github.com/siufai6/hcb_dpi/blob/main/dpi.ipynb

Note: the LSOA21_TO_OA_MAPPING file "PCD_OA21_LSOA21_MSOA21_LAD_MAY23_UK_LU.csv" is not in the repo, please download from https://geoportal.statistics.gov.uk/datasets/ons::postcode-to-oa-2021-to-lsoa-to-msoa-to-lad-may-2023-best-fit-lookup-in-the-uk/about
