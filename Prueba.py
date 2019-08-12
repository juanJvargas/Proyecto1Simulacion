
import random

import simpy


RANDOM_SEED = 42
ENSAMBLY_DURATION = 30.0    # Duration of other jobs in minutes
WEEKS = 4              # Simulation time in weeks
SIM_TIME = WEEKS * 7 * 24 * 60  # Simulation time in minutes
Q = 0 #Numero de partes ensambladas con la maquina
P1 = 0 #numero de partes 1 en la cola
P2 = 0 #numero de partes 2 en la cola
MaxIterations = 100 #Numero maximo de operacion de ensamble que se realizaran
ocupada = False


def Tiempo_para_llegada_parte1():
    """Retorna el tiempo de llegada de la parte 1."""
    return random.uniform(1,6)

def Tiempo_para_llegada_parte2():
    """Retorna el timepo de lelgada de la parte 2."""
    return random.uniform(3,8)

def Tiempo_para_ensamblaje():
    """Retorna el tiempo de finalizacion del ensamblaje de dos partes."""
    return random.uniform(5,9)

def GenerateP1(env, maquina):
    global P1
    global P2
    global ocupada
    env.process(GenerateP2(env, maquina))
    global ocupada
    contador = 0
    while contador < MaxIterations:
        tiempo =   Tiempo_para_llegada_parte1()
        yield env.timeout(tiempo)
        print ("una parte 1 llego en: %d"%(env.now))
        P1 += 1
        contador += 1
        if((P1 > 0) and (P2 > 0) and (not ocupada)):
            env.process(maquina.ensamblaje(env))
            
def GenerateP2(env, maquina):
    global P1
    global P2
    global ocupada
    contador = 0
    while contador < MaxIterations:
        tiempo =   Tiempo_para_llegada_parte2()
        yield env.timeout(tiempo)
        print ("una parte 2 llego en: %d"%(env.now))
        P2 = P2 + 1
        contador += 1
        if((P1 > 0) and (P2 > 0) and (not ocupada)):
            env.process(maquina.ensamblaje(env))
    print (contador)

class Maquina(object):
    """
    Una maquina ensambla dos tipos partes de maquinaria diferentes en un tiempo previsto 
    """
    
    def __init__(self, env):
        self.env = env
    
    def ensamblaje(self, env):
        global Q
        global P1
        global P2
        global ocupada
        ocupada= True
        while ocupada:
            tiempo_ensablaje = Tiempo_para_ensamblaje()
            print ("Se ha empezado a ensamblar un par de partes en t = %d" %(env.now))
            yield self.env.timeout(tiempo_ensablaje)
            Q += 1
            P1 -= 1
            P2 -= 1
            print ("Se han ensamblado las partes en el timepo t = %d" %(env.now))
            if( P1 == 0 or  P2 == 0):
                print(Q)
                ocupada = False
            
            

def proc():
    global Q
    global MaxIterations
    if(Q == MaxIterations):
        return None

def main():
    env = simpy.Environment()
    maquina = Maquina(env)
    env.process(GenerateP1(env, maquina))
    env.run(until=(proc()))
    print("Partes ensambladas = " + str(Q) + "\nPartes1 por ensamblar" + str(P1) + "\nPartes2 por ensamblar" + str(P2)) 

if __name__ == "__main__":
    main()