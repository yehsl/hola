import MySQLdb
from flask import Flask, render_template
from flask_mysqldb import MySQL
import mysql.connector

cnx = mysql.connector.connect(user='root', password='198789',
                              host='127.0.0.1',
                              database='mydatabase')
cur = cnx.cursor()
app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '198789'  # Cambia esto a tu contraseña de MySQL
app.config['MYSQL_DB'] = 'mydatabase'
app.config['MYSQL_PORT'] = 3306  # Puerto por defecto para MySQL

mysql = MySQL(app)
#cnx = mysql.connector.connect(database='mydatabase')
#cursor = cnx.cursor()

def create_database_and_table():
    # Crear la base de datos y la tabla si no existen
    conn = MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD']
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
    cursor.execute("USE mydatabase")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    """)
    cursor.execute("CREATE USER 'root'@'%' IDENTIFIED BY '198789';")
    cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';")
    conn.commit()
    cursor.close()
    conn.close()

@app.before_first_request
def setup():
    create_database_and_table()

@app.route('/')
def index():
    #cnx = mysql.connector.connect(user='root', password='198789',
                                 #host='127.0.0.1',
                                 #database='mydatabase')
    #cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(port=3006, debug=True)
