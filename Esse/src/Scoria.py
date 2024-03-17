import subprocess
import os

#file_id example = esse08_02_Scoria_Export_2024-03-12_14-14-29

# <--- Settings --->
address = 'C:/sqlite/Library/bin'  # parent location of the sqlite3.exe
extension = '.sqlite'  # extension, usually .db or .sqlite

# <--- Code --->
while True:
    file_id = input("Enter file ID (or 'exit' to quit): ")
    if file_id.lower() == 'exit':
        break
    filename = address + '/' + file_id
    print(filename)
    # SQLite executable path
    sqlite_executable = address + '/sqlite3.exe'
    print(sqlite_executable)
    # SQLite commands
    commands = [
        ".open " + filename + ".sqlite",
        ".mode csv",
        ".headers on",
        ".once " + filename + ".csv",
        "SELECT * FROM location;",
        ".quit"
    ]

    print(os.linesep.join(commands))

    # Run the commands with elevated privileges
    subprocess.run([sqlite_executable], input='\n'.join(commands), text=True, check=True)

