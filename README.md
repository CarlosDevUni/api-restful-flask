# Ejemplo de API RESTful implementada con Python + Flask + MYSQL


1. Crear directorio de proyecto (backend)

2. Crear entorno virtual    **py -3 -m venv .venv**

3. Activamos el entorno virtual  **.\.venv\Scripts\activate**

4. Creamos el archivo de requisitos
 - **requirements.txt**
	+ flask == 2.3.3
	+ flask-mysqldb == 1.0.1
	+ PyJWT == 2.8.0
	+ flask-cors

5. Instalar dependencias    **pip install -r requirements.txt**

6. Crear estructura de directorios
	* /backend
		* /backend/api
			+ /backend/api/routes
				* /backend/api/routes/client.py
			+ /backend/api/models
				* /backend/api/models/client.py
			+ /backend/api/db
				* /backend/api/db/dp.py
			+ /backend/api/__init__.py
			+ /backend/api/utils.py
		* /backend/main.py
		* /backend/requirements.txt
---

## Explicación:

### main.py 
Es el punto de inicio de la aplicación, su función es importar el objeto app y ejecutar su método run.

	from api import app
	import sys

	if len(sys.argv) > 1 and sys.argv[1] == "list":
		print(app.url_map)
	elif __name__ == "__main__":
		app.run( debug=True, port= 5200)

---
	
### Directorios 
+ /api organiza la estructura interna de la aplicación.
+ /api/routes contiene todos los archivos relacionados con las creaciones de rutas, cada uno agrupando las rutas referidas a un mismo recurso.
+ /api/models contiene todos los archivos relacionados con las definiciones de clases, principalmente para facilitar el formateo de datos desde la BD en formato JSON.
+ /api/db contiene lo relacionado a la configuración y conección a la BD.

---

### Archivos
**api/_\_init_\_.py** crea el objeto app como una instancia de Flask, incorpora CORS y configura la clave secreta de la aplicación. También debe importar todas las rutas para cada recurso.

	from flask import Flask
	from flask_cors import CORS
	app = Flask(__name__)
	CORS(app)
	app.config['SECRET_KEY'] = 'app_123'
	import api.routes.client
	import api.routes.user

**api/utils.py** contiene funciones genéricas que se utilizan en diferentes partes de la aplicación, por ejemplo los wrappers empleados para el control de acceso a diferentes rutas.

	from functools import wraps
	from flask import request, jsonify
	import jwt
	from api import app
	from api.db.db import mysql

	def token_required(func):
		@wraps(func)
		def decorated(\*args, \*\*kwargs):
			\# Control de token y retorno en caso de errores 
			\...
			return func(\*args, \*\*kwargs)
		return decorated
	
	\# Otras funciones ..

**api/db/db.py** contiene la configuración de la BD y crea el objeto mysql, que debe ser importado desde todos los módulos que requieran una conección a la BD.

	from api import app
	from flask_mysqldb import MySQL
	app.config['MYSQL_HOST'] = 'localhost'
	app.config['MYSQL_USER'] = 'user_api_flask'
	app.config['MYSQL_PASSWORD'] ='password'
	app.config['MYSQL_DB'] = 'db_api_flask'
	mysql = MySQL(app)

**api/models/client.py** contiene la definición de la clase Client, con su constructor y un método para formatear en JSON.

	class Client():
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
   
**api/routes/client.py** contiene las rutas para las operaciones CRUD del recurso client, y puede incorporar otras funcionalidades específicas sobre ese recurso. Debe importar la clase Client, el objeto app, el objeto mysql y las funciones de utilidades necesarias.
	
 	from api import app
	from api.models.client import Client
	from flask import jsonify
	from api.utils import token_required, client_resource, user_resources
	from api.db.db import mysql
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
	
	/# Otras rutas del recurso client


Con esta estructura, la escalabilidad del proyecto se logra creando archivos de modelo y rutas para cada nuevo recurso que se deba incorporar.

