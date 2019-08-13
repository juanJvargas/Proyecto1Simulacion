
import random
import simpy


RANDOM_SEED = 42
ENSAMBLY_DURATION = 30.0    # Duration of other jobs in minutes
WEEKS = 4              # Simulation time in weeks
SIM_TIME = WEEKS * 7 * 24 * 60  # Simulation time in minutes

Q = 0 # Number of parts assembled with the machine
P1 = 0 # Number of parts in queue 1
P2 = 0 # Number of parts in queue 2
MaxIterations = 100 #Max numbers of iterations

AT_Part1=[]
AT_Part2=[]
ET_Parts=[]
ocupada = False


def Tiempo_para_llegada_parte1():
    """Returns the arrival time of part 1"""
    #return random.uniform(1,6)    
    #return random.triangular(1,6) #distribucion triangular 1<=x<=6
    return random.normalvariate(4,0.5) #distribucion normal con media=4 y desviacion=0.5

def Tiempo_para_llegada_parte2():
    """Returns the arrival time of part 2"""
    #return random.uniform(3,8)    
    #return random.triangular(3,8) #distribucion triangular 3<=x<=8
    return random.normalvariate(5,0.5) #distribucion normal con media=5 y desviacion=0.5

def Tiempo_para_ensamblaje():
    """Returns the completion time of the two-part assembly"""
    #return random.uniform(5,9)    
    #return random.triangular(5,9) #distribucion triangular 3<=x<=8
    return random.normalvariate(7,0.5) #distribucion normal con media=7 y desviacion=0.5

def Tiempo_de_espera_prom_partes1():
    global AT_Part1
    global ET_Parts
    contador = 0
    t= len(AT_Part1)
    for i in range(t):
        contador += ET_Parts[i] - AT_Part1[i]
        print("Parte 1 #%d tiempo de llegada: %d"%(i, AT_Part1[i]))
        print("Parte 1 #%d tiempo de Salida: %d"%(i, ET_Parts[i]))
        print("Parte 1 #%d tiempo de espera: %d"%(i, ET_Parts[i] - AT_Part1[i]))
    return (contador/len(AT_Part1))

def Timepo_de_espera_prom_partes2():
    global AT_Part2
    global ET_Parts
    contador = 0
    t= len(AT_Part2)
    for i in range(t):
        contador += ET_Parts[i] - AT_Part2[i]
    return (contador/len(AT_Part2))

def GenerateP1(env, maquina):
    global P1
    global P2
    global ocupada
    global AT_Part1
    env.process(GenerateP2(env, maquina))
    contador = 0
    while contador < MaxIterations:
        tiempo =   Tiempo_para_llegada_parte1()
        yield env.timeout(tiempo)
        print ("Una parte 1 llegó en: %d"%(env.now))
        AT_Part1.append(int(env.now))
        P1 += 1
        contador += 1
        if((P1 > 0) and (P2 > 0) and (not ocupada)):
            env.process(maquina.ensamblaje(env))
            
def GenerateP2(env, maquina):
    global P1
    global P2
    global ocupada
    global AT_Part2
    contador = 0
    while contador < MaxIterations:
        tiempo =   Tiempo_para_llegada_parte2()
        yield env.timeout(tiempo)
        print ("Una parte 2 llegó en: %d"%(env.now))
        AT_Part2.append(int(env.now))
        P2 = P2 + 1
        contador += 1
        if((P1 > 0) and (P2 > 0) and (not ocupada)):
            env.process(maquina.ensamblaje(env))
    print (contador)

class Maquina(object):
    """
    A machine assembles two different types of machinery parts in an expected time 
    """
    
    def __init__(self, env):
        self.env = env
    
    def ensamblaje(self, env):
        global Q
        global P1
        global P2
        global ocupada
        global ET_Parts
        ocupada= True
        while ocupada:
            tiempo_ensablaje = Tiempo_para_ensamblaje()
            print ("Se ha empezado a ensamblar un par de partes en t = %d" %(env.now))
            ET_Parts.append(int(env.now))
            yield self.env.timeout(tiempo_ensablaje)
            Q += 1
            P1 -= 1
            P2 -= 1
            print ("Se han ensamblado las partes en el tiempo t = %d" %(env.now))
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
    print("Partes ensambladas = " + str(Q)) 
    print("Tiempo promedio de espera para las partes 1: %d"%Tiempo_de_espera_prom_partes1())
    print("Tiempo promedio de espera para las partes 2: %d"%Tiempo_de_espera_prom_partes2())

if __name__ == "__main__":
    main()
