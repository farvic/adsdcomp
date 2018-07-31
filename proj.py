import random
import simpy
import numpy as np
import statistics as st
"""
simpy: pip install simpy
msgpack: conda install -c anaconda msgpack-python
"""

tamanhoPopulacao = 2
taxaEntrada = 1.0 / 2.0        #Inverso do intervalo médio entre chegadas em minutos
taxaServico = 1.0 / 3.0    #Inverso do tempo de médio de atendimento em minutos
numeroTestes = 2

momentoChegada = [0]*100
momentoAtendimento = [0]*100
momentoPartida = [0]*100

def entrada(env):
    for i in range(tamanhoPopulacao):
        yield env.timeout(random.expovariate(taxaEntrada))
        name = 'Cliente %d' % (i+1)
        env.process(saida(env, name,i))

def saida(env, name,i):
    global momentoChegada
    global momentoAtendimento
    global momentoPartida
    momentoChegada[i] = env.now
    print('%7.2f\t Chegada\t %s' % (env.now, name))
    atendReq = Servidor1.request()
    yield atendReq
    momentoAtendimento[i] = env.now
    tempoEsperaCliente = momentoAtendimento[i] - momentoChegada[i]
    print('%7.2f\t Atendimento\t %s \t Tempo de Espera:%7.2f' % (env.now, name,tempoEsperaCliente))
    yield env.timeout(random.expovariate(taxaServico))
    Servidor1.release(atendReq)
    momentoPartida[i] = env.now
    tempoAtendimentoCliente = momentoPartida[i] - momentoAtendimento[i]
    print('%7.2f\t Partida\t %s \t Tempo de Atendimento:%7.2f' % (env.now, name,tempoAtendimentoCliente))
    
    global tempoEspera
    global tempoAtendimento
    global tempoOcioso
    
    if (i>0):
        tempoOcioso = tempoOcioso + momentoAtendimento[i] - momentoPartida[i-1]

    
    tempoEspera = tempoEspera + tempoEsperaCliente
    tempoAtendimento = tempoAtendimento + tempoAtendimentoCliente
     

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
 
print('\nM/M/1\n')
print('Tempo\t', 'Evento\t\t', 'Cliente\n')

#random.seed()
y = 0
ro = intensidadeTrafego(taxaEntrada,taxaServico)
p0 = probabilidadeNenhumJob(ro)
pn = probabilidadeNJobsSistema(ro,tamanhoPopulacao,p0)
En,VarEn,EnQueue = numeroMedioJobs(ro)
Er = tempoMedioResposta(taxaServico,ro)
Ew = tempoMedioEspera(ro,Er)

tempoEspera = 0
tempoAtendimento = 0
tempoFila = 0
tempoAtendimentoSistema = 0
tempoOciosoTotal = 0
tempoOciosoSistema = 0
vetor = [0]*100

auxiliarDesvioEsperaMedia = [0]*numeroTestes
auxiliarDesvioAtendimentoMedio = [0]*numeroTestes
auxiliarDesvioOciosidadeAmostra = [0]*numeroTestes
auxiliarDesvioOciosidadeMedia  = [0]*numeroTestes

for i in range(numeroTestes):
    tempoOcioso = 0
    tempoEspera = 0
    env = simpy.Environment()
    Servidor1 = simpy.Resource(env, capacity=1)
    env.process(entrada(env))
    env.run()
    print("\n")
    tempoEsperaMedioAmostral = tempoEspera/tamanhoPopulacao
    tempoAtendimentoMedioAmostral = tempoAtendimento/tamanhoPopulacao
    tempoOciosoMedio = tempoOcioso/tamanhoPopulacao
    
    auxiliarDesvioEsperaMedia[i] = tempoEsperaMedioAmostral
    auxiliarDesvioAtendimentoMedio[i] = tempoEsperaMedioAmostral
    auxiliarDesvioOciosidadeAmostra[i] = tempoOcioso
    auxiliarDesvioOciosidadeMedia[i] = tempoOciosoMedio
    
    print('Tempo de espera médio da amostra: %7.2f \nTempo de atendimento médio da amostra: %7.2f' % (tempoEsperaMedioAmostral,tempoAtendimentoMedioAmostral))
    print('Tempo ocioso da amostra:%7.2f' % tempoOcioso)

    print('Tempo ocioso médio da amostra:%7.2f\n' % tempoOciosoMedio)
    tempoOciosoSistema = tempoOciosoSistema + tempoOcioso
    tempoOciosoTotal = tempoOciosoTotal + tempoOciosoMedio
    tempoFila = tempoFila + tempoEsperaMedioAmostral
    tempoAtendimentoSistema = tempoAtendimentoSistema + tempoAtendimentoMedioAmostral

tempoMedioFila = tempoFila/numeroTestes
tempoMedioAtendimento = tempoAtendimentoSistema/numeroTestes

desvioMedioFila = st.stdev(auxiliarDesvioEsperaMedia)
desvioAtendimentoMedio = st.stdev(auxiliarDesvioAtendimentoMedio)
desvioOciosidadeAmostral = st.stdev(auxiliarDesvioOciosidadeAmostra)
desvioOciosidadeMedia = st.stdev(auxiliarDesvioOciosidadeMedia)

dMF = 1.96*desvioMedioFila/np.sqrt(numeroTestes)
#(tempoMedioFila - dMF, tempoMedioFila + dMF)
dAM = 1.96*desvioAtendimentoMedio/np.sqrt(numeroTestes)
#(tempoMedioAtendimento - dAM), (tempoMedioAtendimento + dAM)
dOA = 1.96*desvioOciosidadeAmostral/np.sqrt(numeroTestes)
#(tempoOciosoTotal/numeroTestes - dOA), (tempoOciosoTotal/numeroTestes + dOA)
dOM = 1.96*desvioOciosidadeMedia/np.sqrt(numeroTestes)
#(tempoOciosoSistema/numeroTestes - dOM), (tempoOciosoSistema/numeroTestes + dOM)

print('\n')
print('Tempo médio na fila:%7.2f \t Intervalo de confiança: (%7.2f,%7.2f)' % (tempoMedioFila,(tempoMedioFila - dMF), (tempoMedioFila + dMF)))
print('Tempo médio em atendimento: %7.2f\t Intervalo de confiança:(%7.2f,%7.2f)' % (tempoMedioAtendimento,(tempoMedioAtendimento - dAM), (tempoMedioAtendimento + dAM)))
print('Tempo ocioso médio entre clientes:%7.2f\t Intervalo de confiança:(%7.2f,%7.2f)' % ((tempoOciosoTotal/numeroTestes),(tempoOciosoTotal/numeroTestes - dOA), (tempoOciosoTotal/numeroTestes + dOA)))
print('Tempo ocioso médio entre clientes:%7.2f\t Intervalo de confiança:(%7.2f,%7.2f)' % ((tempoOciosoSistema/numeroTestes),(tempoOciosoSistema/numeroTestes - dOM), (tempoOciosoSistema/numeroTestes + dOM)))