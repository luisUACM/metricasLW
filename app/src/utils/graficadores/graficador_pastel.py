import plotly.graph_objects as go
from..metricas import densidad_lineas_duplicadas as dld

def grafico_pastel(duplicados_visitor):
    # Create a figure with subplots for each class
    fig = go.Figure()

    # Extract the data from the dictionary
    lineas_duplicadas = duplicados_visitor['Lineas Duplicadas']
    lineas_unicas = duplicados_visitor['Lineas Únicas']

    # Create a pie chart
    fig.add_trace(go.Pie(labels=['Lineas Duplicadas', 'Lineas Únicas'],
                         values=[lineas_duplicadas, lineas_unicas]))

    fig.update_layout(title_text="Densidad de lineas duplicadas",
                       height=700, width=700)

    return fig