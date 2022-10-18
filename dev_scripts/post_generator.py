from asyncore import write
from hashlib import new
import os
from colorama import Fore
from file_name_fixer import FileNameFixer
import datetime

# Need to fix actually outputting URL
# Also need to be able to update urls after second file name fixer is run

# get the current date
current_date = datetime.datetime.now()
current_date = current_date.strftime("%m-%d-%Y")

vid_exts = [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".vob", ".ogv", ".ogg", ".drc", ".gif", ".gifv", ".mng", ".qt", ".yuv", ".rm", ".rmvb", ".asf", ".amv", ".m4p", ".m4v", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".m2v", ".m4v", ".svi", ".3gp", ".3g2", ".mxf", ".roq", ".nsv", ".flv", ".f4v", ".f4p", ".f4a", ".f4b"]

hosting_subdomains = ["clips", "photos", "lectures", "resources", "podcasts"]

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def determine_hosting_url(file_path):
    # if os is windows
    if os.name == "nt":
        file_path = file_path.replace("\\", "/")
    
    file_path = file_path.split("/")
    hosting_url = ""
    url_to_file = ""
    # if folder in file path is a hosting subdomain
    for subdomain in range(0, len(hosting_subdomains)-1):
        if ("archive-"+hosting_subdomains[subdomain]) in file_path:
            hosting_url = "https://"+hosting_subdomains[subdomain]+".dev00ps.com/"
            new_file_path = file_path[file_path.index("archive-"+hosting_subdomains[subdomain]):]

            url_to_file = hosting_url + new_file_path

    print(Fore.GREEN + "[+]" + Fore.YELLOW + "URL: " + Fore.WHITE + url_to_file)
    return url_to_file

def get_src(hosting_url, file_path):
    file_name = file_path.split("/")[-1]
    src = hosting_url + file_name
    return src

def get_info(post_name, file_path, ext):
    num_steps = 3
    curr_step = 1

    print(Fore.YELLOW + "\nCurrent media file path:\n" + Fore.WHITE + file_path)

    print(Fore.YELLOW + "\nCurrent post name:\n" + Fore.WHITE + post_name)

    change_name = input(Fore.YELLOW + "\nChange name? (y/N): " + Fore.WHITE)
    if change_name == "y":
        post_name = input(Fore.YELLOW + "Enter new name: " + Fore.WHITE)
        new_file = "/".join(file_path.split("/")[:-1]) + "/" + post_name.lower() + ext
        os.rename(file_path, new_file)
        print(Fore.GREEN + "\n[+]" + Fore.YELLOW + " Name changed to: " + Fore.WHITE + post_name)
        print(Fore.GREEN + "[+]" + Fore.YELLOW + " File path changed to:\n" + Fore.WHITE + new_file)
    elif change_name == "n":
        pass
    elif change_name == "":
        print(Fore.BLUE + "defaulting to no change...")
    else:
        print(Fore.RED + "Invalid option, defaulting to no change...")

    print(Fore.YELLOW + "\nExample Entry: " + Fore.BLUE + "ah" + Fore.WHITE + "\n(short, lecture, etc... \ndefinitions will be added automatically based on folder names in file path)\n")
    description = input(Fore.GREEN + "[{} of {}] ".format(curr_step, num_steps) + Fore.YELLOW + "Enter a description for the post: " + Fore.WHITE)

    # if subdomain in file path
    for subdomain in range(0, len(hosting_subdomains)-1):
        if ("archive-"+hosting_subdomains[subdomain]) in file_path:
            description = description + ", " + hosting_subdomains[subdomain]
    
    curr_step += 1
    print(Fore.YELLOW + "\nExample: " + Fore.WHITE + "tag1, tag2, tag3")
    tag_to_add = input(Fore.GREEN + "[{} of {}] ".format(curr_step, num_steps) + Fore.YELLOW + "Enter tags for the post (separate with commas): " + Fore.WHITE)
    if " " and "," in tag_to_add:
        pass
    elif " " and not "," in tag_to_add:
        print(Fore.RED + "Please separate tags with commas\n" + Fore.WHITE)
    tags = tag_to_add.split(",")
    tags = [tag.strip() for tag in tags]
    new_tags = ""
    for tag in tags:
        new_tag = "\"    {}\",\n".format(tag)
        new_tags += new_tag

    curr_step += 1
    print(Fore.YELLOW + "\nExample: " + Fore.WHITE + "category1, category2, category3")
    category = input(Fore.GREEN + "[{} of {}] ".format(curr_step, num_steps) + Fore.YELLOW + "Enter categories for the post (separate with commas): " + Fore.WHITE)
    if " " and "," in category:
        pass
    elif " " and not "," in category:
        print(Fore.RED + "Please separate categories with commas\n" + Fore.WHITE)
    categories = category.split(",")
    categories = [category.strip() for category in categories]
    new_categories = ""
    for category in categories:
        new_category = "\"    {}\",\n".format(category)
        new_categories += new_category
    
    return description, new_tags, new_categories
     
