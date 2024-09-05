"""
Este modulo se encarga de descargar los horarios de las asignaturas
de la web de la UGR y guardarlos en un archivo CSV.
"""

import re
import csv
import sqlite3
import requests
from unidecode import unidecode
import pandas as pd
import pdfplumber


def correspondencia_subgrupos():
    """Esta función se encarga de extraer los subgrupos de las asignaturas de un archivo PDF."""

    archivo_pdf = "./pdf/Correspondencia subgrupos.pdf"
    with pdfplumber.open(archivo_pdf) as pdf:
        first_page = pdf.pages[0]
        tables = first_page.extract_tables()

    for i, tabla in enumerate(tables):
        df = pd.DataFrame(tabla)
        df.to_csv(f"./parsed/tabla_{i+1}.csv", index=False)

    lista_grupos = ["A", "B", "C", "D", "E", "F"]
    lista_asignaturas = [
        "ÁlgebraLinealyEstructurasMatemáticas",
        "Cálculo",
        "FundamentosFísicosyTecnológicos",
        "FundamentosdelSoftware",
        "FundamentosdeProgramación",
        "LógicayMétodosDiscretos",
        "Estadística",
        "TecnologíayOrganizacióndeComputadores",
        "MetodologíadelaProgramación",
        "Ingeniería,EmpresaySociedad",
        "EstructuradeComputadores",
        "SistemasOperativos",
        "ProgramaciónyDiseñoOrientadoaObjetos",
        "SistemasConcurrentesydistribuidos",
        "EstructuradeDatos",
        "ArquitecturadeComputadores",
        "Algorítmica",
        "InteligenciaArtificial",
        "FundamentosdeBasesdeDatos",
        "FundamentosdeIngenieríadelSoftware",
        "IngenieríadeServidores",
        "FundamentosdeRedes",
        "ModelosdeComputación",
        "InformáticaGráfica",
        "DiseñoyDesarrollodeSistemasdeInformación",
    ]
    dict_correspondencia_subgrupos = {}

    df1 = pd.read_csv("./parsed/tabla_1.csv")
    df2 = pd.read_csv("./parsed/tabla_2.csv")
    df3 = pd.read_csv("./parsed/tabla_3.csv")

    df = pd.concat([df1, df2, df3])

    df.to_csv("./parsed/correspondencia_subgrupos.csv", index=False)

    filename = "./parsed/correspondencia_subgrupos.csv"

    df = pd.read_csv(filename)
    df["2"] = df["2"].replace("EstructurasdeDatos", "EstructuradeDatos")

    steps = start = 4
    grupos = 6
    cont_indice_grupo = 0
    cont_indice_subgrupos = 1

    for asignatura in lista_asignaturas:
        selected_row = df[df[df.columns[2]] == asignatura]
        key_one = selected_row.iloc[0, 2].upper()  # type: ignore # Nombre de la asignatura
        for i in range(start, len(selected_row.columns), steps):
            # Select the next 4 columns, convert them to a list, and filter out NaN values
            columns = [
                int(float(x))
                for x in selected_row.iloc[:, i : i + 4].values.tolist()[0]
                if pd.notna(x)
            ]
            for sub_grupo in columns:
                key_two = str(sub_grupo)  # Numero del subgrupo Ej: "1"
                dict_correspondencia_subgrupos[(key_one, key_two)] = str(
                    lista_grupos[cont_indice_grupo % grupos]
                    + str(cont_indice_subgrupos)
                )  # Ej: "A1"
                cont_indice_subgrupos += 1
            cont_indice_grupo += 1
            cont_indice_subgrupos = 1
    return dict_correspondencia_subgrupos


def obtener_json_asignaturas(param1, param2, param3, param4, param5, cookies):
    """Esta función se encarga de obtener los json de los grupos y subgrupos de una asignatura"""
    base_url = "https://oficinavirtual.ugr.es/ordenacion/GestorInicial"
    action = "?accion=consultaHorarioGrupoAsignatura&param1="
    full_url = base_url + action
    res = requests.get(
        full_url
        + param1
        + "&param2="
        + param2
        + "&param3="
        + param3
        + "&param4="
        + param4
        + "&param5="
        + param5
        + "&start=2024-04-08T00:00:00+02:00&end=2024-04-13T00:00:00+02:00",
        cookies,
        timeout=10,
    )
    return res.json()


def obtener_siglas(palabras):
    """Esta función se encarga de obtener las siglas de las asignaturas"""
    excluidas = ["Y", "DE", "LA", "EN", "DEL", "A", "E", "PARA", "ESP", "LOS"]
    if len(palabras) == 1:  # If nombre_asignatura is a single word
        siglas = palabras[0][:2]  # Use the first two letters
    else:  # If nombre_asignatura is multiple words
        siglas = [palabra[0] for palabra in palabras if palabra not in excluidas]
    return unidecode("".join(siglas))


