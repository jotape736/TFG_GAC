import sqlite3

ruta = "instance/universidad.db"
# ruta = "../instance/universidad.db"


def get_cuatrimestre(codigo):
    conn = sqlite3.connect(ruta)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT Cuatrimestre FROM Asignatura WHERE Codigo = ?""",
        (codigo,),
    )
    cuatrimestre = cursor.fetchone()[0]
    conn.close()
    return cuatrimestre


def get_fecha_grupo(asignatura_codigo, letra):
    conn = sqlite3.connect(ruta)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT Fecha FROM Grupo WHERE Asignatura_Codigo = ? AND Letra = ?""",
        (asignatura_codigo, letra),
    )
    fecha = cursor.fetchone()
    conn.close()
    return fecha


def get_fecha_subgrupo(asignatura_codigo, letra, numero):
    conn = sqlite3.connect(ruta)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT Fecha FROM Subgrupo WHERE Asignatura_Codigo = ? AND Grupo_Letra = ? AND Numero = ?""",
        (asignatura_codigo, letra, numero),
    )
    fecha = cursor.fetchone()
    conn.close()
    return fecha


def get_asignaturas_curso(curso, cuatrimestre):
    conn = sqlite3.connect(ruta)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT Siglas, Nombre, Especialidad, Codigo FROM Asignatura WHERE Curso = ? AND Cuatrimestre = ?""",
        (curso, cuatrimestre),
    )
    asignaturas = cursor.fetchall()
    conn.close()
    return asignaturas


def get_subgrupos(asignatura_codigo, letra):
    conn = sqlite3.connect(ruta)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT Asignatura_Codigo, Grupo_Letra || Numero AS Subgrupo FROM Subgrupo WHERE Asignatura_Codigo = ? AND Grupo_Letra = ?""",
        (asignatura_codigo, letra),
    )
    subgrupos = cursor.fetchall()
    conn.close()
    return subgrupos


def get_asignatura_grupos_teoria(asignatura_codigo):
    conn = sqlite3.connect(ruta)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT 
                A.Nombre AS NombreAsignatura,
                A.Siglas AS SiglasAsignatura,
                A.codigo AS CodigoAsignatura,
                G.Letra AS GrupoLetra,
                G.Profesor_Nombre AS GrupoProfesorNombre
            FROM 
                Asignatura A
            JOIN 
                Grupo G ON A.Codigo = G.Asignatura_Codigo
            WHERE
                A.Codigo = ?
            GROUP BY
                G.Letra""",
        (asignatura_codigo,),
    )
    grupos = cursor.fetchall()
    conn.close()
    return grupos


def get_datos_grupo(asignatura_codigo, letra):
    conn = sqlite3.connect(ruta)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT 
                A.Siglas AS SiglasAsignatura,
                G.Letra AS GrupoLetra,
                G.Profesor_Nombre AS GrupoProfesorNombre
            FROM 
                Asignatura A
            JOIN 
                Grupo G ON A.Codigo = G.Asignatura_Codigo
            WHERE
                A.Codigo = ? AND G.Letra = ?
            GROUP BY
                G.Letra""",
        (asignatura_codigo, letra),
    )
    grupo = cursor.fetchone()
    conn.close()
    return grupo


def get_datos_subgrupo(asignatura_codigo, letra, numero):
    conn = sqlite3.connect(ruta)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT 
            A.Siglas AS SiglasAsignatura,
            S.Grupo_Letra AS SubgrupoLetra,
            S.Numero AS SubgrupoNumero,
            GROUP_CONCAT(S.Profesor_Nombre, '\n') AS SubgrupoProfesorNombre
        FROM 
            Asignatura A
        JOIN 
            Subgrupo S ON A.Codigo = S.Asignatura_Codigo
        WHERE
            A.Codigo = ? AND S.Grupo_Letra = ? AND S.Numero = ?
        GROUP BY
            A.Siglas, S.Grupo_Letra, S.Numero""",
        (asignatura_codigo, letra, numero),
    )
    subgrupo = cursor.fetchone()
    conn.close()
    return subgrupo
