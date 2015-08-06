# This script will generate plots of steady state/time course (inf/tau) for activation variables (m, h, etc)
# for the channels in mod files. Requires pyNeuroML: https://github.com/NeuroML/pyNeuroML

# Run ../NeuroML2/channels/analyse_chans.sh also and then compare_nml2_mods.py

pynml-modchananalysis im   -stepV 5 -temperature 36 -modFile IM_cortex.mod    -nogui
pynml-modchananalysis it   -stepV 5 -temperature 36 -modFile IT_huguenard.mod -nogui
pynml-modchananalysis ical -stepV 5 -temperature 36 -modFile IL_gutnick.mod   -nogui
pynml-modchananalysis hh2  -stepV 5 -temperature 36 -modFile HH_traub.mod     -nogui -dt 0.001  # due to fast m i.e. low tau




