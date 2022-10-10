from flask_app import app
from flask import flash, render_template, redirect, request
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja

@app.route("/")
def index():
    return redirect('/dojos')

@app.route("/dojos")
def dashboard():
    dojos = Dojo.get_all()
    return render_template("dojo/index.html", dojos=dojos)

@app.route("/dojos", methods = ["POST"])
def createDojo():
    if not Dojo.validDojo(request.form):
        return redirect('/dojos')

    data = {
        'name': request.form['name'],
    }

    idDojo = Dojo.save(data)

    if idDojo is False:
        flash("Lo sentimos, ha ocurrido un error al crear un nuevo Dojo", "danger")
    else:
        flash("Dojo creado correctamente", "success")
    
    return redirect('/dojos')

@app.route("/dojos/<int:dojo_id>")
def showDojo(dojo_id):

    dojo = Dojo.getWithNinjas(dojo_id)

    # ninjas = Ninja.getByDojo(dojo_id)
    return render_template('dojo/show.html', dojo=dojo)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404