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


time = clienteArquivo[:,0]
"""inputKbps = clienteArquivo[:,1]
outputKbps = clienteArquivo[:,2]"""
"""
O inputKbps e output kbps 

"""

txEntrada =[0]*4
inputKbps= clienteArquivo[:,1]
outputKbps= clienteArquivo[:,2]
tamanhoLista = len(inputKbps)

inputTotal = np.sum(inputKbps)
outputTotal = np.sum(outputKbps)

inputIperf = 0
outputIperf = 0

for i in range(116):
    inputIperf = inputIperf + inputKbps[i+58]
    outputIperf = outputIperf + outputKbps[i+58]
    

txEntrada[0] = inputTotal/tamanhoLista
txEntrada[1] = outputTotal/tamanhoLista
txEntrada[2] = inputIperf/116
txEntrada[3] = outputIperf/116

tamanhoPopulacao = 10
#taxaEntrada = 1.0 / 2.0        #Inverso do intervalo médio entre chegadas em minutos
#taxa serviço é 100Mbps = 100000 Kbps tráfego entre índice 8 e 125
taxaServico = 100000    #Inverso do tempo de médio de atendimento em minutos
numeroTestes = 100

momentoChegada = [0]*numeroTestes
momentoAtendimento = [0]*numeroTestes
momentoPartida = [0]*numeroTestes

for taxaEntrada in txEntrada:  
    def entrada(env):
        for i in range(tamanhoPopulacao):
            yield env.timeout(random.expovariate(taxaEntrada))
            name = 'Cliente %d' % (i+1)
            env.process(saida(env, name,i))
    
    def saida(env, name,i):
        global momentoChegada
        global momentoAtendimento
        global momentoPartida
        tempoEsperaCliente = [0]*numeroTestes
        tempoAtendimentoCliente = [0]*numeroTestes
        momentoChegada[i] = env.now
        #print('%f\t Chegada\t %s' % (env.now, name))
        arq.write('{:f}\t Chegada \t {!s}\n'.format(env.now,name))
        atendReq = Servidor1.request()
        yield atendReq
        momentoAtendimento[i] = env.now
        tempoEsperaCliente[i] = momentoAtendimento[i] - momentoChegada[i]
        #print('%f\t Atendimento\t %s \t Tempo de Espera:%f' % (env.now, name,tempoEsperaCliente[i]))
        arq.write('{:f}\t Atendimento\t {!s} \t Tempo de Espera: {:f}\n'.format(env.now, name,tempoEsperaCliente[i]))
        yield env.timeout(random.expovariate(taxaServico))
        Servidor1.release(atendReq)
        momentoPartida[i] = env.now
        tempoAtendimentoCliente[i] = momentoPartida[i] - momentoAtendimento[i]
        #print('%f\t Partida\t %s \t Tempo de Atendimento:%f' % (env.now, name,tempoAtendimentoCliente[i]))
        arq.write('{:f}\t Partida\t {!s} \t Tempo de Atendimento: {:f}\n'.format(env.now, name,tempoAtendimentoCliente[i]))
        
        global tempoEspera
        global tempoAtendimento
        global tempoOcioso
        
        if (i>0):
            tempoOcioso = tempoOcioso + momentoAtendimento[i] - momentoPartida[i-1]
    
        
        tempoEspera = tempoEspera + tempoEsperaCliente[i]
        tempoAtendimento = tempoAtendimento + tempoAtendimentoCliente[i]
         
    """
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
    """
    #intervaloConfianca = 1.96
     
    #print('\nM/M/1\n')
    #print('Tempo\t', 'Evento\t\t', 'Cliente\n')
    arq.write('\t\tSimulador M/M/1\n')
    arq.write('Tempo\t\t Evento\t\t Cliente\n\n')
    
    y = 0
    """
    ro = intensidadeTrafego(taxaEntrada,taxaServico)
    p0 = probabilidadeNenhumJob(ro)
    pn = probabilidadeNJobsSistema(ro,tamanhoPopulacao,p0)
    En,VarEn,EnQueue = numeroMedioJobs(ro)
    Er = tempoMedioResposta(taxaServico,ro)
    Ew = tempoMedioEspera(ro,Er)
    """
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
        env.process(entrada(env))
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
        
        """print('Tempo de espera médio da amostra: %f \nTempo de atendimento médio da amostra: %7.2f' % (tempoEsperaMedioAmostral,tempoAtendimentoMedioAmostral))
        print('Tempo ocioso da amostra:%f' % tempoOcioso)
        print('Tempo ocioso médio da amostra:%f\n' % tempoOciosoMedio)"""

        
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
    #(tempoMedioFila - dMF, tempoMedioFila + dMF)
    dAM = 1.96*desvioAtendimentoMedio/np.sqrt(numeroTestes)
    #(tempoMedioAtendimento - dAM), (tempoMedioAtendimento + dAM)
    dOA = 1.96*desvioOciosidadeAmostral/np.sqrt(numeroTestes)
    #(tempoOciosoTotal/numeroTestes - dOA), (tempoOciosoTotal/numeroTestes + dOA)
    dOM = 1.96*desvioOciosidadeMedia/np.sqrt(numeroTestes)
    #(tempoOciosoSistema/numeroTestes - dOM), (tempoOciosoSistema/numeroTestes + dOM)
    
    """
    print('\n')
    print('Tempo médio na fila:%f \t Intervalo de confiança: (%f,%f)' % (tempoMedioFila,(tempoMedioFila - dMF), (tempoMedioFila + dMF)))
    print('Tempo médio em atendimento: %f\t Intervalo de confiança:(%f,%f)' % (tempoMedioAtendimento,(tempoMedioAtendimento - dAM), (tempoMedioAtendimento + dAM)))
    print('Tempo ocioso médio entre clientes:%f\t Intervalo de confiança:(%f,%f)' % ((tempoOciosoTotal/numeroTestes),(tempoOciosoTotal/numeroTestes - dOA), (tempoOciosoTotal/numeroTestes + dOA)))
    print('Tempo ocioso médio do sistema:%f\t Intervalo de confiança:(%f,%f)' % ((tempoOciosoSistema/numeroTestes),(tempoOciosoSistema/numeroTestes - dOM), (tempoOciosoSistema/numeroTestes + dOM)))
    """
    arq.write('\n')
    arq.write('Tempo médio na fila: {:f} \t Intervalo de confiança: ({:f},{:f})'.format(tempoMedioFila,(tempoMedioFila - dMF), (tempoMedioFila + dMF)))
    arq.write('Tempo médio em atendimento: {:f}\t Intervalo de confiança: ({:f},{:f})'.format(tempoMedioAtendimento,(tempoMedioAtendimento - dAM), (tempoMedioAtendimento + dAM)))
    arq.write('Tempo ocioso médio entre clientes: {:f}\t Intervalo de confiança:({:f},{:f})\n\n'.format((tempoOciosoTotal/numeroTestes),(tempoOciosoTotal/numeroTestes - dOA), (tempoOciosoTotal/numeroTestes + dOA)))
    
    plt.title('Tempo de espera médio')
    plt.plot(auxiliarDesvioEsperaMedia)
    x = np.arange(0,numeroTestes,1)
    plt.errorbar(x,auxiliarDesvioEsperaMedia,yerr=1.69,fmt='o')
    plt.savefig('EsperaMedia.png',dpi=300)
    plt.show()
    
    print(txEntrada)

arq.close()