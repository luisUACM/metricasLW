import plotly.graph_objects as go
from..metricas.metodoss_ponderados import MetodosClaseVisitor
def grafica_lineas():
    # Analizar el archivo y obtener los métodos de cada clase
    with open('archivo_especifico.py', 'r') as file:
        tree = ast.parse(file.read())
        visitor = MetodosClaseVisitor()
        visitor.visit(tree)

        # Calcular la sumatoria de C para cada método
        sumatorias_c = sumatorias_c(visitor)

        # Crear la gráfica de líneas
        fig = go.Figure()
        for clase, metodos in visitor.metodos_por_clase.items():
            x_values = [clase] * len(metodos)
            y_values = [sumatorias_c[clase][metodo] if clase in sumatorias_c and metodo in sumatorias_c[clase] else None for metodo in metodos]
            fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name=clase))

        # Configurar la gráfica
        fig.update_layout(title='Sumatoria de C por método',
                          xaxis_title='Clase',
                          yaxis_title='Sumatoria de C')

        return fig