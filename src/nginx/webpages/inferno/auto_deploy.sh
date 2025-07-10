#!/bin/bash

# Colores ANSI
CRE='\033[31m'  # Rojo
CGR='\033[32m'  # Verde
CBL='\033[34m'  # Azul
CBLE='\033[36m' # Cyan
CBK='\033[37m'  # Blanco
CNC='\033[0m'   # Resetear colores

printf "\n"

printf "${CRE}⠀⠀⠀⡠⢺⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⢸⢢⠀⠀⠀⠀   \n"
printf "${CRE}⠀⠀⣰⠁⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⢸⠀⢳⠀⠀⠀ \n"
printf "${CRE}⠀⢠⡇⠀⢸⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⢸⠀⠀⡇⠀⠀ \n"
printf "${CRE}⠀⢸⡄⠀⠀⠢⣠⣴⡋⠉⠁⠀⠀⠀⠀⠀⠈⠻⣶⣄⡠⠃⠀⠀⡇⠀⠀ \n"
printf "${CRE}⡀⠈⣧⠀⠀⠀⠈⡇⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡏⠀⠀⠀⢠⠇⠀⡀ \n"
printf "${CRE}⣷⡀⠘⣆⠀⠀⠀⣿⠀⠀⠀⠀⠀⢀⣀⣠⡤⢾⣿⡁⠀⠀⢠⡟⠀⣴⡇ \n"
printf "${CRE}⡏⢻⣦⡘⣷⣦⠼⠃⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠻⢷⣤⣴⡏⣠⡾⠃⡇   \n"
printf "${CRE}⢳⠀⠙⢿⣿⡏⠀⠀⠀⡰⠃⠀⠀⠀⠀⠀⠣⡀⠀⠀⠀⢹⣿⠟⠀ ⡇⠀   \n"
printf "${CRE}⠈⢧⡀⢸⣿⣿⣀⡀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⣀⠀⠈⣿⠀⢀⠌⠀  \n"
printf "${CRE}⠀⠀⠙⢾⣿⣿⣿⣿⡗⢄⡀⠀⡀⠀⡀⠀⡀⠔⡿⠀⠀⠀⣿⠔⠁⠀⠀   \n"
printf "${CRE}⠀⠀⠀⠀⢿⣿⡋⠉⠙⠒⠉⠙⡇⢀⡟⠉⠑⠊⠁⠀⠀⢠⠇⠀⠀⠀⠀   \n"
printf "${CRE}⠀⠀⠀⠀⠈⠻⡇⠀⠀⠀⢀⠀⠃⢸⣷⣀⠀⠀⠀⢀⡴⠃⠀⠀⠀⠀⠀   \n"
printf "${CRE}⠀⠀⠀⠀⠀⠀⣿⣶⣶⣖⠛⠦⠀⠈⡿⠟⢑⣶⣶⣾⠇⠀⠀⠀⠀⠀⠀   \n"
printf "${CRE}⠀⠀⠀⠀⠀⠀⢻⣯⠉⢩⠧⠄⠓⠒⠁⣔⢵⠈⣡⣿⠀⠀⠀⠀⠀⠀⠀   \n"
printf "${CRE}⠀⠀⠀⠀⠀⠀⠈⢿⣧⠘⢜⣉⣁⣈⣉⣏⠄⢰⣿⠃⠀⠀⠀⠀⠀⠀⠀   \n"
printf "${CRE}⠀⠀⠀⠀⠀⠀⠀⠈⢿⡀⠀⠐⠒⠒⠒⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀   \n"
printf "${CRE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢤⣀⣀⣀⣀⣠⠜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀   \n"
printf "${CRE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⣉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   \n"
printf "\n"



# Validación de argumentos
if [ $# -ne 1 ]; then
    echo -e "${CRE}Uso: $0 <archivo_tar>${CNC}"
    exit 1
fi

TAR_FILE="$1"
IMAGE_NAME=$(basename "$TAR_FILE" .tar)
CONTAINER_NAME="${IMAGE_NAME}_container"

# Comprobar si Docker está instalado
docker -v &> /dev/null || { echo -e "${CRE}Docker no está instalado.${CNC}"; exit 1; }

# Eliminar contenedor e imagen previos
if docker ps -aq -f name=$CONTAINER_NAME &> /dev/null; then
    echo -e "${CBL}Eliminando contenedor previo: $CONTAINER_NAME...${CNC}"
    docker stop $CONTAINER_NAME &> /dev/null
    docker rm $CONTAINER_NAME &> /dev/null
fi

if docker images -q $IMAGE_NAME &> /dev/null; then
    echo -e "${CBL}Eliminando imagen previa: $IMAGE_NAME...${CNC}"
    docker rmi $IMAGE_NAME &> /dev/null
fi

# Cargar la imagen desde el archivo TAR
echo -e "${CGR}Cargando la imagen desde el archivo: $TAR_FILE...${CNC}"
docker load -i "$TAR_FILE" || { echo -e "${CRE}Error al cargar la imagen Docker.${CNC}"; exit 1; }

# Verificar si existe un archivo docker-compose.yml
echo -e "${CGR}Desplegando la máquina vulnerable...${CNC}"
if [ -f "docker-compose.yml" ]; then
    docker-compose up -d

    echo -e "${CBLE}IPs de los servicios desplegados:${CNC}"
    
    # Obtener todos los contenedores del proyecto docker-compose
    CONTAINERS=$(docker-compose ps -q)

    for cid in $CONTAINERS; do
        NAME=$(docker inspect -f '{{.Name}}' "$cid" | sed 's/^\/\(.*\)/\1/')
        IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$cid")
        echo -e "  ${CBK}$NAME${CNC} -> ${CBLE}$IP${CNC}"
    done
else
    docker run -d --name $CONTAINER_NAME $IMAGE_NAME

    # Obtener la IP del contenedor
    IP_ADDRESS=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CONTAINER_NAME 2>/dev/null)
    echo -e "${CBLE}Máquina desplegada con IP: ${CBK}$IP_ADDRESS${CNC}"
fi

echo -e "${CRE}Presiona Ctrl+C cuando termines para eliminar la máquina${CNC}"

# Capturar Ctrl+C para limpiar
trap cleanup INT
cleanup() {
    echo -e "\n${CRE}Eliminando laboratorio...${CNC}"
    if [ -f "docker-compose.yml" ]; then
        docker-compose down
    else
        docker stop $CONTAINER_NAME &> /dev/null
        docker rm $CONTAINER_NAME &> /dev/null
        docker rmi $IMAGE_NAME &> /dev/null
    fi
    echo -e "${CBLE}Laboratorio eliminado.${CNC}"
    exit 0
}

# Mantener el script en ejecución
while true; do sleep 1; done
