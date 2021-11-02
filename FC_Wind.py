# Importamos las librerías necesarias para el proyecto
import tkinter
from tkinter import messagebox
import math
import random


# Constantes
BACKGROUND_COLOR = "white"
FONT_NAME = "Courier"
VENTANA_WIDTH = 300
VENTANA_HEIGHT = 318
VENTANA_PAD_X = 0
VENTANA_PAD_Y = 0
ROSA_V_W = 300
ROSA_V_H = 318
CENTRO_X = 148
CENTRO_Y = 147
RADIO = 120
BUTTON_SIZE_X = 81
BUTTON_SIZE_Y = 50
ANGULO_STEP = 60
IMAGEN_ROSA_VIENTOS = "rosa_vientos.png"
IMAGEN_NEXT_W = "next_wind.png"
IMAGEN_LAST_W = "last_wind.png"
IMAGEN_LAST_W_D = "last_wind_dea.png"
IMAGEN_DADO = "dado.png"


# variables necesarias para trabajar con las imágenes
id_flecha_rosa = None
id_valor_dado = None
id_number_dado = None
id_canvas_last_w = None
id_canvas_last_w_d = None
valor_next_wind = 0
valor_last_wind = 0


# Variable para el diseño y movimiento de la flecha
angulo_flecha = 0
valor_dado = 0
ultimo_angulo_flecha = 0
ultimo_valor = -1
mostrando_ultimo = False

# ---------------------------- pintar flecha   ------------------------ #
def pintar_flecha(angulo, color):
    global id_flecha_rosa
    global canvas_rosa_vientos
    angulo = calcular_angulo_dibujo(angulo)
    lista_poligono = []
    # Pintamos la flecha según los datos dados de ángulo y rotación.
    punto_xy = calcular_punto_en_rotacion(RADIO, angulo)
    lista_poligono.append([punto_xy[0]+CENTRO_X, punto_xy[1]+CENTRO_Y])
    punto_xy = calcular_punto_en_rotacion(RADIO-20, angulo-10)
    lista_poligono.append([punto_xy[0]+CENTRO_X, punto_xy[1]+CENTRO_Y])
    punto_xy = calcular_punto_en_rotacion(RADIO-20, angulo-3)
    lista_poligono.append([punto_xy[0]+CENTRO_X, punto_xy[1]+CENTRO_Y])
    punto_xy = calcular_punto_en_rotacion(RADIO-80, angulo-20)
    lista_poligono.append([punto_xy[0]+CENTRO_X, punto_xy[1]+CENTRO_Y])
    punto_xy = calcular_punto_en_rotacion(RADIO-65, angulo)
    lista_poligono.append([punto_xy[0]+CENTRO_X, punto_xy[1]+CENTRO_Y])
    punto_xy = calcular_punto_en_rotacion(RADIO-80, angulo+20)
    lista_poligono.append([punto_xy[0]+CENTRO_X, punto_xy[1]+CENTRO_Y])
    punto_xy = calcular_punto_en_rotacion(RADIO-20, angulo+3)
    lista_poligono.append([punto_xy[0]+CENTRO_X, punto_xy[1]+CENTRO_Y])
    punto_xy = calcular_punto_en_rotacion(RADIO-20, angulo+10)
    lista_poligono.append([punto_xy[0]+CENTRO_X, punto_xy[1]+CENTRO_Y])
    # borramos la anterior flecha
    canvas_rosa_vientos.delete(id_flecha_rosa)
    # Pintamos el polígono con la lista de puntos
    id_flecha_rosa = canvas_rosa_vientos.create_polygon(lista_poligono, outline="blue", fill=color)    


# -------------------- calcular punto rotación ------------------------ #                                        
def calcular_punto_en_rotacion(dist_radio, angulo_rot):
    # Pasamos el ángulo a radianes
    angulo_rot = math.radians(angulo_rot)
    # Calculamos los valores de sen y coseno para calcular la trayectoria circular de los puntos.
    cos_val = math.cos(angulo_rot)
    sen_val = math.sin(angulo_rot)
    # Calculamos la posición nueva de los vértices (partimos de 0,0)
    x = dist_radio * sen_val
    y = dist_radio * cos_val      
    # Devolvemos la posición del punto.
    return [x,y]


