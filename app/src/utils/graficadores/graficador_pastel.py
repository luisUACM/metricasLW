import plotly.express as px
from ..metricas import densidad_lineas_duplicadas as dld

def grafico_pastel(total_lineas,lineas_duplicadas ):
    fig = px.pie(values =[total_lineas,lineas_duplicadas],
             nombres = ['TL', 'LD'],
             title = 'Densidad de lineas duplicadas')

    fig.show()