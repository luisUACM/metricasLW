from flask import current_app as app
from flask import render_template
from ..utils.graficadores.graficador_pastel import grafico_pastel

RUTA_ARCHIVO = app.config['UPLOAD_FOLDER'] + 'Clases.py'

@app.route('/DensidadLineasDuplicadas')
def densidad_lineas_duplicadas():
    file = open(RUTA_ARCHIVO)
    contenido = file.read()
    lineas_totales = len(contenido.splitlines())
    lineas_duplicadas = dld(contenido)
    file.close()

    grafico_pastel(lineas_totales, lineas_duplicadas)



    return render_template('densidad_lineas_duplicadas.html', title='Densidad de líneas duplicadas', title_long='Densidad de líneas duplicadas')