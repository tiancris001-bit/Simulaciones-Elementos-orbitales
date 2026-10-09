# Simulaciones de Elementos Orbitales

Colección de simulaciones interactivas en **VPython** para el estudio y visualización de los **elementos orbitales** de los cuerpos del Sistema Solar. Cada simulación ilustra uno o varios conceptos de la mecánica celeste: semiejes, excentricidad, inclinación, nodos, argumento del perihelio, anomalía verdadera, solsticios, equinoccios y acercamientos entre cuerpos.

Este material fue desarrollado como parte de un **trabajo de grado** en el área de astronomía y educación.

---

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `semiejes-excentricidad.py` | Visualiza el semieje mayor, semieje menor y la excentricidad de la órbita terrestre. |
| `Longitud nodo.py` | Muestra gráficamente la **longitud del nodo ascendente (Ω)** y la **inclinación orbital (i)**. |
| `Anomalia-Argumento.py` | Ilustra la **anomalía verdadera (θ)** y el **argumento del perihelio (ω)** usando la ecuación de Kepler. |
| `solstiequi.py` | Simulación de los **solsticios y equinoccios**, con modos geocéntrico (NOAA) y heliocéntrico. |
| `colisión.py` | Simulación del **acercamiento del asteroide 433 Eros a la Tierra**, con gráficas de distancia y sliders interactivos. |
| `sistema solar.py` | Simulación del **Sistema Solar** con planetas, Luna, Eros, Júpiter y Saturno; incluye gráficas de energía cinética y eclipses. |
| `CITATION.cff` | Metadatos de citación académica del repositorio. |

---

## Características generales

- Visualización 3D interactiva con **VPython**.
- Cálculo de posiciones mediante la **ecuación de Kepler** resuelta por Newton-Raphson.
- **Deslizadores** para modificar parámetros orbitales en tiempo real (excentricidad, inclinación, etc.).
- **Gráficas** de distancia, energía cinética y otras magnitudes físicas.
- **Detección de eventos astronómicos**: solsticios, equinoccios, eclipses, acercamientos.
- Órbitas precalculadas con `curve()` para una visualización limpia y sin trazos residuales.

---

## Requisitos

- **Python 3.8 o superior**
- **VPython 7.x**

Instalación:
pip install vpython

text

---

## Cómo ejecutar

### Opción 1: Clonar el repositorio y ejecutar
git clone https://github.com/tiancris001-bit/Simulaciones-Elementos-orbitales.git
cd Simulaciones-Elementos-orbitales
python "semiejes-excentricidad.py"

text

Reemplaza el nombre del archivo por el que quieras ejecutar.

### Opción 2: Desde Google Colab

1. Sube el archivo `.py` que quieras correr.
2. Ejecuta la celda con `!python nombre_archivo.py`.
3. Se abrirá la escena 3D en una ventana emergente.

---

## Descripción de cada simulación

### 1. `semiejes-excentricidad.py`

Muestra de forma didáctica:

- El **semieje mayor (a)** de la órbita terrestre.
- El **semieje menor (b)** calculado como `b = a·√(1 − e²)`.
- El valor numérico de la **excentricidad (e)**.

Al finalizar la primera órbita completa, la simulación pausa y muestra los elementos gráficamente.

### 2. `Longitud nodo.py`

Visualiza:

- La **línea de nodos** (intersección entre el plano orbital y la eclíptica).
- El **nodo ascendente** y **descendente**.
- El **arco de la longitud del nodo ascendente (Ω)**.
- El **arco de la inclinación orbital (i)**.

### 3. `Anomalia-Argumento.py`

Ilustra:

- El **vector excentricidad**.
- La **anomalía verdadera (θ)** como ángulo entre el vector excentricidad y el vector posición.
- El **argumento del perihelio (ω)**.
- El **arco de la inclinación (i)**.

### 4. `solstiequi.py`

Simula los **solsticios y equinoccios** con dos modos:

- **Geocéntrico** (Tierra fija): el Sol se mueve según los cálculos astronómicos del **NOAA** (Julian Day).
- **Heliocéntrico** (Sol fijo): la Tierra se mueve según la ecuación de Kepler.

Detecta eventos y pausa automáticamente la simulación para señalarlos.

### 5. `colisión.py`

Simulación del acercamiento entre la **Tierra** y el asteroide **433 Eros**:

- Gráfica de la **distancia Tierra–Eros** en UA reales.
- Gráfica de las **distancias al Sol** de ambos cuerpos.
- **Deslizadores** para modificar excentricidad, inclinación y velocidad angular.
- Detección de **acercamientos notables** y **colisiones**.

### 6. `sistema solar.py`

Simulación completa del Sistema Solar con:

- **Sol, Tierra, Luna, Eros, Júpiter y Saturno** (con anillos).
- **Selector de objetos** (modo normal, par, impar) para elegir qué mostrar.
- **Gráficas** de distancia al Sol y energía cinética (vis-viva).
- Detección de **eclipses solares y lunares**.
- Controles para mostrar/ocultar nodos, planos orbitales y trayectorias.

---

## Fundamento físico

Cada simulación parte de los **elementos orbitales** del cuerpo correspondiente:

| Elemento | Símbolo | Significado |
|---|---|---|
| Semieje mayor | `a` | Tamaño de la órbita |
| Excentricidad | `e` | Qué tan ovalada es la órbita |
| Inclinación | `i` | Ángulo respecto a la eclíptica |
| Longitud del nodo ascendente | `Ω` | Ángulo del nodo ascendente |
| Argumento del perihelio | `ω` | Ángulo del perihelio |
| Anomalía media | `M` | Posición angular media |

La posición se obtiene resolviendo la **ecuación de Kepler** `M = E − e·sin(E)` mediante el método de Newton-Raphson, y transformando después a coordenadas cartesianas eclípticas.

---

## Cómo citar

Si usas este software en tu investigación o docencia, por favor cítalo así:

> <Tu Apellido>, <Tu Nombre>. (2026). *Simulaciones de Elementos Orbitales* (Versión 1.0.0) [Software]. GitHub. https://github.com/tiancris001-bit/Simulaciones-Elementos-orbitales

O usa el botón **"Cite this repository"** en la barra lateral de GitHub.

---

## Licencia

Este proyecto está bajo la licencia **Apache 2.0**. Consulta el archivo `LICENSE` para más detalles.

---



