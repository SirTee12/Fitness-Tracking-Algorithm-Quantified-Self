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

# Lets look at the brief description of the data. We need to convert
# `epoch (ms)` and `time (01:00)` too timestamp data type.
# the epoch column is in unix scale. it shows the number of milliseconds
# that have elapsed since `January 1, 1970 at 00:00 UTC.`
acc_df.info()


# verify

# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------
# convert the epoch feature to datetime and set as index
acc_df.index = pd.to_datetime(acc_df['epoch (ms)'], unit='ms')
gyr_df.index = pd.to_datetime(gyr_df['time (01:00)'])

# remove the epoch and time column
acc_df.drop(['epoch (ms)', 'time (01:00)'], axis=1, inplace=True)
gyr_df.drop(['epoch (ms)', 'time (01:00)'], axis=1, inplace=True)


# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------
# lets turn everything into a function
def read_data_from_files(files):
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
    # drop the NaN columns
    acc_df.dropna(axis=1, inplace=True)
    gyr_df.dropna(axis=1, inplace=True)

    # convert the epoch feature to datetime and set as index
    acc_df.index = pd.to_datetime(acc_df['epoch (ms)'], unit='ms')
    gyr_df.index = pd.to_datetime(gyr_df['time (01:00)'])

    # remove the epoch and time column
    acc_df.drop(['epoch (ms)', 'time (01:00)', 'elapsed (s)'],
                axis=1, inplace=True)
    gyr_df.drop(['epoch (ms)', 'time (01:00)', 'elapsed (s)'],
                axis=1, inplace=True)

    return acc_df, gyr_df


# Apply the function to extract the file data
acc_df, gyr_df = read_data_from_files(files)


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------
data_merged = pd.merge(
    acc_df.iloc[:, :3], gyr_df, how='outer', left_index=True, right_index=True)

# rename columns
data_merged.columns = ['acc_x', 'acc_y', 'acc_z', 'gyr_x',
                       'gyr_y', 'gyr_z', 'participant', 'label', 'category', 'set']


# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# create a resampling rule for each column
sampling = {'acc_x': 'mean', 'acc_y': 'mean', 'acc_z': 'mean', 'gyr_x': 'mean', 'gyr_y': 'mean',
            'gyr_z': 'mean', 'participan': 'last', 'label': 'last', 'category': 'last', 'set': 'last'}

# split data into days
days = [g for n, g in data_merged.groupby(pd.Grouper(freq='D'))]
# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
