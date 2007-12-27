import re, web
from PyZ3950 import zoom
from pymarc import marc8_to_unicode

urls = (
  '/search/(\S*)', 'search'
)

render = web.template.render('search.html')

def run_query(c, qs):
  out = []
  query = zoom.Query('CCL', qs)
  results = c.search(query)
  for result in results:
    out.append(marc8_to_unicode(result.__str__()))
  return out

class search:
  def GET(self, query_string):
    zconn = zoom.Connection('z3950.loc.gov', 7090, databaseName='VOYAGER')
    results = run_query(zconn, query_string)
    print render(query_string=query_string, results=results)
    zconn.close()
  
  def POST(self):
    zconn = zoom.Connection('z3950.loc.gov', 7090, databaseName='VOYAGER')
    query_string = web.input()
    results = run_query(zconn, query_string)
    print render(query_string=query_string, results=results)
    zconn.close()

web.webapi.internalerror = web.debugerror
if __name__ == '__main__': web.run(urls, globals())