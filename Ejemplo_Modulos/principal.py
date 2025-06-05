# Si se quiere hacer el "import" de una subcarpeta, se pone el nombre de la carpeta "." y el nombre del archivo
# El punto (.) indica misma carpeta -- No es necesario
from calculos import area_circulo, aplicar_iva

# Ejemplo de uso
radio = 5
precio_sin_iva = 100

print(f"Área del círculo (radio={radio}): {area_circulo(radio):.2f}")
print(f"Precio con IVA: ${aplicar_iva(precio_sin_iva):.2f}")