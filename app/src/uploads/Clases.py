class Carro():
    velocidad: int
    motor_encendido: bool
    color = 'rojo'
    volumen = sonido = 0
    tono: str = 'estandar'

    def encender_motor(self):
        self.motor_encendido = True

    def acelerar(self, cantidad: int):
        if self.motor_encendido:
            self.velocidad += cantidad
        else:
            print('No se puede acelerar con el motor apagado')
            self.edad: int
    
    def frenar(self, cantidad: int):
        self.edad += 1
        if self.velocidad > 0:
            self.velocidad -= cantidad
        else:
            print('No se puede frenar con el carro detenido')

    def tocar_claxon():
        a:str
        print('¡piiiip piiiip!')

    def poner_reversa(self, cantidad: int):
        self.frenar(self.velocidad)
        self.acelerar(cantidad)
        self.encender_luces_traseras()

    def encender_luces_traseras():
        b = 0
        b += 3