#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vpython import *
import math

scene.autoscale = False
sphere(pos=vector(0,0,0), texture="https://i.imgur.com/1nVWbbd.jpg", radius=35, shininess=0)
scene.lights = []
running = True
scene.width = 650
scene.height = 600
scene.title = "Sistema Solar\n"

# ================= SISTEMA DE CONTROL =================
def Run(b):
    global running
    running = not running
    b.text = "Pause" if running else "Play"

button(text="Pause", pos=scene.title_anchor, bind=Run)

# Lista de todos los objetos
# Lista de todos los objetos
All = []


# Funciones para controlar visibilidad
def mostrar_todos():
    for objeto in All:
        objeto.visible = True

def ocultar_todos():
    for objeto in All:
        objeto.visible = False

def toggle_todos(b):
    if All and All[0].visible:
        ocultar_todos()
        b.text = "Mostrar Todos"
    else:
        mostrar_todos()
        b.text = "Ocultar Todos"

boton_todos = button(text="Ocultar Todos", bind=toggle_todos)

# Variables de velocidad
velocidad_rotacion = 1.0
velocidad_traslacion = 1.0

def set_rot_speed(s):
    global velocidad_rotacion
    velocidad_rotacion = s.value
    wt_rot.text = f'{s.value:1.2f}'

def set_trans_speed(s):
    global velocidad_traslacion
    velocidad_traslacion = s.value
    wt_trans.text = f'{s.value:1.2f}'

scene.append_to_caption("\n<b>Velocidades:</b> Rotación: ")
sl_rot = slider(min=0.1, max=5, value=1.0, length=100, bind=set_rot_speed)
wt_rot = wtext(text=f'{sl_rot.value:1.2f}')
scene.append_to_caption("   Traslación: ")
sl_trans = slider(min=0.1, max=5, value=1.0, length=100, bind=set_trans_speed)
wt_trans = wtext(text=f'{sl_trans.value:1.2f}')
scene.append_to_caption('')
# ================= CONTROLES DE ELEMENTOS ORBITALES =================

scene.append_to_caption("\n<b>Elementos Orbitales:</b>\n")

# Diccionario para almacenar textos de valores
wt_elem = {}

def set_param(s, param):
    global currentobject
    valor = s.value
    
    # Si es una lista de planetas seleccionados
    if isinstance(currentobject, list):
        for obj in currentobject:
            for nombre, datos in cuerpos.items():
                if datos["obj"] == obj:
                    cuerpos[nombre][param] = valor
    
    # Si es un solo planeta seleccionado
    elif currentobject:
        for nombre, datos in cuerpos.items():
            if datos["obj"] == currentobject:
                cuerpos[nombre][param] = valor
    
    wt_elem[param].text = f"{valor: .3f}"


# Línea 1: inclinación (i), nodo ascendente (Ω), argumento del perihelio (ω)
scene.append_to_caption("i: ")
sl_i = slider(min=-30, max=30, value=0, length=100, bind=lambda s: set_param(s,"i"))
wt_elem["i"] = wtext(text=f"{sl_i.value: .3f}")

scene.append_to_caption("   Ω: ")
sl_o = slider(min=-180, max=180, value=0, length=100, bind=lambda s: set_param(s,"o"))
wt_elem["o"] = wtext(text=f"{sl_o.value: .3f}")

scene.append_to_caption("   ω: ")
sl_w = slider(min=-180, max=180, value=0, length=100, bind=lambda s: set_param(s,"w"))
wt_elem["w"] = wtext(text=f"{sl_w.value: .3f}")

scene.append_to_caption("\n")

# Línea 2: semieje mayor (a), excentricidad (e), movimiento medio (n)
scene.append_to_caption("a: ")
sl_a = slider(min=0.5, max=15, value=3, length=100, bind=lambda s: set_param(s,"a"))
wt_elem["a"] = wtext(text=f"{sl_a.value: .3f}")

scene.append_to_caption("   e: ")
sl_e = slider(min=0, max=0.9, value=0.01, length=100, bind=lambda s: set_param(s,"e"))
wt_elem["e"] = wtext(text=f"{sl_e.value: .3f}")

