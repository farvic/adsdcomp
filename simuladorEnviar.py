"""
Avaliação de Desempenho de Sistemas
Aluno: Victor Fonseca Araujo

Simulador de Fila M/M/1
"""

import random
import simpy
import numpy as np
import statistics as st
import matplotlib.pyplot as plt
import string

"""
simpy: pip install simpy
msgpack: conda install -c anaconda msgpack-python
"""
clienteArquivo = np.genfromtxt("captura1.txt",usecols=(0,1,2),skip_header=1,dtype=int)
arq = open('salvar.txt','w')
arqv = open('resultadoSimulacao.txt','w')


time = clienteArquivo[:,0]

fila = 0

txEntrada =[0]*6
inputKbps= clienteArquivo[:,1]
outputKbps= clienteArquivo[:,2]
tamanhoLista = len(inputKbps)

inputTotal = np.sum(inputKbps)
outputTotal = np.sum(outputKbps)

inputIperf = 0
outputIperf = 0
fila = 0

for i in range(116):
    inputIperf = inputIperf + inputKbps[i+58]
    outputIperf = outputIperf + outputKbps[i+58]

outputx = 0
inputx = 0

for i in range(58):
    inputx = inputx+inputKbps[i]
    outputx = outputx+outputKbps[i]    

for i in range(63):
    inputx = inputx+inputKbps[i+174]
    outputx = outputx+outputKbps[i+174]
    
txEntrada[0] = inputTotal/tamanhoLista
txEntrada[1] = outputTotal/tamanhoLista
txEntrada[2] = inputIperf/117
txEntrada[3] = outputIperf/117
txEntrada[4] = inputx/121
txEntrada[5] = outputx/121


tamanhoPopulacao = 100
#taxa serviço é 100Mbps = 100000 Kbps tráfego entre índice 8 e 125
taxaServico = 100000
numeroTestes = 100

momentoChegada = [0]*tamanhoPopulacao
momentoAtendimento = [0]*tamanhoPopulacao
momentoPartida = [0]*tamanhoPopulacao
clientesFila = [0]*tamanhoPopulacao

