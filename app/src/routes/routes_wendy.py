from flask import current_app as app
from flask import render_template
from..utils.graficadores.graficador_pastel import grafico_pastel
from..utils.graficadores.graficador_lineas import grafica_lineas

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

    # Create a dictionary to store the data for the pie chart
    duplicados_visitor = {
        'Lineas Duplicadas': lineas_duplicadas,
        'Lineas Únicas': lineas_totales - lineas_duplicadas
    }

    # Generate the HTML representation of the plot and append it to the list
   
    plot = grafico_pastel(duplicados_visitor)
    plot_html = plot.to_html(full_html=False)
   

    return render_template('dld.html', title='Densidad de líneas duplicadas', title_long='Densidad de líneas duplicadas', densidad=densidad, descripcion=descripcion, plot_html=plot_html)


RUTA_ARCHIVO = app.config['UPLOAD_FOLDER'] + 'Clases.py'

@app.route('/SumatoriaC')
def sumatoria_c():
    fig = grafica_lineas(RUTA_ARCHIVO)
    descripcion = '''Para calcular la Metodos ponderados de un programa es necesaria la formula
   MP= Σ.c, resuerda que va de i=1 hasta n, donde n es el numero de metodos por clase'''
    plot_html = fig.to_html(full_html=False)

    return render_template('mp.html', title='Sumatoria de C', title_long='Metodos Ponderados', descripcion=descripcion ,plot_html=plot_html)