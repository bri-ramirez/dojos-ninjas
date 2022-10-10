from flask import flash
from flask_app.models.models import Model
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ninja

class Dojo(Model):
    tabla = "dojos"

    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []

    @classmethod
    def save(cls, data):
        query = f"INSERT INTO {cls.tabla} ( name ) VALUES ( %(name)s );" 
        return connectToMySQL(cls.esquema).query_db( query, data )

    @staticmethod
    def validDojo(dataDojo):
        is_valid = True

        if len(dataDojo['name']) < 2:
            flash("El nombre debe poseer al menos 2 caracteres")
            is_valid = False
        
        return is_valid

    @classmethod
    def getWithNinjas(cls, dojo_id):

        query = f"SELECT * FROM dojos \
            JOIN ninjas ON dojos.id = ninjas.dojo_id \
            WHERE dojos.id = %(dojo_id)s;"
        
        results = connectToMySQL(cls.esquema).query_db(query, {
            "dojo_id": dojo_id
        })

        if len(results) == 0 or results is False:
            return False

        dojo = cls(results[0])

        for row_from_db in results:
            ninja_data = {
                'id': row_from_db["ninjas.id"],
                'first_name': row_from_db["first_name"],
                'last_name': row_from_db["last_name"],
                'age': row_from_db["age"],
                'dojo_id': row_from_db["dojo_id"],
                'created_at': row_from_db["ninjas.created_at"],
                'updated_at': row_from_db["ninjas.updated_at"]
            }

            dojo.ninjas.append( ninja.Ninja( ninja_data )  )

        return dojo        