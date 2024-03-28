from flask import current_app as app
from flask import render_template, redirect, flash
from flask import request
import re, py_compile

RUTA_ARCHIVO = 'src/uploads/Clases.py'

@app.route('/')
@app.route('/inicio')
def home():
    return render_template('index.html', title='Inicio')

@app.route('/guardar', methods=['POST'])
def guardar():
    code = request.form['textareacode']
    file = request.files['classfile']
    if file.filename != '':
        if re.match('^.*\.py$', file.filename) != None:
            file.save(RUTA_ARCHIVO)
        else:
            flash('El archivo seleccionado no es un archivo de python', category='error')
            return redirect('/inicio')
    elif code != '':
        file = open(RUTA_ARCHIVO, 'w')
        file.write(code)
        file.close()
    else:
        flash('Por favor introduzca el código de python', category='info')
        return redirect('/inicio')
    try:
        py_compile.compile(RUTA_ARCHIVO, doraise=True)
    except:
        flash('El código de python contiene errores', category='error')
        return redirect('/inicio')
    return redirect('/LIM')
