
# Now make a bunch of scan plots to make it easier to identify bad data

import os
import numpy as np

# Make sure ms_active is defined
assert isinstance(ms_active, str)

# Plot the bandpasses per SPW as well
bp_folder = "finalBPcal_plots"
if not os.path.exists(bp_folder):
    os.mkdir(bp_folder)

tb.open(ms_active + "/SPECTRAL_WINDOW")
nspws = tb.getcol("NAME").shape[0]
tb.close()

# Final BP cal table
finalbpcal_name = "final_caltables/finalBPcal.b"

for ii in range(nspws):
    filename = 'finalBPcal_amp_spw_' + str(ii) + '.png'
    syscommand = 'rm -rf ' + filename
    os.system(syscommand)

    default('plotcal')
    caltable = finalbpcal_name
    xaxis = 'freq'
    yaxis = 'amp'
    poln = ''
    field = ''
    antenna = ''
    spw = str(ii)
    timerange = ''
    subplot = 111
    overplot = False
    clearpanel = 'Auto'
    iteration = ''
    showflags = False
    plotsymbol = 'o'
    plotcolor = 'blue'
    markersize = 5.0
    fontsize = 10.0
    showgui = False
    figfile = os.path.join(bp_folder, filename)
    async = False
    plotcal()

for ii in range(nspws):
    filename = 'finalBPcal_phase_spw_' + str(ii) + '.png'
    syscommand = 'rm -rf ' + filename
    os.system(syscommand)

    antPlot = str(ii * 3) + '~' + str(ii * 3 + 2)

    default('plotcal')
    caltable = finalbpcal_name
    xaxis = 'freq'
    yaxis = 'phase'
    poln = ''
    field = ''
    antenna = ''
    spw = str(ii)
    timerange = ''
    subplot = 111
    overplot = False
    clearpanel = 'Auto'
    iteration = ''
    # plotrange=[0,0,-phaseplotmax,phaseplotmax]
    showflags = False
    plotsymbol = 'o'
    plotcolor = 'blue'
    markersize = 5.0
    fontsize = 10.0
    showgui = False
    figfile = os.path.join(bp_folder, filename)
    async = False
    plotcal()

# SPWs to loop through
tb.open(os.path.join(ms_active, "SPECTRAL_WINDOW"))
spws = range(len(tb.getcol("NAME")))
nchans = tb.getcol('NUM_CHAN')
tb.close()

# Read the field names
tb.open(os.path.join(ms_active, "FIELD"))
names = tb.getcol('NAME')
numFields = tb.nrows()
tb.close()

# Intent names
tb.open(os.path.join(ms_active, 'STATE'))
intentcol = tb.getcol('OBS_MODE')
tb.close()

tb.open(ms_active)
scanNums = np.unique(tb.getcol('SCAN_NUMBER'))
field_scans = []
is_calibrator = np.empty_like(scanNums, dtype='bool')
is_all_flagged = np.empty((len(spws), len(scanNums)), dtype='bool')
for ii in range(numFields):
    subtable = tb.query('FIELD_ID==%s' % ii)
    field_scan = np.unique(subtable.getcol('SCAN_NUMBER'))
    field_scans.append(field_scan)

    # Is the intent for calibration?
    scan_intents = intentcol[np.unique(subtable.getcol("STATE_ID"))]
    is_calib = False
    for intent in scan_intents:
        if "CALIBRATE" in intent:
            is_calib = True
            break

    is_calibrator[field_scan - 1] = is_calib

    # Are any of the scans completely flagged?
    for spw in spws:
        for scan in field_scan:
            scantable = \
                tb.query("SCAN_NUMBER=={0} AND DATA_DESC_ID=={1}".format(scan,
                                                                         spw))
            if scantable.getcol("FLAG").all():
                is_all_flagged[spw, scan - 1] = True
            else:
                is_all_flagged[spw, scan - 1] = False

tb.close()

# Make folder for scan plots
scan_dir = "scan_plots"

if not os.path.exists(scan_dir):
    os.mkdir(scan_dir)

