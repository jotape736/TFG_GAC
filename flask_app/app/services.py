"""Este modulo genera todos los horarios posibles con las asignaturas seleccionadas"""

import itertools
from collections import Counter
import random

from app.models import (
    get_cuatrimestre,
    get_fecha_grupo,
    get_fecha_subgrupo,
    get_datos_grupo,
    get_datos_subgrupo,
)

# from models import (
#     get_cuatrimestre,
#     get_fecha_grupo,
#     get_fecha_subgrupo,
#     get_datos_grupo,
#     get_datos_subgrupo,
# )


def separar_asignaturas(asignaturas):
    """Este metodo separa las asignaturas por cuatrimestre"""
    cuatrimestre_1 = {}
    cuatrimestre_2 = {}
    for key in asignaturas.keys():
        cuatrimestre = get_cuatrimestre(key)
        if cuatrimestre == 1:
            cuatrimestre_1[key] = asignaturas[key]
        else:
            cuatrimestre_2[key] = asignaturas[key]
    return cuatrimestre_1, cuatrimestre_2


def generar_horarios(asignaturas):
    """Este metodo genera todos los horarios posibles con las asignaturas seleccionadas"""
    # print("\n--------------------ASIGNATURAS------------------------\n")
    # for key, value in asignaturas.items():
    #     print(key, value)
    # Se combinan todos los subgrupos seleccionados
    productos = list(itertools.product(*asignaturas.values()))
    # print("\n--------------------PRODUCTOS------------------------\n")
    # for item in productos:
    #     print(item)

    # Se crea un diccionario con las combinaciones de subgrupos
    # concatenadas con el codigo de la asignatura
    dict_combinaciones = {}
    llaves_asignaturas = list(asignaturas.keys())
    for idx, producto in enumerate(productos):
        combinacion = [
            llaves_asignaturas[i] + producto[i] for i in range(len(producto))
        ]
        dict_combinaciones[idx] = combinacion
    # print("--------------------COMBINACIONES------------------------\n")
    # for indice, item in enumerate(dict_combinaciones.values()):
    #     print(indice, item)

    # Se obtienen las horas de clase de cada combinacion
    dict_horarios = {}
    for idx, item in enumerate(dict_combinaciones.values()):
        # print("\n--------------------COMBINACION------------------------\n")
        # print(idx, item)
        lista_horas = []
        # Se toman los códigos de cada combinación
        for value in item:
            letra = value[-2]
            numero = value[-1]
            asignatura_codigo = value[:-2]
            # Se obtienen las horas de clase de teoria y prácticas
            # horas_grupo = get_fecha_grupo(asignatura_codigo, letra)
            # print("horas grupo:", horas_grupo)
            lista_teoria = [
                int(hora)
                for hora in get_fecha_grupo(asignatura_codigo, letra)[0].split(", ")
            ]
            lista_horas.extend(lista_teoria)
            # for hora in horas_grupo:
            #     lista_horas.extend(map(int, hora[0].split(",")))
            # print("lista horas:", lista_horas)
            lista_practicas = [
                int(hora)
                for hora in get_fecha_subgrupo(asignatura_codigo, letra, numero)[
                    0
                ].split(", ")
            ]
            # print("lista practicas:", lista_practicas)
            lista_horas.extend(lista_practicas)
            # horas_subgrupo = get_fecha_subgrupo(asignatura_codigo, letra, numero)
            # for hora in horas_subgrupo:
            #     lista_horas.extend(map(int, hora[0].split(",")))
        lista_horas = sorted(lista_horas)
        dict_horarios[idx] = lista_horas
    # print("\n--------------------HORARIOS------------------------\n")
    # for key, value in dict_horarios.items():
    #     print(key, value)
    # print("\n--------------------CLASIFICACION------------------------\n")
    lista_horarios = []
    for horario, horas in dict_horarios.items():
        # Se cuentan las horas repetidas
        counter = Counter(horas)
        elementos_repetidos = {
            element: count for element, count in counter.items() if count > 1
        }
        solapamientos = len(elementos_repetidos)
        # Se cuentan los dias asistidos
        dias = len(list(set(int(hora / 100) for hora in horas)))
        # Se cuentan las horas libres
        grouped = {}
        horas_sr = set(horas)  # horas sin repetir
        for hora in horas_sr:  # Se agrupan por centenas
            key = hora // 100
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(hora)
        # Se restan los valores de cada grupo para obtener las horas libres
        HORAS_LIBRES = 0
        for key, value in grouped.items():
            differences = [j - i for i, j in zip(value[:-1], value[1:]) if j - i > 1]
            HORAS_LIBRES += sum(differences)
        lista_horarios.append((horario, solapamientos, dias, HORAS_LIBRES))
        # print(f"{horario}: S: {solapamientos}, D: {dias}, H: {HORAS_LIBRES}")

    # print("\n")
    # Se ordenan los horarios por menor número de solapamientos, horas libres y días asistidos
    solapamientos = 1
    horas_libres = 3
    dias = 2
    lista_horarios.sort(key=lambda x: (x[solapamientos], x[horas_libres], x[dias]))
    resultado = []
    # print("\n")
    # Se toman los 10 mejores combinaciones
    for item in lista_horarios[:10]:
        resultado.append(dict_combinaciones[item[0]])
        # print(f"Key: {item[0]}, Value: {dict_combinaciones[item[0]]}")
    return resultado