scene.append_to_caption("   n: ")
sl_n = slider(min=0.001, max=1, value=0.017, length=100, bind=lambda s: set_param(s,"n"))
wt_elem["n"] = wtext(text=f"{sl_n.value: .3f}")

scene.append_to_caption("")

# ================= SISTEMA DE SELECCIÓN =================
modo_seleccion = "normal"
currentobject = None
menu_opciones = None

def actualizar_menu():
    global menu_opciones
    
    if menu_opciones:
        menu_opciones.delete()
    
    if modo_seleccion == "normal":
        opciones = ['Seleccionar objeto', 'Tierra', 'Luna', 'Eros', 'Jupiter', 'Saturno', 'All']
    elif modo_seleccion == "par":
        opciones = ['Seleccionar objeto', 'Sol-Tierra', 'Sol-Eros', 'Sol-Jupiter', 'Sol-Saturno']
    else:
        opciones = ['Seleccionar objeto', 'Sol-Tierra-Luna', 'Sol-Tierra-Eros', 'Sol-Tierra-Jupiter', 'Sol-Tierra-Saturno']
    
    menu_opciones = menu(choices=opciones, index=0, bind=M)

def M(m):
    global currentobject
    seleccion = m.selected
    ocultar_todos()

    if modo_seleccion == "normal":
        if seleccion == "Tierra":
            currentobject = Tierra
            Tierra.visible = True
            Npole.visible = True
            spole.visible = True
        elif seleccion == "Luna":
            currentobject = Luna
            Luna.visible = True
        elif seleccion == "Eros":
            currentobject = Eros
            Eros.visible = True
        elif seleccion == "Jupiter":
            currentobject = Jupiter
            Jupiter.visible = True
        elif seleccion == "Saturno":
            currentobject = Saturno
            Saturno.visible = True
            for anillo in Anillos_Saturno:
                anillo.visible = True
        elif seleccion == "All":
            currentobject = All
            mostrar_todos()
            Npole.visible = True
            spole.visible = True
            for anillo in Anillos_Saturno:
                anillo.visible = True

    elif modo_seleccion == "par":
        if seleccion == "Sol-Tierra":
            currentobject = [Sun, Tierra]
            Sun.visible = True
            Tierra.visible = True
            Npole.visible = True
            spole.visible = True
        elif seleccion == "Sol-Eros":
            currentobject = [Sun, Eros]
            Sun.visible = True
            Eros.visible = True
        elif seleccion == "Sol-Jupiter":
            currentobject = [Sun, Jupiter]
            Sun.visible = True
            Jupiter.visible = True
        elif seleccion == "Sol-Saturno":
            currentobject = [Sun, Saturno]
            Sun.visible = True
            Saturno.visible = True
            for anillo in Anillos_Saturno:
                anillo.visible = True

    elif modo_seleccion == "impar":
        if seleccion == "Sol-Tierra-Luna":
            currentobject = [Sun, Tierra, Luna]
            Sun.visible = True
            Tierra.visible = True
            Luna.visible = True
            Npole.visible = True
            spole.visible = True
        elif seleccion == "Sol-Tierra-Eros":
            currentobject = [Sun, Tierra, Eros]
            Sun.visible = True
            Tierra.visible = True
            Eros.visible = True
            Npole.visible = True
            spole.visible = True
        elif seleccion == "Sol-Tierra-Jupiter":
            currentobject = [Sun, Tierra, Jupiter]
            Sun.visible = True
            Tierra.visible = True
            Jupiter.visible = True
            Npole.visible = True
            spole.visible = True
        elif seleccion == "Sol-Tierra-Saturno":
            currentobject = [Sun, Tierra, Saturno]
            Sun.visible = True
            Tierra.visible = True
            Saturno.visible = True
            Npole.visible = True
            spole.visible = True
            for anillo in Anillos_Saturno:
                anillo.visible = True
                
           # --- Mostrar / ocultar gráficas según selección ---
    if isinstance(currentobject, sphere) or isinstance(currentobject, ellipsoid):
        graf_dist.visible = True
        graf_Ec.visible = True
        curva_dist.delete()
        curva_Ec.delete()
    else:
        graf_dist.visible = False
        graf_Ec.visible = False

        
        

    actualizar_elementos_orbitales()

