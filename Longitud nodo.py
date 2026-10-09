


from vpython import *
import math

# -------------------------------------------------------------------
# PARÁMETROS ORBITALES (valores reales de la Tierra, excepto a escalado)
# -------------------------------------------------------------------
a = 3.0                     # semieje mayor (escala visual, 1 UA ≈ 3 unidades)
e = 0.01671123              # excentricidad
i = math.radians(0)         # inclinación (0° para simplificar, puedes cambiarla)
omega = math.radians(102.93768193)   # argumento del perihelio (radianes)
Omega = math.radians(30)               # longitud del nodo ascendente (radianes)
n = 2 * math.pi / 365.2422  # movimiento medio (rad/día), año trópico
# FASE INICIAL para que la órbita comience en X+
M0 = -omega

# -------------------------------------------------------------------
# OPCIÓN DE ROTACIÓN AL PUNTO VERNAL
# -------------------------------------------------------------------
# Si True, rota toda la escena para que la Tierra empiece en el punto vernal (eje X+)
# Si False, la Tierra empieza en el perihelio (posición real, alrededor del 4 de enero)
ROTAR_AL_PUNTO_VERNAL = False 

# -------------------------------------------------------------------
# CONFIGURACIÓN DE LA ESCENA
# -------------------------------------------------------------------
scene.title = "Longitud del nodo - Inclinación"
scene.width = 800
scene.height = 700
#scene.background = color.black
scene.autoscale = False #evita el cambio del zoom de la cámara automático
sphere(pos=vector(0,0,0),texture="https://upload.wikimedia.org/wikipedia/commons/6/62/Sextans_B.jpg",radius=35,shininess=0)
scene.lights = []
scene.ambient = vector(0.6, 0.6, 0.6)
# Configuramos el eje Z como "arriba" para que el plano XY sea el suelo (eclíptica)
scene.up = vector(0, 0, 1)
scene.forward = vector(-1, 0, 0)   # cámara mirando desde -X

# -------------------------------------------------------------------
# CREACIÓN DE OBJETOS ESTÁTICOS (ejes, eclíptica, etiquetas)
# -------------------------------------------------------------------
# Plano de la eclíptica (plano XY)
ecliptica = box(pos=vector(0,0,0), size=vector(12,12,0.05), color=color.green, opacity=0.2)

# Ejes coordenados según convención astronómica
eje_x = arrow(pos=vector(0,0,0), axis=vector(5,0,0), shaftwidth=0.04)
eje_y = arrow(pos=vector(0,0,0), axis=vector(0,5,0), shaftwidth=0.04)
eje_z = arrow(pos=vector(0,0,0), axis=vector(0,0,5), shaftwidth=0.04)

# Etiquetas (se reposicionarán manualmente si hay rotación)
label_x = label(text="X", pos=vector(5,0,0), height=15, opacity=0.5, box=False)
label_y = label(text="Y", pos=vector(0,5,0), height=15, opacity=0.5, box=False)
label_z = label(text="Z", pos=vector(0,0,5), height=15, opacity=0.5, box=False)
label_ecl = label(text="Eclíptica", pos=vector(-6,-6,0), height=14, opacity=0.3, box=False)
label_vernal = label(text="Punto Vernal", pos=vector(6,0,0), height=14, opacity=0.3, color=color.yellow)

# Sol (en el origen)
sol = sphere(pos=vector(0,0,0), radius=0.7,texture="https://upload.wikimedia.org/wikipedia/commons/9/98/SDO_Sun_This_Week_%28SVS5577%29.jpg",  emissive=True, make_trail=True )
sol_label = label(text="Sol", pos=vector(0,0,0), height=13, opacity=0.5, box=False)
sol.rotate(axis=vector(0,0,1), angle=0.005)
luz = local_light(pos=sol.pos, color=color.white)

# Tierra (se crea sin posición, se asignará después)
tierra = sphere(texture=textures.earth, radius=0.5, make_trail=True,color=vector(1,1,1))
tierra_label = label(text="Tierra", height=13, opacity=0.2, box=False)
tierra.shininess = 0
# ----------------------------------
# EJE AXIAL REAL DE LA TIERRA
# ----------------------------------
inclinacion_axial = math.radians(23.5)

eje_axial = vector(
    0,
    math.sin(inclinacion_axial),
    math.cos(inclinacion_axial)
)
Npole = cylinder(
    pos=tierra.pos,
    axis=eje_axial,
    radius=0.05,
    color=color.white
)

Spole = cylinder(
    pos=tierra.pos,
    axis=-eje_axial,
    radius=0.05,
    color=color.white
)

