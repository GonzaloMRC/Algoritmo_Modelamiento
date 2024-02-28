
#----------------------------------------------------------------------------------------------------------------------------------------
#Librerias
#----------------------------------------------------------------------------------------------------------------------------------------

from re import X
from numpy.core.fromnumeric import size #Probar 2200167
from numpy.ma.core import count
import math
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import style

# ----------------------------------------------------------------------------------------------------------------------------------------
#Funciones
#----------------------------------------------------------------------------------------------------------------------------------------

# Función para calcular número de vueltas en octavos, siendo una vuelta equivalente a 8
def vueltas_a_octavos(vr): return 8 * vr #Cambiado de funcion de Renee

#Función para calcular longitud, siendo util para hallar las longitudes de la primera y última vuelta
def longitud_extremo(tipo_extrm,luz,d_al): #Cambiado de funcion de Renee
  long = 0
  if (tipo_extrm == "TASE"):
    long = luz + d_al
  elif (tipo_extrm == "TAE"):
    long = luz + 0.5*d_al #Cambiado de funcion de Renee
  elif (tipo_extrm == "TCSE"):
    long = d_al #Cambiado de funcion de Renee
  elif (tipo_extrm == "TCE"):
    long = 0.5*d_al #Cambiado de funcion de Renee
  return long

  #Función para calcular el ángulo pi*n, siendo una vuelta 2pi o lo que sería 8pi/4
    # m es el numero de vueltas y t_ant es el angulo inicial -> cambio de variables
    # t_max es el angulo final obtenido
def tramo_a_angulo(n_octavos, angulo_inicial):
  t = 0
  t_max = (math.pi/4)*n_octavos + angulo_inicial
  return t_max #todo ok

  #Función para ubicar el tramo. Dentro de los 5 mencionados al inicio de este codigo
def ubicar_tramo(angulo,cero,uno,dos,tres,cuatro,cinco):
  posicion = 0
  if(angulo > cero and angulo <= uno):
    posicion = 1
  if(angulo > uno and angulo <= dos):
    posicion = 2
  if(angulo > dos and angulo < tres):
    posicion = 3
  if(angulo >= tres and angulo < cuatro):
    posicion = 4
  if(angulo >= cuatro and angulo < cinco):
    posicion = 5
  return posicion #todo ok

  #Función para setear cantidad de nodos. Siendo esta cantidad tal que se puedan separar los numeros cada pi/4 múltiplos. Es decir cada pi/4 o pi/8 o pi/16 , etc..
def n_nodos_multiploPi4(ang_fin,ang_inicio,grado):
  m = ang_fin - ang_inicio
  a = pow(2,grado + 2)
  n_previa = (m * a)/math.pi
  n = round(n_previa)
  return n #me cuesta entender pero ok

  #Función de la secante. Método de la secante, con esto se halla el x (i+1) de la serie
def f_secante(xi,xiprev,f_xi,f_xiprev):
  solucion = xi - ((f_xi * (xiprev - xi)) / (f_xiprev - f_xi))
  return solucion #Metodos numericos / ok

#Ordenamiento burbuja, ordena en ascendente los pares del arreglo basado en el segundo elemento de cada par (?)
def ord_burbuja(arreglo):
  arreglo_ord = []
  arreglo_ord = arreglo
  n = len(arreglo_ord)
  for i in range(n-1):       # <-- bucle padre
    for j in range(n-1-i): # <-- bucle hijo
      if arreglo_ord[j][1] > arreglo_ord[j+1][1]:
        arreglo_ord[j], arreglo_ord[j+1] = arreglo_ord[j+1], arreglo_ord[j]
  return arreglo_ord #Ordenamiento burbuja, ordena en ascendente los pares del arreglo basado en el segundo elemento de cada par (?)


#----------------------------------------------------------------------------------------------------------------------------------------
#Inicio de codigo
#----------------------------------------------------------------------------------------------------------------------------------------

#Ingreso de datos

flag = 0 #flag
while (flag == 0):  #loop para datos ingresados, si no es conforme se vuelven a ingresar todos los datos
  print("Ingrese medidas en mm")
  d_str = input("Diámetro del alambre: ") #Pide diametro de alambre - string
  d = float(d_str) #Guarda valor ingresado en d - valor numerico
  d_alambre = d #Copia d en d_alambre <- Creo que es inutil

  D_str = input("Diámetro exterior: ")
  D = float(D_str) #Guarda valor ingresado en D

  d1_str = input("Diámetro interior 1 (Ingrese 0 si no cuenta con reducción): ")
  d1 = float(d1_str) #Guarda valor ingresado en d1

  d2_str = input("Diámetro interior 2 (Ingrese 0 si no cuenta con reducción): ")
  d2 = float(d2_str) #Guarda valor ingresado en d2

  L_str = input("Longitud: ")
  L = float(L_str) #Guarda valor ingresado en L

  N_str = input("Número de vueltas: ")
  N = float(N_str) #Guarda valor ingresado en N


  Luz_1 = -0.1 #Funciona de flag
  while Luz_1<0: #Loop para verificar que se ingrese un tipo de extremo correcto sin que crashee el codigo
    E1 = input("Extremo 1 (TASE, TAE, TCSE o TCE): ")  #indicacion de las respuestas esperadas
    if (E1 == "TASE" or E1 == "TAE"):
      Luz1_str = input("Luz 1: ")  #Podria haber verificacion de que luz ingresada no sea 0
      Luz_1 = float(Luz1_str)
    elif (E1 == "TCSE" or E1 == "TCE"):
      Luz_1 = 0
    else:
      Luz_1 = -0.1
      print("No valido, ingrese tipo de extremo")

  if (d1 > 0):  #Se definen las vueltas reducidas, si se ingresa Dint=0 se entiende sin vuelta reducida
    vred1_str = input("Vueltas reducidas del d1: ")
    vred1 = float(vred1_str)
  else:
    vred1 = 0.0

  Luz_2 = -0.1
  while Luz_2<0:#Loop para verificar que se ingrese un tipo de extremo correcto sin que crashee el codigo
    E2 = input("Extremo 2 (TASE, TAE, TCSE o TCE): ")  #indicacion de las respuestas esperadas
    if (E2 == "TASE" or E2 == "TAE"):
      Luz2_str = input("Luz 2: ")  #Podria haber verificacion de que luz ingresada no sea 0
      Luz_2 = float(Luz2_str)
    elif (E2 == "TCSE" or E2 == "TCE"):
      Luz_2 = 0
    else:
      Luz_2 = -0.1
      print("No valido, ingrese tipo de extremo")

  if (d2 > 0): #Se definen las vueltas reducidas, si se ingresa Dint=0 se entiende sin vuelta reducida
    vred2_str = input("Vueltas reducidas del d2: ")
    vred2 = float(vred2_str)
  else:
    vred2 = 0.0

  grado_str = input("Grado de resolución (1/2/3...):") #Grado de resolución para la cantidad de puntos a graficar
  grado = float(grado_str)

 #Se agrega un verificador de todos los datos ingresados, formato similar a lo usado en el trabajo
  print(f"""
  Ingreso:
  {d} x {D} x {L} x {N}
  {E1} L={Luz_1}mm c./{vred1} vta.red. a {d1}mm int
  {E2} L={Luz_2}mm c./{vred2} vta.red. a {d2}mm int
  """)

  conforme = "a" #flag, en caso de ingreso de respuesta no valida solo se pide nueva respuesta de conformidad
  while (conforme != "si" and conforme != "no"): #loop para verificar que se verifican los datos ingresados, si no es conforme se vuelven a ingresar todos los datos
    conforme = input("¿De acuerdo con todos los datos? (si/no):")
    if (conforme=="si" or conforme=="Si"or conforme=="SI" or conforme=="sí" or conforme=="SÍ" or conforme=="Sí" or conforme=="sI" or conforme=="sÍ" or conforme=="y" or conforme=="Y"):
      conforme = "si" #se actualizan los flags de ambos loops
      flag = 1
    elif (conforme == "no" or conforme == "No" or conforme == "NO"  or conforme == "nO"):
      conforme = "no" #Se pide nuevamente ingreso de datos por datos no conformes
      print ("Ingrese datos nuevamente")

