import time
import random
import threading
import tkinter as tk
from tkinter import LEFT, SUNKEN, messagebox
import tkinter.ttk as ttk
import sys

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
root.title("La cena de los filósofos")
root.geometry("745x650")
root.resizable(0,0)


#Buttons
#create a button to start the game with grid
start_button = ttk.Button(root, text="Start", command=main)
#align the button to the bottom of the window
start_button.place(relx=0.3, rely=0.95, anchor=tk.CENTER)
#create a button to pause the game
pause_button = ttk.Button(root, text="Pausar", command=root.quit)
#align the button to the bottom of the window
pause_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
#create a button to reset the game
reset_button = ttk.Button(root, text="Reset", command=root.quit)
#align the button to the bottom of the window
reset_button.place(relx=0.7, rely=0.95, anchor=tk.CENTER)
#create a button to quit the game
quit_button = ttk.Button(root, text="Quit", command=root.quit)
#align the button to the bottom of the window
quit_button.place(relx=0.9, rely=0.9, anchor=tk.CENTER)
#create a button of the credits
credits_button = ttk.Button(root, text="Créditos", command=root.quit)
#align the button to the bottom of the window
credits_button.place(relx=0.9, rely=0.95, anchor=tk.CENTER)

checkbutton_var = tk.IntVar()

#create a checkbutton with a ticked state
checkbutton = ttk.Checkbutton(root, text="Crear un log", variable=checkbutton_var)
#align the button to the bottom of the window
checkbutton.place(relx=0.1, rely=0.95, anchor=tk.CENTER)

#Frames
#create a frame to hold the buttons
frame=ttk.Frame(root,relief=SUNKEN,borderwidth=5)
frame.grid(column=0,row=2,columnspan=4,sticky=('N','S','E','W'))
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=1)
frame.rowconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)
frame.rowconfigure(2, weight=1)
frame.rowconfigure(3, weight=1)

#create a frame on the first row that is 300 pixels wide and 400 pixels high
frame1=ttk.Frame(root,width=500,height=260,relief=SUNKEN,borderwidth=5)
frame1.grid(column=0,row=0,sticky=('N','S','E','W'))

#create another frame on the second row that is 400 pixels wide and 360 pixels high
frame2=ttk.Frame(root,width=500,height=260,relief=SUNKEN,borderwidth=5)
frame2.grid(column=0,row=1,sticky=('N','S','E','W'))

#create a frame on the second column and the first row that is 100 pixels wide and 260 pixels high
frame3=ttk.Frame(root,width=300,height=260,relief=SUNKEN,borderwidth=5)
frame3.grid(column=1,row=0,sticky=('N','S','E','W'))
frame4=ttk.Frame(root,width=300,height=260,relief=SUNKEN,borderwidth=5)
frame4.grid(column=1,row=1,sticky=('N','S','E','W'))

frame1.columnconfigure(0, weight=1)
frame1.columnconfigure(1, weight=1)
frame1.columnconfigure(2, weight=1)
frame1.columnconfigure(3, weight=1)
frame1.rowconfigure(0, weight=1)
frame1.rowconfigure(1, weight=1)
frame1.rowconfigure(2, weight=1)
frame1.rowconfigure(3, weight=1)

#add a text on the frame on the first row and second column
text0=ttk.Label(frame3,text="Código de colores:",font=("Arial", 17, "bold"))
text0.grid(column=0,row=0,sticky=('N','S','E','W'))
text1=ttk.Label(frame3,text="Filósofo entra a comer",font=("Arial",15))
text1.grid(column=0,row=2,sticky=('N','S','E','W'))
text2=ttk.Label(frame3,text="Filosofo tiene un tenedor",font=("Arial",15))
text2.grid(column=0,row=3,sticky=('N','S','E','W'))
text3=ttk.Label(frame3,text="Filósofo esta comiendo",font=("Arial",15))
text3.grid(column=0,row=4,sticky=('N','S','E','W'))
text4=ttk.Label(frame3,text="Filósofo esta pensando",font=("Arial",15))
text4.grid(column=0,row=5,sticky=('N','S','E','W'))
text5=ttk.Label(frame3,text="Tenedor ocupado",font=("Arial",15))
text5.grid(column=0,row=6,sticky=('N','S','E','W'))
text6=ttk.Label(frame3,text="Tenedor libre",font=("Arial",15))
text6.grid(column=0,row=7,sticky=('N','S','E','W'))

#add a text on the frame on the first row and second column
text7=ttk.Label(frame4,text="Cuántas veces han comido:",font=("Arial", 17, "bold"))
text7.grid(column=0,row=0,sticky=('N','S','E','W'))

text8=ttk.Label(frame4,text="Filósofo 1:",font=("Arial",15))
text8.grid(column=0,row=2,sticky=('N','S','E','W'))
#create a text box next to text8 that will hold the number of times the philosopher 1 has eaten
text8_1=ttk.Entry(frame4,width=5)
text8_1.grid(column=1,row=2,sticky=('N','S','E','W'))



text9=ttk.Label(frame4,text="Filosofo 2:",font=("Arial",15))
text9.grid(column=0,row=3,sticky=('N','S','E','W'))
text10=ttk.Label(frame4,text="Filósofo 3:",font=("Arial",15))
text10.grid(column=0,row=4,sticky=('N','S','E','W'))
text11=ttk.Label(frame4,text="Filósofo 4:",font=("Arial",15))
text11.grid(column=0,row=5,sticky=('N','S','E','W'))
text12=ttk.Label(frame4,text="Filósofo 5:",font=("Arial",15))
text12.grid(column=0,row=6,sticky=('N','S','E','W'))







#stop the mainloop when the window is closed
root.mainloop()
#close the program
sys.exit()



if __name__=="__main__":
    main()
