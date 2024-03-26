import networkx as nx
import plotly.graph_objects as go
import ast
from ..calculadoras.calculadora_lcom4 import crear_matriz_adyacencia


def crear_grafica_test() -> nx.Graph:
    """
    Regresa: Una gráfica de prueba networkx
    """
    grafica = nx.Graph()

    grafica.add_node('A')
    grafica.add_node('B')
    grafica.add_node('C')
    grafica.add_node('D')

    grafica.add_edge('A', 'B')
    grafica.add_edge('C', 'D')

    pos = nx.spring_layout(grafica)
    nx.set_node_attributes(grafica, pos, 'pos')
    return grafica


def crear_grafo_lcom(clase: ast.ClassDef) -> tuple[str, nx.Graph, int]:
    """
    Parametros: La clase de la que se quiere graficar LCOM4
    Regresa: Un tupla de la forma (nombre_clase, grafica_networkx, valor_lcom)
    """
    matriz, nombres = crear_matriz_adyacencia(clase)
    grafica: nx.Graph = nx.from_numpy_array(matriz)
    dict_nombres = dict()

    i = 0
    for n in nombres:
        dict_nombres[i] = n
        i += 1
    grafica = nx.relabel_nodes(grafica, dict_nombres)

    lcom = nx.number_connected_components(grafica) # LCOM value
    pos = nx.spring_layout(grafica, iterations=25, k= 0.4)
    nx.set_node_attributes(grafica, pos, 'pos')
    return (clase.name, grafica, lcom)

def networkx_to_figure(grafica: nx.Graph, titulo: str = None) -> go.Figure:
    """
    Parametros: Una grafica de redes de networkx, titulo y pie de foto
    Regresa: La misma grafica pero hecha figura de plotly
    """
    edge_x = []
    edge_y = []
    node_x = []
    node_y = []

    for edge in grafica.edges():
        x0, y0 = grafica.nodes[edge[0]]['pos']
        x1, y1 = grafica.nodes[edge[1]]['pos']
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#000'),
        hoverinfo='none',
        mode='lines')
    
    for node in grafica.nodes():
        x, y = grafica.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text = list(grafica.nodes()),
        textposition='bottom center',
        hoverinfo='text',
        marker=dict(size=30, color='skyblue', line_width=1.5))
    
    layout = go.Layout(
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), 
        margin=dict(l=0, r=0, t=0, b=0)
    )
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    if titulo != None:
        fig.update_layout(dict(text = titulo))
    return fig