import ast
from flask import current_app as app
from flask import render_template
from..utils.graficadores.graficador_pastel import grafico_pastel
from..utils.graficadores.graficador_puntos import grafica_puntos
from ..utils.metricas.metodoss_ponderados import MetodosClaseVisitor, calcular_suma_de_c

RUTA_ARCHIVO = app.config['UPLOAD_FOLDER'] + 'Clases.py'

def dld(code):
    lines = [line for line in code.splitlines() if line.strip()]
    unique_lines = set(line for line in lines if line.strip())
    duplicates = [line for line in lines if line.strip() and line in lines and lines.count(line) > 1]
    return len(duplicates)

@app.route('/DensidadLineasDuplicadas')
def densidad_lineas_duplicadas():
    with open(RUTA_ARCHIVO) as file:
        contenido = file.read()
    lineas_totales = len(contenido.splitlines())
    lineas_duplicadas = dld(contenido)
    descripcion = '''Para calcular la Densidad de lineas de un programa es necesaria la formula
    X = Lineas Duplicadas/Lineas totales * 100, aqui mostramos que no toma las lineas en blanco '''

    # Calcula la densidad de líneas de código
    densidad = lineas_duplicadas / lineas_totales * 100

    # Crea un diccionario para almacenar los datos del gráfico circular.
    duplicados_visitor = {
        'Lineas Duplicadas': lineas_duplicadas,
        'Lineas Únicas': lineas_totales - lineas_duplicadas
    }

    # Genera la representación HTML del gráfico y añádala a la lista.
   
    plot = grafico_pastel(duplicados_visitor)
    plot_html = plot.to_html(full_html=False)
   

    return render_template('dld.html', title='Densidad de líneas duplicadas', title_long='Densidad de lineas duplicadas', densidad=densidad, descripcion=descripcion, plot_html=plot_html)


@app.route('/MetodosPonderados')
def sumatorias_c():
    fig = grafica_puntos(RUTA_ARCHIVO)
    descripcion = '''Para calcular la Metodos ponderados de un programa es necesaria la formula
   MP= Σ.c, resuerda que va de i=1 hasta n, donde n es el numero de metodos por clase'''
    
   #Parsea el codigo fuente de python en un ast
    with open(RUTA_ARCHIVO,'r') as file:
        codigo_fuente = file.read()
    tree = ast.parse(codigo_fuente)
    modulos_clase = {}
    calcular_suma_de_c(tree, modulos_clase)
   
    #convierte el grafico a html
    plot_html = fig.to_html(full_html=False)

    return render_template('mp.html', title='Metodos Ponderados', title_long='Metodos Ponderados', modulos_clase=modulos_clase, descripcion=descripcion ,plot_html=plot_html)