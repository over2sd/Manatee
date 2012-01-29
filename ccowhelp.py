#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
## old line: # coding: utf-8

import sys
import os
import re
import cgi
import cgitb; cgitb.enable()
import codecs
from sqlalchemy import (create_engine, Column)

BUILDNUM = "064"
MYNAME = os.path.basename(sys.argv[0])

import tmpvalues
dict = tmpvalues.populate()

def showTop(t):
  """Given a title string, prints the stuff needed at the top of our XHTML
  documents.
  """
  print "Content-Type: text/html\n\n",
  print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n<html xmlns=\"http://www.w3c.org/1999/xhtml\" lang=\"EN\">\n<head>\n\t<title>" + t + "</title>\n\t<link rel=\"stylesheet\" type=\"text/css\" href=\"main.css\" />\n</head>\n<body>"


def showFoot(lang):
  """Given a program name and a 2-character language abbreviation, prints
  an XHTML footer with standard links and information, along with the
  closing tags to complete the XHTML output. This should be the last
  method called in the program.
  """
  print "\n\t<p class=\"clearit\">Don't know what these categories mean? Check out <a href=\"" + MYNAME + "?lang=" + lang + "&cowc=yxxx\">Category Explanation</a>"
  print "\t<p class=\"clearit\"> </p>"
  glot("scc1",lang)
  glot("scc2",lang)
  glot("ssou",lang)
  print "\t<p class=\"buildnum\" id=\"sm04\">Build: " + str(BUILDNUM) + "</p>\n</body>\n</html>\n\n"

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

def langSel():
  """Prints HTML with links to allow the user to choose language
  in which to browse the help system.
  """
  print "\n\t<h1 id=\"sm10\">Select Language</h1>"
  print "\n\t\t<div class=\"languages\">"
  langs = {}
# later, we'll populate this from the SQL database.
  langs["en"] = "Language: English"
  langs["es"] = "Idioma: Español"
  for k,v in langs.items():
    print "\t\t\t<p class=\"lingua\"><a href=\"" + MYNAME + "?lang=" + k + "\">" + v + "</a></p>"
  print "\t\t</div>"

def getStage(code):
  """Simple function that returns 0-4 to denote which stage of
  the catalog the given code belongs to.
  """
  loc = code.find('x')
  if loc < 0: loc = 4
  if code == "XXXX": loc = 0
  return loc

def glotCrumbs(code,stage,lang):
  """This function prints a trail of breadcrumbs in the appropriate
  language.
  """
  print "<!-- Code: " + str(code) + " stage " + str(stage) + " language: " + lang + " -->"
  if code[0] == 'x' or stage == 0: # already at the top
    print "\n\t\t<ul class=\"loaf\" id=\"breadtrail\">\n\t\t\t<li class=\"crumb\" id=\"sm05\"><a href=\"" + MYNAME + "\">",
    glot("slan",lang,stage)
    print "</a></li>\n\t\t</ul>"
    return
  else:
    print "\t\t<ul class=\"loaf\" id=\"breadtrail\">\n\t\t\t<li class=\"crumb\" id=\"sm06\"><a href=\"" + MYNAME + "?lang=" + lang + "&cowc=xxxx\">",
    glot("soop",lang,stage)
    print "</a> &gt;</li>"
    ic = 1
    while ic < stage and code[ic] != 'x':
      print "\t\t\t<li class=\"crumb\" id=\"sm0" + str(ic + 6) + "\"><a href=\"" + MYNAME + "?lang=" + lang + "&cowc=" + str(code[:ic]) + "\">",
      sc = code[:ic]
      while len(sc) < 4: sc += 'x'
      glot(sc,lang,ic)
      print "</a> &gt;</li>"
      ic = ic + 1
    print "\n\t\t</ul>"

def glotInf(code,lang,verbose = 1):
  """Given a category code, a language, and instruction on whether
  to be verbose, this function finds the appropriate description file
  in the cats/<langabbrev>/ subdirectory and prints its contents.
  """
  filename = os.path.join("cats/" + lang + "/",code)
  lines = []
  try:
    f = codecs.open(filename,'rU','utf-8')
    lines = f.readlines()
    f.close()
  except IOError as e:
    if verbose:
      filename = os.path.basename(filename)
      if lang != "en":
        sglot("seng",lang,filename)
        glotInf(code,"en",verbose)
      else:
        sglot("snia",lang,filename)
  for line in lines:
    print line,

def explainCats(lang):
  """Just what it says on the tin."""
  print "\n\t\t<h1 id=\"sm17\">",
  glot("sxpl",lang)
  print "</h1>\n\t\t<div class=\"content\" id=\"sm18\">\n\t\t\t<div class=\"menu\" id=\"sm16\">\n\t\t\t\t",
  glotInf("yxxx",lang,0)
  print "\n\t\t\t\t<p class=\"clearit\"> </p>"
  showSubs("yxxx",lang,3)
# I think this is incomplete, too

