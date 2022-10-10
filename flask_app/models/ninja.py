from flask import flash
from flask_app.models.models import Model
from flask_app.config.mysqlconnection import connectToMySQL

class Ninja(Model):
    tabla = "ninjas"

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.dojo_id = data['dojo_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = f"INSERT INTO {cls.tabla} ( first_name , last_name , age, dojo_id ) VALUES ( %(fname)s , %(lname)s , %(age)s, %(dojo_id)s );" 
        return connectToMySQL(cls.esquema).query_db( query, data )

    @staticmethod
    def validNinja(dataNinja):
        is_valid = True

        if len(dataNinja['first_name']) < 2:
            flash("El nombre debe poseer al menos 2 caracteres", "warning")
            is_valid = False

        if len(dataNinja['last_name']) < 2:
            flash("El apellido debe poseer al menos 2 caracteres", "warning")
            is_valid = False

        if int(dataNinja['age']) < 18:
            flash("El ninja debe ser mayor de edad", "warning")
            is_valid = False

        if dataNinja['dojo_id'] == "":
            flash("Debe seleccionar un Dojo", "warning")
            is_valid = False

        return is_valid

    @classmethod
    def getByDojo(cls, dojo_id):
        query = f"SELECT * FROM {cls.tabla} WHERE dojo_id = %(dojo_id)s;"
        results = connectToMySQL(cls.esquema).query_db(query, {
            "table": cls.tabla,
            'dojo_id': dojo_id
        })
        
        listResult = []
        for result in results:
            listResult.append( cls(result) )
        return listResult