# Botones para modos de selección
def set_modo_normal(b):
    global modo_seleccion
    modo_seleccion = "normal"
    actualizar_menu()

def set_modo_par(b):
    global modo_seleccion
    modo_seleccion = "par"
    actualizar_menu()

def set_modo_impar(b):
    global modo_seleccion
    modo_seleccion = "impar"
    actualizar_menu()

button(text="Modo Normal", bind=set_modo_normal)
button(text="Modo Par", bind=set_modo_par)
button(text="Modo Impar", bind=set_modo_impar)
scene.append_to_caption("\n")

# Inicializar menú
actualizar_menu()


# ================= FUNCIONES GENÉRICAS =================
def crear_cuerpo_celeste(tipo, **kwargs):
    """Función genérica para crear cuerpos celestes"""
    if tipo == "sphere":
        obj = sphere(**kwargs)
    elif tipo == "ellipsoid":
        obj = ellipsoid(**kwargs)
    elif tipo == "ring":
        obj = ring(**kwargs)
    elif tipo == "cylinder":
        obj = cylinder(**kwargs)
    
    return obj

def kepler_position(n, e, a, i, o, w, t):
    """Calcula la posición (x,y,z) a partir de elementos orbitales"""
    M = n * t
    E0 = M
    E1 = M + ((180/math.pi) * e * math.sin(E0 * math.pi / 180))
    
    teta = 2 * math.atan((((1 + e)/(1 - e))**0.5) * math.tan(E1/2 * math.pi/180)) * 180/math.pi
    r = a * (1 - e * math.cos(E1 * math.pi / 180))

    x = r * (math.sin(o*math.pi/180) * math.cos((teta*math.pi/180) + (w*math.pi/180)) +
             math.cos(i*math.pi/180) * math.sin((teta*math.pi/180) + (w*math.pi/180)) * math.cos(o*math.pi/180))
    y = r * (math.sin((teta*math.pi/180) + (w*math.pi/180)) * math.sin(i*math.pi/180))
    z = r * (math.cos((teta*math.pi/180) + (w*math.pi/180)) * math.cos(o*math.pi/180) -
             math.cos(i*math.pi/180) * math.sin(o*math.pi/180) * math.sin((teta*math.pi/180) + (w*math.pi/180)))
    return vector(x, y, z)
def energia_cinetica(obj, elem, r):
    """
    Calcula la energía cinética de un planeta con la ecuación vis-viva.
    obj : cuerpo (con .mass)
    elem : diccionario con elementos orbitales (incluye 'a')
    r : distancia actual al Sol
    """
    G = 1    # unidades normalizadas
    M = Sun.mass
    a = elem["a"]
    m = obj.mass

    # Fórmula vis-viva: v^2 = GM(2/r - 1/a)
    v2 = G * M * (2/r - 1/a)
    return 0.5 * m * v2


# ================= ELEMENTOS ORBITALES =================
ELEMENTOS_ORBITALES = {
    "Tierra": {"i": -0.00001531, "o": -11.261, "w": 102.93768193, "a": 3, "e": 0.01671123, "n": 2*math.pi/365},
    "Luna": {"i": 5.145, "o": 125.08, "w": 318.15, "a": 1, "e": 0.0549, "n": 2*math.pi/27.321661},
    "Eros": {"i": 10.82773, "o": 304.27434, "w": 178.91030, "a": 1.4581813*3, "e": 0.2226906, "n": 2*(math.pi/643)},
    "Jupiter": {"i": 1.30530, "o": 100.55615, "w": 14.75385, "a": 5.20336301, "e": 0.04839266, "n": 2*(math.pi/4332.589)},
    "Saturno": {"i": 2.485240, "o": 113.71504, "w": 92.43194, "a": 9.53707032, "e": 0.05415060, "n": 2 * math.pi / 10759.22}
}

# ================= CREACIÓN DE CUERPOS CELESTES =================
lamp = local_light(pos=vector(0,0,0), color=vector(1,1,1))

# Sol
Sun = crear_cuerpo_celeste("sphere",
    pos=vector(0,0,0), radius=0.7,
    texture="https://upload.wikimedia.org/wikipedia/commons/a/a0/Sun_in_February.jpg",
    emissive=True, make_trail=True
)
Sun.mass = 1
label(text="Sol", pos=vector(0, 0, 0), height=10, opacity=0.5)

