#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

def showTop(t):
  """Given a title string, prints the stuff needed at the top of our XHTML
  documents.
  """
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

