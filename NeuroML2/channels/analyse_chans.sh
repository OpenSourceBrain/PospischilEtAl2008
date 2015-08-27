# This script will generate plots of steady state/time course (inf/tau) for activation variables (m, h, etc)
# for the channels in NeuroML2 files. Requires pyNeuroML: https://github.com/NeuroML/pyNeuroML

# Run ../NEURON_MODIFIED/analyse.sh also and then ../NEURON_MODIFIED/compare_nml2_mods.py

pynml-channelanalysis Na/Na.channel.nml \
                      IT/IT.channel.nml \
                      IM/IM.channel.nml \
                      IL/IL.channel.nml \
                      Kd/Kd.channel.nml \
                      -caConc 4.3e-4 -temperature 36 -html -md