# Tierra
elem_tierra = ELEMENTOS_ORBITALES["Tierra"]
Tierra = crear_cuerpo_celeste("sphere",
    pos=kepler_position(**elem_tierra, t=0),
    texture=textures.earth, radius=0.4, make_trail=True
)
tierra_label = label(
    pos=Tierra.pos,
    text="Tierra",
    height=14,
    opacity=0.2,
    box=False
)

Tierra.mass = 3.003e-6


# Polos de la Tierra (corregidos para seguir la inclinación axial)
Npole = crear_cuerpo_celeste("cylinder",
    pos=Tierra.pos,
    axis=vector(-sin(23.5*pi/180), cos(23.5*pi/180), 0),
    radius=0.03, color=color.blue
)
spole = crear_cuerpo_celeste("cylinder",
    pos=Tierra.pos,
    axis=-vector(-sin(23.5*pi/180), cos(23.5*pi/180), 0),
    radius=0.03, color=color.red
)

# Luna
elem_luna = ELEMENTOS_ORBITALES["Luna"]
Luna = crear_cuerpo_celeste("sphere",
    pos=Tierra.pos + kepler_position(**elem_luna, t=0),
    texture="https://upload.wikimedia.org/wikipedia/commons/e/e1/FullMoon2010.jpg",
    radius=0.1, make_trail=True, interval=10, retain=100
    
)
luna_label = label(
    pos=Luna.pos,
    text="Luna",
    height=14,
    opacity=0.2,
    box=False
)    
Luna.mass = 3.694e-8

# Eros
elem_eros = ELEMENTOS_ORBITALES["Eros"]
Eros = crear_cuerpo_celeste("ellipsoid",
    pos=kepler_position(**elem_eros, t=0),
    texture="https://upload.wikimedia.org/wikipedia/commons/c/cd/Eros_celestia.jpg",
    length=0.26, height=0.10, width=0.12, make_trail=True, interval=10, retain=300
)
Eros.mass = 3.36e-15

# Jupiter
elem_jupiter = ELEMENTOS_ORBITALES["Jupiter"]
Jupiter = crear_cuerpo_celeste("sphere",
    pos=kepler_position(**elem_jupiter, t=0),
    texture="https://upload.wikimedia.org/wikipedia/commons/2/23/Jupiter_Showcases_Auroras%2C_Hazes_%28NIRCam_Closeup%29.jpg",
    radius=0.8, make_trail=True
)
Jupiter.mass = 9.55e-4

# Saturno
elem_saturno = ELEMENTOS_ORBITALES["Saturno"]
Saturno = crear_cuerpo_celeste("sphere",
    pos=kepler_position(**elem_saturno, t=0),
    texture="https://upload.wikimedia.org/wikipedia/commons/c/c7/Saturn_during_Equinox.jpg",
    radius=0.7, make_trail=True
)
Saturno.mass = 2.857e-4

# Anillos de Saturno
anillos_config = [
    {"radius": 1.0, "thickness": 0.05, "color": vector(0.7,0.7,0.7), "opacity": 0.4},
    {"radius": 1.2, "thickness": 0.08, "color": color.white, "opacity": 0.8},
    {"radius": 1.4, "thickness": 0.06, "color": vector(0.9,0.9,0.9), "opacity": 0.6},
    {"radius": 1.6, "thickness": 0.02, "color": color.white, "opacity": 0.3}
]

Anillos_Saturno = []
for config in anillos_config:
    anillo = crear_cuerpo_celeste("ring",
        pos=Saturno.pos, axis=vector(0,1,0), **config
    )
    Anillos_Saturno.append(anillo)

# Lista de todos los objetos
# Lista de todos los objetos
All = [Tierra, Luna, Eros, Jupiter, Saturno, Sun, Npole, spole] + Anillos_Saturno


# Diccionario de cuerpos con parámetros orbitales
cuerpos = {
    "Tierra": {"obj": Tierra, **elem_tierra},
    "Eros": {"obj": Eros, **elem_eros},
    "Jupiter": {"obj": Jupiter, **elem_jupiter},
    "Saturno": {"obj": Saturno, **elem_saturno},
}

