#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fenc=utf-8 ai ts=4 sw=4 sts=4 et:

# This file is part of Maze Runner.
# Copyright (c) 2019, Marcus Rowe <undisbeliever@gmail.com>.
# Distributed under The MIT License, see the LICENSE file for more details.

"""
Generator for the Mode 7 perspective HDMA tables.

The formula for the transformation (with clockwise rotation) is:

    M7A =  cos(θ) * scale/(scanline+1)
    M7B =  sin(θ) * scale/(scanline+1)
    M7C = -sin(θ) * scale/(scanline+1)
    M7D =  cos(θ) * scale/(scanline+1)  // Duplicate of M7A


This effect requires 3 HDMA channels.

    Channel 1: M7A          (one register write twice)
    Channel 2: M7B & M7C    (two registers write twice)
    Channel 3: M7D - Pointing to the same data as M7A
"""

import math

RODATA_BLOCK = 'rodata0';

DIRECTION_ROTATION_SHIFT = 2 # Rotate the map 90 degrees in 4 frames
N_SCANLINES = 224
SCALE = 64

N_ROTATIONS = 4 << DIRECTION_ROTATION_SHIFT


def float_to_fp_bytes(f):
    i = int(f * 256)
    if i < 0:
        i = 0x10000 + i
    if i > 0xFFFF:
        i %= 0xFFFF

    return (i & 0xff, i >> 8)


def mode7_hdma_tables(r):
    r = r / N_ROTATIONS * 2 * math.pi

    table_a = bytearray()
    table_bc = bytearray()

    line_count = 0
    for s in range(N_SCANLINES):
        if line_count == 0:
            line_count = min(127, N_SCANLINES - s)
            nltr = line_count | 0x80
            table_a.append(nltr)
            table_bc.append(nltr)
        line_count -= 1

        a =  math.cos(r) * SCALE / (s + 1)
        b =  math.sin(r) * SCALE / (s + 1)
        c = -math.sin(r) * SCALE / (s + 1)

        table_a.extend(float_to_fp_bytes(a))
        table_bc.extend(float_to_fp_bytes(b))
        table_bc.extend(float_to_fp_bytes(c))

    table_a.append(0)
    table_bc.append(0)

    return table_a, table_bc


def main():
    ROTATION_MASK   = N_ROTATIONS - 1

    TABLE_A_SIZE    = N_SCANLINES * 2 + 3
    TABLE_BC_SIZE   = N_SCANLINES * 4 + 3

    print( 'import "../src/memmap";')
    print()
    print( 'namespace mode7_hdma_data {')
    print(f"in {RODATA_BLOCK} {{")
    print(f"\tlet N_ROTATIONS = {N_ROTATIONS};")
    print(f"\tlet ROTATION_MASK = {ROTATION_MASK};")
    print(f"\tlet DIRECTION_ROTATION_SHIFT = {DIRECTION_ROTATION_SHIFT};")
    print()
    print(f"\tlet TABLE_A_SIZE = {TABLE_A_SIZE};")
    print(f"\tlet TABLE_BC_SIZE = {TABLE_BC_SIZE};")
    print()
    print( '\t// List of concatenated HDMA tables for each rotation')
    print( '\t//\ttable_a = tables[r]')
    print( '\t//\ttable_bc = tables[r] + TABLE_A_SIZE')
    print( '\tconst tables : [*const u8] = [')

    for r in range(N_ROTATIONS):
        table_a, table_bc = mode7_hdma_tables(N_ROTATIONS - r)

        assert(len(table_a) == TABLE_A_SIZE)
        assert(len(table_bc) == TABLE_BC_SIZE)

        print('\t\t@[ ', table_a[0], 'u8', sep='', end='')

        for i in table_a[1:]:
            print(',', i, end='')
        for i in table_bc:
            print(',', i, end='')

        print('],')

    print('\t];')
    print('}')
    print('}')
    print()


if __name__ == '__main__':
    main()

