import pytest
from algorithms import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    binary_search,
)
from pathfinding import bfs, dfs, dijkstra


ALGORITMOS_ORDENACION = [
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
]


@pytest.mark.parametrize("algoritmo", ALGORITMOS_ORDENACION)
def test_ordenar_lista_desordenada(algoritmo):
    datos = [64, 34, 25, 12, 22, 11, 90]
    esperado = sorted(datos)

    for _ in algoritmo(datos):
        pass

    assert datos == esperado


@pytest.mark.parametrize("algoritmo", ALGORITMOS_ORDENACION)
def test_ordenar_lista_con_duplicados(algoritmo):
    datos = [5, 2, 8, 2, 5, 1, 9, 1]
    esperado = sorted(datos)

    for _ in algoritmo(datos):
        pass

    assert datos == esperado


def test_busqueda_binaria_encontrado():
    lista = [10, 20, 30, 40, 50, 60, 70]
    objetivo = 40

    resultado = None
    gen = binary_search(lista, objetivo)
    try:
        while True:
            next(gen)
    except StopIteration as e:
        resultado = e.value

    assert resultado == 3
    assert lista[resultado] == objetivo


def test_busqueda_binaria_no_encontrado():
    lista = [10, 20, 30, 40, 50]
    objetivo = 99

    resultado = None
    gen = binary_search(lista, objetivo)
    try:
        while True:
            next(gen)
    except StopIteration as e:
        resultado = e.value

    assert resultado is None


def test_bfs_camino_corto():
    inicio = (0, 0)
    destino = (0, 4)
    filas, columnas = 5, 5
    muros = set()

    camino = []
    gen = bfs(inicio, destino, filas, columnas, muros)
    try:
        while True:
            next(gen)
    except StopIteration as e:
        camino = e.value

    assert len(camino) == 5
    assert camino[0] == inicio
    assert camino[-1] == destino


def test_dijkstra_ruta_optima():
    inicio = (0, 0)
    destino = (2, 0)
    filas, columnas = 5, 5
    muros = {(1, 0)}

    camino = []
    gen = dijkstra(inicio, destino, filas, columnas, muros)
    try:
        while True:
            next(gen)
    except StopIteration as e:
        camino = e.value

    assert len(camino) > 0
    assert (1, 0) not in camino
    assert camino[0] == inicio
    assert camino[-1] == destino
