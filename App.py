############# importar librerias o recursos#####
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

# inicializaciones
app = Flask(__name__)




# Mysql Conexión
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'adata' # NOMBRE DE LA BASE DE DATOS#
mysql = MySQL(app)

# Flask utilizará esta clave para poder cifrar la información de la cookie
app.secret_key = "mysecretkey"


 



### LOGIN' ###

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
   
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Conectarse a la base de datos
   
    cursor = mysql.connection.cursor()
   
    cursor.execute("SELECT * FROM usuario WHERE usuario=%s AND contraseña=%s", (username, password))
    user = cursor.fetchone()

    
    if user:
        response = {
            'success': True,
            'message': 'Login exitoso',
            'token': 'abcd1234'
        }
    else:
        response = {
            'success': False,
            'message': 'Usuario o contraseña incorrectos'
        }

    return jsonify(response)

### -----------------------------CONSULTAR-------------------------------------------------------###


@app.route('/consultar', methods=['GET'])
@cross_origin()
def getAll():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM carro_nissan')
    rv = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in rv:
       content = {'COL5': result[4], 'COL6': result[5], 'COL7': result[6], 'COL8': result[7],'COL9': result[8],'COL10': result[9],'id': result[10]}
       payload.append(content)
    return jsonify(payload)




@app.route('/actualizar/<id>', methods=['PUT'])
@cross_origin()
def update(id):
    data = request.get_json()
    precio = data['precio']
    marca = data['marca']
    modelo = data['modelo']
    antiguedad = data['antiguedad']
    kilometraje = data['kilometraje']
    color = data['color']
    id = data['id']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE carro_nissan
        SET  COL5 = %s,
             COL6 = %s,
             COL7 = %s,
             COL8 = %s,
             COL9 = %s,
             COL10 = %s
        WHERE id = %s
    """, (precio, marca, modelo, antiguedad, kilometraje,color,id,))
    mysql.connection.commit()
    response = {
        'success': True,
        'message': 'Dato actualizado exitosamente'
    }
    
    return jsonify(response)


### RUTA PARA ELIMINAR UN REGISTRO EN LA TABLA  ###

@app.route('/eliminar/<id>', methods = ['DELETE'])
@cross_origin()
def delete(id):
    
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM  carro_nissan WHERE id = %s', (id,))
    mysql.connection.commit()
    response = {
        'success': True,
        'message': 'Dato  eliminado exitosamente'
    }
    return jsonify(response)

###*************************************************************************************###

@app.route('/insertar', methods=['POST'])
@cross_origin()
def insertar():
    data = request.get_json()
    precio = data['precio']
    marca = data['marca']
    modelo = data['modelo']
    antiguedad = data['antiguedad']
    kilometraje = data['kilometraje']
    color = data['color']

    # Conectarse a la base de datos
    cursor = mysql.connection.cursor()
   
    # Insertar los datos en la base de datos
    cursor.execute("INSERT INTO carro_nissan (COL5,COL6,COL7,COL8,COL9,COL10) VALUES (%s, %s,%s,%s,%s,%s)", (precio,marca,modelo,antiguedad,kilometraje,color))
    mysql.connection.commit()

    # Crear una respuesta con éxito
    response = {
        'success': True,
        'message': 'Dato creado exitosamente'
    }

    return jsonify(response)

# La API inicia
if __name__ == "__main__":
    app.run(port=3000, debug=True)


