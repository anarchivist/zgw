#!/usr/bin/env python
"""
zgw.py: a lightweight Z39.50/Web gateway
Copyright (c) 2007-2008, Mark A. Matienzo
"""

import pymarc
import web
from PyZ3950 import zoom
from parsers import ParseError, Parser
from settings import ELEMENT_SET_NAME, QUERY_SYNTAX, RESULT_SYNTAX, SERVER

urls = (
  '/', 'usage',
  '/search/(.*)', 'search'
)

render = web.template.render('templates/')
zoom.ResultSet.__bases__ += (Parser,)
pymarc.Record.__bases__ += (Parser,)
p = Parser()

def run_query(server, qs):
  """Creates Z39.50 connection, sends query, parses results"""
  conn = zoom.Connection(SERVER['host'], SERVER['port'],
                         databaseName=SERVER['db'],
                         preferredRecordSyntax=RESULT_SYNTAX,
                         elementSetName=ELEMENT_SET_NAME)
  out = []
  query = zoom.Query(QUERY_SYNTAX, qs)
  result_set = conn.search(query)
  for result in result_set:
    if result.syntax == 'USMARC':
      r = pymarc.Record(data=result.data)   # deserialize
      conv_record = r.to_unicode()          # serialize, encode, htmlify
    elif result.syntax in ('SUTRS', 'XML'): # doesn't account for MARC8 text
      conv_record = p.to_html(result.data)
    else:
      raise 
    out.append(conv_record)
  conn.close()
  return out

class search:
  """web.py class for submitting a Z39.50 query and returning results"""
  def GET(self, query_string):
    print render.base(server=SERVER['host'], query_string=query_string)
    results = run_query(SERVER, query_string)
    print render.search(query_string=query_string, results=results,
                        total=len(results))

class usage:
  """web.py class to display usage information"""
  def GET(self):
    print render.usage()
    
web.webapi.internalerror = web.debugerror
if __name__ == '__main__':
  web.run(urls, globals())
