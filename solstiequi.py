#!/usr/bin/env python
# coding: utf-8

# In[1]:

# Librerias, matemática y vpython 3D
from vpython import *	
import math
from datetime import datetime, timedelta, timezone
from math import sin, cos, tan, asin, atan2
from math import radians

scene.autoscale = False  # evita el cambio del zoom de la cámara automático
sphere(pos=vector(0, 0, 0), texture="https://upload.wikimedia.org/wikipedia/commons/6/62/Sextans_B.jpg", radius=25, shininess=0)
scene.lights = []
scene.ambient = vector(0.4, 0.4, 0.4)
scene.width = 700
scene.height = 700
#scene.ambient = vector(0.6, 0.6, 0.6)

# ------------------ Constantes astronómicas (visualización) ------------------
OBLICUIDAD = radians(23.44)  # oblicuidad media de la eclíptica (valor visual)

# BOTONES DE CONTROL (estilo solsyequi.py)
# ------------------------------------------------------------
running = True
sistema_geocentrico = True  # True = Tierra fija, False = Sol fijo
pausa_en_eventos = True  # Nueva variable para controlar pausa en eventos
ultimo_evento = None  # Para evitar múltiples detecciones del mismo evento
tiempo_simulado_helio = 0
boton_run = None
# Labels para eventos (solsticios y equinoccios)
label_equinoccio_marzo = None
label_equinoccio_septiembre = None
label_solsticio_junio = None
label_solsticio_diciembre = None
event_labels = []

def Run(b):
    global running
    running = not running
    if running: 
        b.text = "Pause"
        #limpiar_labels_eventos()  # Limpiar labels al reanudar
    else: 
        b.text = "Play"

def CambiarSistema(b):
    global sistema_geocentrico, t, dt_utc, ultimo_evento, tiempo_simulado_helio, boton_run
    sistema_geocentrico = not sistema_geocentrico
    t = 0
    tiempo_simulado_helio=0
    ultimo_evento=None
    running=True
    boton_run.text = "Pause"
    
    
    Sun.clear_trail()
    Tierra.clear_trail()
    #limpiar_labels_eventos()
    actualizar_visibilidad()
    
    if sistema_geocentrico:
        b.text = "Geocéntrico (Tierra fija)"
        Tierra.pos = vector(0, 0, 0)
        Tierra.make_trail = False
        # inicializar posición del Sol según NOAA
        Sun.pos = posicion_solar_noaa(dt_utc)
        Sun.make_trail = True
        #print("🔄 Cambiado a modo GEOCÉNTRICO")
    else:
        b.text = "Heliocéntrico (Sol fijo)"
        Sun.pos = vector(0, 0, 0)
        Sun.make_trail = True
        Tierra.make_trail = True
        #print("🔄 Cambiado a modo HELIOCÉNTRICO")
       
       # Tierra.pos = vector(x, y, z)  # posiciones iniciales calculadas previamente

def Reiniciar(b):
    global t, dt_utc, ultimo_evento, tiempo_simulado_helio
    t = 0
    tiempo_simulado_helio = 0
    ultimo_evento = None
    # Reiniciar tiempo NOAA
    dt_utc = datetime(2025, 3, 20, 12, 0, 0, tzinfo=timezone.utc)
    Sun.clear_trail()
    Tierra.clear_trail()
    #limpiar_labels_eventos()  # Limpiar labels al reiniciar
    b.text = "Reiniciar"
    print ("Simulación reiniciada")
    
def TogglePausaEventos(b):
    """Activar/desactivar pausa automática en eventos"""
    global pausa_en_eventos
    pausa_en_eventos = not pausa_en_eventos
    if pausa_en_eventos:
        b.text = "Pausa Eventos: ON"
    else:
        b.text = "Pausa Eventos: OFF"
        
            

def actualizar_visibilidad():
    """Actualiza la visibilidad de los objetos según el sistema activo"""
    if sistema_geocentrico:
        # Objetos visibles en modo geocéntrico
        ecuatorial.visible = True
        ecliptica_geo.visible = True
        label_geopunto.visible = True
        label_geoecliptica.visible = True
        label_ecuatorial.visible = True
        
        # Objetos ocultos en modo geocéntrico
        ecliptica_helio.visible = False
        label_heliopunto.visible = False
        label_helioecliptica.visible = False
    else:
        # Objetos visibles en modo heliocéntrico
        ecliptica_helio.visible = True
        label_heliopunto.visible = True
        label_helioecliptica.visible = True
        
        # Objetos ocultos en modo heliocéntrico
        ecuatorial.visible = False
        ecliptica_geo.visible = False
        label_geopunto.visible = False
        label_geoecliptica.visible = False
        label_ecuatorial.visible = False
        
