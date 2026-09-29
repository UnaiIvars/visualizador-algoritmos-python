def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        intercambio = False
        for j in range(0, n - i - 1):
            yield lista, (j, j + 1), f"Comparando {lista[j]} y {lista[j+1]}"
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                intercambio = True
                yield lista, (j, j + 1), f"Intercambiando {lista[j]} y {lista[j+1]}"
        if not intercambio:
            break


def selection_sort(lista):
    n = len(lista)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield lista, (j, min_idx), f"Buscando mínimo: comparando {lista[j]} con {lista[min_idx]}"
            if lista[j] < lista[min_idx]:
                min_idx = j
                yield lista, (min_idx,), f"Nuevo mínimo: {lista[min_idx]}"
        if min_idx != i:
            lista[i], lista[min_idx] = lista[min_idx], lista[i]
            yield lista, (i, min_idx), f"Colocando {lista[i]} en posición {i}"


def insertion_sort(lista):
    n = len(lista)
    for i in range(1, n):
        clave = lista[i]
        j = i - 1
        yield lista, (i,), f"Insertando elemento: {clave}"
        while j >= 0 and lista[j] > clave:
            yield lista, (j, j + 1), f"Desplazando {lista[j]} a la derecha"
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = clave
        yield lista, (j + 1,), f"Insertado {clave} en posición {j + 1}"


def merge_sort(lista):
    def _merge_sort(inicio, fin):
        if inicio >= fin:
            return
        medio = (inicio + fin) // 2
        yield from _merge_sort(inicio, medio)
        yield from _merge_sort(medio + 1, fin)
        yield from _fusionar(inicio, medio, fin)

    def _fusionar(inicio, medio, fin):
        izq = lista[inicio:medio + 1]
        der = lista[medio + 1:fin + 1]
        i = j = 0
        k = inicio

        while i < len(izq) and j < len(der):
            yield lista, (k,), f"Fusionando: {izq[i]} y {der[j]}"
            if izq[i] <= der[j]:
                lista[k] = izq[i]
                i += 1
            else:
                lista[k] = der[j]
                j += 1
            k += 1

        while i < len(izq):
            lista[k] = izq[i]
            i += 1
            k += 1
            yield lista, (k - 1,), "Copiando restantes de la izquierda"

        while j < len(der):
            lista[k] = der[j]
            j += 1
            k += 1
            yield lista, (k - 1,), "Copiando restantes de la derecha"

    yield from _merge_sort(0, len(lista) - 1)


def quick_sort(lista):
    def _quick_sort(bajo, alto):
        if bajo < alto:
            pivote_idx = yield from _particionar(bajo, alto)
            yield from _quick_sort(bajo, pivote_idx - 1)
            yield from _quick_sort(pivote_idx + 1, alto)

    def _particionar(bajo, alto):
        pivote = lista[alto]
        i = bajo - 1
        yield lista, (alto,), f"Pivote: {pivote}"
        for j in range(bajo, alto):
            yield lista, (j, alto), f"Comparando {lista[j]} con pivote {pivote}"
            if lista[j] <= pivote:
                i += 1
                lista[i], lista[j] = lista[j], lista[i]
                yield lista, (i, j), f"Moviendo {lista[i]} a la izquierda"
        lista[i + 1], lista[alto] = lista[alto], lista[i + 1]
        yield lista, (i + 1, alto), f"Pivote colocado en posición {i + 1}"
        return i + 1

    yield from _quick_sort(0, len(lista) - 1)


def binary_search(lista, objetivo):
    bajo = 0
    alto = len(lista) - 1

    while bajo <= alto:
        medio = (bajo + alto) // 2
        yield lista, (medio,), f"Probando punto medio: lista[{medio}] = {lista[medio]}"

        if lista[medio] == objetivo:
            yield lista, (medio,), f"¡Encontrado! El {objetivo} está en la posición {medio}"
            return medio
        elif lista[medio] < objetivo:
            yield lista, (medio,), f"{lista[medio]} < {objetivo}: descartando mitad izquierda"
            bajo = medio + 1
        else:
            yield lista, (medio,), f"{lista[medio]} > {objetivo}: descartando mitad derecha"
            alto = medio - 1

    yield lista, (), f"El número {objetivo} no está en la lista"
    return None
