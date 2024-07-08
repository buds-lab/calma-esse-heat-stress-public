from all_imports import *

from .helper import print_log_separator
from .utilities import DisplayGroupedData

# ----------------------------------------------------
## Flag the time difference
# ----------------------------------------------------
#This function flags now the time difference in a new column based on a certain treshold.

def flag_on_int_threshold(dictionary: Dict, reference_column: str = 'c_difference_time_ws', threshold: int = 500, debug: bool = False):
    
    # Check if reference_column exists
    if reference_column not in dictionary[next(iter(dictionary))].columns:
        print(f"Failed: The reference column '{reference_column}' does not exist in the DataFrame.")
        return None  # Return None to indicate failure
    
    for participant_id, df in dictionary.items():
        if debug: print(f'Iterating now: {participant_id}')
        # Adjust the column beginning to 'flag'
        parts = reference_column.split('_')
        c_columnname = '_'.join([parts[0], 'flag', parts[1]])
        #df[c_columnname] = df[reference_column].apply(lambda x: pd.isna(x) or x > threshold)
        df[c_columnname] = df[reference_column].apply(lambda x: np.nan if pd.isna(x) else x > threshold)

    if debug:
        first_participant_key = next(iter(dictionary))
        print(f'Results for flagged items as booleans for {first_participant_key} in the dictionary, NaN values are removed for presentation')
        display(dictionary[first_participant_key][dictionary[first_participant_key][reference_column].notna()][['index_time', 'id_participant', reference_column,  c_columnname]].head(10))

    return dictionary # type: ignore

    
# ----------------------------------------------------
## Flag Step Count and determine intensity 
# ----------------------------------------------------

def calculate_step_count_intensity(dictionary, reference_step_column: str = 'ws_step_count', reference_ws_column: str = 'q_general_location_envi', reference_timediff_column: str = 'c_difference_time_ws', debug: bool = False):
    for participant_id, df in dictionary.items():
        df['c_run_changed'] = False  # Add a new column 'run_changed' with default value False
        df['c_ws_step_count'] = np.nan

        for index, row in df.iterrows():
            if not pd.isna(row[reference_ws_column]):
                df.at[index, 'c_run_changed'] = True  # Set 'c_run_changed' to True if q_general_location_envi is not NaN

        count_rows = 0
        for index, row in df.iterrows():
            if not row['c_run_changed']:
                count_rows += 1
                continue
            else:
                start_index = max(0, index - count_rows)
                end_index = index - 1
                if start_index <= end_index:
                    max_ws_step_count = df.loc[start_index:end_index, reference_step_column].max()
                    if pd.isna(max_ws_step_count):
                        df.at[index, 'c_ws_step_count'] = 0
                    else:
                        df.at[index, 'c_ws_step_count'] = max_ws_step_count
                count_rows = 0  # Reset count_rows

        df['c_ws_step_count_intensity'] = np.nan
        df['flag_ws_step_count'] = np.nan

        slow_threshold_default = 79
        medium_threshold_default = 99
        brisk_threshold_default = 119
        flag_threshold_default = 100


        for index, row in df.iterrows():
            if not pd.isna(row['c_ws_step_count']):
                if pd.notnull(row['c_difference_time_ws']):  # Check if time difference is not NaN
                    total_minutes = row['c_difference_time_ws'] / 60
                    
                    slow_threshold = slow_threshold_default * total_minutes
                    medium_threshold = medium_threshold_default * total_minutes
                    brisk_threshold = brisk_threshold_default * total_minutes
                    flag_threshold = flag_threshold_default * total_minutes

                    steps_per_minute = row['c_ws_step_count'] / total_minutes
                    # Determine intensity level
                    if steps_per_minute <= slow_threshold:
                        intensity_level = 0
                    elif steps_per_minute <= medium_threshold:
                        intensity_level = 1
                    elif steps_per_minute <= brisk_threshold:
                        intensity_level = 2
                    else:
                        intensity_level = 3

                    # Update flag_ws_step_count based on threshold
                    df.at[index, 'flag_ws_step_count'] = steps_per_minute >= flag_threshold

                    # Update c_ws_step_count_intensity
                    df.at[index, 'c_ws_step_count_intensity'] = intensity_level
            
    if debug:
        first_participant_key = next(iter(dictionary))
        print(f'Results of index_time and calculated time difference in seconds for {first_participant_key} in the dictionary, NaN values are removed for presentation')
        display(dictionary[first_participant_key][dictionary[first_participant_key][reference_ws_column].notna()][['index_time', 'id_participant', 'c_ws_step_count', 'c_difference_time_ws', 'c_ws_step_count_intensity', 'flag_ws_step_count']].head(10))


    return dictionary

