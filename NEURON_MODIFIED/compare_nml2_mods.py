# This script will compare plots of steady state/time course (inf/tau) for activation variables (m, h, etc)
# for the channels in mod files vs NeuroML2 files. 

# See ../NeuroML2/channels/analyse_chans.sh also and analyse.sh


import matplotlib.pyplot as pylab
import os.path


chans = [ ['IM', 'im', ['p'], ['m']],
          ['IT', 'it', ['s','u'], ['m','h']] ,
          ['IL', 'ical', ['q','r'], ['m','h']],
          ['Na', 'hh2', ['m', 'h'], ['m', 'h']], 
          ['Kd', 'hh2', ['n'], ['n']] ]



for chan in chans:
    
    channel_id = chan[0]
    vramp_lems_file  = '../NeuroML2/channels/%s.rampV.lems.dat'%(channel_id)

    ts = []
    volts = []
    for line in open(vramp_lems_file):
        ts.append(float(line.split()[0])*1000)
        volts.append(float(line.split()[1])*1000)
    
    fig = pylab.figure()
    fig.canvas.set_window_title("Time Course(s) of activation variables of %s"%(channel_id))

    pylab.xlabel('Membrane potential (mV)')
    pylab.ylabel('Time Course - tau (ms)')
    pylab.grid('on')

    for gate in chan[2]:
        
        tau_lems_file  = '../NeuroML2/channels/%s.%s.tau.lems.dat'%(channel_id, gate)
        
        if os.path.isfile(tau_lems_file):
            taus = []
            for line in open(tau_lems_file):
                ts.append(float(line.split()[0])*1000)
                taus.append(float(line.split()[1])*1000)

            pylab.plot(volts, taus, linestyle='-', linewidth=2, label="LEMS %s %s tau"%(channel_id, gate))

    for gate in chan[3]:
        
        tau_mod_file  = '%s.%s.tau.dat'%(chan[1], gate)
        
        if os.path.isfile(tau_mod_file):
            vs = []
            taus = []
            for line in open(tau_mod_file):
                vs.append(float(line.split()[0]))
                taus.append(float(line.split()[1]))

            pylab.plot(vs, taus, '--x', label="Mod %s %s tau"%(channel_id, gate))
            
            
    pylab.legend()
    pylab.savefig("TimeCourse_%s.png"%channel_id, bbox_inches="tight", dpi=300)
    
    
    fig = pylab.figure()
    fig.canvas.set_window_title("Steady state(s) of activation variables of %s"%(channel_id))

    pylab.xlabel('Membrane potential (mV)')
    pylab.ylabel('Steady state (inf)')
    pylab.grid('on')

    for gate in chan[2]:
        
        inf_lems_file  = '../NeuroML2/channels/%s.%s.inf.lems.dat'%(channel_id, gate)
        
        if os.path.isfile(inf_lems_file):
            infs = []
            for line in open(inf_lems_file):
                infs.append(float(line.split()[1]))

            pylab.plot(volts, infs, linestyle='-', linewidth=2, label="LEMS %s %s inf"%(channel_id, gate))
            
    for gate in chan[3]:
        
        inf_mod_file  = '%s.%s.inf.dat'%(chan[1], gate)
        
        if os.path.isfile(inf_mod_file):
        
            vs = []
            infs = []
            for line in open(inf_mod_file):
                vs.append(float(line.split()[0]))
                infs.append(float(line.split()[1]))

            pylab.plot(vs, infs, '--x', label="Mod %s %s inf"%(channel_id, gate))
            
    pylab.legend()
    pylab.savefig("SteadyState_%s.png"%channel_id, bbox_inches="tight", dpi=300)

    
pylab.show()
