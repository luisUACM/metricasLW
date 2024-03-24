import ast, numpy as np

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
    eliminar_metodos_acceso(metodos)    #TODO
    for m in metodos:
        nodos.append(m)
        nombres_nodos.append(m.name + '()')
        i += 1
    i_atributos = i
    
    #Contar y agregar atributos
    agregar_asignaciones_metodos(asignaciones, metodos)      #TODO
    for a in asignaciones:
        atributos = get_variables_asignacion(a)
        for attr in atributos:
            nodos.append(attr)
            nombres_nodos.append(attr)
            i += 1
        atributos = []
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

def eliminar_metodos_acceso(l:list):
    pass

def agregar_asignaciones_metodos(l:list, l2: list):
    pass

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
        ast.NodeVisitor.generic_visit(self, node)
    
    def get_llamadas(self):
        l = self.lista_calls
        self.lista_calls = []
        return l
    
    def get_accesos(self):
        l = self.lista_accesos
        self.lista_accesos = []
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

def get_variables_asignacion(nodo: ast.AST):
    """
    Parámetros: Un nodo ast.Assign o ast.AnnAssign
    Regresa: Una lista con los nombres de las variables en la operación de asignación
    """
    nombres_variables = []
    if isinstance(nodo, ast.Assign):
        for t in nodo.targets:
            if isinstance(t, ast.Name):
                nombres_variables.append(t.id)
    elif isinstance(nodo, ast.AnnAssign):
        if isinstance(nodo.target, ast.Name):
            nombres_variables.append(nodo.target.id) 
    return nombres_variables