# ----------------------------------------------------
## Calculate Distance
# ----------------------------------------------------
# This functions caluclates the distnace using haversine, between two location points, from one row 
# of locations points

def calculate_distances(dictionary, reference_column_latitude: str = 'c_latitude', reference_column_longitude: str = 'c_longitude', reference_distance_column: str = 'c_distance', debug: bool = False):
    for participant_id, df in dictionary.items():
        df[reference_distance_column] = np.nan  
        first_time = True

        for index, row in df.iterrows():
            #if not pd.isna(row['q_general_location_envi']):
                if first_time:
                    previous_lat  = row[reference_column_latitude]
                    previous_lon = row[reference_column_longitude]
                    first_time = False
                else:
                    current_lat = row[reference_column_latitude]
                    current_lon = row[reference_column_longitude]
                    distance = haversine_vector((previous_lat, previous_lon), (current_lat, current_lon), Unit.METERS)
                    distance = np.round(distance)  # Round distance to the nearest integer    

                    previous_lat  = row[reference_column_latitude]
                    previous_lon = row[reference_column_longitude]

                    df.at[index, reference_distance_column] = distance

    if debug:
        first_participant_key = next(iter(dictionary))
        print(f'Results of all location differences for {first_participant_key} in the dictionary for the given lat and log values, NaN values are removed for presentation')
        display(dictionary[first_participant_key][dictionary[first_participant_key][reference_distance_column].notna()][['index_time', 'id_participant', reference_column_longitude, reference_column_latitude, reference_distance_column]].head(10))

    return dictionary

# ----------------------------------------------------
## Calculate Time Differnece (NEW)
# ----------------------------------------------------
# This functions caluclates the time between the reference columns

def ComputeTimeDifference(df: pd.DataFrame, refColumn: str = 'q_general_location_envi', resultColumn: str = 'c_time_difference',
                            defaultColumns: List[str] = ['index_time'], groupbyColumn: str = 'id_participant', debug: bool = True, size: int = 5):

    print_log_separator(text = '>>> ComputeTimeDifference for [' + refColumn + '] by [' + groupbyColumn + '] to [' + resultColumn  + ']')

    missing_columns = [col for col in [refColumn, groupbyColumn] + defaultColumns if col not in df.columns]
    if missing_columns:
        print(f"Failed: The following columns are missing in the DataFrame: {missing_columns}")
        return

    df[resultColumn] = np.nan
    previous_time_ws = None
    previous_id_participant = None

    for index, row in df.iterrows():
        if pd.isna(row[refColumn]):
            continue

        current_time_ws = pd.to_datetime(row['index_time'])

        if previous_id_participant != row['id_participant']:
            previous_time_ws = current_time_ws 
            df.at[index, resultColumn] = 0
        else:
            if previous_time_ws is not None:
                time_difference = current_time_ws - previous_time_ws
                df.at[index, resultColumn] = int(time_difference.total_seconds())

        previous_id_participant = row['id_participant']
        previous_time_ws = current_time_ws 

    if debug:
        print_log_separator(text = 'Debugging')
        print(f'Results of index_time and calculated time difference in seconds, NaN values are removed for presentation')

        columns_to_display = [col for col in defaultColumns + [groupbyColumn, refColumn, resultColumn] if col in df.columns]
        filtered_df = df[df[resultColumn].notna()][columns_to_display]
        DisplayGroupedData(filtered_df, groupbyColumn, columns_to_display, 5)
    
    return df

# ----------------------------------------------------
## Calculate Runs based on time difference (NEW)
# ----------------------------------------------------
# This functions caluclates the time between the reference columns

def ComputeRunsOnTimeDifference(df: pd.DataFrame, timeColumn: str, resultColumn: str = 'c_run_number', defaultColumns: List[str] = ['index_time'], groupbyColumn: str = 'id_participant',
                                    min_threshold: float = 360, max_threshold: float = 1800, debug: bool = True, size: int = 5) -> pd.DataFrame:
    
    print_log_separator(text = '>>> ComputeRunsOnTimeDifference for [' + timeColumn + '] by [' + groupbyColumn + '] to [' + resultColumn + ']')
    
    missing_columns = [col for col in [groupbyColumn] + defaultColumns if col not in df.columns]
    if missing_columns:
        print(f"Failed: The following columns are missing in the DataFrame: {missing_columns}")
        return

    run_number = 0
    previous_id = None  # Variable to store the previous id_participant
    
    for index, row in df.iterrows():
        if pd.isna(row[timeColumn]):
            df.loc[index, resultColumn] = np.nan
            continue  # Skip if reference_time_column is NaN
        
        current_id = row[groupbyColumn]  # Get current id_participant
        
        # Reset run_number to 0 if id_participant changes
        if current_id != previous_id:
            run_number = 0
            previous_id = current_id
        
        time_difference = row[timeColumn]

        if pd.isna(time_difference):
            df.loc[index, resultColumn] = run_number
            continue  # Skip if time_difference is NaN
        
        if max_threshold >= time_difference >= min_threshold:
            df.loc[index, resultColumn] = run_number
        else:
            run_number += 1
            df.loc[index, resultColumn] = run_number

    df[resultColumn] = df[resultColumn].fillna(-1).astype(int)

    if debug:
        print('Results of index_time and calculated time difference in seconds, NaN values are removed for presentation')
        columns_to_display = [col for col in defaultColumns + [groupbyColumn, timeColumn, resultColumn] if col in df.columns]
        filtered_df = df[df['q_general_location_envi'].notna()][columns_to_display]
        DisplayGroupedData(filtered_df, groupbyColumn, columns_to_display, size)

    return df

