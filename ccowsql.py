#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from sqlalchemy import (create_engine, Column)

def unsql(strin):
  """Given a string, replaces SKR-type SQL-safe escapes with their unsafe counterparts."""
  strout = ""
  strout = strin.replace("~9","&")
  strout = strout.replace("~8","*")
  strout = strout.replace("~7","#")
  strout = strout.replace("~6","x")
  strout = strout.replace("~5","--")
  strout = strout.replace("~4","=")
  strout = strout.replace("~3",'"')
  strout = strout.replace("~2",";")
  strout = strout.replace("~1","'")
  strout = strout.replace("~0","~")
  return strout

def dosql(strin):
  """Given a string, replaces unsafe characters with SKR-type SQL-safe escapes."""
  strout = ""
  strout = strin.replace("~","~0")
  strout = strout.replace("*","~8")
  strout = strout.replace("#","~7")
  strout = strout.replace("x","~6",)
  strout = strout.replace("--","~5")
  strout = strout.replace("=","~4")
  strout = strout.replace('"',"~3")
  strout = strout.replace(";","~2")
  strout = strout.replace("'","~1")
  strout = strout.replace("&","~9")
  return strout

