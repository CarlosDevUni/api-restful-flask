from api import app
from api.models.client import Client
from flask import jsonify, request
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

# Create a new client
@app.route('/user/<int:id_user>/client', methods = ['POST'])
@token_required
@user_resources
def create_client(id_user):
    data = request.get_json()
    data["id_user"] = id_user
    try:
        new_client = Client.create_client(data)
        return jsonify( new_client ), 201
    except Exception as e:
        return jsonify( {"message": e.args[0]} ), 400
    
# Update a client
@app.route('/user/<int:id_user>/client/<int:id_client>', methods = ['PUT'])
@token_required
@user_resources
@client_resource
def update_client(id_user, id_client):
    data = request.get_json()
    data["id_user"] = id_user
    try:
        updated_client = Client.update_client(id_client, data)
        return jsonify( updated_client ), 200
    except Exception as e:
        return jsonify( {"message": e.args[0]} ), 400