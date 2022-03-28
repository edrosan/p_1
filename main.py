from fun import *

run = True
tam_memoria = 16

ram = [0] * tam_memoria
mv = [0] * tam_memoria
mapa_bits = crear_mapa_bits(tam_memoria)
lista_huecos = lista(ram)
lista_nombres = lista_nombre(ram)

tabla_procesos = []

pid = 1709

while(run):
    print("")
    print("1.Crear proceso")
    print("2.Finalizar")
    print("3.Compactacion")
    print("4.Representacion")
    print("5.Salir")
    respuesta = int(input("Ingrese una opcion: "))

#*---------------------------------------------------------------------------------------------------------------
    if respuesta == 1:# Crear proceso
        tam_proceso = int(input('Ingrese el tamaño del proceso: '))
        posicion_insercion = espacio_memoria(ram, tam_proceso)
    #---------------------------------------------------------------------------------------------------------------

        if (posicion_insercion != -1):# Memoria con espacio disponible 
            pid += 1
            ram = agregar_memoria(ram, posicion_insercion, pid, tam_proceso)
            proceso_creado = crear_proceso(pid, tam_proceso, 'ram')
            tabla_procesos.append(proceso_creado)
    #---------------------------------------------------------------------------------------------------------------
        elif(posicion_insercion == -1):# Memoria RAM sin espacio disponible
            #* Se busca el proceso a mover de RAM a MV

            (tabla_procesos, proceso_mover) = buscar_tabla(tabla_procesos, 2,"ram", "ram")
            print(f'Proceso a mover: {proceso_mover}')

            if (proceso_mover != -1): #* Hay procesos a mover de RAM a MV
                posicion_insercion = espacio_memoria(mv, proceso_mover['tam_proceso'])
                mover = True
            else: #* No hay procesos a mover de Ram a MV
                posicion_insercion = espacio_memoria(mv, tam_proceso)
                mover = False

    #---------------------------------------------------------------------------------------------------------------
    #? Mover = Hay procesos a mover en RAM
    #? Not Mover = No hay procesos a mover en RAM
    #? posicion_insercion != -1 Hay espacio en MV 
    #? posicion_insercion == -1 No hay  espacio en MV
    #*---------------------------------------------------------------------------------------------------------------
    # Caso 1
    # Hay procesos en RAM para mover y hay espacio en MV
            if(mover and posicion_insercion != -1): 
                print("\nCaso 1:\n")
                pid += 1
                proceso_creado = crear_proceso(pid, tam_proceso, 'ram')
                print("Proceso creado: ", proceso_creado)
                try_add = True
                if proceso_creado['prioridad'] != 3 or proceso_creado['prioridad'] == 3:
                    while try_add:
                        (tabla_procesos, proceso_mover) = buscar_tabla(tabla_procesos, 2,"ram", "ram")
                        if proceso_mover != -1:# Encontro algun proceso para mover a MV
                            posicion_insercion = espacio_memoria(mv, proceso_mover['tam_proceso'])
                            if posicion_insercion != -1:# Hay espacio en MV para mover el proceso
                                (tabla_procesos, proceso_mover) = buscar_tabla(tabla_procesos, 2,"ram", "mv")
                                ram = eliminar_memoria(ram, proceso_mover['pid'])
                                mv = agregar_memoria(mv, posicion_insercion, proceso_mover['pid'], proceso_mover['tam_proceso'])
                                posicion_insercion = espacio_memoria(ram, proceso_creado["tam_proceso"])
                                if posicion_insercion != -1:# Si hay espacio en RAM introduce el nuevo proceso
                                    ram = agregar_memoria(ram, posicion_insercion, proceso_creado['pid'], proceso_creado['tam_proceso'])
                                    tabla_procesos.append(proceso_creado)
                                    try_add = False
                            elif posicion_insercion == -1:# No hay espacio en MV para mover el proceso
                                print("Ya no hay espacio en MV")
                                print("1.Eliminar nuevo proceso ")
                                print("2.Intentar eliminar proceso 'w' en MV y seguir intentando mover procesos")
                                respuesta = int(input("Ingrese una opcion: "))
                                if respuesta == 1:
                                    print("Proceso eliminado")
                                    pid -= 1
                                    try_add = False
                                elif respuesta == 2:
                                    (tabla_procesos, proceso_eliminar) = buscar_tabla(tabla_procesos, 1,"mv", "mv")
                                    if proceso_eliminar != -1:# Encuentra proceso 'w' en MV para eliminar
                                        mv = eliminar_memoria(ram, proceso_eliminar['pid'])
                                        tabla_procesos.remove(proceso_eliminar)
                                    elif proceso_eliminar == -1:# No encuentra proceso 'w' en MV
                                        print("No hay procesos disponiblea a eliminar")
                                        print("Finalice manualmente algun proceso")
                                        pid -= 1
                                        try_add = False
                        elif proceso_mover == -1:# No hay procesos para mover de RAM a MV
                            print(f"Ya no hay mas procesos a mover de RAM a MV")
                            print(f"1.Eliminar nuevo proceso")
                            print(f"2.Interntar ingresar nuevo proceso a MV como 'w'")
                            respuesta = int(input("Ingrese una opcion: "))
                            if (respuesta == 1):
                                print("Proceso eliminado")
                                pid -= 1
                                try_add = False
                            elif respuesta == 2:
                                proceso_creado['estado'] = 'w' 
                                proceso_creado['prioridad'] = 1 
                                proceso_creado['memoria'] = 'mv'
                                posicion_insercion = espacio_memoria(mv, proceso_creado['tam_proceso'])
                                if posicion_insercion != -1:
                                    mv = agregar_memoria(mv, posicion_insercion, proceso_creado['pid'], proceso_creado['tam_proceso'])
                                    tabla_procesos.append(proceso_creado)
                                    try_add = False
                                elif posicion_insercion == -1:
                                    print ("No hay espacio suficiente en MV")
                                    print("1.Eliminar nuevo proceso")
                                    print("2.Eliminar procesos 'w' e intentar ingresar el nuevo proceso ")
                                    respuesta = int(input("Ingrese una opcion: "))
                                    if respuesta == 1:
                                        print("proceso eliminado")
                                        pid -= 1
                                        try_add = False
                                    elif respuesta == 2:
                                        while try_add:
                                            (tabla_procesos, proceso_eliminar) = buscar_tabla(tabla_procesos, 1,"mv", "mv")
                                            if (proceso_eliminar != -1):
                                                mv = eliminar_memoria(mv, proceso_eliminar['pid'])
                                                tabla_procesos.remove(proceso_eliminar)
                                                posicion_insercion = espacio_memoria(mv, proceso_creado['tam_proceso'])
                                                if posicion_insercion != -1:
                                                    mv = agregar_memoria(mv, posicion_insercion, proceso_creado['pid'], proceso_creado['tam_proceso'])
                                                    tabla_procesos.append(proceso_creado)
                                                    try_add = False
                                            elif (proceso_eliminar == -1):
                                                print("No hay procesos a eliminar de MV")
                                                print("Finalice manualmente algun proceso")
                                                pid -= 1
                                                try_add = False
    #*---------------------------------------------------------------------------------------------------------------
    # Caso 2
            elif (mover and posicion_insercion == -1):
                print("\nCaso 2:\n")
                pid += 1
                proceso_creado = crear_proceso(pid, tam_proceso, 'ram')
                try_add = True
                print("Memoria RAM y MV sin espacio disponible")
                print("1.Eliminar proceso en MV con estado: espera 'w' e intentar mover procesos de RAM ")
                print("2.No agregar proceso")
                respuesta = int(input("Ingrese una opcion: "))
                if (respuesta == 1):
                    while try_add:
                        (tabla_procesos, proceso_eliminar) = buscar_tabla(tabla_procesos, 1,"mv", "mv")
                        if(proceso_eliminar != -1):# Hay procesos 'w' a eliminar de MV
                            mv = eliminar_memoria(mv, proceso_eliminar['pid'])
                            tabla_procesos.remove(proceso_eliminar)
                            (tabla_procesos, proceso_mover) = buscar_tabla(tabla_procesos, 2,"ram", "ram")
                            if proceso_mover != -1:# Hay procesos en la RAM para mover a MV
                                posicion_insercion = espacio_memoria(mv, proceso_mover['tam_proceso'])
                                if posicion_insercion != -1:# Si hay espacio en MV, mueve procesos de la RAM
                                    (tabla_procesos, proceso_mover) = buscar_tabla(tabla_procesos, 2,"ram", "mv")
                                    mv = agregar_memoria(mv, posicion_insercion, proceso_mover['pid'], proceso_mover['tam_proceso'])
                                    ram = eliminar_memoria(ram, proceso_mover['pid'])
                                    posicion_insercion = espacio_memoria(ram, proceso_creado['tam_proceso'])
                                    if posicion_insercion != -1:
                                        ram = agregar_memoria(ram, posicion_insercion, proceso_creado['pid'], proceso_creado['tam_proceso'])
                                        tabla_procesos.append(proceso_creado)
                                        print("Proceso nuevo, insertado en la memoria RAM")
                                        try_add = False
                            elif proceso_mover == -1: # No hay procesos en la RAM para mover a MV
                                print("No hay procesos a mover de RAM a MV")
                                print("1.Intentar insertar el nuevo proceso en MV con estado 'w' ")
                                print("2.No agregar proceso")
                                respuesta = int(input("Ingrese una opcion: "))
                                if (respuesta == 1):
                                    posicion_insercion = espacio_memoria(mv, proceso_creado['tam_proceso'])
                                    if posicion_insercion != -1:
                                        mv = agregar_memoria(mv, posicion_insercion, proceso_creado['pid'], proceso_creado['tam_proceso'])
                                        tabla_procesos.append(proceso_creado)
                                        print("Proceso nuevo, insertado en la memoria RAM")
                                        try_add = False
                                    elif posicion_insercion == -1:
                                        print("No se pudo agregar el proceso a MV")
                                        print("Finalice manualmente algun proceso")
                                        pid -= 1
                                        try_add = False
                        elif proceso_eliminar == -1:
                            print("No hay procesos w a eliminar")
                            print("Finalice manualmente algun proceso")
                            pid -= 1
                            try_add = False
                if respuesta == 2:# Opcion 2, no agregar proceso
                    pid -= 1
    #*---------------------------------------------------------------------------------------------------------------
    # Caso 3
    # No hay espacio en RAM pero si hay en MV
            elif(not mover and posicion_insercion != -1):
                print("\nCaso 3:\n")
                pid += 1
                proceso_creado = crear_proceso(pid, tam_proceso, 'mv')
                if proceso_creado['prioridad'] != 3:
                    mv = agregar_memoria(mv, posicion_insercion, pid, tam_proceso)
                    tabla_procesos.append(proceso_creado)
                else:
                    print("No se puede agregar a MV, proceso en ejecucion ")
                    print("1.Eliminar proceso")
                    print("2.Cambier estado y mover a MV")
                    respuesta = int(input("Ingrese una opcion: "))
                    if respuesta == 1:# Se elimina el proceso
                        pid -= 1
                        proceso = 0
                        print(f"Proceso eliminado")
                    elif respuesta == 2:# Cambia estado y se agrega a MV
                        proceso_creado['estado'] = 'r'
                        proceso_creado['prioridad'] = 2
                        mv = agregar_memoria(mv, posicion_insercion, pid, tam_proceso)
                        tabla_procesos.append(proceso_creado)
                        print(f"Proceso agregado:{proceso_creado['pid']} ")
    #*---------------------------------------------------------------------------------------------------------------
    # Caso 4
    # Sin espacio en RAM y en MV, elimina 'w', se intenta agregar proceso
            elif(not mover and posicion_insercion == -1):
                print("\nCaso 4:\n")
                pid += 1
                proceso_creado = crear_proceso(pid, tam_proceso, 'mv')
                print("Memoria RAM y MV sin espacio disponible")
                if proceso_creado['prioridad'] != 3:# Proceso 'w' o 'r'
                    print("")
                    print("1.Eliminar proceso en MV con estado: espera 'w'. E intentar ingresar el proceso.")
                    print("2.No agregar proceso y eliminar")
                    respuesta = int(input("Ingrese una opcion: "))
                    if (respuesta == 1):
                        try_add = True
                        while try_add:
                            (tabla_procesos, proceso_eliminar) = buscar_tabla(tabla_procesos, 1,"mv", "mv")
                            if(proceso_eliminar != -1):
                                mv = eliminar_memoria(mv, proceso_eliminar['pid'])
                                tabla_procesos.remove(proceso_eliminar)
                                posicion_insercion = espacio_memoria(mv, proceso_creado['tam_proceso'])
                                if posicion_insercion != -1:# Si hay espacio disponible en MV
                                    mv = agregar_memoria(mv, posicion_insercion, proceso_creado['pid'], proceso_creado['tam_proceso'])
                                    tabla_procesos.append(proceso_creado)
                                    try_add = False
                            elif proceso_eliminar == -1: # No se pudo agregar el proceso
                                print("No hay espacio continuo suficiente en la MV")
                                print(f"Proceso no agregado")
                                pid -= 1
                                try_add = False
                    if respuesta == 2:# No agregar proceso
                        pid -= 1
                        print("\nProceso no insertado")
                        print("Finalice manualmente algun proceso")
                        print("Regresando al menu\n")
                elif proceso_creado['prioridad'] == 3:#proceso en ejecucion
                    print("No se puede agregar a MV, proceso en ejecucion ")
                    print("1.Eliminar proceso")
                    print("2.Cambiar estado, mover a MV y eliminar un estado: espera 'w' ")
                    respuesta = int(input("Ingrese una opcion: "))
                    if respuesta == 1:
                        pid -= 1
                        proceso_creado = 0
                    elif respuesta == 2:
                        proceso_creado['estado'] = 'w'
                        proceso_creado['prioridad'] = 1
                        try_add = True
                        while try_add:
                            (tabla_procesos, proceso_eliminar) = buscar_tabla(tabla_procesos, 1,"mv", "mv")
                            if(proceso_eliminar != -1):# Hay procesos a eliminar de MV
                                mv = eliminar_memoria(mv, proceso_eliminar['pid'])
                                tabla_procesos.remove(proceso_eliminar)
                                posicion_insercion = espacio_memoria(mv, proceso_creado['tam_proceso'])
                                if posicion_insercion != -1:
                                    mv = agregar_memoria(mv, posicion_insercion, proceso_creado['pid'], proceso_creado['tam_proceso'])
                                    tabla_procesos.append(proceso_creado)
                                    print("Proceso agregado a MV")
                                    try_add = False
                            if(proceso_eliminar == -1):
                                print("No hay espacio continuo suficiente, nuevo proceso no agregado.")
                                try_add = False
