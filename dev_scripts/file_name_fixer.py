# This script attempts to remove all defined special characters from file names in a given folder recursively
# It also attempts to remove emojis from file names

# Run this script from the folder you want to rename files in

# Example Usage
# cd /path/to/folder/with/files/to/rename
# python3 python file_name_fixer.py

import os
from colorama import Fore
import re

# Use Current Directory
print("""
{}Example Usage: 
{}
$ python3 file_name_fixer.py
Enter Folder Path: /home/user/Downloads/

{}ok... now starting...
""".format(Fore.YELLOW, Fore.WHITE, Fore.GREEN))

folder = input("{}Enter Folder Path Here: {}".format(Fore.WHITE, Fore.BLUE)) 

# Run the whole thing x number of times just to be sure
checks_2_run = 1

# ultimately replace all special characters with an underscore
replacement_char = "_"


# Define Special Characters
special_chars = "\"'!@#$%^&*()[]\{\};:,/<>?\\|`~-=+"

# Define Extra Special Characters (really just substrings)
xtra_special_chars = (" ", "..", "__")

# Customize replacements for specific substrings
xtra_xtra_special_chars = ("39", "_.", "_mp4", "_pdf", "_py", "_md", "_html", "_css", "_json", "_toml", "_js", "_scss", "_png", "_jpg", "_jpeg", "_txt")
xtra_xtra_special_chars_dict = {
    "39": "", 
    "_.": ".", 
    "_mp4": ".mp4", 
    "_pdf": ".pdf", 
    "_py": ".py", 
    "_md": ".md", 
    "_html": ".html", 
    "_css": ".css", 
    "_json": ".json", 
    "_toml": ".toml", 
    "_js": ".js", 
    "_scss": ".scss", 
    "_png": ".png", 
    "_jpg": ".jpg", 
    "_jpeg": ".jpeg", 
    "_txt": ".txt"}


# Characters that you don't want starting a file name
startswith_chars = [replacement_char]
for char in special_chars:
    startswith_chars.append(char)
for char in xtra_special_chars:
    startswith_chars.append(char)


# start with 0 matches
num_file_matches = 0


def get_num_file_matches(folder_path, old):
    num = 0
    for path, subdirs, files in os.walk(folder_path):
        for name in files:
            if(old.lower() in name.lower()):
                num += 1
    return num

def fix_startswith(rep_char):
    for path, subdirs, files in os.walk(folder):
        for name in files:
            if name.startswith(rep_char):
                file_path = os.path.join(path,name)
                new_name = os.path.join(path,name.replace(rep_char, "", 1))
                print(Fore.YELLOW + "[+]" + Fore.GREEN + "Renaming: " + Fore.BLUE + file_path)
                print("   " + Fore.GREEN + "To: " + Fore.BLUE + new_name + "\n")
                os.rename(file_path, new_name)

def handle_emojis():
    print(Fore.YELLOW + "\n Searching For Emojis ...\n")

    emoji_pattern = re.compile("["
        u"\U0001F000-\U0001FFFF" # lol just nuke it all
        "]+", flags=re.UNICODE)

    for path, subdirs, files in os.walk(folder):
        for name in files:
            if name.lower() != emoji_pattern.sub(r'', name.lower()):
                file_path = os.path.join(path,name)
                new_file_name = emoji_pattern.sub(r'', name.lower())
                new_name = os.path.join(path,new_file_name)
                print(Fore.YELLOW + "[+]" + Fore.GREEN + "Renaming: " + Fore.BLUE + file_path)
                print("   " + Fore.GREEN + "To: " + Fore.BLUE + new_name + "\n")
                os.rename(file_path, new_name)

def replace(folder_path, old, new, t_int):
    curr_int = 1
    for path, subdirs, files in os.walk(folder_path):
        for name in files:
            if(old.lower() in name.lower()):
                file_path = os.path.join(path,name)
                new_name = os.path.join(path,name.lower().replace(old,new))
        

                print(Fore.YELLOW + "[{}\{}] ".format(curr_int, t_int) + Fore.GREEN + "Renaming: " + Fore.BLUE + file_path)
                space_chars = len("[{}\{}] ".format(curr_int, t_int) )
                space_string = " " * space_chars
                print(Fore.GREEN + space_string + "To: " + Fore.BLUE + new_name + "\n")

                os.rename(file_path, new_name)

                curr_int += 1

def print_found(num_file_matches, char):
    if char == " ":
        print(Fore.YELLOW + "[-]" + Fore.WHITE + " Found " + Fore.RED + str(num_file_matches) + Fore.WHITE + " files with ... " + Fore.RED + "space" + Fore.WHITE + " ... \n")
    else:
        print(Fore.YELLOW + "[-]" + Fore.WHITE + " Found " + Fore.RED + str(num_file_matches) + Fore.WHITE + " files with ... " + Fore.RED + char + Fore.WHITE + " ... \n")

def main():
    
    for check_num in range(1, checks_2_run+1):
        
        print(Fore.RED + "\n[{}/{}]".format(check_num, checks_2_run) + Fore.WHITE + " Running Check #" + Fore.RED + str(check_num) + Fore.WHITE + " ...\n")

        for char in special_chars:
            num_file_matches = get_num_file_matches(folder, char)
            if(num_file_matches > 0):
                print_found(num_file_matches, char)
                replace(folder, char, replacement_char, num_file_matches)

        handle_emojis()

        for char in xtra_special_chars:
            num_file_matches = get_num_file_matches(folder, char)
            if(num_file_matches > 0):
                print_found(num_file_matches, char)
                replace(folder, char, replacement_char, num_file_matches)

        for char in xtra_xtra_special_chars:
            num_file_matches = get_num_file_matches(folder, char)
            if(num_file_matches > 0):
                print_found(num_file_matches, char)
                replace(folder, char, xtra_xtra_special_chars_dict[char], num_file_matches)

        for char in startswith_chars:
            num_file_matches = get_num_file_matches(folder, char)
            if(num_file_matches > 0):
                fix_startswith(char)

if __name__ == "__main__":
    main()
    print(Fore.GREEN + "\n[+] Done!\n")
