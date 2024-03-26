import plotly.express as px
from ...utils.metricas.localizacion_impacto import obtener_atributos


fig = px.pie(values =[va,vt],
             nombres = ['vA', 'vT'],
             title = 'Localización de impacto de la modificacion')

fig.show()
