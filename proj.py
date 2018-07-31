import random
import simpy
import numpy as np
"""
simpy: pip install simpy
msgpack: conda install -c anaconda msgpack-python
"""

tamanhoPopulacao = 2
taxaEntrada = 1.0 / 2.0        #Inverso do intervalo médio entre chegadas em minutos
taxaServico = 1.0 / 3.0    #Inverso do tempo de médio de atendimento em minutos

def entrada(env):
    for i in range(tamanhoPopulacao):
        yield env.timeout(random.expovariate(taxaEntrada))
        name = 'Cliente %d' % (i+1)
        env.process(saida(env, name))

def saida(env, name):
    momentoChegada = env.now
    print('%7.2f\t Chegada\t %s' % (env.now, name))
    atendReq = Servidor1.request()
    yield atendReq
    momentoAtendimento = env.now
    tempoEspera = momentoAtendimento - momentoChegada
    print('%7.2f\t Atendimento\t %s \t Tempo de Espera:%7.2f' % (env.now, name,tempoEspera))
    yield env.timeout(random.expovariate(taxaServico))
    Servidor1.release(atendReq)
    momentoPartida = env.now
    tempoAtendimento = momentoPartida - momentoAtendimento
    print('%7.2f\t Partida\t %s \t Tempo de Atendimento:%7.2f' % (env.now, name,tempoAtendimento))
     

def intensidadeTrafego(lambd,mi):
    return (lambd/mi)
    
def probabilidadeNenhumJob(ro):
    return (1-ro)

def numeroMedioJobs(ro):
    nMedioJobsSistema = ro/(1-ro)
    nMedioJobFila = ro*nMedioJobsSistema
    return nMedioJobsSistema,nMedioJobsSistema/(1-ro),nMedioJobFila

def probabilidadeNJobsSistema(ro,n,p0):
    return np.power(ro,n)*p0    

def tempoMedioResposta(mi,ro):
    return (1/mi)/(1-ro)

def tempoMedioEspera(ro,Er):
    return ro*Er

#intervaloConfianca = 1.96

"""
txEntrada (R[i])

tempoAtendimento (S[i])

momentoChegada[i] (A[i]) = momentoChegada[i-1] + R[i]

inicioAtendimento[i] (B[i]) = max{C[i-1];A[i]}

terminoAtendimento[i] (C[i]) = inicioAtendimento[i] + tempoAtendimento[i]


tempoFila[i] (W[i]) = inicioAtendimento[i] - momentoChegada[i]

tempoSistema[i] (U[i]) = terminoAtendimento[i] - momentoChegada[i]

tempoOciosoServidor[i] (O[i]) = inicioAtendimento[i] - terminoAtendimento[i-1]

mediaTemporal (w barrado) = sum(tempoFila[i])/numeroClientes

"""



 
print('\nM/M/1\n')
print('Tempo\t', 'Evento\t\t', 'Cliente\n')

#random.seed()

ro = intensidadeTrafego(taxaEntrada,taxaServico)
p0 = probabilidadeNenhumJob(ro)
pn = probabilidadeNJobsSistema(ro,tamanhoPopulacao,p0)
En,VarEn,EnQueue = numeroMedioJobs(ro)
Er = tempoMedioResposta(taxaServico,ro)
Ew = tempoMedioEspera(ro,Er)

for i in range(1):
    env = simpy.Environment()
    Servidor1 = simpy.Resource(env, capacity=1)
    env.process(entrada(env))
    env.run()
    print("\n")