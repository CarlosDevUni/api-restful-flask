from api import app
from api.models.client import Client
from flask import jsonify
from api.utils import token_required, client_resource, user_resources
from api.db.db import mysql

""" @app.route('/test')
def test():
    return jsonify({"ruta": "cliente-route"}) """

@app.route('/user/<int:id_user>/client/<int:id_client>', methods = ['GET'])
@token_required
@user_resources
@client_resource
def get_client_by_id(id_user, id_client):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM client WHERE id = {0}'.format(id_client))
    data = cur.fetchall()
    print(cur.rowcount)
    print(data)
    if cur.rowcount > 0:
        objClient = Client(data[0])
        return jsonify( objClient.to_json() )
    return jsonify( {"message": "id not found"} ), 404


@app.route('/user/<int:id_user>/client', methods = ['GET'])
@token_required
@user_resources
def get_all_clients_by_user_id(id_user):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM client WHERE id_user = {0}'.format(id_user))
    data = cur.fetchall()
    clientList = []
    for row in data:
        objClient = Client(row)
        clientList.append(objClient.to_json())
    
    return jsonify(clientList)