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
        if True:
            pass
        else:
            pass
        if True:
            pass
            if True:
                pass
    
    def frenar(self, cantidad: int):
        self.edad += 1
        #while i < 10:
        #    i += 1
            
        if self.velocidad > 0 or self.motor_encendido and True:
            self.velocidad -= cantidad
        else:
            print('No se puede frenar con el carro detenido')

    def tocar_claxon(self):
        a:str
        i = 0
        while i < 10:
            i += 1
            
            while i < 10:
                print("")
                print("")
        c = b = 1
        print("")
        print(str(self.llantas))
        print('¡piiiip piiiip!' + str(c) + str(b))

    def poner_reversa(self, cantidad: int):
        self.frenar(self.velocidad)
        self.acelerar(cantidad)
        c: bool
        d: bool
        #a = (True and False) or (False and True)
        #b = c or True or (True and True) or (c and d)
        c = c and d or True
        d = False or True
        self.encender_luces_traseras()

    def encender_luces_traseras():
        while True or False and True:
            pass
        b = 0
        b += 3