# -------------------------------------------------------------------
# FUNCIÓN QUE CALCULA LA POSICIÓN DE LA TIERRA EN UN TIEMPO t (días)
# Devuelve un vector (x, y, z) en coordenadas astronómicas estándar.
# -------------------------------------------------------------------
def estado_orbital(t):

    M = n * t + M0

    E = M
    for _ in range(10):
        E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))

    theta = 2 * math.atan2(
        math.sqrt(1+e) * math.sin(E/2),
        math.sqrt(1-e) * math.cos(E/2)
    )

    r = a * (1 - e * math.cos(E))

    # Derivadas
    dE_dt = n / (1 - e * math.cos(E))
    dr_dt = a * e * math.sin(E) * dE_dt
    dtheta_dt = (math.sqrt(1 - e**2) / (1 - e * math.cos(E))) * dE_dt

    # Posición
    x = r * (math.cos(omega + theta) * math.cos(Omega) - math.sin(omega + theta) * math.sin(Omega) * math.cos(i))
    y = r * (math.cos(omega + theta) * math.sin(Omega) + math.sin(omega + theta) * math.cos(Omega) * math.cos(i))
    z = r * math.sin(omega + theta) * math.sin(i)

    # Velocidad
    vx = dr_dt*(math.cos(omega+theta)*math.cos(Omega) - math.sin(omega+theta)*math.sin(Omega)*math.cos(i)) \
         + r*(-math.sin(omega+theta)*math.cos(Omega) - math.cos(omega+theta)*math.sin(Omega)*math.cos(i))*dtheta_dt

    vy = dr_dt*(math.cos(omega+theta)*math.sin(Omega) + math.sin(omega+theta)*math.cos(Omega)*math.cos(i)) \
         + r*(-math.sin(omega+theta)*math.sin(Omega) + math.cos(omega+theta)*math.cos(Omega)*math.cos(i))*dtheta_dt

    vz = dr_dt*(math.sin(omega+theta)*math.sin(i)) \
         + r*(math.cos(omega+theta)*math.sin(i))*dtheta_dt

    r_vec = vector(x, y, z)
    v_vec = vector(vx, vy, vz)
    h_vec = cross(r_vec, v_vec)

    return r_vec, v_vec, h_vec

# -------------------------------------------------------------------
# POSICIÓN INICIAL (t=0)
# -------------------------------------------------------------------
r_vec, v_vec, h_vec = estado_orbital(0)
pos0 = r_vec


# -------------------------------------------------------------------
# APLICAR ROTACIÓN GLOBAL SI SE DESEA QUE LA TIERRA EMPIECE EN EL PUNTO VERNAL
# -------------------------------------------------------------------
if ROTAR_AL_PUNTO_VERNAL:
    # Calculamos el ángulo necesario para llevar pos0 al eje X positivo
    # (como estamos en el plano XY, usamos atan2(y, x))
    ang_rot = -math.atan2(pos0.y, pos0.x)  # negativo para rotar hacia el eje X
    print("Ángulo de rotación (grados):", math.degrees(ang_rot))

    # Rotamos todos los objetos estáticos alrededor del eje Z (que es la vertical)
    eje_x.rotate(angle=ang_rot, axis=vector(0,0,1))
    eje_y.rotate(angle=ang_rot, axis=vector(0,0,1))
    eje_z.rotate(angle=ang_rot, axis=vector(0,0,1))
    ecliptica.rotate(angle=ang_rot, axis=vector(0,0,1))

    # Las etiquetas (label) no tienen método rotate, así que reposicionamos
    label_x.pos = vector(5,0,0).rotate(angle=ang_rot, axis=vector(0,0,1))
    label_y.pos = vector(0,5,0).rotate(angle=ang_rot, axis=vector(0,0,1))
    label_z.pos = vector(0,0,5).rotate(angle=ang_rot, axis=vector(0,0,1))
    label_ecl.pos = vector(-6,-6,0).rotate(angle=ang_rot, axis=vector(0,0,1))
    label_vernal.pos = vector(6,0,0).rotate(angle=ang_rot, axis=vector(0,0,1))

    # También rotamos la posición inicial (aunque luego se recalculará en el bucle)
    pos0 = pos0.rotate(angle=ang_rot, axis=vector(0,0,1))
else:
    ang_rot = 0.0

# Colocamos la Tierra en su posición inicial
tierra.pos = pos0
tierra_label.pos = pos0 + vector(0.7,0.7,0.7)

# -------------------------------------------------------------------
# CONTROL DE LA ANIMACIÓN (botones)
# -------------------------------------------------------------------
running = True
t = 0.0
dt = 1.0  # paso de tiempo en días

# -------------------------------------------------
# CONTROL DE ÓRBITAS
# -------------------------------------------------
orbita_actual = 1
vueltas = 0
mostro_elementos_1 = False
mostro_elementos_2 = False

def toggle_run(b):
    global running, orbita_actual, i

    running = not running
    b.text = "Pause" if running else "Play"

    # Si ya terminó la primera órbita y vuelve a correr
    if running and orbita_actual == 1:
        orbita_actual = 2
        i = math.radians(30)  # Nueva inclinación
        