# -------------------------- Calcular angulo para dibujar ------------- #
def calcular_angulo_dibujo(angulo_real):
    # El ángulo de dibujo del canvas difiere de nuestra forman de 
    # ver Norte, Sur, Este y Oeste, por lo que hay que hacer una
    # Conversión. Referencia -> 0 grados pinta una flecha apuntando a 180.
    angulo_pintado = angulo_real + 180
    if angulo_pintado > 360:
        angulo_pintado -= 360
    return angulo_pintado


# -------------------------- Cambiar número visible del dado ---------- #
def cambiar_texto_dado(numero_mostrar):
    # Le paso el canvas y el id del texto del dado para cambiarlo
    canvas_dado.itemconfig(id_number_dado, text=str(numero_mostrar))


# - genera la posicion para el nuevo valor seǵun las reglas del juego - #
def generar_nuevo_calculo_viento(valor_numerico):
    global angulo_flecha
    global ultimo_angulo_flecha
    # Salvo el último ángulo de flecha para consulta
    ultimo_angulo_flecha = angulo_flecha
    # Si es de 0-5 no cambia la dirección del viento.
    if (valor_numerico > 5) and (valor_numerico < 8):
        # Si es 6 o 7, cambia un punto en dir agujas reloj
        angulo_flecha -= ANGULO_STEP
        pintar_flecha(angulo_flecha, "red")
    elif valor_numerico == 8:
        # Si es 8, cambia dos punto en dir agujas reloj
        angulo_flecha -= ANGULO_STEP*2
        pintar_flecha(angulo_flecha, "red")
    elif valor_numerico == 9:
        # Si es 9, cambia un punto en dir contraria a agujas reloj        
        angulo_flecha += ANGULO_STEP
        pintar_flecha(angulo_flecha, "red")
    
# --- vuelve a mostrar la última posición del viento para consulta ---- #
def generar_antiguo_calculo_viento(angulo):
    pintar_flecha(angulo, "grey")

# ---------------------------- click next wind ------------------------ #
def click_on_cavas_next_wind(event):
    # Si hemos mostrado el último, al pulsar next, volvemos al valor actual
    # y no generamos uno nuevo.
    global valor_dado
    global ultimo_valor
    global mostrando_ultimo
    if mostrando_ultimo:
        # Indicamos que ya no estamos mostrando el último
        mostrando_ultimo = False
        pintar_flecha(angulo_flecha, "red")
        # Pinto el valor del dado
        cambiar_texto_dado(valor_dado)
        # Cambiamos el icono del botón last_valor
        canvas_last_wind.itemconfigure(id_canvas_last_w, state='normal')
        canvas_last_wind.itemconfigure(id_canvas_last_w_d, state='hidden')
    else:
        # Vemos si es el primer click a next para poner en rojo el botón last-
        if ultimo_valor == -1:
            canvas_last_wind.itemconfigure(id_canvas_last_w, state='normal')
            canvas_last_wind.itemconfigure(id_canvas_last_w_d, state='hidden')    
        # Vamos a generar un nuevo valor a mostrar
        # Guardo el último valor para consulta
        ultimo_valor = valor_dado
        # Genero un nuevo número aleatorio entre 0 y 9
        valor_dado = random.randint(0,9)
        # Actuamos según las reglas del juego
        generar_nuevo_calculo_viento(valor_dado)
        # Pinto el valor del dado
        cambiar_texto_dado(valor_dado)



# ---------------------------- click last wind ------------------------ #
def click_on_cavas_last_wind(event):
    global ultimo_valor
    global mostrando_ultimo
    # Si aún no se ha pulsado nunca next_number, no entramos aquí
    if not (ultimo_valor == -1):
        # Si ya estamos mostrando el último, no hacemos nada
        # Pinto el ultimo valor del dado
        cambiar_texto_dado(ultimo_valor)
        #actuamos según las reglas del juego
        generar_antiguo_calculo_viento(ultimo_angulo_flecha)
        # Ponemos a true que estamos mostrando el último valor
        mostrando_ultimo = True
        # Cambiamos el icono del botón last_valor
        canvas_last_wind.itemconfigure(id_canvas_last_w, state='hidden')
        canvas_last_wind.itemconfigure(id_canvas_last_w_d, state='normal')