# Periodos de rotación
rotaciones = {
    "Tierra": 365, "Luna": 27.3, "Eros": 0.22, 
    "Jupiter": 0.41, "Saturno": 0.44, "Sun": 25
}

# ================= ELEMENTOS VISUALES =================
# Ejes
eje1 = arrow(pos=vector(0, 0, 0), axis=vector(5, 0, 0), shaftwidth=0.04)
eje2 = arrow(pos=vector(0, 0, 0), axis=vector(0, 5, 0), shaftwidth=0.04)
eje3 = arrow(pos=vector(0, 0, 0), axis=vector(0, 0, -5), shaftwidth=0.04)

label(text="X", pos=vector(5, 0, 0), height=15, opacity=0.5)
label(text="Z", pos=vector(0, 5, 0), height=15, opacity=0.5)
label(text="Y", pos=vector(0, 0, -5), height=15, opacity=0.5)
label(text="Punto Vernal", pos=vector(6, 0, 0), height=14, opacity=0.3)

ecliptica = box(pos=vector(0, 0, 0), size=vector(18, 0.05, 18), 
               color=color.green, opacity=0.2)
label(text="Ecliptica", pos=vector(-6, 0, -6), height=14, opacity=0.3)
shadow_spot = sphere(pos=vector(0,0,0), radius=Tierra.radius*0.5,
                     color=color.red, opacity=0.7, visible=False)
shadow_on_moon = sphere(pos=Luna.pos, radius=Luna.radius*1.5,
                        color=color.black, opacity=0.7, visible=False)
shadow_on_moon = sphere(pos=Luna.pos,
                        radius=Luna.radius*1.5,
                        color=color.red, opacity=0.7,
                        visible=False)



# ================= LÍNEAS DE NODOS Y PLANOS ORBITALES =================
mostrar_nodos = False
mostrar_planos = False

def crear_linea_punteada(direccion, longitud, color_linea):
    segmentos = []
    num_segmentos = 24
    longitud_segmento = longitud / num_segmentos
    
    for i in range(num_segmentos):
        if i % 2 == 0:
            inicio = direccion * (i * longitud_segmento - longitud/2)
            fin = direccion * ((i + 1) * longitud_segmento - longitud/2)
            segmento = cylinder(pos=inicio, axis=fin-inicio, 
                              radius=0.015, color=color_linea, opacity=0.8)
            segmentos.append(segmento)
    
    return segmentos

def crear_plano_orbital_por_kepler(n, e, a, i, o, w, color_plano, tamaño=20, t0=0.0, dt_t=0.01):
    r1 = kepler_position(n, e, a, i, o, w, t0)
    r2 = kepler_position(n, e, a, i, o, w, t0 + dt_t)

    if mag(r1 - r2) < 1e-6:
        r2 = kepler_position(n, e, a, i, o, w, t0 + dt_t*10)

    normal = norm(cross(r1, r2))
    dir_en_plano = norm(r1) if mag(r1) > 1e-6 else norm(r2)

    plano = box(pos=vector(0,0,0), size=vector(tamaño, 0.01, tamaño),
                color=color_plano, opacity=0.12, visible=False)
    plano.axis = dir_en_plano * tamaño
    plano.up = normal

    return plano

def crear_visualizacion_orbital(n, e, a, i, o, w, color_visual, cuerpo, n_ref=vector(0,1,0), tamaño_plano=20):
    plano = crear_plano_orbital_por_kepler(n, e, a, i, o, w, color_visual, tamaño=tamaño_plano)
    n_orb = plano.up
    dir_nodos = norm(cross(n_ref, n_orb))

    if mag(dir_nodos) < 1e-6:
        return None, plano

    longitud_linea = 12 + 8 * (abs(i)/90)
    segmentos_linea = crear_linea_punteada(dir_nodos, longitud_linea, color_visual)

    for segmento in segmentos_linea:
        segmento.visible = False

    cuerpo.linea_nodos = segmentos_linea
    cuerpo.plano_orbital = plano

    return segmentos_linea, plano

