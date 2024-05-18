from flask import current_app as app
from flask import render_template, redirect, flash
from flask import request
import re, py_compile, shutil
from ..utils.metricas.puntos_funcion import calcular_vfa, calcular_pf, calcular_pfa, determinar_constantes_duracion,determinar_constantes_esfuerzo

descripcion_pf = '''La Calculadora de Puntos de función es un asistente para el método de estimación de costos 
mediante Puntos de Funcion Ajustados.

Pasos para utilizar la calculadora:\n
    <b>1-.</b> Ingresar la cantidad de ILF, EIF, EI, EO y EQ indicando cuantos hay de cada una de las 
        complejidades (Baja, Media o Alta).\n
    <b>2-.</b> Evaluar cada uno de los 14 atributos de ajuste con una puntuación de 0-5 según sea su 
        importancia en el sistema.\n
    <b>3-.</b> Especificar al menos 1 de las características del proyecto como lenguajes de programación,
        modalidad de desarrollo o plataforma de desarrollo.
        Para más información sobre las caracterísicas del proyecto visita la segunda página de 
        este <a href="https://isbsg.org/wp-content/uploads/2017/05/e.-ISBSG-Release-2017-R1-Field-Descriptions.pdf">documento.</a>

Tras ingresar toda la información necesaria, la calculadora obtendrá todos los datos de 
estimación utilizando el método de Análisis de Puntos de Función.
'''

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

@app.route('/PuntosFuncion')
def calculadora():
    return render_template('base_pf.html', 
                           title='Calculadora PF', 
                           title_long='Calculadora de Puntos de Función', 
                           descripcion=descripcion_pf)

@app.route('/Estimaciones', methods=['POST'])
def estimaciones():
    vfa = calcular_vfa()
    pfa = calcular_pfa()
    pf = calcular_pf()
    tupla_esfuerzo = determinar_constantes_esfuerzo()
    tupla_duracion = determinar_constantes_duracion()
    return render_template('estimaciones.html', 
                           title='Estimaciones PF', 
                           title_long='Estimaciones mediante Análisis de Puntos de Función', 
                           descripcion=descripcion_pf,
                           pf=pf,
                           vfa=vfa,
                           pfa=pfa,
                           c_esfuerzo=tupla_esfuerzo[0],
                           e_esfuerzo=tupla_esfuerzo[1],
                           c_duracion=tupla_duracion[0],
                           e_duracion=tupla_duracion[1])