# ----------------------------------------------------
## Calculate Runs based on time difference (NEW)
# ----------------------------------------------------
# This functions caluclates the time between the reference columns

def MarkFalseRuns(df: pd.DataFrame, debug: bool = True, size: int = 5) -> pd.DataFrame:
    # Initialize the new columns
    df['run_valid'] = False
    df['is_valid_run'] = np.nan
    df['run_amount'] = np.nan


    df.sort_values(['index_time'])
    # Group by 'id_participant' and 'c_run_number' and count the occurrences
    run_counts = df.groupby(['id_participant', 'c_run_number']).size().reset_index(name='counts')
    

    # Iterate over each participant
    for participant_id in df['id_participant'].unique():
        participant_runs = run_counts[run_counts['id_participant'] == participant_id]
        
        # Additional check for c_run_number == -1
        invalid_run_indices = df[(df['id_participant'] == participant_id) & (df['c_run_number'] == -1)].index
        df.loc[invalid_run_indices, 'is_valid_run'] = np.nan
        
        # Filter runs with counts >= 2, excluding c_run_number == -1
        valid_runs = participant_runs[(participant_runs['counts'] >= 2) & (participant_runs['c_run_number'] != -1)]
        
        # Iterate over each valid run number for the current participant
        for _, row in valid_runs.iterrows():
            run_number = row['c_run_number']
            
            # Mark valid runs in the temporary columns
            valid_run_indices = (df['id_participant'] == participant_id) & (df['c_run_number'] == run_number)
            df.loc[valid_run_indices, 'is_valid_run'] = True
            df.loc[valid_run_indices, 'run_amount'] = row['counts']

    # Propagate the validity to all indices between the first and last valid occurrence
    for participant_id in df['id_participant'].unique():
        participant_data = df[df['id_participant'] == participant_id]
        last_valid = False
        occurrences = 0
        
        for index, row in participant_data.iterrows():
            if row['is_valid_run'] == True:
                occurrences += 1
                last_valid = True
                df.loc[index, 'run_valid'] = last_valid
                # Reset validity if occurrences match the run amount
                if row['run_amount'] == occurrences:
                    last_valid = False
                    occurrences = 0
            elif pd.notna(row['is_valid_run']):
                if row['run_amount'] >= 2:
                    last_valid = True
                    df.loc[index, 'run_valid'] = last_valid
                if row['run_amount'] == occurrences:
                    last_valid = False
                    occurrences = 0
                df.loc[index, 'run_valid'] = last_valid
            elif pd.isna(row['is_valid_run']):
                df.loc[index, 'run_valid'] = last_valid
            else:
                last_valid = False
                occurrences = 0
                df.loc[index, 'run_valid'] = last_valid

    # if debug:
    #     filtered_df = df[df['q_general_location_envi'].notna()][['index_time', 'id_participant', 'q_general_location_envi', 'c_run_number', 'is_valid_run', 'run_valid', 'run_amount']]
    #     #display_grouped_data(filtered_df, 'id_participant', ['index_time', 'id_participant', 'q_general_location_envi', 'c_run_number', 'is_valid_run', 'run_valid', 'run_amount'], size)

    #     # Save the relevant columns to a CSV file
    #     df[['index_time', 'id_participant', 'q_general_location_envi', 'c_run_number', 'is_valid_run', 'run_valid', 'run_amount']].to_csv('processed_testing.csv', index=False)

    return df

# ----------------------------------------------------
## Combine Columns in a dataframe based on a priority list (NEW)
# ----------------------------------------------------
# This fucntions...

def CombineColumns(df: pd.DataFrame, columns_priority: List[str]):
    return df[columns_priority].bfill(axis=1).iloc[:, 0]