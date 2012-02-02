#!/usr/bin/python -tt

# import ccowprogress
from PIL import (Image, ImageDraw)
import glob, os
from cgi import escape

imgsize = 424, 424

def main():
  if "HTTP_HOST" in os.environ:
    print "Content-Type: text/html\n\n"
    print "<html><body>This program is not CGI. Please run from the command line. To view this program's output, load <a href=\"progress.htm\">progress.htm</a></body></html>"
    exit(0)
  else:
    print "Run from command line. All okay."

#  print "Content-type: text/html\n\n"
  for k in sorted(os.environ):
    print " %s:\t\t%s \t\t<br />" %(escape(k), escape(os.environ[k]))

"""
  png = Image.new("RGBA",imgsize,ccowprogress.SKRED)
#  png.putpixel((ccowprogress.L4O + 2,ccowprogress.L4O + 5),ccowprogress.SKGREEN)
  draw = ImageDraw.Draw(png)
  draw.point((ccowprogress.L4O + 2,ccowprogress.L4O + 5),ccowprogress.SKGRN)
  draw.rectangle([(200,200),(ccowprogress.L3W + 200,ccowprogress.L3W + 200)], outline = ccowprogress.SKGRN)
  del draw
  png.save("test.png","PNG")
  exit(0)
"""

# Standard boilerplate to call the main()
if __name__ == '__main__':
  main()