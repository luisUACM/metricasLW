import ast
import os

class DuplicadosLineasCodigoVisitor(ast.NodeVisitor):
    def __init__(self, ruta_archivo):
        self.lineas_codigo = []
        self.ruta_archivo = ruta_archivo

    def visit_FunctionDef(self, node):
        start_lineno = node.lineno
        end_lineno = node.end_lineno

        with open(self.ruta_archivo, 'r') as file:
            codigo_funcion = "\n".join(ast.get_source_segment(ast.parse(file.read()), start_lineno, end_lineno))
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

# Ruta del archivo a analizar
RUTA_ARCHIVO = os.path.join(os.path.dirname(__file__))

# Analizar el archivo y calcular la densidad de líneas duplicadas
with open(RUTA_ARCHIVO, "r") as file:
    contenido = file.read()
    arbol = ast.parse(contenido)
    duplicados_visitor = DuplicadosLineasCodigoVisitor(RUTA_ARCHIVO)
    duplicados_visitor.visit(arbol)
    densidad_duplicados = calcular_densidad_duplicados(duplicados_visitor.lineas_codigo)

print("Densidad de líneas de código duplicadas:", densidad_duplicados)
