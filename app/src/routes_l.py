from flask import current_app as app
from flask import render_template
from .graficador_grafos import crear_grafo_lcom, networkx_to_figure
import ast

RUTA_ARCHIVO = 'src/uploads/Clases.py'

@app.route('/LCOM4')
def lcom():
    file = open(RUTA_ARCHIVO)
    contenido = ast.parse(file.read())
    clases = [n for n in contenido.body if isinstance(n, ast.ClassDef)]
    graficas = []

    file.close()
    for c in clases:
        n, g, v = crear_grafo_lcom(c)
        fig = networkx_to_figure(g)
        graficas.append((n, fig.to_html(full_html = False), v))
    return render_template('lcom4.html', title='LCOM 4', graficas = graficas)