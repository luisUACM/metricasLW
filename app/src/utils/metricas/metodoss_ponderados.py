import ast
from ..metricas.complejidad_ciclomatica import calcular_mccabe

class ComplejidadCiclomaticaVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complejidad = 0

    def visit_If(self, node: ast.If) -> None:
        self.complejidad += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.complejidad += 1
        self.generic_visit(node)
    def visit_While(self, node: ast.While) -> None:
        self.complejidad += 1
        self.generic_visit(node)

class MetodosClaseVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metodos = []
        self.suma_c = {}

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.metodos.append([])
        self.suma_c[len(self.metodos) - 1] = {}
        for child_node in ast.iter_child_nodes(node):
            if isinstance(child_node, ast.FunctionDef):
                self.metodos[-1].append(child_node)
                self.suma_c[len(self.metodos) - 1][child_node.name] = 0
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        pass
        self.suma_c[len(self.metodos) - 1][node.name] = 0
        self.generic_visit(node)

def analizar_archivo(ruta_archivo: str) -> ast.AST:
    try:
        with open(ruta_archivo, 'r') as archivo:
            return ast.parse(archivo.read())
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado - {ruta_archivo}")
        return None

def calcular_suma_de_c(tree: ast.AST, visitor: MetodosClaseVisitor) -> None:
    for i, clase in enumerate(visitor.metodos):
        print(f"Sumatoria de C para la clase {clase[0].name}:")
        sumatorias_c = 0
        for nombre_metodo, complejidad_visitor in visitor.suma_c[i].items():
            metodo = next((n for n in clase if isinstance(n, ast.FunctionDef) and n.name == nombre_metodo), None)
            if metodo:
                complejidad_visitor.visit(metodo)
                c = calcular_mccabe(complejidad_visitor.complejidad)
                sumatoria_c += c
        print(f"    Sumatoria de C: {sumatorias_c}")

def main() -> None:
    ruta_archivo = __file__
    arbol = analizar_archivo(ruta_archivo)
    if arbol:
        visitante = MetodosClaseVisitor()
        visitante.visit(arbol)
        calcular_suma_de_c(arbol, visitante)

if __name__ == "__main__":
    main