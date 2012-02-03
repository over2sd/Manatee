#!/usr/bin/python -tt

from ccowprogress import (codeLoc, SKRED, SKGRN, SKYEL, L3W, L2W, L1W, L4O, L3O, L2O, timeStamper)
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
  print timeStamper()

#  print "Content-type: text/html\n\n"
  """
  l = ["0000","000x","00xx","0xxx","a102","ffff"]
  for i in l:
    t = codeLoc(i)
    print t[0]
  png = Image.new("RGBA",imgsize,SKRED)
  draw = ImageDraw.Draw(png)
  l = ["0","5","a","f"]
  c = SKYEL
  t = codeLoc("fa50")
  draw.point(t[0],c)
  c = SKGRN
  t = codeLoc("ffff")
  draw.point(t[0],c)
  print(">")
  c = SKGRN
  for i in l:
    x = "000" + i
    t = codeLoc(x)
    draw.point(t[0],c)
  c = SKYEL
  for i in l:
    x = "00" + i + "x"
    t = codeLoc(x)
#    print(t[1])
    a = t[0]
    b = (t[0][0] + t[1],t[0][1] + t[1])
    draw.rectangle([a,b], outline = c)
  c = SKGRN
  for i in l:
    x = "0" + i + "xx"
    t = codeLoc(x)
    a = t[0]
    b = (t[0][0] + t[1],t[0][1] + t[1])
    draw.rectangle([a,b], outline = c)
  c = SKYEL
  for i in l:
    x = i + "xxx"
    t = codeLoc(x)
    a = t[0]
    b = (t[0][0] + t[1],t[0][1] + t[1])
    draw.rectangle([a,b], outline = c)
  del draw
  png.save("test.png","PNG")
# """
  exit(0)

# Standard boilerplate to call the main()
if __name__ == '__main__':
  main()