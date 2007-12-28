import pymarc, web
from PyZ3950 import zoom
from pymarc_helper import Serializer, Humanizer

urls = (
  '/search/(\S*)', 'search'
)

render = web.template.render('/home/matienzo/Desktop/python/zgw/templates')
zoom.ResultSet.__bases__ += (Serializer,)
pymarc.Field.__bases__ += (Humanizer,)
pymarc.Record.__bases__ += (Humanizer,)

def run_query(c, qs):
  out = []
  query = zoom.Query('CCL', qs)
  result_set = c.search(query)
  reader = result_set.pymarc_serialize()
  for result in reader:
    out.append(result.humanize())
  return out

class search:
  def GET(self, query_string):
    zconn = zoom.Connection('z3950.loc.gov', 7090, databaseName='VOYAGER')
    results = run_query(zconn, query_string)
    print render.search(query_string=query_string, results=results, total=len(results))
    zconn.close()
  
  def POST(self):
    zconn = zoom.Connection('z3950.loc.gov', 7090, databaseName='VOYAGER')
    query_string = web.input()
    results = run_query(zconn, query_string)
    print render.search(query_string=query_string, results=results, total=len(results))
    zconn.close()

web.webapi.internalerror = web.debugerror
if __name__ == '__main__': web.run(urls, globals())