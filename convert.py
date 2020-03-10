#!/usr/bin/env python3

"""
Asynchronously generates an MD5 hash for every image in the in/ directory,
then moves them to a specified directory before running wpg -a on them.
"""

import asyncio
import argparse

from subprocess import run
from hashlib import md5
from PIL import Image
from os import rename
from filetype import guess


class MissingExecutableException(Exception):
    """
    Raised if wpg executable is not found in the user's PATH.
    """
    pass


class ImageMD5:
    def __init__(self, wpg, outpath, images):
        self.outpath = outpath
        if self.outpath[-1] != '/':
            self.outpath = outpath + '/'
        self.images = images
        self.wpg = wpg

    async def get_files(self):
        for file in self.images:
            yield file

    async def test(self):
        print(self.outpath)

    async def conversion(self):
        async for filename in self.get_files():
            md5hash = md5(Image.open(filename).tobytes())
            filetype = guess(filename)
            new_file = f'{self.outpath}{md5hash.hexdigest()}.{filetype.extension}'

            try:
                rename(filename, new_file)
            except Exception as exception:
                raise exception
            finally:
                print(f'Moved {filename}\n to: {new_file}')

            if self.wpg:
                try:
                    run(['wpg', '-a', new_file])
                except Exception:
                    raise MissingExecutableException


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate md5 hashes from images, rename them, '
                                                 'move them, and optionally run wpg on them.')
    parser.add_argument('-o', '--out', default='/home/valkyrie/.papes/',
                        type=str, help='Directory where converted images are outputted.')
    parser.add_argument('-w', '--wpg',
                        action='store_true', help='Run wpg on the converted images.')
    parser.add_argument('FILES', nargs='+', help='Files to be converted.')

    args = vars(parser.parse_args())
    asyncio.run(ImageMD5(args['wpg'], args['out'], args['FILES']).conversion())
