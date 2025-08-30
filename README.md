Instrucciones del Juego del Laberinto con Q-Learning
Objetivo del juego

El objetivo es mover al agente (representado por un cuadro azul) a través del laberinto hasta llegar a la salida (cuadro verde “E”), evitando paredes (cuadros negros) y acumulando puntos. También puedes usar la opción de Q-Learning para que el agente resuelva automáticamente el laberinto.

Inicio del juego

Al ejecutar el juego, se abrirá una ventana de Pygame con el menú de selección de laberinto.

Las opciones son:

1: Laberinto 1 (prediseñado)

2: Laberinto 2 (prediseñado, accesible)

3: Laberinto 3 (prediseñado, accesible)

4: Generar un laberinto aleatorio

5: Resolver laberinto automáticamente con Q-Learning

Modo manual (opciones 1-4)

Después de seleccionar el laberinto, el agente se posicionará en la esquina superior izquierda (posición inicial).

Para mover al agente:

Flecha arriba: mueve hacia arriba

Flecha abajo: mueve hacia abajo

Flecha izquierda: mueve hacia la izquierda

Flecha derecha: mueve hacia la derecha

Reglas de puntuación:

Cada paso correcto suma +1 punto

Chocar con una pared resta -5 puntos

Llegar a la salida suma +50 puntos y termina el juego

Mientras juegas, verás:

Puntaje acumulado en rojo

Mensaje de instrucción: “Usa las flechas para moverte”

Mensaje de victoria al llegar a la salida

Modo Q-Learning (opción 5)

Selecciona 5 en el menú principal.

Luego se volverá a mostrar el menú para elegir qué laberinto quieres que el agente resuelva.

El agente aprenderá automáticamente cómo llegar a la salida mediante Q-Learning:

Aprende tras varios intentos simulados.

Luego se mueve paso a paso hacia la salida.

Verás el movimiento en la pantalla y el puntaje acumulado.

Al llegar a la salida, se mostrará un mensaje:
“¡Q-Learning resolvió el laberinto!”

Después de terminar el juego

Al ganar o completar el laberinto con Q-Learning, se mostrará un mensaje final.

Luego aparecerá la pregunta:
“¿Quieres jugar de nuevo? S - Sí | N - No”

Pulsa S para volver a elegir un laberinto y jugar otra vez.

Pulsa N para salir del juego.

Consejos

Observa las paredes negras y planea tus movimientos para evitar perder puntos.

En laberintos grandes o generados aleatoriamente, analiza bien el camino antes de avanzar.

Usa Q-Learning si quieres ver cómo un agente inteligente aprende a resolver laberintos automáticamente.
