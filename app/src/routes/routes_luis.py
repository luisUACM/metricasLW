from flask import current_app as app
from flask import render_template
from ..utils.graficadores.graficador_grafos import crear_grafo_lcom, networkx_to_figure, crear_grafos_mccabe
import ast
from ..utils import manipulacion_ast as ma

RUTA_ARCHIVO = app.config['UPLOAD_FOLDER'] + 'Clases.py'

@app.route('/LCOM4')
def lcom():
    file = open(RUTA_ARCHIVO)
    contenido = ast.parse(file.read())
    clases = [n for n in contenido.body if isinstance(n, ast.ClassDef)]
    graficas = []
    descripcion = '''El valor de LCOM representa la cantidad de responsabilidades que posee una clase.\n
<b>Cómo calcular:</b>
    - Realizar un grafo con los métodos y atributos de una clase como nodos.
    - Un método se relaciona con otro si uno es llamado por el otro
    - Un método se relaciona con un atributo si este accede a él
    - Contando los componentes conectados del grafo se obtiene LCOM4.\n
Cada clase debe tener una y sólo una repsonsabilidad. Para clases con valor de LCOM 
mayor a 1 es recomendable dividir las clases segun los compenentes que se relacionan.
    '''

    file.close()
    for c in clases:
        n, g, v = crear_grafo_lcom(c)
        fig = networkx_to_figure(g)
        graficas.append((n, fig.to_html(full_html = False), v))
    return render_template('lcom4.html', title='LCOM 4', graficas = graficas, title_long = 'Lack of Cohesion of Methods 4', descripcion = descripcion)

@app.route('/McCabe')
def mccabe():
    file = open(RUTA_ARCHIVO)
    contenido = ast.parse(file.read())
    clases = [n for n in contenido.body if isinstance(n, ast.ClassDef)]
    graficas_metodo = []
    figuras_metodo = []
    figuras_clase = []

    file.close()
    for c in clases:
        graficas_metodo = crear_grafos_mccabe(c)
        for g in graficas_metodo:
            fig = networkx_to_figure(g)
            figuras_metodo.append(fig.to_html(full_html = False))
        figuras_clase.append(figuras_metodo)
        figuras_metodo = []
    return render_template('mccabe.html', title='McCabe', title_long='Complejidad cicolmática', graficas=figuras_clase)