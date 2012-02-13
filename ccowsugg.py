#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

BUILD = "002"

from jinja2 import (Environment, FileSystemLoader)
from ccowi18n import (glot, glotCrumbs, glotCrumbs, glotSubs)
from ccowcgi import (cgi, loadConfig, cleanCode, chooseStyle, getStage, formClean)
from ccowsql import (create_engine)
from flask import (Flask, render_template, request, url_for)
app = Flask(__name__,instance_relative_config=True)

import sys
import os
MYNAME = os.path.basename(sys.argv[0])


@app.route('/suggest', methods=['GET', 'POST'])
def suggest():
  config = loadConfig()
  var = {}
  var['build'] = BUILD
  # check for input
#  query = cgi.FieldStorage()
  lang = request.values.get("lang","en")[:2]
  var['lang'] = lang
  code = request.values.get("scod",None)
  if code:
    var['scod'] = str(cleanCode(code)).lower()
  else:
    var['showerr'] = True
    var['showform'] = False
    var['scod'] = "----"
    var['error'] = "You must provide a code. Please try again."
  desc = request.values.get("sdesc","[Suggestion]")
  var['sdesc'] = formClean(desc)
  rationale = request.values.get("srat","[Rationale]")
  var['srat'] = formClean(rationale)
  style = request.values.get("style",None)
  if style: var['style'] = style
  style = chooseStyle(style)
  if style: var['custom'] = url_for('static', filename=style + ".css")
  if "site" not in config:
    config['site'] = "Manatee"
  var['title'] = "Suggest a Category"
  # if no input, display form
  if desc[0] == '[': var['showform'] = True
  # check input validity
  # ccode
  if var['scod'] == "xxxx" or str(var['scod']).find('y') != -1:
    var['showform'] = False
    var['showerr'] = True
    var['error'] = "You have entered an invalid CCOW code. You may not suggest new names for the top-level category or explanation categories. Please try again."
  # make a connection
  # category already assigned?
  # maybe a field for reasoning?
  # suggested category text
  # if it's all good, insert a row into the suggestions table
  # if bad input, display form
# """
  return render_template("suggest.jtl", config=config, var=var)

if __name__ == '__main__':
  app.debug = True
  app.run('0.0.0.0')