def limpiar_labels_eventos():
    """Eliminar todos los labels de eventos"""
    global event_labels
    for lbl in event_labels:
        lbl.visible = False
        del lbl
    event_labels = []

def crear_label_evento(texto, posicion, color_evento):
    """Crear un label para un evento astronómico"""
    lbl = label(text=texto, pos=posicion, height=16, color=color_evento, 
                box=False, line=False, opacity=1.0)
    event_labels.append(lbl)
    return lbl
    
# ========== NUEVA FUNCIÓN PARA HELIOCÉNTRICO ==========
def detectar_eventos_heliocentrico(tiempo_dias, pos_tierra):
    """Detecta eventos usando la LONGITUD ANGULAR de la Tierra (Kepler)"""
    global running, ultimo_evento, pausa_en_eventos,boton_run
    
    if not pausa_en_eventos:
        return
    
    # Calcular anomalía media
    M = n * tiempo_dias
    M = M % 360
    
    # Resolver Kepler (anomalía excéntrica)
    E = radians(M)
    for _ in range(5):
        E = E + (radians(M) + e * sin(E) - E) / (1 - e * cos(E))
    
    # Calcular anomalía verdadera (nu)
    nu = 2 * atan2(sqrt(1 + e) * sin(E/2), sqrt(1 - e) * cos(E/2))
    nu = degrees(nu)
    
    # LONGITUD ECLÍPTICA
    longitud = (nu + w) % 360
    
    # Tolerancia para detección
    tolerancia = 2.0
    
    evento = None
    color_evento = None
    
    # Detectar por LONGITUD
    if abs(longitud - 0) <= tolerancia or abs(longitud - 360) <= tolerancia:
        evento = "Equinoccio de Marzo"
        color_evento = color.white
    elif abs(longitud - 90) <= tolerancia:
        evento = "Solsticio de Junio"
        color_evento = color.white
    elif abs(longitud - 180) <= tolerancia:
        evento = "Equinoccio de Septiembre"
        color_evento = color.white
    elif abs(longitud - 270) <= tolerancia:
        evento = "Solsticio de Diciembre"
        color_evento = color.white
    
    # Depuración: muestra la longitud cada cierto tiempo
    #if int(tiempo_dias) % 30 == 0 and int(tiempo_dias) != 0:
       # print(f"Helio - Día: {tiempo_dias:.1f}, Longitud: {longitud:.1f}°")
    
    # Si detectó evento y es nuevo
    if evento and ultimo_evento != evento:
        ultimo_evento = evento
        running = False
        boton_run.text = "Play"
        
        # Label cerca de la Tierra
        pos_label = pos_tierra + vector(0.3, 0.3, 0.3)
        crear_label_evento(evento, pos_label, color_evento)
        #print(f"🎉 HELIOCÉNTRICO: {evento} - Longitud: {longitud:.1f}°")    

def detectar_eventos_solsticios_equinoccios(dt_actual, pos_sol):
    """Detectar si estamos en un solsticio o equinoccio (funciona en ambos modos)"""
    global running, ultimo_evento, pausa_en_eventos, sistema_geocentrico
    
    if not pausa_en_eventos:
        return
    
    # Obtener la fecha (sin hora) para comparar
    fecha_actual = dt_actual.date()
    
    # Fechas aproximadas de los eventos (puedes ajustarlas)
    # Para 2025:
    equinoccio_marzo = datetime(2025, 3, 20).date()
    solsticio_junio = datetime(2025, 6, 21).date()
    equinoccio_septiembre = datetime(2025, 9, 22).date()
    solsticio_diciembre = datetime(2025, 12, 21).date()
    
    eventos = {
   
        solsticio_junio: ("Solsticio de Junio", color.white),
        equinoccio_septiembre: ("Equinoccio de Septiembre", color.white),
        solsticio_diciembre: ("Solsticio de Diciembre", color.white),
        #equinoccio_marzo: ("Equinoccio de Marzo", color.white)
    }
    
    # Verificar si la fecha actual es un evento
    if fecha_actual in eventos:
        nombre_evento, color_evento = eventos[fecha_actual]
        
        # Evitar detectar el mismo evento múltiples veces
        if ultimo_evento != nombre_evento:
            ultimo_evento = nombre_evento
            
            # Pausar la simulación
            running = False
            boton_run.text = "Play"
            
            # Determinar la posición del label según el modo
            if sistema_geocentrico:
                # Modo geocéntrico: label cerca del Sol (que se mueve)
                pos_label = pos_sol + vector(1.5, 1.5, 1)
            else:
                # Modo heliocéntrico: label en posición fija
                pos_label = vector(2.5, 1.5, 2)
            
            lbl = crear_label_evento(nombre_evento, pos_label, color_evento)
            
            # Imprimir en consola para depuración
            fecha_str = dt_actual.strftime("%Y-%m-%d %H:%M")
            modo_str = "Geocéntrico" if sistema_geocentrico else "Heliocéntrico"
            
            #break  # Solo manejar un evento a la vez    
    
             

