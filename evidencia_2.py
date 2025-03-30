import random
from datetime import datetime
import csv
import openpyxl
import statistics





notas={}

def cargar_notas():
    notas_cargadas={}

    try:
        with open("Evidencia1.csv", "r", encoding="latin1") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                folio = int(fila["Folio"])
                notas_cargadas[folio] = {
                    "Fecha":fila["Fecha"],
                    "Nombre":fila["Nombre"],
                    "Servicios":fila["Servicios"],
                    "Monto a pagar":float(fila["Monto a pagar"]),
                    "Estado":fila["Estado"]
                }

    except Exception as e:
        print("\nSe iniciara el trabajo sin datos anteriores.")

    return notas_cargadas
        

def opcion1():

    print("\nMenu principal > Registrar una nota\n")

    folio = random.randint(100000,900000)

    while True:

        fecha_str = input("Ingrese la fecha (dd/mm/yyyy):")
        try:
            fecha_usuario = validar_fechas(fecha_str)
            fecha_actual = datetime.now().date()

            if fecha_usuario > fecha_actual:
                print("Error: Fecha posterior a la fecha actual.")
            else:
                break
        except:
            print("formato de fecha incorrecto.")

    

    while True:
        nombre = input("Ingrese su nombre: ").title()
        if len(nombre) < 3:
            print("\nERROR! Nombre invalido.\n")
        else:
            break
            
    servicios = []

    control = 1

    while control == 1:
        servicio = input("Ingrese el nombre del servicio: ")
        servicios.append(servicio)

        print("""Desea agregar otro servicio?
1. SI
2. NO""")
                
        control = int(input("Seleccion: "))

        if control != 1:
            break            
    
    while True:

        try:
            costo = float(input("Ingrese el monto a pagar: "))
            if costo > 0:
                break
            else: 
                print("Error el monto debe ser mayor a 0.")

        except:
            print("Error entrada invalidad. Ingrese un numero valido.")

    Estado = "Activa"

    notas[folio] = {
        "Fecha":fecha_usuario.strftime("%d/%m/%Y"),
        "Nombre":nombre,
        "Servicios":servicios,
        "Monto a pagar":costo,
        "Estado":Estado

    }

    archivo_existente=False
    try:
        with open("Evidencia1.csv", "r", encoding='latin1'):
            archivo_existente=True
    except Exception as e:
        pass


    with open("Evidencia1.csv", "a", encoding='latin1', newline="") as archivo:
        grabador = csv.DictWriter(archivo, fieldnames=["Folio", "Fecha", "Nombre", "Servicios", "Monto a pagar", "Estado"])

        if not archivo_existente:
            grabador.writeheader()

        grabador.writerow({
            "Folio":folio,
            "Fecha":notas[folio]["Fecha"],
            "Nombre":notas[folio]["Nombre"],
            "Servicios":notas[folio]["Servicios"],
            "Monto a pagar":notas[folio]["Monto a pagar"],
            "Estado":notas[folio]["Estado"]

        })
    print(f"\nNota con folio {folio} registrada correctamente.\n")


def validar_fechas(fecha_str):
    try:
        return datetime.strptime(fecha_str, "%d/%m/%Y").date()
    except: 
        print("Error: formato de fecha no valido.")
   

def consulta_x_periodo():

    global notas

    print("\nMenu principal > Consultas y Reportes > Consulta por periodo\n")
    while True:
        try:    
            fecha_str1=input("Ingrese la fecha de inicio del periodo: ")
            fecha_str2=input("Ingrese la fecha de fin del periodo: ")

            fecha_inicio = validar_fechas(fecha_str1) #si no es valida dara false
            fecha_fin= validar_fechas(fecha_str2)
            
            if not fecha_inicio or not fecha_fin:
                print("Formato de fecha erroneo. Usar el formato: (dd/mm/yyyy)")
                continue
            
            notas_encontradas = []

            for folio, datos in notas.items():
                
                fecha = datetime.strptime(datos.get("Fecha"), "%d/%m/%Y").date()

                if fecha_inicio <= fecha <= fecha_fin:
                    notas_encontradas.append((folio,datos["Fecha"]))

            if notas_encontradas:
                exportar = int(input("Desea exportar los datos a excel?  si(1) no(2)"))
                if exportar == 1:
                    exportar_excel(notas_encontradas)
                    break
            else:
                print("No hay notas en dicho periodo.")
                break

        except Exception as e:
            print(e)

def exportar_excel(notas_encontradas):
    
    libro = openpyxl.Workbook()
    hoja = libro.active
    hoja.title = "Reporte"

    hoja["A1"] = "Folio"
    hoja["B1"] = "Fecha"

    for index,row in enumerate(notas_encontradas, start=2):
        hoja[f"A{index}"] = row[0]
        hoja[f"B{index}"] = row[1]

    libro.save("Reportes.xlsx")


