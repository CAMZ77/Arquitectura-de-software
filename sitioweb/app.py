from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/admin/')
def admin_index():
    return render_template('admin_index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/games')
def admin_games():
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `juegos`")
    juegos=cursor.fetchall()
    conexion.commit()
    print(juegos)

    return render_template('admin_games.html', juegos=juegos)

@app.route('/admin/games/guardar', methods=['POST'])
def admin_games_guardar():
    _nombre=request.form['txtNombre']
    _archivo=request.files['txtImagen']
    _plataforma=request.form['txtPlataforma']
    _precio=request.form['txtPrecio']
    _url=request.form['txtURL']

    sql="INSERT INTO `juegos` (`nombre`, `imagen`, `plataforma`, `precio`, `url`, `ID`) VALUES (%s,%s,%s,%s,%s,NULL);"
    datos=(_nombre,_archivo.filename,_plataforma,_precio,_url)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    print(_nombre)
    print(_archivo)
    print(_plataforma)
    print(_precio)
    print(_url)

    return redirect('/admin/games')

@app.route("/admin/games/borrar", methods=['POST'])
def admin_games_borrar():
    _id=request.form['txtID']
    print(_id)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `juegos` WHERE id=%s",(_id))
    juego=cursor.fetchall()
    conexion.commit()
    print(juego)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM `juegos` WHERE id=%s",(_id))
    conexion.commit()
    
    return redirect('/admin/games')

if __name__ =='__main__':
    app.run(debug=True)
