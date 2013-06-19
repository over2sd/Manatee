#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
"""This program will pull information from the database and generate
a PNG image representing the progress of the categorization effort,
or an HTML page listing some of the unassigned categories.
"""
from __future__ import print_function

BUILD = "024"

import sys
from PIL import (Image, ImageDraw)
from jinja2 import (Environment, FileSystemLoader)
import glob, os, shutil
import codecs
from ccowsql import (create_engine)
import math
from datetime import (date,time,datetime)

SKRED = "#770000"
SKGRN = "#22ff22"
SKYEL = "#cccc00"

MAXMISS = 9999
L3W = 6
L2W = 26
L1W = 106
L4O = 3
L3O = 2
L2O = 1

imgsize = 424, 424

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
        # for each row, set dict['ccode'] = 'ctext'[:5]
        code = row['ccode']
        code = code.replace('o','x')
        dict[code] = row['ctext'][:5] # We don't need to store the whole text, just enough to check for [Un...
  else:
    print("Language not found!")
    sqlconn.close()
    exit(4)
# Oh, and do error checking along the way. (TODO)
  sqlconn.close()
  return (dict, config)

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

def unhex(c):
  """Given a hex character, returns the decimal value in an integer."""
  c = c[:1]
  if "abcdefABCDEF0123456789".find(c) != -1:
    return int(c,16)
  else:
    return 0

# Function: take the ccode and return a tuple ((x,y),width) where that pixel/box goes, and how wide a box should be.
def codeLoc(code):
  """Given a code, this function returns a tuple containing a tuple
  of the x,y coordinates that belong to the code, and its width by
  stage level. The draw function will use these to determine where
  and how big to draw the box for that code.
  """
  stage = code.find('x')
  if stage == -1: stage = 4 # No x in code, must be 4th stage.
  width = [L1W - 1,L2W - 1,L3W - 1,0]
  xs = [0,0,0,0]
  ys = [0,0,0,0]
  if stage > 0:
    a = unhex(code[0])
    xs[0] = (a % 4) * L1W
    ys[0] = int(math.floor(a/4) * L1W)
    if stage > 1:
      a = unhex(code[1])
      xs[1] = (a % 4) * L2W
      ys[1] = int(math.floor(a/4) * L2W)
      if stage > 2:
        a = unhex(code[2])
        xs[2] = (a % 4) * L3W
        ys[2] = int(math.floor(a/4) * L3W)
        if stage > 3:
          a = unhex(code[3])
          xs[3] = (a % 4)
          ys[3] = int(math.floor(a/4))
  offset = [0,0,L2O,L3O,L4O]
  stage = offset[stage]
  x = int(sum(xs) + stage)
  y = int(sum(ys) + stage)
  return ((x,y),width[stage])

def timeStamper():
  """Returns a timestamp string suitable for use in filenames."""
  t = datetime.utcnow()
  s = "{0:%y%m%d-%H%M}".format(t) # Running this progress report more than once a minute is porbably excessive.
  return s

def buildPNG(codes):
  """Given a dict of codes, builds a PNG image representing the progress
  of assigning categories. Returns the number of categories described as
  [Reserved]. (int)
  """
  numres = 0
  png = Image.new("RGBA",imgsize,SKRED)
  draw = ImageDraw.Draw(png)
  i = 0
  for c in codes:
    if (i % 50) == 0: print(".",end = '')
    color = SKGRN
    if codes[c].find("[R") == 0:
      color = SKYEL
      numres += 1
    t = codeLoc(c)
    a = t[0]
    if t[1] == 0:
      draw.point(a,color)
    else:
      b = (t[0][0] + t[1],t[0][1] + t[1])
      draw.rectangle([a,b], outline = color)
    i += 1
  del draw
  png.save("temp.png","PNG")
  return numres

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
    here = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(here))
    template = env.get_template('templates/progress.jtl')
    var = {}
    var['build'] = BUILD
 # push the SQL database into a dict
    (codes, config) = dictpop()
 # cycle through the dict, writing pixels to the new image
    reserved = buildPNG(codes)
    var['res'] = reserved
    x = 69904.00 # 16^4 + 16^3 + 16^2 + 16
    var['creq'] = round(x,0);
#    print(len(codes))
    x = round(len(codes) / x,7)
    var['cdone'] = len(codes);
    var['pcdone'] = x * 100 # To make the percentage display a percentage, not a decimal
    var['perwid'] = round(var['pcdone'],1);
    var['ts'] = "{0:%H:%M:%Sh (UTC) on %b %d, %Y}".format(datetime.utcnow())
 # save the new image to a timestamp-containing filename
    ts = timeStamper()
    try:
      os.rename("temp.png","progress" + ts + ".png")
 # move the old one to a filename preserving its original timestamp / rely on the old image already being saved in a timestamped filename?
 # point progress-old.png symlink at the old progress image, or copy the old new image to that name
      old = "progress.png"
      older = "progress-old.png"
      if os.path.exists(older):
        os.remove(older)
      if os.path.exists(old):
        os.rename(old,older)
 # point progress.png symlink to new image, or copy new image to that name
      shutil.copy("progress" + ts + ".png",old)
 # write a new progress.htm
      with codecs.open("progress.htm",'wU',"UTF-8") as f:
        f.write(template.render({"var": var, "config": config}).encode("utf-8"))
        f.close()
    except Exception as e:
      print("An error occurred attempting to process files: %s" % e)
 # all done, right?

  elif sys.argv[1] == 'm': # elif missing, create a new missing.htm
    print("Missing..",end='')
    here = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(here))
    template = env.get_template('templates/missing.jtl')
    var = {}
    var['build'] = BUILD
 # push the SQL database into a dict
    (codes, config) = dictpop()
    var['codes'] = listMissing(codes)
#    print var['codes']
 # loop through codes, writing missing cats to a dict for templating
 # finally, open the file, call the templater, and try to write the file.
    try:
      with codecs.open("missing.htm",'wU',"UTF-8") as f:
        f.write(template.render({"var": var, "config": config}).encode("utf-8"))
        f.close()
    except Exception as e:
      print("An error occurred attempting to open file for writing: %s" % e)

  else:
    print("Valid parameters are: \"" + sys.argv[0] + " m\" for missing or \"" + sys.argv[0] + " p\" for progress. Please run again with a valid parameter.")
  print(".")


# Standard boilerplate to call the main()
if __name__ == '__main__':
  main()