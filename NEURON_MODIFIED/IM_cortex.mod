TITLE Cortical M current
:
:   M-current, responsible for the adaptation of firing rate and the 
:   afterhyperpolarization (AHP) of cortical pyramidal cells
:
:   First-order model described by hodgkin-Hyxley like equations.
:   K+ current, activated by depolarization, noninactivating.
:
:   Model taken from Yamada, W.M., Koch, C. and Adams, P.R.  Multiple 
:   channels and calcium dynamics.  In: Methods in Neuronal Modeling, 
:   edited by C. Koch and I. Segev, MIT press, 1989, p 97-134.
:
:   See also: McCormick, D.A., Wang, Z. and Huguenard, J. Neurotransmitter 
:   control of neocortical neuronal activity and excitability. 
:   Cerebral Cortex 3: 387-398, 1993.
:
:   Written by Alain Destexhe, Laval University, 1995
:

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX im
	USEION k READ ek WRITE ik
    RANGE gkbar, pinf, tp, taumax

}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
}


PARAMETER {
	v		(mV)
	celsius = 36    (degC)
	ek		(mV)
	gkbar	= 1e-6	(mho/cm2)
	taumax	= 1000	(ms)		: peak value of tau
}



STATE {
	p m
}

ASSIGNED {
	ik	(mA/cm2)
	pinf
	tp	(ms)
}

BREAKPOINT {
	SOLVE states METHOD cnexp
	ik = gkbar * p * (v - ek)
    m = p
}

DERIVATIVE states {

	evaluate_fct(v)

	p'=(pinf-p)/tp
}

UNITSOFF
PROCEDURE evaluate_fct(v(mV)) {

    pinf=1/(1+exp(-(v+35)/10))
    tp=taumax/(3.3*exp((v+35)/20)+exp(-(v+35)/20))

}
UNITSON

