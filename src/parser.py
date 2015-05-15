import re

types = ('void', 'enum', 'union', 'class', 'struct', 'char', 'int', 'float',
         'double', 'unsigned', 'size_t', 'string')
containers = (
    'deque', 'list', 'map', 'multimap', 'multiset', 'queue', 'set', 'stack',
    'vector', 'unordered_map', 'unordered_multimap', 'unordered_multiset',
    'unordered_set'
)
m_funcs = (                     # common container member functions
    'at', 'assign', 'back', 'begin', 'clear', 'emplace', 'emplace_back',
    'emplace_front', 'empty', 'end', 'erase', 'front', 'insert', 'max_size',
    'pop', 'pop_back', 'pop_front', 'push', 'push_back', 'push_front',
    'remove', 'reverse', 'size', 'sort', 'swap', 'top'
)
controls = ('for', 'while', 'do')
streams = ('cout', 'cin')
others = ('NULL', 'auto', 'const', 'extern', 'sizeof', 'static', 'include')
keywords = types + containers + controls + m_funcs + streams + others

brackets = r'[()[\]{}]'
quotes = r'\'"'
operators = '|'.join(('<<=?', '>>=?', '->\*?', '\+{2}', '-{2}', '&{2}',
                      '\|{2}', '::?', '\.\*?', '[-+*/%&\|^!=<>]=?', '[,;?#$]'))
words = r'\w+'
tokens = (
    brackets,
    quotes,
    operators,
    words
)

_lexer = re.compile('|'.join(tokens))


def tokenize(s):
    return _lexer.findall(s)
