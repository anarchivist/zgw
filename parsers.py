from web.net import htmlquote
from pymarc import MARCReader, marc8_to_unicode

class ParseError(Exception):
  """Base class for exceptions from this module"""
  pass

class URIParseError(ParseError):
  def __init__(self, _reason):
    self.reason = _reason
    ParseError.__init__(self)
    
  def __str__(self):
    return self.reason

class Parser:
  """Base class for parsers used by zgw"""
  
  def humanize(self):
    """Humanizes a pymarc.Field or pymarc.Record object.
    
    Uses the string methods of pymarc to generate MARCBreaker format data.
    Newlines are prettified into line break tags, and then the ANSEL characters
    are encoded into Unicode."""
    marc = self.__str__()
    h = htmlquote(marc)
    h = h.replace('\n', '<br/>\n')
    return marc8_to_unicode(h) 
  
  def parse_uri(self):
    """Parse a Z39.50 URL in RFC 2056 format - not completely implemented"""
    uri = self

    def pull(v, q, index):
      _i = index + 1, v.find(q, index)
      return v[_i[0]:_i[1]], _i[1]
    
    if uri[0:10] == 'z39.50s://':
      host, _index = pull(uri, ':', 9)
      port, _index = pull(uri, '/', _index)
      if uri.find('?') == -1:
        db = uri[_index + 1:]
        query = None
      else:
        db, _index = pull(uri, '?', _index)
        query = uri[_index + 1:]
        if uri.find('&') <> -1:
          #to be implemented...
          pass
      return {'host': host, 'port': int(port), 'db': db, 'query': query}
    elif uri[0:10] == 'z39.50r://':
      raise URIParseError('URI scheme "z39.50r:" not yet implemented')
    else:
      raise URIParseError('%s is not a valid Z39.50 URI' % uri)
  
  def pymarc_deserialize(self):
    """De serializes a PyZ3950.zoom.ResultSet object as a pymarc.MARCReader object"""
    result_list = []
    for result in self:
      result_list.append(result.data)
    return MARCReader("".join(result_list))
