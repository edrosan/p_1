import random

# Revisa si hay espacio disponible en memoria
# Return = -1 -> no hay espacio disponible
# Return != -1 -> hay espacio disponible
def espacio_memoria (memoria, tam):
    contador = 0
    posicion = -1

    for pos, proceso in enumerate(memoria):
        if (proceso == 0):
            contador += 1
            if (posicion == -1): posicion = pos
        elif (proceso != 0):
            contador = 0;
            posicion = -1
        if ( contador == tam ): return posicion
    
    return -1


def crear_proceso(PID, tam, lugar):
    n = random.randrange(1,10)
    estado = ''
    prioridad = 0

    if (n >= 1 and n <= 4):
        estado = 'x'
        prioridad = 3
    elif ( n>=5 and n <=7):
        estado = 'w'
        prioridad = 1
    elif (n >= 8 and n <=10):
        estado = 'r'
        prioridad = 2

    return {'pid': PID, 'tam_proceso': tam, 'estado': estado, 'prioridad': prioridad, 'memoria': lugar}
    # return [PID, tam, estado, prioridad, lugar]


# Agrega a memoria el proceso
def agregar_memoria(memoria, posicion_insercion, pid, tam_proceso):
    for i in range(0, tam_proceso):
        memoria[posicion_insercion + i] = pid

    return memoria


def buscar_tabla (tabla_procesos, prioridad_maxima, memoria_buscar, memoria_mover ):
    pos = -1
    tam = -1
    prioridad = 1

    for i in range(0, prioridad_maxima):
        
        for (indice, nodo) in enumerate(tabla_procesos):
            if (nodo['memoria'] == memoria_buscar and nodo['prioridad'] == prioridad):
                if (nodo['tam_proceso'] > tam):
                    pos = indice
                    tam = nodo['pid']

        if (pos != -1):
            tabla_procesos[pos]['memoria'] = memoria_mover
            return (tabla_procesos, tabla_procesos[pos])
            
        elif(pos == -1):
            prioridad += 1

    return (tabla_procesos, -1)

def eliminar_memoria(memoria, pid):
    for (indice, proceso) in enumerate(memoria):
        if proceso == pid:
            memoria[indice] = 0;
    return memoria



