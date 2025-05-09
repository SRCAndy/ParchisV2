import random
import json
from socket import socket, error
from threading import Thread
from settings import *

posiciones_fichas = {
    'rojo':[0, 0, 0, 0],
    'verde':[0, 0, 0, 0],
    'amarillo':[0, 0, 0, 0],
    'azul':[0, 0, 0, 0]
}

clientes = []
jugadores = []
canti_tiros = 0
pos_turno = 0
turno = ''
inicia = False

class Cliente(Thread):
    def __init__(self, s):
        Thread.__init__(self)
        self.socket = s
        self.name = ''
        self.inicia = False
        self.registrado = False
        self.cantidad_movimientos = 0
        self.combo = 0
        self.sacar_ficha = False
        self.dados = [0, 0]
        self.oportunides = 0
        self.carcel = []
    
    def enviar(self, mensaje):
        mensaje = json.dumps(mensaje)
        self.socket.send(mensaje.encode())
    
    def broadcast(self, msj, comodin = False):
        for cliente in clientes:
            if cliente.registrado or comodin:
                cliente.enviar(msj)
    
    def definir_siguiente(self):
        siguiente = False
        if self.dados[0] == self.dados[1]:
            if self.oportunides == 0:
                self.combo += 1
            if self.combo == 3:
                dict = {
                    'tipo':'sacar ficha',
                    'contenido':True
                }
                self.enviar(dict)
                self.combo = 0
                self.sacar_ficha = True
                self.cantidad_movimientos = 0
        else:
            self.combo = 0
            siguiente = True
        return siguiente
    
    def run(self):
        turno
        pos_turno
        jugadores
        inicia
        clientes
        
        while True:
            try:
                mensaje = self.socket.recv(1024).decode()
            except error:
                print(f'{self.name}:desconectado')
                if self.registrado and self in clientes:
                    index = 0
                    color = 0
                    for jugador in jugadores:
                        if jugador['nombre'] == self.name:
                            color = jugador['color']
                            break
                        index += 1
                    jugadores.pop(index)
                    dict = {
                        'tipo':'',
                        'contenido':''
                    }
                    for cliente in clientes:
                        if cliente != self:
                            if inicia:
                                if not cliente.registrado:
                                    dict['tipo'] = 'actualizar'
                                    dict['contenido'] = [jugadores, color]
                                else:
                                    dict['tipo'] = 'mueve fichas'
                                    dict['contenido'] = jugadores
                            else:
                                dict['tipo'] = 'actualizar'
                                dict['contenido'] = [jugadores, color]
                            cliente.enviar(dict)
                    if len(jugadores) == 1:
                        dict['tipo'] = 'ganador'
                        dict['contenido'] = jugadores[0]['nombre']
                        self.broadcast(dict, comodin=True)

                        for cliente in clientes:
                            if cliente.registrado:
                                cliente.name = ''
                                cliente.inicia = False
                                cliente.registrado = False
                                cliente.cantidad_movimientos = 0
                                cliente.combo = 0
                                cliente.sacar_ficha = False
                                cliente.dados = [0, 0]
                                cliente.oportunides = 0
                                cliente.carcel = []

                        pos_turno = 0
                        canti_tiros = 0
                        turno = ''
                        inicia = False
                        jugadores.clear()

                #self.socket.close()
                if self in clientes:
                    clientes.remove(self)
                break
            else:
                mensaje = json.loads(mensaje)
                tipo = mensaje['tipo']
                contenido = mensaje['contenido']

                # Los diferentes tipos de mensajes son procesados en esta parte
                # ------------------- Mensajes del cliente en la pantalla de inicio --------------#
                if not self.inicia:
                    if tipo == 'registro':
                        #Se le asignan las posiciones iniciales dependiendo del color
                        #Se agrega el jugador a la lista de jugadores en partida
                        repetido = False
                        dict = {
                                'tipo':'repetido',
                                'contenido':['Ese nombre ya esta en uso, escriba otro', False]
                            }
                        for jugador in jugadores:
                            if jugador['nombre'] == contenido['nombre']:
                                repetido = True
                                break
                        if repetido:
                            self.enviar(dict)
                        
                        else:
                            dict['contenido']=['',True]
                            self.enviar(dict)
                            color = contenido['color']
                            contenido.setdefault('fichas', carcel_fichas[color])
                            self.carcel = carcel_fichas[color].copy()
                            self.registrado = True
                            contenido.setdefault('dados',[0, 0])
                            contenido.setdefault('inicia',False)
                            jugadores.append(contenido)

                            self.name = contenido['nombre']

                            self.broadcast(mensaje, comodin=True)
                            
                            if len(jugadores) == CANTIDAD_JUGADORES:
                                mensaje = {
                                    'tipo':'info',
                                    'contenido':'La sala ya esta llena'
                                }
                                for cliente in clientes:
                                    if not cliente.registrado:
                                        cliente.enviar(mensaje)
                        
                    
                    # Cuando un cliente se conecta solicita la lista de jugadores listos
                    elif tipo == 'conexion':
                        if inicia:
                            mensaje = {
                            'tipo':'info',
                            'contenido':['Ya a iniciado la partida, espere a que esta termine para jugar',
                            jugadores]
                            }
                            self.enviar(mensaje)
                        else:
                            if len(jugadores) == CANTIDAD_JUGADORES:
                                mensaje = {
                                'tipo':'info',
                                'contenido':'La sala ya esta llena'
                                }
                                for cliente in clientes:
                                    if not cliente.registrado:
                                        cliente.enviar(mensaje)
                            else:
                                if jugadores:
                                    mensaje['contenido'] = jugadores
                                    self.enviar(mensaje)
                    
                    elif tipo == 'listo':
                        jugadores = contenido
                        dic = {
                            'tipo':'actualizar',
                            'contenido':jugadores
                        }
                        self.broadcast(dic, comodin=True)
                        if len(jugadores) >1 and len(jugadores) <= CANTIDAD_JUGADORES:
                            inicia = True
                            for jugador in jugadores:
                                if not jugador['inicia']:
                                    inicia = False
                                    break
                        
                            if inicia:
                                jugador = random.choice(jugadores)
                                pos_turno = jugadores.index(jugador)
                                turno = jugador['nombre']
                                dic = {
                                    'tipo':'iniciar juego',
                                    'contenido':turno
                                }
                                msj = json.dumps(dic).encode()
                                for cliente in clientes:
                                    if cliente.registrado:
                                        cliente.inicia = True
                                        cliente.socket.send(msj)
                                    else:
                                        dic = {
                                            'tipo':'info',
                                            'contenido':'Ya inicio la partida, espere a que esta termine para jugar'
                                        }
                                        cliente.enviar(dic)
                
                # ------------------- Mensajes del cliente una vez iniciada la partida -------------#
                else:
                    if tipo == 'registro':
                        mensaje = {
                            'tipo':'info',
                            'contenido':'Ya inicio la partida, espere a que esta termine para jugar'
                        }
                        self.enviar(mensaje)
                    elif tipo == 'conexion':
                        mensaje = {
                            'tipo':'info',
                            'contenido':['Ya inicio la partida, espere a que esta termine para jugar',
                            jugadores]
                        }
                        self.enviar(mensaje)
                    # Se determina quien inicia de primero
                    elif tipo == 'primer':
                        canti_tiros
                        dict = {
                                'tipo':'turno',
                                'contenido':''
                            }
                        canti_tiros += 1
                        jugadores[pos_turno]['dados'] = contenido
                        if canti_tiros != len(jugadores):
                            #Pasa al siguiente jugador
                            pos_turno = (pos_turno+1)%len(jugadores)
                            jugador = jugadores[pos_turno]
                            turno = jugador['nombre']    
                            dict['contenido'] = turno

                        else:
                            mayor = max(jugadores, key= lambda jugador: sum(jugador['dados']))
                            turno = mayor['nombre']
                            pos_turno = jugadores.index(mayor)
                            dict['tipo'] = 'juegue'
                            dict['contenido'] = turno
                        
                        self.broadcast(dict)
                    
                    #   Recibe el tiro de los dados del jugador
                    elif tipo == 'tiro':
                        dict = {
                            'tipo':'',
                            'contenido':''
                        }

                        jugador = jugadores[pos_turno]
                        self.dados = contenido
                        nombre = jugador['nombre']
                        afuera = True
                        if jugador['fichas'] == self.carcel and self.oportunides < OPORTUNIDADES_SALIR:
                            
                            self.oportunides += 1
                            afuera = False
                            if self.dados[0] == self.dados[1]:
                                
                                casilla = casillas[salidas[jugador['color']]]
                                jugadores[pos_turno]['fichas'] = [casilla for x in range(len(jugador['fichas']))]
                                dict['tipo'] = 'mueve fichas'
                                dict['contenido'] = jugadores
                                self.broadcast(dict)
                                self.oportunides = 0
                    
                        siguiente = False
                        if self.oportunides == OPORTUNIDADES_SALIR:
                            siguiente = True
                            self.oportunides = 0
                        elif afuera:
                            siguiente = self.definir_siguiente()
                            #------------------------------------------#
                            if jugador['fichas'] != self.carcel and not self.sacar_ficha:
                                self.sacar_ficha = False
                                
                                nombre = jugador['nombre']
                                
                                fichas = jugador['fichas']
                
                                siguiente = False
                                self.oportunides = 0
                                #-----------------------------------------#
                                ls_casillas = list(casillas.values())
                                posibles_movimientos = []
                                self.cantidad_movimientos = sum(self.dados) + 2
                                casa = casas[jugador['color']]
                                final = final_fichas[jugador['color']]
                                index_casa = ls_casillas.index(casa[0]) + 1
                                index = 0
                                for ficha in jugador['fichas']:
                                    if not ficha in self.carcel and not ficha in final:

                                        if ficha in ls_casillas and ficha != casa[0]:
                                            index = ls_casillas.index(ficha) + 1
                                        else:
                                            index = casa.index(ficha) + 1
                                        
                                        
                                        pos1 = index + self.dados[0] + 1
                                        pos2 = index + self.dados[1] + 1
                                        pos3 = index + sum(self.dados) + 2
                                        if ficha in ls_casillas and ficha != casa[0]:
                                            if pos1 >= index_casa and index <= index_casa:
                                                
                                                pos1 = pos1 - index_casa
                                                
                                                if pos1 >= len(casa):
                                                    pos1 = [-15, -15]
                                                else:
                                                    
                                                    pos1 = casa[pos1]
                                            else:
                                                if pos1 > 68:
                                                    pos1 = pos1 - 68
                                                pos1 = casillas[pos1]
                                
                                            
                                            if pos2 >= index_casa and index <= index_casa:
                                                pos2 = pos2 - index_casa
                                                if pos2 >= len(casa):
                                                    pos2 = [-15, -15]
                                                else:
                                                    
                                                    pos2 = casa[pos2]
                                            else:
                                                if pos2 > 68:
                                                    pos2 = pos2 - 68
                                                pos2 = casillas[pos2]
                                    
                                            
                                            if pos3 >= index_casa and index <= index_casa:
                                                pos3 = pos3 - index_casa
                                                if pos3 >= len(casa):
                                                    pos3 = [-15, -15]
                                                else:
                                                    
                                                    pos3 = casa[pos3]
                                            else:
                                                if pos3 > 68:
                                                    pos3 = pos3 - 68
                                                pos3 = casillas[pos3]
                                        else:
                                            pos1 -= 1
                                            pos2 -= 1
                                            pos3 -= 1
                                            if pos1 >= len(casa):
                                                pos1 = [- 15, -15]
                                            else:
                                                pos1 = casa[pos1]
                                            
                                            if pos2 >= len(casa):
                                                pos2 = [- 15, -15]
                                            else:
                                                pos2 = casa[pos2]
                                            
                                            if pos3 >= len(casa):
                                                pos3 = [- 15, -15]
                                            else:
                                                pos3 = casa[pos3]
                
                                        posibles_movimientos.append([pos1, pos2, pos3])
                                    else:
                                        posibles_movimientos.append([])
                                    movimientos = [self.dados[0]+1, self.dados[1]+1, sum(self.dados)+2]
                                sin_movimientos = False
                                for moves in posibles_movimientos:
                                    for mov in moves:
                                        if mov != [-15, -15]:
                                            sin_movimientos=True
                                            break
                                if sin_movimientos:      
                                    dict['tipo'] = 'posibilidades'
                                    dict['contenido'] = [self.cantidad_movimientos, movimientos, posibles_movimientos]

                                    self.enviar(dict)
                                else:
                                    siguiente= self.definir_siguiente()


                        if siguiente :
                            pos_turno = (pos_turno+1)%len(jugadores)
                            jugador = jugadores[pos_turno]
                            turno = jugador['nombre']
                            dict['tipo'] = 'turno'   
                            dict['contenido'] = turno
                            self.broadcast(dict)

                    #   Se mueven las fichas     
                    elif tipo == 'mover':
                        canti = contenido[0]
                        self.cantidad_movimientos -= canti

                        if self.sacar_ficha:
                            self.sacar_ficha = False

                        jugadores = contenido[1]
                        
                        jugador = jugadores[pos_turno]

                        casa = casas[jugador['color']]
                        fin = final_fichas[jugador['color']]
                        index = 0
                        # Posicionar fichas sacadas
                        for ficha in jugador['fichas']:
                            if ficha == casa[-1]:
                                jugadores[pos_turno]['fichas'][index] = fin[index]
                                break
                            index += 1

                        # Se comen las fichas
                        ls_casillas = list(casillas.values())
                        index = 0
                        for ficha in jugador['fichas']:
                            if not ficha in fin and not ficha in carcel_fichas[jugador['color']] and not ficha in casa:
                                index = ls_casillas.index(ficha) + 1
                                for player in jugadores:
                                    if player['nombre'] != jugador['nombre']:
                                        index_ficha = 0
                                        color = player['color']
                                        for f in player['fichas']:
                                            if f == ficha and not index in seguros and not index in salidas.values():
                                                player['fichas'][index_ficha] = carcel_fichas[color][index_ficha]
                                            index_ficha += 1
                                            
                        mensaje = {
                            'tipo':'mueve fichas',
                            'contenido':jugadores
                        }
                        self.broadcast(mensaje)

                        # Determinar si alguien gano el juego
                        ganador = False
                        for jugador in jugadores:
                            final = final_fichas[jugador['color']]
                            if jugador['fichas'] == final:
                                ganador = True
                                mensaje['tipo'] = 'ganador'
                                mensaje['contenido'] = jugador['nombre']
                                nombre = jugador['nombre']
                                
                                break
                        if ganador:
                            self.broadcast(mensaje, comodin=True)
                            for cliente in clientes:
                                if cliente.registrado:
                                    cliente.name = ''
                                    cliente.inicia = False
                                    cliente.registrado = False
                                    cliente.cantidad_movimientos = 0
                                    cliente.combo = 0
                                    cliente.sacar_ficha = False
                                    cliente.dados = [0, 0]
                                    cliente.oportunides = 0
                                    cliente.carcel = []
                            

                            jugadores.clear()
                            pos_turno = 0
                            canti_tiros = 0
                            turno = ''
                            inicia = False

                        else:
                            if self.cantidad_movimientos == 0 and self.combo == 0 and not self.sacar_ficha:
                                
                                if self.dados[0] != self.dados[1]:
                                    siguiente = self.definir_siguiente()
                                else:
                                    siguiente = True
                                
                                if siguiente :
                                    pos_turno = (pos_turno+1)%len(jugadores)
                                    jugador = jugadores[pos_turno]
                                    turno = jugador['nombre']
                                    dict['tipo'] = 'turno'   
                                    dict['contenido'] = turno
                                    self.broadcast(dict)
                        

def iniciar_servidor():
    s = socket()
    s.bind(("10.253.43.28", 8001))
    s.listen(4)
    print('Servidor escuchando...')
    while True:
        cli, addr = s.accept()
        cliente = Cliente(cli)
        clientes.append(cliente)
        print(f'Cliente conectado:{cliente}')
        cliente.start()
    s.close()
