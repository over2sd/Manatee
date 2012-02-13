#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import cgi
import codecs
import cgitb; cgitb.enable()

def chooseStyle(c):
  """Given a three-letter code 'c', this function returns a string
  containing the relative filename (without extension) of a stylesheet
  to load after the main sheet, allowing users to view the helper
  application in a different style.
  alt = First alternate stylesheet. Subcats show in a list instead of a grid.
  """
  if c == None: return None
  c = c[:3]
  styledict = {}
  styledict['alt'] = "alpha"
  if c in styledict:
    return styledict[c]
  else:
    return None

def cleanCode(si):
  """Given an input code, returns a validated, 4-character code. Any
  invalid character causes the function to cease checking and fill
  any remaining characters with 'x'.
  """
  while len(si) < 4: si += 'x' # fill out the length of the code string
  so = ""
  for ii in range(4):
    if si[ii] in "1234567890abcdefxyABCDEFX": # check if this is a valid character
# [0-9a-fA-FxyX]
      so += si[ii] # valid character
    else:
      so += "xxxx" # fill the string with 'x'
      ii = 4 # hit a bad one, stop checking string
  return so[:4] # clean code is 4 characters long

def getStage(code):
  """Simple function that returns 0-4 to denote which stage of
  the catalog the given code belongs to.
  """
  loc = code.find('x')
  if loc < 0: loc = 4
  if code == "XXXX": loc = 0
  return loc

def unhexchar(c):
  """Given a hex character, returns the decimal value in an integer."""
  c = c[:1]
  if "abcdefABCDEF0123456789".find(c) != -1:
    return int(c,16)
  else:
    return None

def hexchar(i):
  """Given an int, return a hex character"""
  if i > -1 and i < 16:
    return "%X" % i
  else:
    return None

def formClean(s):
  """Given a string, replaces double-quotes and other troublesome
  characters so the string can be used in a form.
  """
  s = s.replace('"',"'")
  s = s.replace("\n"," ")
  return s

from os import path
def loadConfig():
  """Returns a dict containing the config options in the CCOW config file."""
  lines = []
  config = {}
  here = path.dirname(__file__)
  fn = path.join(here,'manatee.conf')
  try:
    with codecs.open(fn,'rU','utf-8') as conf:
      lines = conf.readlines()
      conf.close()
  except IOError as e:
    print " Could not open configuration file: %s" % e

  for line in lines:
    try:
      line = line.strip()
      if line:
        values = [x.strip() for x in line.split('=')]
        config[values[0]] = values[1]
    except Exception as e:
      print "There was an error in the configuration file: %s" % e
  # TODO: Any strings from the config file that might be displayed or passed into the SQL server need to be validated here.
#  config = validateConfig(config)
  return config