#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""Polyglot functions for CCOW"""

import sys
import os
from ccowsql import unsql
from ccowcgi import (hexchar, cleanCode, unhexchar)
MYNAME = os.path.basename(sys.argv[0])

import svalues
dict = svalues.populate()

def glot(code,sql,lang,stage = 5):
  """Given a category code, a language abbreviation (e.g. "en"), and a
  stage, this function returns the category's description in that
  language, if available, and falls back to English, if not.
  """
  outstring = ""
  nodict = False
  # Some day, SQL...
  # for now, a dict:
  if code[0] == 's' or code[0] == 'y':
    if lang in dict:
      if code in dict[lang]:
        outstring += dict[lang][code]
      elif stage == 5:
        if code == "sms1":
          return "'Missing string' string not found! The sky is falling!"
        glot("sms1",lang)
      else:
        nodict = True
    else:
      nodict = True
  else:
    nodict = True
  if nodict:
#    if stage == 5: stage = 4
    cmd = "SHOW TABLES LIKE 'categories_" + lang + "';"
    result = sql.execute(cmd)
#    print "<!-- Rows: " + str(result.rowcount) + " -->"
    if result.rowcount:
      code = code.replace('x','o') # x isn't allowed in the SQL because of 0x combinations
      code = code.replace('X','o') # Special for no category given
      cmd = "SELECT ctext FROM categories_" + lang + " WHERE ccode = '" + code + "' LIMIT 1;"
      result = sql.execute(cmd)
      if result.rowcount:
        for row in result:
          return unsql(row['ctext'])
      else:
        outstring = "[Unassigned] (%s)"
        laspects = ["Hol","Ras","Dua","Chi","Ter","Fum","Sek","Zab","Med","Neu","Uay","Arz","Pax","Ord","Iyu","Ech"]
        aspect = unhexchar(code[stage - 1])
 #    print "<!-- Aspect: " + str(aspect) + " stage: " + str(stage) + "-->",
        if aspect != None:
          outstring = outstring.replace("%s",laspects[aspect])
    elif lang != "en":
      glot(code,sql,"en")
    else:
      return "Database query failed: No languages found!"
    #sql
  return outstring

def glotCrumbs(sql,code,stage,lang):
  """This function returns a list loaded with one or more tuples containing
  the strings needed to print a trail of breadcrumbs in the
  appropriate language.
  """
  crumbs = []
  if code[0] == 'x' or stage == 0: # already at the top
    a = "5"
    b = MYNAME
    c = glot("slan",sql,lang)
    crumbs.append((a,b,c))
    return crumbs
  else:
    a = "6"
    b = MYNAME + "?lang=" + lang
    c = glot("soop",sql,lang,stage)
    crumbs.append((a,b,c))

    ic = 1
    while ic < stage and code[ic] != 'x':
      a = str(ic + 6)
      b = MYNAME + "?lang=" + lang + "&cowc=" + str(code[:ic])
      sc = code[:ic]
      while len(sc) < 4: sc += 'x'
      c = glot(sc,sql,lang,ic)
      crumbs.append((a,b,c))
      ic = ic + 1
    return crumbs

def glotSubs(sql,code,stage,lang):
  """Given a database connection, a category code, a language
  abbreviation, and a code stage (int), this function returns
  a list of tuples containing the code, digit, and description
  of its 16 subcategories.
  """
  subs = []
  for i in range(16):
    c = hexchar(i)
    scode = code[:stage]
    scode += c.lower()
    scode = cleanCode(scode)
    sdesc = glot(scode,sql,lang,stage + 1)
    subs.append((scode,c,sdesc))
  return subs