#*---------------------------------------------------------------------------------------------------------------
    elif respuesta == 2:# Finalizar
        if len(tabla_procesos) != 0:
            print("")
            print("1.Cola")
            print("2.PID")
            respuesta = int(input("Ingrese una opcion: "))

            if respuesta == 1:
                pid_eliminar = buscar_primero(ram)
                ram = eliminar_memoria(ram, pid_eliminar)
                tabla_procesos = eliminar_tabla(tabla_procesos, pid_eliminar)
            elif (respuesta == 2):#PID
                    print("")
                    print("--------------------------------------------")
                    print("\tPID\tTamaño\tMemoria")
                    for proceso in tabla_procesos:
                        print(f"\t{proceso['pid']}\t{proceso['tam_proceso']}\t{proceso['memoria']}")
                    print("--------------------------------------------")
                    print("")
                    print("Ingresa el PID del proceso a finalizar")
                    respuesta = int(input("Ingrese una opcion: "))
                    pid_eliminar = respuesta
                    ram = eliminar_memoria(ram, pid_eliminar)
                    mv = eliminar_memoria(mv, pid_eliminar)
                    tabla_procesos = eliminar_tabla(tabla_procesos, pid_eliminar)
        else:
            print("")
            print("No hay procesos a finalizar")

#*---------------------------------------------------------------------------------------------------------------

    elif respuesta == 3:# Compactacion
        if len(tabla_procesos)  != 0:
            print("")
            print("1.Compactar RAM")
            print("2.Compactar MV")
            respuesta = int(input("Ingrese una opcion: "))

            if respuesta == 1:
                ram_auxiliar = [0] * tam_memoria
                print("\nRAM:")
                print(ram)
                ram =  compactar(ram, ram_auxiliar, tabla_procesos)
                print("\nRAM compactada:")
                print(ram)
                print("")
            if respuesta == 2:
                mv_auxiliar = [0] * tam_memoria
                print("\nMV:")
                print(mv)
                mv =  compactar(mv, mv_auxiliar, tabla_procesos)
                print("\nMV compactada:")
                print(mv)
                print("")

        else:
            print("No hay procesos")

