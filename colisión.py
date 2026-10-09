from vpython import *
import math
scene.title = "Colisión asteroide"
scene.width = 800
scene.height = 700
scene.autoscale = False
sphere(pos=vector(0,0,0),texture="https://upload.wikimedia.org/wikipedia/commons/6/62/Sextans_B.jpg",radius=35,shininess=0)
scene.lights=[]
scene.ambient = vector(0.6, 0.6, 0.6)
running = True

def Run(b):
    global running
    running = not running
    if running: 
        b.text = "Pause"
    else: 
        b.text = "Play"
    
button(text="Pause", bind=Run)




# Ejes coordenados según convención astronómica
eje_x = arrow(pos=vector(0,0,0), axis=vector(5,0,0), shaftwidth=0.04)
eje_z = arrow(pos=vector(0,0,0), axis=vector(0,5,0), shaftwidth=0.04)
eje_y = arrow(pos=vector(0,0,0), axis=vector(0,0,-5), shaftwidth=0.04)

# Etiquetas (se reposicionarán manualmente si hay rotación)
label_x = label(text="X", pos=vector(5,0,0), height=15, opacity=0.5, box=False)
label_z = label(text="Z", pos=vector(0,5,0), height=15, opacity=0.5, box=False)
label_y = label(text="Y", pos=vector(0,0,-5), height=15, opacity=0.5, box=False)
label_vernal = label(text="Punto Vernal", pos=vector(6,0,0), height=14, opacity=0.3, color=color.yellow)
# Define los vértices del plano de la órbita terrestre (ajustados para que sean coplanarios con la órbita)

                                     # Elementos Orbitales
# elementos de la tierra
ecliptica3 = box(pos=vector(0, 0, 0), size=vector(12, 0.05, 12), color=color.green, opacity=0.2,)
label(text="Ecliptica", pos=vector(-6, 0, -6), height=10, opacity=0.3)


G = 2.951e-4
i = -0.00001531
o = 0
w = 102.93768193 
a = 3
e = 0.01671123
b = a * (1 - e**2)**0.5
n = 2*pi/365 *4

# elementos Eros



iE = 10.82773
oE = 304.27434 
wE= 178.91030 
aE = 1.4581813*3
eE = 0.2226906
bE= a * (1 - eE**2)**0.5
nE= 2*(pi/643) *10




 #Posiciones de los cuerpos celestes a animar(anomalia media,coordenadas cartecianas)

# Calcula posiciones iniciales Ecuacion de kepler para la tierra

M = n * 0
E0 = M
E1 = M + ((180 / pi) * e * sin(E0 * pi / 180))

teta = 2 * atan((((1 + e) / (1 - e))**0.5) * tan(E1 / 2 * 3.1419 / 180)) * 180 / pi    
r = a * (1 - e * cos(E1 * pi / 180))

x = r * (sin(o * pi / 180) * cos((teta * pi / 180) + (w * pi / 180)) + cos(i * pi / 180) * sin((teta * pi / 180) + (w * pi / 180)) * cos(o * pi / 180))
y = r * (sin((teta * pi / 180) + (w * pi / 180)) * sin(i * pi / 180))
z = r * (cos((teta * pi / 180) + (w * pi / 180)) * cos(o * pi / 180) - cos(i * pi / 180) * sin(o * pi / 180) * sin((teta * pi / 180) + (w * pi / 180)))

# Calcula posiciones iniciales Ecuacion de kepler para Eros (E)
k = 0.01720209895
ME = nE * 0
E0E = ME
E1E = ME + ((180 / pi) * eE * sin(E0E * pi / 180))
tetaE = 2 * atan((((1 + eE) / (1 - eE))**0.5) * tan(E1E / 2 * 3.1419 / 180)) * 180 / pi    
rE = aE * (1 - eE * cos(E1E * pi / 180))

