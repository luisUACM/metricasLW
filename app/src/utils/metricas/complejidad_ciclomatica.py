import ast, networkx as nx
from .. import manipulacion_ast as ma

def graficar_complejidad_ciclomatica(metodo: ast.FunctionDef) -> tuple [str, nx.Graph, int]:
    """
    Parámetros: Un nodo que representa método del cual se quiere graficar la complejidad ciclomática
    Regresa: Un grafo que representa el flujo del método
    """
    grafica = nx.Graph()
    lista_decisiones = []
    lista_nombres = []

    lista_decisiones = [n for n in metodo.body if isinstance(n, ast.If) or isinstance(n, ast.While) or isinstance(n, ast.For) or isinstance(n, ast.BoolOp)]
    for d in lista_decisiones:
        nombre_padre = get_nombre_decision(d)
        lista_nombres.append(nombre_padre)
        agregar_decision(d, grafica)

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

def agregar_decision(decision: ast.AST, grafica: nx.Graph, padre: str = None) -> list:
    """
    Parámetros: La decisión ast para agregar, la gráfica networkx en donde agregarla y el nombre del nodo padre (en la gráfica) si es que tiene uno
    Regresa: La lista de nodos que continuan el con flujo del programa despues de la decisión.
    Esta es una funcion recursiva que usa esta información de retorno para agregar conexiones a la grafica
    """
    nodos_hoja = []
    nombre_decision = get_nombre_decision(decision)
    camino_else = ''
    camino_feliz = ''
    lista_decisiones_hijas = []
    fin_decision = ''
    nodos_fin = []

    #               Pasos para procesar If
    #1 - Agregar nodo if
    #2 - Agregar camino 'True'
    #3 - Agregar camino 'False'
    #4 - Agregar decisiones internas y procesar las mismas
    #5 - Obtener y conectar la lista de nodos_hoja. Aquellos nodos que no tienen mas decisiones internas
    #6 - Obtener y conectar la lista de nodos_fin. Representan el flujo que continua tras la decision
    if isinstance(decision, ast.If):

        #Pasos 1 y 2
        camino_feliz = str(decision.lineno + 1) + ' (T)'
        grafica.add_edge(nombre_decision, camino_feliz)
        
        if decision.orelse:
            fin_decision = str(decision.orelse[-1].lineno + 1) + ' (Endif)'
            camino_else = str(decision.orelse[0].lineno) + ' (Else)'
            lista_decisiones_hijas = ma.obtener_decisiones_directas(decision)

            #Paso 3
            grafica.add_edge(nombre_decision, camino_else)

            #Pasos 4, 5 y 6 (Parte del if simple)
            if len(lista_decisiones_hijas) != 0:
                for d in lista_decisiones_hijas:
                    nodos_fin = agregar_decision(d, grafica, camino_feliz)
            else:
                nodos_hoja.append(camino_feliz)
            if padre != None:
                nodos_fin.append(fin_decision)

            #Pasos 4, 5, y 6 (Parte del else)
            lista_decisiones_hijas = ma.obtener_decisiones_directas(decision, True)
            if len(lista_decisiones_hijas) != 0:
                for d in lista_decisiones_hijas:
                    for i in agregar_decision(d, grafica, camino_else):
                        nodos_fin.append(i)
            else:
                nodos_hoja.append(camino_else)
            for d in nodos_hoja:
                grafica.add_edge(fin_decision, d)
        else:
            fin_decision = str(decision.body[-1].end_lineno + 1) + ' (Endif)'
            camino_else = str(decision.end_lineno + 1) + ' (F)'
            lista_decisiones_hijas = ma.obtener_decisiones_directas(decision)

            #Paso 3
            nodos_hoja.append(camino_else)
            grafica.add_edge(nombre_decision, camino_else)

            #Pasos 4, 5 y 6
            if len(lista_decisiones_hijas) != 0:
                for d in lista_decisiones_hijas:
                    nodos_fin = agregar_decision(d, grafica, camino_feliz)
            else:
                nodos_hoja.append(camino_feliz)
            for d in nodos_hoja:
                grafica.add_edge(camino_else, d)
            if padre != None:
                nodos_fin.append(camino_else)

        if padre == None:
            for d in nodos_fin:
                grafica.add_edge(fin_decision, d)

    elif isinstance(decision, ast.For):
        #TODO
        pass
    elif isinstance(decision, ast.While):
        #TODO
        pass
    elif isinstance(decision, ast.BoolOp):
        #TODO
        pass
        
    if padre != None:
        grafica.add_edge(padre, nombre_decision)

    return nodos_fin

