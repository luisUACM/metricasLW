import re, ast, numpy as np
from .. import manipulacion_ast as ma

def crear_matriz_adyacencia(clase: ast.ClassDef) -> tuple[np.array, list[str]]:
    """
    Parametros: La clase de la que se quiere sacar la matriz de adyacencia segun LCOM4
    Regresa: Una tupla de la forma (matriz, lista_nombres_nodos)
    """
    metodos = [n for n in clase.body if isinstance(n, ast.FunctionDef)]
    asignaciones = [n for n in clase.body if isinstance(n, ast.AnnAssign) or isinstance(n,ast.Assign)]
    nodos = []
    nombres_nodos = []
    atributos = []
    i = 0
    i_atributos = 0

    #Contar y agregar métodos
    metodo_innit = eliminar_metodos_acceso(metodos)
    for m in metodos:
        nodos.append(m)
        nombres_nodos.append(m.name + '()')
        i += 1
    i_atributos = i
    
    #Contar y agregar atributos
    atributos = get_all_atributos(asignaciones, metodos, init = metodo_innit)
    for attr in atributos:
        nodos.append(attr)
        nombres_nodos.append(attr)
        i += 1
    matriz_adjacencia = np.zeros((i,i))

    #Procesar métodos
    for col in range(0, i_atributos):
        for fila in range(col + 1, i_atributos):
            if adyacencia_nodos(f1=nodos[col], f2=nodos[fila]):
                matriz_adjacencia[col][fila] = 1
                matriz_adjacencia[fila][col] = 1

    #Procesar atributos
    for col in range(0, i_atributos):
        for fila in range(i_atributos, len(matriz_adjacencia)):
            if adyacencia_nodos(f1=nodos[col], v1=nodos[fila]):
                matriz_adjacencia[col][fila] = 1
                matriz_adjacencia[fila][col] = 1
    return (matriz_adjacencia, nombres_nodos)

def get_all_atributos(asignaciones:list, metodos: list, init: ast.FunctionDef = None) -> list:
    """
    Parámetros: 
    asignaciones -> lista de objetos ast.Assgin y ast.AnnAssign con los atributos declarados fuera de métodos
    metodos -> lista de métodos de la clase
    init -> método constructor de la clase (Opcional)
    Regresa: 
    Una lista con todos los atributos de una clase
    """
    lista_atributos = []
    lista_nuevos_atributos = []
    visitante = ma.VisitanteNodos()
    repetido = False
    for a in asignaciones:
        lista = ma.get_variables_asignacion(a)
        for l in lista:
            lista_atributos.append(l)

    if init != None:
        metodos.append(init)
    for m in metodos:
        visitante.visit(m)
        lista_nuevos_atributos = visitante.get_self_accesos()
        for a in lista_nuevos_atributos:
            if isinstance(a, ast.Attribute):
                if isinstance(a.value, ast.Name):
                    if a.value.id == 'self':

                        for m2 in metodos:
                            if isinstance (m2, ast.FunctionDef):
                                if m2.name == a.attr:
                                    repetido = True
                                    break
                        for a2 in lista_atributos:
                           
                            if a2 == a.attr:
                                repetido = True
                                break
                        if not repetido:
                            lista_atributos.append(a.attr)
            repetido = False
    if init != None:
        metodos.remove(init)
    return lista_atributos

def eliminar_metodos_acceso(metodos: list) -> ast.FunctionDef:
    """
    Parámetros: La lista de todos los métodos de una clase
    Se eliminarán todos loss métodos getters, setters junto con el método __init_
    """
    metodo_init = None
    lista_borrar = []
    for m in metodos:
        if isinstance(m, ast.FunctionDef):
            if m.name == '__init__':
                metodo_init = m
                lista_borrar.append(m)
            elif re.match('^(get_.*|set_.*)', m.name):
                lista_borrar.append(m)
            else:
                for d in m.decorator_list:
                    if isinstance(d, ast.Name):
                        if d.id == 'property':              #Getter
                            lista_borrar.append(m)
                    elif isinstance(d, ast.Attribute):
                        if d.attr == 'setter':              #Setter
                            lista_borrar.append(m)
    for m in lista_borrar:
        metodos.remove(m)
    return metodo_init

def adyacencia_nodos(f1: ast.FunctionDef, f2: ast.FunctionDef = None, v1: str = None) -> bool:
    """
    Parametros: Los dos nodos que pueden ser adyacentes, f1 y f2 son nodos de funciones, v1 es el nombre de una variable.
    Si v1 no es pasado por parametro se buscarán llamadas mutuas de f2 y f1. De lo contrario se buscaran en f1 que acceda a v1.
    Regresa: Verdadero si uno de los nodos f1 o f2 llama a otro o si los dos acceden a v1 
    """
    visitante = ma.VisitanteNodos()
    lista_llamadas = []
    lista_accesos = []

    if v1 == None:    # Se buscan llamadas de f1 o f2
        visitante.visit(f1)
        lista_llamadas = visitante.get_llamadas()
        if ma.busca_funcion(lista_llamadas, f2):
            return True
        else:
            visitante.visit(f2)
            lista_llamadas = visitante.get_llamadas()
            return ma.busca_funcion(lista_llamadas, f1)
    else:               # Se buscan accesos de f1 a v1
        visitante.visit(f1)
        lista_accesos = visitante.get_accesos()
        return ma.busca_variable(lista_accesos, v1)



