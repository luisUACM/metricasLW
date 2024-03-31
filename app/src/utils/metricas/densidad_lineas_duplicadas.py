import ast
import os

class DuplicadosLineasCodigoVisitor(ast.NodeVisitor):   
    def __init__(self):
        self.lineas_codigo = []

    def visit_FunctionDef(self, node):
        # Get the lines of code for the function
        start_lineno = node.lineno
        end_lineno = node.end_lineno
        with open(__file__, 'r') as file:
            contenido_archivo = file.readlines()
            codigo_funcion = contenido_archivo[start_lineno-1:end_lineno]
            self.lineas_codigo.extend(codigo_funcion)
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

# Analizar el archivo y calcular la densidad de líneas duplicadas
duplicados_visitor = DuplicadosLineasCodigoVisitor()
duplicados_visitor.visit(ast.parse(open(__file__).read()))
densidad_duplicados = calcular_densidad_duplicados(duplicados_visitor.lineas_codigo)

#print("Densidad de líneas de código duplicadas:", densidad_duplicados)