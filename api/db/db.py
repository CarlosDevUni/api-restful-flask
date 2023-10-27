from api import app
from flask_mysqldb import MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user_api_flask'
app.config['MYSQL_PASSWORD'] ='password'
app.config['MYSQL_DB'] = 'db_api_flask'

mysql = MySQL(app)