import plotly.express as px
from ...utils.metricas.densidad_lineas_duplicadas import DuplicadosLineasCodigoVisitor


fig = px.pie(values =[total_lineas,lineas_duplicadas],
             nombres = ['TL', 'LD'],
             title = 'Densidad de lineas duplicadas')

fig.show()
