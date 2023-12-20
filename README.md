# olink_data_preparation_final

Script for preparing Olink raw data for analysis (20230126_olink_data_preparation.py)

CSV files needed:

data - raw Olink NPX data with the rows corresponding to each sample and columns corresponding to each cytokine

attributes - sample information containing the matching sample ID, Dataset (Umea or Örebro), Sampling day, disease severity (Progress), and patient ID

covum_attributes - patient information containing the matching patient ID, site (Umea or Örebro), disease severity (Progress), age, sex, presence (1) or absence (0) of comorbidities and treatments

mpo_data - MPO-DNA levels with matching sample IDs


Script for finding maximum value of each cytokine, time frame, and individual (20230419_olink_max_cytokine_filter.py)
Use resulting CSV file from previous script.