def crear_mapa_bits(tam_memoria):
    mapaBits = []
    n = (tam_memoria // 8)
    for i in range(n): 
        mapaBits.append([0] * 8)
    return mapaBits

def llenar_mapa(memoria, mapa_bits):
    for (i, proceso) in enumerate(memoria):
        fila = i // 8
        columna = i % 8

        if (proceso != 0): 
            mapa_bits[fila][columna] = 1
        elif(proceso == 0): 
            mapa_bits[fila][columna] = 0
    return mapa_bits

colores = {
    '1'   : '\x1b[48;5;52m',
    '2'   : '\x1b[48;5;61m',
    '3'   : '\x1b[48;5;94m',
    '4'   : '\x1b[48;5;17m',
    '5'   : '\x1b[48;5;89m',
    'amarillo'   : '\x1b[38;5;220m',
    'verde' : '\x1b[48;5;28m',
    'rojo'  : '\x1b[48;5;124m',
    'default'   : '\x1b[0m'
}

def print_mapa(mapa_bits):
    linea = ''
    print()
    for line in mapa_bits:
        for element in line:
            if (element == 0): linea += colores['verde']+' 0 '+colores['default']
            elif(element == 1): linea += colores['rojo']+' 1 '+colores['default']
        print(linea)
        linea = '' 
    print()  

def crear_lista_ligada(ram):
    contProcesos = 0
    contHuecos = 0
    lista = []

    for indice in range(len(ram)): 
        if(ram[indice] == 0):#* encontro hueco
            if(contProcesos != 0): 
                posFinal = (contProcesos - 1) + posInicial
                lista.append(['P', [posInicial, posFinal]])
                contProcesos = 0
            if(contHuecos == 0): posInicial = indice
            contHuecos += 1
        elif(ram[indice] != 0):#* encuentra proceso
            if(contHuecos!=0): 
                posFinal = (contHuecos - 1) + posInicial
                lista.append(['H', [posInicial, posFinal]])
                contHuecos = 0
            if(contProcesos == 0): posInicial = indice
            contProcesos += 1

    #* Agrega al ultimo proceso en la RAM
    if(contHuecos!=0):
        posFinal = (contHuecos-1)+posInicial
        lista.append(['H', [posInicial, posFinal]])
    elif(contProcesos!=0):
        posFinal = (contProcesos-1)+posInicial
        lista.append(['P', [posInicial, posFinal]])
    return lista

def print_lista_color(listaLigada):
    print()
    for i in listaLigada:
        if(i[0]=='H'): 
            print('[',colores['verde'],i[0],colores['default'],'|',i[1][0],'/',i[1][1],']->', end=' ')
        else: 
            print('[',colores['rojo'],i[0],colores['default'],'|',i[1][0],'/',i[1][1],']->', end=' ')
    print('\n')


def lista (ram):
    contHueco = 0
    contProce = 0
    procesoActual = 0
    tam = len (ram)
    lista = []

    for (i, elemento) in  enumerate(ram):
        if (elemento == 0):
            contHueco+= 1
            if (contProce != 0):
                posFinal = i-1
                posInicial = posFinal-contProce+1
                tam_proceso = (posFinal - posInicial) + 1
                lista.append(["P",tam_proceso,posInicial,posFinal])
                contProce = 0
        elif (elemento != 0):  
            if (contHueco != 0):
                posFinal = i-1
                posInicial = posFinal-contHueco+1
                tam_proceso = (posFinal - posInicial) + 1
                lista.append(["H",tam_proceso,posInicial,posFinal])
                contHueco = 0 
            if (contProce == 0):
                procesoActual = elemento
                contProce+= 1
            else:
                if (procesoActual == elemento):
                    contProce+=1
                else:
                    posFinal = i-1
                    posInicial = posFinal-contProce+1
                    tam_proceso = (posFinal - posInicial) + 1
                    lista.append(["P",tam_proceso,posInicial,posFinal])
                    contProce = 0
                    procesoActual = elemento
                    contProce+= 1
    if (contHueco != 0):
        posFinal = tam-1
        posInicial = posFinal-contHueco+1
        tam_proceso = (posFinal - posInicial) + 1
        lista.append(["H",tam_proceso,posInicial,posFinal])
        contHueco = 0
    if (contProce != 0):
        posFinal = tam-1
        posInicial = posFinal-contProce+1
        tam_proceso = (posFinal - posInicial) + 1
        lista.append(["P",tam_proceso,posInicial,posFinal])
        contProce = 0
    return lista 


def lista_nombre (ram):
    contHueco = 0
    contProce = 0
    procesoActual = 0
    tam = len (ram)
    lista = []

    for (i, elemento) in  enumerate(ram):
        if (elemento == 0):
            contHueco+= 1
            if (contProce != 0):
                posFinal = i-1
                posInicial = posFinal-contProce+1
                tam_proceso = (posFinal - posInicial) + 1
                lista.append([procesoActual,tam_proceso,posInicial,posFinal])
                contProce = 0
        elif (elemento != 0):  
            if (contHueco != 0):
                posFinal = i-1
                posInicial = posFinal-contHueco+1
                tam_proceso = (posFinal - posInicial) + 1
                lista.append(['H',tam_proceso,posInicial,posFinal])
                contHueco = 0 
            if (contProce == 0):
                procesoActual = elemento
                contProce+= 1
            else:
                if (procesoActual == elemento):
                    contProce+=1
                else:
                    posFinal = i-1
                    posInicial = posFinal-contProce+1
                    tam_proceso = (posFinal - posInicial) + 1
                    lista.append([procesoActual,tam_proceso,posInicial,posFinal])
                    contProce = 0
                    procesoActual = elemento
                    contProce+= 1

    if (contHueco != 0):
        posFinal = tam-1
        posInicial = posFinal-contHueco+1
        tam_proceso = (posFinal - posInicial) + 1
        lista.append(['H',tam_proceso,posInicial,posFinal])
        contHueco = 0
    if (contProce != 0):
        posFinal = tam-1
        posInicial = posFinal-contProce+1
        tam_proceso = (posFinal - posInicial) + 1
        lista.append([ram[-1] ,tam_proceso,posInicial,posFinal])
        contProce = 0
    return lista 

def eliminar_tabla(tabla_procesos, pid):
    for proceso in tabla_procesos:
        if proceso['pid'] == pid:
            tabla_procesos.remove(proceso)
    return tabla_procesos


def buscar_primero(memoria):
    for proceso in memoria:
        if proceso != 0:
            return proceso

def buscar_p_tabla( tabla_procesos, pid):

    for proceso in tabla_procesos:
        if proceso['pid'] == pid:
            return proceso

    return -1




def compactar(memoria, memoria_auxiliar, tabla_procesos):
    pid_auxiliar = -1
    for proceso in memoria:
        if proceso != 0 and proceso != pid_auxiliar :
            proceso_auxiliar = buscar_p_tabla( tabla_procesos, proceso)
            pid_auxiliar = proceso_auxiliar['pid']
            posicion_insercion = espacio_memoria (memoria_auxiliar, proceso_auxiliar['tam_proceso'])
            memoria_auxiliar = agregar_memoria(memoria_auxiliar, posicion_insercion, pid_auxiliar, proceso_auxiliar['tam_proceso'])
    return memoria_auxiliar
