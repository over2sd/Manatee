#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
"""This program will pull information from the database and generate
a PNG image representing the progress of the categorization effort,
or an HTML page listing some of the unassigned categories.
"""
from __future__ import print_function

BUILD = "006"

import sys
from PIL import (Image, ImageDraw)
from jinja2 import (Environment, FileSystemLoader)
import glob, os
import codecs
from ccowsql import (create_engine)

SKRED = "#770000"
SKGRN = "#22ff22"

MAXMISS = 9999
L3W = 6
L2W = 26
L1W = 106
L4O = 3
L3O = 2
L2O = 1

# Function: pull all values from the <lang> string table into a single dict.
def dictpop(lang = "en"): # Should always be "en"
  """Given a language abbreviation, pulls all of the table rows out
  of the SQL database into a dict for fast processing without excessive
  network usage.
  This function hasn't been written yet.
  """
  lines = []
  config = {}
  try:
    with codecs.open('manatee.conf','rU','utf-8') as conf:
      lines = conf.readlines()
      conf.close()
  except IOError as e:
    print(" Could not open configuration file: %s" % e)
    exit(2)
  for line in lines:
    try:
      line = line.strip()
      if line:
        values = [x.strip() for x in line.split('=')]
        config[values[0]] = values[1]
    except Exception as e:
      print("There was an error in the configuration file: %s" % e)
      exit(3)
  # TODO: Any strings from the config file that might be displayed or passed into the SQL server need to be validated here.
  dict = {}
# create a connection
  # Create connection to SQL server (currently MySQL)
  engine = create_engine("%(host)s/%(base)s" % {'host':config["host"],'base':config["base"] } )
  sqlconn = engine.connect()
# send the query to grab all rows from the categories_en table
  cmd = "SHOW TABLES LIKE 'categories_" + lang + "';"
  result = sqlconn.execute(cmd)
  if result.rowcount:
    cmd = "SELECT * FROM categories_" + lang + ";"
    result = sqlconn.execute(cmd)
    if result.rowcount:
      for row in result:
        code = row['ccode']
        code = code.replace('o','x')
        dict[code] = row['ctext'][:5] # We don't need to store the whole text, just enough to check for [Un...
  else:
    print("Language not found!")
    sqlconn.close()
    exit(4)
# for each row, set dict['ccode'] = 'ctext'[:5]
# Oh, and do error checking along the way.
  sqlconn.close()
  return dict

# def isReserved(string): # Check if the value is "[Reserved]"

def isAssigned(code,dict):
  """Given a category code, checks for its presence in the previously
  populated dictionary and whether its value is [U* ([Unassigned],
  [Untranslated], etc). This latter check shouldn't be needed anymore,
  because the SQL version didn't include the [Unassiged] values, but
  it's here anyway.
  Returns True or False
  """
  if code in dict:
    s = dict[code]
    if s[0] == '[' and s[1] == 'U': # 
      return False
    else:
      return True
  else:
    return False

# Function: Create the progress image.

# Function: take the ccode and return a tuple ((x,y),width) where that pixel/box goes, and how wide a box should be.

def codeparent(code):
  """Given a CCOW code, returns its parent code."""
  code = code.lower()
  if code == "xxxx":
    return None # Top level has no parent
  stage = code.find('x')
  if stage == -1:
    stage = 3 # lowest level category, move up one level
  elif stage != 0:
    stage -= 1 # move up one level
  out = code[:stage] + "xxxx"[stage:]
  return out

# Function: Takes a dictionary of codes and returns a list of tuples: (iterator,code's parent code, code)
def listMissing(dict):
  """Given a dictionary, makes a list of its keys and the CCOW parent
  of each code in this form: (iterator,code's parent code, code)
  """
  n = 1
  list = []
  codes = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
  sys.stdout.write('.')
  key = "xxxx"
  if dict.get(key,None) == None:
    list.append((n,codeparent(key),key))
    n += 1
  for i in codes: # ?xxx
    key = i + "xxx"
    if dict.get(key,None) == None:
      list.append((n,codeparent(key),key))
      n += 1
  for i in codes: # ??xx
    for j in codes:
      key = i + j + "xx"
      if dict.get(key,None) == None:
        list.append((n,codeparent(key),key))
        n += 1
      if n > MAXMISS: break
    if n > MAXMISS: break
  for i in codes: # ???x
    for j in codes:
      for k in codes:
        key = i + j + k + "x"
        if dict.get(key,None) == None:
          list.append((n,codeparent(key),key))
          n += 1
        if n > MAXMISS: break
      if n > MAXMISS: break
    if n > MAXMISS: break

  for i in codes: # lowest level codes
    sys.stdout.write("\n" + i)
    for j in codes:
      sys.stdout.write(j)
      for k in codes:
        sys.stdout.write(".")
        for l in codes:
          key = i + j + k + l
#          print key
          if dict.get(key,None) == None:
            list.append((n,codeparent(key),key))
            n += 1
          if n > MAXMISS: break
        if n > MAXMISS: break
      if n > MAXMISS: break
    if n > MAXMISS: break
  return list

def main(): # The main event
  """Runs when called from the shell"""
  if "HTTP_HOST" in os.environ:
    print("Content-Type: text/html\n\n")
    print("<html><body>This program is not CGI. It should not be accessible on your Web server. Please run it from the command line. To view this program's output, load <a href=\"progress.htm\">progress.htm</a></body></html>")
    exit(0)
  print("  CCOW Progress image generator v1.1 build " + BUILD + " loaded.")
  if len(sys.argv) == 1: # read CLI args to see if we should build a missing list or a progress page
    print("You must specify a parameter: \"" + sys.argv[0] + " m\" for missing or \"" + sys.argv[0] + " p\" for progress. Please run again with a parameter.")
    exit(1)
  if sys.argv[1] == 'p': # if progress, create the new progress png
    print("Progress..", end='')
 # push the SQL database into a dict
    codes = dictpop()
 # cycle through the dict, writing pixels to the new image
 # save the new image to a timestamp-containing filename
 # move the old one to a filename preserving its original timestamp / rely on the old image already being saved in a timestamped filename?
 # point progress-old.png symlink at the old progress image, or copy the old new image to that name
 # point progress.png symlink to new image, or copy new image to that name
 # write a new progress.htm
 # all done, right?

  elif sys.argv[1] == 'm': # elif missing, create a new missing.htm
    print("Missing..",end='')
    here = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(here))
    template = env.get_template('missing.jtl')
    var = {}
 # push the SQL database into a dict
    codes = dictpop()
    var['codes'] = listMissing(codes)
#    print var['codes']
 # loop through codes, writing missing cats to a dict for templating
 # finally, open the file, call the templater, and try to write the file.
    try:
      with codecs.open("missing.htm",'wU',"UTF-8") as f:
        f.write(template.render({"var": var}).encode("utf-8"))
        f.close()
    except Exception as e:
      print("An error occurred attempting to open file for writing: %s" % e)

  else:
    print("Valid parameters are: \"" + sys.argv[0] + " m\" for missing or \"" + sys.argv[0] + " p\" for progress. Please run again with a valid parameter.")


# Standard boilerplate to call the main()
if __name__ == '__main__':
  main()