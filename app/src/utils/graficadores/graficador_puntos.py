import ast
from ..metricas.metodoss_ponderados import MetodosClaseVisitor
import plotly.graph_objects as go

def grafica_puntos(route):
    # Analizar el archivo y obtener los métodos de cada clase
    with open(route, 'r') as file:
        tree = ast.parse(file.read())
        visitor = MetodosClaseVisitor()
        visitor.visit(tree)

        # Crear la gráfica de puntos
        fig = go.Figure()
        for clase_index, clase_metodos in enumerate(visitor.metodos):
            x_values = [clase_index] * len(clase_metodos)
            y_values = [visitor.suma_c[clase_index][metodo] if clase_index in visitor.suma_c and metodo in visitor.suma_c[clase_index] else None for metodo in clase_metodos]
            fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name=clase_index))

            # Configurar la gráfica
            fig.update_layout(xaxis_title='Clase',
                              yaxis_title='Sumatoria de C')

        return fig
