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
    padre = None
    for d in lista_decisiones:
        nombre_padre = get_nombre_decision(d)
        lista_nombres.append(nombre_padre)
        (i, padre) = agregar_decision(d, grafica, padre)

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

def agregar_decision(decision: ast.AST, grafica: nx.Graph, padre: str = None) -> tuple[list, str]:
    """
    Parámetros: La decisión ast para agregar, la gráfica networkx en donde agregarla y el nombre del nodo padre (en la gráfica) si es que tiene uno
    Regresa: Una tupla con la lista de nodos que no han sido conectados con el final y el nodo que continua con el flujo del programa despues de la decisión.
    Esta es una funcion recursiva que usa esta información de retorno para agregar conexiones a la grafica
    """
    nodos_hoja = []
    nombre_decision = get_nombre_decision(decision)
    camino_else = ''
    camino_feliz = ''
    lista_decisiones_hijas = []
    fin_decision = ''
    nodos_fin = []
    ultimo_nodo = ''
    camino_loop = ''

    #bug 1: Dos nodos directamente del cuerpo del metodo no se conectan. Posiblemente tenga que ver con que los 2 no tienen padre
    #bug 2: Dos while que terminen en la misma linea sse diagraman mal dado que el nodo de fin de ambos tiene el mismo nombre 

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
        fin_decision = str(decision.end_lineno + 1) + ' (Endif)'

        if decision.orelse:
            camino_else = str(decision.orelse[0].lineno) + ' (Else)'
            lista_decisiones_hijas = ma.obtener_decisiones_directas(decision)

            #Paso 3
            grafica.add_edge(nombre_decision, camino_else)

            #Pasos 4, 5 y 6 (Parte del if simple)
            ultimo_nodo = camino_feliz
            if len(lista_decisiones_hijas) != 0:
                for d in lista_decisiones_hijas:
                    (nodos_fin, ultimo_nodo) = agregar_decision(d, grafica, ultimo_nodo)
            else:
                nodos_hoja.append(camino_feliz)
            if padre != None:
                nodos_fin.append(fin_decision)

            #Pasos 4, 5, y 6 (Parte del else)
            ultimo_nodo = camino_else
            lista_decisiones_hijas = ma.obtener_decisiones_directas(decision, True)
            if len(lista_decisiones_hijas) != 0:
                for d in lista_decisiones_hijas:
                    for i, j in agregar_decision(d, grafica, ultimo_nodo):
                        nodos_fin.append(i)
                        ultimo_nodo = j
            else:
                nodos_hoja.append(camino_else)
            for d in nodos_hoja:
                grafica.add_edge(fin_decision, d)
        else:
            camino_else = str(decision.end_lineno + 1) + ' (F)'
            lista_decisiones_hijas = ma.obtener_decisiones_directas(decision)

            #Paso 3
            nodos_hoja.append(camino_else)
            grafica.add_edge(nombre_decision, camino_else)

            #Pasos 4, 5 y 6
            ultimo_nodo = camino_feliz
            if len(lista_decisiones_hijas) != 0:
                for d in lista_decisiones_hijas:
                    (nodos_fin, ultimo_nodo) = agregar_decision(d, grafica, ultimo_nodo)
            else:
                nodos_hoja.append(camino_feliz)
            for d in nodos_hoja:
                grafica.add_edge(fin_decision, d)
            if padre != None:
                nodos_fin.append(fin_decision)

        if padre == None:
            for d in nodos_fin:
                grafica.add_edge(fin_decision, d)

    elif isinstance(decision, ast.For):
        #TODO
        pass
    elif isinstance(decision, ast.While):
        camino_loop = str(decision.end_lineno) + ' (While-loop)'
        camino_feliz = str(decision.lineno + 1) + ' (T)'
        fin_decision = str(decision.end_lineno + 1) + ' (Endwhile)'
        lista_decisiones_hijas = ma.obtener_decisiones_directas(decision)

        #Caminos True y False
        grafica.add_edge(nombre_decision, camino_feliz)
        grafica.add_edge(nombre_decision, fin_decision)

        #Decisiones internas
        ultimo_nodo = camino_feliz
        if len(lista_decisiones_hijas) != 0:
            for d in lista_decisiones_hijas:
                (nodos_fin, ultimo_nodo) = agregar_decision(d, grafica, ultimo_nodo)
            else:
                grafica.add_edge(ultimo_nodo, camino_loop)
                grafica.add_edge(camino_loop, nombre_decision)
        else:
            #Ciclo
            grafica.add_edge(ultimo_nodo, camino_loop)
            grafica.add_edge(camino_loop, nombre_decision)
            nodos_hoja.append(camino_feliz)

       
    elif isinstance(decision, ast.BoolOp):
        #TODO
        pass
        
    if padre != None:
        grafica.add_edge(padre, nombre_decision)

    return (nodos_fin, fin_decision)

def calcular_mccabe(metodo: ast.FunctionDef) -> int:
    """
    Parámetros: El método del cual calcular la complejidad ciclomática
    Regresa: El valor de la complejidad ciclomática
    """
    visitante = ma.VisitanteNodos()
    visitante.visit(metodo)
    lista = visitante.get_decisiones()
    return len(lista) + 1