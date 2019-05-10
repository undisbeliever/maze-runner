#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fenc=utf-8 ai ts=4 sw=4 sts=4 et:


import tmx
import argparse


def convert_tiles(layer, firstgid):
    tiles = layer.tiles

    if len(tiles) != 128 * 128:
        raise ValueError('Invalid number of tiles in layer')

    mode7_map = bytearray()

    for t in tiles:
        if t.hflip or t.vflip or t.dflip:
            raise ValueError('Mode 7 map does not support tile flipping')

        mode7_map.append(t.gid - firstgid)

    return mode7_map



def convert_map(tmx_map):
    if tmx_map.tilewidth != 8 or tmx_map.tileheight != 8:
        raise ValueError('tmx tile size must be 8x8px')

    if tmx_map.width != 128 or tmx_map.height != 128:
        raise ValueError('tmx map must be 128x128 tiles in size')

    if tmx_map.renderorder != 'right-down':
        raise ValueError('Map Render Order must be right-down.')

    if len(tmx_map.tilesets) != 1:
        raise ValueError('Only one tileset is accepted')

    if len(tmx_map.layers) != 1:
        raise ValueError('Only one layer is accepted')

    mode7_map = None

    for layer in tmx_map.layers:
        if type(layer) == tmx.Layer:
            if mode7_map:
                raise ValueError('Only one tile layer is allowed per tmx map')
            mode7_map = convert_tiles(layer, tmx_map.tilesets[0].firstgid)

    if not mode7_map:
        raise ValueError('No tile layer found')

    return mode7_map



def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True,
                        help='mode 7 map output file')
    parser.add_argument('tmx_file', action='store',
                        help='tmx input file')

    args = parser.parse_args()

    return args;


def main():
    args = parse_arguments()

    tmx_map = tmx.TileMap.load(args.tmx_file)

    mode7_map = convert_map(tmx_map)

    assert len(mode7_map) == 128 * 128

    with open(args.output, 'wb') as fp:
        fp.write(mode7_map)


if __name__ == '__main__':
    main()

