#!/usr/bin/python2

# Microassembler for Tinystack. This doesn't do much except map mnemonics to
# nibbles and generate pushl instruction sequences.

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
    if line == ['']: continue
    if line[0][0] == ';': continue
    opcode = tinystack_emu.by_name[line[0]].opcode
    if line[0] == 'pushl':
        pushl = lambda x: nibbles.extend([opcode, x])
        n = int(line[1]) & 0xffff
        pushl(n & 0xF)
        while n > 0xF:
            n >>= 4
            pushl(n & 0xF)
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
