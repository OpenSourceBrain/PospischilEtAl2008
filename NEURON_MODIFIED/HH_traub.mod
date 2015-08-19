TITLE Hippocampal HH channels
:
: Fast Na+ and K+ currents responsible for action potentials
: Iterative equations
:
: Equations modified by Traub, for Hippocampal Pyramidal cells, in:
: Traub & Miles, Neuronal Networks of the Hippocampus, Cambridge, 1991
:
: range variable vtraub adjust threshold
:
: Written by Alain Destexhe, Salk Institute, Aug 1992
:
: Modified Oct 96 for compatibility with Windows: trap low values of arguments
:

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX hh2
	USEION na READ ena WRITE ina
	USEION k READ ek WRITE ik
	RANGE gnabar, gkbar, vtraub
	RANGE alpha_m, alpha_h, alpha_n
    RANGE beta_m, beta_h, beta_n
}


UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
}

PARAMETER {
	gnabar  = .003  (mho/cm2)
	gkbar   = .005  (mho/cm2)

	ena     = 50    (mV)
	ek      = -90   (mV)
	celsius = 36    (degC)
	dt              (ms)
	v               (mV)
	vtraub  = -63   (mV)   : PG changed this from -63 to -55, as this is value for vtraub is used in all ModelDB examples
}

STATE {
	m h n
}

ASSIGNED {
	ina     (mA/cm2)
	ik      (mA/cm2)
    alpha_m
    alpha_h
    alpha_n
    beta_m
    beta_h
    beta_n
}


BREAKPOINT {

    SOLVE states

	ina = gnabar * m*m*m*h * (v - ena)
	ik  = gkbar * n*n*n*n * (v - ek)
}


DERIVATIVE states {   : exact Hodgkin-Huxley equations

       evaluate_fct(v)

       m' = alpha_m*(1-m)-beta_m*m
       h' = alpha_h*(1-h)-beta_h*h
       n' = alpha_n*(1-n)-beta_n*n

}

UNITSOFF
PROCEDURE evaluate_fct(v(mV)) { LOCAL vt

    vt = vtraub

    alpha_m = (-0.32*(v-vt-13))/(exp(-(v-vt-13)/4)-1)
    beta_m = (0.28*(v-vt-40))/(exp((v-vt-40)/5)-1)

    alpha_h = 0.128*exp(-(v-vt-17)/18)
    beta_h = 4/(1+exp(-(v-vt-40)/5))

    alpha_n = (-0.032*(v-vt-15))/(exp(-(v-vt-15)/5)-1)
    beta_n = 0.5*exp(-(v-vt-10)/40)

}
