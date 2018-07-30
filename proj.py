import random
import simpy

"""
simpy: pip install simpy
msgpack: conda install -c anaconda msgpack-python
"""

qtdClientes = 10
taxaChegada = 1.0 / 6.0        #Inverso do intervalo médio entre chegadas em minutos
taxaAtendimento = 1.0 / 5.0    #Inverso do tempo de médio de atendimento em minutos

def entrada(env):
    """ Gera as chegadas dos clientes no sistema """
    for i in range(qtdClientes):
        yield env.timeout(random.expovariate(taxaChegada))
        name = 'Cliente %d' % (i+1)
        env.process(saida(env, name))

def saida(env, name):
    """ Simula atendimento dos clientes no servidor 1 """
    print('%7.2f\t Chegada\t %s' % (env.now, name))
    atendReq = Servidor1.request()
    yield atendReq
    print('%7.2f\t Atendimento\t %s' % (env.now, name))
    yield env.timeout(random.expovariate(taxaAtendimento))
    Servidor1.release(atendReq)
    print('%7.2f\t Partida\t %s' % (env.now, name))
 
""" Bloco principal """
print('\nM/M/1\n')
print('Tempo\t', 'Evento\t\t', 'Cliente\n')

random.seed(10)
env = simpy.Environment()
Servidor1 = simpy.Resource(env, capacity=1)
env.process(entrada(env))
env.run()