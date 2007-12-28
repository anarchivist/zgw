import pymarc, web
from PyZ3950 import zoom
from parsers import Parser, ParseError

server_uri = 'z39.50s://z3950.loc.gov:7090/VOYAGER'

urls = (
  '/', 'usage',
  '/search/(.*)', 'search',
  '/parse/(.*)', 'parse'
)

render = web.template.render('/home/matienzo/Desktop/python/zgw/templates')
zoom.ResultSet.__bases__ += (Parser,)
pymarc.Field.__bases__ += (Parser,)
pymarc.Record.__bases__ += (Parser,)
server = Parser().parse_uri(server_uri)

def run_query(server, qs):
  conn = zoom.Connection(server['host'], server['port'], databaseName=server['db'])
  out = []
  query = zoom.Query('CCL', qs)
  result_set = conn.search(query)
  reader = result_set.pymarc_serialize()
  conn.close()
  for result in reader:
    out.append(result.humanize())
  return out

class parse:
  def GET(self, uri):
    print Parser().parser.parse_uri(uri)
    
  def POST(self):
    print Parser().parser.parse_uri(web.input())

class search:
  def GET(self, query_string):
    print render.base(server=server['host'], query_string=query_string)
    results = run_query(server, query_string)
    print render.search(query_string=query_string, results=results, total=len(results))
  
  def POST(self):
    query_string = web.input()
    print render.base(server=server['host'], query_string=query_string)
    results = run_query(server, query_string)
    print render.search(query_string=query_string, results=results, total=len(results))

class usage:
  def GET(self):
    print render.usage()

web.webapi.internalerror = web.debugerror
if __name__ == '__main__': web.run(urls, globals())