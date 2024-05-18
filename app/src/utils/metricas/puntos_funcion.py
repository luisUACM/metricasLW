from flask import request

def calcular_vfa() -> int:
    """
    Regresa: El factor de ajuste ingresado en el formulario de atributos de ajuste.
    """
    vfa = 0
    att = 'att'
    for i in range(1,14):
        vfa += int(request.form[att + str(i)])
    return vfa

def calcular_pf() -> float:
    """
    Regresa: El total de puntos de función según fueron ingresados en el formulario de complejidades.
    """
    pass

def calcular_pfa() -> float:
    """
    Regresa: El total de puntos de función ajustados, según se ingresaron en el formulario.
    """
    pass

def determinar_constantes_duracion() -> tuple[float, float]:
    """
    Regresa: Una tupla con las constantes C y E para la fórmula de duración, según se ingresó en el formulario de caracteristicas del proyecto.
    """
    return (0,0)

def determinar_constantes_esfuerzo() -> tuple[float, float]:
    """
    Regresa: Una tupla con las constantes C y E para la fórmula de esfuerzo, según se ingresó en el formulario de caracteristicas del proyecto.
    """
    return (0,0)