# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 19:04:21 2019

@author: SUN
"""


#####################################################################
# Black Scholes pour Devise (Garman Khlhagen) et les lettres grecques
#####################################################################

import math

from math import pi #Importation de la constante pi du module math
from math import e #Importation de la constante e du module math

from math import sqrt #Importation de la fonction sqrt du module math
from math import log #Importation de la fonction log du module math
from math import exp #Importation de la fonction exp du module math

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import scipy # SciPy Package
import scipy.stats as stats

# Paire de devise considérée : EURUSD

#------------------------------------
# Prix Forward EURUSD vs. EURUSD Spot
#------------------------------------

def Fwd(S, r, q, T):
    Fw = S * exp((r - q) * T)
    return Fw

# Fw: Prix forward EURUSD

# S: Prix Spot EURUSD

# T: Echéance

# Fonction d1

S = 1.135 # Spot EURUSD
r = 2.60/100 # Taux sans risque $
q = -0.31/100 # Taux sans risque €
T = 0.25 # 3 mois

Fw = Fwd(S, r, q, T)

#print("EURUSD Forward 3 mois:" "%.5f" % Fw)

#--------------------------------------
# Formules Black Scholes Prime Call Put
#--------------------------------------

# Calcul de d1 et d2
#-------------------

def d_un(S,K,sigma,T,r,q):#S: (EUR/DOL: getFX) (DOL/MAD - MAD/EUR: TBA), K variable, sigma(T), T variable, r LIBOR(MAD == getMad)(T),q EURIBOR(T)
    d1=(1/(sigma*sqrt(T)))*(log(S/K)+(r-q+(sigma**2)/2)*T)
    return(d1)

def d_deux(S,K,sigma,T,r,q):
    d2 =d_un(S,K,sigma,T,r,q) - (sigma*sqrt(T))
    return(d2)

# Option Call
#------------

def bs_call(S,K,sigma,T,r,q):
    d1=d_un(S,K,sigma,T,r,q)
    d2=d_deux(S,K,sigma,T,r,q)
    N_d1=stats.norm.cdf(d1, 0, 1)
    N_d2=stats.norm.cdf(d2, 0, 1)
    op_call=(S*exp(-q*T)*N_d1)-(K*exp(-r*T)*N_d2)
    return(op_call)

S = 1.135 # Spot EURUSD
r = 2.60/100 # Taux sans risque $
q = -0.31/100 # Taux sans risque €
T = 0.25 # 3 mois

K = 1.1432
sigma = 6.16/100

prime_call = bs_call(S,K,sigma,T,r,q)

#print("prime_call:" "%.5f" % prime_call)

# Option put
#-----------

def bs_put(S,K,sigma,T,r,q):
    d1=d_un(S,K,sigma,T,r,q)
    d2=d_deux(S,K,sigma,T,r,q)
    N_nd1=stats.norm.cdf(-d1, 0, 1)
    N_nd2=stats.norm.cdf(-d2, 0, 1)
    op_put=(-S*exp(-q*T)*N_nd1)+(K*exp(-r*T)*N_nd2)
    return(op_put)

S = 1.135 # Spot EURUSD
r = 2.60/100 # Taux sans risque $
q = -0.31/100 # Taux sans risque €
T = 0.25 # 3 mois

K = 1.1432
sigma = 6.16/100

prime_put = bs_put(S,K,sigma,T,r,q)

#print("prime_put:" "%.5f" % prime_put)

#----------------------------------------
# Formules Black Scholes Lettres Grecques
#----------------------------------------

# Delta Call
#-----------

def delta_call(S,K,sigma,T,r,q):
    d1=d_un(S,K,sigma,T,r,q)
    N_d1=stats.norm.cdf(d1, 0, 1)
    v_delta=exp(-q*T)*N_d1
    return(v_delta)

S = 1.135 # Spot EURUSD
r = 2.60/100 # Taux sans risque $
q = -0.31/100 # Taux sans risque €
T = 0.25 # 3 mois

K = 1.1432
sigma = 6.16/100

delta_call_v = delta_call(S,K,sigma,T,r,q)

#print("delta_call:" "%.5f" % delta_call_v)

# Delta put
#----------

def delta_put(S,K,sigma,T,r,q):
    d1=d_un(S,K,sigma,T,r,q)
    N_d1=stats.norm.cdf(d1, 0, 1)
    v_delta=exp(-q*T)*(N_d1 - 1)
    return(v_delta)

S = 1.135 # Spot EURUSD
r = 2.60/100 # Taux sans risque $
q = -0.31/100 # Taux sans risque €
T = 0.25 # 3 mois

K = 1.1432
sigma = 6.16/100

delta_put_v = delta_put(S,K,sigma,T,r,q)

#print("delta_put:" "%.5f" % delta_put_v)


# Lettre Gamma
#-------------

def bs_gamma(S,K,sigma,T,r,q):
    d1=d_un(S,K,sigma,T,r,q)
    Np_d1=stats.norm.pdf(d1, 0, 1)
    v_gamma=(Np_d1*exp(-q*T))/(S*sigma*sqrt(T))
    return(v_gamma)

S = 1.135 # Spot EURUSD
r = 2.60/100 # Taux sans risque $
q = -0.31/100 # Taux sans risque €
T = 0.25 # 3 mois

K = 1.1432
sigma = 6.16/100

v_gamma = bs_gamma(S,K,sigma,T,r,q)

#print("gamma:" "%.5f" % v_gamma)

###############################################################
# Fin de codes validés
###############################################################