#----------------------------------------------------------------------------------------------------------------------------------------
#Calculos
#----------------------------------------------------------------------------------------------------------------------------------------

#Obtención de valores útiles para los cálculos internos
if ((E1=="TASE" or E1 == "TAE") and (E2=="TASE" or E2 == "TAE") ):
  Lt = L - d #Longitud total, como marca en soliworks
elif ( ((E1=="TASE" or E1 == "TAE") and (E2=="TCSE" or E2 == "TCE")) or ((E1=="TCSE" or E1=="TCE") and (E2=="TASE" or E2=="TAE"))):
  Lt = L - 0.5*d #Longitud total, como marca en soliworks
elif ((E1=="TCSE" or E1 == "TCE") and (E2=="TCSE" or E2 == "TCE")):
  Lt = L #Longitud total, como marca en soliworks

Nt = 8 * N #Numero total de vueltas, pasado a octavos

#Longitud de tramos
L1 = longitud_extremo(E1,Luz_1,d) #1era vuelta (Extremo 1)
L3 = longitud_extremo(E2,Luz_2,d) #Ultima vuelta (Extremo 2)
L2 = Lt - L1 - L3        #Longitud del cuerpo

#Diámetro medio
Dm = D - d    #Diámetro constante

#A evaluar, numeros sacados del aire:
#Buscar iterar esto
p0 = 0 #paso inicial, seteo (paso intantáneo en el que empieza el extremo inicial del resorte)
pf = 5 # paso final, seteo (paso intantáneo en el que acaba el extremo final del resorte)
paso_2 = 30 #seteo (limite inferior del rango para evaluar el paso constante del cuerpo del resorte)(Valor obtenido en base a la tendencia en fabricaciones TRANSMETA)
paso_2_final = 70 #seteo (limite superior del rango para evaluar el paso constante del cuerpo del resorte)(Valor obtenido en base a la tendencia en fabricaciones TRANSMETA)(Puede llegar a 70, probar luego)
p = 0 #parametro que da inicio a la iteracion
#No se ha definido este dato, pero para fines prácticos se tomará media vuelta
nc1 = 0.5 #numero de vueltas adicionales (> 1) antes del paso constante
nc2 = 0.5 #numero de vueltas despues del paso constante (< N - 1)
n1 = 1 #primera vuelta otorgamos 1 vuelta entera para el primer paso
n3 = 1 #ultima vuelta otorgamos 1 vuelta entera para el ultimo paso

pi = round(math.pi,5)#define pi como constante

#---------------------------------------------------------------------------------------------------------------------------------------------------------
#Cálculo DIRECTO del paso ideal del cuerpo del Resorte

#Formulas explicadas en Docs Guía

#Numero de vueltas por tramo
x1 = 1
x2 = nc1
x4 = nc2
x5 = 1
x3 = N - x1 - x2 - x4 - x5

Ncalculado = x1+x2+x3+x4+x5 #verificador

J = (L2 - (2*L3-pf+p0-2*L1)*nc1/2 - 2*(L1-p0)*nc1 - (2*L3-pf)*(N-2-nc1-nc2) - (2*L3-pf)*nc2)/(nc1*nc2 + 2*nc2*(N-2-nc1-nc2) + pow(nc2,2)) #Factor calculado para otros calculos
I = (2*J*nc2 + 2*L3 - pf + p0 - 2*L1)/(2*nc1) #Factor calculado para otros calculos
K = 2*J*nc2+2*L3-pf #Paso ideal

#Pasos calculados por tramo
P1 = 2*L1 - p0
P2 = 2*I*nc1 + 2*L1 - p0
P4 = 2*J*nc2 + 2*L3 - pf
P5 = 2*L3 - pf

#Alturas calculadas por tramo
y1 = (L1-p0)*x1*x1 + p0*x1
y2 = I*x2*x2 + P1*x2
y3 = K*x3
y4 = J*x4*x4 + P5*x4
y5 = (L3-pf)*x5*x5 + pf*x5

#Altura total según cálculos
y_total = y1+y2+y3+y4+y5

#Impresión de datos para monitoreo
print("P2: ", P2)
print("P4: ", P4)
print("K: ", K)
print("Vueltas calculadas (Verificación): ", Ncalculado)
print("Altura calculada: ", y_total)
print("y1: ", y1)
print("y2: ", y2)
print("y3: ", y3)
print("y4: ", y4)
print("y5: ", y5)
print("y_total: ",y_total)

#---------------------------------------------------------------------------------------------------------------------------
#Defino mis ecuaciones de tramo, tomando como el paso constante el hallada mediante el método de la secante

#Numero de vueltas en cada tramo, se cuentan cuantos 1/8 x vuelta hay
N1 = vueltas_a_octavos(n1) #Primera vuelta
Nc1 = vueltas_a_octavos(nc1) #paso variable 1
N3 = vueltas_a_octavos(n3) #Última vuelta
Nc2 = vueltas_a_octavos(nc2) #paso variable 2
N2 = Nt - N1 - Nc1 - N3 - Nc2 #paso constante

#Ángulo máximo de cada tramo --- guarda los angulos correspondientes a cada tramo/define tramos
t1_max = tramo_a_angulo(N1,0) #ángulo con el que termina la primera vuelta
tNc1_max = tramo_a_angulo(Nc1,t1_max)#ángulo con el que termina el tramo de paso ascendente
t2_max = tramo_a_angulo(N2,tNc1_max)#ángulo con el que termina el tramo de paso constante
tNc2_max = tramo_a_angulo(Nc2,t2_max)#ángulo con el que termina el tramo de paso descendente
t3_max = tramo_a_angulo(N3,tNc2_max)#ángulo con el que termina la última vuelta

#Ecuaciones por tramo, partiendo del eje "Z"
#Genera nodos/puntos a lo largo de ciertas secciones de una curva para el modelado, np.linspace genera un arreglo de numeros igualmente espaciado en el rango especificado.
t1 = np.linspace(0,t1_max,100) #nodos x cada tramo
tNc1 = np.linspace(t1_max,tNc1_max,100)
t2 = np.linspace(tNc1_max,t2_max,400)
tNc2 = np.linspace(t2_max,tNc2_max,100)
t3 = np.linspace(tNc2_max,t3_max,100)

