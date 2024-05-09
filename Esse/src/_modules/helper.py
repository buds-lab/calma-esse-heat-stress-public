from all_imports import *

def print_log_separator(text: str = 'Separator'):
    width = 100
    print(width * '-')
    print('{: ^{width}}'.format(text, width=width))
    print(width * '-')
    return


def find_files_in_directory(dir: str, file_ext: str = 'csv'):
    file_paths = []
    file_names = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(file_ext):
                file_paths.append(os.path.join(root, file))
                file_names.append(file)
    return file_paths, file_names

def merge_list_of_columns_in_dictionary(dictionary, list_of_columns, new_columnname: str = 'NewColumn'):
    for participant_id, df in dictionary.items():
        df[new_columnname] = np.nan  

        for index, row in df.iterrows():
            for column in list_of_columns:
                if not pd.isna(row[column]):
                    df.at[index, new_columnname] = row[column]

    return dictionary

def add_dfdata_to_participant_id_in_dictionary(df, dictionary, participant_id, selected_columns):
    # Check if participant_id already exists in the dictionary
    if participant_id not in dictionary:
        # If not, initialize an empty DataFrame for that participant_id
        dictionary[participant_id] = pd.DataFrame()
    # Add 'id_participant' column to the DataFrame
    df['participant_id'] = participant_id
    # Select the desired columns
    df_selected = df[selected_columns + ['participant_id']]

    # Concatenate the DataFrame with the existing data in the dictionary
    dictionary[participant_id] = pd.concat([dictionary[participant_id], df_selected])

    return dictionary
