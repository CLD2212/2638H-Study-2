"""
Created on Tue Aug 22 11:13:44 2023
Updated on Wed Aug 23 10:09:00 2023

@author: cleed
"""


import pandas as pd
import os
import scipy.signal as sp

#%% Step 1: Data Import

# a. Identify File Paths
folder_path = "C:\\Users\\cleed\\OneDrive\\Desktop\\Participant 1\\Session 1\\Pre\\TMS\\10\\Ecc"
all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# b. Load the Data & c. Parse Filenames
data_list = []
for file in all_files:
    filename = os.path.basename(file).split('.')[0]
    
    # Load the data skipping the first 23 rows
    df = pd.read_csv(file, skiprows=23)

    # Parse the filename and add the information as columns
    parts = filename.split('_')
    
    participant_no = parts[0]
    test_type = parts[1].split()[0]
    stim_intensity = parts[1].split()[1] if len(parts[1].split()) > 1 else None
    stim_no = parts[2]

    df['Participant'] = participant_no
    df['Test Type'] = test_type
    df['Stimulation Intensity'] = stim_intensity
    df['Stimulation Number'] = stim_no
    
    data_list.append(df)

# d. Combine Data
all_data = pd.concat(data_list, ignore_index=True)

#%% Step 2: Filters (Butterworth, rmsEMG and Position) 

# Build butterworth filter
high = 13 / (1000 / 2)
low = 499 / (1000 / 2)
b, a = sp.butter(4, [high, low], btype='bandpass', analog=False)

# Apply the filter
all_data['BF EMG (Filtered)'] = sp.filtfilt(b, a, all_data['BF EMG (Trigger)'])

# Filtering the dataframe based on 'Position (Trigger)'
all_data = all_data[(all_data['Postition (Trigger)'] >= 27) & (all_data['Postition (Trigger)'] <= 33)]

# Position filer
start_indices = all_data[all_data['Postition (Trigger)'] == 27].index

# List of indices to drop
to_drop = []

for start in start_indices:
    rms_value = all_data.at[start, 'BF max rmsEMG (Trigger)']
    if not (0.7 <= rms_value <= 1.3):
        # If the rmsEMG is outside of the range, collect indices for the entire repetition
        to_drop.extend(range(start, start + len(all_data[(all_data['Postition (Trigger)'] >= 27) & (all_data['Postition (Trigger)'] <= 33)])))

# Drop the collected indices
all_data.drop(to_drop, inplace=True)

#%% Initial Analysis

# Group by 'Test Type' and then aggregate
agg_data_pre = all_data.groupby('Test Type')['BF EMG (Filtered)'].agg(['mean', 'std'])

#%% Step 3: Import MVC Data and Get Max Torque

mvc_folder_path = "C:\\Users\\cleed\\OneDrive\\Desktop\\Participant 1\\Session 1\\Pre\\Strength"
mvc_files = [os.path.join(mvc_folder_path, f) for f in os.listdir(mvc_folder_path) if os.path.isfile(os.path.join(mvc_folder_path, f)) and "Hamstring_MVC" in f]

max_torques = []

for file in mvc_files:
    # Load the torque data skipping the first 23 rows
    df_mvc = pd.read_csv(file, skiprows=23)
    max_torque = df_mvc['Torque'].max()
    max_torques.append(max_torque)

# Get the maximum torque value from all MVC tests
max_torque_value = max(max_torques)

#%% Step 4: Normalize AMT data

# Filtering out the rows where Test Type is "AMT"
amt_rows = agg_data_pre.loc['AMT']

# Normalize the mean and standard deviation values for AMT
amt_rows['AMT_Norm'] = amt_rows['mean'] / max_torque_value
amt_rows['AMT_SD_Norm'] = amt_rows['std'] / max_torque_value 

agg_data_pre.loc['AMT', 'mean_norm'] = amt_rows['AMT_Norm']
agg_data_pre.loc['AMT', 'std_norm'] = amt_rows['AMT_SD_Norm']

