#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fenc=utf-8 ai ts=4 sw=4 sts=4 et:


import PIL.Image
import argparse
import struct


def convert_palette(palette, max_colors):
    if not palette:
        raise ValueError('Image must have a palette')

    data_type, pdata = palette.getdata()

    if data_type != 'RGB':
        raise ValueError('Image palette is invalid')

    n_colors = len(pdata) / 3
    if n_colors > max_colors:
        raise ValueError('Image palette has too many colors')

    snes_pal_data = bytearray()

    for c in struct.iter_unpack('BBB', pdata):
        r, g, b = c

        b = (b >> 3) & 31;
        g = (g >> 3) & 31;
        r = (r >> 3) & 31;

        u16 = (b << 10) | (g << 5) | r;

        snes_pal_data.append(u16 & 0xff);
        snes_pal_data.append(u16 >> 8);

    assert len(snes_pal_data) == n_colors * 2;

    return snes_pal_data



def extract_tiles(image, max_tiles):
    if image.width % 8 != 0 or image.height % 8 != 0:
        raise ValueError('Image width MUST BE a multiple of 8')

    if image.height % 8 != 0:
        raise ValueError('Image height MUST BE a multiple of 8')

    t_width = image.width // 8
    t_height = image.height // 8

    if t_width * t_height > max_tiles:
        raise ValueError('Too many tiles in image')

    img_data = image.getdata()

    for ty in range(t_height):
        ty *= 8
        for tx in range(t_width):
            tx *= 8

            tile_data = bytearray()

            for y in range(ty, ty + 8):
                for x in range(tx, tx + 8):
                    tile_data.append(image.getpixel((x, y)))

            yield tile_data


def convert_mode7_tileset(image):
    return bytes().join(extract_tiles(image, 256))

FORMATS = {
    'm7'    : convert_mode7_tileset,
    'mode7' : convert_mode7_tileset,
}


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--format', required=True,
                        choices=FORMATS.keys(),
                        help='tile format')
    parser.add_argument('-t', '--tileset-output', required=True,
                        help='tileset output file')
    parser.add_argument('-p', '--palette-output', required=True,
                        help='palette output file')
    parser.add_argument('-c', '--max-colors', required=False,
                        type=int, default=256,
                        help='maximum number of colors')
    parser.add_argument('image_filename', action='store',
                        help='Indexed png image')

    args = parser.parse_args()

    return args;


def main():
    args = parse_arguments()

    image = PIL.Image.open(args.image_filename)

    palette = convert_palette(image.palette, args.max_colors)
    tileset = convert_mode7_tileset(image)

    with open(args.tileset_output, 'wb') as fp:
        fp.write(tileset)

    with open(args.palette_output, 'wb') as fp:
        fp.write(palette)


if __name__ == '__main__':
    main()

