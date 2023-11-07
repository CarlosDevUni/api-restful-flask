from api.db.db import mysql, DBError
from flask import jsonify

class Client():
    schema = {
        "name": str,
        "id_user": int
    }

    def check_data_schema(data):
        if data == None or type(data) != dict:
            return False
        # check if data contains all keys of schema
        for key in Client.schema:
            if key not in data:
                return False
            # check if data[key] has the same type as schema[key]
            if type(data[key]) != Client.schema[key]:
                return False
        return True

    def __init__(self, row):
        self._id = row[0]
        self._name = row[1]
        self._id_user = row[2]

    def to_json(self):
        return {
            "id": self._id,
            "name": self._name,
            "id_user" : self._id_user
        }    
    
    def client_exists(name, id_user):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM client WHERE name = %s AND id_user = %s', (name, id_user))
        cur.fetchall()
        return cur.rowcount > 0

    def create_client(data):
        if Client.check_data_schema(data):
            # check if client already exists
            if Client.client_exists(data["name"], data["id_user"]):
                raise DBError("Error creating client - client already exists")
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO client (name, id_user) VALUES (%s, %s)', (data["name"], data["id_user"]))
            mysql.connection.commit()
            if cur.rowcount > 0:
                # get the id of the last inserted row
                cur.execute('SELECT LAST_INSERT_ID()')
                res = cur.fetchall()
                id = res[0][0]
                return Client((id, data["name"], data["id_user"])).to_json()
            raise DBError("Error creating client - no row inserted")
        raise TypeError("Error creating client - wrong data schema")
    
    def update_client(id, data):
        if Client.check_data_schema(data):
            cur = mysql.connection.cursor()
            cur.execute('UPDATE client SET name = %s WHERE id = %s', (data["name"], id))
            mysql.connection.commit()
            if cur.rowcount > 0:
                return Client.get_client_by_id(id)
            raise DBError("Error updating client - no row updated")
        raise TypeError("Error updating client - wrong data schema")
    
    def get_client_by_id(id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM client WHERE id = {0}'.format(id))
        data = cur.fetchall()
        if cur.rowcount > 0:
            return Client(data[0]).to_json()
        raise DBError("Error getting client by id - no row found")