from neuromllite import *
from neuromllite.NetworkGenerator import *
from neuromllite.utils import create_new_model
import sys

sys.path.append("..")

colors = {'RS':'0 0 0.8', 'FS':'0.8 0 0', 'LTS':'0 0 0.8', 'IB':'0.8 0 0', 'IBR':'0.8 0 0'}

def generate(cell, duration, config='IClamp'):
    
    reference = "%s_%s"%(config, cell)

    cell_id = '%s'%cell
    cell_nmll = Cell(id=cell_id, neuroml2_source_file='../%s/%s.cell.nml'%(cell,cell))
 
    ################################################################################
    ###   Add some inputs
    
    if 'IClamp' in config:
        parameters = {}
        parameters['stim_amp'] = '350pA'
        parameters['stim_delay'] = '100ms'
        parameters['stim_dur'] = '500ms'
        input_source = InputSource(id='iclamp_0', 
                                   neuroml2_input='pulseGenerator', 
                                   parameters={'amplitude':'stim_amp', 'delay':'stim_delay', 'duration':'stim_dur'})
      
        
    else:

        parameters = {}
        parameters['average_rate'] = '100 Hz'
        parameters['number_per_cell'] = '10'
        input_source = InputSource(id='pfs0', 
                                   neuroml2_input='PoissonFiringSynapse', 
                                   parameters={'average_rate':'average_rate', 
                                               'synapse':syn_exc.id, 
                                               'spike_target':"./%s"%syn_exc.id})
                                               
    sim, net = create_new_model(reference,
                     duration, 
                     dt=0.01, # ms 
                     temperature=34, # degC
                     default_region='CA1',
                     parameters = parameters,
                     cell_for_default_population=cell_nmll,
                     color_for_default_population=colors[cell],
                     input_for_default_population=input_source)
                     
    sim.record_variables={'biophys/membraneProperties/Na_all/Na/m/q':{'all':'*'},
                         'biophys/membraneProperties/Na_all/Na/h/q':{'all':'*'},
                         'biophys/membraneProperties/Kd_all/Kd/n/q':{'all':'*'}}
    
    if cell != 'FS':
        sim.record_variables['biophys/membraneProperties/IM_all/IM/p/q']={'all':'*'}
        
    if cell == 'IB' or cell == 'IBR':
        sim.record_variables['biophys/membraneProperties/IL_all/IL/q/q']={'all':'*'}
        sim.record_variables['biophys/membraneProperties/IL_all/IL/r/q']={'all':'*'}
        
    if cell == 'LTS':
        sim.record_variables['biophys/membraneProperties/IT_all/IT/s/q']={'all':'*'}
        sim.record_variables['biophys/membraneProperties/IT_all/IT/u/q']={'all':'*'}
        
    sim.to_json_file()

    return sim, net



if __name__ == "__main__":
    
    if '-all' in sys.argv:
        for cell in colors:
            generate(cell, 700, config="IClamp")
            
        
    else:
        #generate('IFcurve_PV')
        #generate('olm')
        sim, net = generate('RS', 700, config="IClamp")
        #generate('olm', 1000, config="PoissonFiringSynapse")
        #generate('bistratified')
        #generate('IClamp_Pyr')
        
        check_to_generate_or_run(sys.argv, sim)
    
