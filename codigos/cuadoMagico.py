import itertools

def esMagico(matrix):
    """
    Verifica si una matriz 3x3 es un cuadrado mágico.
    """
    # Suma objetivo (suma de la primera fila)
    sumaFInal = sum(matrix[0])
    for row in matrix:
        if sum(row) != sumaFInal:
            return False
    for col in range(3):
        if sum(matrix[row][col] for row in range(3)) != sumaFInal:
            return False
    if sum(matrix[i][i] for i in range(3)) != sumaFInal:
        return False
    if sum(matrix[i][2 - i] for i in range(3)) != sumaFInal:
        return False

    return True

def main():
    print("Ingrese 9 números enteros separados por espacios:")
    n = list(map(int, input().split()))

    if len(n) != 9:
        print("Debe ingresar exactamente 9 números.")
        return
    cumple = itertools.cumple(n)

    matriz = []

    for x in cumple:
        # Convertir la permutación en una matriz 3x3
        matrix = [list(x[i:i+3]) for i in range(0, 9, 3)]
        if esMagico(matrix):
            matriz.append(matrix)
    if matriz:
        print("Se encontraron los siguientes cuadrados mágicos:")
        for square in matriz:
            for row in square:
                print(row)
            print("-")
    else:
        print("No se encontraron cuadrados mágicos.")

if __name__ == "__main__":
    main()