#*---------------------------------------------------------------------------------------------------------------
    elif respuesta == 4:# Representancion
        print("")
        print("1.Mapa de bits")
        print("2.Lista de huecos")
        print("3.RAM y MV")
        print("4.Mostrar prioridad de procesos")
        respuesta = int(input("Ingrese una opcion: "))

        if respuesta == 1:
            print("")
            print("RAM:\n",ram)
            print("Mapa de bits: ")
            mapa_bits = llenar_mapa(ram, mapa_bits)
            print_mapa(mapa_bits)
        elif respuesta == 2:
            print("")
            print("1.Procesos y huecos")
            print("2.Nombre de procesos y huecos")
            respuesta = int(input("Ingrese una opcion: "))

            if respuesta == 1:
                print("")
                lista_huecos = lista(ram)
                print_lista(lista_huecos)
            elif respuesta == 2:
                print("")
                lista_nombres = lista_nombre(ram)
                print_lista_color(lista_nombres, tabla_procesos)
        
        elif respuesta == 3:
            print("")
            print("RAM:\n",ram)
            print("MV:\n", mv)
        
        elif respuesta == 4:
            if len(tabla_procesos) != 0:
                print("")
                print("RAM:\n",ram)
                print("MV:\n", mv)
                print("--------------------------------------------")
                print_procesos(tabla_procesos)
                print("--------------------------------------------")
            else:
                print("No hay procesos que mostrar")


        print("")
    
#*---------------------------------------------------------------------------------------------------------------
    elif( respuesta == 5):# Salir
        run = False