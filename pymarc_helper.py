from PyZ3950 import zoom
from pymarc import MARCReader, marc8_to_unicode

class Serializer:
  """Serializes a PyZ3950.zoom.ResultSet object as a pymarc.MARCReader object"""
  def pymarc_serialize(self):
    result_list = []
    for result in self:
      result_list.append(result.data)
    return MARCReader("".join(result_list))

class Humanizer:
  def humanize(self):
    h = self.__str__()
    h = h.replace('\n', '<br/>')
    return marc8_to_unicode(h)
#