#%% Repeat for Post
#%% Step 1: Data Import

# a. Identify File Paths
folder_path = "C:\\Users\\cleed\\OneDrive\\Desktop\\Participant 1\\Session 1\\Post\\TMS\\10\\Ecc"
all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# b. Load the Data & c. Parse Filenames
data_list = []
for file in all_files:
    filename = os.path.basename(file).split('.')[0]
    
    # Load the data skipping the first 23 rows
    df = pd.read_csv(file, skiprows=23)

    # Parse the filename and add the information as columns
    parts = filename.split('_')
    
    participant_no = parts[0]
    test_type = parts[1].split()[0]
    stim_intensity = parts[1].split()[1] if len(parts[1].split()) > 1 else None
    stim_no = parts[2]

    df['Participant'] = participant_no
    df['Test Type'] = test_type
    df['Stimulation Intensity'] = stim_intensity
    df['Stimulation Number'] = stim_no
    
    data_list.append(df)

# d. Combine Data
all_data = pd.concat(data_list, ignore_index=True)

#%% Step 2: Filters (Butterworth, rmsEMG and Position) 

# Build butterworth filter
high = 13 / (1000 / 2)
low = 499 / (1000 / 2)
b, a = sp.butter(4, [high, low], btype='bandpass', analog=False)

# Apply the filter
all_data['BF EMG (Filtered)'] = sp.filtfilt(b, a, all_data['BF EMG (Trigger)'])

# Filtering the dataframe based on 'Position (Trigger)'
all_data = all_data[(all_data['Postition (Trigger)'] >= 27) & (all_data['Postition (Trigger)'] <= 33)]

# Position filer
start_indices = all_data[all_data['Postition (Trigger)'] == 27].index

# List of indices to drop
to_drop = []

for start in start_indices:
    rms_value = all_data.at[start, 'BF max rmsEMG (Trigger)']
    if not (0.7 <= rms_value <= 1.3):
        # If the rmsEMG is outside of the range, collect indices for the entire repetition
        to_drop.extend(range(start, start + len(all_data[(all_data['Postition (Trigger)'] >= 27) & (all_data['Postition (Trigger)'] <= 33)])))

# Drop the collected indices
all_data.drop(to_drop, inplace=True)

#%% Initial Analysis

# Group by 'Test Type' and then aggregate
agg_data_post = all_data.groupby('Test Type')['BF EMG (Filtered)'].agg(['mean', 'std'])

#%% Step 3: Import MVC Data and Get Max Torque

mvc_folder_path = "C:\\Users\\cleed\\OneDrive\\Desktop\\Participant 1\\Session 1\\Pre\\Strength"
mvc_files = [os.path.join(mvc_folder_path, f) for f in os.listdir(mvc_folder_path) if os.path.isfile(os.path.join(mvc_folder_path, f)) and "Hamstring_MVC" in f]

max_torques = []

for file in mvc_files:
    # Load the torque data skipping the first 23 rows
    df_mvc = pd.read_csv(file, skiprows=23)
    max_torque = df_mvc['Torque'].max()
    max_torques.append(max_torque)

# Get the maximum torque value from all MVC tests
max_torque_value = max(max_torques)

#%% Step 4: Normalize AMT data

# Filtering out the rows where Test Type is "AMT"
amt_rows = agg_data_post.loc['AMT']

# Normalize the mean and standard deviation values for AMT
amt_rows['AMT_Norm'] = amt_rows['mean'] / max_torque_value
amt_rows['AMT_SD_Norm'] = amt_rows['std'] / max_torque_value 

agg_data_post.loc['AMT', 'mean_norm'] = amt_rows['AMT_Norm']
agg_data_post.loc['AMT', 'std_norm'] = amt_rows['AMT_SD_Norm']

#%% Repeat for Post30
#%% Step 1: Data Import

