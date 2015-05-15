import bisect
from collections import defaultdict
import readline

import parser


class AutoCompleter:

    def __init__(self):
        self.tags = defaultdict(list)
        v = sorted(parser.types + parser.containers + parser.controls +
                   parser.streams + parser.others)
        self.tags['$'].extend(v)
        self.tags['.'].extend(sorted(parser.m_funcs))
        self.tags['->'].extend(sorted(parser.m_funcs))

    def _add(self, prev, word):
        l = bisect.bisect_left(self.tags[prev], word)
        r = bisect.bisect_right(self.tags[prev], word)
        if l == r:
            self.tags[prev].insert(l, word)

    def complete(self, text, state):
        # print(text, ':', state)
        if state == 0:
            line = '$' + readline.get_line_buffer()
            words = parser.tokenize(line)
            if words[-1].isidentifier():
                self.pretext = text[:-len(words[-1])]
                self.prev = words[-2]
                text = words[-1]
            else:
                self.pretext = text
                self.prev = words[-1]
                text = ''
            utext = text.ljust(200, '~')
            self.l = bisect.bisect_left(self.tags[self.prev], text)
            self.r = bisect.bisect_right(self.tags[self.prev], utext)
            # print()
            # print(self.pretext, self.prev, text, self.l, self.r)
        try:
            return self.pretext+self.tags[self.prev][self.l:self.r][state]
        except IndexError:
            return None

    def learn(self, tokens):
        for k, v in zip(['$']+tokens, tokens):
            if len(v) > 2:
                self._add(k, v)


def main():
    completer = AutoCompleter(['unordered_map', 'unordered_set', 'list',
                               'print'])
    readline.set_completer(completer.complete)
    readline.read_init_file('linereader.rc')
    while True:
        line = input('["Q" to quit]: ')
        if line.strip() == 'Q':
            break
        else:
            completer.learn(parser.tokenize(line))


if __name__ == '__main__':
    main()