# Crear botones (estilo solsyequi.py)
# Crear botones (estilo solsyequi.py)
boton_run = button(text="Pause", pos=scene.title_anchor, bind=Run)
boton_sistema = button(text="Geocéntrico (Tierra fija)", pos=scene.title_anchor, bind=CambiarSistema)
boton_reiniciar = button(text="Reiniciar", pos=scene.title_anchor, bind=Reiniciar)
boton_pausa_eventos = button(text="Pausa Eventos: ON", pos=scene.title_anchor, bind=TogglePausaEventos)

# Esta parte del código superior, crea la esfera mayor "Boveda celeste" y añade un botón de play-pause

# Ejes
eje1 = arrow(pos=vector(0, 0, 0), axis=vector(5, 0, 0), shaftwidth=0.04)
eje2 = arrow(pos=vector(0, 0, 0), axis=vector(0, 5, 0), shaftwidth=0.04)
eje3 = arrow(pos=vector(0, 0, 0), axis=vector(0, 0, -5), shaftwidth=0.04)

# Etiquetas de ejes (siempre visibles)		
label(text="X", pos=vector(5, 0, 0), height=15, opacity=0.5)
label(text="Z", pos=vector(0, 5, 0), height=15, opacity=0.5)
label(text="Y", pos=vector(0, 0, -5), height=15, opacity=0.5)

# Objetos que dependen del sistema
# Crearlos primero con visibilidad por defecto (se ajustará después)
label_geopunto = label(text="Punto Vernal", pos=vector(6, 0, 0), height=14, opacity=0.3, visible=False)
label_heliopunto = label(text="Punto Vernal", pos=vector(6, 0, 0), height=14, opacity=0.3, visible=False)

# Parte superior, define el plano de coordenadas y el punto vernal

# Dibuja el plano de la eclíptica (geocéntrico)
ecliptica_geo = box(pos=vector(0, 0, 0), size=vector(12, 0.05, 12), color=color.green, opacity=0.09, visible=False)
label_geoecliptica = label(text="Eclíptica", pos=vector(6, 3, 2), height=14, visible=False)

# Eclíptica heliocéntrica
ecliptica_helio = box(pos=vector(0, 0, 0), size=vector(12, 0.05, 12), color=color.green, opacity=0.09, visible=False)
label_helioecliptica = label(text="Eclíptica", pos=vector(-6, 0, -6), height=14, visible=False)

# Orientación correcta del plano
ecliptica_geo.up = vector(0, -2*cos(OBLICUIDAD), 10*sin(OBLICUIDAD))

# Plano ecuatorial
ecuatorial = box(pos=vector(0, 0, 0), size=vector(12, 0.05, 12), color=color.blue, opacity=0.1, shininess=0, visible=False)
label_ecuatorial = label(text="Plano Ecuatorial", pos=vector(-4, 0, -4), height=14, opacity=0.3, visible=False)

# Elementos Orbitales, aqui se definen los elementos orbitales
# elementos de la tierra
G = 2.951e-4  # UA
i = -0.00001531
o = -11.261
w = 102.93768193 
a = 3  # aqui el semieje de la tierra es 1UA, pero en la simulación queda muy cerca del sol, por tanto se modifica ese parámetro para alejarla
e = 0.01671123
b = a * (1 - e**2)**0.5
n = 2*pi/365.25 

# Calcula posiciones iniciales Ecuacion de kepler para la tierra
M = n * 0
E0 = M
E1 = M + ((180 / pi) * e * sin(E0 * pi / 180))

