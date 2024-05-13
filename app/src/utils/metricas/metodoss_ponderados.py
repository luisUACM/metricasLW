import ast
from..metricas.complejidad_ciclomatica import calcular_mccabe

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
        self.clases = []
        self.metodos = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.clases.append(node)
        self.metodos.append([])
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if isinstance(node.parent, ast.ClassDef):
            class_index = self.clases.index(node.parent)
            complejidad_visitor = ComplejidadCiclomaticaVisitor()
            self.metodos[class_index].append((node.name, complejidad_visitor))
        self.generic_visit(node)

def analizar_archivo(ruta_archivo: str) -> ast.AST:
    try:
        with open(ruta_archivo, 'r') as archivo:
            return ast.parse(archivo.read())
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado - {ruta_archivo}")
        return None

def calcular_suma_de_c(arbol: ast.AST, visitante: MetodosClaseVisitor) -> None:
    for i, clase in enumerate(visitante.clases):
        print(f"Sumatoria de C para la clase {clase.name}:")
        sumatoria_c = 0
        for nombre_metodo, complejidad_visitor in visitante.metodos[i]:
            metodo = next((n for n in clase.body if isinstance(n, ast.FunctionDef) and n.name == nombre_metodo), None)
            if metodo:
                complejidad_visitor.visit(metodo)
                c = calcular_mccabe(complejidad_visitor.complejidad)
                sumatoria_c += c
        print(f"    Sumatoria de C: {sumatoria_c}")

def main() -> None:
    ruta_archivo = __file__
    arbol = analizar_archivo(ruta_archivo)
    if arbol:
        visitante = MetodosClaseVisitor()
        visitante.visit(arbol)
        calcular_suma_de_c(arbol, visitante)

if __name__ == "__main__":
    main()