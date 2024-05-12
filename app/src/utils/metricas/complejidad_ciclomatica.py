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
    lista_decisiones_compuestas = []
    lista_asignaciones = []

    lista_decisiones = [n for n in metodo.body if isinstance(n, ast.If) or isinstance(n, ast.While) or isinstance(n, ast.For)]
    lista_asignaciones = [n for n in metodo.body if isinstance(n, ast.Assign)]
    lista_decisiones_compuestas = ma.extraer_operaciones_compuestas(lista_asignaciones)
    for d in lista_decisiones_compuestas:
        lista_decisiones.append(d)


    padre = None
    for d in lista_decisiones:
        nombre_padre = get_nombre_decision(d)
        lista_nombres.append(nombre_padre)
        (i, padre) = agregar_decision(d, grafica, padre)

    pos = nx.planar_layout(grafica)
    nx.set_node_attributes(grafica, pos, 'pos')
    return (metodo.name, grafica, 0)

def get_nombre_decision(nodo: ast.If | ast.For | ast.While | ast.BoolOp) -> str:
    """
    Parámetros: Un nodo ast que represente una decisión en el código. Si no es un nodo de tipo decision regresa una cadena vacia
    Regresa: Una cadena con el nombre del tipo de nodo
    """
    nombre = ''
    linea = ''

    if isinstance(nodo, ast.If):
        linea = str(nodo.lineno)
        nombre = 'If'
        return nombre + ' ' + linea
    elif isinstance(nodo, ast.For):
        linea = str(nodo.lineno)
        nombre = 'For'
        return nombre + ' ' + linea
    elif isinstance(nodo, ast.While):
        linea = str(nodo.lineno)
        nombre = 'While'
        return nombre + ' ' + linea
    elif isinstance(nodo, ast.BoolOp):
        linea = str(nodo.lineno)
        lista = obtener_operadores_internos(nodo)
        n = 0
        tipo = ''
        tuplas = []
        i = 0
        n = len(nodo.values) - 1
        if isinstance(nodo.op, ast.And):
            tipo = 'And '
        elif isinstance(nodo.op, ast.Or):
            tipo = 'Or '
        nombre += tipo
        tuplas.append((n, tipo, 0))
        ma.print_node(nodo)
        print(lista)
        for o in lista:
            print(tuplas)
            if isinstance(o, ast.BoolOp):
                if isinstance(o.values[-1], ast.BoolOp):
                    n = len(o.values) - 1
                else:
                    n = len(o.values)
                if isinstance(o.op, ast.And):
                    tipo = 'And '
                elif isinstance(o.op, ast.Or):
                    tipo = 'Or '
                tuplas.append((n, tipo, 0))
            else:
                (n, tipo, i) = tuplas.pop()
                i += 1
                if i <= n:
                    nombre += tipo
                    tuplas.append((n, tipo, i))
                else:
                    nombre += tipo
        return nombre + linea
    

