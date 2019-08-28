Because each target was sporadically covered with different sensitivity, configurations, etc., each target has a custom clean script. The tclean calls are fairly similar for all.

Cleaning is done in 2 stages: (1) multi-scale clean with auto-masking and frequent major cycles (`cycleniter=500`) to 2-sigma, and (2) multi-scale clean with a pb-mask to 2-sigma. The second step is useful for low-level emission that was not captured in the clean mask. By triggering rapid major cycles, the second step minimally cleans negative bowls.

There is only a single NGC 6822 track from this project. Imaging of this source will be combined with the 14B-212 data elsewhere.