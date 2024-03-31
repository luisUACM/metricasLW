import plotly.graph_objects as go
from ..metricas import densidad_lineas_duplicadas as dld

def grafico_pastel(total_lineas,lineas_duplicadas ):
    fig = go.Figure(data=[go.Pie(labels=['TL', 'LD'],
            values=[total_lineas, lineas_duplicadas],
            title='Densidad de líneas duplicadas')])

    return fig