# ---------------------------- UI SETUP ------------------------------- #
ventana = tkinter.Tk()
ventana.config(background="white")
# Lo configuro sin bordes
ventana.config(highlightthickness = 0)
# ventana.config(highlightbackground="blue")
ventana.title("Flying Colors Random Wind")
ventana.minsize(width=VENTANA_WIDTH, height=VENTANA_WIDTH)
# La configuramos para que no sea resizable
ventana.resizable(width=False, height=False)
ventana.config(padx=VENTANA_PAD_X, pady=VENTANA_PAD_Y)
# Creamos la estructura de imágenes. Primero cargamos las imágenes desde data.
carga_imgs_correcta = True
# Creo variables fuera del try para no recibir error de variables "indefinidas" fuera del try
canvas_rosa_vientos = None
canvas_next_wind = None
canvas_last_wind = None
canvas_dado = None

try:
    img_rosa_vientos = tkinter.PhotoImage(file=IMAGEN_ROSA_VIENTOS)
    img_next_w = tkinter.PhotoImage(file=IMAGEN_NEXT_W)
    img_last_w = tkinter.PhotoImage(file=IMAGEN_LAST_W)
    img_dado = tkinter.PhotoImage(file=IMAGEN_DADO)   
    img_last_w_dea = tkinter.PhotoImage(file=IMAGEN_LAST_W_D)   
except FileNotFoundError:
    # Si alguna no se puede cargar, no ejecutamos el software.
    messagebox.showinfo(title="Error", message="Error cargando las imágenes")
    carga_imgs_correcta = False
except:
    # Si alguna no se puede cargar, no ejecutamos el software.
    messagebox.showinfo(title="Error", message="Error cargando las imágenes")
    carga_imgs_correcta = False
else:
    # Creo el canvas del tamaño de la rosa de los vientos
    canvas_rosa_vientos = tkinter.Canvas(width=ROSA_V_W, heigh=ROSA_V_H)
    # Creamos e insertamos las imágenes en la ventana.
    # Es importante que la fecha esté encima de la rosa de los vientos
    canvas_rosa_vientos.create_image(ROSA_V_W/2, ROSA_V_H/2, image=img_rosa_vientos)
    canvas_rosa_vientos.config(highlightthickness = 0)
    canvas_rosa_vientos.grid(row=0, column=0, columnspan=3)
    # Seguimos con el posicionamiento de los botones_canvas para next wind o last wind
    canvas_next_wind = tkinter.Canvas(width=BUTTON_SIZE_X, heigh=BUTTON_SIZE_Y)
    canvas_next_wind.create_image(BUTTON_SIZE_X/2, BUTTON_SIZE_Y/2, image=img_next_w)
    canvas_next_wind.config(highlightthickness = 0)
    canvas_next_wind.config(background="white")
    canvas_next_wind.grid(row=1, column=2)
    canvas_last_wind = tkinter.Canvas(width=BUTTON_SIZE_X, heigh=BUTTON_SIZE_Y)
    id_canvas_last_w = canvas_last_wind.create_image(BUTTON_SIZE_X/2, BUTTON_SIZE_Y/2, image=img_last_w)
    id_canvas_last_w_d = canvas_last_wind.create_image(BUTTON_SIZE_X/2, BUTTON_SIZE_Y/2, image=img_last_w_dea)
    canvas_last_wind.config(highlightthickness = 0)
    canvas_last_wind.config(background="white")
    canvas_last_wind.grid(row=1, column=0)
    # Finalmente un canvas para el dado
    canvas_dado = tkinter.Canvas(width=BUTTON_SIZE_X, heigh=BUTTON_SIZE_Y)
    canvas_dado.create_image(BUTTON_SIZE_X/2, BUTTON_SIZE_Y/2, image=img_dado)
    canvas_dado.config(highlightthickness = 0)
    canvas_dado.config(background="white")
    canvas_dado.grid(row=1, column=1)
    # Creamos el número del dado como texto
    id_number_dado = canvas_dado.create_text(BUTTON_SIZE_X/2, BUTTON_SIZE_Y/2+5, text=valor_dado,
                                           fill="White",  font=("Courier", 18, "bold"))
# Si la carga es correcta, seguimos
if carga_imgs_correcta:
    # Hacemos el binding de ratón para detectar los clicks en lo canvas-botones.
    canvas_next_wind.bind("<Button-1>", click_on_cavas_next_wind)
    canvas_last_wind.bind("<Button-1>", click_on_cavas_last_wind)
    # Iniciamos la posición de la brújula 
    pintar_flecha(angulo_flecha, "red")
    # Entramos en el bucle del entorno gráfico
    # Main loop
    ventana.mainloop()  
else:
    messagebox.showinfo(title="Error", message="Error cargando el entorno gráfico.")
    # Salimos.
