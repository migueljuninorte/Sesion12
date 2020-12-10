from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
import yagmail as yagmail
import utils
import os
from formulario import Registro
from datos import listadatos
import json


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('s12.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/checklogin', methods=['POST'])
def checklogin():
    try:
        usuario = request.form['usuario']
        password = request.form['password']

        if not usuario:
            flash('Debe ingresar el usuario')
            return render_template('login.html')

        if not password:
            flash('Debe ingresar la contraseña')
            return render_template('login.html')

        if usuario == 'admin' and password == 'admin123':
            return redirect('datos')
        else:
            flash('Usuario o contraseña inválidos.')
            return render_template('login.html')
    except:
        flash('Error interno')
        return render_template('login.html')
    

@app.route('/datos')
def datos():
    print(listadatos)
    #return jsonify({'datos':listadatos})
    return render_template('datos.html', titulo='Datos', datosjson=json.dumps(listadatos))

@app.route('/datos/<string:nom_usuario>')
def datos_bus(nom_usuario):
    resultado = [usr for usr in listadatos if usr["usuario"]==nom_usuario]
    return render_template('datos.html', titulo='Resultado', datosjson=json.dumps(resultado))

@app.route('/registro')
def registro():
    form=Registro()
    return render_template('registro.html',titulo="Registrarse", form=form)

@app.route('/register',methods=('GET','POST'))
def register():
    try:
        print(request.method)
        if request.method == 'POST':
            print('Post')
            username = request.form['usuario']
            password = request.form['password']
            email = request.form['email']
            
        else:
            print('Get')
            username = request.args.get('usuario')
            password = request.args.get('password')
            email = request.args.get('email')
        
        error = None

        if not utils.isUsernameValid(username):
            error = "El usuario debe ser alfanumérico o incluir . , _ - y debe ser de al menos 8 carateres"            
            flash(error)
            return render_template("s12.html")
        
        if not utils.isPasswordValid(password):
            error = "La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres"            
            flash(error)
            return render_template("s12.html")

        if not utils.isEmailValid(email):
            error = "Correo inválido"            
            flash(error)
            return render_template("s12.html")
        
        yag = yagmail.SMTP('misionticgrupo9@gmail.com','Holamundo1')
        yag.send(to=email, subject='Activa tu cuenta', 
                    contents='Bienvenido, usa este vínculo para activar tu cuenta ('+request.method+')')
        flash('Revisa tu correo para activar tu cuenta')
        return render_template('login.html')
    except:
        return render_template('s12.html')
        #flash('Ocurrió un error al enviar el correo')

if __name__ == '__main__':
    app.run(debug=True, port=80)