# Crear visualizaciones orbitales
linea_tierra, plano_tierra = crear_visualizacion_orbital(**elem_tierra, color_visual=color.blue, cuerpo=Tierra)
linea_luna, plano_luna = crear_visualizacion_orbital(**elem_luna, color_visual=color.cyan, cuerpo=Luna)
linea_eros, plano_eros = crear_visualizacion_orbital(**elem_eros, color_visual=color.yellow, cuerpo=Eros)
linea_jupiter, plano_jupiter = crear_visualizacion_orbital(**elem_jupiter, color_visual=color.orange, cuerpo=Jupiter)
linea_saturno, plano_saturno = crear_visualizacion_orbital(**elem_saturno, color_visual=color.magenta, cuerpo=Saturno)

todas_lineas = [linea_tierra, linea_luna, linea_eros, linea_jupiter, linea_saturno]
todos_planos = [plano_tierra, plano_luna, plano_eros, plano_jupiter, plano_saturno]

def actualizar_elementos_orbitales():
    for cuerpo in [Tierra, Luna, Eros, Jupiter, Saturno]:
        if hasattr(cuerpo, 'linea_nodos'):
            for segmento in cuerpo.linea_nodos:
                segmento.visible = False
        if hasattr(cuerpo, 'plano_orbital'):
            cuerpo.plano_orbital.visible = False
    
    if isinstance(currentobject, list):
        for obj in currentobject:
            if hasattr(obj, 'linea_nodos') and mostrar_nodos:
                for segmento in obj.linea_nodos:
                    segmento.visible = True
            if hasattr(obj, 'plano_orbital') and mostrar_planos:
                obj.plano_orbital.visible = True
    elif currentobject:
        if hasattr(currentobject, 'linea_nodos') and mostrar_nodos:
            for segmento in currentobject.linea_nodos:
                segmento.visible = True
        if hasattr(currentobject, 'plano_orbital') and mostrar_planos:
            currentobject.plano_orbital.visible = True

def toggle_nodos(b):
    global mostrar_nodos
    mostrar_nodos = not mostrar_nodos
    actualizar_elementos_orbitales()
    b.text = "Líneas Nodos: " + ("ON" if mostrar_nodos else "OFF")

def toggle_planos(b):
    global mostrar_planos
    mostrar_planos = not mostrar_planos
    actualizar_elementos_orbitales()
    b.text = "Planos Orb: " + ("ON" if mostrar_planos else "OFF")

button(text="Líneas Nodos: OFF", bind=toggle_nodos)
button(text="Planos Orb: OFF", bind=toggle_planos)
scene.append_to_caption("\n")

# ================= SISTEMA DE ESTACIONES =================
estaciones_visibles = True
luz_solar = cylinder(pos=vector(0, 0, 0), axis=vector(10, 0, 0), 
                    radius=2, color=color.yellow, opacity=0.3,
                    visible=estaciones_visibles)

etiqueta_estacion = label(pos=vector(0, -5, 0), text="", 
                         height=20, box=False, color=color.white,
                         visible=estaciones_visibles)

def determinar_estacion(t):
    angulo_orbital = (t % 365) / 365 * 360
    angulo_ajustado = (angulo_orbital + elem_tierra["w"]) % 360
    
    if 0 <= angulo_ajustado < 90:
        return "Verano (HS) / Invierno (HN)", color.blue
    elif 90 <= angulo_ajustado < 180:
        return "Otoño (HS) / Primavera (HN)", color.green
    elif 180 <= angulo_ajustado < 270:
        return "Invierno (HS) / Verano (HN)", color.red
    else:
        return "Primavera (HS) / Otoño (HN)", color.orange

def toggle_estaciones(b):
    global estaciones_visibles
    estaciones_visibles = not estaciones_visibles
    luz_solar.visible = estaciones_visibles
    etiqueta_estacion.visible = estaciones_visibles
    b.text = "Estaciones: " + ("ON" if estaciones_visibles else "OFF")

# ================= BOTONES DE CONTROL =================

def toggle_trayectorias(b):
    for obj in All:
        obj.make_trail = not obj.make_trail
        if not obj.make_trail:
            obj.clear_trail()
    b.text = "Trayectorias: " + ("ON" if All[0].make_trail else "OFF")