teta = 2 * atan((((1 + e) / (1 - e))**0.5) * tan(E1 / 2 * pi / 180)) * 180 / pi    
r = a * (1 - e * cos(E1 * pi / 180))

x = r * (sin(o * pi / 180) * cos((teta * pi / 180) + (w * pi / 180)) + cos(i * pi / 180) * sin((teta * pi / 180) + (w * pi / 180)) * cos(o * pi / 180))
y = r * (sin((teta * pi / 180) + (w * pi / 180)) * sin(i * pi / 180))
z = r * (cos((teta * pi / 180) + (w * pi / 180)) * cos(o * pi / 180) - cos(i * pi / 180) * sin(o * pi / 180) * sin((teta * pi / 180) + (w * pi / 180)))

# ------------------ Funciones NOAA (Julian Day) ------------------
def datetime_to_julian_day(dt):
    # dt: datetime con tzinfo=timezone.utc
    year = dt.year
    month = dt.month
    # incluir fracción de día
    day = dt.day + (dt.hour + dt.minute/60 + dt.second/3600) / 24.0
    if month <= 2:
        year -= 1
        month += 12
    A = int(year/100)
    B = 2 - A + int(A/4)
    JD = int(365.25*(year + 4716)) + int(30.6001*(month + 1)) + day + B - 1524.5
    return JD
    
    
def calcular_longitud_solar(dt_utc):
    """Calcular la longitud eclíptica del Sol en grados"""
    JD = datetime_to_julian_day(dt_utc)
    T = (JD - 2451545.0) / 36525.0

    # Longitud media del Sol (deg)
    L0 = 280.46646 + 36000.76983*T + 0.0003032*(T**2)
    L0 = L0 % 360  # Normalizar a 0-360°
    
    # Anomalía media (deg)
    M = 357.52911 + 35999.05029*T - 0.0001537*(T**2)
    M = M % 360
    
    # Ecuación del centro (deg)
    C = (1.914602 - 0.004817*T - 0.000014*(T**2))*sin(radians(M)) \
        + (0.019993 - 0.000101*T)*sin(radians(2*M)) \
        + 0.000289*sin(radians(3*M))
    
    # Longitud verdadera
    longitud = L0 + C
    longitud = longitud % 360  # Normalizar a 0-360°
    
    return longitud    
    
    
    
    

def posicion_solar_noaa(dt_utc, scale=3.0):
    """
    Versión NOAA simplificada con correcciones en T.
    dt_utc: datetime con tzinfo=timezone.utc
    devuelve vector(x,y,z) geocéntrico aparente (escala para visual)
    """
    JD = datetime_to_julian_day(dt_utc)
    T = (JD - 2451545.0) / 36525.0

    # Longitud media del Sol (deg)
    L0 = 280.46646 + 36000.76983*T + 0.0003032*(T**2)
    # Anomalía media (deg)
    M = 357.52911 + 35999.05029*T - 0.0001537*(T**2)
    # Excentricidad (no estrictamente necesario para λ pero se incluye)
    e_nn = 0.016708634 - 0.000042037*T - 0.0000001267*(T**2)

    # Ecuación del centro (deg)
    C = (1.914602 - 0.004817*T - 0.000014*(T**2))*sin(radians(M)) \
        + (0.019993 - 0.000101*T)*sin(radians(2*M)) \
        + 0.000289*sin(radians(3*M))

    lam_deg = L0 + C    # longitud verdadera (deg)
    lam = radians(lam_deg)

    # Oblicuidad media corregida (deg -> rad)
    eps_deg = 23.43929111 - 0.013004167*T - 0.0000001639*(T**2) + 0.0000005036*(T**3)
    eps = radians(eps_deg)

    # Declinación
    delta = asin(sin(eps) * sin(lam))

    x = cos(delta) * cos(lam)
    y = cos(delta) * sin(lam)
    z = sin(delta)

    return vector(scale*x, scale*y, scale*z)

# Definicion de los cuerpos celestes que estarán en la animacion(geometria, masas, propiedades)

# El sol como fuente de emision luminica, masa
Sun = sphere(pos=vector(0, 0, 0), radius=0.6, texture="https://upload.wikimedia.org/wikipedia/commons/9/98/SDO_Sun_This_Week_%28SVS5577%29.jpg", make_trail=True)
Sun.emissive = True
Sun.mass = 1
S = label(text="Sol", pos=vector(0.5, 0.5, 0.5), height=16, opacity=0.5)
Sun.rotate(axis=vector(0, 0.99, 0.12), angle=2*pi/(365 * 25))
lamp = local_light(pos=Sun.pos, color=color.white)

