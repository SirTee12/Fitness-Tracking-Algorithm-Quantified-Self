import pandas as pd
from glob import glob

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------
single_file_acc = pd.read_csv(
    "../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv")
single_file_gyr = pd.read_csv(
    "../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv")

# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------
files = glob("../../data/raw/MetaMotion/*.csv")
len(files)
# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------
data_path = "../../data/raw/MetaMotion\\"
f = files[0]

participant = f.split('-')[0].replace(data_path, '')
label = f.split('-')[1]
category = f.split('-')[2].rstrip('123')

# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------
# create empty dataframes
acc_df = pd.DataFrame()
gyr_df = pd.DataFrame()

# set the counter for the number of set
acc_set = 1
gyr_set = 1
# apply the for loop
for f in files:
    participant = f.split('-')[0].replace(data_path, '')
    label = f.split('-')[1]
    category = f.split('-')[2].rstrip('123').rstrip('_MetaWear_2019')

    # read the csv file of f
    df = pd.read_csv(f)

    # add the newly extracted features as columns
    df['participant'] = participant
    df['label'] = label
    df['category'] = category

    # append to the acc_df and gyr_df
    if 'Accelerometer' in f:
        df['set'] = acc_set
        acc_set += 1
        acc_df = pd.concat([acc_df, df])
    if 'Gyroscope' in f:
        df['set'] = gyr_set
        gyr_set += 1
        gyr_df = pd.concat([gyr_df, df])

    # print(category)

# remove the unnamed column from accelerometer and gyroscope dataframes
acc_df.dropna(axis=1, inplace=True)
gyr_df.dropna(axis=1, inplace=True)

# verify
acc_df.head()

# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------


# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------

# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