for taxaEntrada in txEntrada:  
    def entrada(env,fila,clientesFila):
        fila = fila + 1
        for i in range(tamanhoPopulacao):
            yield env.timeout(random.expovariate(taxaEntrada))
            env.process(saida(env, i,fila))
            clientesFila[i] = fila
    
    def saida(env,i,fila):
        fila = fila - 1
        global momentoChegada
        global momentoAtendimento
        global momentoPartida
        tempoEsperaCliente = [0]*tamanhoPopulacao
        tempoAtendimentoCliente = [0]*tamanhoPopulacao
        momentoChegada[i] = env.now
        atendReq = Servidor1.request()
        yield atendReq
        momentoAtendimento[i] = env.now
        tempoEsperaCliente[i] = momentoAtendimento[i] - momentoChegada[i]
        yield env.timeout(random.expovariate(taxaServico))
        Servidor1.release(atendReq)
        momentoPartida[i] = env.now
        tempoAtendimentoCliente[i] = momentoPartida[i] - momentoAtendimento[i]
                
        global tempoEspera
        global tempoAtendimento
        global tempoOcioso
        
        if (i>0):
            tempoOcioso = tempoOcioso + momentoAtendimento[i] - momentoPartida[i-1]
    
        
        tempoEspera = tempoEspera + tempoEsperaCliente[i]
        tempoAtendimento = tempoAtendimento + tempoAtendimentoCliente[i]

    #intervaloConfianca = 1.96
     
    arq.write('\t\tSimulador M/M/1\n')
    #arq.write('Tempo\t\t Evento\t\t Cliente\n\n')
    
    y = 0

    tempoEspera = 0
    tempoAtendimento = 0
    tempoFila = 0
    tempoAtendimentoSistema = 0
    tempoOciosoTotal = 0
    tempoOciosoSistema = 0
    vetor = [0]*numeroTestes
    
    auxiliarDesvioEsperaMedia = [0]*numeroTestes
    auxiliarDesvioAtendimentoMedio = [0]*numeroTestes
    auxiliarDesvioOciosidadeAmostra = [0]*numeroTestes
    auxiliarDesvioOciosidadeMedia  = [0]*numeroTestes
    
    for i in range(numeroTestes):
        tempoOcioso = 0
        tempoEspera = 0
        env = simpy.Environment()
        Servidor1 = simpy.Resource(env, capacity=1)
        env.process(entrada(env,fila,clientesFila))
        env.run()
        #print("\n")
        arq.write('\n')
        tempoEsperaMedioAmostral = tempoEspera/tamanhoPopulacao
        tempoAtendimentoMedioAmostral = tempoAtendimento/tamanhoPopulacao
        tempoOciosoMedio = tempoOcioso/tamanhoPopulacao
        
        auxiliarDesvioEsperaMedia[i] = tempoEsperaMedioAmostral
        auxiliarDesvioAtendimentoMedio[i] = tempoAtendimentoMedioAmostral
        auxiliarDesvioOciosidadeAmostra[i] = tempoOcioso
        auxiliarDesvioOciosidadeMedia[i] = tempoOciosoMedio
                
        arq.write('Tempo de Espera Médio da Amostra: {:f}\nTempo de Atendimento Médio da Amostra: {:.2f}\n'.format(tempoEsperaMedioAmostral,tempoAtendimentoMedioAmostral))
        arq.write('Tempo Ocioso da Amostra: {:f} '.format(tempoOcioso))
        arq.write('Tempo Ocioso Médio da Amostra: {:f}\n\n'.format(tempoOciosoMedio))
        
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
    dAM = 1.96*desvioAtendimentoMedio/np.sqrt(numeroTestes)
    dOA = 1.96*desvioOciosidadeAmostral/np.sqrt(numeroTestes)
    dOM = 1.96*desvioOciosidadeMedia/np.sqrt(numeroTestes)
    
    arq.write('\n')
    arq.write('Tempo médio na fila: {:f} \t Intervalo de confiança: ({:f},{:f})\n'.format(tempoMedioFila,(tempoMedioFila - dMF), (tempoMedioFila + dMF)))
    arq.write('Tempo médio em atendimento: {:f}\t Intervalo de confiança: ({:f},{:f})\n'.format(tempoMedioAtendimento,(tempoMedioAtendimento - dAM), (tempoMedioAtendimento + dAM)))
    arq.write('Tempo ocioso médio entre clientes: {:f}\t Intervalo de confiança:({:f},{:f})\n\n'.format((tempoOciosoTotal/numeroTestes),(tempoOciosoTotal/numeroTestes - dOA), (tempoOciosoTotal/numeroTestes + dOA)))
    
    arqv.write('Tempo médio na fila: {:f} \t Intervalo de confiança: ({:f},{:f})\n'.format(tempoMedioFila,(tempoMedioFila - dMF), (tempoMedioFila + dMF)))
    arqv.write('Tempo médio em atendimento: {:f}\t Intervalo de confiança: ({:f},{:f})\n'.format(tempoMedioAtendimento,(tempoMedioAtendimento - dAM), (tempoMedioAtendimento + dAM)))
    arqv.write('Tempo ocioso médio entre clientes: {:f}\t Intervalo de confiança:({:f},{:f})\n\n'.format((tempoOciosoTotal/numeroTestes),(tempoOciosoTotal/numeroTestes - dOA), (tempoOciosoTotal/numeroTestes + dOA)))

    
print(txEntrada)
arq.write('Lambda inputTotal: {:f} / Lambda outputTotal: {:f}\n'.format(txEntrada[0],txEntrada[1]))
arq.write('Lambda inputDuranteIperf: {:f} / Lambda outputDuranteIperf: {:f}\n'.format(txEntrada[2],txEntrada[3]))
arq.write('Lambda inputSemIperf: {:f} / Lambda outputSemIperf: {:f}'.format(txEntrada[4],txEntrada[5]))

arq.close()
arqv.close()