for spw_num in spws:
    print("On SPW {}".format(spw))

    avg_chan = "1"

    spw_folder = os.path.join(scan_dir, "spw_{}".format(spw_num))
    if not os.path.exists(spw_folder):
        os.mkdir(spw_folder)
    else:
        # Make sure any old plots are removed first.
        os.system("rm {}/*.png".format(spw_folder))

    for ii in range(len(field_scans)):
        print("On field {}".format(names[ii]))
        for jj in field_scans[ii]:

            # Check if all of the data is flagged.
            if is_all_flagged[spw_num, jj - 1]:
                print("All data flagged in SPW {0} scan {1}"
                      .format(spw_num, jj))
                continue

            print("On scan {}".format(jj))

            # Amp vs. time
            default('plotms')
            vis = ms_active
            xaxis = 'time'
            yaxis = 'amp'
            ydatacolumn = 'corrected'
            selectdata = True
            field = names[ii]
            scan = str(jj)
            spw = str(spw_num)
            avgchannel = str(avg_chan)
            correlation = "RR,LL"
            averagedata = True
            avgbaseline = True
            transform = False
            extendflag = False
            plotrange = []
            title = 'Amp vs Time: Field {0} Scan {1}'.format(names[ii], jj)
            xlabel = ''
            ylabel = ''
            showmajorgrid = False
            showminorgrid = False
            plotfile = os.path.join(
                spw_folder, 'field_{0}_amp_scan_{1}.png'.format(names[ii], jj))
            overwrite = True
            showgui = False
            async = False
            plotms()

            # Amp vs. channel
            default('plotms')
            vis = ms_active
            xaxis = 'chan'
            yaxis = 'amp'
            ydatacolumn = 'corrected'
            selectdata = True
            field = names[ii]
            scan = str(jj)
            spw = str(spw_num)
            avgchannel = str(avg_chan)
            avgtime = "1e8"
            correlation = "RR,LL"
            averagedata = True
            avgbaseline = True
            transform = False
            extendflag = False
            plotrange = []
            title = 'Amp vs Chan: Field {0} Scan {1}'.format(names[ii], jj)
            xlabel = ''
            ylabel = ''
            showmajorgrid = False
            showminorgrid = False
            plotfile = os.path.join(
                spw_folder, 'field_{0}_amp_chan_scan_{1}.png'.format(names[ii], jj))
            overwrite = True
            showgui = False
            async = False
            plotms()

            # Plot amp vs uvdist
            default('plotms')
            vis = ms_active
            xaxis = 'uvdist'
            yaxis = 'amp'
            ydatacolumn = 'corrected'
            selectdata = True
            field = names[ii]
            scan = str(jj)
            spw = str(spw_num)
            avgchannel = str(4096)
            avgtime = '1e8'
            correlation = "RR,LL"
            averagedata = True
            avgbaseline = False
            transform = False
            extendflag = False
            plotrange = []
            title = 'Amp vs UVDist: Field {0} Scan {1}'.format(names[ii], jj)
            xlabel = ''
            ylabel = ''
            showmajorgrid = False
            showminorgrid = False
            plotfile = os.path.join(
                spw_folder, 'field_{0}_amp_uvdist_scan_{1}.png'.format(names[ii], jj))
            overwrite = True
            showgui = False
            async = False
            plotms()

            # Skip the phase plots for the HI SPW (0)
            if is_calibrator[jj - 1] and spw_num != 0:
                # Plot phase vs time
                default('plotms')
                vis = ms_active
                xaxis = 'time'
                yaxis = 'phase'
                ydatacolumn = 'corrected'
                selectdata = True
                field = names[ii]
                scan = str(jj)
                spw = str(spw_num)
                correlation = "RR,LL"
                averagedata = True
                avgbaseline = False
                transform = False
                extendflag = False
                plotrange = []
                title = 'Phase vs Time: Field {0} Scan {1}'.format(
                    names[ii], jj)
                xlabel = ''
                ylabel = ''
                showmajorgrid = False
                showminorgrid = False
                plotfile = os.path.join(
                    spw_folder, 'field_{0}_phase_scan_{1}.png'.format(names[ii], jj))
                overwrite = True
                showgui = False
                async = False
                plotms()

                # Plot phase vs channel
                default('plotms')
                vis = ms_active
                xaxis = 'chan'
                yaxis = 'phase'
                ydatacolumn = 'corrected'
                selectdata = True
                field = names[ii]
                scan = str(jj)
                spw = str(spw_num)
                correlation = "RR,LL"
                averagedata = True
                avgbaseline = False
                transform = False
                extendflag = False
                plotrange = []
                title = 'Phase vs Chan: Field {0} Scan {1}'.format(
                    names[ii], jj)
                xlabel = ''
                ylabel = ''
                showmajorgrid = False
                showminorgrid = False
                plotfile = os.path.join(
                    spw_folder, 'field_{0}_phase_chan_scan_{1}.png'.format(names[ii], jj))
                overwrite = True
                showgui = False
                async = False
                plotms()

                # Plot phase vs uvdist
                default('plotms')
                vis = ms_active
                xaxis = 'uvdist'
                yaxis = 'phase'
                ydatacolumn = 'corrected'
                selectdata = True
                field = names[ii]
                scan = str(jj)
                spw = str(spw_num)
                correlation = "RR,LL"
                avgchannel = "4096"
                avgtime = '1e8'
                averagedata = True
                avgbaseline = False
                transform = False
                extendflag = False
                plotrange = []
                title = 'Phase vs UVDist: Field {0} Scan {1}'.format(
                    names[ii], jj)
                xlabel = ''
                ylabel = ''
                showmajorgrid = False
                showminorgrid = False
                plotfile = os.path.join(
                    spw_folder, 'field_{0}_phase_uvdist_scan_{1}.png'.format(names[ii], jj))
                overwrite = True
                showgui = False
                async = False
                plotms()
