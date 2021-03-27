import scipy.integrate
import numpy as np
# import matplotlib.pyplot as plt

# SIRmodel
def SIR_model1(y, t, pop, beta, gamma):
    S, I, R = y
    dS_dt = -beta * S * I/pop
    dI_dt = beta * S * I/pop - gamma * I
    dR_dt = gamma * I
    return ([dS_dt, dI_dt, dR_dt])

# SEIRmodel
def SEIR_model1(y, t, pop, beta, lambd, gamma):
    S, E, I, R = y
    dS_dt = -beta * S * I/pop
    dE_dt = beta * S * I / pop - lambd * E
    dI_dt = lambd * E - gamma * I
    dR_dt = gamma * I
    return ([dS_dt, dE_dt, dI_dt, dR_dt])

R_num=[]
# RMILmodel
def RMIL_model1(y, t, pop, beta, lambd, gamma, kappa, omega):
    S, E, I, R, D = y
    dS_dt = - beta * S * I /pop
    dE_dt = beta * S * I / pop - lambd * E
    #print(t)
    if(t<15):
        dI_dt = lambd * E - gamma * I - kappa * I
        dR_dt = gamma * I
        R_num.append(dR_dt)
        #print(R_num)
    else:
        dI_dt = lambd * E - gamma * I - kappa * I + omega * R_num[int(t)-14]
        dR_dt = gamma * I - omega * R_num[int(t)-14]
        R_num.append(dR_dt)
    dD_dt = kappa * I
    return ([dS_dt, dE_dt, dI_dt, dR_dt, dD_dt])

def SIR_model(pop,beta,gamma):
    t = np.linspace(0, 120, 120)
    res = scipy.integrate.odeint(SIR_model1, [pop, 500, 0],t, args=(pop,beta, gamma))
    res = np.array(res)
    list = [int(x) for x in res[:, 1]]
    # print(list)
    # accu = []
    # temp = 0
    # for i in list:
    #     temp = temp + i
    #     accu.append(temp)
    #print(accu)
    return [list]

def SEIR_model(pop,beta,lambd,gamma):
    t = np.linspace(0, 120, 120)
    res = scipy.integrate.odeint(SEIR_model1, [pop, 0, 500, 0],t, args=(pop,beta,lambd,gamma))
    res = np.array(res)
    list = [int(x) for x in res[:, 2]]
    # print(list)
    # accu = []
    # temp = 0
    # for i in list:
    #     temp = temp + i
    #     accu.append(temp)
    #print(accu)
    return [list]

def RMIL_model(pop,beta,lambd,gamma,kappa,omega):
    t = np.linspace(0, 120, 121)
    res = scipy.integrate.odeint(RMIL_model1, [pop, 0, 500, 0, 0], t, args=(pop,beta,lambd,gamma,kappa,omega))
    res = np.array(res)
    list = [int(x) for x in res[:, 2]]
    # print(list)
    # accu = []
    # temp = 0
    # for i in list:
    #     temp = temp + i
    #     accu.append(temp)
    #print(accu)
    return [list]