from collections import deque
import heapq
import random


def obtener_vecinos(nodo, filas, columnas, muros):
    r, c = nodo
    vecinos = []
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < filas and 0 <= nc < columnas:
            if (nr, nc) not in muros:
                vecinos.append((nr, nc))
    return vecinos


def reconstruir_camino(padres, destino):
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = padres.get(actual)
    camino.reverse()
    return camino


def bfs(inicio, destino, filas, columnas, muros):
    cola = deque([inicio])
    padres = {inicio: None}
    visitados = {inicio}

    yield visitados, inicio, [], "Iniciando BFS..."

    while cola:
        actual = cola.popleft()

        if actual == destino:
            camino = reconstruir_camino(padres, destino)
            yield visitados, actual, camino, f"¡Destino alcanzado! Longitud: {len(camino) - 1} pasos"
            return camino

        for vecino in obtener_vecinos(actual, filas, columnas, muros):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                cola.append(vecino)
                yield visitados, vecino, [], f"BFS explorando celda {vecino}"

    yield visitados, None, [], "No existe camino hacia el destino"
    return []


def dfs(inicio, destino, filas, columnas, muros):
    pila = [inicio]
    padres = {inicio: None}
    visitados = {inicio}

    yield visitados, inicio, [], "Iniciando DFS..."

    while pila:
        actual = pila.pop()

        if actual == destino:
            camino = reconstruir_camino(padres, destino)
            yield visitados, actual, camino, f"¡Destino alcanzado! Longitud: {len(camino) - 1} pasos"
            return camino

        for vecino in reversed(obtener_vecinos(actual, filas, columnas, muros)):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                pila.append(vecino)
                yield visitados, vecino, [], f"DFS avanzando a celda {vecino}"

    yield visitados, None, [], "No existe camino hacia el destino"
    return []


def dijkstra(inicio, destino, filas, columnas, muros):
    heap = [(0, inicio)]
    distancias = {inicio: 0}
    padres = {inicio: None}
    visitados = set()

    yield visitados, inicio, [], "Iniciando Dijkstra..."

    while heap:
        dist_actual, actual = heapq.heappop(heap)

        if actual in visitados:
            continue
        visitados.add(actual)

        if actual == destino:
            camino = reconstruir_camino(padres, destino)
            yield visitados, actual, camino, f"¡Dijkstra completado! Coste: {dist_actual}"
            return camino

        for vecino in obtener_vecinos(actual, filas, columnas, muros):
            nueva_dist = dist_actual + 1
            if vecino not in distancias or nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                padres[vecino] = actual
                heapq.heappush(heap, (nueva_dist, vecino))
                yield visitados, vecino, [], f"Dijkstra evaluando celda {vecino} (distancia: {nueva_dist})"

    yield visitados, None, [], "No existe camino hacia el destino"
    return []


def generar_muros_aleatorios(filas, columnas, inicio, destino, probabilidad=0.25):
    muros = set()
    for r in range(filas):
        for c in range(columnas):
            if (r, c) != inicio and (r, c) != destino:
                if random.random() < probabilidad:
                    muros.add((r, c))
    return muros
