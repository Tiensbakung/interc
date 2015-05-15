#!/usr/bin/env python3
import os
import readline
import shutil
import subprocess
import sys
import tempfile

from autocompleter import AutoCompleter
import parser

completer = AutoCompleter()
readline.set_completer(completer.complete)
readline.read_init_file('linereader.rc')
default_dir = os.path.join(tempfile.gettempdir(), 'interc')
source_file = 'interc.cc'
o_start = 0

headers = set([
    '#include <unordered_map>',
    '#include <map>',
    '#include <iostream>',
    '#include "prettyprint.hpp"'
])

funcs = []

main_begin = '''
using namespace std;

int main()
{
'''

main_body = []

main_close = '''
    return 0;
}
'''


def s_type(tokens):
    if not tokens:
        return ''               # No code
    elif tokens[0] == '#':
        return '#INC'           # #include directive
    else:
        return 'CODE'           # code in main body


def is_brace_balance(snippet):
    c1 = sum([line.count('{') for line in snippet])
    c2 = sum([line.count('}') for line in snippet])
    return c1 == c2


def dump(fn, t, snippet):
    '''Dump the current source code to file `filename`.
    '''
    with open(fn, 'w') as f:
        f.write('\n'.join(headers))
        if t == '#INC':
            f.write('\n    ')
            f.write('\n    '.join(snippet))
        f.write('\n'.join(funcs))
        f.write(main_begin)
        f.write('    ')
        f.write('\n    '.join(main_body))
        if t == 'CODE':
            f.write('\n    ')
            f.write('\n    '.join(snippet))
        f.write(main_close)


def interpret(fn):
    try:
        subprocess.check_output(['clang++', '-std=c++11', '-o',
                                 'myprogram', fn],
                                stderr=subprocess.STDOUT)
#       subprocess.check_output(['g++', '-std=c++11', '-fsyntax-only',
#                                fn],
#                               stderr=subprocess.STDOUT)
        result = subprocess.check_output(['./myprogram'],
                                         stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(e.output.decode('utf-8'), file=sys.stderr)
        return None


def ic_read():
    '''Read function of REPL. Returns a code snippet.
    '''
    prompts = ('>>> ', '... ')
    imbalance = 0
    snippet = []
    while True:
        try:
            line = input(prompts[imbalance > 0])
        except (EOFError, KeyboardInterrupt):
            line = None

        if line is None:
            yield None
            snippet = []
        elif line.strip():      # Non-empty snippet
            snippet.append(line)
            imbalance = not is_brace_balance(snippet)
            if not imbalance:
                yield snippet
                snippet = []


def ic_eval(snippet):
    '''Eval function of REPL. Return code snippet excution output.
    '''
    global o_start
    tokens = parser.tokenize(''.join(snippet))
    t = s_type(tokens)
    if not t:
        return ''

    dump(source_file, t, snippet)
    output = interpret(source_file)
    if output is None:
        return None
    else:
        completer.learn(tokens)
        if t == '#INC':
            list(map(lambda x: headers.add(x.strip()), snippet))
        else:
            main_body.extend(snippet)
        i = o_start
        o_start = len(output)
        return output[i:]


def ic_print(output):
    if output is not None:
        print(output)


def main():
    reader = ic_read()
    while True:
        snippet = next(reader)
        if snippet is None:
            break
        output = ic_eval(snippet)
        ic_print(output)


if __name__ == '__main__':
    os.makedirs(default_dir, exist_ok=True)
    shutil.copy('prettyprint.hpp', default_dir)
    os.chdir(default_dir)
    main()
