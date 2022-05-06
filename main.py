import time
import random
import threading
import tkinter as tk
from tkinter import LEFT, messagebox
import tkinter.ttk as ttk

N = 5
TIEMPO_TOTAL = 3

class filosofo(threading.Thread):
    semaforo = threading.Lock() #SEMAFORO BINARIO ASEGURA LA EXCLUSION MUTUA
    estado = [] #PARA CONOCER EL ESTADO DE CADA FILOSOFO
    tenedores = [] #ARRAY DE SEMAFOROS PARA SINCRONIZAR ENTRE FILOSOFOS, MUESTRA QUIEN ESTA EN COLA DEL TENEDOR
    count=0

    def __init__(self):
        super().__init__()      #HERENCIA
        self.id=filosofo.count #DESIGNA EL ID AL FILOSOFO
        filosofo.count+=1 #AGREGA UNO A LA CANT DE FILOSOFOS
        filosofo.estado.append('PENSANDO') #EL FILOSOFO ENTRA A LA MESA EN ESTADO PENSANDO
        filosofo.tenedores.append(threading.Semaphore(0)) #AGREGA EL SEMAFORO DE SU TENEDOR( TENEDOR A LA IZQUIERDA)
        print("FILOSOFO {0} - PENSANDO".format(self.id))

    def __del__(self):
        print("FILOSOFO {0} - Se para de la mesa".format(self.id))  #NECESARIO PARA SABER CUANDO TERMINA EL THREAD

    def pensar(self):
        time.sleep(random.randint(0,5)) #CADA FILOSOFO SE TOMA DISTINTO TIEMPO PARA PENSAR, ALEATORIO

    def derecha(self,i):
        return (i-1)%N #BUSCAMOS EL INDICE DE LA DERECHA

    def izquierda(self,i):
        return(i+1)%N #BUSCAMOS EL INDICE DE LA IZQUIERDA

    def verificar(self,i):
        if filosofo.estado[i] == 'HAMBRIENTO' and filosofo.estado[self.izquierda(i)] != 'COMIENDO' and filosofo.estado[self.derecha(i)] != 'COMIENDO':
            filosofo.estado[i]='COMIENDO'
            filosofo.tenedores[i].release()  #SI SUS VECINOS NO ESTAN COMIENDO AUMENTA EL SEMAFORO DEL TENEDOR Y CAMBIA SU ESTADO A COMIENDO

    def tomar(self):
        filosofo.semaforo.acquire() #SEÑALA QUE TOMARA LOS TENEDORES (EXCLUSION MUTUA)
        filosofo.estado[self.id] = 'HAMBRIENTO'
        self.verificar(self.id) #VERIFICA SUS VECINOS, SI NO PUEDE COMER NO SE BLOQUEARA EN EL SIGUIENTE ACQUIRE
        filosofo.semaforo.release() #SEÑALA QUE YA DEJO DE INTENTAR TOMAR LOS TENEDORES (CAMBIAR EL ARRAY ESTADO)
        filosofo.tenedores[self.id].acquire() #SOLO SI PODIA TOMARLOS SE BLOQUEARA CON ESTADO COMIENDO

    def soltar(self):
        filosofo.semaforo.acquire() #SEÑALA QUE SOLTARA LOS TENEDORES
        filosofo.estado[self.id] = 'PENSANDO'
        self.verificar(self.izquierda(self.id))
        self.verificar(self.derecha(self.id))
        filosofo.semaforo.release() #YA TERMINO DE MANIPULAR TENEDORES

    def comer(self):
        print("FILOSOFO {} COMIENDO".format(self.id))
        time.sleep(2) #TIEMPO ARBITRARIO PARA COMER
        print("FILOSOFO {} TERMINO DE COMER".format(self.id))

    def run(self):
        for i in range(TIEMPO_TOTAL):
            self.pensar() #EL FILOSOFO PIENSA
            self.tomar() #AGARRA LOS TENEDORES CORRESPONDIENTES
            self.comer() #COME
            self.soltar() #SUELTA LOS TENEDORES

def main():
    lista=[]
    for i in range(N):
        lista.append(filosofo()) #AGREGA UN FILOSOFO A LA LISTA

    for f in lista:
        f.start() #ES EQUIVALENTE A RUN()

    for f in lista:
        f.join() #BLOQUEA HASTA QUE TERMINA EL THREAD

#create a window
root = tk.Tk()
root.title("Filosofos")
root.geometry("700x700")

#Buttons
#create a button to start the game
start_button = ttk.Button(root, text="Start", command=main)
start_button.pack()
#align the button to the bottom of the window
start_button.place(relx=0.3, rely=0.95, anchor=tk.CENTER)
#create a button to pause the game
pause_button = ttk.Button(root, text="Pausar", command=root.quit)
pause_button.pack()
#align the button to the bottom of the window
pause_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
#create a button to reset the game
reset_button = ttk.Button(root, text="Reset", command=root.quit)
reset_button.pack()
#align the button to the bottom of the window
reset_button.place(relx=0.7, rely=0.95, anchor=tk.CENTER)
#create a button to quit the game
quit_button = ttk.Button(root, text="Quit", command=root.quit)
quit_button.pack()
#align the button to the bottom of the window
quit_button.place(relx=0.9, rely=0.9, anchor=tk.CENTER)
#create a button of the credits
credits_button = ttk.Button(root, text="Créditos", command=root.quit)
credits_button.pack()
#align the button to the bottom of the window
credits_button.place(relx=0.9, rely=0.95, anchor=tk.CENTER)




#stop the mainloop when the window is closed
root.mainloop()
#close the window
root.destroy()













tk.mainloop()

if __name__=="__main__":
    main()
