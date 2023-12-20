# can type in the python console `help(name of function)` to get the documentation
from pydoc import help
import pandas as pd
import numpy as np
#import itertools
#from IPython.display import display, HTML
#import math
from datetime import datetime

np.set_printoptions(suppress=True)

DISPLAY_MAX_ROWS = 20  # number of max rows to print for a DataFrame
pd.set_option('display.max_rows', DISPLAY_MAX_ROWS)

# Define functions used

# Append patient data to cytokine data


def append_attributes_new_categories(givendata, dataattributes, additionalattributes, mpodata):
    # Create empty dataframe to append
    add_data = pd.DataFrame(
        columns=["Sample", "Dataset", "Day", "Progress", "PatientID", "Phase", "MPO-DNA", "Age", "Sex", "Diabetes", "Hypertension", "Coronary heart disease", "Chronic lung disorder", "Asthma", "Automimmune disease", "Cancer", "Dementia", "Beta blocker", "ACE inhib or ARB", "Antidiabetic treatment", "Immunomodulatory treatment", "Corticosteroids"])

    for ind in givendata.index:
        currentattribute = dataattributes.loc[dataattributes.Sample.astype(
            str) == str(givendata.Sample[ind])]
        currentMPO = mpodata.loc[mpodata.SampleID.astype(
            str) == str(givendata.Sample[ind])]
        covumattribute = additionalattributes.loc[additionalattributes.PatientID.astype(
            str) == str(currentattribute.PatientID.iloc[0])]
        currentattribute.Progress.iloc[0] = covumattribute.Progress.iloc[0]
        covumattribute = covumattribute.loc[:,  ~covumattribute.columns.isin(
            ['Progress', 'site', 'PatientID'])]

        phase = ""

        if not dataattributes.loc[dataattributes.Sample.astype(
                str) == str(givendata.Sample[ind])].empty:
            if (currentattribute["Day"].item() <= 30):
                phase = pd.Series(["1-30d"], name="Phase")
            elif (currentattribute["Day"].item() <= 90):
                phase = pd.Series(["1-90d"], name="Phase")
            elif (currentattribute["Day"].item() > 90 and currentattribute["Day"].item() <= 180):
                phase = pd.Series(["91-180d"], name="Phase")
            elif (currentattribute["Day"].item() > 180):
                phase = pd.Series([">180d"], name="Phase")

            currentattribute.reset_index(drop=True, inplace=True)
            covumattribute.reset_index(drop=True, inplace=True)
            mposeries = pd.Series(currentMPO["MPO-DNA"].iloc[0], name="MPO-DNA")

            currentattribute = pd.concat(
                [currentattribute, phase, mposeries, covumattribute], axis=1)

        if dataattributes.loc[dataattributes.Sample.astype(
                str) == str(givendata.Sample[ind])].empty:
            print(givendata.Sample[ind])
            add_data = pd.concat([add_data, pd.DataFrame(
                [[np.NaN]*15], columns=add_data.columns)], ignore_index=True)
        else:
            add_data = add_data.append(currentattribute, ignore_index=True)
    return(add_data)


# LOAD DATA
data = pd.read_csv(
    "C:/umea_immunology/PROJECTS/corona/olink_data/formatted_data/20201969_Forsell_NPX_edit.csv")
IL33data = pd.read_csv(
    "C:/umea_immunology/PROJECTS/corona/olink_data/formatted_data/20230224_IL33_olink.csv")
attributes = pd.read_csv(
    "C:/umea_immunology/PROJECTS/corona/olink_data/formatted_data/olink_sample_names.csv")
covum_attributes = pd.read_csv(
    "C:/umea_immunology/PROJECTS/corona/olink_data/formatted_data/20211116_olink_cohort_orebro_formatted.csv")
covum_attributes = covum_attributes.fillna(0)

mpo_data = pd.read_csv(
    "C:/umea_immunology/PROJECTS/corona/olink_data/formatted_data/20221118_olink_COVID_complete_MPODNA.csv")

attributes.columns = attributes.columns.str.strip()  # get rid of whitespace in columns
covum_attributes.columns = covum_attributes.columns.str.strip()  # get rid of whitespace in columns

print("Data loaded.")

# Append sample attributes to the right sample ID with new disease progress COVUM

additionaldata = append_attributes_new_categories(data, attributes, covum_attributes, mpo_data)

# Append additionaldata to data, in order to add attributes to the corresponding samples
#print("TAIL:\n", additionaldata.tail())
#print(additionaldata["Phase"].unique())
additionaldata = additionaldata.reset_index(drop=True)

complete_data = pd.concat([data, additionaldata.drop("Sample", axis=1)],
                          axis=1)

print("Information appended.")

#print(complete_data.head())

# Save complete covum data to new csv file

complete_data.to_csv(
    "C:/umea_immunology/PROJECTS/corona/olink_data/formatted_data/" + datetime.today().strftime("%Y%m%d") + "_Forsell_NPX_edit_complete.csv", index=False)

print("File saved.")
