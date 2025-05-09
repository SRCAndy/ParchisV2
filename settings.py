import pygame

pygame.init()
color_fondo = (225,225,225)
fondo = pygame.image.load("imagenes/tablero.png")

#Cargar ficha amarilla
ficha_amarilla = pygame.image.load("imagenes/amarillo.png")

#Cargar fichas azul
ficha_azul = pygame.image.load("imagenes/azul.png")

#Cargar ficha roja
ficha_rojo = pygame.image.load("imagenes/rojo.png")


#Cargar ficha verde
ficha_verde = pygame.image.load("imagenes/verde.png")

fichas_imagenes = {
    'amarillo':ficha_amarilla, 
    'azul':ficha_azul, 
    'verde':ficha_verde, 
    'rojo':ficha_rojo
}

#Cargar dado
Cara_dado_1 = pygame.image.load("imagenes/Dado1.png")
Cara_dado_2 = pygame.image.load("imagenes/Dado2.png")
Cara_dado_3 = pygame.image.load("imagenes/Dado3.png")
Cara_dado_4 = pygame.image.load("imagenes/Dado4.png")
Cara_dado_5 = pygame.image.load("imagenes/Dado5.png")
Cara_dado_6 = pygame.image.load("imagenes/Dado6.png")

Lista_dado = [Cara_dado_1, Cara_dado_2, Cara_dado_3, Cara_dado_4, Cara_dado_5, Cara_dado_6]

# -----------------------------------------------------------------------------------------------

ANCHO, ALTO = 750,600

WHITE = (255,255,255)

AZUL = (43,143,228)
AMARILLO = (227,227,43)
ROJO = (227,43,43)
VERDE = (43,184,43)
VERDE_LISTO = (28,171,29)
NEGRO = (0,0,0)


POS_USERNAME= (50, 200)
POS_COLORES = (50, 250)
TAMAÑO_CUADRO = 40
GRID = 50
POS_LISTA = (400, 200)

colores_parques = {
    'azul':AZUL,
    'amarillo':AMARILLO,
    'rojo':ROJO,
    'verde':VERDE
}

CANTIDAD_JUGADORES = 4
OPORTUNIDADES_SALIR = 3

BORDE_COLOR = 4

# Posiciones de cada ficha en la carcel
carcel_fichas = {
    'amarillo':[[410, 405],[450, 405],[410, 465],[450, 465]],
    'azul':[[410, 55],[450, 55],[410, 115],[450, 115]],
    'verde':[[60, 405],[100, 405],[60, 465],[100, 465]],
    'rojo':[[60,55],[100,55],[60,115],[100,115]]
}

final_fichas = {
    'verde': [[197, 296], [197, 220], [218, 255], [239, 255]], 
    'rojo': [[289, 210], [260, 217], [227, 210], [258, 241]], 
    'azul': [[303, 225], [274, 252], [303, 255], [303, 280]], 
    'amarillo': [[256, 271], [256, 287], [280, 297], [233, 297]]
}

pos_nombres = {
    'amarillo':(400, 420),
    'azul':(400, 70),
    'verde':(50 , 420),
    'rojo':(50 , 70)
}

casillas = {
    1:[318, 499],
    2:[318, 476],
    3:[318, 453],
    4:[318, 430],
    5:[318, 407],
    6:[318, 384],
    7:[318, 361],
    8:[318, 338],
    9:[338, 319],
    10:[361, 319],
    11:[384, 319],
    12:[407, 319],
    13:[430, 319],
    14:[453, 319],
    15:[476, 319],
    16:[499, 319],
    17:[499, 256],
    18:[499, 194],
    19:[476, 194],
    20:[453, 194],
    21:[430, 194],
    22:[407, 194],
    23:[384, 194],
    24:[361, 194],
    25:[338, 194],
    26:[318, 172],
    27:[318, 149],
    28:[318, 126],
    29:[318, 103],
    30:[318, 80],
    31:[318, 57],
    32:[318, 34],
    33:[318, 11],
    34:[256, 11],
    35:[192, 11],
    36:[192, 34],
    37:[192, 57],
    38:[192, 80],
    39:[192, 103],
    40:[192, 126],
    41:[192, 149],
    42:[192, 172],
    43:[172, 194],
    44:[149, 194],
    45:[126, 194],
    46:[103, 194],
    47:[80, 194],
    48:[57, 194],
    49:[34, 194],
    50:[11, 194],
    51:[11, 255],
    52:[11, 319],
    53:[34, 319],
    54:[57, 319],
    55:[80, 319],
    56:[103, 319],
    57:[126, 319],
    58:[149, 319],
    59:[172, 319],
    60:[192, 338],
    61:[192, 361],
    62:[192, 384],
    63:[192, 407],
    64:[192, 430],
    65:[192, 453],
    66:[192, 476],
    67:[192, 499],
    68:[254, 499]
}

casas = {
    'azul':[[499, 256], [476, 256], [453, 256], [430, 256], [407, 256], [384, 256], [361, 256], [338, 256], [315, 256]],
    'rojo':[[256, 11], [256, 34], [256, 57], [256, 80], [256, 103], [256, 126], [256, 149], [256, 172], [256, 195]],
    'verde':[[11, 255], [34, 255], [57, 255], [80, 255], [103, 255], [126, 255], [149, 255], [172, 255], [195, 255]],
    'amarillo':[[254, 499], [254, 476], [254, 453], [254, 430], [254, 407], [254, 384], [254, 361], [254, 338], [254, 315]]
}

seguros = [12, 17, 29, 34, 46, 51, 63, 68]

salidas = {
    'azul':22,
    'rojo':39,
    'verde':56,
    'amarillo':5
}

tam_ficha = (10, 15)