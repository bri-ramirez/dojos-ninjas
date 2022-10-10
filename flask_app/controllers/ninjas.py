from flask_app import app
from flask import flash, render_template, redirect, request
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja

@app.route("/ninjas")
def newNinja():
    dojos = Dojo.get_all()
    return render_template("ninja/form.html", dojos=dojos)

@app.route("/ninjas", methods = ["POST"])
def createNinja():
    if not Ninja.validNinja(request.form):
        return redirect('/ninjas')

    data = {
        'fname': request.form['first_name'],
        'lname': request.form['last_name'],
        'age': request.form['age'],
        'dojo_id': request.form['dojo_id'],
    }

    idNinja = Ninja.save(data)

    if idNinja is False:
        flash("Lo sentimos, ha ocurrido un error al crear un nuevo Ninja", "danger")
        return redirect('/ninjas')

    flash("Ninja creado correctamente", "success")
    return redirect('/dojos')