def agregar_decision(decision: ast.AST, grafica: nx.Graph, padre: str = None, bool_op_padre: bool = False) -> tuple[list, str]:
    """
    Parámetros: La decisión ast para agregar, la gráfica networkx en donde agregarla y el nombre del nodo padre (en la gráfica) si es que tiene uno
    Regresa: Una tupla con la lista de nodos que no han sido conectados con el final y el nodo que continua con el flujo del programa despues de la decisión.
    Esta es una funcion recursiva que usa esta información de retorno para agregar conexiones a la grafica
    """
    nodos_hoja: list[str] = []
    nombre_decision = get_nombre_decision(decision)
    camino_else = ''
    camino_feliz = ''
    lista_decisiones_hijas: list[str] = []
    fin_decision = ''
    nodos_fin: list[str] = []
    ultimo_nodo = ''
    camino_loop = ''
    operandos: list[ast.AST] = []
    
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
        fin_decision = str(decision.end_lineno + 1) + ' (End)'

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
            camino_else = str(decision.end_lineno + 1) + ' (F ' + str(decision.lineno) + ')'
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
        if padre != None:
            grafica.add_edge(padre, nombre_decision)

    elif isinstance(decision, ast.While) or isinstance(decision, ast.For):
        camino_loop = str(decision.end_lineno) + ' (Loop' + str(decision.lineno) +')'
        camino_feliz = str(decision.lineno + 1) + ' (T)'
        fin_decision = str(decision.end_lineno + 1) + ' (End ' + str(decision.lineno) +')'
        lista_decisiones_hijas = ma.obtener_decisiones_directas(decision)

        #Caminos True y False
        grafica.add_edge(nombre_decision, camino_feliz)
        grafica.add_edge(nombre_decision, fin_decision)

        #Decisiones internas
        ultimo_nodo = camino_feliz
        if len(lista_decisiones_hijas) != 0:
            for d in lista_decisiones_hijas:
                (nodos_fin, ultimo_nodo) = agregar_decision(d, grafica, ultimo_nodo)
            grafica.add_edge(ultimo_nodo, camino_loop)
            grafica.add_edge(camino_loop, nombre_decision)
        else:
            #Ciclo
            grafica.add_edge(ultimo_nodo, camino_loop)
            grafica.add_edge(camino_loop, nombre_decision)
            nodos_hoja.append(camino_feliz)
    if padre != None:
        grafica.add_edge(padre, nombre_decision)

    elif isinstance(decision, ast.BoolOp):
        fin_decision = str(decision.end_lineno + 1) + ' (' + nombre_decision + ')'
        camino_feliz = 'T ' + nombre_decision
        camino_else = 'F ' + nombre_decision
        i = 1
        if not bool_op_padre:
            grafica.add_edge(nombre_decision, camino_feliz)
            grafica.add_edge(nombre_decision, camino_else)
            if isinstance(decision.op, ast.Or):
                ultimo_nodo = camino_else
                nodos_fin.append(camino_feliz)
            elif isinstance(decision.op, ast.And):
                ultimo_nodo = camino_feliz
                nodos_fin.append(camino_else)

        operandos = obtener_operadores_internos(decision)
        
        if not isinstance(operandos[0], ast.BoolOp):
            operandos = operandos[1:]
        if not isinstance(operandos[-1], ast.BoolOp):
            operandos = operandos[:-1]
        for o in operandos:
            if isinstance(o, ast.BoolOp):
                operandos_internos = o.values
                if not isinstance(operandos_internos[-1], ast.BoolOp):
                    operandos_internos = o.values[:-1]
                for o2 in operandos_internos:
                    operandos.append(o2)
            else:
                camino_feliz = 'T ' + cortar_operador_boleano(nombre_decision, i)
                camino_else = 'F ' + cortar_operador_boleano(nombre_decision, i)
                grafica.add_edge(ultimo_nodo, camino_feliz)
                grafica.add_edge(ultimo_nodo, camino_else)
                if isinstance(decision.op, ast.Or):
                    ultimo_nodo = camino_else
                    nodos_fin.append(camino_feliz)
                elif isinstance(decision.op, ast.And):
                    ultimo_nodo = camino_feliz
                    nodos_fin.append(camino_else)
                i += 1
        if isinstance(decision.op, ast.Or):
            nodos_fin.append(camino_else)
        elif isinstance(decision.op, ast.And):
            nodos_fin.append(camino_feliz)
        if not bool_op_padre:
            for n in nodos_fin:
                grafica.add_edge(fin_decision,n)
        if bool_op_padre:
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

def cortar_operador_boleano(nombre_nodo: str, index: int):
    nombre_cortado = nombre_nodo
    i = 0
    while i < index:
        if nombre_cortado[0] == 'O':
            nombre_cortado = nombre_cortado[3:]
        elif nombre_cortado[0] == 'A':
            nombre_cortado = nombre_cortado[4:]
        i += 1
    return nombre_cortado

def obtener_operadores_internos(operador: ast.BoolOp, lista: list[ast.AST] = None):
    """
    TODO
    """
    operandos_internos = operador.values
    if lista == None:
        lista = []
    if not isinstance(operandos_internos[-1], ast.BoolOp):
        operandos_internos = operandos_internos[:-1]
    for o in operandos_internos:
        lista.append(o)
        if isinstance(o, ast. BoolOp):
            obtener_operadores_internos(o, lista)
    if lista == None:
        operandos_internos.insert(0, operador)
    return lista