#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
## old line: # coding: utf-8

import sys
import os
import codecs
from jinja2 import (Environment, FileSystemLoader)
from ccowi18n import (glot, glotCrumbs, glotCrumbs, glotSubs)
from ccowcgi import (cgi, cleanCode, chooseStyle, getStage)
from ccowsql import (create_engine)

BUILDNUM = "099"
MYNAME = os.path.basename(sys.argv[0])

def main():
  """Run if the program is called from the shell, of course."""
  print "Content-Type: text/html\n\n",

  lines = []
  config = {}
  var = {}
  try:
    with codecs.open('manatee.conf','rU','utf-8') as conf:
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

  here = os.path.dirname(os.path.abspath(__file__))
  env = Environment(loader=FileSystemLoader(here))
  template = env.get_template(os.path.join("template",'ccowhelp.jtl'))
  #  validateConfig(config)

  # Create connection to SQL server (currently MySQL)
  engine = create_engine("%(host)s/%(base)s" % {'host':config["host"],'base':config["base"] } )
  sqlconn = engine.connect()
  # Grab GET data from URL
  query = cgi.FieldStorage()
  lang = query.getvalue("lang","en")[:2]
  var['lang'] = lang
  langarg = query.getvalue("lang",None) # needed for query present, language not
  code = query.getvalue("cowc","XXXX")
  code = str(cleanCode(code))
  style = query.getvalue("style",None)
  if style: var['style'] = "style=" + style
  style = chooseStyle(style)
  if style: var['custom'] = style
  if "site" not in config:
    config['site'] = "Manatee"
  # check for query string
  if len(query) == 0 or langarg == None:
    # if no query, offer lang selection
    var['title'] = "Select Language"
  else:
  # if query provided, show a page...
    var['code'] = code
    var['title'] = var['code']
    var['dosnip'] = True
    showsubs = False
    stage = getStage(var['code'])
    cat00 = str(code[:stage])
    if stage > 0:
      var['cattrim'] = cat00
    if stage < 4:
      showsubs = True
      for i in range(4 - stage): cat00 += '0'
      var['catmul'] = cat00
      var['muldesc'] = glot(cat00,sqlconn,lang,4) # the multiplicity topic desc will be stage 4.
    var['catname'] = glot(code,sqlconn,lang,stage)
    if code[0] == 'y': # Explanation key
      if code[3] == 'x': # explain subcats
        var['expl'] = True
        var['catname'] = glot("sxpl",sqlconn,lang)
        stage = 3 # the subcat explanations are stage 4, so we need to consider yxxx to be stage 3.
      else: # explain a single subcat type
        del var['catmul']
        var['cattrim'] = '*' + code[3]
        stage = 4 # make sure we don't show subcats
        del var['dosnip']
        showsubs = False
    var['stage'] = stage
    var['catinf'] = os.path.join("cats",lang,code)
    var['crumbs'] = glotCrumbs(sqlconn,code,stage,lang)
    if len(var['crumbs']) > 0 and code[0] != 'X' and code[0] != 'x': var['crumbdiv'] = True
    var['border'] = cat00[:3]
    if showsubs:
      var['subcats'] = glotSubs(sqlconn,code,stage,lang)
  var['progress'] = glot("spro",sqlconn,lang)
#  print "<!-- Code: " + var['code'] + " stage " + str(var['stage']) + " language: " + var['lang'] + " -->"

  print template.render({'config': config, 'var': var}).encode("utf-8")
  sqlconn.close()
  exit(0)

# Standard boilerplate to call the main()
if __name__ == '__main__':
  main()