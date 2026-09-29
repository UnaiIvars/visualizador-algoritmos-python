import random
import pygame
from algorithms import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    binary_search,
)
from pathfinding import (
    bfs,
    dfs,
    dijkstra,
    generar_muros_aleatorios,
)

ANCHO = 1000
ALTO = 650
FPS = 60

COLOR_FONDO = (24, 27, 36)
COLOR_PANEL = (32, 36, 49)
COLOR_TEXTO = (235, 240, 245)
COLOR_SECUNDARIO = (140, 155, 180)
COLOR_BARRA_NORMAL = (99, 102, 241)
COLOR_BARRA_ACTIVA = (245, 158, 11)
COLOR_BARRA_VERDE = (34, 197, 94)
COLOR_INICIO = (34, 197, 94)
COLOR_DESTINO = (239, 68, 68)
COLOR_MURO = (15, 17, 23)
COLOR_VISITADO = (59, 130, 246)
COLOR_CAMINO = (250, 204, 21)
COLOR_LINEA_GRID = (40, 46, 62)

CATALOGO = [
    ("1. Burbuja", "ordenacion", bubble_sort, "O(n²)", "Ordenación básica"),
    ("2. Selección", "ordenacion", selection_sort, "O(n²)", "Ordenación básica"),
    ("3. Inserción", "ordenacion", insertion_sort, "O(n²)", "Ordenación básica"),
    ("4. Merge Sort", "ordenacion", merge_sort, "O(n log n)", "Divide y vencerás"),
    ("5. Quick Sort", "ordenacion", quick_sort, "O(n log n)", "Partición con pivote"),
    ("6. Búsqueda Binaria", "busqueda", binary_search, "O(log n)", "Búsqueda en lista ordenada"),
    ("7. BFS (Anchura)", "grafos", bfs, "O(V + E)", "Garantiza camino más corto"),
    ("8. DFS (Profundidad)", "grafos", dfs, "O(V + E)", "Exploración en profundidad"),
    ("9. Dijkstra", "grafos", dijkstra, "O((V+E) log V)", "Camino mínimo con pesos"),
]