dict_horas = {
    1: "08:30",
    2: "09:30",
    3: "10:30",
    4: "11:30",
    5: "12:30",
    6: "13:30",
    7: "14:30",
    8: "15:30",
    9: "16:30",
    10: "17:30",
    11: "18:30",
    12: "19:30",
    13: "20:30",
    14: "21:30",
}

base = "2022-08-0"
base_final = ":00"


def traducir_horas(horas):
    """Este metodo traduce los enteros de una lista como horas lectivas"""
    horas.sort()
    grouped = {}
    resultado = []
    for hora in horas:
        key = hora // 100
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(hora)  # Se agrupan por centenas

    for key, value in grouped.items():
        fecha = base + str(key) + "T"
        start_time = end_time = fecha
        if len(value) == 1:
            try:
                start_time = start_time + dict_horas[value[0] % 100] + base_final
            except KeyError:
                print(f"Error en la hora inicio {value[0]}")
            try:
                end_time = end_time + dict_horas[(value[0] % 100) + 1] + base_final
            except KeyError:
                print(f"Error en la hora final {value[0]}")
            resultado.append([start_time, end_time])
        else:
            try:
                start_time = start_time + dict_horas[value[0] % 100] + base_final
            except KeyError:
                print(f"Error en la hora inicio {value[0]}")
            try:
                end_time = end_time + dict_horas[(value[-1] % 100) + 1] + base_final
            except KeyError:
                print(f"Error en la hora final {value[0]}")
            resultado.append([start_time, end_time])
    return resultado


