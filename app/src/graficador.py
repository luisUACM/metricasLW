import networkx as nx
import plotly.graph_objects as go

def crear_grafica_test():
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

"""
Parametros: Una grafica de redes de networkx
Regresa: La misma grafica pero hecha figura de plotly
"""
def networkx_to_figure(grafica: nx.Graph):
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
        line=dict(width=0.5, color='#888'),
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
        marker=dict(size=30, color='skyblue', line_width=2))
    
    layout = go.Layout(
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    return fig