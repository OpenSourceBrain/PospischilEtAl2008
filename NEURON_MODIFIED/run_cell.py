import neuron
import sys

h = neuron.h

def parse_arguments():
    """Parse command line arguments"""
    import argparse

    parser = argparse.ArgumentParser(description='Run one cell from Pospischil et al 2008')

    parser.add_argument('cell', metavar='cell', type=str,
                        help='Which cell to run (RS, FS, etc.)')


    parser.add_argument('-nogui', action='store_true',
                        help='Show no plots, just save results', 
                        default=False)
                        
    parser.add_argument('-showca', action='store_true',
                        help='Show plot of ca', 
                        default=False)
                        
    parser.add_argument('-diameter',
                        type=float,
                        metavar='<diameter>',
                        default=None,
                        help='Diameter and Length of body segment')
                        
    parser.add_argument('-duration', 
                        type=float,
                        metavar='<duration>',
                        default=1000,
                        help='Duration of simulations, in ms') 
                        
    parser.add_argument('-dt', 
                        type=float,
                        metavar='<time step>',
                        default=0.1,
                        help='Timestep for simulations, dt, in ms')
                        
    parser.add_argument('-idelay', 
                        type=float,
                        metavar='<current clamp delay>',
                        default=300,
                        help='Current clamp delay, in ms') 
                        
    parser.add_argument('-iduration', 
                        type=float,
                        metavar='<current clamp duration>',
                        default=400,
                        help='Current clamp duration, in ms') 
                        
    parser.add_argument('-iamp', 
                        type=float,
                        metavar='<current clamp amplitude>',
                        default=0.75,
                        help='Current clamp amplitude, in nA') 
   
    parser.add_argument('-iampbackground',
                       type=float,
                       metavar='<current clamp background amplitude>',
                       default=0,
                       help='Current clamp background amplitude, in nA')
       
       
    parser.add_argument('-gcabar_it', 
                        type=float,
                        metavar='<gcabar_it>',
                        default=None,
                        help='Conductance density of it')
                        
    parser.add_argument('-shift_it',
                        type=float,
                        metavar='<shift_it>',
                        default=None,
                        help='Vx parameter of it')
                        
    parser.add_argument('-gcabar_ical', 
                        type=float,
                        metavar='<gcabar_ical>',
                        default=None,
                        help='Conductance density of ical') 
                        
    parser.add_argument('-gkbar_im', 
                        type=float,
                        metavar='<gkbar_im>',
                        default=None,
                        help='Conductance density of im') 
 
    parser.add_argument('-taumax_im',
                     type=float,
                     metavar='<taumax_im>',
                     default=None,
                     help='TauMAX of im')

    parser.add_argument('-e_pas', 
                        type=float,
                        metavar='<e_pas>',
                        default=None,
                        help='Erev of passive cond') 
                        
    parser.add_argument('-g_pas', 
                        type=float,
                        metavar='<g_pas>',
                        default=None,
                        help='Conductance density of passive cond') 
                        
    parser.add_argument('-gnabar_hh2', 
                        type=float,
                        metavar='<gnabar_hh2>',
                        default=None,
                        help='Conductance density of na in hh2') 
                        
    parser.add_argument('-gkbar_hh2', 
                        type=float,
                        metavar='<gkbar_hh2>',
                        default=None,
                        help='Conductance density of k in hh2') 
                        
    parser.add_argument('-vtraub_hh2', 
                        type=float,
                        metavar='<vtraub_hh2>',
                        default=None,
                        help='Voltage shift from Traub model in hh2') 
                        
    parser.add_argument('-v_init', 
                        type=float,
                        metavar='<v_init>',
                        default=None,
                        help='Initial membrane potential') 
                        
    return parser.parse_args()
                        