xE = rE * (sin(oE * pi / 180) * cos((tetaE * pi / 180) + (wE * pi / 180)) + cos(iE * pi / 180) * sin((tetaE * pi / 180) + (wE * pi / 180)) * cos(oE * pi / 180))
yE = rE * (sin((tetaE * pi / 180) + (wE * pi / 180)) * sin(iE * pi / 180))
zE = rE * (cos((tetaE * pi / 180) + (wE * pi / 180)) * cos(oE * pi / 180) - cos(iE * pi / 180) * sin(oE * pi / 180) * sin((tetaE * pi / 180) + (wE * pi / 180)))

 #Definicion de los cuerpos celestes que estaran en la animacion(geometria ,masas,propiedades)

#El sol como fuente de emision luminica,masa

lamp =local_light(pos=vector(0,0,0), color=vector(1,1,1))
Sun = sphere(pos=vector(0,0,0), radius=0.7,texture="https://upload.wikimedia.org/wikipedia/commons/9/98/SDO_Sun_This_Week_%28SVS5577%29.jpg",  emissive=True, make_trail=True )
Sun.mass = 1
Sun.emissive = True
label(text="Sol", pos=vector(0, 0, 0), height=10, opacity=0.5)

#definicion geometrica de Tierra ,masa y rotación

Tierra = sphere(pos=vector(x, y, z), texture=textures.earth, radius=0.5 , make_trail=True,color=vector(1,1,1))
Tierra.mass = 3.003e-6
Tierra.rotate(axis=vector(0,0,1), angle=23.5*pi/180)
T=label(text="Tierra", pos=vector(0.7,0.7,0.7), height=10, opacity=0.2)



#definición geométrica de Eros ,masa y rotacion

Eros = ellipsoid(
    pos=vector(xE,yE,zE),
    size=vector(0.45,0.15,0.15), texture="https://upload.wikimedia.org/wikipedia/commons/2/2e/433eros.jpg" , radius=0.15 , make_trail=True,color=vector(0,1,0),interval=10, retain=400)
Eros.mass = 1.004e-10
Eros.rotate(axis=vector(0,0,1), angle=23.5*pi/180)
E=label(text="Eros", pos=vector(0.7,0.7,0.7), height=10, opacity=0.2)
#definicion de los polos terrestres

Npole = cylinder(pos=Tierra.pos,axis=1*vector(-sin(23.5*pi/180),cos(23.5*pi/180),0),radius=0.03,make_trail=False)
spole = cylinder(pos=Tierra.pos,axis=1*vector(sin(23.5*pi/180),-cos(23.5*pi/180),0),radius=0.03,make_trail=False)

Eros.v = vector(-0.00706088655405, -0.00239725667064, -0.0018906242615)
vx = ((aE**2) * 2 * (pi / 643) * 10 * sin(E1E * pi / 180) / rE**2) * xE + k * ((1 +  Eros.mass/Sun.mass)**0.5) *  (((aE * (1 - (eE * eE)))**0.5) / rE) * (-sin(oE * pi / 180) * sin((tetaE * pi / 180) + (wE * pi / 180)) + cos(iE * pi / 180) * cos((tetaE * pi / 180) + (wE * pi / 180)) * cos(oE * pi / 180))
vy = ((aE**2) * 2 * (pi / 643) * 10 * sin(E1E * pi / 180) / rE**2) * yE + k * ((1 +  Eros.mass/Sun.mass)**0.5) * (((aE * (1 - (eE * eE)))**0.5) / rE) / rE  * (cos((tetaE * pi / 180) + (wE * pi / 180)) * sin(iE * pi / 180))
vz = ((aE**2) * 2 * (pi / 643) * 10 * sin(E1E * pi / 180) / rE**2) * zE + k * ((1 +  Eros.mass/Sun.mass)**0.5) * (((aE * (1 - (eE * eE)))**0.5) / rE) * (-cos(oE * pi / 180) * sin((tetaE * pi / 180) + (wE * pi / 180)) - sin(oE * pi / 180) * cos(iE * pi / 180) * cos((tetaE * pi / 180) + (wE * pi / 180)))
Eros.v=vector(vx,vy,vz)


print(Eros.v)#parametros para la animacion 

# Gráficos
graph1 = graph(title="Distancia entre la Tierra y Eros", xtitle="t", ytitle="r", fast=False ,width=600,height=200)
distance_plot_DeltaR = gcurve(color=color.blue, label="Eros")


