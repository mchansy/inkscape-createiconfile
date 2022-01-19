# coding=utf-8

# Copyright 2022 Sven Schork

# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "CreateIconFile"), to deal in the 
# Software without restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
# Software, and to permit persons to whom the Software is furnished to do so, subject 
# to the following conditions:

# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.

# 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from tempfile import tempdir
import inkex
from pathlib import Path
from PIL import Image
from inkex.command import inkscape
from inkex.base import TempDirMixin

class CreateIconFile (TempDirMixin, inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)

        self.arg_parser.add_argument('-t', '--iconfilename',
            type = str, dest = 'iconfilename', default = 'newicon.ico',
            help = 'The selected icon filename with path')

    def createIconFile(self, exportpar):
        # Write the global header
        number_of_sources = len(exportpar)
        data = bytes((0, 0, 1, 0, number_of_sources, 0))
        offset = 6 + number_of_sources * 16

        # Write the header entries for each individual image
        for exportfilepar in exportpar:
            img = Image.open(exportfilepar['filename'])
            # inkex.errormsg("Width: " + str(img.width) + ", Height: " + str(img.height))
            if (img.width >= 256): # Icon max size 256 needs to set the size bytes to zero
                data += bytes((0, 0, 0, 0, 1, 0, 32, 0, ))
            else:
                data += bytes((img.width, img.height, 0, 0, 1, 0, 32, 0, ))
            bytesize = Path(exportfilepar['filename']).stat().st_size
            data += bytesize.to_bytes(4, byteorder="little")
            data += offset.to_bytes(4, byteorder="little")
            offset += bytesize

        # Write the image data to the icon file
        for exportfilepar in exportpar:
            data += Path(exportfilepar['filename']).read_bytes()
        # Save the icon file
        Path(self.options.iconfilename).write_bytes(data)

        return data

    def effect(self):
        try:
            svg = self.svg
            # inkex.utils.debug("start create icon: " + self.options.iconfilename)
            
            # inkex.utils.debug("TempDir: " + self.tempdir)
            export = [
                {'filename': self.tempdir + "/" + "image_016.png", 'size': 16, 'dpi': 96},
                {'filename': self.tempdir + "/" + "image_024.png", 'size': 24, 'dpi': 96},
                {'filename': self.tempdir + "/" + "image_032.png", 'size': 32, 'dpi': 96},
                {'filename': self.tempdir + "/" + "image_048.png", 'size': 48, 'dpi': 96},
                {'filename': self.tempdir + "/" + "image_064.png", 'size': 64, 'dpi': 96},
                {'filename': self.tempdir + "/" + "image_072.png", 'size': 72, 'dpi': 96},
                {'filename': self.tempdir + "/" + "image_096.png", 'size': 96, 'dpi': 96},
                {'filename': self.tempdir + "/" + "image_128.png", 'size': 128, 'dpi': 96},
                {'filename': self.tempdir + "/" + "image_180.png", 'size': 180, 'dpi': 96},
                {'filename': self.tempdir + "/" + "image_256.png", 'size': 256, 'dpi': 96},
            ]

            for exportfilepar in export:
                inkscape(self.options.input_file, export_dpi=exportfilepar['dpi'], export_filename=exportfilepar['filename'], export_width=exportfilepar['size'], export_height=exportfilepar['size'])

            self.createIconFile(export)

            # inkex.utils.debug("finished")
        except Exception as e:
            inkex.errormsg("Exception! %s " % e.message)

effect = CreateIconFile()
effect.run()