def create_template(post_name, file_path, ext, t_files, curr_file):
    
    clear_screen()
    
    print(Fore.GREEN + "\n\n[+]" + Fore.BLUE + " Generating post " + Fore.GREEN + "[{} of {}]\n".format(curr_file, t_files))
    
    new_name = post_name.replace(ext, "")
    new_name = new_name.replace("_", " ")
    new_name = new_name.upper()

    description, tags, categories = get_info(new_name, file_path, ext)
    url_to_file = determine_hosting_url(file_path)

    template = """
---
title: "{}"
date: "{}"
description: "{}"
tags: [
{}
]
categories: [
{}
]
type: \"post\"
---
{{< rawhtml >}}
    <video style=\"height=40%;width=auto\" overflow=\"hidden\" controls>
        <source src="{}" type=\"video/{}\"> 
    </video>
{{< /rawhtml >}}
""".format(new_name, current_date, description, tags, categories, url_to_file, ext.replace(".", ""))

    return template
    
def write_post(posts_dir, post_name, template):
    
    if post_name[len(post_name)-3:] != ".md":
        post_name = (post_name[:len(post_name)-4] + ".md").lower()

    with open(posts_dir + post_name, "w") as f:
        f.write(template)
        print(Fore.GREEN + "[+]" + Fore.BLUE + " Post generated: " + Fore.YELLOW + posts_dir + post_name)
    f.close()

def get_count():
    count = 0
    for path, subdirs, files in os.walk(media_dir):
        for name in files:
            for ext in vid_exts:
                if name.endswith(ext):
                    count += 1
    return count

def main(media_dir, posts_dir):
    clear_screen()
    t_files = get_count()
    print(Fore.GREEN + "[+]" + Fore.BLUE + "Found {} files to generate posts for".format(t_files))

    posts_dir = "./posts/"
    # if folder doesn't exist, create it
    if not os.path.exists(posts_dir):
        os.mkdir(posts_dir)

    curr_file = 1
    for path, subdirs, files in os.walk(media_dir):
        for name in files:
            for ext in vid_exts:
                if name.endswith(ext):
                    file_path = os.path.join(path,name)
                    template = create_template(name, file_path, ext, t_files, curr_file)
                    write_post(posts_dir, name, template)
                    curr_file += 1

def init():
    # get content directory
    if os.name == "nt":
        print(Fore.YELLOW + "Example: " + Fore.WHITE + "C:\\Users\\user\\Desktop\\archive")
    else:
        print(Fore.YELLOW + "Example: " + Fore.WHITE + "/home/user/Desktop/archive/")

    media_dir = input(Fore.YELLOW + "Enter the directory with files generate posts of: " + Fore.WHITE)
    FileNameFixer(media_dir)

    # get posts directory
    if os.name == "nt":
        print(Fore.YELLOW + "Example: " + Fore.WHITE + "C:\\Users\\user\\Desktop\\archive\\content\\posts")
    else:
        print(Fore.YELLOW + "Example: " + Fore.WHITE + "/home/user/Desktop/archive/content/posts/")
    posts_dir = input(Fore.YELLOW + "Enter the directory to write posts to: " + Fore.WHITE)
    if posts_dir == "":
        print(Fore.RED + "An Error Occured, Defaulting to:" + Fore.WHITE + media_dir + "/posts/")
        posts_dir = media_dir + "/posts/"
    
    if media_dir[:-1] == " ":
        media_dir = media_dir[:len(media_dir) - 1]
    
    if posts_dir[:-1] == " ":
        posts_dir = posts_dir[:len(posts_dir) - 1]

    return media_dir, posts_dir

clear_screen()

media_dir, posts_dir = init()
main(media_dir, posts_dir)

clear_screen()

print(Fore.GREEN + "\n[+]" + Fore.BLUE  + "Running a double check on file names...\n")
FileNameFixer(media_dir)
print(Fore.GREEN + "\n[+]" + Fore.BLUE + " Finished generating posts" + Fore.GREEN + " [+]\n")