#Formulas explicadas en Docs Guía
paso0 = p0
paso1_calc = 2*(L1-p0)*x1+p0
altura1_calc = (L1-p0)*pow(1,2)+p0*1
paso2_calc = 2*I*x2+paso1_calc
altura2_calc = L1 + I*pow(x2,2)+paso1_calc*x2
paso3_calc = K
altura3_calc = altura2_calc + K*x3
paso4_calc = K
paso5_calc = 2*(L3-pf)*x5+pf
altura4_calc = altura3_calc + J*pow(x4,2)+paso5_calc*x4

t_1 = t1_max
t_Nc1 = tNc1_max
t_2 = t2_max
t_Nc2 = tNc2_max
t_3 = t3_max


#--------------------------------------------------------------------------------
#Vuelvo a definir las ecuaciones, tomando en cuentas las reducciones

#Numero de vueltas de las vueltas reducidas #Formulas explicadas en Docs Guía
if (d1 > 0): #Para Extremo 1
  N_vr1 = vueltas_a_octavos(vred1) #vueltas reducidas de E1 a octavos
  t_vr1 = round((math.pi/4)*N_vr1,5) #Ángulo para ese tramo reducido - angulo tope
  Dm_vr1 = d1 + d #Dm = Dint + d , dm de vuelta reducida
  t_vr_1 = t_vr1 - math.pi #no entiendo (angulo tope menos media vuelta)
  C1 = (Dm - Dm_vr1) / (2 * t_vr_1) #no entiendo
else:
  N_vr1 = 0
  Dm_vr1 = Dm
  C1 = 0
  t_vr1 = round(t_1,5)

if (d2 > 0):
  N_vr2 = vueltas_a_octavos(vred2)
  t_vr2 = round(t_3 - (math.pi/4)*N_vr2,5) #Dif de angulo final - angulo del tramo -> angulo tope
  Dm_vr2 = d2 + d
  t_vr_2 = (math.pi/4)*N_vr2 - math.pi+0.001 #V.red de E2 no podia ser 0.5
  C2 = (Dm - Dm_vr2) / (2 * t_vr_2)

else:
  N_vr2 = 0
  Dm_vr2 = Dm
  C2 = 0
  t_vr2 = round(t_Nc2,5)

#Contador de nodos totales basado en input de grado
n_1 = n_nodos_multiploPi4(t_1,0,grado + 2) #nodos por tramo
n_2 = n_nodos_multiploPi4(t_Nc1,t_1,grado + 2)
n_3 = n_nodos_multiploPi4(t_2,t_Nc1,grado + 2)
n_4 = n_nodos_multiploPi4(t_Nc2,t_2,grado + 2)
n_5 = n_nodos_multiploPi4(t_3,t_Nc2,grado + 2)

nodos_totales = n_1 + 1 + n_2 + n_3 + n_4 + n_5

print("Cantidad de nodos totales será de: ") #Información para usuario
print(nodos_totales)

#Ecuaciones por tramo, partiendo el eje y en 5 tramos
ang_t1 = np.linspace(0,t_1,n_1 + 1) #nodos x cada tramo
ang_t1_2 = [] #se crea lista vacia
for i in ang_t1: #se itera sobre cada nodo generado y redondea el resultado a 5 dec.
  truncado = round(i,5)
  ang_t1_2.append(truncado) #se agrega a la lista de nodos

#se repite la creacion de los arrays de nodos redondeados para todos los tramos
ang_tNc1 = np.linspace(t_1,t_Nc1,n_2 + 1)
ang_tNc1_2 = []
for i in ang_tNc1:
  truncado = round(i,5)
  ang_tNc1_2.append(truncado)

ang_t2 = np.linspace(t_Nc1,t_2,n_3 + 1)
ang_t2_2 = []
for i in ang_t2:
  truncado = round(i,5)
  ang_t2_2.append(truncado)

ang_tNc2 = np.linspace(t_2,t_Nc2,n_4 + 1)
ang_tNc2_2 = []
for i in ang_tNc2:
  truncado = round(i,5)
  ang_tNc2_2.append(truncado)

ang_t3 = np.linspace(t_Nc2,t_3,n_5 + 1)
ang_t3_2 = []
for i in ang_t3:
  truncado = round(i,5)
  ang_t3_2.append(truncado)

#Lo pasamos a lista estos array, para poder obtener las posiciones de ciertos elementos
#No me hace mucho sentido esta parte del codigo, solo iguala las vriables, no los conviertia a lista, considerar descartar
list_t1 = list(ang_t1_2)#se pasa a lista, el resultado es lo mismo parece
list_tNc1 = list(ang_tNc1_2)#.tolist()
list_t2 = list(ang_t2_2)#.tolist()
list_tNc2 = list(ang_tNc2_2)#.tolist()
list_t3 = list(ang_t3_2)#.tolist()
print(list_t1)
#print(list_tNc1)
pos_1 = list_t1.index(pi)
ang_t0_5 = np.linspace(0,math.pi,pos_1 + 1) #primera media vuelta (0 a 0.5)
ang_t1_5 = np.linspace(math.pi,t_1,pos_1 + 1) #resto de la primera vuelta (0.5 a 1)
medio_final = round(t_3 - math.pi,5)
pos_2 = list_t3.index(medio_final)
ang_tN_0 = np.linspace(t_Nc2,medio_final,pos_2 + 1)#penúltima media vuelta (N - 1 a N - 0.5)
ang_tN_5 = np.linspace(medio_final,t_3,pos_2 + 1)#última media vuelta(N - 0.5 a N)

#Vectores para las coordenadas, dudo que se use todo
coord_x1 = []
coord_y1 = []
coord_z1 = []
coord_x2 = []
coord_y2 = []
coord_z2 = []
coord_x3 = []
coord_y3 = []
coord_z3 = []
coord_x4 = []
coord_y4 = []
coord_z4 = []
coord_x5 = []
coord_y5 = []
coord_z5 = []

coord1_x1 = []
coord1_y = []
coord1_z1 = []
coord1_x2 = []
coord1_z2 = []
coord1_x3 = []

coord1_z3 = []
coord1_x4 = []
coord1_y4 = []
coord1_z4 = []
coord1_x5 = []
coord1_z5 = []
coord2_y = []

#Vector de pasos
Pi = []

#Tramo 1 #vuelta 0 a vuelta 1 #y = ax^2 + bx
for a in ang_t1: #itera sobre cada valor en array ang_t1
  Ni_1 = a/(2*math.pi) #posicion angular de un punto entre 360 para hallar su "posicion en la vuelta"
  Pi_1 = 2*(L1-p0)*Ni_1+p0 #Paso basado en posición angular, define trayectoria de la curva a traves del paso
  y_1_decimal = (L1-p0)*pow(Ni_1,2)+p0*Ni_1 #Calcula la coordenada y en formato decimal para el valor actual de Ni_1 utilizando la ecuación y=ax^2+bx
  y_1 = round(y_1_decimal,6) #Redondea el valor de y_1_decimal a 6 decimales y lo asigna a y_1.
  coord1_y.append(y_1) # Agrega el valor de y_1 a la lista coord1_y, que probablemente almacena las coordenadas y de la trayectoria.
  Pi.append(Pi_1) #Agrega el valor de Pi_1 a la lista Pi, que probablemente almacena los puntos de la trayectoria en el eje y.

