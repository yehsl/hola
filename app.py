import MySQLdb
from flask import Flask, request, render_template_string, redirect, url_for, render_template
from flask_mysqldb import MySQL


app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'https://hola-8bz4.onrender.com'
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
    conn.commit()
    cursor.close()
    conn.close()

@app.before_first_request
def setup():
    create_database_and_table()

def restar_stock(new_stock,product):
    conn = MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD']
    )
    cursor = conn.cursor()
    cursor.execute('USE mydatabase;')
    cursor.execute(f'UPDATE p SET s = {new_stock} WHERE p = "{product}";')
    conn.commit()
    cursor.close()
    conn.close()
    
@app.route('/')
def index():
    conn = MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD']
    )
    cur = conn.cursor()
    cur.execute("USE mydatabase")
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.execute("SELECT * FROM p")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('main.html',data=data)


# Página principal con el formulario


# Ruta para procesar los datos



@app.route('/comprar', methods=['POST'])
def comprar():
    lista_str = request.form.get('info', "")
    lista = eval(lista_str)  # Convertir la cadena de vuelta a lista
    new_stock = int(lista[2])
    new_stock -= 1
    product = lista[0]
    print(new_stock)
    restar_stock(new_stock,product)
    return render_template('pr.html',data=lista)
@app.route('/pro', methods=['POST'])
def pro():
    lista_str = request.form.get('info', "")
    lista = eval(lista_str)  # Convertir la cadena de vuelta a lista
    lista_str2 = request.form.get('info2', "")
    lista2 = eval(lista_str2)  # Convertir la cadena de vuelta a lista
    return f"{lista} ::: {lista2}"
if __name__ == '__main__':
    app.run(port=3006, debug=True)