def clear_trails(b):
    """Limpia las trayectorias sin resetear posiciones"""
    for obj in All:
        obj.clear_trail()
    Luna.clear_trail()

def toggle_ejes(b):
    estado = not eje1.visible
    eje1.visible = estado
    eje2.visible = estado
    eje3.visible = estado
    b.text = "Ejes: " + ("ON" if estado else "OFF")

def toggle_ecliptica(b):
    estado = not ecliptica.visible
    ecliptica.visible = estado
    b.text = "Eclíptica: " + ("ON" if estado else "OFF")

def reset_orbital_elements(b):
    """Restaura posiciones y parámetros orbitales iniciales"""
    global t
    for nombre, vals in cuerpos.items():
        obj = vals["obj"]
        obj.pos = kepler_position(vals["n"], vals["e"], vals["a"],
                                vals["i"], vals["o"], vals["w"], 0)
        obj.clear_trail()

    Luna.pos = Tierra.pos + kepler_position(elem_luna["n"], elem_luna["e"], elem_luna["a"],
                                          elem_luna["i"], elem_luna["o"], elem_luna["w"], 0)
    Luna.clear_trail()
    
    t = 0

# ================= ORGANIZACIÓN EN DOS LÍNEAS =================
scene.append_to_caption("<b>Controles:</b>\n")

# Línea 1
button(text="Estaciones: ON", bind=toggle_estaciones)
button(text="Trayectorias: ON", bind=toggle_trayectorias)
button(text="Limpiar Trayectorias", bind=clear_trails)
button(text="Resetear Valores", bind=reset_orbital_elements)

scene.append_to_caption("\n")

# Línea 2
button(text="Ejes: ON", bind=toggle_ejes)
button(text="Eclíptica: ON", bind=toggle_ecliptica)
button(text="Líneas Nodos: OFF", bind=toggle_nodos)
button(text="Planos Orb: OFF", bind=toggle_planos)

# ================= GRÁFICAS =================
graf_dist = graph(
    title="Distancia Sol-Planeta",
    xtitle="Tiempo (días)",
    ytitle="Distancia (UA)",
    width=400, height=250,
    align="left",
    visible=False
)
curva_dist = gcurve(color=color.cyan, graph=graf_dist)

graf_Ec = graph(
    title="Energía cinética",
    xtitle="Tiempo (días)",
    ytitle="E_c",
    width=400, height=250,
    align="left",   # <- usa también "left"
    visible=False
)
curva_Ec = gcurve(color=color.red, graph=graf_Ec)

# ================= SIMULACIÓN PRINCIPAL =================
t = 0
dt = 1
currentobject = Tierra
# --- Función auxiliar para detectar intersección línea-esfera ---
def line_sphere_intersection(p0, dir_vec, center, R):
    d = dir_vec
    oc = p0 - center
    a = dot(d, d)
    b = 2 * dot(oc, d)
    c = dot(oc, oc) - R*R
    disc = b*b - 4*a*c
    if disc < 0:
        return []
    t1 = (-b + math.sqrt(disc)) / (2*a)
    t2 = (-b - math.sqrt(disc)) / (2*a)
    return [t1, t2]