def obtener_asignaturas(dict_correspondencia_subgrupos):
    """Esta función se encarga de obtener las asignaturas de la web de la UGR"""

    dict_horas = {
        "08:30": 1,
        "09:30": 2,
        "10:30": 3,
        "11:30": 4,
        "12:30": 5,
        "13:30": 6,
        "14:30": 7,
        "15:30": 8,
        "16:30": 9,
        "17:30": 10,
        "18:30": 11,
        "19:30": 12,
        "20:30": 13,
    }
    column_names = [
        "CODIGO",
        "ASIGNATURA",
        "GRUPO",
        "PROFESOR",
        "CUATRIMESTRE",
        "HORA1",
        "HORA2",
        "HORA3",
        "HORA4",
        "HORA5",
    ]

    # Open the CSV file in write mode with explicit encoding
    with open("result.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Write the column names
        writer.writerow(column_names)

    cookies = {"JSESSIONID": "7CC5C08E397D910FA2936508D72B0896"}

    base_url = "https://oficinavirtual.ugr.es/ordenacion/GestorInicial"
    action = "?accion=cargaCentros&id=NT0501502296"
    full_url = base_url + action
    res = requests.get(
        full_url,
        timeout=10,
    )
    # Todas las asignaturas
    listado_asignaturas = res.json()

    conn = sqlite3.connect("universidad.db")
    cursor = conn.cursor()

    for item in listado_asignaturas:  # Recorro todas las asignaturas
        print(item["text"])
        curso = item["text"][-1]  # Curso de la asignatura
        nombre_asignatura = item["text"][:-9]  # Quito el "Curso:*" del nombre
        especialidad = re.search(r"\((.*?)\)", nombre_asignatura)
        if especialidad is not None:
            especialidad = re.sub(r"[().]", " ", especialidad.group())
            especialidad = obtener_siglas(especialidad.split())
        else:
            especialidad = "TRONCAL"

        nombre_asignatura = re.sub(
            r"\([^)]*\)", "", nombre_asignatura
        )  # Quito los parentesis
        nombre_asignatura = re.sub(r"\.", " ", nombre_asignatura)  # Quito los puntos
        siglas = obtener_siglas(nombre_asignatura.split())

        # curso = item['text'][-1] #Curso de la asignatura
        node_id = item["id"]
        # subprocess.run(['mkdir', '-p', 'download/' + nombre_asignatura])

        base_url = "https://oficinavirtual.ugr.es/ordenacion/GestorInicial"
        action = "?accion=consultaAsignatura&nodeId="
        full_url = base_url + action + node_id
        res = requests.get(
            full_url,
            cookies=cookies,
            timeout=10,
        )  # Todos los grupos de una asignatura
        datos_asignatura = res.json()
        print("     " + especialidad + " ->" + siglas)

        # Guardo el JSON en el directorio
        # with open('download/' + nombre_asignatura + '/' + nombre_asignatura + '.json', 'w') as f:
        #     json.dump(datos_asignatura, f, indent=4)
        seccion_codigo = datos_asignatura["asignatura"][-11:]
        match = re.search(r"\((.*?)\.(.*?)\.(.*?)\)", seccion_codigo)
        codigo = match.group(1) + match.group(2) + match.group(3)  # type: ignore
        if match:
            param1 = match.group(1)
            param2 = match.group(2)
            param3 = match.group(3)

        with open("result.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            for grupo_teoria in datos_asignatura[
                "docentesGruposT"
            ]:  # Horarios grupos teoría
                grupo = grupo_teoria["grupo"]  # Pj: A, B, C
                profesor_teoria = re.sub(
                    r"\([^)]*\)", "", grupo_teoria["nombre"]
                )  # Quito los parentesis
                horarios = obtener_json_asignaturas(
                    param1, param2, param3, grupo, "1", cookies
                )
                try:
                    cuatrimestre = horarios[0]["title"]
                except IndexError:
                    cuatrimestre = None
                    aula = None
                if cuatrimestre is not None:
                    aula = horarios[0]["title"][-2:]
                    if cuatrimestre.startswith("Primer cuatrimestre"):
                        cuatrimestre = "1"
                    else:
                        cuatrimestre = "2"
                horas = []
                for item in horarios:
                    dia = int(re.sub(r"[\[\]]", "", item["daysOfWeek"])) * 100
                    inicio = int(dict_horas.get(item["startTime"], -1))
                    fin = int(dict_horas.get(item["endTime"], -1))
                    consecutivas = fin - inicio
                    print(siglas)
                    if consecutivas > 1:
                        for hora in range(consecutivas):
                            horas.append(int(dia + inicio + hora))
                    else:
                        horas.append(int(dia + dict_horas[item["startTime"]]))
                # ---------------------------------
                cursor.execute(
                    "INSERT OR IGNORE INTO Asignatura (Codigo, Siglas, Cuatrimestre, Nombre, Curso, Especialidad) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        codigo,
                        siglas,
                        cuatrimestre,
                        nombre_asignatura,
                        curso,
                        especialidad,
                    ),
                )
                print(siglas)
                cursor.execute(
                    "INSERT OR IGNORE INTO Grupo (Asignatura_Codigo, Letra, Fecha, Profesor_Nombre, Aula) VALUES (?, ?, ?, ?, ?)",
                    (codigo, grupo, ", z".join(map(str, horas)), profesor_teoria, aula),
                )
                # ---------------------------------

            default_cont = 1
            lista_subgrupos = {"A": [], "B": [], "C": [], "D": [], "E": [], "F": []}
            for grupo_practicas in datos_asignatura[
                "docentesGruposP"
            ]:  # Horarios grupos prácticas
                subgrupo = grupo_practicas["grupo"]  # Pj: 1, 2, 3
                profesor_practicas = re.sub(
                    r"\([^)]*\)", "", grupo_practicas["nombre"]
                )  # Quito los parentesis
                horarios = obtener_json_asignaturas(
                    param1, param2, param3, subgrupo, "2", cookies
                )
                try:
                    cuatrimestre = horarios[0]["title"]
                except IndexError:
                    cuatrimestre = None
                    aula = None
                if cuatrimestre is not None:
                    aula = horarios[0]["title"][-2:]
                    if cuatrimestre.startswith("Primer cuatrimestre"):
                        cuatrimestre = "1"
                    else:
                        cuatrimestre = "2"
                horas = []
                for item in horarios:
                    dia = int(re.sub(r"[\[\]]", "", item["daysOfWeek"])) * 100
                    inicio = int(dict_horas.get(item["startTime"], -1))
                    fin = int(dict_horas.get(item["endTime"], -1))
                    consecutivas = fin - inicio
                    if consecutivas > 1:
                        for hora in range(consecutivas):
                            horas.append(int(dia + inicio + hora))
                    else:
                        horas.append(int(dia + dict_horas[item["startTime"]]))
                nombre_asignatura = nombre_asignatura.replace(" ", "")
                subgrupo = dict_correspondencia_subgrupos.get(
                    (nombre_asignatura, subgrupo), "A" + subgrupo
                )
                default_cont += 1
                lista_subgrupos[
                    dict_correspondencia_subgrupos.get(
                        (nombre_asignatura, subgrupo), "A"
                    )[0]
                ].append(
                    [
                        codigo,
                        siglas,
                        subgrupo,
                        profesor_practicas,
                        cuatrimestre,
                    ]
                    + horas
                )
                # ---------------------------------
                cursor.execute(
                    "INSERT OR IGNORE INTO Subgrupo (Asignatura_Codigo, Grupo_Letra, Numero, Fecha, Profesor_Nombre, Aula) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        codigo,
                        subgrupo[0],  # Grupo_Letra
                        subgrupo[1],  # Numero
                        ", ".join(map(str, horas)),
                        profesor_practicas,
                        aula,
                    ),
                )
                # ---------------------------------

    # # Create a new table with the aggregated data
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS Subgrupo_new AS
    #     SELECT Asignatura_Codigo, Grupo_Letra, Numero, Fecha, GROUP_CONCAT(Profesor_Nombre, '|') as Profesor_Nombre, Aula
    #     FROM Subgrupo
    #     GROUP BY Asignatura_Codigo, Grupo_Letra, Numero, Fecha
    # """
    # )

    # # Drop the old table
    # cursor.execute("DROP TABLE IF EXISTS Subgrupo")

    # # Rename the new table to the original name
    # cursor.execute("ALTER TABLE Subgrupo_new RENAME TO Subgrupo")
    script_sql = """
    UPDATE Asignatura SET Siglas = 'CRIP' WHERE Codigo = '29611AF';
    UPDATE Asignatura SET Siglas = 'SMM' WHERE Codigo = '296113V';
    UPDATE Asignatura SET Siglas = 'MH' WHERE Codigo = '296113E';
    UPDATE Asignatura SET Especialidad = 'TI' WHERE Codigo = '29611FC';
    UPDATE Asignatura SET Especialidad = 'TI' WHERE Codigo = '29611FD';
    UPDATE Asignatura SET Especialidad = 'CSI' WHERE Codigo = '296113D';
    UPDATE Asignatura SET Especialidad = 'CSI' WHERE Codigo = '296114C';
    UPDATE Asignatura SET Especialidad = 'TI' WHERE Codigo = '296114P';
    UPDATE Asignatura SET Especialidad = 'CSI' WHERE Codigo = '296113B';
    UPDATE Asignatura SET Siglas = 'ISE' WHERE Codigo = '2961135';
    UPDATE Asignatura SET Siglas = 'PLD' WHERE Codigo = '29611AB';
    UPDATE Asignatura SET Siglas = 'ALG' WHERE Codigo = '2961126';
    """

    cursor.executescript(script_sql)
    conn.commit()
    conn.close()


obtener_asignaturas(correspondencia_subgrupos())
