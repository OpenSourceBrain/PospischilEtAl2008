

print_the_diffs()
{
    echo
    echo
    echo "####################   $1    ####################"
    echo
    diff -w $1 ../NEURON_ORIG/$1 

}

print_the_diffs 'cadecay_destexhe.mod'
print_the_diffs 'IT_huguenard.mod'
print_the_diffs 'IL_gutnick.mod'
print_the_diffs 'IM_cortex.mod'
print_the_diffs 'HH_traub.mod'

print_the_diffs 'demo_IN_FS.hoc'
print_the_diffs 'demo_PY_IB.hoc'
print_the_diffs 'demo_PY_IBR.hoc'
print_the_diffs 'demo_PY_LTS.hoc'
print_the_diffs 'demo_PY_RS.hoc'



