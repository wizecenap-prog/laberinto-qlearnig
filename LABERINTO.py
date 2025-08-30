import pygame
import random
import sys
from collections import defaultdict, deque

# Inicializar Pygame
pygame.init()

# Dimensiones
CELL_SIZE = 40
ROWS, COLS = 10, 10
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE + 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego del Laberinto")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Fuente
font = pygame.font.SysFont(None, 28)

# Laberintos prediseñados
mazes = [
    [
        "##########",
        "#        #",
        "#  ####  #",
        "#     #  #",
        "### # ## #",
        "#   #    #",
        "# ### ####",
        "#        #",
        "#   #### #",
        "########E#",
    ],
    [
        "##########",
        "#        #",
        "# ####   #",
        "#   ##   #",
        "# #      #",
        "#   ##   #",
        "#  ###   #",
        "#      # #",
        "#   ##   #",
        "####### E#",
    ],
    [
        "##########",
        "#        #",
        "# ####   #",
        "#   ##   #",
        "##   ##  #",
        "#    #   #",
        "#  ####  #",
        "#        #",
        "#   ##   #",
        "#####   E#",
    ]
]

# Generar laberinto aleatorio accesible
def generate_random_maze():
    maze = [["#" for _ in range(COLS)] for _ in range(ROWS)]
    path = [(1,1)]
    maze[1][1] = " "
    current = (1,1)
    while current != (ROWS-1,COLS-1):
        r, c = current
        moves = []
        if r < ROWS-1: moves.append((r+1,c))
        if c < COLS-1: moves.append((r,c+1))
        if moves:
            next_cell = random.choice(moves)
            nr, nc = next_cell
            maze[nr][nc] = " "
            path.append((nr,nc))
            current = next_cell
    maze[ROWS-1][COLS-1] = "E"
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == "#" and random.random() < 0.25:
                maze[r][c] = "#"
            elif maze[r][c] != "E":
                maze[r][c] = " "
    maze_str = ["".join(row) for row in maze]
    return maze_str

# Dibujar laberinto
def draw_maze(maze, agent_pos, score=0, message=""):
    screen.fill(WHITE)
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == "#":
                pygame.draw.rect(screen, BLACK, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[r][c] == "E":
                pygame.draw.rect(screen, GREEN, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, BLUE, (agent_pos[1] * CELL_SIZE, agent_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    text_score = font.render(f"Puntos: {score}", True, RED)
    screen.blit(text_score, (10, HEIGHT - 90))
    if message:
        msg = font.render(message, True, RED)
        screen.blit(msg, (10, HEIGHT - 60))
    instr = font.render("Usa las flechas para moverte", True, RED)
    screen.blit(instr, (10, HEIGHT - 30))
    pygame.display.flip()

# Menú principal
def show_menu(qlearning=False):
    screen.fill(WHITE)
    title = font.render("Selecciona un laberinto:", True, BLACK)
    screen.blit(title, (WIDTH//4, HEIGHT//4))
    options = [
        "1 - Laberinto 1",
        "2 - Laberinto 2",
        "3 - Laberinto 3",
        "4 - Generar Aleatorio"
    ]
    if not qlearning:
        options.append("5 - Q-Learning")
    for i, opt in enumerate(options):
        txt = font.render(opt, True, BLACK)
        screen.blit(txt, (WIDTH//4, HEIGHT//3 + i*40))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: return mazes[0]
                if event.key == pygame.K_2: return mazes[1]
                if event.key == pygame.K_3: return mazes[2]
                if event.key == pygame.K_4: return generate_random_maze()
                if not qlearning and event.key == pygame.K_5: return "Q-Learning"

# Preguntar si desea jugar de nuevo
def ask_play_again():
    screen.fill(WHITE)
    msg1 = font.render("¿Quieres jugar de nuevo?", True, RED)
    msg2 = font.render("S - Sí   |   N - No", True, RED)
    screen.blit(msg1, (WIDTH//4, HEIGHT//3))
    screen.blit(msg2, (WIDTH//4, HEIGHT//3 + 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return True
                if event.key == pygame.K_n:
                    return False

# Q-Learning
def q_learning_solver(selected_maze):
    # Convertir el laberinto a lista de listas
    maze = [list(row) for row in selected_maze]
    start = (1,1)
    goal = None
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == "E":
                goal = (r,c)

    actions = [(0,1),(0,-1),(1,0),(-1,0)] # derecha, izquierda, abajo, arriba
    q_table = defaultdict(lambda: {a:0 for a in range(len(actions))})
    alpha, gamma, epsilon = 0.2, 0.9, 0.2
    episodes = 500

    # Función de paso
    def step(state, action):
        r,c = state
        dr,dc = actions[action]
        nr,nc = r+dr,c+dc
        if nr<0 or nr>=ROWS or nc<0 or nc>=COLS or maze[nr][nc]=="#":
            return state, -5, False
        if (nr,nc)==goal:
            return (nr,nc), 50, True
        return (nr,nc), -1, False

    # Entrenamiento
    for _ in range(episodes):
        state = start
        done = False
        while not done:
            if random.random() < epsilon:
                action = random.choice(range(len(actions)))
            else:
                action = max(q_table[state], key=q_table[state].get)
            next_state, reward, done = step(state, action)
            q_old = q_table[state][action]
            q_max_next = max(q_table[next_state].values())
            q_table[state][action] = q_old + alpha*(reward + gamma*q_max_next - q_old)
            state = next_state

    # Demostración visual
    state = start
    done = False
    score = 0
    while not done:
        draw_maze(selected_maze, state, score)
        pygame.time.delay(200)
        action = max(q_table[state], key=q_table[state].get)
        state, reward, done = step(state, action)
        score += reward if reward>0 else 0
    draw_maze(selected_maze, state, score, "¡Q-Learning resolvió el laberinto!")
    pygame.time.delay(1000)

# Juego principal
def main():
    while True:
        maze_or_option = show_menu()
        if maze_or_option == "Q-Learning":
            # Si seleccionó Q-Learning, preguntar nuevamente qué laberinto resolver
            selected_maze = show_menu(qlearning=True)
            q_learning_solver(selected_maze)
        else:
            maze = maze_or_option
            agent_pos = [1, 1]
            score = 0
            running = True
            win = False
            while running:
                draw_maze(maze, agent_pos, score, "¡Ganaste!" if win else "")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    elif event.type == pygame.KEYDOWN and not win:
                        new_pos = agent_pos[:]
                        if event.key == pygame.K_UP: new_pos[0] -= 1
                        if event.key == pygame.K_DOWN: new_pos[0] += 1
                        if event.key == pygame.K_LEFT: new_pos[1] -= 1
                        if event.key == pygame.K_RIGHT: new_pos[1] += 1

                        if 0 <= new_pos[0] < ROWS and 0 <= new_pos[1] < COLS:
                            if maze[new_pos[0]][new_pos[1]] == "#":
                                score -= 5
                            else:
                                agent_pos = new_pos
                                score += 1
                                if maze[new_pos[0]][new_pos[1]] == "E":
                                    win = True
                                    score += 50
                                    running = False
                pygame.time.delay(100)

            draw_maze(maze, agent_pos, score, "¡Ganaste!")
            pygame.time.delay(500)
        if not ask_play_again():
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