class Visualizador:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Visualizador de Algoritmos")
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("arial", 14)
        self.fuente_grande = pygame.font.SysFont("arial", 17, bold=True)
        self.fuente_mono = pygame.font.SysFont("consolas,monospace", 13)

        self.en_ejecucion = False
        self.completado = False
        self.velocidad = 2
        self.indice_algoritmo = 0
        self.mensaje_estado = "Pulsa [ESPACIO] para iniciar o [1-9] para cambiar de algoritmo"

        self.cantidad_barras = 45
        self.lista = []
        self.indices_activos = ()
        self.objetivo_busqueda = None

        self.filas = 22
        self.columnas = 38
        self.inicio = (self.filas // 2, 4)
        self.destino = (self.filas // 2, self.columnas - 5)
        self.muros = set()
        self.visitados = set()
        self.nodo_actual = None
        self.camino = []

        self.generador = None
        self.reiniciar_datos()

    def reiniciar_datos(self):
        self.en_ejecucion = False
        self.completado = False
        self.indices_activos = ()
        self.visitados = set()
        self.camino = []
        self.nodo_actual = None

        _, tipo, funcion, _, _ = CATALOGO[self.indice_algoritmo]

        if tipo == "ordenacion":
            self.lista = [random.randint(15, 380) for _ in range(self.cantidad_barras)]
            self.generador = funcion(list(self.lista))
            self.mensaje_estado = "Listo. Pulsa [ESPACIO] para ordenar."

        elif tipo == "busqueda":
            self.lista = sorted([random.randint(10, 380) for _ in range(30)])
            self.objetivo_busqueda = random.choice(self.lista)
            self.generador = funcion(list(self.lista), self.objetivo_busqueda)
            self.mensaje_estado = f"Buscando el número {self.objetivo_busqueda}. Pulsa [ESPACIO]."

        elif tipo == "grafos":
            self.generador = funcion(
                self.inicio, self.destino, self.filas, self.columnas, set(self.muros)
            )
            self.mensaje_estado = "Haz clic en la cuadrícula para pintar muros. Pulsa [ESPACIO] para buscar."

    def cambiar_algoritmo(self, nuevo_indice):
        if 0 <= nuevo_indice < len(CATALOGO):
            self.indice_algoritmo = nuevo_indice
            self.reiniciar_datos()

    def avanzar_paso(self):
        if not self.generador or self.completado:
            return

        try:
            _, tipo, _, _, _ = CATALOGO[self.indice_algoritmo]
            if tipo in ("ordenacion", "busqueda"):
                self.lista, self.indices_activos, self.mensaje_estado = next(self.generador)
            else:
                self.visitados, self.nodo_actual, self.camino, self.mensaje_estado = next(
                    self.generador
                )
        except StopIteration:
            self.en_ejecucion = False
            self.completado = True
            self.indices_activos = ()
            self.mensaje_estado = "¡Algoritmo finalizado con éxito!"

    def procesar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.en_ejecucion = not self.en_ejecucion

                elif evento.key == pygame.K_r:
                    self.reiniciar_datos()

                elif evento.key == pygame.K_m:
                    _, tipo, _, _, _ = CATALOGO[self.indice_algoritmo]
                    if tipo == "grafos":
                        self.muros = generar_muros_aleatorios(
                            self.filas, self.columnas, self.inicio, self.destino
                        )
                        self.reiniciar_datos()

                elif evento.key == pygame.K_l:
                    self.muros.clear()
                    self.reiniciar_datos()

                elif evento.key == pygame.K_UP:
                    self.velocidad = min(15, self.velocidad + 1)
                elif evento.key == pygame.K_DOWN:
                    self.velocidad = max(1, self.velocidad - 1)

                elif pygame.K_1 <= evento.key <= pygame.K_9:
                    idx = evento.key - pygame.K_1
                    self.cambiar_algoritmo(idx)

            elif evento.type == pygame.MOUSEBUTTONDOWN and not self.en_ejecucion:
                _, tipo, _, _, _ = CATALOGO[self.indice_algoritmo]
                if tipo == "grafos":
                    self._modificar_muro_con_raton(evento.pos, es_borrado=(evento.button == 3))

            elif evento.type == pygame.MOUSEMOTION and not self.en_ejecucion:
                _, tipo, _, _, _ = CATALOGO[self.indice_algoritmo]
                if tipo == "grafos" and pygame.mouse.get_pressed()[0]:
                    self._modificar_muro_con_raton(evento.pos, es_borrado=False)
                elif tipo == "grafos" and pygame.mouse.get_pressed()[2]:
                    self._modificar_muro_con_raton(evento.pos, es_borrado=True)

        return True

    def _modificar_muro_con_raton(self, pos_raton, es_borrado=False):
        x, y = pos_raton
        alto_encabezado = 70
        alto_cuadricula = ALTO - alto_encabezado - 70
        tam_celda_x = ANCHO / self.columnas
        tam_celda_y = alto_cuadricula / self.filas

        if alto_encabezado <= y < alto_encabezado + alto_cuadricula:
            col = int(x // tam_celda_x)
            fila = int((y - alto_encabezado) // tam_celda_y)
            coord = (fila, col)
            if coord != self.inicio and coord != self.destino:
                if es_borrado and coord in self.muros:
                    self.muros.remove(coord)
                    self.reiniciar_datos()
                elif not es_borrado and coord not in self.muros:
                    self.muros.add(coord)
                    self.reiniciar_datos()

    def actualizar(self):
        if self.en_ejecucion and not self.completado:
            for _ in range(self.velocidad):
                self.avanzar_paso()
                if self.completado:
                    break

    def dibujar(self):
        self.pantalla.fill(COLOR_FONDO)
        self._dibujar_encabezado()

        _, tipo, _, _, _ = CATALOGO[self.indice_algoritmo]
        if tipo in ("ordenacion", "busqueda"):
            self._dibujar_barras()
        else:
            self._dibujar_cuadricula()

        self._dibujar_pie()
        pygame.display.flip()

    def _dibujar_encabezado(self):
        pygame.draw.rect(self.pantalla, COLOR_PANEL, (0, 0, ANCHO, 65))
        nombre, _, _, complejidad, nota = CATALOGO[self.indice_algoritmo]

        texto_titulo = self.fuente_grande.render(f"Algoritmo: {nombre}", True, COLOR_TEXTO)
        self.pantalla.blit(texto_titulo, (20, 12))

        texto_info = self.fuente.render(
            f"Complejidad Big-O: {complejidad}  •  {nota}  •  Velocidad: {self.velocidad}x",
            True,
            COLOR_SECUNDARIO,
        )
        self.pantalla.blit(texto_info, (20, 38))

        estado_txt = "EN EJECUCIÓN" if self.en_ejecucion else ("COMPLETADO" if self.completado else "EN PAUSA")
        color_estado = COLOR_BARRA_VERDE if self.en_ejecucion or self.completado else COLOR_BARRA_ACTIVA
        surf_estado = self.fuente_grande.render(estado_txt, True, color_estado)
        self.pantalla.blit(surf_estado, (ANCHO - surf_estado.get_width() - 25, 20))

    def _dibujar_barras(self):
        alto_disponible = ALTO - 150
        ancho_barra = (ANCHO - 60) / len(self.lista)
        max_valor = max(self.lista) if self.lista else 1

        for i, val in enumerate(self.lista):
            altura = (val / max_valor) * alto_disponible
            x = 30 + i * ancho_barra
            y = ALTO - 75 - altura

            if i in self.indices_activos:
                color = COLOR_BARRA_ACTIVA
            elif self.completado:
                color = COLOR_BARRA_VERDE
            else:
                color = COLOR_BARRA_NORMAL

            rect = pygame.Rect(int(x), int(y), max(1, int(ancho_barra - 2)), int(altura))
            pygame.draw.rect(self.pantalla, color, rect, border_radius=3)

    def _dibujar_cuadricula(self):
        alto_encabezado = 70
        alto_cuadricula = ALTO - alto_encabezado - 70
        ancho_celda = ANCHO / self.columnas
        alto_celda = alto_cuadricula / self.filas

        for r in range(self.filas):
            for c in range(self.columnas):
                rect = pygame.Rect(int(c * ancho_celda), int(alto_encabezado + r * alto_celda), int(ancho_celda), int(alto_celda))
                coord = (r, c)

                if coord == self.inicio:
                    color = COLOR_INICIO
                elif coord == self.destino:
                    color = COLOR_DESTINO
                elif coord in self.camino:
                    color = COLOR_CAMINO
                elif coord == self.nodo_actual:
                    color = COLOR_BARRA_ACTIVA
                elif coord in self.visitados:
                    color = COLOR_VISITADO
                elif coord in self.muros:
                    color = COLOR_MURO
                else:
                    color = COLOR_FONDO

                pygame.draw.rect(self.pantalla, color, rect)
                pygame.draw.rect(self.pantalla, COLOR_LINEA_GRID, rect, 1)

    def _dibujar_pie(self):
        pygame.draw.rect(self.pantalla, COLOR_PANEL, (0, ALTO - 65, ANCHO, 65))

        txt_msg = self.fuente_mono.render(f"Paso actual: {self.mensaje_estado}", True, (56, 189, 248))
        self.pantalla.blit(txt_msg, (20, ALTO - 53))

        txt_ayuda = self.fuente.render(
            "[ESPACIO] Play/Pausa  •  [R] Reiniciar  •  [1-9] Algoritmo  •  [M] Laberinto  •  [L] Limpiar  •  [↑/↓] Velocidad",
            True,
            COLOR_SECUNDARIO,
        )
        self.pantalla.blit(txt_ayuda, (20, ALTO - 26))

    def ejecutar(self):
        corriendo = True
        while corriendo:
            corriendo = self.procesar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)

        pygame.quit()
