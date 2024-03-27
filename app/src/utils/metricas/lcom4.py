import re, ast, numpy as np

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
    visitante = VisitanteNodos()
    repetido = False
    for a in asignaciones:
        lista = get_variables_asignacion(a)
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
    visitante = VisitanteNodos()
    lista_llamadas = []
    lista_accesos = []

    if v1 == None:    # Se buscan llamadas de f1 o f2
        visitante.visit(f1)
        lista_llamadas = visitante.get_llamadas()
        if busca_llamadas(lista_llamadas, f2):
            return True
        else:
            visitante.visit(f2)
            lista_llamadas = visitante.get_llamadas()
            return busca_llamadas(lista_llamadas, f1)
    else:               # Se buscan accesos de f1 a v1
        visitante.visit(f1)
        lista_accesos = visitante.get_accesos()
        return busca_accesos(lista_accesos, v1)
    
class VisitanteNodos(ast.NodeVisitor):
    def __init__(self) -> None:
        self.lista_calls = []
        self.lista_accesos = []
        self.lista_atributos = []
        super().__init__()

    def visit_Call(self,node):
        self.lista_calls.append(node)
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_Assign(self,node):
        self.lista_accesos.append(node)
        ast.NodeVisitor.generic_visit(self, node)
        
    def visit_AnnAssign(self,node):
        self.lista_accesos.append(node)
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_AugAssign(self,node):
        self.lista_accesos.append(node)
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_Attribute(self,node):
        self.lista_accesos.append(node)
        self.lista_atributos.append(node)
        ast.NodeVisitor.generic_visit(self, node)
    
    def get_llamadas(self):
        l = self.lista_calls
        self.lista_calls = []
        return l
    
    def get_accesos(self):
        l = self.lista_accesos
        self.lista_accesos = []
        return l
    
    def get_self_accesos(self):
        l = self.lista_atributos
        self.lista_atributos = []
        return l

def busca_llamadas(lista_llamadas: list, funcion: ast.FunctionDef) -> bool:
    """
    Parámetros: Una lista de objetos ast.Call y la funcion que se está buscando
    Regresa: True si alguna de las llamadas es la funcion pasada por parametro, de lo contrario False
    """
    for n in lista_llamadas:
        if isinstance(n, ast.Call):
            if isinstance(n.func, ast.Name):
                if n.func.id == funcion.name:
                    return True
            elif isinstance(n.func, ast.Attribute):
                if isinstance(n.func.value, ast.Name):
                    if n.func.attr == funcion.name:
                        return True
    return False

def busca_accesos(lista_accesos: list, nombre_variable: str) -> bool:
    """
    Parámetros: Una lista de objetos ast.AST que pudieran ser accesos a un atributo y el nombre de la variable que se está buscando
    Formas conocidas de acceder a una variable en un método: ast.AnnAssign, ast.Assign, ast.AugAssign, ast.Attribute
    Regresa: True si alguna de los accesos es la variable buscada, de lo contrario False
    """
    for n in lista_accesos:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Attribute):
                    if isinstance(t.value, ast.Name):
                        if t.value.id == 'self' and t.attr == nombre_variable:
                            return True
        elif isinstance(n, ast.AnnAssign):
            if isinstance(n.target, ast.Attribute):
                if isinstance(n.target.value, ast.Name):
                    if n.target.value.id == 'self' and n.target.attr == nombre_variable:
                        return True
        elif isinstance(n, ast.AugAssign):
            if isinstance(n.target, ast.Attribute):
                if isinstance(n.target.value, ast.Name):
                    if n.target.value.id == 'self' and n.target.attr == nombre_variable:
                        return True
        elif isinstance(n, ast.Attribute):
            if isinstance(n.value, ast.Name):
                if n.value.id == 'self' and n.attr == nombre_variable:
                    return True
    return False

def print_node(nodo: ast.AST):
    """
    Imprime el arbol de sintaxis abstracta de un nodo AST
    """
    print(ast.dump(ast.parse(nodo), indent=2))

def get_variables_asignacion(nodo: ast.AST, solo_self: bool = False):
    """
    Parámetros: Un nodo ast.Assign o ast.AnnAssign
    Regresa: Una lista con los nombres de las variables en la operación de asignación
    """
    nombres_variables = []
    nombres_variables_self = []

    if isinstance(nodo, ast.Assign):
        for t in nodo.targets:
            if isinstance(t, ast.Name):                 #No self
                nombres_variables.append(t.id)
            elif isinstance(t, ast.Attribute):          #Self
                if isinstance(t.value, ast.Name):
                    if t.value.id == 'self':
                        nombres_variables.append(t.attr)
                        nombres_variables_self.append(t.attr)
    elif isinstance(nodo, ast.AnnAssign):
        if isinstance(nodo.target, ast.Name):           #No self
            nombres_variables.append(nodo.target.id)
        elif isinstance(nodo.target, ast.Attribute):    #Self
            if isinstance(nodo.target.value, ast.Name):
                if nodo.target.value.id == 'self':
                    nombres_variables.append(nodo.target.attr)
                    nombres_variables_self.append(nodo.target.attr)
    elif isinstance(nodo, ast.AugAssign):
        if isinstance(nodo.target, ast.Name):           #No self
            nombres_variables.append(nodo.target.id)
        elif isinstance(nodo.target, ast.Attribute):      #Self
            if isinstance(nodo.target.value, ast.Name):
                if nodo.target.value.id == 'self':
                    nombres_variables.append(nodo.target.attr)
                    nombres_variables_self.append(nodo.target.attr)

    if solo_self:
        return nombres_variables_self
    else:
        return nombres_variables