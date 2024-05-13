import ast
import os

class DuplicadosLineasCodigoVisitor(ast.NodeVisitor):
    def __init__(self):
        self.lineas_codigo = {}

    def visit_FunctionDef(self, node):
        # Obtiene las líneas de código para la función
        start_lineno = node.lineno
        end_lineno = node.end_lineno
        nombre_funcion = node.name
        with open(__file__, 'r') as file:
            contenido_archivo = file.readlines()
            # String que verifica que no se encuentre líneas vacías
            codigo_funcion = [line for line in contenido_archivo[start_lineno-1:end_lineno] if line.strip()]
            if nombre_funcion not in self.lineas_codigo:
                self.lineas_codigo[nombre_funcion] = {'lineas_codigo': [],'lineas_unicas': set(), 'lineas_duplicadas': 1}
            self.lineas_codigo[nombre_funcion]['lineas_codigo'].extend(codigo_funcion)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # Obtiene las líneas de código para la clase
        start_lineno = node.lineno
        end_lineno = node.end_lineno
        nombre_clase = node.name
        with open(__file__, 'r') as file:
            contenido_archivo = file.readlines()
            # String que verifica que no se encuentre líneas vacías
            codigo_clase = [line for line in contenido_archivo[start_lineno-1:end_lineno] if line.strip()]
            if nombre_clase not in self.lineas_codigo:
                self.lineas_codigo[nombre_clase] = {'lineas_codigo': [],'lineas_unicas': set(), 'lineas_duplicadas': 1}
            self.lineas_codigo[nombre_clase]['lineas_codigo'].extend(codigo_clase)
        self.generic_visit(node)

# Calcula la métrica de densidad de líneas de código duplicadas
def calcular_densidad_duplicados(lineas_codigo):
    total_lineas = 0
    lineas_unicas = set()
    for codigo in lineas_codigo:
        total_lineas += len(codigo)
        lineas_unicas.update(codigo)
    lineas_duplicadas = total_lineas - len(lineas_unicas)
    if total_lineas > 0:
        densidad_duplicados = lineas_duplicadas / total_lineas * 100
    else:
        densidad_duplicados = 0
    return densidad_duplicados

# Analizar el archivo y calcular la densidad de líneas duplicadas
duplicados_visitor = DuplicadosLineasCodigoVisitor()
duplicados_visitor.visit(ast.parse(open(__file__).read()))

lineas = []
for nombre_clase, codigo in duplicados_visitor.lineas_codigo.items():
    lineas.append(codigo['lineas_codigo'])

lineas_unidas = sum(lineas, [])
lineas_duplicadas = calcular_densidad_duplicados(lineas_unidas)

#print("Densidad de líneas de código duplicadas:", lineas_duplicadas)