def consulta_x_folio():
    global notas
    
    print("\nMenu principal > Consultas y Reportes > Consulta por folio\n")

    while True:

        # muestra previa de las notas en el sistema.
        for folio, datos in notas.items():
            if datos["Estado"]=="Activa":
                print(f"{folio}---{datos["Fecha"]}")

        # buscando la nota segun su folio y su estado
        buscar_folio = int(input("\nIngrese el folio:"))
        if buscar_folio in notas and notas[buscar_folio]["Estado"] == "Activa":
            
            for folio, datos in notas[buscar_folio].items():
                print(f"{folio}:{datos}")
        else:
            print(f"La nota con folio:{buscar_folio}. NO se encuentra en el sistema.")

        break


def consultas_y_reportes():


    print("\nMenu principal > Consultas y Reportes")

    while True:

        print("""
1. Consulta por periodo.
2. Consulta por folio.
3. Regresar al menu principal""")
        opcion = int(input("\nSeleccione un opcion: "))
        if opcion == 1:
            consulta_x_periodo()
        elif opcion == 2:
            consulta_x_folio()
        elif opcion == 3:
            break

def cancelar_una_nota():
    
    global notas

    print("\nMenu Principal > Cancelar una nota\n")
    while True:
        
        buscar_folio = int(input("Ingrese el folio de la nota a cancelar: "))
        
        if buscar_folio in notas and notas[buscar_folio]["Estado"] == "Activa":
            print("\nDatos de la nota:\n")

            for folio,datos in notas[buscar_folio].items(): #esto puede  SER una funcion
                print(f"{folio}:{datos}")
            
            cancelar = int(input(f"\nDesea cancelar la nota con folio: {buscar_folio} si(1) no(2)."))
            if cancelar == 1:
                #funcion actulizar estado
                actualizar_estado(buscar_folio, "Cancelada")
                print("\nNota cancelada con exito.")
                break
            elif cancelar == 0:
                print(f"\nLa nota con folio: {buscar_folio} NO fue cancelada.")
                break
            else:
                print(f"Error: {cancelar} no es una opcion valida.")
                break
        elif buscar_folio not in notas:
            print(f"\nNo existe la nota con el folio: {buscar_folio}")
            break
        
def actualizar_estado(Folio, Estado):
    global notas


    notas[Folio]["Estado"] = Estado

    with open ("Evidencia1.csv", "w", encoding="latin1", newline="") as archivo:

        grabador = csv.DictWriter(archivo, fieldnames=["Folio", "Fecha", "Nombre", "Servicios", "Monto a pagar", "Estado"])
        grabador.writeheader()


        for folio, datos in notas.items():
            grabador.writerow({
                "Folio":folio,
                "Fecha":datos["Fecha"],
                "Nombre":datos["Nombre"],
                "Servicios":datos["Servicios"],
                "Monto a pagar":datos["Monto a pagar"],
                "Estado":datos["Estado"]

        })


def recuperar_nota():
    global notas
    existen_notas = False
    print("\nMenu principal > Recuperar una nota\n")

    for folio,datos in notas.items(): # SABER SI HAY NOTAS CON EL ESTADO CANCELADO
        if datos["Estado"]=="Cancelada":
            existen_notas = True

    if existen_notas == True:
        print("Notas en el sistema:\n")

        for folio,datos in notas.items(): # MOSTRAR LOS FOLIOS DE LAS NOTAS
            if datos["Estado"]=="Cancelada":
                print(f"Folio: {folio}")
        recuperar_folio = int(input("\nIngrese el folio de la nota a recuperar: "))
        print("")
        
        if recuperar_folio in notas and notas[recuperar_folio]["Estado"] == "Cancelada":

            for folio, datos in notas[recuperar_folio].items():
                print(f"{folio}:{datos}")

            recuperar = int(input(f"\nDesea recuperar la nota con folio: {recuperar_folio} si(1) no(2)."))

            if recuperar == 1:
                actualizar_estado(recuperar_folio, "Activa")
                print("Nota recuperada con exito.")
            elif recuperar == 2:
                print(f"\nLa nota con folio: {recuperar_folio} NO fue recuperada.")
            else:
                print(f"Error: {recuperar} no es una opcion valida.")
        
        elif recuperar_folio not in notas:
                print(f"\nNo existe la nota con el folio: {recuperar_folio}")
    else:
        print("No hay notas por recuperar en este momento.")
            
def guardar_notas():
    with open("Evidencia1.csv", "w", encoding="latin1", newline="") as archivo:
        grabador = csv.DictWriter(archivo, fieldnames=["Folio", "Fecha", "Nombre", "Servicios", "Monto a pagar", "Estado"])
        grabador.writeheader()

        for folio, datos in notas.items():
            grabador.writerow({
                "Folio": folio,
                "Fecha": datos["Fecha"],
                "Nombre": datos["Nombre"],
                "Servicios": datos["Servicios"],
                "Monto a pagar": datos["Monto a pagar"],
                "Estado": datos["Estado"]
            })


#primero ocupamos la funcion que nos ayude a extraer la fechas mas antiguas y recientes.

def fechas ():

    fechas = [datetime.strptime(notas[folio]["Fecha"], "%d/%m/%Y").date() for folio in notas]
    return fechas

