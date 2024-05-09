from all_imports import *

# ----------------------------------------------------
# Time functions
# ----------------------------------------------------
## Calculate the time difference
# ----------------------------------------------------
#This function calculates the time difference between not NaN Data 
#in the specified column 'reference_column' and stores it into a 
#column called c_difference_time_XXXX' with XXXX being an addition 
#'identifier' that can be manually defined. 

def calculate_time_difference(dictionary: Dict, reference_column: str = 'q_general_location_envi', identifier: str = None, debug: bool = False):

    c_columnname = 'c_difference_time_ws'

    #Check if reference_column exists
    if reference_column not in dictionary[next(iter(dictionary))].columns:
        print(f"Failed: The reference column '{reference_column}' does not exist in the DataFrame.")
        return None  # Return None to indicate failure

    for participant_id, df in dictionary.items():
        if debug: print(f'Iterating now: {participant_id}')
        df[c_columnname] = None  # Initialize column with NaT
        previous_time_ws = None

        for index, row in df.iterrows():
            if pd.isna(row[reference_column]):
                continue  # Skip if reference_column is NaN

            current_time_ws = pd.to_datetime(row['index_time'])

            # Calculate time difference if previous_time_ws exists
            if previous_time_ws is not None:
                time_difference = current_time_ws - previous_time_ws
                #df.at[index, c_columnname] = time_difference #also possible but prints out a warning for non compatiabiliy for future pandas versions
                df.at[index, c_columnname]: int = int(time_difference.total_seconds()) 
            previous_time_ws = current_time_ws
            

    if debug:
        first_participant_key = next(iter(dictionary))
        print(f'Results of index_time and calculated time difference in seconds for {first_participant_key} in the dictionary, NaN values are removed for presentation')
        display(dictionary[first_participant_key][dictionary[first_participant_key][c_columnname].notna()][['index_time', 'id_participant', c_columnname]].head(10))

    return dictionary  # type: ignore # Return the modified dictionary

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
## Define Run's based on time difference
# ----------------------------------------------------

def calculate_runs_on_time_difference(dictionary: Dict, reference_time_column, min_threshold: int = 360, max_threshold: int = 1800, debug: bool = False):
    for participant_id, df in dictionary.items():
        first_ws_bool = False
        run_number = 0

        for index, row in df.iterrows():
            if pd.isna(row[reference_time_column]):
                df.loc[index, 'c_run_number'] = run_number
                continue  # Skip if reference_time_column is NaN
            
            if not first_ws_bool:
                first_ws_bool = True
                df.loc[index, 'c_run_number'] = run_number

            time_difference = df.loc[index, reference_time_column]

            if time_difference is None:
                df.loc[index, 'c_run_number'] = run_number
                continue  # Skip if c_difference_time_ws_timedelta is None
            
            if max_threshold >= time_difference >= min_threshold:
                df.loc[index, 'c_run_number'] = run_number
            else:
                run_number += 1
                df.loc[index, 'c_run_number'] = run_number
                continue

        df['c_run_number'] = df['c_run_number'].astype(int)

    if debug:
        first_participant_key = next(iter(dictionary))
        print(f'Results of index_time and calculated time difference in seconds for {first_participant_key} in the dictionary, NaN values are removed for presentation')
        display(dictionary[first_participant_key][dictionary[first_participant_key][reference_time_column].notna()][['index_time', 'id_participant', reference_time_column, 'c_run_number']].head(10))

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

