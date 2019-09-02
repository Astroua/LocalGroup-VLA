
'''
Convert concatenated cube to FITS.

'''

import sys

from tasks import exportfits


imgname = sys.argv[-1]

# Run impbcor for an image

impbcor(imagename=imgname,
        fitsimage="{0}".format(imgname),
        dropdeg=True,
        velocity=True,
        optical=False,
        history=False)
