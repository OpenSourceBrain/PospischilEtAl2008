import neuron
import sys

def parse_arguments():
    """Parse command line arguments"""
    import argparse

    parser = argparse.ArgumentParser(description='Run one cell from Pospischil et al 2008')

    parser.add_argument('cell', metavar='cell', type=str,
                        help='Which cell to run (RS, FS, etc.)')


    parser.add_argument('-nogui', action='store_true',
                        help='Show no plots, just save results', default="False")
                        
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
                        
    return parser.parse_args()
                        


def evaluate_arguments(args):

    h = neuron.h

    h.load_file("stdlib.hoc")
    h.load_file("stdrun.hoc")
    h.load_file("electrod.hoc")	# electrode template

    if not args.nogui:
        h.load_file("stdgui.hoc")

    h("objref p")
    h("p = new PythonObject()")
    
    h.celsius = 36
    
    
    h.dt = args.dt
    h.tstop = args.duration
    h.steps_per_ms = int(1/args.dt) 
    
    h("objectvar myCell")
    
    if args.cell == 'RS':
        h.load_file("../NEURON_ORIG/sPY_template")
        h("myCell = new sPY()")
    elif args.cell == 'FS':
        h.load_file("../NEURON_ORIG/sIN_template")
        h("myCell = new sIN()")
    elif args.cell == 'IB':
        h.load_file("../NEURON_ORIG/sPYb_template")
        h("myCell = new sPYb()")
    elif args.cell == 'IBR':
        h.load_file("../NEURON_ORIG/sPYbr_template")
        h("myCell = new sPYbr()")
    elif args.cell == 'LTS':
        h.load_file("../NEURON_ORIG/sPYr_template")
        h("myCell = new sPYr()")
    else:
        print('Unknown cell type: %s'%args.cell)
        exit()
    

    h("objectvar Input")
    h("myCell.soma[0] { Input = new Electrode(0.5) } ")
    h("{ Input.stim.del = %s } "%args.idelay)
    h("{ Input.stim.dur = %s } "%args.iduration)
    h("{ Input.stim.amp = %s } "%args.iamp)
    
    
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
    
    print("Running a simulation of %sms (dt = %sms)" % (h.tstop, h.dt))

    h.run()

    print("Finished simulation, saving results...")
    

    
    v_file_name = '%s.v.dat'%args.cell
    f_cell = open(v_file_name, 'w')
    for i in range(int(h.tstop * h.steps_per_ms) + 1):
        f_cell.write('%f\t'% (float(h.v_time.get(i))/1000.0)) # Time in first column, save in SI units...
        f_cell.write('%f\t'%(float(h.v_vect.get(i)) / 1000.0)) # Saving as SI, variable has dim: voltage
        f_cell.write("\n")
    f_cell.close()
    print("Saved data to: %s"%v_file_name)
    
    
def main(args=None):
    """Main"""

    if args is None:
        args = parse_arguments()

    evaluate_arguments(args)
    
    
if __name__ == "__main__":
    main()