while True:
    rate(200)
    
    if running:
        t += dt 
        t_efectivo = t * velocidad_traslacion

        # Actualizar posiciones
        for nombre, vals in cuerpos.items():
            obj = vals["obj"]
            obj.pos = kepler_position(vals["n"] * velocidad_traslacion,
                                    vals["e"], vals["a"],
                                    vals["i"], vals["o"], vals["w"], t)

        # La Luna depende de la Tierra
        Luna.pos = Tierra.pos + kepler_position(
            elem_luna["n"] * velocidad_traslacion,
            elem_luna["e"], elem_luna["a"],
            elem_luna["i"], elem_luna["o"], elem_luna["w"], t
        )
        # Actualizar etiquetas
        tierra_label.pos = Tierra.pos + vector(0,0.5,0)
        luna_label.pos = Luna.pos + vector(0,0.2,0)
        tierra_label.visible = Tierra.visible
        luna_label.visible = Luna.visible
        
        
        
        
        
        # Actualizar anillos
        for anillo in Anillos_Saturno:
            anillo.pos = Saturno.pos

        # Actualizar polos de la Tierra (siguen la inclinación axial)
        Npole.pos = Tierra.pos
        spole.pos = Tierra.pos
        Npole.axis = vector(-sin(23.5*pi/180), cos(23.5*pi/180), 0)
        spole.axis = -vector(-sin(23.5*pi/180), cos(23.5*pi/180), 0)

        # Rotaciones
        for nombre, periodo in rotaciones.items():
            obj = eval(nombre)
            obj.rotate(axis=vector(0,1,0), 
                      angle=2*math.pi/periodo * dt * velocidad_rotacion)

        # Actualizar luz solar
        direccion_tierra = norm(Tierra.pos)
        luz_solar.axis = direccion_tierra * 10
        luz_solar.pos = Sun.pos

        # Actualizar estaciones
        if estaciones_visibles:
            try:
                angulo_orbital = math.acos(dot(vector(1, 0, 0), direccion_tierra)) * 180/math.pi
                cruz = cross(vector(1, 0, 0), direccion_tierra)
                if cruz.y < 0:
                    angulo_orbital = 360 - angulo_orbital
                
                dia_anual = (angulo_orbital / 360) * 365.25
                estacion, color_estacion = determinar_estacion(dia_anual)
                #etiqueta_estacion.text = f"Día: {int(dia_anual)} - {estacion}"
                #etiqueta_estacion.color = color_estacion
            except:
                pass
                
                           # --- Energía cinética y distancia del planeta seleccionado ---
        if isinstance(currentobject, sphere) or isinstance(currentobject, ellipsoid):
            obj = currentobject
            r = mag(obj.pos - Sun.pos)

            # Buscar elementos orbitales del objeto actual
            elem = None
            for nombre, vals in cuerpos.items():
                if vals["obj"] == obj:
                    elem = vals
                    break

            if elem:
                Ec = energia_cinetica(obj, elem, r)
                curva_dist.plot(t, r)   # graficar distancia
                curva_Ec.plot(t, Ec)    # graficar energía cinética


                # -------- Detección y visualización de eclipses --------
        # Tolerancia angular / de profundidad (ajusta si quieres más/menos sensibilidad)
        tol = 0.98  # factor para asegurar que el cuerpo esté aproximadamente en la línea

        # 1) Eclipse Solar: Luna entre Sol y Tierra y la recta Sol->Luna cruza la Tierra
        dir_sun_to_moon = Luna.pos - Sun.pos
        dir_sun_to_earth = Tierra.pos - Sun.pos

        # condición aproximada: distancia Sol->Luna < distancia Sol->Tierra (Luna "por delante")
        if mag(dir_sun_to_moon) < mag(dir_sun_to_earth)*1.05:
            # checar intersección de la línea Sol->Luna con esfera Tierra
            ts = line_sphere_intersection(Sun.pos, dir_sun_to_moon, Tierra.pos, Tierra.radius)
            if ts:
                # buscamos t positivo (punto entre Sol y Luna)
                valid_t = [t for t in ts if t > 0]
                if valid_t:
                    t_int = min(valid_t)  # intersección más cercana al Sol
                    p_int = Sun.pos + dir_sun_to_moon * t_int
                    shadow_spot.pos = p_int
                    shadow_spot.visible = True
                else:
                    shadow_spot.visible = False
            else:
                shadow_spot.visible = False
        else:
            shadow_spot.visible = False

        # 2) Eclipse Lunar: Tierra entre Sol y Luna y la recta Sol->Tierra cruza la Luna
        dir_sun_to_earth = Tierra.pos - Sun.pos
        dir_sun_to_moon = Luna.pos - Sun.pos
        if mag(dir_sun_to_earth) < mag(dir_sun_to_moon)*1.05:
            ts2 = line_sphere_intersection(Sun.pos, dir_sun_to_earth, Luna.pos, Luna.radius)
            if ts2:
                # Si hay intersección con la esfera de la Luna → sombra sobre la Luna
                shadow_on_moon.pos = Luna.pos
                shadow_on_moon.radius = Luna.radius * 1.02
                shadow_on_moon.visible = True
            else:
                shadow_on_moon.visible = False
        else:
            shadow_on_moon.visible = False

