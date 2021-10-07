#------------------------------------------------------------------------------
#------- Primer trabajo: Videojuego controlado por cámara ---------------------
#------- Nombre del juego: Space Legends (Naves espaciales) -------------------
#------- Por: - Santiago Orozco Holguín           CC 1088318863 ---------------
#-------------correo: santiago.orozcoh@udea.edu.co ----------------------------
#------------ - Hugo Alejandro Cosme Valencia     CC1061805820-----------------
#-------------correo: hugo.cosme@udea.edu.co ----------------------------------
#--------Estudiantes Ingeniería Electrónica  ----------------------------------
#--------Universidad de Antioquia ---------------------------------------------
#------- Curso: Procesamiento Digital de Imágenes I ---------------------------
#------- Fecha: Abril de 2021 -------------------------------------------------
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#--1. Inicializo el sistema ---------------------------------------------------
#------------------------------------------------------------------------------

#Se importan librerías de turtle(manejo de gráficos), math, numpy (cálculos),... 
#...random(números aleatorios), opencv (PDI), time y datetime(manejo del programa) 
import turtle, math, random
import time, cv2, datetime
import numpy as np

#------------------------------------------------------------------------------
#--1. Inicialización el sistema -----------------------------------------------
#------------------------------------------------------------------------------

#---------------- Configuración de la ventana----------------------------------
wn = turtle.Screen()        #Inicializo la ventana para graficar el juego
wn.bgcolor("black")         #Color de fondo inicial sobre el que se pinta
wn.title("Space Legends")   #Título del juego se visualiza en la ventana
wn.bgpic("Assets/fondo4.png")      #Se sobrepone la imagen usandola como fondo

#---------------- Registro de las formas --------------------------------------
turtle.register_shape("Assets/enemie1.gif")    #ícono para las naves enemigas
turtle.register_shape("Assets/player.gif")     #ícono para el jugador
turtle.register_shape("Assets/rocket.gif")     #ícono para el misil

#----------------- Dibujo de los bordes ---------------------------------------
border_pen = turtle.Turtle()        #Inicializar el lápiz para dibujo del marco   
border_pen.speed(0)                 #La mayor velocidad de dibujo
border_pen.color("white")           #Seleccionar color del lápiz
border_pen.penup()                  #Para subir el lápiz (no dibujar)
border_pen.setposition(-300,-300)   #Ubicar el lápiz en la posición inicial 
border_pen.pendown()                #Para bajar el lápiz (dibujar)
border_pen.pensize(3)               #Tamaño del lápiz para el marco
for side in range(4):               #4 bordes (marco cuadrado)
    border_pen.fd(600)              #dibuje hacia delante long=600px
    border_pen.lt(90)               #Gire 90 grados el lápiz hacia la izquierda
border_pen.hideturtle()             #Ocultar el lápiz a medida que va dibujando

#--------------------- Dibujar el puntaje en la pantalla ----------------------
score = 0                           #Poner el puntaje inicial en 0
score_pen = turtle.Turtle()         #Inicializar el lápiz para dibujo del score
score_pen.speed(0)                  #La mayor velocidad de dibujo
score_pen.color("white")            #Seleccionar color del lápiz
score_pen.penup()                   #Para subir el lápiz
score_pen.setposition(-290, 280)    #Ubicar el lápiz en la posición inicial 
scorestring = "Score: %s" %score    #String con los caracteres "score"
#Se escoge el tipo de letra para escribir texto
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()              #Ocultar el lápiz a medida que va dibujando

#---------------------- Crear el objeto del jugador --------------------------
player = turtle.Turtle()            #Inicializar objeto del jugador
player.color("blue")                #Se escoge el color inicial del objeto
player.shape("Assets/player.gif")          #Se escoge la imagen de la nave principal
player.penup()                      #Preparar el lapiz para dibujar el objeto
player.speed(0)                     #Velocidad de escritura del lapiz máxima
player.setposition(0, -250)         #Seleccionar posición inicial del jugador
player.setheading(90)               #Posicionar jugador según ángulo(90=norte)

