from flask import current_app as app
from flask import render_template, redirect, flash
from flask import request
from jinja2 import Template
import re, py_compile, shutil
from ..utils.metricas.puntos_funcion import CalculadoraPF

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
    descripcion = '''La Calculadora de Puntos de función es un asistente para el método de estimación de
costos mediante Puntos de Funcion Ajustados.

Pasos para utilizar la calculadora:\n
    <b>1-.</b> Ingresar la cantidad de ILF, EIF, EI, EO y EQ indicando cuantos hay de cada una de
        las complejidades (Baja, Media o Alta). Para más información sobre como calcular 
        las complejidades puedes visitar este <a href="https://www.infor.uva.es/~manso/calidad/PFA-CLM-2011">documento</a> (pag. 15).\n
    <b>2-.</b> Evaluar cada uno de los 14 atributos de ajuste con una puntuación de 0-5 según
        sea su importancia en el sistema. Para más información sobre como evaluar cada 
        factor puedes visitar este <a href="https://bibliotecadigital.usb.edu.co/server/api/core/bitstreams/c814e3a5-f9aa-4e3d-8484-3719ad4b742e/content">documento</a> (pags. 58-65).\n
    <b>3-.</b> Especificar al menos 1 de las características del proyecto:
            ■ Plataforma de desarrollo: PC, MidRange, MainFrame o multiplataforma.
            ■ Lenguajes de programación: de 3ra generación, de 4ta generación o 
                aplicación general.
            ■ Modalidad de desarrollo: Nuevo desarrollo o mantenimiento.

Tras ingresar toda la información necesaria, la calculadora obtendrá todos los datos de 
estimación utilizando el método de Análisis de Puntos de Función.
'''
    return render_template('base_pf.html', 
                           title='Calculadora PF', 
                           title_long='Calculadora de Puntos de Función', 
                           descripcion=descripcion)

@app.route('/Estimaciones', methods=['POST'])
def estimaciones():
    pfsa = calcular_pfsa()
    if pfsa <= 0:
        flash('Se debe ingresar al menos 1 componente y su complejidad', category='error1')
        return redirect('/PuntosFuncion')
    
    caracteristicas = obtener_caracteristicas()
    if caracteristicas == '':
        flash('Se debe seleccionar al menos un atributo del proyecto', category='error2')
        return redirect('/PuntosFuncion')
    
    descripcion = renderizar_descripcion_estimaciones1()
    gsc = calcular_gsc()
    calculadora = CalculadoraPF(pfsa, gsc, caracteristicas)
    vfa = calculadora.calcular_vfa()
    pf = calculadora.calcular_pfa()
    esfuerzo = calculadora.calcular_esfuerzo()
    duracion = calculadora.calcular_duracion()
    return render_template('estimaciones.html', 
                           title='Estimaciones', 
                           title_long='Estimaciones mediante Análisis de Puntos de Función', 
                           descripcion=descripcion,
                           vfa=vfa,
                           pf=pf,
                           esfuerzo=esfuerzo,
                           duracion=duracion)

def renderizar_descripcion_estimaciones1():
    descripcion_string = '''Fórmulas para las estimaciones con Puntos de Función:

    ■ VFA = 0.65 + 0.01 * sumatoria_GSC\n
    ■ PF = PFsA * VFA\n
    ■ Esfuerzo = C_esfuerzo * PF ^ E_esfuerzo\n
    ■ Duración = C_duración * PF ^ E_duración\n
    ■ Personal = Esfuerzo / (Duración * 20 * 8)\n

    Donde:

    - sumatoria_GSC es la sumatoria de las puntuaciones de las características generales del sistema = {{ gsc }}
    - VFA es factor de ajuste = {{ vfa }}
    - PFsA son los puntos de función sin ajustar = {{ pfsa }}
    - PF son los puntos de función ajustados = {{ pf }}
    - C_esfuerzo es una constante derivada de las caracteristicas del sistema = {{ c_esfuerzo }}
    - E_esfuerzo es una constante derivada de las caracteristicas del sistema = {{ e_esfuerzo }}
    - C_duración es una constante derivada de las caracteristicas del sistema = {{ c_duracion }}
    - E_duración es una constante derivada de las caracteristicas del sistema = {{ c_duracion }}

'''
    calculadora = CalculadoraPF(calcular_pfsa(), calcular_gsc(), obtener_caracteristicas())
    descripcion_template = Template(descripcion_string)
    gsc = calcular_gsc()
    vfa = calculadora.calcular_vfa()
    pfsa = calcular_pfsa()
    pf = calculadora.calcular_pfa()
    tupla_esfuerzo = calculadora.get_constantes_esfuerzo()
    tupla_duracion = calculadora.get_constantes_duracion()
    descripcion = descripcion_template.render(
        gsc=gsc,
        vfa=vfa,
        pfsa=pfsa,
        pf=pf,
        c_esfuerzo=tupla_esfuerzo[0],
        e_esfuerzo=tupla_esfuerzo[1],
        c_duracion=tupla_duracion[0],
        e_duracion=tupla_duracion[1]
    )
    return descripcion

def calcular_pfsa() -> int:
    """
    Regresa: El total de puntos de función sin ajustar según fueron ingresados en el formulario de complejidades.
    """
    return 0

def calcular_gsc() -> int:
    """
    Regresa: El factor de ajuste ingresado en el formulario de atributos de ajuste.
    """
    gsc = 0
    att = 'att'
    for i in range(1,14):
        gsc += int(request.form[att + str(i)])
    return gsc

def obtener_caracteristicas() -> str:
    """
    Regresa: Las caracteristicas del sistema en forma de string con el formato: plataforma-lenguaje-modalidad
    """
    plataforma = request.form['plataforma']
    lenguaje = request.form['lenguaje']
    modalidad = request.form['modalidad']
    caracteristicas: str = plataforma
    
    if caracteristicas == '':
        caracteristicas = lenguaje
    elif lenguaje != '':
        caracteristicas += '-' + lenguaje
    if caracteristicas == '':
        caracteristicas = modalidad
    elif modalidad != '':
        caracteristicas += '-' + modalidad

    return caracteristicas