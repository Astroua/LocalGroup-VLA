
'''
Make pb-corrected image cube
'''

import sys

from tasks import impbcor, exportfits


imgname = sys.argv[-2]
pbname = sys.argv[-1]

# Run impbcor for an image

impbcor(imagename=imgname,
        pbimage=pbname,
        outfile="{}.fits".format(imgname),
        overwrite=True)