playerspeed = 20 #Velocidad de movimiento de la nave principal en la pantalla

#-------------- Empezar a agregar los enemigos a la pantalla ------------------
number_of_enemies = 5 #Escoger número de enemigos
enemies = [] #Crear una lista vacía de enemigos
for i in range(number_of_enemies):  #ciclo por cada enemigo
    enemies.append(turtle.Turtle()) #Agregando el enemigo i en pantalla
for enemy in enemies:               #ciclo for para cada las naves enemigas
    enemy.color("red")              #Se escoge el color inicial del objeto
    enemy.shape("Assets/enemie1.gif")      #Se escoge la imagen de las naves enemigas
    enemy.penup()                   #Preparar el lapiz para dibujar el objeto
    enemy.speed(0)                  #Velocidad de escritura del lapiz máxima
    x = random.randint(-200, 200)   #Posición inicial aleatoria x (full range)
    y = random.randint(100, 250)    #Posición inicial aleatoria y (mid range)
    enemy.setposition(x, y)         #Seleccionar posición inicial del enemigo

enemyspeed =3 #Velocidad de movimiento de las naves enemigas en la pantalla

#------------------- Crear el objeto del misil --------------------------------
bullet = turtle.Turtle()    #Inicializar objeto del misil
bullet.color("yellow")      #Se escoge el color inicial del objeto
bullet.shape("Assets/rocket.gif")  #Se escoge la imagen del misil
bullet.penup()              #Preparar el lapiz para dibujar el misil
bullet.speed(0)             #Velocidad de escritura del lapiz máxima
bullet.setheading(90)       #Posicionar misil según ángulo(90=norte)
bullet.hideturtle()         #Ocultar el lápiz a medida que va dibujando
#Estados del misil: "ready" (listo para disparar) y "fire"(misil en pantalla) 
bulletstate = "ready"

bulletspeed = 20 #Velocidad de movimiento del misil en la pantalla

#--------------------------------------------------------------------------
#--2. Definición de funciones----------------------------------------------
#--------------------------------------------------------------------------

#------- Función para ajustar el tamaño de la imagen (en opencv)---------------
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]                #Obtiene altura y ancho de la imagen
    if width is None and height is None:    #Si no hay valores nuevos...
        return image                        #...devuelve la misma imagen
    if width is None:                       #Si solo se ingresa la altura...
        r = height / float(h)               #...ajuste nueva altura
        dim = (int(w * r), height)          #Para que queden proporcionales
    else:                                   #Si solo se ingresa el ancho...
        r = width / float(w)                #...ajuste nuevo ancho
        dim = (width, int(h * r))           #Para que queden proporcionales
    
    resized = cv2.resize(image, dim, interpolation = inter) #redimensionar
    return resized             #Entrega la imagen con las nuevas dimensiones

#------- Función para cerrar correctamente el juego---------------
def closeGame():
    cap.release()                           #Libera espacio en memoria y desactiva camara
    cv2.destroyAllWindows()                 #Cierra todas las ventanas generadas con cv2.imshow()
    wn.clear()                              #Borra de memoria todo lo relacionado con los graficos del juego de la libreria turtle
    turtle.write("GAME OVER", move=False ,align="center", font=("Arial", 24, "normal")) #Cuando el juego acaba, aparece en pantalla "GAME OVER"
    time.sleep(3)                           #Espera 3 segundos
    wn._delete("all")                       #Borra todo lo relacionado con la ventana creada por turtle
    exit()                                 #Termina ejecucion de python
    
    
#------- Función para mover la nave a la izquierda---------------
def move_left():
    x = player.xcor()                       #Toma la posicion de la nave
    x -= playerspeed                        #Le resta 20 (playerspeed) a la posicion en X (izquierda)
    if x < -280:                            #Si la poscicion es menor a -280
        x = - 280                           #Se establece -280 como el limite
    player.setx(x)                          #Se actualiza posicion de la nave

