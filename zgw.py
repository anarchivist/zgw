"""
zgw.py: a lightweight Z39.50/Web gateway
Copyright (c) 2007-2008, Mark A. Matienzo
"""

import pymarc
import web
from PyZ3950 import zoom
from parsers import Parser

urls = (
  '/', 'usage',
  '/search/(.*)', 'search',
  '/validate/(.*)', 'validate'
)

server = {
  'host': 'z3950.loc.gov',
  'port': 7090,
  'db': 'VOYAGER',
  'query_language': 'CCL'
}

#commented out as this is just an example and not yet totally implemented
#server_uri = 'z39.50s://z3950.loc.gov:7090/VOYAGER'
#server = Parser().parse_uri(server_uri)

render = web.template.render('templates/')
zoom.ResultSet.__bases__ += (Parser,)
pymarc.Field.__bases__ += (Parser,)
pymarc.Record.__bases__ += (Parser,)

def run_query(server, qs):
  """Creates Z39.50 connection, sends query, serializes and humanizes results"""
  conn = zoom.Connection(server['host'], server['port'], databaseName=server['db'])
  out = []
  query = zoom.Query(server['query_language'], qs)
  result_set = conn.search(query)
  reader = result_set.pymarc_deserialize()
  conn.close()
  for result in reader:
    out.append(result.humanize())
  return out

class search:
  """web.py class for submitting a Z39.50 query and returning results"""
  def GET(self, query_string):
    print render.base(server=server['host'], query_string=query_string)
    results = run_query(server, query_string)
    print render.search(query_string=query_string, results=results, total=len(results))

class usage:
  """web.py class to display usage information"""
  def GET(self):
    print render.usage()
    
class validate:
  """web.py class to validate Z39.50 URIs"""
  def GET(self, uri):
    print Parser().parse_uri(uri)

web.webapi.internalerror = web.debugerror
if __name__ == '__main__': web.run(urls, globals())
