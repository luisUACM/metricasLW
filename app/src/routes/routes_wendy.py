from flask import current_app as app
from flask import render_template
from ..utils.graficadores.graficador_pastel import grafico_pastel

RUTA_ARCHIVO = app.config['UPLOAD_FOLDER'] + 'Clases.py'

def dld(code):

    lines = code.splitlines()
    unique_lines = set()
    duplicates =[]

    for line in lines:
        if line in unique_lines:
            duplicates.append(line)
        else:
            unique_lines.add(line)
    return len(duplicates)


@app.route('/DensidadLineasDuplicadas')
def densidad_lineas_duplicadas():
    with open(RUTA_ARCHIVO) as file:
        contenido = file.read()
    lineas_totales = len(contenido.splitlines())
    lineas_duplicadas = dld(contenido)

    # Calcula la densidad de líneas de código
    densidad = lineas_duplicadas / lineas_totales * 100

    grafico_pastel(lineas_totales, lineas_duplicadas)

    return render_template('dld.html', title='Densidad de líneas duplicadas', title_long='Densidad de líneas duplicadas', densidad=densidad)