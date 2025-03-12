# Configuración de Icecast y ICES2 para FondoRadio

Este documento describe cómo configurar Icecast y ICES2 para transmitir una radio en `fondomarcador.com/icecast/`.

## Estructura de archivos

```plaintext
icecast/
├── icecast.xml
├── ices2
│   ├── Dockerfile
│   └── ices-playlist.xml
├── mymusic
│   ├── Entradilla1.ogg
│   ├── Entradilla2.ogg
│   ├── Entradilla3.ogg
│   └── list.txt
└── README.md
```

## Archivos de configuración

### 1. `icecast.xml`

Este archivo configura el servidor Icecast. Aquí se definen los límites de clientes, autenticación, puertos de escucha, rutas de archivos y configuración de registros.

### 2. `ices-playlist.xml`

Este archivo configura ICES2 para transmitir una lista de reproducción a Icecast. Aquí se definen los metadatos del stream, la lista de reproducción y la configuración de conexión al servidor Icecast.

### 3. `list.txt`

Este archivo contiene la lista de reproducción de archivos de audio que ICES2 transmitirá a Icecast.

### 4. `Dockerfile`

Este archivo crea una imagen de Docker que contiene ICES2 configurado para transmitir la lista de reproducción definida en `ices-playlist.xml`.

También hay que tener en cuenta que hay otro contenedor en el Docker-Compose para Icecast2, con la imagen de `libretime/icecast`, perfecta para aarch64.

[Ver Docker-Compose](../../docker-compose.yml#L34)

### 5. `fondomarcador.conf`

Este archivo configura Nginx para servir como proxy inverso para Icecast y otros servicios en `fondomarcador.com`.

[Ver configuración](../../src/nginx/nginxconf/fondomarcador.conf#L108)

### 6. `icecast.py`

Este archivo automatiza la descarga del video que se le pasa al bot de telegram. Su contenedor tiene un volumen compartido con el contenedor de ICES2, enviando las canciones y la modificación de la lista a ices2 directamente.

[Ver Documentación](../../scripts/telegramBot/README.md)

## Configuración de archivos

Vamos a profundizar en la configuración tanto de Icecast como ICES2, explicando cómo funciona su estructura. Por lo que Ices2 actúa como un cliente de fuente que toma archivos de audio o listas de reproducción, los codifica en formato OGG Vorbis y los transmite a Icecast2 a través de un punto de montaje predefinido; Icecast2, como servidor de streaming, recibe esta señal y la redistribuye a los clientes conectados, permitiendo la reproducción en tiempo real.

### 1. `icecast.xml` [Configuración de Icecast](./icecast.xml)

#### `<limits>`
- `<clients>100</clients>`: Número máximo de clientes simultáneos.
- `<sources>2</sources>`: Número máximo de fuentes de audio activas.

#### `<authentication>`
- `<admin-user>admin</admin-user>`: Usuario de administración.
- `<admin-password>hackme</admin-password>`: Contraseña de administración.
- `<source-password>sourcepass</source-password>`: Contraseña para fuentes de audio.

#### `<listen-socket>`
- `<port>8000</port>`: Puerto donde Icecast escucha.

#### `<fileserve>`
- `<fileserve>1</fileserve>`: Habilita la opción de servir archivos estáticos.

#### `<paths>`
- `<logdir>/var/log/icecast</logdir>`: Ruta de los logs.
- `<webroot>/usr/share/icecast/web</webroot>`: Ruta de la interfaz web.

#### `<logging>`
- `<accesslog>access.log</accesslog>`: Archivo de log de accesos.
- `<loglevel>3</loglevel>`: Nivel de log: `3` (informativo).

#### `<mount>`
- `<mount-name>/stream</mount-name>`: Punto de montaje del stream.
- `<password>sourcepass</password>`: Contraseña de la fuente.

---

### 2. `ices-playlist.xml` [Configuración de ICES2](./ices2/ices-playlist.xml)

#### `<logpath>` y `<logfile>`
- `<logpath>/var/log/ices2</logpath>`: Ruta de los logs.
- `<logfile>ices.log</logfile>`: Archivo de log de Ices2.

#### `<stream>`
- `<metadata>`: Información sobre el stream (nombre, género, descripción).
- `<input>`: Configura la entrada de la lista de reproducción.
  - `<module>playlist</module>`: Usa una lista de reproducción.
  - `<param name="file">/songs/list.txt</param>`: Ruta de la lista de canciones.
  - `<param name="random">0</param>`: Reproducción aleatoria desactivada.
  - `<param name="restart-after-reread">0</param>`: No reiniciar después de releer.
  - `<param name="once">0</param>`: Repetir la lista de reproducción.

- `<instance>`
  - `<hostname>icecast</hostname>`: Nombre del servidor Icecast.
  - `<port>8000</port>`: Puerto del servidor Icecast.
  - `<password>sourcepass</password>`: Contraseña de la fuente.
  - `<mount>/stream</mount>`: Punto de montaje en Icecast.

#### Reconexión automática
- `<reconnectdelay>2</reconnectdelay>`: Tiempo de espera entre reconexiones.
- `<reconnectattempts>5</reconnectattempts>`: Número de intentos de reconexión.

## Solución de problemas

### Problemas comunes con la lista de canciones:

- **Sin canciones**: ICES2 no funcionará, mostrando un error al no encontrar canciones en la lista.
- **1 canción**: ICES2 funcionará, pero al finalizar la canción, se detendrá.
- **2 o más canciones**: ICES2 funcionará correctamente, y las canciones se pondrán en cola, repitiéndose según el parámetro `random` (0 = lineal, 1 = aleatorio).
