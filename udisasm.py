#!/usr/bin/python2

# Disassembler for Tinystack

from argparse import ArgumentParser, FileType
from sys import stdin

from tinystack_emu import by_opcode

parser = ArgumentParser()
parser.add_argument('infile', nargs='?', type=FileType('r'), default=stdin)
args = parser.parse_args()

lit = False

def print_nibble(n):
    global lit
    print hex(n)[2:], '\t',
    if lit:
        lit = False
        print
        return
    instr = by_opcode[n]
    print instr.__name__
    if instr.__name__ == 'lit':
        lit = True



for addr, byte in enumerate(map(ord, args.infile.read())):
    print addr, '\t',
    print_nibble(byte >> 4)
    print '\t',
    print_nibble(byte & 0xf)
