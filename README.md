# 🖥️ Fut OS - Simulador de Escritorio Interactivo

`ui.py` es el núcleo gráfico de **Fut OS**, un entorno de escritorio interactivo desarrollado con `tkinter` en Python. Este entorno simula funciones básicas de un sistema operativo, integrando elementos como un navegador web, un terminal interactivo, un dock con reloj, fondos personalizados y minijuegos como Pong.

## 🚀 Características principales

- **Interfaz gráfica moderna** con `tkinter` y `ttk`, adaptada a pantallas grandes (1280x720).
- **Simulación de rutas de archivos** en un sistema de usuario virtual.
- **Carga de fondos personalizados** mediante `PIL`.
- **Navegador web integrado** usando `tkinterweb`.
- **Terminal interactiva** con ejecución de comandos en tiempo real (`subprocess`).
- **Integración de minijuegos**, por ejemplo `pong.py`.
- **Estilización personalizada** con temas y configuraciones para botones, etiquetas y entradas.

## 📂 Estructura esperada

El sistema espera una ruta base de archivos en:
```
/Users/aquiles/PycharmProjects/ShellUI/user
```


## 📦 Requisitos

- Python 3.x
- Bibliotecas:
  - `tkinter`
  - `PIL` (Pillow)
  - `tkinterweb`
  - `pong.py` (archivo de minijuego)

Puedes instalar los paquetes requeridos con:

```bash
pip install pillow tkinterweb
```

