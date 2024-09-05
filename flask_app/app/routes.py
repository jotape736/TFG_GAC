from flask import Flask, jsonify, request, json
from json import JSONDecodeError
from .services import generar_horarios, traducir_horarios
from .models import get_asignaturas_curso, get_asignatura_grupos_teoria, get_subgrupos
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def home():
    return jsonify({"message": "Hello, World!"})


# @app.route("/horarios/", methods=["GET"])
# def get_horarios():
#     asignaturas = {
#         "2961115": ["A1", "A2", "A3"],
#         "2961125": ["C1", "C2", "C3"],
#         "296113V": ["A1", "A2", "A3"],
#         "2961123": ["A1", "A2", "A3"],
#     }
#     # asignaturas = {"2961115": ["A1", "A2", "A3"]}
#     return jsonify(generar_horarios(asignaturas))


@app.route("/horarios/", methods=["GET"])
def get_horarios():
    try:
        asignaturas_json = request.args.get("asignaturas")
        if asignaturas_json:
            data = json.loads(asignaturas_json)
            asignaturas = {key: value for key, value in data.items()}
            lista = generar_horarios(asignaturas)
            lista_horarios = traducir_horarios(lista)
            # for item in generar_horarios(asignaturas):
            #     lista_horarios.append(traducir_horarios(item))
            return jsonify(lista_horarios)
        else:
            return jsonify({"error": "No se proporcionaron asignaturas"}), 400
    except JSONDecodeError:
        return jsonify({"error": "Error al decodificar JSON"}), 400
    except Exception as e:
        # Imprime el error en los registros del servidor
        print(f"Error: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route("/subgrupos/<string:asignatura_codigo_letra>", methods=["GET"])
def get_subgrupos_asignatura(asignatura_codigo_letra):
    # la letra es el último caracter
    asignatura_codigo = asignatura_codigo_letra[:-1]
    # el codigo es el resto de la cadena
    letra = asignatura_codigo_letra[-1]
    return jsonify(get_subgrupos(asignatura_codigo, letra))


@app.route("/asignaturas/curso/<int:curso>/<int:cuatrimestre>", methods=["GET"])
def get_asignaturas(curso, cuatrimestre):
    return jsonify(get_asignaturas_curso(curso, cuatrimestre))


@app.route("/teoria/<string:asignatura_codigo>", methods=["GET"])
def get_grupos(asignatura_codigo):
    return jsonify(get_asignatura_grupos_teoria(asignatura_codigo))


@app.route("/traducir/", methods=["GET"])
def get_traduccion():
    horarios = ["2961111B1", "2961111B2"]
    return jsonify(traducir_horarios(horarios))
