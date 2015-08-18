#!/usr/bin/python2

# Microassembler for Tinystack. This doesn't do much except map mnemonics to
# nibbles and generate lit instruction sequences.

from tinystack_emu import *

parser = ArgumentParser()
parser.add_argument('infile', nargs='?',
                    type=FileType('r'), default=sys.stdin)
parser.add_argument('-o', '--outfile',
                    nargs='?', type=FileType('w+'), default=sys.stdout)
args = parser.parse_args()

nibbles = []
macros = {}
labels = {}


def align(nibbles):
    return nibbles.append(0) if len(nibbles) & 1 else 0


def emit_lit(n):
    lit = lambda x: nibbles.extend([Tinystack.lit_instr.opcode, x])
    lit(n & 0xF)
    while n > 0xF:
        n >>= 4
        lit(n & 0xF)


def proc_line(line):
    global nibbles
    line = line.strip().split(' ')
    if line == ['']: return  # ignore blank lines
    first = line[0]
    if first[0] == ';': return  # ignore lines which start with a comment
    if first[-1] == ':':
        align(nibbles)
        labels[first.strip(':')] = len(nibbles) / 2
    if first == 'align':
        return align(nibbles)
    if first == 'skip':
        nibbles.append(0) if len(nibbles) & 3 == 3 else 0
    if first == 'call':
        align(nibbles)
    if first == 'include':
        return map(proc_line, open(line[1]))
    if first[-2:] == '.s':
        return map(proc_line, open(first))
    if first == 'defmacro':
        return macros.update({line[1]: line[2:]})
    try:
        return emit_lit(int(first, 0) & 0xffff)
    except ValueError:  # not a number
        pass
    if first in by_name:
        return nibbles.append(by_name[first].opcode)
    return map(proc_line, macros[first])


map(proc_line, args.infile)

byte = 0
for i, nibble in enumerate(nibbles):
    if i % 2:
        byte |= nibble
        args.outfile.write(chr(byte))
    else:
        byte = nibble << 4

if not i % 2:
    args.outfile.write(chr(byte))
