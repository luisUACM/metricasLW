import ast

class ImpactoModificacionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.va = set()
        self.vt = 0
        self.proporcion_afectadas = 0

    def visit_Assign(self, node):
        # Recopilamos las variables afectadas por el cambio
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.va.add(target.id)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # Contamos el total de variables en la clase
        self.vt = len(node.body)
        self.generic_visit(node)

        # Calculamos la proporción de variables afectadas respecto al total
        if self.vt > 0:
            self.proporcion_afectadas = len(self.va) / self.vt

# Uso de ejemplo:
codigo_fuente_modificado = """
class MiClase:
    def __init__(self):
        self.variable1 = 10
        self.variable2 = 20

    def funcion_modificada(self):
        self.variable1 = 15
        resultado = self.variable1 + self.variable2
"""

arbol_modificado = ast.parse(codigo_fuente_modificado)
impacto_visitor = ImpactoModificacionVisitor()
impacto_visitor.visit(arbol_modificado)

print("Variables afectadas por el cambio:", impacto_visitor.va)
print("Total de variables en la clase:", impacto_visitor.vt)
print("Proporción de variables afectadas respecto al total en la clase:", impacto_visitor.proporcion_afectadas)
# ya esta pero solo que no se aun como colocarle lo de los archivos de el "index" o la primera pagina y como pasarle la grafica