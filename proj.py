import random
import simpy
import numpy as np
"""
simpy: pip install simpy
msgpack: conda install -c anaconda msgpack-python
"""

tamanhoPopulacao = 100
taxaEntrada = 1.0 / 2.0        #Inverso do intervalo médio entre chegadas em minutos
taxaServico = 1.0 / 3.0    #Inverso do tempo de médio de atendimento em minutos

def entrada(env):
    for i in range(tamanhoPopulacao):
        yield env.timeout(random.expovariate(taxaEntrada))
        name = 'Cliente %d' % (i+1)
        env.process(saida(env, name))

def saida(env, name):
    print('%7.2f\t Chegada\t %s' % (env.now, name))
    atendReq = Servidor1.request()
    yield atendReq
    print('%7.2f\t Atendimento\t %s' % (env.now, name))
    yield env.timeout(random.expovariate(taxaServico))
    Servidor1.release(atendReq)
    print('%7.2f\t Partida\t %s' % (env.now, name))
    
    

def intensidadeTrafego(lambd,mi):
    return (lambd/mi)
    
def probabilidadeNenhumJob(ro):
    return (1-ro)

def numeroMedioJobsSistema(ro):
    return ro/(1-ro)

def probabilidadeNJobsSistema(ro,n,p0):
    return np.power(ro,n)*p0    

def tempoMedioResposta(mi,ro):
    return (1/mi)/(1-ro)

#intervaloConfianca = 1.96
 
print('\nM/M/1\n')
print('Tempo\t', 'Evento\t\t', 'Cliente\n')

#random.seed()

ro = intensidadeTrafego(taxaEntrada,taxaServico)
p0 = probabilidadeNenhumJob(ro)
pn = probabilidadeNJobsSistema(ro,tamanhoPopulacao,p0)
En = numeroMedioJobsSistema(ro)
Er = tempoMedioResposta(taxaServico,ro)


env = simpy.Environment()
Servidor1 = simpy.Resource(env, capacity=1)
env.process(entrada(env))
env.run()