# Proyecto de Bot de Telegram para Streaming Multimedia

Este es un proyecto que implementa un bot de Telegram para automatizar la descarga y el streaming de contenido multimedia desde YouTube. El bot descarga videos y audios de YouTube y los prepara para su transmisión mediante servidores NGINX (para video) e Icecast (para audio).

## Requisitos

1. Python 3
2. PIP (gestor de paquetes de Python)
3. Virtualenv (entorno virtual para Python)

## Pasos para la instalación

Sigue los siguientes pasos para instalar y ejecutar el bot:

### 1. Instalar Python

En primer lugar, instala Python 3 si aún no lo tienes instalado. Puedes hacerlo con el siguiente comando:

```bash
sudo apt install python3
```

### 2. Instalar PIP

Instala PIP, el gestor de paquetes para Python, utilizando el siguiente comando:

```bash
sudo apt install python3-pip
```

### 3. Instalar entorno virtual

Es recomendable usar un entorno virtual para el proyecto. Esto asegura que las dependencias de tu proyecto estén aisladas del sistema. Para ello, instala el paquete python3-venv:

``` bash
sudo apt install python3-venv
```
### 4. Crear entorno virtual

Crea el entorno virtual para tu proyecto con el siguiente comando:

``` bash
python3 -m venv myenv
```
### 5. Activar entorno virtual

Activa el entorno virtual para que puedas usar las librerías y dependencias instaladas solo dentro de ese entorno:

``` bash
source myenv/bin/activate
```
Cuando el entorno esté activo, deberías ver algo como (myenv) antes de la línea de comandos.

### 6. Instalar dependencias

Instala la librería python-telegram-bot utilizando pip dentro del entorno virtual:

``` bash
cd /usr/local/bin/telegram
rm -rf myenv
pip install python_dotenv python-telegram-bot yt_dlp flask requests
```

### 7. Iniciar el bot

Una vez que el entorno esté configurado y las dependencias estén instaladas, puedes ejecutar el bot con el siguiente comando:

``` bash
python bot.py
```
Esto iniciará el bot y debería comenzar a escuchar mensajes y comandos desde Telegram.

### 8. Desactivar entorno virtual

Cuando hayas terminado de trabajar con el proyecto, puedes desactivar el entorno virtual con el siguiente comando:
``` bash
deactivate
```

Este comando devolverá tu terminal a su estado normal y desactivará el entorno virtual.
## Estructura del proyecto

La estructura del proyecto debería lucir algo así:
``` bash
.
├── bot.py       # Código del bot
├── myenv/       # Entorno virtual
└── README.md
```

# Problemas
Actualmente no está funcionando automaticamente, es necesario hacer un 
``` bash
docker exec -ti nginx /bin/bash 
```
Hacer un entorno, entrar y 
``` bash
python3 bot.py && python3 backend.py
```
Esto se pondrá más adelante 

https://medium.com/@peer5/setting-up-hls-live-streaming-server-using-nginx-67f6b71758db