altura1 = coord1_y[len(coord1_y)-1] #altura se obtiene leyendo el final de la coordenada
print("altura1: ", altura1)
paso1 = Pi[len(Pi)-1] #paso se obtiene leyendo el final ultimo elemento del paso

#Comentarios se repiten
#Tramo 2 #vuelta 1 a la vuelta donde comienza el paso constante #y = ax2 + bx
for b in ang_tNc1:
 Ni_2 = (b-ang_t1[len(ang_t1)-1])/(2*math.pi)
 Pi_2 = 2*I*Ni_2+paso1
 y_2_decimal = altura1 + I*pow(Ni_2,2)+paso1*Ni_2
 y_2 = round(y_2_decimal,6)
 if (b > ang_tNc1[0]): #se utiliza para no agregar valores en el inicio de la trayectoria
  coord1_y.append(y_2)
  Pi.append(Pi_2)

altura2 = coord1_y[len(coord1_y)-1]
print("altura2: ", altura2)
paso2 = Pi[len(Pi)-1]

#Tramo 3 #el tramo donde el paso es constante y = mx + b
for c in ang_t2:
  Ni_3 = (c-ang_tNc1[len(ang_tNc1)-1])/(2*math.pi)
  Pi_3 = paso2
  y_3_decimal = altura2 + paso2*(Ni_3)
  y_3 = round(y_3_decimal,6)
  if (c > ang_t2[0]):
   coord1_y.append(y_3)
   Pi.append(Pi_3)

altura3 = coord1_y[len(coord1_y)-1]
print("altura3: ", altura3)
paso3 = Pi[len(Pi)-1]

#Tramo 5 #la vuelta N-1 a vuelta N # y = ax2 + bx
arreglo_Pi_5_creciente = [] #Se crean arreglos/listas
arreglo_y_5_decimal_creciente = []
for e in ang_t3: #iteracion para todos los elementos del arreglo del tramo 3
  Ni_5 = (e - ang_tNc2[len(ang_tNc2)-1])/(2*math.pi) #"Vuelta" en la que se encuentra en relacion al angulo en el que esta
  Pi_5_creciente = 2*(L3-pf)*Ni_5+pf #Valor variable del paso de la curva
  y_5_decimal_creciente = (L3-pf)*pow(Ni_5,2)+pf*Ni_5 #Altura o coord.y del tramo
  if (e < ang_t3[len(ang_t3)-1]): #Verifica si aun no se llega al final del tramo
    arreglo_y_5_decimal_creciente.append(y_5_decimal_creciente) #Se agregan los valores respectivos a la lista
    arreglo_Pi_5_creciente.append(Pi_5_creciente)

paso5 = arreglo_Pi_5_creciente[len(arreglo_Pi_5_creciente)-1] #Se asigna el ultimo valor del arreglo a "paso5"

#Se repiten comentarios
#Tramo 4 #la vuelta donde termina el paso constante a la vuelta N-1 # y = ax2 + bx
#paso4_abajo = J*pow(nc2,2)+L3*nc2
arreglo_Pi_4_creciente = []
arreglo_y_4_decimal_creciente = []
for d in ang_tNc2:
  Ni_4 = (d- ang_t2[len(ang_t2)-1])/(2*math.pi)
  Pi_4_creciente = 2*J*Ni_4+paso5
  y_4_decimal_creciente = J*pow(Ni_4,2) + (2*L3 - pf) * Ni_4
  if (d < ang_tNc2[len(ang_tNc2)-1]):
    arreglo_y_4_decimal_creciente.append(y_4_decimal_creciente)
    arreglo_Pi_4_creciente.append(Pi_4_creciente)

paso4 = arreglo_Pi_4_creciente[len(arreglo_Pi_4_creciente)-1]



#Agregando el Tramo 4 al arreglo de coordenadas y (Se agrega de forma decreciente y se resta)
v = 0
altura_tramo4 = arreglo_y_4_decimal_creciente[len(arreglo_y_4_decimal_creciente)-1] - arreglo_y_4_decimal_creciente[0] #Altura del tramo 4
altura3_toerico = y1+y2+y3 #altura teorica de tramo 3
dif_altura3 = altura3_toerico - altura3 #altura teorica menos altura "real" de tramo 3
print("altura3_toerico - altura3: ", dif_altura3) #Comprobacion para usuario

while (v < len(arreglo_y_4_decimal_creciente)): #bucle
  y_4_decimal = Lt-L3-altura_tramo4 + (altura_tramo4 - arreglo_y_4_decimal_creciente[len(arreglo_y_4_decimal_creciente)-1-v]) #coordenada y de tramo 4
  y_4 = round(y_4_decimal,6) #redondeo
  coord1_y.append(y_4) #se agrega coordenada a lista
  Pi_4 = arreglo_Pi_4_creciente[len(arreglo_Pi_4_creciente)-1-v] #Se halla el paso del tramo 4 "actual" usando el contador "v"
  Pi.append(Pi_4) #Se agrega el paso instantaneo a una lista de paso instantaneo general
  v = v + 1 #contador

altura4 = coord1_y[len(coord1_y)-1] #Se obtiene altura total en tramo 4 de la lista general de coordernadas y hasta el momento

#Agregando el Tramo 5 al arreglo de coordenadas y (Se agrega de forma decreciente y se resta)
q = 0 #contador
while (q < len(arreglo_y_5_decimal_creciente)): #bucle para totalidad de elementos en el array
  y_5_decimal = Lt-L3 + (L3 - arreglo_y_5_decimal_creciente[len(arreglo_y_5_decimal_creciente)-1-q]) #coordenada y de tramo 5 instaneo
  y_5 = round(y_5_decimal,6) #redondeo
  coord1_y.append(y_5) #se agrega ultima coordenada "y" a arreglo de coordenadas totales de "y"
  Pi_5 = arreglo_Pi_5_creciente[len(arreglo_Pi_5_creciente)-1-q] #Se define el paso instaneo
  Pi.append(Pi_5) #Se agrega el paso instaneo al array de pasos instaneos general
  q = q + 1 #contador

final = len(coord1_y) #numero de elementos total en la lista de coordenadas y

altura_final = coord1_y[len(coord1_y)-1] #Se obtiene altura total de la lista general de coordernadas y

#---------------------------------------------------------------------------------------------------------------------------------

#Tramos en base de coordenadas x , z

#Tramo 0.5 (vuelta 0 a vuelta 0.5)
for a in ang_t0_5:
  x_1 = (Dm_vr1/2) * math.sin(a) #se hallan las coordenadas para "x" y "z"
  z_1 = (Dm_vr1/2) * math.cos(a) * (-1)
  coord1_x1.append(x_1) #Se agregan las coordenadas instanteas a sus respectivas listas
  coord1_z1.append(z_1)