def run_cell(cell, 
             nogui = False, 
             showca = False,
             diameter = None,
             duration = 1000, 
             dt = 0.01, 
             idelay = 300, 
             iduration = 400, 
             iamp = 0.75,
             iampbackground = 0,
             gcabar_ical=None,
             gcabar_it=None,
             shift_it=None,
             gkbar_im=None,
             taumax_im=None,
             e_pas=None,
             g_pas=None,
             gnabar_hh2=None,
             gkbar_hh2=None,
             vtraub_hh2=None,
             v_init=None,
             label=None):
    

    h.load_file("stdlib.hoc")
    h.load_file("stdrun.hoc")
    #h.load_file("electrod.hoc")	# electrode template

    if not nogui:
        h.load_file("stdgui.hoc")

    h("objref p")
    h("p = new PythonObject()")
    
    h.celsius = 36
    
    
    h.dt = dt
    h.tstop = duration
    h.steps_per_ms = int(1/dt) 
    
    h("objectvar myCell")
    
    if cell == 'RS':
        h.load_file("../NEURON_ORIG/sPY_template")
        h("myCell = new sPY()")
    elif cell == 'FS':
        h.load_file("../NEURON_ORIG/sIN_template")
        h("myCell = new sIN()")
    elif cell == 'IB':
        h.load_file("../NEURON_ORIG/sPYb_template")
        h("myCell = new sPYb()")
    elif cell == 'IBR':
        h.load_file("../NEURON_ORIG/sPYbr_template")
        h("myCell = new sPYbr()")
    elif cell == 'LTS':
        h.load_file("../NEURON_ORIG/sPYr_template")
        h("myCell = new sPYr()")
    else:
        print('Unknown cell type: %s'%cell)
        exit()
    
    
    if diameter is not None:
        h('myCell.soma[0] { diam = %s } '%diameter)
        h('myCell.soma[0] { L = %s } '%diameter)
    if gcabar_ical is not None:
        h('myCell.soma[0] { if (ismembrane("ical")) { gcabar_ical = %s } } '%gcabar_ical)
    if gcabar_it is not None:
        h('myCell.soma[0] { if (ismembrane("it")) { gcabar_it = %s } } '%gcabar_it)
    if shift_it is not None:
        h('myCell.soma[0] { if (ismembrane("it")) { shift_it = %s } } '%shift_it)
    if gkbar_im is not None:
        h('myCell.soma[0] { if (ismembrane("im")) { gkbar_im = %s } } '%gkbar_im)
    if taumax_im is not None:
        h('myCell.soma[0] { if (ismembrane("im")) { taumax_im = %s } } '%taumax_im)
    if e_pas is not None:
        h('myCell.soma[0] { e_pas = %s } '%e_pas)
    if g_pas is not None:
        h('myCell.soma[0] { g_pas = %s } '%g_pas)
    if gnabar_hh2 is not None:
        h('myCell.soma[0] { if (ismembrane("hh2")) { gnabar_hh2 = %s } } '%gnabar_hh2)
    if gkbar_hh2 is not None:
        h('myCell.soma[0] { if (ismembrane("hh2")) { gkbar_hh2 = %s } } '%gkbar_hh2)
    if vtraub_hh2 is not None:
        h('myCell.soma[0] { if (ismembrane("hh2")) { vtraub_hh2 = %s } } '%vtraub_hh2)
    if v_init is not None:
        h('v_init = %s '%v_init)
        
    h("objectvar InputBG")
    h("myCell.soma[0] { InputBG = new IClamp(0.5) } ")
    h("{ InputBG.del = 0 } ")
    h("{ InputBG.dur = %s } "%duration)
    h("{ InputBG.amp = %s } "%iampbackground)

    h("objectvar Input")
    h("myCell.soma[0] { Input = new IClamp(0.5) } ")
    h("{ Input.del = %s } "%idelay)
    h("{ Input.dur = %s } "%iduration)
    h("{ Input.amp = %s } "%iamp)
    
    
    h("forall psection()")
    
    # File to save: time
    h(' objectvar v_time ')
    h(' { v_time = new Vector() } ')
    h(' v_time.record(&t) ')
    h.v_time.resize((h.tstop * h.steps_per_ms) + 1)
    
    h(' objectvar v_vect ')
    h(' { v_vect = new Vector() } ')
    h(' v_vect.record(&myCell.soma[0].v(0.5)) ')
    h.v_vect.resize((h.tstop * h.steps_per_ms) + 1)
    
    h('myCell.soma[0] { if (ismembrane("ical")) { is_ical = 1 } } ')
    is_ical = h.is_ical == 1.0
    
    if showca:
        h(' objectvar cai_vect ')
        h(' { cai_vect = new Vector() } ')
        h(' cai_vect.record(&myCell.soma[0].cai(0.5)) ')
        h.cai_vect.resize((h.tstop * h.steps_per_ms) + 1)
        
        h(' objectvar eca_vect ')
        h(' { eca_vect = new Vector() } ')
        h(' eca_vect.record(&myCell.soma[0].eca(0.5)) ')
        h.eca_vect.resize((h.tstop * h.steps_per_ms) + 1)
        
        h(' objectvar ica_vect ')
        h(' { ica_vect = new Vector() } ')
        h(' ica_vect.record(&myCell.soma[0].ica(0.5)) ')
        h.ica_vect.resize((h.tstop * h.steps_per_ms) + 1)

        if is_ical:
            h(' objectvar carev_vect ')
            h(' { carev_vect = new Vector() } ')
            h(' carev_vect.record(&myCell.soma[0].carev_ical(0.5)) ')
            h.carev_vect.resize((h.tstop * h.steps_per_ms) + 1)
    
    print("Running a simulation of %sms (dt = %sms)" % (h.tstop, h.dt))

    h.run()

    print("Finished simulation, saving results...")
    
    if label == None:
        label = cell
        
    
    v_file_name = '%s.v.dat'%label.replace(' ', '_')
    save_vector(v_file_name, h.v_vect, h.v_time, 1000.0)
    
    if showca:
        cai_file_name = '%s.cai.dat'%label.replace(' ', '_')
        save_vector(cai_file_name, h.cai_vect, h.v_time, 1)

        eca_file_name = '%s.eca.dat'%label.replace(' ', '_')
        save_vector(eca_file_name, h.eca_vect, h.v_time, 1000.0)

        ica_file_name = '%s.ica.dat'%label.replace(' ', '_')
        save_vector(ica_file_name, h.ica_vect, h.v_time, 1000.0)
        
        if is_ical:
            carev_file_name = '%s.carev.dat'%label.replace(' ', '_')
            save_vector(carev_file_name, h.carev_vect, h.v_time, 1000.0)
    
    
    if not nogui:
        
        print('Plotting saved results')
        import matplotlib.pyplot as pylab
        
        fig = pylab.figure()
        fig.canvas.set_window_title("Membrane potential of %s (%s)"%(cell, label))
        
        pylab.xlabel('Time (ms)')
        pylab.ylabel('Membrane potential (mV)')
        pylab.grid('on')
        
        pylab.plot(h.v_time, h.v_vect, label=label)
        pylab.legend()
        
        if showca:
            fig = pylab.figure()
            fig.canvas.set_window_title("[Ca2+] of %s (%s)"%(cell, label))

            pylab.xlabel('Time (ms)')
            pylab.ylabel('[Ca2+]')
            pylab.grid('on')

            pylab.plot(h.v_time, h.cai_vect, label='[Ca2+] %s'%label)
            pylab.legend()
            
            fig = pylab.figure()
            fig.canvas.set_window_title("Rev pot of Ca of %s (%s)"%(cell, label))

            pylab.xlabel('Time (ms)')
            pylab.ylabel('Reversal potential Ca (mV)')
            pylab.grid('on')

            pylab.plot(h.v_time, h.eca_vect, label='eca %s'%label)
            pylab.legend()
            
            fig = pylab.figure()
            fig.canvas.set_window_title("Ca curent density of %s (%s)"%(cell, label))

            pylab.xlabel('Time (ms)')
            pylab.ylabel('Ca curent density (mA/cm2)')
            pylab.grid('on')

            pylab.plot(h.v_time, h.ica_vect, label='ica %s'%label)
            pylab.legend()
            
            if is_ical:
                fig = pylab.figure()
                fig.canvas.set_window_title("carev of ical in %s (%s)"%(cell, label))

                pylab.xlabel('Time (ms)')
                pylab.ylabel('carev')
                pylab.grid('on')

                pylab.plot(h.v_time, h.carev_vect, label='carev %s'%label)
                pylab.legend()
        
        pylab.show()
        
def save_vector(file_name, vector, time_v, factor):
    vfile = open(file_name, 'w')
    for i in range(int(h.tstop * h.steps_per_ms) + 1):
        vfile.write('%f\t%e\t\n'% ( (float(time_v.get(i))/1000.0), (float(vector.get(i)) / factor))) # Time in first column, save in SI units...; Saving as SI, variable has dim: voltage
    vfile.close()
    print("Saved data to: %s"%file_name)
    
def main(args=None):
    """Main"""
    if args is None:
        args = parse_arguments()
        

    run_cell(args.cell, 
             args.nogui,
             args.showca,
             args.diameter,
             args.duration, 
             args.dt, 
             args.idelay, 
             args.iduration, 
             args.iamp,
             args.iampbackground,
             args.gcabar_it,
             args.shift_it,
             args.gcabar_ical, 
             args.gkbar_im,
             args.taumax_im,
             args.e_pas, 
             args.g_pas, 
             args.gnabar_hh2, 
             args.gkbar_hh2, 
             args.vtraub_hh2, 
             args.v_init)
    
    
if __name__ == "__main__":
    main()