"""
Proyecto de sqlite con flask y postman para manejar una base de datos de estudiantes de la FIIS
"""

import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


class Estudiante:
    """Crea a un estudiante"""
    def __init__(self, codigo, nombre, apellido, promedio):
        self.codigo = codigo
        self.nombre = nombre
        self.apellido = apellido
        self.promedio = promedio


def insertar_estudiante(estudiante):
    """Inserta a un estudiante en la bd"""
    global senial
    conn = sqlite3.connect("FIIS.db")
    cur = conn.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS estudiantes(
        codigo TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        promedio REAL)"""
    )

    try:
        cur.execute(
            "INSERT INTO estudiantes VALUES (?, ?, ?, ?)",
            (
                estudiante.codigo,
                estudiante.nombre,
                estudiante.apellido,
                estudiante.promedio,
            ),
        )
        print("Estudiante insertado correctamente.")
        senial = True
    except sqlite3.IntegrityError:
        print("Error: El código del estudiante ya existe en la base de datos.")
        senial = False

    conn.commit()
    conn.close()


@app.route("/insertar", methods=["POST"])
def agregar_estudiante():
    """Agrega a un estudiante a la bd"""
    data = request.get_json()
    estudiante = Estudiante(
        data["codigo"], data["nombre"], data["apellido"], data["promedio"]
    )
    insertar_estudiante(estudiante)
    if senial is True:
        return jsonify({"message": "Estudiante agregado correctamente"})
    else:
        return jsonify(
            {
                "message": "Error: El código del estudiante ya existe en la base de datos."
            }
        )


@app.route("/mostrar", methods=["GET"])
def obtener_estudiantes():
    """Consulta todos los estudiantes de la bd"""
    conn = sqlite3.connect("FIIS.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM estudiantes")
    rows = cur.fetchall()

    estudiantes = []
    for row in rows:
        estudiante = Estudiante(row[0], row[1], row[2], row[3])
        estudiantes.append(estudiante.__dict__)

    conn.close()

    return jsonify(estudiantes)


@app.route("/mostrar_codigo", methods=["POST"])
def mostrar_codigo():
    """Muestra un estudiante en especifico de la bd"""
    conn = sqlite3.connect("FIIS.db")
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("SELECT * FROM estudiantes WHERE codigo=?", (data["codigo"],))
    row = cur.fetchone()

    if row is not None:
        estudiante = Estudiante(row[0], row[1], row[2], row[3])
        return jsonify(estudiante.__dict__)
    else:
        return jsonify(
            {"message": "No se encontró un estudiante con el código especificado."}
        )


@app.route("/eliminar", methods=["POST"])
def eliminar_estudiante():
    """Elimina a un estudiante en especifico de la bd"""
    conn = sqlite3.connect("FIIS.db")
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("DELETE FROM estudiantes WHERE codigo=?", (data["codigo"],))
    if cur.rowcount > 0:
        conn.commit()
        conn.close()
        return jsonify({"message": "Estudiante eliminado correctamente"})
    else:
        conn.commit()
        conn.close()
        return jsonify(
            {"message": "No se encontró un estudiante con el código especificado."}
        )

if __name__ == "__main__":
    app.run()