# a. Identify File Paths
folder_path = "C:\\Users\\cleed\\OneDrive\\Desktop\\Participant 1\\Session 1\\Post30\\TMS\\10\\Ecc"
all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# b. Load the Data & c. Parse Filenames
data_list = []
for file in all_files:
    filename = os.path.basename(file).split('.')[0]
    
    # Load the data skipping the first 23 rows
    df = pd.read_csv(file, skiprows=23)

    # Parse the filename and add the information as columns
    parts = filename.split('_')
    
    participant_no = parts[0]
    test_type = parts[1].split()[0]
    stim_intensity = parts[1].split()[1] if len(parts[1].split()) > 1 else None
    stim_no = parts[2]

    df['Participant'] = participant_no
    df['Test Type'] = test_type
    df['Stimulation Intensity'] = stim_intensity
    df['Stimulation Number'] = stim_no
    
    data_list.append(df)

# d. Combine Data
all_data = pd.concat(data_list, ignore_index=True)

#%% Step 2: Filters (Butterworth, rmsEMG and Position) 

# Build butterworth filter
high = 13 / (1000 / 2)
low = 499 / (1000 / 2)
b, a = sp.butter(4, [high, low], btype='bandpass', analog=False)

# Apply the filter
all_data['BF EMG (Filtered)'] = sp.filtfilt(b, a, all_data['BF EMG (Trigger)'])

# Filtering the dataframe based on 'Position (Trigger)'
all_data = all_data[(all_data['Postition (Trigger)'] >= 27) & (all_data['Postition (Trigger)'] <= 33)]

# Position filer
start_indices = all_data[all_data['Postition (Trigger)'] == 27].index

# List of indices to drop
to_drop = []

for start in start_indices:
    rms_value = all_data.at[start, 'BF max rmsEMG (Trigger)']
    if not (0.7 <= rms_value <= 1.3):
        # If the rmsEMG is outside of the range, collect indices for the entire repetition
        to_drop.extend(range(start, start + len(all_data[(all_data['Postition (Trigger)'] >= 27) & (all_data['Postition (Trigger)'] <= 33)])))

# Drop the collected indices
all_data.drop(to_drop, inplace=True)

#%% Initial Analysis

# Group by 'Test Type' and then aggregate
agg_data_post30 = all_data.groupby('Test Type')['BF EMG (Filtered)'].agg(['mean', 'std'])

#%% Step 3: Import MVC Data and Get Max Torque

mvc_folder_path = "C:\\Users\\cleed\\OneDrive\\Desktop\\Participant 1\\Session 1\\Pre\\Strength"
mvc_files = [os.path.join(mvc_folder_path, f) for f in os.listdir(mvc_folder_path) if os.path.isfile(os.path.join(mvc_folder_path, f)) and "Hamstring_MVC" in f]

max_torques = []

for file in mvc_files:
    # Load the torque data skipping the first 23 rows
    df_mvc = pd.read_csv(file, skiprows=23)
    max_torque = df_mvc['Torque'].max()
    max_torques.append(max_torque)

# Get the maximum torque value from all MVC tests
max_torque_value = max(max_torques)

#%% Step 4: Normalize AMT data

# Filtering out the rows where Test Type is "AMT"
amt_rows = agg_data_post30.loc['AMT']

# Normalize the mean and standard deviation values for AMT
amt_rows['AMT_Norm'] = amt_rows['mean'] / max_torque_value
amt_rows['AMT_SD_Norm'] = amt_rows['std'] / max_torque_value 

agg_data_post30.loc['AMT', 'mean_norm'] = amt_rows['AMT_Norm']
agg_data_post30.loc['AMT', 'std_norm'] = amt_rows['AMT_SD_Norm']

#%% Repeat for Post60
#%% Step 1: Data Import