ang_f1 = pi #angulo igual a paso instaneo / angulo final 1(?)

posicion1 = list_t1.index(ang_f1) #Se busca en la lista el valor de angulo f1 y se guarda esa posicion
hasta1 = posicion1 + 1 #Siguiente posicion
coord2_y1 = coord1_y[0:hasta1] #Guarda todas las coordenadas hasta la inmedianta siguiente al tramo 0.5

#-------------------------------------------------------------------------------------------------------------------------------------

#Tramo 0.5 al final de la vuelta reducida 1
tramo_2 = ubicar_tramo(t_vr1,0,t_1,t_Nc1,t_2,t_Nc2,t_3) #Se ubica el tramo al que pertenece

#Condicional dependiendo del tramo que se determino
if (tramo_2 == 1):
  posicion2 = list_t1.index(t_vr1) #Se busca en la lista el valor de y se guarda esa posicion
  hasta2 = posicion2  #misma posicion, entendible por orden y simetria
  coord2_y2 = coord1_y[posicion1:hasta2] #Guarda todas las coordenadas hasta la ultima del tramo
  dif1 = hasta2 - posicion1 #dif. de registros para llegar a final del tramo

elif (tramo_2 == 2):
 posicion2 = list_tNc1.index(t_vr1) #Se busca el indice en el que el valor aparece
 hasta2 = (n_1 + 1) + posicion2 #posicion + numero de nodos pertenecientes al tramo anterior
 coord2_y2 = coord1_y[posicion1:hasta2] #nro de elemtos, derecha - izquierda
 dif1 = hasta2 - posicion1 #dif. de registros para llegar a final del tramo
#aqui
elif (tramo_2 == 3):
 posicion2 = list_t2.index(t_vr1) #Se busca el indice en el que el valor aparece
 hasta2 = (n_1 + n_2 + 1) + posicion2 #posicion + numero de nodos pertenecientes a los tramos anteriores
 coord2_y2 = coord1_y[posicion1:hasta2] #nro de elemtos, derecha - izquierda
 dif1 = hasta2 - posicion1 #dif. de registros para llegar a final del tramo

ang_t_red1 = np.linspace(math.pi,t_vr1,dif1) #hasta llegar al final de la vuelta reducida
print(ang_t_red1)
for b in ang_t_red1: #se itera cada elemento de la lista de angulos de la reduccion 1
 x_2 = (Dm_vr1/2 + C1 * (b - math.pi)) * math.sin(b) #Se calcula coord. x para cada elemento de ang_t_red1 / tramo 3
 z_2 = (Dm_vr1/2 + C1 * (b - math.pi)) * math.cos(b) * (-1) #Se calcula coord. z para cada elemento de ang_t_red1
 coord1_x2.append(x_2) #Se agregan las coordenadas "x" y "z" a la lista de coordenadas
 coord1_z2.append(z_2)

#-------------------------------------------------------------------------------------------------------------------------------------

#Tramo cuerpo sin reducciones
tramo3 = ubicar_tramo(t_vr2,0,t_1,t_Nc1,t_2,t_Nc2,t_3) #Se ubica el tramo al que pertenece t_vr2

#comentarios muy similares a seccion anterior
if (tramo3 == 3):
 posicion3 = list_t2.index(t_vr2)
 hasta3 = (n_1 + n_2 + 1) + posicion3
 inicio = hasta2 - 1 #indicar desde donde comenzar
 coord2_y3 = coord1_y[inicio:hasta3]
 dif2 = hasta3 - inicio

elif (tramo3 == 4):
 posicion3 = list_tNc2.index(t_vr2)
 hasta3 = (n_1 + n_2 + n_3 + 1) + posicion3
 inicio = hasta2 - 1 #indicar desde donde comenzar
 coord2_y3 = coord1_y[inicio:hasta3]
 dif2 = hasta3 - inicio

elif (tramo3 == 5):
 posicion3 = list_t3.index(t_vr2)
 hasta3 = (n_1 + n_2 + n_3 + n_4 + 1) + posicion3
 inicio = hasta2 - 1 #indicar desde donde comenzar
 coord2_y3 = coord1_y[inicio:hasta3]
 dif2 = hasta3 - inicio

ang_t_red2 = np.linspace(t_vr1,t_vr2,dif2)
for a in ang_t_red2: #se itera cada elemento de la lista de angulos de la reduccion 2
  x_3 = (Dm/2) * math.sin(a) #coordenadas "x" y "z" para tramo 3
  z_3 = (Dm/2) * math.cos(a) * (-1)
  coord1_x3.append(x_3) #Se agregan las coordenadas "x" y "z" a la lista de coordenadas
  coord1_z3.append(z_3)


#-------------------------------------------------------------------------------------------------------------------------------------

#Tramo red2 a tramo N - 0.5
tramo4 = ubicar_tramo(medio_final,0,t_1,t_Nc1,t_2,t_Nc2,t_3)

#comentarios muy similares a seccion anterior
posicion4 = list_t3.index(medio_final)
hasta4 = (n_1 + n_2 + n_3 + n_4 + 1) + posicion4
inicio2 = hasta3 - 1
coord2_y4 = coord1_y[inicio2:hasta4]
dif3 = hasta4 - inicio2

ang_t_red3 = np.linspace(t_vr2,medio_final,dif3)
for a in ang_t_red3: #se itera para todo ang_t_red3
  x_4 = (Dm/2 - C2 * (a - t_vr2)) * math.sin(a)
  z_4 = (Dm/2 - C2 * (a - t_vr2)) * math.cos(a) * (-1)
  coord1_x4.append(x_4)
  coord1_z4.append(z_4)

#-------------------------------------------------------------------------------------------------------------------------------------

#Tramo N - 0.5 a tramo N
for a in ang_tN_5: #se itera sobre cada elemento
  x_5 = (Dm_vr2/2) * math.sin(a) #se hallan coordenadas x z
  z_5 = (Dm_vr2/2) * math.cos(a) * (-1)
  coord1_x5.append(x_5) #se agregan a lista
  coord1_z5.append(z_5)
inicio3 = hasta4 - 1 #rango de anterior - tope(1)
coord2_y5 = coord1_y[inicio3:final] #se agregan coordenadas

#----------------------------------------------------------------------------------------------------------------------------------------
#Datos para Solidworks
#------------------------------------------------------------------------------------------------------------------------------------
#Obtención de datos para el modelamiento del resorte en Solidworks

tabla_solidworks = [] #se crea lista para datos de solidworks

#Punto 0 vueltas (0) / punto ref 0 - inicial
vta_punto0_vueltas = 0.0 #vueltas inicial 0
paso_punto0_vueltas = p0 #asigna p0 definido previamente (=0)
y_punto0_vueltas = 0.0  #asigna altura (=0) para inicio de resorte
if (vred1 > 0): #se comprueba si hay una reducción
  Dm_punto0_vueltas = d1 + d_alambre #en caso haya reducción se define nuevo dm para incio de vueltas
else:
  Dm_punto0_vueltas = Dm #caso contrario se usa diametro medio normal para inicio de vueltas
