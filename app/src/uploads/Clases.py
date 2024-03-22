class Carro():
    velocidad: int
    motor_encendido: bool

    def encender_motor(self):
        self.motor_encendido = True

    def acelerar(self, cantidad: int):
        if self.motor_encendido:
            self.velocidad += cantidad
        else:
            print('No se puede acelerar con el motor apagado')
    
    def frenar(self, cantidad: int):
        if self.velocidad > 0:
            self.velocidad -= cantidad
        else:
            print('No se puede frenar con el carro detenido')

    def tocar_claxon():
        print('¡piiiip piiiip!')