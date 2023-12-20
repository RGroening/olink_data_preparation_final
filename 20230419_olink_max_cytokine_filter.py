# can type in the python console `help(name of function)` to get the documentation
from pydoc import help
import pandas as pd
import numpy as np
from datetime import datetime

np.set_printoptions(suppress=True)

DISPLAY_MAX_ROWS = 20  # number of max rows to print for a DataFrame
pd.set_option('display.max_rows', DISPLAY_MAX_ROWS)

# Define functions used
# Filter max cytokine value for each cytokine separately of each unique patient in each unique phase

def filter_max(givendata):
    # Create empty dataframe to append 
    filtered_data = pd.DataFrame(columns=givendata.columns)
   
    phases = np.unique(givendata["Phase"])

    for onephase in phases:
        onephaseframe = givendata.loc[givendata["Phase"] == onephase]
        patients = np.unique(onephaseframe["PatientID"])
        for onepatient in patients:
            onepatientframe = onephaseframe.loc[onephaseframe["PatientID"] == onepatient]
            current_max = onepatientframe.max()
            filtered_data = filtered_data.append(current_max, ignore_index=True)
    return(filtered_data)


# LOAD DATA
data = pd.read_csv(
    "C:/umea_immunology/PROJECTS/corona/olink_data/formatted_data/20231211_Forsell_NPX_edit_complete.csv")

print("Data loaded.")


# Filter data

filtered_data = filter_max(data)

print("Data filtered.")

# Save data

filtered_data = filtered_data.reset_index(drop=True)

filtered_data.to_csv(
    "C:/umea_immunology/PROJECTS/corona/olink_data/formatted_data/" + datetime.today().strftime("%Y%m%d") + "_Forsell_NPX_edit_complete_filtered_max.csv", index=False)

print("File saved.")

