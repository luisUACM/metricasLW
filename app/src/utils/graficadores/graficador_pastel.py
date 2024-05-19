import plotly.graph_objects as go
from..metricas import densidad_lineas_duplicadas as dld

def grafico_pastel(duplicados_visitor):
    # Crea una figura con subtramas para cada clase.
    fig = go.Figure()

    # Extraer los datos del diccionario.
    lineas_duplicadas = duplicados_visitor['Lineas Duplicadas']
    lineas_unicas = duplicados_visitor['Lineas Únicas']

    # Crea el grafico circular
    fig.add_trace(go.Pie(labels=['Lineas Duplicadas', 'Lineas Únicas'],
                         values=[lineas_duplicadas, lineas_unicas]))

    fig.update_layout(title_text="Densidad de lineas duplicadas",
                       height=700, width=700)

    return fig