#------- Función para mover la nave a la derecha---------------
def move_right():
    x = player.xcor()                       #Toma la posicion de la nave
    x += playerspeed                        #Le suma 20 (playerspeed) a la posicion en X (derecha)
    if x > 280:                             #Si la poscicion es mayor a 280
        x = 280                             #Se establece -280 como el limite
    player.setx(x)                          #Se actualiza posicion de la nave

#------- Función para disparar proyectil---------------
def fire_bullet():
    global bulletstate                                  #Se declara bulletstate como global para poder cambiar el valor fuera de la funcion
    if bulletstate == "ready":                          #Se pregunta por si el estado del proyectil esta en: Preparado
        bulletstate = "fire"                            #En caso afirmativo, se asigna el estado de disparo (fire)
        #winsound.PlaySound('pum.wav',winsound.SND_ASYNC)
        x = player.xcor()                               #Se toma posicion X de la nave
        y = player.ycor() + 10                          #Se toma posicion y de la nave y se suma 10 para que el misil se dispare desde el frente
        bullet.setposition(x, y)                        #Fija la posicion inicla del disparo del misil
        bullet.showturtle()                             #Inicia animacion del misil

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 25:
        return True
    else:
        return False
    
    
#Create keyboard bindings
turtle.listen()                             #Permite a turtle estar pendiente del teclado
#turtle.onkey(fire_bullet, "space")
turtle.onkey(closeGame, "Escape")           #Cierra el juego cuando se oprime la tecla esc

#--------------------------------------------------------------------------
#--3. Procesamiento de Imagen----------------------------------------------
#--------------------------------------------------------------------------

#Image detection
cap = cv2.VideoCapture(0)                       #Inicializa objeto de captura de imagen
kernel = np.ones((5,5),np.uint8)                #Crea kernel para realizar erosion y dilatacion
xa=0                                            #Variable para diferencia de posicion

