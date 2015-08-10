from argparse import ArgumentParser, FileType
from sys import stdin

from tinystack_emu import by_opcode, Tinystack

parser = ArgumentParser()
parser.add_argument('infile', nargs='?', type=FileType('r'), default=stdin)
args = parser.parse_args()

pushl = False

def print_nibble(n):
    global pushl
    print hex(n)[2:], '\t',
    if pushl:
        pushl = False
        print
        return
    instr = by_opcode[n]
    print instr.__name__
    if instr.__name__ == 'pushl':
        pushl = True



for addr, byte in enumerate(map(ord, args.infile.read())):
    print addr, '\t',
    print_nibble(byte >> 4)
    print '\t',
    print_nibble(byte & 0xf)