graph2 = graph(title="Distancia entre la Tierra ,Eros vs Sol", xtitle="t", ytitle="r", fast=False,width=600,height=200)
distance_plot_Earth= gcurve(color=color.blue, label="Eros")
distance_plot_Eros = gcurve(color=color.red, label="Tierra")


# Función para actualizar la excentricidad
def actualizar_excentricidad(s):
    global eE
    eE = s.value
    wt_excentry.text = 'Excentricidad: {:1.6f}'.format(eE)  # Formato más preciso para evitar el problema de desaparición

# Deslizador para la excentricidad
excentry = slider(min=0, max=0.5, value=eE, step=0.000001, length=220, bind=actualizar_excentricidad)
wt_excentry = wtext(text='Excentricidad: {:1.6f}'.format(eE))  # Mostrar valor inicial con más decimales

# Función para actualizar la inclinación
def actualizar_inclinacion(s):
    global iE
    iE = s.value
    wt_inclinacion.text = 'Inclinación: {:1.3f}'.format(iE)  # También más decimales para evitar problemas de actualización

# Deslizador para la inclinación
inclinacion_slider = slider(min=0, max=360, value=iE, step=0.001, length=220, bind=actualizar_inclinacion)
wt_inclinacion = wtext(text='Inclinación: {:1.3f}'.format(iE))  # Mostrar valor inicial con más precisión

# Función para actualizar el nuevo parámetro nE
def actualizar_nE(s):
    global  nE
    nE = s.value
    wt_nE.text = 'nE: {:1.3f}'.format(nE)  # Actualizar el texto de nE con formato adecuado

# Deslizador para nE
nE_slider = slider(min=nE/10, max=nE+2*nE/5, value=nE, step=nE/10, length=220, bind=actualizar_nE)
wt_nE = wtext(text='nE: {:1.3f}'.format(nE))  # Mostrar el valor inicial de nE

# Función para reiniciar la simulación

dt = 1
t = 0
def reiniciar(b):
    global running, t, eE, iE, nE
    running = False
    t = 0
    
    # Reiniciar las posiciones de los objetos
    Tierra.clear_trail()
    Tierra.pos = vector(x, y, z)
    Eros.pos = vector(xE, yE, zE)
    Eros.clear_trail()

    # Reiniciar valores de deslizadores
    excentry.value = 0.2226906
    iE = 10.82773
    inclinacion_slider.value = iE
    nE = 2*(pi/643) *10
    nE_slider.value = nE
    
    # Actualizar textos de los deslizadores
    wt_excentry.text = 'Excentricidad: {:1.6f}'.format(eE)
    wt_inclinacion.text = 'Inclinación: {:1.3f}'.format(iE)
    wt_nE.text = 'nE: {:1.3f}'.format(nE)

    # Eliminar trazos anteriores de los gráficos
    distance_plot_DeltaR.delete()
    distance_plot_Earth.delete()
    distance_plot_Eros.delete()

    running = True
    b.text = "Reiniciar"