# a. Identify File Paths
folder_path = "C:\\Users\\cleed\\OneDrive\\Desktop\\Participant 1\\Session 1\\Post\\TMS\\10\\Ecc"
all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# b. Load the Data & c. Parse Filenames
data_list = []
for file in all_files:
    filename = os.path.basename(file).split('.')[0]
    
    # Load the data skipping the first 23 rows
    df = pd.read_csv(file, skiprows=23)

    # Parse the filename and add the information as columns
    parts = filename.split('_')
    
    participant_no = parts[0]
    test_type = parts[1].split()[0]
    stim_intensity = parts[1].split()[1] if len(parts[1].split()) > 1 else None
    stim_no = parts[2]

    df['Participant'] = participant_no
    df['Test Type'] = test_type
    df['Stimulation Intensity'] = stim_intensity
    df['Stimulation Number'] = stim_no
    
    data_list.append(df)

# d. Combine Data
all_data = pd.concat(data_list, ignore_index=True)

#%% Step 2: Filters (Butterworth, rmsEMG and Position) 

# Build butterworth filter
high = 13 / (1000 / 2)
low = 499 / (1000 / 2)
b, a = sp.butter(4, [high, low], btype='bandpass', analog=False)

# Apply the filter
all_data['BF EMG (Filtered)'] = sp.filtfilt(b, a, all_data['BF EMG (Trigger)'])

# Filtering the dataframe based on 'Position (Trigger)'
all_data = all_data[(all_data['Postition (Trigger)'] >= 27) & (all_data['Postition (Trigger)'] <= 33)]

# Position filer
start_indices = all_data[all_data['Postition (Trigger)'] == 27].index

# List of indices to drop
to_drop = []

for start in start_indices:
    rms_value = all_data.at[start, 'BF max rmsEMG (Trigger)']
    if not (0.7 <= rms_value <= 1.3):
        # If the rmsEMG is outside of the range, collect indices for the entire repetition
        to_drop.extend(range(start, start + len(all_data[(all_data['Postition (Trigger)'] >= 27) & (all_data['Postition (Trigger)'] <= 33)])))

# Drop the collected indices
all_data.drop(to_drop, inplace=True)

#%% Initial Analysis

# Group by 'Test Type' and then aggregate
agg_data_post60 = all_data.groupby('Test Type')['BF EMG (Filtered)'].agg(['mean', 'std'])

#%% Step 3: Import MVC Data and Get Max Torque

mvc_folder_path = "C:\\Users\\cleed\\OneDrive\\Desktop\\Participant 1\\Session 1\\Pre\\Strength"
mvc_files = [os.path.join(mvc_folder_path, f) for f in os.listdir(mvc_folder_path) if os.path.isfile(os.path.join(mvc_folder_path, f)) and "Hamstring_MVC" in f]

max_torques = []

for file in mvc_files:
    # Load the torque data skipping the first 23 rows
    df_mvc = pd.read_csv(file, skiprows=23)
    max_torque = df_mvc['Torque'].max()
    max_torques.append(max_torque)

# Get the maximum torque value from all MVC tests
max_torque_value = max(max_torques)

#%% Step 4: Normalize AMT data

# Filtering out the rows where Test Type is "AMT"
amt_rows = agg_data_post60.loc['AMT']

# Normalize the mean and standard deviation values for AMT
amt_rows['AMT_Norm'] = amt_rows['mean'] / max_torque_value
amt_rows['AMT_SD_Norm'] = amt_rows['std'] / max_torque_value 

agg_data_post60.loc['AMT', 'mean_norm'] = amt_rows['AMT_Norm']
agg_data_post60.loc['AMT', 'std_norm'] = amt_rows['AMT_SD_Norm']

#%% Group Data and Export

participant_1_S1_output = pd.concat([agg_data_pre, agg_data_post, agg_data_post30, agg_data_post60], axis=1, keys=['Pre', 'Post', 'Post30', 'Post60'])
participant_1_S1_output.to_excel("Participant 1 S1 Output.xlsx")

print(participant_1_S1_output)