def tendencias_centrales():
    print("\nMenu principal > Analisis Estadistico de los totales por nota > Tendencias Centrales.\n")
    while True:
        
        omitir_1 = input("Omitir la fecha inicial? (y/n): ").lower()
        if omitir_1 == "y":
            lista_fechas = fechas()
            fecha_inicio_1 = min(lista_fechas)
            break
        else:
            fecha_str_1=input("Ingrese la fecha de inicio del periodo: ")
            fecha_inicio_1 = validar_fechas(fecha_str_1)
            if fecha_inicio_1:
                break

    while True:
        
        omitir_2 = input("Omitir la fecha fin? (y/n): ").lower()
        if omitir_2 == "y":
            lista_fechas = fechas()
            fecha_fin_1 = max(lista_fechas)
            break
        else:
            fecha_str_2=input("Ingrese la fecha de fin del periodo: ")
            fecha_fin_1 = validar_fechas(fecha_str_2)
            if fecha_fin_1:
                break

    montos = []
    for folio, datos in notas.items():
        fecha_nota = datetime.strptime(datos["Fecha"], "%d/%m/%Y").date()

        if fecha_inicio_1 <= fecha_nota <= fecha_fin_1:
            montos.append(datos["Monto a pagar"])

    if len(montos) > 0:

        media = sum(montos)/len(montos)
        print(f"\nLa media es: {media}")
        print(f"La Meadiana es: {statistics.median(montos)}")
        print(f"La Moda es: {statistics.mode(montos)}")
    else:
        print("No hay notas emitidas en dicho periodo.")

def dispersion_distribucion():

    print("\nMenu principal > Analisis Estadistico de los totales por nota > Dispersion y distribucion.\n")
    
    while True:
        
        omitir_1 = input("Omitir la fecha inicial? (y/n): ").lower()
        if omitir_1 == "y":
            lista_fechas = fechas()
            fecha_inicio_1 = min(lista_fechas)
            break
        elif omitir_1 == "n":
            fecha_str_1=input("Ingrese la fecha de inicio del periodo: ")
            fecha_inicio_1 = validar_fechas(fecha_str_1)
            if fecha_inicio_1:
                break 
        else:
            pass
    
    while True:
        
        omitir_2 = input("Omitir la fecha fin? (y/n): ").lower()
        if omitir_2 == "y":
            lista_fechas = fechas()
            fecha_fin_1 = max(lista_fechas)
            break
        elif omitir_2 == "n":
            fecha_str_2=input("Ingrese la fecha de fin del periodo: ")
            fecha_fin_1 = validar_fechas(fecha_str_2)
            if fecha_fin_1:
                break
        else:
            pass

    montos = []
    for folio, datos in notas.items():
        fecha_nota = datetime.strptime(datos["Fecha"], "%d/%m/%Y").date()

        if fecha_inicio_1 <= fecha_nota <= fecha_fin_1:
            montos.append(datos["Monto a pagar"])

    if len(montos) > 0:
        varianza = statistics.variance(montos)
        desviacion = statistics.stdev(montos)
        q1 = statistics.quantiles(montos, n=4)[0]
        mediana = statistics.median(montos)
        q3 = statistics.quantiles(montos, n=4)[-1]
        rango_intercuartilico = q3 - q1
        
        print(f"\nVarianza: {varianza:.2f}")
        print(f"Desviación estándar: {desviacion:.2f}")
        print(f"Primer cuartil (Q1): {q1:.2f}")
        print(f"Mediana (Q2): {mediana:.2f}")
        print(f"Tercer cuartil (Q3): {q3:.2f}")
        print(f"Rango intercuartílico: {rango_intercuartilico:.2f}")
    else:
        print("No hay notas emitidas en dicho periodo.")

        




def analisis_estadistico():
    print("\nMenu principal > Analisis Estadistico de los totales por nota.")

    while True:

        try:

            print("""
1. Tendencias Centrales.
2. Dispersion y distribucion.
3. Regresar al menu principal""")
            opcion = int(input("\nSeleccione un opcion: "))
            if opcion == 1:
                tendencias_centrales()
            elif opcion == 2:
                dispersion_distribucion()
            elif opcion == 3:
                break
        except:
            pass


while True:

    try:

        notas = cargar_notas()
        
        print("""\nMenu Principal
1. Registrar una nota
2. Consultas y Reportes
3. Cancelar una nota
4. Recuperar una nota
5. Analisis Estadistico de los totales por nota.
6. Salir del sistema""")
        
        opcion = int(input("Seleccione una opcion: "))

        if opcion == 1:
            opcion1()

        elif opcion == 2:
            consultas_y_reportes()

        elif opcion == 3:
            cancelar_una_nota()
            
        elif opcion == 4:
            recuperar_nota()
        
        elif opcion == 5:
            analisis_estadistico()

        elif opcion == 6:
            guardar_notas()
            print("Saliendo de la aplicacion")
            break 
        else:
            print("ERROR! LA OPCION NO EXISTE")
    
    except:
        print("ERROR!. Seleccione una opcion del menu")
        

    




