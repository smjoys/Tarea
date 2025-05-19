from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Conexión a MongoDB (puedes cambiar el puerto si es necesario)
client = MongoClient("mongodb://localhost:27023/")
db = client["escuela"]
estudiantes_collection = db["estudiantes"]

# Ruta para agregar un estudiante
@app.route("/estudiantes", methods=["POST"])
def agregar_estudiante():
    data = request.get_json()  # corregido: antes decía request.json()
    
    if not data or "rut" not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    if estudiantes_collection.find_one({"rut": data["rut"]}):
        return jsonify({"error": "El estudiante ya existe"}), 400

    estudiantes_collection.insert_one(data)
    return jsonify({"message": "Estudiante agregado"}), 201

# Ruta para obtener todos los estudiantes
@app.route("/estudiantes", methods=["GET"])
def obtener_estudiantes():
    estudiantes = list(estudiantes_collection.find({}, {"_id": 0}))
    return jsonify(estudiantes)

# Ruta para obtener un estudiante por RUT
@app.route("/estudiantes/<rut>", methods=["GET"])
def obtener_estudiante_por_rut(rut):
    estudiante = estudiantes_collection.find_one({"rut": rut}, {"_id": 0})
    if estudiante:
        return jsonify(estudiante)
    return jsonify({"error": "Estudiante no encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