punto_solidworks = [paso_punto0_vueltas,y_punto0_vueltas,vta_punto0_vueltas,Dm_punto0_vueltas] #se crea un punto con datos de paso, altura, vueltas, dm
tabla_solidworks.append(punto_solidworks) #se agrega a lista de puntos

#Punto 0.5 vueltas (1) / punto ref 1
vta_punto1_vueltas = 0.5 #Primera media vuelta, en donde se mantiene dm inicial
paso_punto1_vueltas = 2*(L1-p0)*vta_punto1_vueltas+p0 #asigna paso en el punto de se cumple primera media vuelta
y_punto1_vueltas = (L1-p0)*pow(vta_punto1_vueltas,2)+vta_punto1_vueltas*p0 #asigna altura para punto donde se cumple primera media vuelta
if (vred1 > 0): #se comprueba si hay una reducción
  Dm_punto1_vueltas = d1 + d_alambre #en caso haya reducción se define nuevo dm para incio de vueltas
else:
  Dm_punto1_vueltas = Dm #caso contrario se usa diametro medio normal del resorte
punto_solidworks = [paso_punto1_vueltas,y_punto1_vueltas,vta_punto1_vueltas,Dm_punto1_vueltas] #se crea un punto con datos de paso, altura, vueltas, dm
tabla_solidworks.append(punto_solidworks) #Se agrega el punto a la lista

#Punto 1 vuelta (2) /punto ref 2
vta_punto2_vueltas = 1 #se define este punto para cuando este completa la primera vuelta del resorte
paso_punto2_vueltas = 2*(L1-p0)*vta_punto2_vueltas+p0 #asigna paso en el punto de se cumple primera vuelta
y_punto2_vueltas = (L1-p0)*pow(vta_punto2_vueltas,2)+vta_punto2_vueltas*p0 #asigna altura para punto donde se cumple primera vuelta
if (vred1 > 0): #se comprueba si hay una reducción al inicio del resorte
  if (vta_punto2_vueltas <= vred1): #se comprueba ya se terminaron de realizar todas las vueltas de reducción en esta vuelta
    Dm_punto2_vueltas = 2*(2*pi*C1*(vta_punto2_vueltas-0.5)+(d1+d_alambre)/2) #en caso en este punto aún se encuentre envuelta reducida se asigna dm
  else:
    Dm_punto2_vueltas = Dm #caso contrario se usa diametro medio normal del resorte
else:
  Dm_punto2_vueltas = Dm #caso contrario se usa diametro medio normal del resorte
punto_solidworks = [paso_punto2_vueltas,y_punto2_vueltas,vta_punto2_vueltas,Dm_punto2_vueltas] #se crea un punto con datos de paso, altura, vueltas, dm
tabla_solidworks.append(punto_solidworks) # Se agrega punto a lista

#Punto 1+nc1 vueltas (3) / punto ref 3
vta_punto3_vueltas = 1+nc1  #se define vueltas en este punto = una vuelta + número de vueltas variables antes de llegar a tramo constante
paso_punto3_vueltas = paso2 #asigna paso en el punto
y_punto3_vueltas = altura1 + I*pow((vta_punto3_vueltas-1),2)+(vta_punto3_vueltas-1)*paso1 #asigna altura para punto
if (vred1 > 0): #se comprueba si hay una reducción al inicio del resorte
  if (vta_punto3_vueltas <= vred1): #se comprueba si ya se terminaron de realizar todas las vueltas de reducción en esta vuelta
    Dm_punto3_vueltas = 2*(2*pi*C1*(vta_punto3_vueltas-0.5)+(d1+d_alambre)/2) #en caso en este punto aún se encuentre envuelta reducida se asigna dm
  else:
    Dm_punto3_vueltas = Dm #caso contrario se usa diametro medio normal del resorte
else:
  Dm_punto3_vueltas = Dm #caso contrario se usa diametro medio normal del resorte
punto_solidworks = [paso_punto3_vueltas,y_punto3_vueltas,vta_punto3_vueltas,Dm_punto3_vueltas]  #se crea un punto con datos de paso, altura, vueltas, dm
tabla_solidworks.append(punto_solidworks) # Se agrega punto a lista

#Punto N-1-nc2 vueltas (4) / punto ref 4
vta_punto4_vueltas = N-1-nc2 #se define vueltas en este punto =Vuelta total - número de vueltas variables despues de pasar el tramo constante
paso_punto4_vueltas = paso2 #asigna paso en el punto
y_punto4_vueltas = altura2 + (vta_punto4_vueltas-1-nc1)*paso2 #asigna altura para punto
if (vred2 > 0): #se comprueba si hay una reducción al final del resorte
  if ((N - vta_punto4_vueltas) <= vred2): #se comprueba si hay vueltas de reducción en este punto basado en el numero de vueltas de reduccion del extremo final
    Dm_punto4_vueltas = 2*(2*pi*C2*(N-vta_punto4_vueltas-0.5)+(d2+d_alambre)/2)  #en caso en este punto se encuentre en vueltas reducida se asigna dm
  else:
    Dm_punto4_vueltas = Dm #caso contrario se usa diametro medio normal del resorte
else:
  Dm_punto4_vueltas = Dm #caso contrario se usa diametro medio normal del resorte
punto_solidworks = [paso_punto4_vueltas,y_punto4_vueltas,vta_punto4_vueltas,Dm_punto4_vueltas] #se crea un punto con datos de paso, altura, vueltas, dm
tabla_solidworks.append(punto_solidworks) # Se agrega punto a lista

#Punto N-1 vueltas (5) / punto ref 5 - una vuelta antes de final del resorte
vta_punto5_vueltas = N-1 #se define vueltas en este punto = Vuelta total - 1 vuelta
paso_punto5_vueltas = 2*(L3-pf)*(N-vta_punto5_vueltas)+pf #asigna paso en el punto
y_punto5_vueltas = Lt - ((L3-pf)*pow((N-vta_punto5_vueltas),2)+pf*(N-vta_punto5_vueltas)) #asigna altura para punto
if (vred2 > 0): #se comprueba si hay una reducción al final del resorte
  if ((N - vta_punto5_vueltas) <= vred2):  #se comprueba si hay vueltas de reducción en este punto basado en el numero de vueltas de reduccion del extremo final
    Dm_punto5_vueltas = 2*(2*pi*C2*(N-vta_punto5_vueltas-0.5)+(d2+d_alambre)/2) #en caso en este punto se encuentre en vueltas reducida se asigna dm
  else:
    Dm_punto5_vueltas = Dm #caso contrario se usa diametro medio normal del resorte
else:
  Dm_punto5_vueltas = Dm #caso contrario se usa diametro medio normal del resorte
punto_solidworks = [paso_punto5_vueltas,y_punto5_vueltas,vta_punto5_vueltas,Dm_punto5_vueltas] #se crea un punto con datos de paso, altura, vueltas, dm
tabla_solidworks.append(punto_solidworks) # Se agrega punto a lista

