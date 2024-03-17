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