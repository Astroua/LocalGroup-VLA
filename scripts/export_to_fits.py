
'''
Convert concatenated cube to FITS.

'''

import sys

from tasks import exportfits


imgname = sys.argv[-1]

exportfits(imagename=imgname,
           fitsimage="{0}.fits".format(imgname),
           dropdeg=True,
           velocity=True,
           optical=False,
           history=False)