def glot(code,lang,stage = 5):
  """Given a category code, a language abbreviation (e.g. "en"), and a
  stage, this function will print the category's description in that
  language, if available, and fall back to English, if not.
  """
  # Some day, SQL...
  # for now, a dict:
  if code in dict:
    print dict[code],
  elif stage == 5:
    if code == "sms1":
      print "'Missing string' string not found! The sky is falling!"
      exit(2)
    glot("sms1",lang)
  else:
    print "[Unassigned] ",
    laspects = ["Hol","Ras","Dua","Chi","Ter","Fum","Sek","Zab","Med","Neu","Uay","Arz","Pax","Ord","Iyu","Ech"]
    aspect = unhexchar(code[stage - 1])
    print "<!-- Aspect: " + str(aspect) + " stage: " + str(stage) + "-->",
    if aspect != None:
      print "(" + laspects[aspect] + ")",

def sglot(code,lang,s):
  """Given a category code, a language abbreviation, and a string,
  loads the code from the language table and replaces '%s' in the
  text with the provided string.
  """
# someday, I'll pull this from SQL, and the lang will matter.
  if code in dict:
    text = dict[code] # for now, pull from temporary dict
  else:
    glot("sms1",lang)
    exit(1)
  print re.sub("%s",s,text),

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

def showSubs(code,lang,stage):
  """Given a category code, a language abbreviation, and a code
  stage (int), this function prints the HTML to produce 16 buttons,
  which link to the subcategories that belong to that code, along
  with their descriptions.
  """
  for i in range(16):
    c = hexchar(i)
    tcode = code[:stage]
    tcode += c.lower()
    tcode = cleanCode(tcode)
    print "\n\t\t\t\t<p class=\"subcat\"><a href=\"" + MYNAME + "?lang=" + lang + "&cowc=" + tcode + "\">" + c.lower() + ": ",
    glot(tcode,lang,stage + 1)
    print "</a></p>",
  print "\n<p class=\"clearit\"> </p>"


def main():
  """Run if the program is called from the shell, of course."""
  conf = open('sql.cfg') # change to: conf = open('manatee.conf')
  lines = conf.readlines()
  engine = create_engine("%s/ccow" % lines[0].strip())
  sqlconn = engine.connect()
  query = cgi.FieldStorage()
  lang = query.getvalue("lang","en")
  code = query.getvalue("cowc","XXXX")
  code = str(cleanCode(code))
# check for query string
  if len(query) == 0:
# if no query, offer lang selection
    showTop("Manatee: Select Language")
    langSel()
  else:
# if query provided, show a page...
    showTop("Manatee: " + str(code)) # ...with a title grabbed from the database...
    stage = getStage(code)
    cat00 = str(code[:stage])
    cattrim = cat00
    for i in range(4 - stage): cat00 += '0'
    if code[0] == 'y':
      glotCrumbs("0xxx",1,lang)
      if code[3] == 'x':
        explainCats(lang)
      else:
        print "\t\t\t<li class=\"crumb\" id=\"sm07\"><a href=\"" + MYNAME + "?lang=" + lang + "&cowc=yxxx\">",
        glot("sxpl",lang)
        print "</a> &gt;</li>"
        print "\n\t\t</ul>"
        print "\n\t\t<h1 id=\"sm11\">#*" + code[-1:] + ": ",
        glot(code,lang,4)
        print "</h1>\n\t\t<div class=\"content\" id=\"sm12\">",
        print "\n\t\t\t<div class=\"menu\" id=\"sm14\" style=\"border-color: #" + cat00[:3] + ";\">\n\t\t\t\t",
        glotInf(code,lang,1)
        print "\n\t\t\t</div>\n\t\t</div>"
        print "\n\t</div>",
    else:
      glotCrumbs(code,stage,lang)
      print "\n\t\t<h1 id=\"sm11\">#" + cattrim + ": ",
      glot(code,lang,stage)
      print "</h1>\n\t\t<div class=\"content\" id=\"sm12\">",
      if stage > 0:
        sglot("sadd",lang,cattrim)
      if stage > 3:
        sglot("smet",lang,cat00)
      else:
        glot("smul",lang,stage)
        print '<a href="' +MYNAME + "?lang=" + lang + "&cowc=" + cat00 + "\"> #" + cat00 + ": ",
        glot(cat00,lang,stage)
        sglot("scod",lang,cat00)
      glot("shed",lang,stage)
      print "\n\t\t\t<div class=\"menu\" id=\"sm14\" style=\"border-color: #" + cat00[:3] + ";\">\n\t\t\t\t",
      if stage < 4:
        glot("snot",lang)
      glotInf(code,lang,0)
      if stage < 4:
        print "\n<p class=\"clearit\"> </p>"
        showSubs(code,lang,stage)
      print "\n\t\t\t</div>\n\t\t</div>"
    print "\n\t</div>",
  print "\n\t<a href=\"progress.htm\">View Progress Report</a>"
  showFoot(lang)
  test = "SELECT ctext FROM category WHERE ccode = 'ee37';"
  result = sqlconn.execute(test)
  for row in result:
    print row['ctext']
  sqlconn.close()
  exit(0)

# Standard boilerplate to call the main()
if __name__ == '__main__':
  main()