# main.py
from spaces import Client
import os
import urllib.parse

infile = "tmp.json"
outfile = "tmp.json_new"

class Gen_Links_File:

  space_name = "dev00psarchive"
  space_region = "nyc3"
  start_url = "https://{}.{}.cdn.digitaloceanspaces.com/".format(space_name, space_region)

  client = Client(
    region_name = space_region, # Required
    space_name = space_name, # Optional, can be set in spaces/env.yaml and/or be updated with <client>.set_space(space_name)
    public_key = 'DO00JYWXHAGAZUF6MGVA', # Required, but can set key in spaces/env.yaml                                                                         
    secret_key = '6nHPAllZ8c+x2Dq61Xbo1Nut3wH0KbghQgX8RJJ6KFE', # Required, but can set key in spaces/env.yaml

    # If any of region_name, public_key or secret_key are not provided, Client will override all values with env.yaml values.

  )

  def get_data(self):
    with open(infile, 'w') as f:
      data1 = self.client.list_files("archive-clips/")
      data2 = self.client.list_files("archive-lectures/")
      data3 = self.client.list_files("archive-podcasts/")

      f.write(str(data1))
      f.write(str(data2))
      f.write(str(data3))
    f.close()

  chars_dict = {
    "'Key': " : "\n",
  }

  chars_2_replace_dict = {
    "'," : "",
    "\"," : "",
    "'" : "",
    "\"" : "",
    "(" : "",
    ")" : "",
    "{" : "",
    "}" : "",

  }

  def reorg_json_data(self, data):
    # replace all chars_dict keys with empty string
    for key in self.chars_dict:
      instances = data.count(key)
      print("Found {} instances of {}".format(instances, key))
      new_data = data.replace(key, self.chars_dict[key])

      lines = new_data.splitlines()
      new_lines = []
      for line in lines:
        new_line = line.split("',")[0]
        new_line = new_line.split("\",")[0]
        for key in self.chars_2_replace_dict:
          new_line = new_line.replace(key, self.chars_2_replace_dict[key])

        url_line = self.start_url + urllib.parse.quote(new_line)
        if url_line != self.start_url:
          new_lines.append(url_line)
      
      new_data = ""
      for line in new_lines:
        new_data += line + "\n"
      return new_data

  def clean(self):
    if os.path.exists(infile):
      os.remove(infile)
    if os.path.exists(outfile):
      os.remove(outfile)

  def __init__(self, infile, outfile):
    
    self.clean()

    self.get_data()
    
    if infile == "clean" and outfile == "fs":
      self.clean()
    else:

      with open(infile, 'r') as f:
        data = f.read()
      f.close()
      
      new_data = self.reorg_json_data(data)
      
      with open(outfile, 'w') as f:
        f.write(new_data)
      f.close()

Gen_Links_File("tmp.txt", "tmp.txt_new")