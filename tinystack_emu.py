#!/usr/bin/python2

# Emulator for Tinystack

import sys
from argparse import ArgumentParser, FileType
from itertools import chain

by_opcode = {}
by_name = {}

def instruction(opcode):
    def instruction_(f):
        def call_instr(cpu):
            return f(cpu)

        call_instr.opcode = opcode
        call_instr.__name__ = f.__name__.split('_')[0]
        by_opcode[opcode] = call_instr
        by_name[call_instr.__name__] = call_instr
        return call_instr
    return instruction_


class Tinystack(object):
    @instruction(0x0)
    def swap_instr(cpu):
        "swap x and y"
        x, y = cpu.stack.pop(), cpu.stack.pop()
        cpu.stack.append(x), cpu.stack.append(y)

    @instruction(0x1)
    def and_instr(cpu):
        "bitwise AND x and y, store result in x"
        cpu.stack.append(cpu.stack.pop() & cpu.stack.pop())

    @instruction(0x2)
    def or_instr(cpu):
        "bitwise OR x and y, store result in x"
        cpu.stack.append(cpu.stack.pop() | cpu.stack.pop())

    @instruction(0x3)
    def xor_instr(cpu):
        "bitwise XOR x and y"
        cpu.stack.append(cpu.stack.pop() ^ cpu.stack.pop())

    @instruction(0x4)
    def add_instr(cpu):
        "add x and y, unsigned"
        cpu.stack.append((cpu.stack.pop() + cpu.stack.pop()) & 0xffff)

    @instruction(0x5)
    def mul_instr(cpu):
        "multiply x and y, unsigned"
        cpu.stack.append((cpu.stack.pop() * cpu.stack.pop()) & 0xffff)

    @instruction(0x6)
    def save_instr(cpu):
        "pop a value from the stack and push it onto the stash"
        cpu.stash.append(cpu.stack.pop())

    @instruction(0x7)
    def disc_instr(cpu):
        "pop x and drop it on the floor"
        cpu.stack.pop()

    @instruction(0x8)
    def pushl_instr(cpu):
        "push a literal nibble"
        if cpu.last_pushl != cpu.cycle_count - 1 or cpu.pushl_shift == 16:
            cpu.pushl_shift = 0
        if not cpu.pushl_shift:
            cpu.stack.append(0)
        cpu.pushl_next = True
        cpu.last_pushl = cpu.cycle_count

    @instruction(0x9)
    def skip_instr(cpu):
        "IP += x; push old IP+1 onto the stack"
        offset = cpu.stack.pop()
        cpu.stack.append(cpu.ip + 1)
        if not offset: return
        cpu.new_ip = (cpu.ip + 1 + offset) & 0xFFFF

    @instruction(0xa)
    def sign_instr(cpu):
        "fill x with x's high bit. That is, 0xa99f -> 0xffff, 0x4485 -> 0x0000"
        cpu.stack.append(0xFFFF if cpu.stack.pop() & 0x8000 else 0)

    @instruction(0xb)
    def neg_instr(cpu):
        "x = -x"
        cpu.stack.append((~cpu.stack.pop() + 1) & 0xffff)

    @instruction(0xc)
    def ld_instr(cpu):
        "x = *x"
        x = cpu.stack.pop()
        value = cpu.mem[x]
        if not x & 1:
            value = (value << 8) | cpu.mem[x + 1]
        cpu.stack.append(value)

    @instruction(0xd)
    def st_instr(cpu):
        "*x = y; x = (x+2)"
        x = cpu.stack.pop()
        y = cpu.stack.pop()
        if y & 1:
            cpu.mem[y] = x & 0xff
        else:
            cpu.mem[y] = x & 0xff00
            cpu.mem[y + 1] = x & 0x00ff
        cpu.stack.append((y + 2) & (~1))

    @instruction(0xe)
    def dup_instr(cpu):
        "duplicate the top of the stack"
        cpu.stack.append(cpu.stack[-1])

    @instruction(0xf)
    def rstor_instr(cpu):
        "pop a value from the stash and push it onto the stack"
        cpu.stack.append(cpu.stash.pop())

    def __init__(self, memory):
        self.ip = 0
        self.cycle_count = 0
        self.mem = memory
        self.stack = []
        self.stash = []
        self.last_pushl = -2
        self.pushl_shift = 16
        self.pushl_next = False
        self.new_ip = None
        self.half = 0

    def execute_instruction(self, instr):
        print self.ip,
        if self.pushl_next:
            self.stack[-1] |= (instr << self.pushl_shift)
            self.pushl_next = False
            self.pushl_shift += 4
            print '\t',
        else:
            instr = by_opcode[instr]
            print '\t', instr.__name__,
            instr(self)
            self.cycle_count += 1
        print '\t', ' '.join(map(str, chain(self.stack, '|', reversed(self.stash))))

    def step_once(self):
        if self.half:
            self.execute_instruction(self.mem[self.ip] & 0x0F)
        else:
            self.execute_instruction(self.mem[self.ip] >> 4)
        if self.half:
            self.ip += 1
        self.half ^= 1

    def step_until(self, end_addr):
        while self.ip < end_addr:
            self.step_once()
            if self.new_ip is not None:
                # We cannot skip in the last quarter of a word
                assert self.half or (self.ip & 1)
                self.step_once()
                self.ip = self.new_ip
                self.half = 0
                self.new_ip = None


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('infile', nargs='?', type=FileType('r'), default=sys.stdin)
    args = parser.parse_args()
    memory = map(ord, args.infile.read())
    Tinystack(memory + [0] * (65536 - len(memory))).step_until(len(memory))