# definición geométrica de Tierra, masa y rotación
Tierra = sphere(pos=vector(x, y, z), texture=textures.earth, radius=0.3, make_trail=True, color=vector(1, 1, 1))
Tierra.mass = 3.003e-6
Tierra.rotate(axis=vector(0, 0, 1), angle=23.5*pi/365)
T = label(text="Tierra", pos=vector(0.7, 0.7, 0.7), height=16, opacity=0.2)
Tierra.shininess = 0

Npole = cylinder(pos=Tierra.pos, axis=vector(-sin(23.5*pi/180), cos(23.5*pi/180), 0), radius=0.03, color=color.white, make_trail=False)
spole = cylinder(pos=Tierra.pos, axis=vector(sin(23.5*pi/180), -cos(23.5*pi/180), 0), radius=0.03, color=color.white, make_trail=False)

dt = 1
t = 0
# Tiempo para NOAA (comienzo de la simulación)
dt_utc = datetime(2025, 3, 20, 12, 0, 0, tzinfo=timezone.utc)  # ejemplo: equinoccio

# Inicializar visibilidad según el sistema inicial
actualizar_visibilidad()

while True:
    rate(300)

    if not running:
        continue

    # -------------------------------
    # MODO GEOCÉNTRICO (NOAA)
    # -------------------------------
    if sistema_geocentrico:
        # Tierra fijada en el origen
        Tierra.pos = vector(0, 0, 0)
        Tierra.make_trail = False
        T.pos = Tierra.pos
        T.make_trail = False

        # Sol moviéndose con NOAA
        Sun.pos = posicion_solar_noaa(dt_utc)
        lamp.pos = Sun.pos
        Sun.make_trail = True
        Sun.rotate(axis=vector(0, 0.99, 0.12), angle=2*pi/(365 * 25))
        S.pos = Sun.pos
        S.make_trail = False 

        # Rotación propia de la Tierra (24 h)
        Tierra.rotate(axis=vector(-sin(23.5*pi/180), cos(23.5*pi/180), 0),
                      angle=2*pi/24)

        # Mover polos
        Npole.pos = Tierra.pos
        spole.pos = Tierra.pos

        # Avanzar tiempo NOAA
        dt_utc += timedelta(hours=1)
        #continue  # ⬅⬅⬅ IMPORTANTE: SALTAR EL HELIOCÉNTRICO
        
        detectar_eventos_solsticios_equinoccios(dt_utc, Sun.pos)

 # ========== MODO HELIOCÉNTRICO ==========
    else:
        # Avanzar tiempo simulado (días)
        t += dt
        
        # Ecuación de Kepler para posición de la Tierra
        M = n * t
        M = M % 360
        
        # Resolver Kepler
        E = radians(M)
        for _ in range(5):
            E = E + (radians(M) + e * sin(E) - E) / (1 - e * cos(E))
        
        # Anomalía verdadera
        nu = 2 * atan2(sqrt(1 + e) * sin(E/2), sqrt(1 - e) * cos(E/2))
        nu = degrees(nu)
        
        # Distancia (radio vector)
        r = a * (1 - e * cos(E))
        
        # Coordenadas de la Tierra
        x = r * (sin(o * pi/180) * cos(radians(nu + w))
                 + cos(i * pi/180) * sin(radians(nu + w)) * cos(o * pi/180))
        y = r * (sin(radians(nu + w)) * sin(i * pi/180))
        z = r * (cos(radians(nu + w)) * cos(o * pi/180)
                 - cos(i * pi/180) * sin(o * pi/180) * sin(radians(nu + w)))
        
        Tierra.pos = vector(x, y, z)
        
        # Rotaciones
        Tierra.rotate(axis=vector(-sin(23.5*pi/180), cos(23.5*pi/180), 0), angle=2*pi/365)
        Sun.rotate(axis=vector(0, 0.99, 0.12), angle=2*pi/(365 * 25))
        
        # Actualizar elementos
        Npole.pos = Tierra.pos
        spole.pos = Tierra.pos
        T.pos = Tierra.pos
        S.pos = Sun.pos
        lamp.pos = Sun.pos
        
        # SOLO DETECTAR EVENTOS EN MODO HELIOCÉNTRICO
        detectar_eventos_heliocentrico(t, Tierra.pos)
