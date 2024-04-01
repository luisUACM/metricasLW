from flask import current_app as app
from flask import render_template
from ..utils.graficadores.graficador_pastel import grafico_pastel

RUTA_ARCHIVO = app.config['UPLOAD_FOLDER'] + 'Clases.py'

def dld(code):

    lines = [line for line in code.splitlines() if line.strip()]
    unique_lines = set(line for line in lines if line.strip())
    duplicates =[line for line in lines if line.strip() and line in lines and lines.count(line) > 1]
    return len(duplicates)

# Inicializa una lista vacía para almacenar los gráficos.


@app.route('/DensidadLineasDuplicadas')
def densidad_lineas_duplicadas():
    with open(RUTA_ARCHIVO) as file:
        contenido = file.read()
    lineas_totales = len(contenido.splitlines())
    lineas_duplicadas = dld(contenido)

    # Calcula la densidad de líneas de código
    densidad = lineas_duplicadas / lineas_totales * 100

    # Generate the HTML representation of the plot and append it to the list
    plot = grafico_pastel(lineas_totales, lineas_duplicadas).to_html(full_html=False)

    return render_template('dld.html', title='Densidad de líneas duplicadas', title_long='Densidad de líneas duplicadas', densidad=densidad, plot=plot)