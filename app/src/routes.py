from flask import current_app as app
from flask import render_template, redirect
from flask import request
from .graficador import crear_grafica_test, networkx_to_figure
import re, py_compile

RUTA_ARCHIVO = 'src/uploads/Clases.py'

@app.route('/')
@app.route('/inicio')
def home():
    return render_template('index.html', title='Inicio')

@app.route('/test')
def test():
    grafica = crear_grafica_test()
    fig = networkx_to_figure(grafica)
    html = fig.to_html(full_html = False)
    return render_template('test.html', fig = html)

@app.route('/LIM')
def lim():
    #Aquí va Wendy
    return render_template('lim.html', title='LIM')

@app.route('/guardar', methods=['POST'])
def guardar():
    code = request.form['textareacode']
    file = request.files['classfile']
    if file.filename != '':
        if re.match('^.*\.py$', file.filename) != None:
            file.save(RUTA_ARCHIVO)
        else:
            #TODO alerta no es achivo .py
            return redirect('/inicio')
    elif code != '':
        file = open(RUTA_ARCHIVO, 'w')
        file.write(code)
        file.close()
    else:
        #TODO alerta introducir algo
        return redirect('/inicio')
    try:
        py_compile.compile(RUTA_ARCHIVO, doraise=True)
    except:
        #TODO alerta error de sintaxis
        return redirect('/inicio')
    return redirect('/LIM')

@app.route('/McCabe')
def mccabe():
    #Aquí va Luis
    return render_template('mccabe.html', title='Complejidad ciclomática')