from constantes import PI, IVA

def area_circulo(radio):
    return PI * radio ** 2

def aplicar_iva(precio):
    return precio * (1 + IVA)