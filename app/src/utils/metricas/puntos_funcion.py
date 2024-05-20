class CalculadoraPF:
    def __init__(self, pfsa: float, gsc: int, caracteristicas: str) -> None:
        self.pfsa = pfsa
        self.gsc = gsc
        self.caracteristicas = caracteristicas
        #Aquellos con valor (0.411, 0.328) no están especificados en la tabla, los valores son para cualquier proyecto, no específico de dichas características.
        diccionario_duracion: dict = {'MF':(0.411, 0.328), 
        'MR':(0.411, 0.328),
        'PC':(0.503, 0.409),
        'Multi':(0.679, 0.341),
        '3GL':(0.411, 0.328),
        '4GL':(0.578, 0.393),
        'GenAp':(0.411, 0.328),
        'Mantenimiento':(0.411, 0.328),
        'Nuevo':(0.739, 0.359),
        'MF-3GL':(0.411, 0.328),
        'MF-4GL':(0.411, 0.328),
        'MF-GenAp':(0.411, 0.328),
        'MR-3GL':(0.411, 0.328),
        'MR-4GL':(0.411, 0.328),
        'MR-GenAp':(0.411, 0.328),
        'PC-3GL':(0.411, 0.328),
        'PC-4GL':(0.348, 0.471),
        'PC-GenAp':(0.411, 0.328),
        'Multi-3GL':(0.411, 0.328),
        'Multi-4GL':(0.366, 0.451),
        'Multi-GenAp':(0.411, 0.328), 
        'MF-Nuevo':(0.411, 0.328),
        'MF-Mantenimiento':(0.411, 0.328), 
        'MR-Nuevo':(0.411, 0.328), 
        'MR-Mantenimiento':(0.411, 0.328),
        'PC-Nuevo':(0.411, 0.328), 
        'PC-Mantenimiento':(0.411, 0.328), 
        'Multi-Nuevo':(0.411, 0.328),
        'Multi-Mantenimiento':(0.411, 0.328),
        '3GL-Nuevo':(0.411, 0.328),
        '3GL-Mantenimiento':(0.411, 0.328),
        '4GL-Nuevo':(0.411, 0.328),
        '4GL-Mantenimiento':(0.411, 0.328),
        'GenAp-Nuevo':(0.411, 0.328),
        'GenAp-Mantenimiento':(0.411, 0.328),
        'MF-3GL-Mantenimiento':(0.411, 0.328),
        'MF-3GL-Nuevo':(0.411, 0.328),
        'MF-4GL-Mantenimiento':(0.411, 0.328),
        'MF-4GL-Nuevo':(0.411, 0.328),
        'MF-GenAp-Mantenimiento':(0.411, 0.328),
        'MF-GenAp-Nuevo':(0.411, 0.328),
        'MR-3GL-Mantenimiento':(0.411, 0.328),
        'MR-3GL-Nuevo':(0.411, 0.328),
        'MR-4GL-Mantenimiento':(0.411, 0.328),
        'MR-4GL-Nuevo':(0.411, 0.328),
        'MR-GenAp-Mantenimiento':(0.411, 0.328),
        'MR-GenAp-Nuevo':(0.411, 0.328),
        'PC-3GL-Mantenimiento':(0.411, 0.328),
        'PC-3GL-Nuevo':(0.411, 0.328),
        'PC-4GL-Mantenimiento':(0.411, 0.328),
        'PC-4GL-Nuevo':(0.25, 0.515),
        'PC-GenAp-Mantenimiento':(0.411, 0.328),
        'PC-GenAp-Nuevo':(0.411, 0.328),
        'Multi-3GL-Mantenimiento':(0.411, 0.328),
        'Multi-3GL-Nuevo':(0.411, 0.328),
        'Multi-4GL-Mantenimiento':(0.411, 0.328),
        'Multi-4GL-Nuevo':(0.24, 0.518),
        'Multi-GenAp-Mantenimiento':(0.411, 0.328),
        'Multi-GenAp-Nuevo':(0.411, 0.328) }
        #Aquellos con valor (11.79, 0.898) no están especificados en la tabla, los valores son para cualquier proyecto, no específico de dichas características.
        diccionario_esfuerzo: dict = {'MF':(49.02, 0.736), 
        'MR':(78.88,0.646),
        'PC':(48.9,0.661),
        'Multi':(16.1, 0.865),
        '3GL':(54.65, 0.717),
        '4GL':(29.5, 0.758),
        'GenAp':(68.11, 0.660),
        'Mantenimiento':(52.58, 0.683),
        'Nuevo':(39.05, 0.731),
        'MF-3GL':(65.37, 0.705),
        'MF-4GL':(52.09, 0.64),
        'MF-GenAp':(65.68, 0.692),
        'MR-3GL':(126.3, 0.565),
        'MR-4GL':(62.35, 0.694),
        'MR-GenAp':(11.79, 0.898),
        'PC-3GL':(60.46, 0.694),
        'PC-4GL':(36.48, 0.694),
        'PC-GenAp':(11.79, 0.898),
        'Multi-3GL':(19.82, 0.666),
        'Multi-4GL':(6.49, 0.983),
        'Multi-GenAp':(11.79, 0.898), 
        'MF-Nuevo':(11.79, 0.898),
        'MF-Mantenimiento':(11.79, 0.898), 
        'MR-Nuevo':(11.79, 0.898), 
        'MR-Mantenimiento':(11.79, 0.898),
        'PC-Nuevo':(11.79, 0.898), 
        'PC-Mantenimiento':(11.79, 0.898), 
        'Multi-Nuevo':(11.79, 0.898),
        'Multi-Mantenimiento':(11.79, 0.898),
        '3GL-Nuevo':(11.79, 0.898),
        '3GL-Mantenimiento':(11.79, 0.898),
        '4GL-Nuevo':(11.79, 0.898),
        '4GL-Mantenimiento':(11.79, 0.898),
        'GenAp-Nuevo':(11.79, 0.898),
        'GenAp-Mantenimiento':(11.79, 0.898),
        'MF-3GL-Mantenimiento':(83.27, 0.65),
        'MF-3GL-Nuevo':(59.21, 0.745),
        'MF-4GL-Mantenimiento':(69.37, 0.538),
        'MF-4GL-Nuevo':(102.8, 0.546),
        'MF-GenAp-Mantenimiento':(11.79, 0.898),
        'MF-GenAp-Nuevo':(65.68, 0.692),
        'MR-3GL-Mantenimiento':(123.2, 0.585),
        'MR-3GL-Nuevo':(81.36, 0.623),
        'MR-4GL-Mantenimiento':(96.31, 0.616),
        'MR-4GL-Nuevo':(11.79, 0.898),
        'MR-GenAp-Mantenimiento':(11.79, 0.898),
        'MR-GenAp-Nuevo':(11.79, 0.898),
        'PC-3GL-Mantenimiento':(83.66, 0.528),
        'PC-3GL-Nuevo':(48.6, 0.699),
        'PC-4GL-Mantenimiento':(29.84, 0.731),
        'PC-4GL-Nuevo':(42.58, 0.668),
        'PC-GenAp-Mantenimiento':(11.79, 0.898),
        'PC-GenAp-Nuevo':(11.79, 0.898),
        'Multi-3GL-Mantenimiento':(5.05, 1.135),
        'Multi-3GL-Nuevo':(58.16, 0.664),
        'Multi-4GL-Mantenimiento':(115.8, 0.45),
        'Multi-4GL-Nuevo':(11.79, 0.898),
        'Multi-GenAp-Mantenimiento':(11.79, 0.898),
        'Multi-GenAp-Nuevo':(11.79, 0.898) }
        self.c_esfuerzo = diccionario_esfuerzo[caracteristicas[0]]
        self.e_esfuerzo = diccionario_esfuerzo[caracteristicas[1]]
        self.c_duracion = diccionario_duracion[caracteristicas[0]]
        self.e_duracion = diccionario_duracion[caracteristicas[1]]

    def calcular_vfa(self) -> float:
        """
        Regresa: El factor de ajuste.
        """
        return 0.65 + 0.01 * self.gsc

    def calcular_pfa(self) -> float:
        """
        Regresa: El total de puntos de función ajustados.
        """
        pass

    def calcular_esfuerzo(self) -> float:
        """
        Regresa: El total de esfuerzo necesario para desarrollar el sistema (en horas).
        """
        pass

    def calcular_duracion(self) -> float:
        """
        Regresa: El total de tiempo necesario para desarrollar el sistema, expresada en meses.
        """
        pass

    def calcular_personal(self) -> int:
        """
        Regresa: El personal necesario para desarrollar el sistema (redondeado).
        """
        pass

    def calcular_costo(self) -> float:
        """
        Regresa: El costo total para desarrollar el sistema (asumiendo un mes de 20 días y una jornada de 8 horas).
        """
        pass

    def calcular_productividad(self) -> float:
        """
        Regresa: La productividad mínima que un desarrollador debe tener para completar el proyecto, expresada en puntos de función por hora.
        """
        pass

    def calcular_velocidad(self) -> float:
        """
        Regresa: La velocidad de entrega del proyecto, expresada en puntos de función por mes.
        """
        pass

    def get_constantes_esfuerzo(self) -> tuple[float, float]:
        """
        Regresa: Las constantes C y E para la formula de esfuerzo, en forma de tupla
        """
        return (self.c_esfuerzo, self.e_esfuerzo)
    
    def get_constantes_duracion(self) -> tuple[float, float]:
        """
        Regresa: Las constantes C y E para la formula de duración, en forma de tupla
        """
        return (self.c_duracion, self.e_duracion)