#Punto N-0.5 vueltas (6) / punto ref 6 - media vuelta antes de final del resorte
vta_punto6_vueltas = N-0.5  #se define vueltas en este punto = Vuelta total - media vuelta
paso_punto6_vueltas = 2*(L3-pf)*(N-vta_punto6_vueltas)+pf #asigna paso en el punto
y_punto6_vueltas = Lt - ((L3-pf)*pow((N-vta_punto6_vueltas),2)+pf*(N-vta_punto6_vueltas)) #asigna altura para punto
if (vred2 > 0): #se comprueba si hay una reducción al final del resorte
  Dm_punto6_vueltas = d2 + d_alambre #en caso haya reducción se define dm para el punto
else:
  Dm_punto6_vueltas = Dm #caso contrario se usa diametro medio normal del resorte
punto_solidworks = [paso_punto6_vueltas,y_punto6_vueltas,vta_punto6_vueltas,Dm_punto6_vueltas] #se crea un punto con datos de paso, altura, vueltas, dm
tabla_solidworks.append(punto_solidworks) # Se agrega punto a lista

#Punto N vueltas (7) / punto ref 7 - final del resorte
vta_punto7_vueltas = N #asigna valor de vueltas totales del resorte
paso_punto7_vueltas = pf #asigna paso en el punto = pf definido previamente (=5)
y_punto7_vueltas = Lt #asigna valor de altura total del resorte
if (vred2 > 0): #se comprueba si hay reducción al final del resorte
  Dm_punto7_vueltas = d2 + d_alambre #en caso haya reducción se define dm para el punto
else:
  Dm_punto7_vueltas = Dm #caso contrario se usa diametro medio normal del resorte
punto_solidworks = [paso_punto7_vueltas,y_punto7_vueltas,vta_punto7_vueltas,Dm_punto7_vueltas] #se crea un punto con datos de paso, altura, vueltas, dm
tabla_solidworks.append(punto_solidworks) # Se agrega punto a lista

#Punto fin vta red 1 (8) / punto ref 8 - punto exacto en que acaban vueltas reducidas de extremo 1
vta_punto8_vueltas = vred1 #asigna valor de vuelta al numero de vueltas reducidas de extremo 1
if (vred1 == 0.0): #si no hay vueltas de reducción
  paso_punto8_vueltas = p0 #asigna el valor de paso inicial a p0 (=0) / si no hay reducciones es el punto inicial
  y_punto8_vueltas = 0.0 #asigna el valor de altura a 0
elif ((vred1 > 0) and (vred1 <= 1)): #si las vueltas de reducciones son 1 o menos
  paso_punto8_vueltas = 2*(L1-p0)*vta_punto8_vueltas+p0 #asigna paso para el punto final de vred1
  y_punto8_vueltas = (L1-p0)*pow(vta_punto8_vueltas,2)+vta_punto8_vueltas*p0 #asigna altura para el punto final de vred1
elif (vred1 <= (1+nc1)): #si las vueltas de reducciones llegan hasta el segmento de paso variable previo a la region constante
  paso_punto8_vueltas = 2*I*(vta_punto8_vueltas-1)+paso1 #asigna paso para el punto final de vred1
  y_punto8_vueltas = altura1 + I*pow((vta_punto8_vueltas-1),2)+(vta_punto8_vueltas-1)*paso1 #asigna altura para el punto final de vred1
else:
  paso_punto8_vueltas = paso2 #caso contrario se le asigna valor de paso2
  y_punto8_vueltas = altura2 + (vta_punto8_vueltas-1-nc1)*paso2 #asigna altura correspondiente para el punto final de vred1
Dm_punto8_vueltas = Dm #diametro medio en el punto final de vred 1
punto_solidworks = [paso_punto8_vueltas,y_punto8_vueltas,vta_punto8_vueltas,Dm_punto8_vueltas] #crea array de valores del punto
tabla_solidworks.append(punto_solidworks) #agrega el punto a la lista/tabla

#Punto fin vta red 2 (9) / punto ref 9 - punto exacto en que empiezan vueltas reducidas de extremo 2
vta_punto9_vueltas = N-vred2 #asigna valor de vuelta al numero de vueltas total - las vueltas reducidas de extremo 2
if (vred2 == 0.0): #si no hay vueltas de reducción
  paso_punto9_vueltas = pf  #asigna el valor de paso final a pf (=5) / si no hay reduccion es el punto final
  y_punto9_vueltas = Lt #asigna el valor de altura a la total del resorte
elif ((vred2 > 0) and (vred2 <= 1)): #si las vueltas de reducciones son 1 o menos
  paso_punto9_vueltas = 2*(L3-pf)*(N-vta_punto9_vueltas)+pf #asigna paso para el punto inicial de vred2
  y_punto9_vueltas = Lt - ((L3-pf)*pow((N-vta_punto9_vueltas),2)+pf*(N-vta_punto9_vueltas)) #asigna altura para el punto inicial de vred2
elif (vred2 <= (1+nc1)): #si las vueltas de reducciones empiezan en el segmento de paso variable luego de la region constante
  paso_punto9_vueltas = 2*J*(vred2-1)+(2*L3-pf) #asigna paso para el punto inicial de vred2
  y_punto9_vueltas = y_punto5_vueltas - (J*pow((vred2-1),2)+(2*L3-pf)*(vred2-1)) #asigna altura para el punto inicial de vred2
else:
  paso_punto9_vueltas = paso2 #caso contrario se le asigna valor de paso2
  y_punto9_vueltas = altura2 + (vta_punto9_vueltas-1-nc1)*paso2 #asigna altura para el punto inicial de vred2
Dm_punto9_vueltas = Dm #Diametro medio en el punto inicial de vred2
punto_solidworks = [paso_punto9_vueltas,y_punto9_vueltas,vta_punto9_vueltas,Dm_punto9_vueltas] #se crea un punto con datos de paso, altura, vueltas, dm
tabla_solidworks.append(punto_solidworks) # Se agrega punto a lista

#Se imprimen los puntos con los datos necesarios para llenar en la tabla de Helicoide en solidworks en el orden operado en el codigo
print("Paso 0 = ",paso0,"/","Altura 0 = ",0,"/","Vueltas = ",0,"/","Tramo angular = [0,",t_1,"]")
print("Paso 1 = ",paso1,"/","Altura 1 = ",altura1,"/","Vueltas = ",1,"/","Tramo angular = [",t_1,",",t_Nc1,"]")
print("Paso 2 = ",paso2,"/","Altura 2 = ",altura2,"/","Vueltas = ",1 + nc1,"/","Tramo angular = [",t_Nc1,",",t_2,"]")
print("Paso 3 = ",paso3,"/","Altura 3 = ",altura3,"/","Vueltas = ",N - 1 - nc2,"/","Tramo angular = [",t_2,",",t_Nc2,"]")
print("Paso 4 = ",paso5,"/","Altura 4 = ",altura4,"/","Vueltas = ",N - 1,"/","Tramo angular = [",t_Nc2,",",t_3,"]")
print("Paso final = ",pf,"/","Altura final = ",altura_final,"/","Vueltas = ",N)
print("Nc1 = ",nc1)
print("Nc2 = ",nc2)