def traducir_horarios(horarios):
    """Este metodo traduce los horarios para el calendario"""
    repetidos = []
    asignaturas = []
    dict_colores = {}
    resultado = []
    colores = [
        "#FF7F50",  # coral
        "#4BC0C0",  # turquesa
        "#9966FF",  # violeta
        "#FFD54F",  # naranja
        "#A1887F",  # cafe
        "#80CBC4",  # verde
        # lima
        "#C5E1A5",
    ]

    # Se obtiene el color de cada grupo
    # Se toma el primera horario y se asigna un color a cada asignatura
    for elemento in horarios[0]:
        codigo = elemento[:-2]
        if codigo not in asignaturas:
            color = random.choice(colores) if len(colores) != 0 else "#FFFFFF"
            dict_colores[codigo] = color
            colores.remove(color)
            asignaturas.append(codigo)

    # Se evalua cada horario [[2961111A1, 296111AB1], [2961111A2, 296111AB2], ...]
    for indice, horario in enumerate(horarios):
        horas_practicas = []
        horas_teoria = []
        grupos_teoria = []
        lista_clases = []
        # Se obtienen los grupos de teoria
        # [2961111A1, 296111AB1] ---> [2961111A, 296111AB]
        # y las horas repetidas (solapamientos)
        horas = []
        for grupo in horario:
            letra = str(grupo[-2])
            codigo = str(grupo[:-2])
            numero = str(grupo[-1])
            elemento = codigo + letra
            if elemento not in grupos_teoria:
                grupos_teoria.append(elemento)
            lista_horas_teoria = [
                int(hora) for hora in get_fecha_grupo(codigo, letra)[0].split(", ")
            ]
            lista_horas_practicas = [
                int(hora)
                for hora in get_fecha_subgrupo(codigo, letra, numero)[0].split(", ")
            ]
            horas.extend(lista_horas_teoria)
            horas.extend(lista_horas_practicas)

        # print("horas teoria y practicas:", horas)
        contador = Counter(horas)
        repetidos = [item for item, count in contador.items() if count > 1]
        # print("repetidos:", repetidos)

        # Por cada grupo de teoria se obtienen sus horas de clase
        # [2961111A] ---> [404, 105, 505]
        # Si hay alguna hora que esté dentro de los solapamientos, se marca todo el conjunto en rojo
        for indice, item in enumerate(grupos_teoria):
            codigo = item[:-1]
            letra = item[-1]
            horas_teoria = [
                int(hora) for hora in get_fecha_grupo(codigo, letra)[0].split(", ")
            ]
            color = dict_colores[codigo]
            border_color = color
            # Se buscan las horas repetidas en los grupos de teoria
            for item in horas_teoria:
                if item in repetidos:
                    # print("repetido en teoría:", item)
                    border_color = "red"

            # Se traducen las horas de clase a formato YYYY-MM-DDTHH:MM:SS
            traducidas = traducir_horas(horas_teoria)

            for item in traducidas:

                texto = get_datos_grupo(codigo, letra)
                clase_teoria = {
                    "text": texto[0] + " (" + texto[1] + ")" + "\n(" + texto[2] + ")",
                    "start": item[0],
                    "end": item[1],
                    "color": color,
                    "borderColor": border_color,
                }
                lista_clases.append(clase_teoria)
        # Para cada grupo de prácticas se obtienen sus horas de clase
        # [296111AB1] ---> [404, 405]
        # Si hay alguna hora que esté dentro de los solapamientos, se marca todo el conjunto en rojo
        for item in horario:
            codigo = item[:-2]
            letra = item[-2]
            numero = item[-1]

            horas_practicas = [
                int(hora)
                for hora in get_fecha_subgrupo(codigo, letra, numero)[0].split(", ")
            ]
            # print("horas practicas:", horas_practicas)
            color = dict_colores[codigo] + "A0"
            border_color = color
            for item in horas_practicas:
                # print("item:", item)
                if item in repetidos:
                    # print("repetido en practicas:", item)
                    border_color = "red"

            for indice, item in enumerate(traducir_horas(horas_practicas)):
                texto = get_datos_subgrupo(codigo, letra, numero)
                clase_practica = {
                    "text": texto[0]
                    + " ("
                    + texto[1]
                    + texto[2]
                    + ")"
                    + "\n("
                    + texto[3]
                    + ")",
                    "start": item[0],
                    "end": item[1],
                    "color": color,
                    "borderColor": border_color,
                }

                lista_clases.append(clase_practica)
        resultado.append(lista_clases)
        # print("----------------")
    # for item in resultado:
    #     for clase in item:
    #         print(clase)
    #     print("\n")
    return resultado


# horarios = [["2961111A1", "296111AB1"]]

# traducir_horarios(horarios)

# asignaturas = {
#     "2961111": ["A1"],
#     "2961112": ["B1"],
# }

# traducir_horarios(generar_horarios(asignaturas))
