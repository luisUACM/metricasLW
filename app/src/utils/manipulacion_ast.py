import ast

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

def busca_variable(lista_accesos: list, nombre_variable: str) -> bool:
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

def busca_funcion(lista_llamadas: list, funcion: ast.FunctionDef) -> bool:
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