#ordena la lista usando metodo de ordenamiento de burbuja
tabla_solidworks_ord = []
tabla_solidworks_ord = ord_burbuja(tabla_solidworks) #Ordenamiento burbuja, ordena en ascendente los "Puntos" del arreglo basado en el segundo elemento de cada "Punto" (?) Segundo elemento del arreglo es "altura"

#Simprime titulo
print("TABLA EN SOLIDWORKS")
index_puntos = 0
for i in tabla_solidworks_ord: #Se itera para imprimir los puntos con los datos necesarios para llenar en la tabla de Helicoide en solidworks en orden
  print("Punto ",index_puntos," : ", "Paso = ",i[0]," / ","Vueltas = ",i[2]," / ","Altura = ",i[1],"/","Diámetro = ",i[3])
  index_puntos = index_puntos +1
# from re import X
  
#----------------------------------------------------------------------------------------------------------------------------------------
#Grafica
#----------------------------------------------------------------------------------------------------------------------------------------

#Trazar la gráfica
fig = plt.figure()#figsize =(8,15)) #Se crea figura vacia de tamaño 8x15 (unidad?)
ax = plt.axes(projection='3d') #Se crea objeto de proyección tridimensional de eje "ax" para la figura con ejes utilizando Matplotlib

#Se trazan lineas para las diferentes secciones del resorte utilizando las listas de coordenadas x y z para cada tramo del resorte
ax.plot(coord1_x1, coord1_z1, coord2_y1,'blue') #se traza linea con las listas de coordenadas del tramo 1
ax.scatter3D(coord1_x1, coord1_z1, coord2_y1, c = "blue") #Se resaltan los puntos con color azul

ax.plot(coord1_x2, coord1_z2, coord2_y2,'red') #se traza linea con las listas de coordenadas del tramo 2
ax.scatter3D(coord1_x2, coord1_z2, coord2_y2, c = "red") #Se resaltan los puntos con color rojo

ax.plot(coord1_x3, coord1_z3, coord2_y3,'black') #se traza linea con las listas de coordenadas del tramo 3
ax.scatter3D(coord1_x3, coord1_z3, coord2_y3, c = "black") #Se resaltan los puntos con color negro

ax.plot(coord1_x4, coord1_z4, coord2_y4,'cyan') #se traza linea con las listas de coordenadas del tramo 4
ax.scatter3D(coord1_x4, coord1_z4, coord2_y4, c = "cyan") #Se resaltan los puntos con color cyan

ax.plot(coord1_x5, coord1_z5, coord2_y5,'yellow') #se traza linea con las listas de coordenadas del tramo 5
ax.scatter3D(coord1_x5, coord1_z5, coord2_y5, c = "yellow") #Se resaltan los puntos con color amarillo

#se añaden etiquetas a los ejes
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Altura media (mm)")

ax.view_init(15,40) #se ajusta la vista de la grafica / angulo de elevacion 15 con rotacion de 40º alrededor del eje z
plt.show() #se muestra la gráfica

#----------------------------------------------------------------------------------------------------------------------------------------

#SALIDA: Arreglo de puntos con coordenadas en 3D
resorte = []

ind1 = 0 #contador
while (ind1 < len(coord1_x1)): #se itera para todos los puntos de coordenada del tramo 1
  punto = [] #Se crea arreglo "punto"
  #Los puntos se agregan de forma: punto=[x1,z1,y1,x2,z2,y2,x3,z3,y3...]   hasta el ultimo punto de los arreglos de coordenadas
  punto.append(coord1_x1[ind1]) #Se agrega la coordenada x al punto
  punto.append(coord1_z1[ind1]) #Se agrega la coordenada z al punto
  punto.append(coord2_y1[ind1]) #Se agrega la coordenada y al punto
  resorte.append(punto) #Se agrega el punto creado
  ind1 = ind1 + 1 #contador + 1

ind2 = 0
while (ind2 < len(coord1_x2)): #se itera para todos los puntos de coordenada del tramo 2
  punto = [] #Se reinicia arreglo "punto"
  #Los puntos se agregan de forma: punto=[x1,z1,y1,x2,z2,y2,x3,z3,y3...]   hasta el ultimo punto de los arreglos de coordenadas
  punto.append(coord1_x2[ind2]) #Se agrega la coordenada x al punto
  punto.append(coord1_z2[ind2]) #Se agrega la coordenada z al punto
  punto.append(coord2_y2[ind2]) #Se agrega la coordenada y al punto
  resorte.append(punto) #Se agrega el punto creado
  ind2 = ind2 + 1 #contador + 1

ind3 = 0
while (ind3 < len(coord1_x3)): #se itera para todos los puntos de coordenada del tramo 3
  punto = [] #Se limpia arreglo "punto"
  #Los puntos se agregan de forma: punto=[x1,z1,y1,x2,z2,y2,x3,z3,y3...]   hasta el ultimo punto de los arreglos de coordenadas
  punto.append(coord1_x3[ind3]) #Se agrega la coordenada x al punto
  punto.append(coord1_z3[ind3]) #Se agrega la coordenada z al punto
  punto.append(coord2_y3[ind3]) #Se agrega la coordenada y al punto
  resorte.append(punto) #Se agrega el punto creado
  ind3 = ind3 + 1 #contador + 1

ind4 = 0
while (ind4 < len(coord1_x4)): #se itera para todos los puntos de coordenada del tramo 4
  punto = [] #Se limpia arreglo "punto"
  #Los puntos se agregan de forma: punto=[x1,z1,y1,x2,z2,y2,x3,z3,y3...]   hasta el ultimo punto de los arreglos de coordenadas
  punto.append(coord1_x4[ind4]) #Se agrega la coordenada x al punto
  punto.append(coord1_z4[ind4]) #Se agrega la coordenada z al punto
  punto.append(coord2_y4[ind4]) #Se agrega la coordenada y al punto
  resorte.append(punto) #Se agrega el punto creado
  ind4 = ind4 + 1 #contador + 1

ind5 = 0
while (ind5 < len(coord1_x5)): #se itera para todos los puntos de coordenada del tramo 5
  punto = [] #Se limpia arreglo "punto"
  #Los puntos se agregan de forma: punto=[x1,z1,y1,x2,z2,y2,x3,z3,y3...]   hasta el ultimo punto de los arreglos de coordenadas
  punto.append(coord1_x5[ind5]) #Se agrega la coordenada x al punto
  punto.append(coord1_z5[ind5]) #Se agrega la coordenada z al punto
  punto.append(coord2_y5[ind5]) #Se agrega la coordenada y al punto
  resorte.append(punto) #Se agrega el punto creado
  ind5 = ind5 + 1 #contador + 1

print("Punto Inicial: X = ",resorte[0][0],", Y = ",resorte[0][1],", Z = ", resorte[0][2]) #Se imprime punto inicial
print("Punto Final: X = ",resorte[len(resorte)-1][0],", Y = ",resorte[len(resorte)-1][1],", Z = ", resorte[len(resorte)-1][2]) #Se imprime punto final
#Durante el codigo se usa coord_y como altura (Eje z)   y    coord_z como profundidad (Eje Y)

#Codigo no contempla la grafica del grosor del alambre cuando grafica el resorte, solo la espiral/helicoide
