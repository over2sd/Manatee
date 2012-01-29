#!/usr/bin/python -tt

import sys
from jinja2 import (
        Environment,
        FileSystemLoader
        )
import os

def main():
    print "Content-Type: text/html\n\n"
    here = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(here))
    template = env.get_template('ccowhelp.jtl')
    print template.render(title='foo')


# Standard boilerplate to call the main()
if __name__ == '__main__':
  main()