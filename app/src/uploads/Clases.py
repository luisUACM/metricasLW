class Carro():
    velocidad: int
    motor_encendido: bool
    volumen = sonido = 0
    tono: str = 'estandar'

    def __init__(self) -> None:
        self.llantas = 4

    @property
    def encender_motor(self):
        self.motor_encendido = True

    @motor_encendido.setter
    def motor_encendido(self, m: bool):
        self.motor_encendido = m
        
    def acelerar(self, cantidad: int):
        if self.motor_encendido:
            self.velocidad += cantidad
        else:
            print('No se puede acelerar con el motor apagado')
            self.edad: int
            self.color = 'rojo'
        a = 0
        if True:
            a
        else:
            if True:
                a
            else:
                if True:
                    a
                else:
                    a
    
    def frenar(self, cantidad: int):
        self.edad += 1
        for i in range(5):
            i += 1
        if self.velocidad > 0 or self.motor_encendido:
            self.velocidad -= cantidad
        else:
            print('No se puede frenar con el carro detenido')

    def tocar_claxon(self):
        a:str
        i = 0
        while i < 10:
            i += 1
        c = b = 1
        print(str(self.llantas))
        print('¡piiiip piiiip!' + str(c) + str(b))

    def poner_reversa(self, cantidad: int):
        self.frenar(self.velocidad)
        self.acelerar(cantidad)
        self.encender_luces_traseras()

    def encender_luces_traseras():
        b = 0
        b += 3