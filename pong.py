import pygame
import sys
import random

# Inicializar Pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("audio.mp3")


# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Configurar pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600


pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Pong')



# Definir las paletas y la pelota
ancho_paleta = 10
alto_paleta = 100
velocidad_paleta = 5
paleta_izquierda = pygame.Rect(50, ALTO_PANTALLA // 2 - alto_paleta // 2, ancho_paleta, alto_paleta)
paleta_derecha = pygame.Rect(ANCHO_PANTALLA - 50 - ancho_paleta, ALTO_PANTALLA // 2 - alto_paleta // 2, ancho_paleta, alto_paleta)
cant_colisiones = 0
score_I = 0
score_r = 0
ancho_pelota = 20
pelota = pygame.Rect(ANCHO_PANTALLA // 2 - ancho_pelota // 2, ALTO_PANTALLA // 2 - ancho_pelota // 2, ancho_pelota, ancho_pelota)
velocidad_pelota_x = 4
velocidad_pelota_y = 0
score_font = pygame.font.SysFont("comicsansms", 35)

modo_juego = None  
dificultad = None

global tiempo_transcurrido
global tiempo_restante

# Variables para el muro
muro_actual = None
tiempo_siguiente_muro = pygame.time.get_ticks() + random.randint(2000, 5000)

# Función para mostrar mensaje en pantalla
def mostrar_mensaje(texto, color, posicion):
    mensaje = score_font.render(texto, True, color)
    pantalla.blit(mensaje, posicion)


def seleccionar_modo():
    global modo_juego
    while True:
        pantalla.fill(NEGRO)
        mostrar_mensaje("Selecciona el modo de juego:", BLANCO, (ANCHO_PANTALLA // 2 - 200, ALTO_PANTALLA // 2 - 100))
        mostrar_mensaje("1. Single Player", BLANCO, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2))
        mostrar_mensaje("2. Multiplayer", BLANCO, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 + 50))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    modo_juego = 'single'
                    seleccionar_dificultad()
                    return
                elif evento.key == pygame.K_2:
                    modo_juego = 'multi'
                    seleccionar_dificultad()
                    return

# Pantalla de selección de dificultad
def seleccionar_dificultad():
    global dificultad
    while True:
        pantalla.fill(NEGRO)
        mostrar_mensaje("Selecciona la dificultad:", BLANCO, (ANCHO_PANTALLA // 2 - 200, ALTO_PANTALLA // 2 - 100))
        mostrar_mensaje("1. Facil", BLANCO, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2))
        mostrar_mensaje("2. Intermedio", BLANCO, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 + 50))
        mostrar_mensaje("3. Dificil", BLANCO, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 + 100))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    dificultad = 'Facil'
                    return
                elif evento.key == pygame.K_2:
                    dificultad = 'Intermedio'
                    return
                elif evento.key == pygame.K_3:
                    dificultad = 'Dificil'
                    return

def configurar_dificultad():
    global velocidad_paleta, velocidad_pelota_x, velocidad_pelota_y
    if dificultad == 'Facil':
        velocidad_pelota_x = 4
        velocidad_paleta = 5
    elif dificultad == 'Intermedio':
        velocidad_pelota_x = 7
        velocidad_paleta = 8
    elif dificultad == 'Dificil':
        velocidad_pelota_x = 10
        velocidad_paleta = 11


def pantalla_inicio():
    seleccionar_modo()
    configurar_dificultad()

# Funcion para mover las paletas
def mover_paletas(teclas, paleta_izquierda, paleta_derecha):
    if teclas[pygame.K_w] and paleta_izquierda.top > 0:
        paleta_izquierda.y -= velocidad_paleta
    if teclas[pygame.K_s] and paleta_izquierda.bottom < ALTO_PANTALLA:
        paleta_izquierda.y += velocidad_paleta
    if teclas[pygame.K_UP] and paleta_derecha.top > 0:
        paleta_derecha.y -= velocidad_paleta
    if teclas[pygame.K_DOWN] and paleta_derecha.bottom < ALTO_PANTALLA:
        paleta_derecha.y += velocidad_paleta

# Funcion para mostrar el puntaje
def yourscore(scorei, scorer):
    value = score_font.render(f"{scorei}", True, BLANCO)
    value1 = score_font.render(f"{scorer}", True, BLANCO)
    pantalla.blit(value, [(ANCHO_PANTALLA / 2 - 30), 0])
    pantalla.blit(value1, [(ANCHO_PANTALLA / 2 + 11), 0])

# Función para mover la pelota
def mover_pelota(muro_actual):
    global velocidad_pelota_x, velocidad_pelota_y, score_I, score_r, cant_colisiones
    pelota.x += velocidad_pelota_x
    pelota.y += velocidad_pelota_y

    # Rebote en los bordes superior e inferior
    if pelota.top <= 0 or pelota.bottom >= ALTO_PANTALLA - 5:
        velocidad_pelota_y = -velocidad_pelota_y

    # Rebote en las paletas
    if pelota.colliderect(paleta_izquierda) or pelota.colliderect(paleta_derecha):
        pygame.mixer.music.play()
        cant_colisiones += 1
        if cant_colisiones == 1:
            velocidad_pelota_y = 5.5
        if cant_colisiones % 5 == 0:
            velocidad_pelota_x *= 1.1
            velocidad_pelota_y *= 1.1
            cant_colisiones = 0
        velocidad_pelota_x = -velocidad_pelota_x

    # Rebote en el muro 
    if muro_actual and pelota.colliderect(muro_actual):
        # Invertir la dirección en ambos ejes
        velocidad_pelota_x = -velocidad_pelota_x
        velocidad_pelota_y = -velocidad_pelota_y

    # Reiniciar posición si hay gol
    if pelota.left <= 0:
        score_r += 1
        velocidad_pelota_x = 4
        velocidad_pelota_y = 0
        cant_colisiones = 0
        reiniciar_pelota()
    if pelota.right >= ANCHO_PANTALLA:
        score_I += 1
        velocidad_pelota_x = -4
        velocidad_pelota_y = 0
        cant_colisiones = 0
        reiniciar_pelota()

# Reiniciar la pelota al centro
def reiniciar_pelota():
    global velocidad_pelota_x, velocidad_pelota_y
    pelota.center = (ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)
    velocidad_pelota_x = -velocidad_pelota_x


def crear_muro():
    x = random.randint(100, ANCHO_PANTALLA - 100)
    y = random.randint(50, ALTO_PANTALLA - 50)
    ancho_muro = random.randint(20, 100)
    alto_muro = random.randint(20, 100)
    return pygame.Rect(x, y, ancho_muro, alto_muro)

# Pantalla de bienvenida
def pantalla_inicio():
    
    seleccionar_modo()
    configurar_dificultad()

# Bucle principal del juego
def bucle_juego():
    global muro_actual, tiempo_siguiente_muro, score_I, score_r, cant_colisiones
    while True:
        
        pantalla_inicio()
        configurar_dificultad()

        # Reiniciar variables
        muro_actual = None
        tiempo_siguiente_muro = pygame.time.get_ticks() + random.randint(2000, 5000)
        tiempo_inicio = pygame.time.get_ticks()  # Reiniciar el tiempo de partida
        score_I, score_r, cant_colisiones = 0, 0, 0  
        tiempoXpartida = 10
        partida_en_curso = True  
        reloj = pygame.time.Clock()

        # Bucle de la partida
        while partida_en_curso:
            
            tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio) / 1000
            tiempo_restante = max(0, tiempoXpartida - int(tiempo_transcurrido)) 

            # Manejo de eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

           
            if tiempo_restante == 0:
                partida_en_curso = False  #
                break  

            # Movimiento de las paletas
            teclas = pygame.key.get_pressed()
            mover_paletas(teclas, paleta_izquierda, paleta_derecha)

            # Movimiento de la pelota
            mover_pelota(muro_actual)

            # Crear un nuevo muro cada cierto tiempo
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual >= tiempo_siguiente_muro:
                muro_actual = crear_muro()
                tiempo_siguiente_muro = tiempo_actual + random.randint(2000, 5000)  # tiempo aleatorio

            # Dibujar en pantalla
            pantalla.fill(NEGRO)
            pygame.draw.rect(pantalla, BLANCO, paleta_izquierda)
            pygame.draw.rect(pantalla, BLANCO, paleta_derecha)
            pygame.draw.ellipse(pantalla, BLANCO, pelota)
            pygame.draw.aaline(pantalla, BLANCO, (ANCHO_PANTALLA // 2, 0), (ANCHO_PANTALLA // 2, ALTO_PANTALLA))

            # Dibujar el muro 
            if muro_actual:
                pygame.draw.rect(pantalla, BLANCO, muro_actual)

            # Estaba mirando lo del bug de las esquinas (Lo pueden quitar)
            pygame.draw.line(pantalla, (255, 0, 0), (0, 0), (ANCHO_PANTALLA, 0), 2)  # linea superior
            pygame.draw.line(pantalla, (255, 0, 0), (0, ALTO_PANTALLA - 5), (ANCHO_PANTALLA - 5 , ALTO_PANTALLA- 5), 2)  # linea inferior

            # Mostrar el puntaje
            yourscore(score_I, score_r)

            # Mostrar el contador de tiempo restante
            mostrar_mensaje(f"Tiempo: {tiempo_restante} s", BLANCO, (ANCHO_PANTALLA - 200, 20))

            # Actualizar pantalla
            pygame.display.flip()

            # Controlar FPS
            reloj.tick(60)


        


# Iniciar el juego
bucle_juego()
