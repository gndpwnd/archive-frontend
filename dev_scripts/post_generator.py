from distutils.fancy_getopt import fancy_getopt
import os
from colorama import Fore
from fixed_posts import Fixed_Posts
from file_name_fixer import FileNameFixer
import datetime
import webbrowser
from do_space_files import Gen_Links_File

# Need to fix actually outputting URL
# Also need to be able to update urls after second file name fixer is run

prog_str = Fore.GREEN + "\n[+] "

# get the current date
current_date = datetime.datetime.now()
current_date = current_date.strftime("%m-%d-%Y")

vid_exts = [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".vob", ".ogv", ".ogg", ".drc", ".gif", ".gifv", ".mng", ".qt", ".yuv", ".rm", ".rmvb", ".asf", ".amv", ".m4p", ".m4v", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".m2v", ".m4v", ".svi", ".3gp", ".3g2", ".mxf", ".roq", ".nsv", ".flv", ".f4v", ".f4p", ".f4a", ".f4b"]

hosting_subdomains = ["clips", "photos", "lectures", "resources", "podcasts"]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_file_links():
    links = []
    Gen_Links_File("tmp.txt", "links.txt")
    with open("links.txt", "r") as f:
        for line in f:
            links.append(line)
    Gen_Links_File("clean", "fs")
    return links

def host_vid(vid_url, vid_name):
    host_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body>
    <video style="width: 100%; border: 7px outset #7DF9FF; border-radius: 25px; overflow: hidden; text-align: center;" controls>
        <source src="{}" type="video/mp4">
    </video>
</body>
</html>
"""

    with open(vid_name + ".html", "w") as f:
        f.write(host_html.format(vid_url))
        print(Fore.GREEN + "Video hosted: " + Fore.WHITE + vid_name + ".html")
    f.close()
    
    new = 2
    webbrowser.open(vid_name + ".html", new=new)
    os.remove(vid_name + ".html")







def get_info(post_name, file_path, ext):

    num_steps = 3
    curr_step = 1

    host_vid(file_path, post_name)

    print(Fore.YELLOW + "\nCurrent media file path:\n" + Fore.WHITE + file_path)

    print(Fore.YELLOW + "\nCurrent post name:\n" + Fore.WHITE + post_name)

    change_name = input(Fore.YELLOW + "\nChange name? (y/N): " + Fore.WHITE)
    if change_name == "y":
        post_name = input(Fore.YELLOW + "Enter new name: " + Fore.WHITE)
        new_file = "/".join(file_path.split("/")[:-1]) + "/" + post_name.lower() + ext
        os.rename(file_path, new_file)
        print(prog_str + Fore.YELLOW + " Name changed to: " + Fore.WHITE + post_name)
        print(prog_str + Fore.YELLOW + " File path changed to:\n" + Fore.WHITE + new_file)
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



def create_template(post_name, url, t_files, curr_file):
    
    clear_screen()
    
    print(Fore.GREEN + "\n\n[+]" + Fore.BLUE + " Generating post " + Fore.GREEN + "[{} of {}]\n".format(curr_file, t_files))
    
    new_name = new_name.replace("_", " ")
    new_name = new_name.upper()

    description, tags, categories = get_info(new_name, file_path, ext)

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
    <video style=\""width: 100%; border: 7px outset #7DF9FF; border-radius: 25px; overflow: hidden;\" controls>
        <source src="{}" type=\"video/{}\"> 
    </video>
{{< /rawhtml >}}
""".format(new_name, current_date, description, tags, categories, url, ext.replace(".", ""))

    return template
 
    
def write_post(posts_dir, post_name, template):
    
    if post_name[len(post_name)-3:] != ".md":
        post_name = (post_name[:len(post_name)-4] + ".md").lower()

    with open(posts_dir + post_name, "w") as f:
        f.write(template)
        print(prog_str + Fore.BLUE + " Post generated: " + Fore.YELLOW + posts_dir + post_name)
    f.close()


def init():
    clear_screen()

    posts_dir = input(Fore.YELLOW + "Enter path to posts directory: " + Fore.WHITE)

    links = get_file_links()
    
    print(prog_str + Fore.BLUE + "Found " + Fore.WHITE + "{}".format(len(links)) + Fore.BLUE + " files to generate posts for")
    for link in links:
        post_name = link.split("/")[-1]
        post_name = post_name.split(".mp4")[0]

        template = create_template(post_name, link, len(links), 1)
        write_post(posts_dir, post_name, template)

    clear_screen()
    print(prog_str + "Generating Fixed Posts...")
    Fixed_Posts(posts_dir)
    
    clear_screen()
    print(prog_str + Fore.BLUE + " Finished generating posts " + prog_str.replace("\n", ""))