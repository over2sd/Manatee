#!/usr/bin/python -tt
"""This program will pull information from the database and generate
a PNG image representing the progress of the categorization effort.
"""

import sys

SKRED = "770000"
SKGRN = "22ff22"

MAXMISS = 9999
L3W = 6
L2W = 26
L1W = 106
L4O = 3
L3O = 2
L2O = 1

# Function: pull all values from the "en" string table into a single dict.
def dictpop(lang):
  """Given a language abbreviation, pulls all of the table rows out
  of the SQL database into a dict for fast processing without excessive
  network usage.
  This function hasn't been written yet.
  """
  dict = {}
  return dict

def isAssigned(code,dict):
  """Given a category code, checks for its presence in the previously
  populated dictionary and whether its value is [U* ([Unassigned],
  [Untranslated], etc).
  Returns True or False
  """
  if code in dict:
    s = dict[code]
    if s[0] == '[' and s[1] == 'U':
      return False
    else:
      return True
  else:
    return False

# Function: (next step)


# Standard boilerplate to call the main()
if __name__ == '__main__':
  main()