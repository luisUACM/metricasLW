import networkx as nx
import plotly.graph_objects as go
import ast, numpy as np
from ..metricas import lcom4, complejidad_ciclomatica as cc
from .. import manipulacion_ast as ma

def crear_grafo_lcom(clase: ast.ClassDef) -> tuple[str, nx.Graph, int]:
    """
    Parametros: La clase de la que se quiere graficar LCOM4
    Regresa: Un tupla de la forma (nombre_clase, grafica_networkx, valor_lcom)
    """
    matriz, nombres = lcom4.crear_matriz_adyacencia(clase)
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

def crear_grafos_mccabe(clase: ast.ClassDef) -> list:
    """
    Parámetros: Un nodo ast.ClassDef del cual se quiere crear todos los grafos de complejidad ciclomática
    Regresa: Una lista con todos los grafos networkx
    """
    visitante = ma.VisitanteNodos()
    metodos = [n for n in clase.body if isinstance(n, ast.FunctionDef)]
    lista_graficas = []

    for m in metodos:
        visitante.visit(m)
        lista_decisiones = visitante.get_decisiones()
        if len(lista_decisiones) > 0:
                grafica = graficar_complejidad_ciclomatica(m)
                lista_graficas.append(grafica)
    return lista_graficas

def graficar_complejidad_ciclomatica(metodo: ast.FunctionDef) -> nx.Graph:
    """
    Parámetros: Un nodo que representa método del cual se quiere graficar la complejidad ciclomática
    Regresa: Un grafo que representa el flujo del método
    """
    grafica = nx.Graph()
    visitante = ma.VisitanteNodos()
    lista_decisiones = []
    lista_nombres = []

    visitante.visit(metodo)
    lista_decisiones = visitante.get_decisiones()

    for d in lista_decisiones:
        nombre_padre = get_nombre_decision(d)
        lista_nombres.append(nombre_padre)
        
        if isinstance(d, ast.If):
            agregar_nodos_else(d, grafica)
            """
            for hijo in ast.iter_child_nodes(d):
                nombre_hijo = get_nombre_decision(hijo)
                if nombre_hijo != ' ':
                    print('Se entro al if de:' + nombre_padre + ', ' + nombre_hijo)
                    lista_nombres.append(nombre_hijo)
                    grafica.add_edge(nombre_padre, nombre_hijo)
            """

    pos = nx.planar_layout(grafica)
    nx.set_node_attributes(grafica, pos, 'pos')
    return grafica

def get_nombre_decision(nodo: ast.AST) -> str:
    """
    Parámetros: Un nodo ast que represente una decisión en el código. Si no es un nodo de tipo decision regresa una cadena vacia
    Nodos de decisiones conocidos: ast.If, ast.For, astWhile, ast.BoolOp
    Regresa: Una cadena con el nombre del tipo de nodo
    """
    nombre = ''
    linea = ''
    if isinstance(nodo, ast.If):
        linea = str(nodo.lineno)
        nombre = 'If'
    elif isinstance(nodo, ast.For):
        linea = str(nodo.lineno)
        nombre = 'For'
    elif isinstance(nodo, ast.While):
        linea = str(nodo.lineno)
        nombre = 'While'
    elif isinstance(nodo, ast.BoolOp):
        linea = str(nodo.lineno)
        if isinstance(nodo.op, ast.And):
            nombre = 'and'
        elif isinstance(nodo.op, ast.Or):
            nombre = 'or'
    return nombre + ' ' + linea

def agregar_nodos_else(nodo: ast.AST, grafica: nx.Graph):
    """
    Parámetros: un nodo que puede ser una decision y la gráfica a la que añadirle el nodo
    Para los nodos If e If-else se agregan 2 nodos
    """
    nombre_nodo = get_nombre_decision(nodo)
    
    if isinstance(nodo, ast.If):
        nombre_if = nombre_nodo
        nombre_flujo_if = ''

        if nodo.orelse:
            nombre_else = 'else ' + str(nodo.orelse[0].lineno - 1)
            grafica.add_edge(nombre_if, nombre_else)
        
        nombre_flujo_if = str(nodo.lineno + 1)
        grafica.add_edge(nombre_if, nombre_flujo_if)
        