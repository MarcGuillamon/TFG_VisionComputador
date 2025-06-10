import kociemba

def kociembas_algorithm(U, R, F, D, L, B):
    """
    Resuelve un cubo de Rubik usando el algoritmo de Kociemba.
    
    Args:
        U (str): Cara superior (Up) en formato de 9 caracteres
        R (str): Cara derecha (Right) en formato de 9 caracteres
        F (str): Cara frontal (Front) en formato de 9 caracteres
        D (str): Cara inferior (Down) en formato de 9 caracteres
        L (str): Cara izquierda (Left) en formato de 9 caracteres
        B (str): Cara trasera (Back) en formato de 9 caracteres
    
    Returns:
        str: Secuencia de movimientos para resolver el cubo
    """
    # Construir la cadena completa del cubo
    scrambled_cube = U + R + F + D + L + B
    
    # Verificar si el cubo ya está resuelto
    if scrambled_cube == 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB':
        return "El cubo ya está resuelto!"
    else:
        try:
            solution = kociemba.solve(scrambled_cube)
            return solution
        except Exception as e:
            return f"Error al resolver el cubo: {str(e)}"