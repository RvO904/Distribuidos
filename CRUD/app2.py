from flask import Flask, render_template, request, redirect
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS
from dotenv import find_dotenv, load_dotenv
import os

app = Flask(__name__)
CORS(app)

'''
Esquema de la base de datos no relacional de tareas
tarea
    _id - ObjectId()
    titulo - str
    description - str
    fechaCreacion - datetime.datetime
'''

# Ruta principal para añadir, eliminar o actualizar tareas
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        formato_fecha = '%d-%m-%Y %H:%M:%S'
        titulo = request.form["title"]
        descripcion = request.form["desc"]
        fecha_creacion = datetime.now().strftime(formato_fecha)
       
        tarea = {'titulo':titulo, 'descripcion':descripcion, 'fechaCreacion':fecha_creacion}  

        collection.insert_one(tarea)

    tareas = [result for result in collection.find({})]
    return render_template("index.html", all_todos=tareas)


# Ruta para actualizar tareas existentes
@app.route("/update/<string:sno>", methods=["GET", "POST"])
def update_item(sno):
    if request.method == "POST":
        user_title = request.form["title"]
        user_desc = request.form["desc"]

        titulo_nuevo = user_title if user_title else tarea['titulo']
        descr_nueva = user_desc if user_desc else tarea['descripcion']

        collection.update_one({'_id': ObjectId(sno)}, {'$set' :{'titulo':titulo_nuevo, 'descripcion':descr_nueva}})
        print('hecho')
        return redirect("/")

    tarea = collection.find_one({'_id':ObjectId(sno)})
    return render_template("update.html", todo=tarea)


#Ruta para eliminar registros de la base de datos
@app.route('/delete/<sno>')
def delete_item(sno):
    collection.delete_one({'_id':ObjectId(sno)})
    return redirect('/')


#Ruta para búsqueda del título de una tarea en la base de datos
@app.route('/search', methods=["GET", "POST"])
def search_item():
    # Obtener la palabra clave de búsqueda del campoo query
    search_query = request.args.get('query')

    # Hacer la búsqueda en la base de datos
    tareas = collection.find({'titulo':search_query})

    # Mostrar el resultado
    return render_template('result.html', posts=tareas)


if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27018/', replicaSet='RS')
    db = client['Distribuidos']
    collection = db['tasks']
    app.run(debug=True, port=8000)
