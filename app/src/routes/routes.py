from flask import current_app as app
from flask import render_template, redirect, flash
from flask import request
import re, py_compile, shutil

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
            shutil.copy(app.config['UPLOAD_FOLDER'] + 'Clases_viejo.py', app.config['UPLOAD_FOLDER'] + 'Clases_viejo_viejo.py')
            shutil.copy(app.config['UPLOAD_FOLDER'] + 'Clases.py', app.config['UPLOAD_FOLDER'] + 'Clases_viejo.py')
            file.save(app.config['UPLOAD_FOLDER'] + 'Clases.py')
            file.close()
        else:
            flash('El archivo seleccionado no es un archivo de python', category='error')
            return redirect('/inicio')
    elif code != '':
        shutil.copy(app.config['UPLOAD_FOLDER'] + 'Clases_viejo.py', app.config['UPLOAD_FOLDER'] + 'Clases_viejo_viejo.py')
        shutil.copy(app.config['UPLOAD_FOLDER'] + 'Clases.py', app.config['UPLOAD_FOLDER'] + 'Clases_viejo.py')
        file = open(app.config['UPLOAD_FOLDER'] + 'Clases.py', 'w', encoding='utf-8')
        file.write(code)
        file.close()
    else:
        flash('Por favor introduzca el código de python', category='error')
        return redirect('/inicio')
    try:
        py_compile.compile(app.config['UPLOAD_FOLDER'] + 'Clases.py', doraise=True)
        old_file = open(app.config['UPLOAD_FOLDER'] + 'Clases_viejo.py')
        old_code = old_file.read()
        old_file.close()
        if old_code == '':
            shutil.copy(app.config['UPLOAD_FOLDER'] + 'Clases.py', app.config['UPLOAD_FOLDER'] + 'Clases_viejo.py')
        flash('El código ha sido guardado correctamente', category='success')
        return redirect('/inicio')
    except py_compile.PyCompileError as e:
        shutil.copy(app.config['UPLOAD_FOLDER'] + 'Clases_viejo.py', app.config['UPLOAD_FOLDER'] + 'Clases.py')
        shutil.copy(app.config['UPLOAD_FOLDER'] + 'Clases_viejo_viejo.py', app.config['UPLOAD_FOLDER'] + 'Clases_viejo.py')
        flash('El código de python contiene errores', category='error')
        return redirect('/inicio')
        
