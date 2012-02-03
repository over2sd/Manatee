#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

BUILD = "002"

from jinja2 import (Environment, FileSystemLoader)
from ccowi18n import (glot, glotCrumbs, glotCrumbs, glotSubs)
from ccowcgi import (cgi, loadConfig, cleanCode, chooseStyle, getStage)
from ccowsql import (create_engine)
from flask import (Flask, render_template)
app = Flask(__name__)

import sys
import os
MYNAME = os.path.basename(sys.argv[0])

def makeForm():
  """returns the lines of a form"""
# form displayer function goes here
  return

@app.route('/suggest')
def suggest():
  print "Content-Type: text/html\n\n",

  config = loadConfig()
  var = {}
  var['build'] = BUILD
  # check for input
  # if no input, display form
  # check input validity
  # ccode
  # make a connection
  # category already assigned?
  # maybe a field for reasoning?
  # suggested category text
  # if it's all good, insert a row into the suggestions table
  # if bad input, display form
  return render_template("suggest.jtl", var=var)

if __name__ == '__main__':
  app.debug = True
  app.run('0.0.0.0')