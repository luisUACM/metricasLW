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
    complejidad = 0

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
    complejidad = grafica.number_of_edges() - grafica.number_of_nodes() + 2

    pos = nx.planar_layout(grafica)
    nx.set_node_attributes(grafica, pos, 'pos')
    return (metodo.name, grafica, complejidad)

def get_nombre_decision(nodo: ast.If | ast.For | ast.While | ast.BoolOp) -> str:
    """
    Parámetros: Un nodo ast que represente una decisión en el código. Si no es un nodo de tipo decision regresa una cadena vacia
    Regresa: Una cadena con el nombre del tipo de nodo, el el caso de una decision compuesta, regresa la cadena con el nombre de cada desicion individual
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
        tipo = ''
        operadores = obtener_operadores_internos(nodo)

        for op, n in operadores:
            if isinstance(op, ast.And):
                tipo = 'And '
            elif isinstance(op, ast.Or):
                tipo = 'Or '
            nombre += tipo*n
        return nombre + linea
    

def agregar_decision(decision: ast.If | ast.For | ast.While | ast.BoolOp, grafica: nx.Graph, padre: str = None, fin_bool_op: tuple[str, str] = None) -> tuple[list[str], str]:
    """
    Parámetros: La decisión ast para agregar y la gráfica networkx en donde agregarla
    Opcionalmente el nombre del nodo padre (en la gráfica) y una tupla con los 2 nodos fin para el caso de las decisiones compuestas
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
    hojas_true: str = []
    hojas_false: str = []
    
    #               Pasos para procesar If
    #1 - Agregar nodo if
    #2 - Agregar camino 'True', si tiene una condicional copmpuesta (contiene operadores And/Or) agregar el arbol de la condicional
    #3 - Agregar camino 'False'
    #4 - Agregar decisiones internas y procesar las mismas
    #5 - Obtener y conectar la lista de nodos_hoja. Aquellos nodos que no tienen mas decisiones internas
    #6 - Obtener y conectar la lista de nodos_fin. Representan el flujo que continua tras la decision
    if isinstance(decision, ast.If):
        camino_feliz = str(decision.lineno + 1) + ' (T)'
        fin_decision = str(decision.end_lineno + 1) + ' (End)'

        if decision.orelse:
            camino_else = str(decision.orelse[0].lineno) + ' (Else)'
            lista_decisiones_hijas = ma.obtener_decisiones_directas(decision)

            #Paso 1 y 2
            if isinstance(decision.test, ast.BoolOp):
                (nodos_fin, ultimo_nodo) = agregar_decision(decision.test, grafica, nombre_decision, (camino_feliz, camino_else))
                nodos_fin = []
            else:
                grafica.add_edge(nombre_decision, camino_feliz)

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
            
            #Paso 1 y 2
            if isinstance(decision.test, ast.BoolOp):
                (nodos_fin, ultimo_nodo) = agregar_decision(decision.test, grafica, nombre_decision, (camino_feliz, camino_else))
                nodos_fin = []
            else:
                grafica.add_edge(nombre_decision, camino_feliz)

            #Paso 3
            grafica.add_edge(nombre_decision, camino_else)
            nodos_hoja.append(camino_else)

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
        camino_loop = str(decision.end_lineno) + ' (Loop ' + str(decision.lineno) +')'
        camino_feliz = str(decision.lineno + 1) + ' (T)'
        fin_decision = str(decision.end_lineno + 1) + ' (End ' + str(decision.lineno) +')'
        lista_decisiones_hijas = ma.obtener_decisiones_directas(decision)
        
        #Caminos True y False
        if isinstance(decision, ast.While):
            if isinstance(decision.test, ast.BoolOp):
                (nodos_fin, ultimo_nodo) = agregar_decision(decision.test, grafica, nombre_decision, (camino_feliz, fin_decision))
                nodos_fin = []
            else:
                grafica.add_edge(nombre_decision, camino_feliz)
        else:   
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
        ultimo_nodo = nombre_decision
        operandos = obtener_operadores_internos(decision)
        i = j = 0
        op = decision.op

        for op, n in operandos:
            while j < n:
                camino_feliz = 'T ' + cortar_operador_boleano(nombre_decision, i + j)
                camino_else = 'F ' + cortar_operador_boleano(nombre_decision, i + j)
                grafica.add_edge(ultimo_nodo, camino_feliz)
                grafica.add_edge(ultimo_nodo, camino_else)
                if isinstance(op, ast.Or):
                    ultimo_nodo = camino_else
                    nodos_fin.append(camino_feliz)
                elif isinstance(op, ast.And):
                    ultimo_nodo = camino_feliz
                    nodos_fin.append(camino_else)
                j += 1
            i += j
            j = 0
        if isinstance(op, ast.Or):
            nodos_fin.append(camino_else)
        elif isinstance(op, ast.And):
            nodos_fin.append(camino_feliz)

        if fin_bool_op == None:
            for n in nodos_fin:
                grafica.add_edge(n, fin_decision)
        else:
            (hojas_true, hojas_false) = separar_nodos(nodos_fin)
            for n in hojas_true:
                grafica.add_edge(n, fin_bool_op[0])
            for n in hojas_false:
                grafica.add_edge(n, fin_bool_op[1])
                
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

def cortar_operador_boleano(nombre_nodo: str, n: int) -> str:
    """
    Parámetros: El nombre del nodo de operacion boleana y la cantidad de operadores que se quieren recortar del nombre nodo.
    Regresa: El nombre del nodo sin los primeros n operadores.
    """
    nombre_cortado = nombre_nodo
    i = 0
    while i < n:
        if nombre_cortado[0] == 'O':
            nombre_cortado = nombre_cortado[3:]
        elif nombre_cortado[0] == 'A':
            nombre_cortado = nombre_cortado[4:]
        i += 1
    return nombre_cortado

def obtener_operadores_internos(operador: ast.BoolOp, lista_acumulada: list[ast.AST] = None) -> list[tuple[ast.Or | ast.And, int]]:
    """
    Parámetros: Un operador boleano ast y la lista de operadores internos acumulada del operador boleano.
    Regresa: Una lista de tuplas de la forma (tipo_operador, numero_ocurrencias) en el orden en que se ejecutan las operaciones.
    Esta es una funcion recursiva que obtiene todos los operadores ast.And y ast.Or de un nodo ast.BoolOp y sus nodos ast.BoolOp internos.
    """
    operandos_internos = operador.values
    i = 0
    if lista_acumulada == None:
        lista_acumulada = []
        for o in operandos_internos:
            if isinstance(o, ast. BoolOp):
                if i != 0:
                    lista_acumulada.append((operador.op,i))
                    i = 0
                obtener_operadores_internos(o, lista_acumulada)
            i += 1
        i -= 1
        if i != 0:
            lista_acumulada.append((operador.op,i))
    else:
        lista_acumulada.append((operador.op,len(operador.values) - 1))
        for o in operandos_internos:
            if isinstance(o, ast. BoolOp):
                lista_acumulada.append((o.op,len(o.values) - 1))
                obtener_operadores_internos(o, lista_acumulada)
    return lista_acumulada

def separar_nodos(lista: list[str]) -> tuple[list[str],list[str]]:
    """
    Parámetros: Una lista de nombres de nodos hoja de la gráfica de complejidad ciclomnática.
    Regresa: Una tupla que separa los nodos en 2 listas: aquellos nodos de camino True y aquellos de camino False 
    """
    lista_true = []
    lista_false = []
    for s in lista:
        if s[0] == 'T':
            lista_true.append(s)
        elif s[0] == 'F':
            lista_false.append(s)
    return (lista_true, lista_false)