# Botón para reiniciar
boton_reiniciar = button(text="Reiniciar", pos=scene.title_anchor, bind=reiniciar)
while True:
    rate(200)
                    
    # Solo actualiza la animación cuando "running" es True (boton)
    if running:
        # Aumenta el tiempo solo cuando la animación está corriendo
        t += dt

        # Cálculos para la órbita de Júpiter
        M = n * t
        E0 = M
        E1 = M + ((180 / pi) * e * sin(E0 * pi / 180))

        # Cálculos para la órbita de Eros
        ME = nE * t
        E0E = ME
        E1E = ME + ((180 / pi) * eE * sin(E0E * pi / 180))

        while abs((E1 - E0))> 0.000000000001 and   abs((E1E - E0E)) > 0.000000000001 :  #posible error
        
            #para la tierra
        
            E0 = E1
            E1 = M + ((180 / pi) * e * sin(E0 * pi / 180))
        
            teta = 2 * atan((((1 + e) / (1 - e))**0.5) * tan(E1 / 2 * pi / 180)) * 180 / pi    
            r = a * (1 - e * cos(E1 * pi / 180))

        
            x = r * (sin(o * pi / 180) * cos((teta * pi / 180) + (w * pi / 180)) + cos(i * pi / 180) * sin((teta * pi / 180) + (w * pi / 180)) * cos(o * pi / 180))
            y = r * (sin((teta * pi / 180) + (w * pi / 180)) * sin(i * pi / 180))
            z = r * (cos((teta * pi / 180) + (w * pi / 180)) * cos(o * pi / 180) - cos(i * pi / 180) * sin(o * pi / 180) * sin((teta * pi / 180) + (w * pi / 180)))
        
            #para Eros
        
            E0E = E1E
            E1E = ME + ((180 / pi) * eE * sin(E0E * pi / 180))

            tetaE = 2 * atan((((1 + eE) / (1 - eE))**0.5) * tan(E1E / 2 * pi / 180)) * 180 / pi    
            rE = aE * (1 - eE * cos(E1E * pi / 180))

            xE = rE * (sin(oE * pi / 180) * cos((tetaE * pi / 180) + (wE * pi / 180)) + cos(iE * pi / 180) * sin((tetaE * pi / 180) + (wE * pi / 180)) * cos(oE * pi / 180))
            yE = rE * (sin((tetaE * pi / 180) + (wE * pi / 180)) * sin(iE * pi / 180))
            zE = rE * (cos((tetaE * pi / 180) + (wE * pi / 180)) * cos(oE * pi / 180) - cos(iE * pi / 180) * sin(oE * pi / 180) * sin((tetaE * pi / 180) + (wE * pi / 180)))
            
            
       
        Tierra.pos= vector(x, y, z)
        Tierra.rotate(axis=vector(-sin(23.5*pi/180),cos(23.5*pi/180),0), angle=2*pi /365)
        
        #Eros.pos=vector(xE,yE,zE)
        Eros.rotate(axis=vector(-sin(23.5*pi/180),cos(23.5*pi/180),0), angle=2*pi /365)

        #Eros.v=vector(vz,vy,vx)
       # Actualiza la posición y configuración de Npole , spole y elementos caracteristicos especificos
        
        Npole.pos = Tierra.pos
        Npole.axis = vector(-sin(23.5*pi/180), cos(23.5*pi/180), 0)
        Npole.make_trail = False  # Asegurarse de que no dejen rastro

        spole.pos = Tierra.pos
        spole.axis = vector(sin(23.5*pi/180), -cos(23.5*pi/180), 0)
        spole.make_trail = False  # Asegurarse de que no dejen rastro

        T.pos=Tierra.pos
        #j.make_trail=False

        E.pos=Eros.pos
        E.make_trail=False
        

        
        # Cálculos para el asteroide
        if mag(Eros.pos - Tierra.pos) > 0.8:
            Eros.pos=vector(xE,yE,zE)
            distance = Eros.pos - Sun.pos
            a1 = -G * Sun.mass * distance / mag(distance)**3
            Eros.pos += Eros.v * dt + 0.5 * a1 * dt * dt
            distance = Eros.pos - Sun.pos
            a2 = -G * Sun.mass * distance / mag(distance)**3
            Eros.v += 0.5 * (a1 + a2) * dt
            
            
    
     #Verifica si la distancia es menor a la tolerancia
            
        else:
            if mag(Eros.pos - Jupiter.pos) <= 0.6:
                   print("Distancia crítica alcanzada entre La tierra y Jupiter. Deteniendo la animación.")
                   running = False  # Detiene la animación
                   break  # Sal del bucle while para detener la simulación
            Asteroide.color = color.blue

            distance2 = Eros.pos - Tierra.pos
            a12 = -G * Tierra.mass * distance2 / mag(distance2)**3
            Eros.pos += Eros.v * dt + 0.5 * a12 * dt * dt
            a22 = -G * Tierra.mass * distance2 / mag(distance2)**3
            Eros.v += 0.5 * (a12 + a22) * dt

          # Graficar la distancia
        distance_plot_DeltaR.plot(t, mag(Eros.pos - Tierra.pos))
        distance_plot_Eros.plot(t,r)
        distance_plot_Earth.plot(t,rE)









