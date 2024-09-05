"""Este modulo crea la BD de las asignaturas, grupos, subgrupos y profesores de la universidad"""

import sqlite3

conn = sqlite3.connect("universidad.db")
cursor = conn.cursor()
cursor.execute("""DROP TABLE IF EXISTS Asignatura""")
cursor.execute("""DROP TABLE IF EXISTS Grupo""")
cursor.execute("""DROP TABLE IF EXISTS Subgrupo""")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS Asignatura (
                  Codigo TEXT PRIMARY KEY,
                  Siglas TEXT,
                  Cuatrimestre NUMERIC,
                  Nombre TEXT,
                  Curso NUMERIC,
                  Especialidad TEXT)"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS Grupo (
                  Asignatura_Codigo TEXT,
                  Letra TEXT,
                  Fecha TEXT,
                  Profesor_Nombre TEXT,
                  Aula TEXT,
                  PRIMARY KEY (Asignatura_Codigo, Letra),
                  FOREIGN KEY (Asignatura_Codigo) REFERENCES Asignatura(Codigo))"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS Subgrupo (
                  Asignatura_Codigo TEXT,
                  Grupo_Letra TEXT,
                  Numero TEXT,
                  Fecha TEXT,
                  Profesor_Nombre TEXT,
                  Aula TEXT,
                  Primary Key (Asignatura_Codigo, Grupo_Letra, Numero, Profesor_Nombre),
                  FOREIGN KEY (Grupo_Letra) REFERENCES Grupo(Letra),
                  FOREIGN KEY (Asignatura_Codigo) REFERENCES Asignatura(Codigo))"""
)

conn.commit()
conn.close()

print("Base de datos creada")
