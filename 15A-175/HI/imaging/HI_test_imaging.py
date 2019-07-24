
'''
Image a channel in B and C separately, w/ and w/o contsub.

Just make sure the split and contsub went well.
'''


myviss = ['15A-175_Btracks_HI_spw_0_LSRK.ms',
          '15A-175_Btracks_HI_spw_0_LSRK.ms.contsub',
          '15A-175_Ctracks_HI_spw_0_LSRK.ms',
          '15A-175_Ctracks_HI_spw_0_LSRK.ms.contsub']


for myvis in myviss:

    tclean(vis=myvis,
           imagename='single_channel_test/{}.chan_1500.dirty'.format(myvis),
           field='M31*',
           pblimit=0.05,
           imsize=5250 if 'Btracks' in myvis else 2048,
           cell="1.0arcsec" if 'Btracks' in myvis else '3.0arcsec',
           gridder='mosaic',
           specmode='cube',
           start=1500,
           width=1,
           nchan=1,
           niter=0,
           restoration=False,
           restfreq='1.42040575177GHz',
           phasecenter='J2000 00:44:33.854 +41d57m42.572',  # M31LARGE_17
           )

# And then try imaging the tracks together


tclean(vis=[myviss[0], myviss[2]],
       imagename='single_channel_test/15A-175_B_C_HI.chan_1500.dirty',
       field='M31*',
       pblimit=0.05,
       imsize=5250,
       phasecenter='J2000 00:44:33.854 +41d57m42.572',  # M31LARGE_17
       cell="1.0arcsec",
       gridder='mosaic',
       specmode='cube',
       start=1500,
       width=1,
       nchan=1,
       niter=0,
       restoration=False,
       restfreq='1.42040575177GHz',
       )


tclean(vis=[myviss[1], myviss[3]],
       imagename='single_channel_test/15A-175_B_C_HI.contsub.chan_1500.dirty',
       field='M31*',
       pblimit=0.05,
       imsize=5250,
       phasecenter='J2000 00:44:33.854 +41d57m42.572',  # M31LARGE_17
       cell="1.0arcsec",
       gridder='mosaic',
       specmode='cube',
       start=1500,
       width=1,
       nchan=1,
       niter=0,
       restoration=False,
       restfreq='1.42040575177GHz',
       )
