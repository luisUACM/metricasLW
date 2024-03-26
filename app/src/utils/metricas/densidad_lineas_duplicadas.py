import ast

class DuplicadosLineasCodigoVisitor(ast.NodeVisitor):
    def __init__(self):
        self.lineas_codigo = []

    def visit_FunctionDef(self, node):
        # Recopilamos las líneas de código dentro de la función
        start_lineno = node.lineno
        end_lineno = node.end_lineno

        #error en el asig esta taratando de accder a un atributo de un objeto asig que no existe y genera el error, esat intenado a acceder a source
        codigo_funcion = "\n".join(ast.get_source_segment(ast.parse(node.body[0].source()), start_lineno, end_lineno))
        self.lineas_codigo.append(codigo_funcion)
        self.generic_visit(node)

# Calcula la métrica de densidad de líneas de código duplicadas
def calcular_densidad_duplicados(lineas_codigo):
    total_lineas = len(lineas_codigo)
    lineas_unicas = set(lineas_codigo)
    lineas_duplicadas = total_lineas - len(lineas_unicas)
    if total_lineas > 0:
        densidad_duplicados = lineas_duplicadas / total_lineas * 100
    else:
        densidad_duplicados = 0
    return densidad_duplicados

# Uso de ejemplo:
codigo_fuente = """
def funcion1():
    x = 1
    y = 2

def funcion2():
    x = 1
    y = 2
"""

arbol = ast.parse(codigo_fuente)
duplicados_visitor = DuplicadosLineasCodigoVisitor()
duplicados_visitor.visit(arbol)
densidad_duplicados = calcular_densidad_duplicados(duplicados_visitor.lineas_codigo)

print("Densidad de líneas de código duplicadas:", densidad_duplicados)
