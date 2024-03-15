from all_imports import *

def test1():
    print(" ### test ### ")
    print(os.getcwd())

def print_functions_folder(modules_folder='_modules', ignore_files=['__init__.py']):
    """
    Prints the functions defined in Python files within a specified folder.

    Parameters:
    -------
    modules_folder: str 
        The name of the folder containing Python files.
    ignore_files: list(str) 
        A list of filenames to ignore.

    Returns:
    -------
    - print of functions_dict
    """
    # Add the modules_folder to the Python path
    sys.path.append(os.path.abspath(modules_folder))

    functions_dict = {}

    # Iterate through files in the _modules folder
    for filename in os.listdir(modules_folder):
        if filename.endswith('.py') and filename not in ignore_files:  # Consider only Python files and not in ignore list
            module_name = filename[:-3]  # Remove the .py extension
            module = __import__(module_name)
            function_names = [name for name, obj in inspect.getmembers(module) if inspect.isfunction(obj)]
            if function_names:
                functions_dict[module_name] = function_names

    # Print using pprint
    pprint(functions_dict)


def folder_variable_setup(man_identifier=None):
    #TODO: Add all other relevant folder variables and paths
    """The following parts hold the settings for the whole notebook in order to be able to run it. Here is a brief description of the variables needed:

    Parameters
    ----------
    man_identifier : str, optional
        Identifier for the individual. If not provided, a timestamp with date and time in the following format of '2024-02-09_1300' will be used.

    Returns
    -------
    directory_paths : str
        Path for main directory of the src code used as a base for all other defined directory paths.
    directory_data_raw_path : str
        Path for the raw data directory under data.
    directory_data_processed_path : str
        Path for the processed data directory under data.
    directory_report_path : str
        Paths to the report directory.
    """
    
    current_datetime = datetime.now()

    ### Used for folder organization and reports ###
    if man_identifier is not None and man_identifier.strip():
        identifier = man_identifier
    else:
        identifier = current_datetime.strftime('%Y-%m-%d_%H%M') 
    print(identifier)

    # Directory paths
    directory_path = os.getcwd()  # Current working directory
    parent_directory_path = os.path.dirname(directory_path)
    directory_data_raw_path = os.path.join(parent_directory_path, 'data\\raw') 
    directory_data_processed_path = os.path.join(parent_directory_path, 'data\\processed')
    directory_report_path = os.path.join(parent_directory_path, 'report')
    directory_data_ws_path = os.path.join(parent_directory_path, 'data\\watch_surveys') 
    
    return directory_path, directory_data_raw_path, directory_data_processed_path, directory_report_path, identifier, directory_data_ws_path


def query_participants_data(lst_participants, YOUR_TIMEZONE, ID_EXPERIMENT, WEEKS, API_KEY):
    participant_data = {}
    for ID_PARTICIPANT in lst_participants:
        print(ID_PARTICIPANT)
        try:
            payload = {'id_participant': ID_PARTICIPANT, 'id_experiment': ID_EXPERIMENT, 'weeks': WEEKS}
            headers = {"Accept": "application/json", 'x-api-key': API_KEY}
            response = requests.get('https://bni6kdfystbmmrulxl7jxonphi0ieqvg.lambda-url.ap-southeast-1.on.aws/', params=payload, headers=headers)
            url = response.content

            with requests.get(url, stream=True) as r:
                with open('cozie.zip', 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

            with open('cozie.zip', 'rb') as f:
                df = pd.read_csv(f, compression={'method': 'zip', 'archive_name': 'sample.csv'}, low_memory=False)

            df = df.drop(columns=['Unnamed: 0'])
            df['index'] = pd.to_datetime(df['index'])
            df = df.set_index('index')
            df.index = df.index.tz_convert(YOUR_TIMEZONE)
            df.reset_index()

            # Define the file path for the CSV
            #csv_filename = f"participant_{ID_PARTICIPANT}.csv"
            #csv_path = os.path.join(output_directory, csv_filename)
            #df.to_csv(csv_path)
            #print(csv_path)

            participant_data[ID_PARTICIPANT] = df
        except Exception as e:
            print(f"Error occurred for participant {ID_PARTICIPANT}: {str(e)}")

    return participant_data
