import ast, networkx as nx
from .. import manipulacion_ast as ma

def graficar_complejidad_ciclomatica(metodo: ast.FunctionDef) -> tuple [str, nx.Graph, int]:
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
    return (metodo.name, grafica, 0)

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
        