#Main game loop
while True:
    _, frame = cap.read()                       #Captura frame
    frame = cv2.flip(frame, 1)                  #Efecto espejo sobre el frame

    frame3 = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)   #Cambia a espacio de colores YCrCb

    fy1 = frame3[:,:,1]                                 #Toma solo la capa 1 (roja)
    fy2 = frame3[:,:,2]                                 #Toma solo la capa 2 (azul)

    ret,bfy1 = cv2.threshold(fy1,155,255,cv2.THRESH_BINARY)      #Partiendo de un valor de rojo (umbral), se binariza la imagen  
    ret,bfy2 = cv2.threshold(fy2,145,255,cv2.THRESH_BINARY)      #Partiendo de un valor de azul (umbral), se binariza la imagen 

    bfy11 = cv2.morphologyEx(bfy1,cv2.MORPH_OPEN,kernel)          #Dilata la imagen binarizada
    bfy111 = cv2.morphologyEx(bfy1,cv2.MORPH_CLOSE,kernel)         #Erosiona la aimagen previamente dilatada para eliminar imperfecciones
    contoursRed, hierarchy = cv2.findContours(bfy111, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #Encuentra el contorno de la imagen binarizada (contorno del objeto rojo)

    bfy22 = cv2.morphologyEx(bfy2,cv2.MORPH_OPEN,kernel)          #Dilata la imagen binarizada
    bfy222 = cv2.morphologyEx(bfy2,cv2.MORPH_CLOSE,kernel)         #Erosiona la aimagen previamente dilatada para eliminar imperfecciones
    contoursBlue, hierarchy = cv2.findContours(bfy222, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #Encuentra el contorno de la imagen binarizada (contorno del objeto rojo)

    for c in contoursRed :                                      #Se recorre cada posicion del contorno 
        if cv2.contourArea(c) <= 50 :                           #Si el area del contorno es menor a 50, no se tiene en cuenta
            continue
        x, y, _, _ = cv2.boundingRect(c)                        #Toma posicion en X, Y del objeto
        if (xa-x)>0:                                            #Si la posicion anterior menos la actual del objeto es mayor a 0 (centro de pantalla), llama funcion mover a la izquierda
            move_left()
        elif (xa-x)<0:                                          #Si la posicion anterior menos la actual del objeto es mayor a 0 (centro de pantalla), llama funcion mover a la derecha
            move_right()
        xa=x
    
    cv2.drawContours(frame, contoursRed, -1, (0, 0, 255), 3)    #Dibuja el contorno del objeto rojo sobre el frame original
    
    cv2.drawContours(frame, contoursBlue, -1, (255, 0, 0), 3)   #Dibuja el contorno del objeto azul sobre el frame original

    if np.count_nonzero(np.sum(bfy2, axis=0)) > 10:             #Cuando en la imagen binarizada que hace referencia al azul no hay 
        fire_bullet()                                               #presencia de azul, no hace nada, cuando hay presencia, dispara

    frame = image_resize(frame, width = 400)                    #Reajusta el tamaño de la imagen a 400
    cv2.imshow("frame", frame)                                  #Muestra el frame original con los contornos de los objetos azul y rojo
    # cv2.imshow("Azul_Pre", bfy2)
    # cv2.imshow("Azul_Open", bfy22)
    # cv2.imshow("Azul_Close", bfy222)
    #cv2.imshow("Azul", bfy2)

    if cv2.waitKey(1) & 0xFF == ord('q'):                       #Cuando se oprime la tecla q, se cierra el programa/ventanas
        break
    
    #--------------------------------------------------------------------------
    #--X. Control de movimiento -----------------------------------------------
    #--------------------------------------------------------------------------
    
    #----------------Movimiento de naves enemigas------------------------------
    for enemy in enemies:               #Ciclo para cada enemigo
        x = enemy.xcor()                #Posición actual del enemigo en x
        x += enemyspeed                 #Aumentar con respecto a su velocidad
        enemy.setx(x)                   #Ubicar en nueva posición
        
        #Mover al enemigo hacia abajo y de vuelta (cuando llega a las paredes)
        if ((enemy.xcor() > 280) or (enemy.xcor() < -280)): 
            for e in enemies:           #Mover a los enemigos hacia abajo
                y = e.ycor()            #Retorna coordenada y actual de cada uno
                y -= 40                 #Le baja 40 pixeles a la posición en y
                e.sety(y)               #Actualiza la posicón en y (hacia abajo)
            
            enemyspeed *= -1            #Cambia la dirección de movimiento

        #Mirar si hay colisión entre el enemigo y el misil
        if isCollision(bullet, enemy):          #Si hubo colisión...
            bullet.hideturtle()                 #Ocultar el objeto misil
            bulletstate = "ready"               #Reiniciar el estado del misil
            bullet.setposition(0, -400)         #Reiniciar posición del objeto
            x = random.randint(-200, 200)       #Reposicionar nuevo enemigo en x
            y = random.randint(100, 250)        #Reposicionar nuevo enemigo en y
            enemy.setposition(x, y)             #Establecer la nueva posición
            score += 10                         #Actualizar el puntaje (+10)
            scorestring = "Score: %s" %score    #Actualizar el string de texto
            score_pen.clear()                   #Borrar anterior puntaje
            #Escribir el nuevo puntaje con el mismo tamaño de letra y alineación
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
        
        #Mirar si hay colisión entre el enemigo y el jugador
        if isCollision(player, enemy):          #Si hubo colisión...
            player.hideturtle()                 #Ocultar el objeto jugador
            enemy.hideturtle()                  #Ocultar el objeto enemigo
            closeGame()                         #Cerrar el juego (1 vida)
            break                               #Salir del main loop
    
    #--------------------- Movimiento del misil ------------------------------
    #Movimiento del misil hacia arriba
    if bulletstate == "fire":                   #Mientras se ha disparado
        y = bullet.ycor()                       #Obtener posición actual en y
        y += bulletspeed                        #Subir respecto a su velocidad
        bullet.sety(y)                          #Establecer nueva posición

    #Si el misil llega al límite superior
    if bullet.ycor() > 275:                     #Si toca el tope superior...
        bullet.hideturtle()                     #...Ocultar el objeto misil
        bulletstate = "ready"                   #Establecer nuevo estado 'listo'

#------------------------------------------------------------------------------
#-------------------------- Fin del juego -------------------------------------
#------------------------------------------------------------------------------