def reiniciar(b):
    global t, running
    running = False
    t = 0.0
    tierra.clear_trail()
    # Recalcular posición inicial con rotación si es necesario
    if ROTAR_AL_PUNTO_VERNAL:
        pos0_rot = posicion_tierra(0).rotate(angle=ang_rot, axis=vector(0,0,1))
    else:
        pos0_rot = posicion_tierra(0)
    tierra.pos = pos0_rot
    tierra_label.pos = pos0_rot + vector(0.7,0.7,0.7)

button(text="Pause", bind=toggle_run)
button(text="Reiniciar", bind=reiniciar)

linea_nodos = curve(color=color.cyan, radius=0.1)
nodo_asc = sphere(radius=0.15, color=color.white)
nodo_desc = sphere(radius=0.15, color=color.white)

label_Omega = label(text="", height=12, box=False, color=color.white)





# -------------------------------------------------------------------
# BUCLE PRINCIPAL
# -------------------------------------------------------------------
while True:
    rate(30)

    b = a * math.sqrt(1 - e**2)

    if running:

        t += dt

        # -----------------------------
        # Detectar órbita completa
        # -----------------------------
        if t >= 365.2422:
            vueltas += 1
            t = 0

        # -----------------------------
        # PRIMERA ÓRBITA COMPLETA
        # -----------------------------
        if vueltas == 1 and not mostro_elementos_1:
        
            running = False
            mostro_elementos_1 = True

        # -----------------------------
        # SEGUNDA ÓRBITA COMPLETA
        # -----------------------------
        if vueltas == 2 and not mostro_elementos_2:

            # ESTADO ORBITAL
            r_vec, v_vec, h_vec = estado_orbital(t)
            k_vec = vector(0, 0, 1)

            # VECTOR NODO
            N_vec = cross(k_vec, h_vec)

            if mag(N_vec) > 1e-8:

                N_hat = norm(N_vec)

                # LÍNEA DE NODOS
                linea_nodos.clear()
                linea_nodos.append(-N_hat * 6)
                linea_nodos.append(N_hat * 6)

                # NODOS
                nodo_asc.pos = N_hat * a
                nodo_desc.pos = -N_hat * a
                
              #Label Nodos
                           
                label(text="Nodo Ascendente",pos=nodo_asc.pos + N_hat * 0.5)
                label(text="Nodo Ascendente",pos=nodo_desc.pos - N_hat * 0.5)
                

                # LONGITUD DEL NODO Ω
                Omega_calc = math.acos(N_hat.x)

                if N_hat.y < 0:
                    Omega_calc = 2 * math.pi - Omega_calc

                # ARCO DE Ω
                radio_Omega = 2.5
                pasos = 50
                puntos_Omega = []

                for k in range(pasos + 1):
                    ang = Omega_calc * k / pasos
                    x = radio_Omega * math.cos(ang)
                    y = radio_Omega * math.sin(ang)
                    puntos_Omega.append(vector(x, y, 0))

                curve(pos=puntos_Omega, color=color.red, radius=0.04)
                   

                # ETIQUETA
                label_Omega.pos = vector(
                    radio_Omega * math.cos(Omega_calc/2),
                    radio_Omega * math.sin(Omega_calc/2),
                    0
                )

                label_Omega.text = f"(Ω) Longitud de nodo ascendente"
                label_Omega.height=14  
                
                
                #Arco Inclinación
                
                radio_arco = 3
                pasos = 40
                puntos_arco = []

                for k in range(pasos + 1):
                    ang = (i*0.9) * k / pasos
             
                    y = radio_arco * math.cos(ang)
                    z = radio_arco * math.sin(ang)
                    puntos_arco.append(vector(0, y, z))

                arco_i = curve(pos=puntos_arco, color=color.orange, radius=0.05)

                label(text="Inclinación (i)",
                pos=vector(0, radio_arco*math.cos(i/2), radio_arco*math.sin(i/2)),
                height=14,
                box=False,
                color=color.white
                )
                
            running = False
            mostro_elementos_2 = True

        # -----------------------------
        # ACTUALIZAR POSICIÓN
        # -----------------------------
        r_vec, v_vec, h_vec = estado_orbital(t)
        pos = r_vec
           
        #if abs(pos.x) < 0.01 and abs(pos.z) < 0.01:
         #   print(pos)
      
        if ROTAR_AL_PUNTO_VERNAL:
            pos = pos.rotate(angle=ang_rot, axis=vector(0,0,1))

        tierra.pos = pos
        tierra_label.pos = pos + vector(0.7,0.7,0.7)

        # Eje terrestre
        Npole.pos = tierra.pos
        Spole.pos = tierra.pos
        Npole.axis = eje_axial
        Spole.axis = -eje_axial

        # Rotaciones
        tierra.rotate(axis=eje_axial, angle=2*math.pi/365)
        sol.rotate(axis=vector(0,0,1), angle=0.005)
