#!/usr/bin/python2

# Microassembler for Tinystack. This doesn't do much except map mnemonics to
# nibbles and generate lit instruction sequences.

import sys
from argparse import ArgumentParser, FileType

import tinystack_emu

parser = ArgumentParser()
parser.add_argument('infile', nargs='?',
                    type=FileType('r'), default=sys.stdin)
parser.add_argument('-o', '--outfile',
                    nargs='?', type=FileType('w+'), default=sys.stdout)
args = parser.parse_args()

nibbles = []
for line in args.infile:
    line = line.strip().split(' ')
    if line == ['']: continue       # ignore blank lines
    if line[0][0] == ';': continue  # ignore lines which start with a comment
    if line[0] == 'align':
        if len(nibbles) & 1:
            nibbles.append(0)
        continue
    if line[0] == 'call':
        if len(nibbles) & 3 == 3:   # add a nop if we're in the last nibble
            nibbles.append(0)
    opcode = tinystack_emu.by_name[line[0]].opcode
    if line[0] == 'lit':
        lit = lambda x: nibbles.extend([opcode, x])
        n = int(line[1]) & 0xffff
        lit(n & 0xF)
        while n > 0xF:
            n >>= 4
            lit(n & 0xF)
    else:
        nibbles.append(opcode)

byte = 0
for i, nibble in enumerate(nibbles):
    if i % 2:
        byte |= nibble
        args.outfile.write(chr(byte))
    else:
        byte = nibble << 4

if not i % 2:
    args.outfile.write(chr(byte))
