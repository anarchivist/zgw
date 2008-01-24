"""
settings.py - for zgw.py
"""

"""
Element set names vary from host to host; e.g. for result syntax XML at
LC, the following are available: 'dc', 'mods', 'marcxml', 'opacxml'. Treat
'F' as the default unless you know you need something else.
"""
ELEMENT_SET_NAME = 'F'

"""
IGNORE_UNICODE_ERRORS does what it says; see parsers.py for the related
implementation. I specifically added this as the EACC records from the Library
of Congress can make pymarc.marc8_to_unicode fail. See
http://www.loc.gov/z3950/lcserver.html#limt for more information.
"""
IGNORE_UNICODE_ERRORS = False

"""
As of PyZ3950 2.04, the following query syntaxes are supported: CCL, S-CCL,
CQL, S-CQL, PQF, C2, SQL, CQL-TREE. See PyZ3950 docs for more information.
"""
QUERY_SYNTAX = 'CCL'

"""
As of PyZ3950 2.04, the following result syntaxes are supported: EXPLAIN,
GRS-1, OPAC, SUTRS, USMARC, XML. zgw does not currently parse GRS-1, OPAC
or EXPLAIN records.
"""
RESULT_SYNTAX = 'USMARC'

"""
SERVER specifies the Z39.50 server for queries. All elements of this
dictionary are required. Sample server entries:

SERVER = {'host': 'library.usc.edu', 'port': 2200, 'db': 'unicorn'}
SERVER = {'host': 'z3950cat.bl.uk, 'port': 9909, 'db': 'BLAC'} # returns SUTRS
"""
SERVER = {'host': 'z3950.loc.gov', 'port': 7090, 'db': 'VOYAGER'}

