#!/bin/bash

# Colores para hacerlo más llamativo
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

API_KEY="7fd025b65326487b96f0b3ceb542515d"
COMPETITION="PD"

mostrar_banner() {
    clear
    echo -e "${NC}"
    echo -e "${NC}███████╗██╗   ██╗████████╗"
    echo -e "${NC}██╔════╝██║   ██║╚══██╔══╝"
    echo -e "${NC}█████╗  ██║   ██║   ██║   "
    echo -e "${NC}██╔══╝  ██║   ██║   ██║   "
    echo -e "${NC}██║     ╚██████╔╝   ██║   "
    echo -e "${NC}╚═╝      ╚═════╝    ╚═╝   "
    echo -e "${YELLOW}     ██████╗ ███████╗"
    echo -e "${YELLOW}    ██╔═══██╗██╔════╝"
    echo -e "${YELLOW}    ██║   ██║███████╗"
    echo -e "${YELLOW}    ██║   ██║╚════██║"
    echo -e "${YELLOW}    ╚██████╔╝███████║"
    echo -e "${YELLOW}     ╚═════╝ ╚══════╝"

    echo -e "${YELLOW}⚽ Bienvenido a FUTOS - Tu Shell de Fútbol ⚽${NC}"
    echo -e "Escribe 'help' para ver la lista de comandos disponibles."
}

# Función para instalar jq si no está instalado
install_jq() {
    # Verificar si jq está instalado
    if ! command -v jq &> /dev/null; then
        echo -e "${CYAN}jq no está instalado. Instalando jq...${NC}"

        # Detectar el sistema operativo y usar el gestor de paquetes adecuado
        if [ -x "$(command -v apt)" ]; then
            # Para Debian/Ubuntu
            sudo apt update && sudo apt install -y jq
        elif [ -x "$(command -v brew)" ]; then
            # Para macOS
            brew install jq
        else
            echo -e "${RED}No se puede instalar jq automáticamente. Por favor, instálalo manualmente.${NC}"
        fi
    else
        echo -e "${CYAN}jq ya está instalado.${NC}"
    fi
}

# Función para instalar
install() {
    echo -e "${GREEN}Instalando...${NC}"
    mkdir -p ~/futshell_instalacion
    mkdir -p ~/futshell_instalacion/shell
    wget -q -O ~/futshell_instalacion/futshell.sh https://raw.githubusercontent.com/Soup-Sopas/Futball-shell/refs/heads/main/futshell.sh
    echo "Archivo de prueba" > ~/futshell_instalacion/test.txt

    install_jq

    wget -q -O ~/futshell_instalacion/github_file.txt https://raw.githubusercontent.com/Soup-Sopas/Futball-shell/refs/heads/main/README.md

    # Mensaje de instalación completa con enlace y pasos para iniciar la shell interactiva
    echo -e "${GREEN}Instalación completa.${NC}"
    echo -e "${CYAN}La carpeta de instalación se guardó en: ~/futshell_instalacion${NC}"
    echo -e "${CYAN}Puedes acceder a esta carpeta con el siguiente comando: ${NC}"
    echo -e "${YELLOW}cd ~/futshell_instalacion${NC}"
    echo -e "${CYAN}Para iniciar la shell interactiva, ejecuta el siguiente comando: ${NC}"
    echo -e "${YELLOW}./futshell_instalacion/futshell.sh interactive${NC}"
    
    # Instrucción si no se pueden ejecutar los comandos debido a permisos
    echo -e "${CYAN}Si el script no se ejecuta correctamente, asegúrate de darle permisos de ejecución con el siguiente comando:${NC}"
    echo -e "${YELLOW}chmod +x ~/futshell_instalacion/futshell.sh${NC}"
    echo -e "${CYAN}Luego vuelve a intentar ejecutar la shell interactiva con:${NC}"
    echo -e "${YELLOW}./futshell_instalacion/futshell.sh interactive${NC}"
    echo -e "${CYAN}¡Disfruta de la experiencia FUTOS!${NC}"
}

# Función para desinstalar
uninstall() {
    echo -e "${RED}Desinstalando...${NC}"
    rm -rf ~/futshell_instalacion
    echo -e "${RED}Desinstalación completa.${NC}"
}

# Mini-juego: Adivina el número con efectos visuales
game() {
    # Opciones posibles para tirar el penalti
    local OPCIONES=("izquierda-abajo" "derecha-abajo" "medio-arriba" "izquierda-arriba" "derecha-arriba" "medio-abajo")

    # Función para mostrar la portería con el portero en el centro
    mostrar_porteria() {
        echo -e "${YELLOW}🥅 ¡Aquí está la portería! 🧤${NC}"
        echo -e "---------------------------------"
        echo -e "|  [ ]       [ ]       [ ]  |"
        echo -e "|             🧤            |"
        echo -e "|  [ ]       [ ]       [ ]  |"
        echo -e "---------------------------------"
    }

    # Función para animar el portero moviéndose (sin borrar pantalla)
    animacion_portero() {
        echo -e "\n${YELLOW}🥅 🧤 El portero se mueve a la izquierda...${NC}"
        sleep 1
        echo -e "${YELLOW}🥅 🧤 El portero vuelve al centro...${NC}"
        sleep 1
        echo -e "${YELLOW}🥅 🧤 El portero se mueve a la derecha...${NC}"
        sleep 1
        echo -e "${YELLOW}🥅 ¡TIRA EL PENALTI! ⚽${NC}"
        sleep 1
    }

    # Función para que el portero elija dos direcciones distintas
    elegir_lugares_portero() {
        PORTERO_1=${OPCIONES[$((RANDOM % 6))]}
        
        # Elegir una segunda posición que sea distinta de la primera
        while true; do
            PORTERO_2=${OPCIONES[$((RANDOM % 6))]}
            if [[ "$PORTERO_2" != "$PORTERO_1" ]]; then
                break
            fi
        done
    }

    # Función principal del juego
    jugar_penalti() {
        while true; do
            mostrar_porteria
            echo "Elige dónde quieres tirar el penalti:"
            echo -e "1) izquierda-abajo \n2) derecha-abajo \n3) medio-arriba \n4) izquierda-arriba \n5) derecha-arriba \n6) medio-abajo"

            # Leer la elección del usuario
            read -p "👉 Introduce tu elección (escribe el nombre): " ELECCION

            # Validar que la opción sea válida
            if [[ ! " ${OPCIONES[@]} " =~ " ${ELECCION} " ]]; then
                echo -e "${RED}❌ Opción no válida. Debes elegir entre: ${OPCIONES[@]} ${NC}"
                continue  # Volver a preguntar
            fi

            # Animación del portero antes de lanzarse
            animacion_portero

            # El portero elige dos lugares distintos
            elegir_lugares_portero

            # Pausa para leer antes de mostrar resultado
            sleep 2

            # Comprobar si el portero ataja o es gol
            if [[ "$ELECCION" == "$PORTERO_1" ]]; then
                echo -e "\n🧤 El portero se lanza a ${BLUE}$PORTERO_1${NC}..."
                echo -e "${RED}❌ ¡El portero ha parado el penalti! 🧤${NC}"
            elif [[ "$ELECCION" == "$PORTERO_2" ]]; then
                echo -e "\n🧤 El portero se lanza a ${BLUE}$PORTERO_2${NC}..."
                echo -e "${RED}❌ ¡El portero ha parado el penalti! 🧤${NC}"
            else
                echo -e "\n🧤 El portero se lanza a ${BLUE}$PORTERO_1${NC}..."
                echo -e "${GREEN}⚽ ¡GOOOOOOL! 🎉🥳${NC}"
            fi

            # Preguntar si quiere jugar otra vez
            echo -e "\n¿Quieres tirar otro penalti? (s/n)"
            read -p "👉 Escribe 's' para jugar otra vez o 'n' para salir: " RESPUESTA
            if [[ "$RESPUESTA" != "s" ]]; then
                echo -e "${YELLOW}¡Gracias por jugar! ⚽🥅${NC}"
                break
            fi
        done
    }
    jugar_penalti
}


# Mostrar fecha y hora con animación
date_time() {
    echo -ne "Cargando fecha y hora"
    for i in {1..3}; do
        sleep 0.5
        echo -ne "."
    done
    echo -e "\n${BLUE}Fecha y hora actual: $(date)${NC}"
}


# Función para mostrar todos los comandos disponibles
help_menu() {
    echo -e "${YELLOW}Lista de comandos disponibles:${NC}"
    echo -e "${GREEN}install${NC} - Instala archivos y dependencias"
    echo -e "${GREEN}uninstall${NC} - Desinstala y borra los archivos creados"
    echo -e "${GREEN}penalti-game${NC} - Juega un mini-juego de tirar penaltis"
    echo -e "${GREEN}date-time${NC} - Muestra la fecha y hora actual"
    echo -e "${GREEN}interactive${NC} - Inicia la shell interactiva"
    echo -e "${GREEN}resultados${NC} - Te devuelve los resultados de los ultimos 5 partidos"
    echo -e "${GREEN}posiciones${NC} - Te devuelve la tabla des posiciones"
    echo -e "${GREEN}competencia-penalti${NC} - Juega un mini-juego de parar penaltis"
    echo -e "${GREEN}mostrar-pid${NC} - Muestra tu PID actual"
    echo -e "${GREEN}matar-proceso${NC} - Mata el proceso del PID que introduzcas"
    echo -e "${GREEN}crear-proceso${NC} - Crea un proceso hijo que dura 10 segundos"
    echo -e "${GREEN}help${NC} - Muestra este menú de ayuda"
    echo -e "${GREEN}exit${NC} - Cerrar la shell"
}

# Shell interactiva con efectos visuales
interactive_shell() {
    cd 
    cd futshell_instalacion/shell
    mostrar_banner

    shopt -s histappend

    while true; do
        echo -ne "⚽ ${CYAN}$(basename $(pwd)) ~ ${NC}"
        read -e input
        history -s "$input"

        case "$input" in
            install) install ;;
            uninstall) uninstall ;;
            penalti-game) game ;;
            date-time) date_time ;;
            ascii-art) ascii_art ;;
            hacker-mode) hacker_mode ;;
            betting) betting ;;
            resultados) obtener_resultados ;;
            posiciones) obtener_tabla_posiciones ;;
            mostrar-pid) mostrar_pid ;;
            matar-proceso) matar_proceso ;;
            crear-proceso) crear_proceso_hijo ;;
            competencia-penalti) competencia_penalti ;;
            help) help_menu ;;
            exit) break ;;
            *) eval "$input" 2>/dev/null || echo -e "${RED}Comando no reconocido${NC}" ;;
        esac
    done
}

betting() {
    echo -e "${YELLOW}Abriendo el sitio de apuestas...${NC}"
    xdg-open "https://www.bet365.com/" &>/dev/null || open "https://www.bet365.com/" &>/dev/null || start "https://www.bet365.com/"
}

obtener_resultados() {
    echo "Obteniendo resultados de La Liga..."
    
    # Hacer la solicitud a la API
    response=$(curl -s -X GET "https://api.football-data.org/v4/competitions/$COMPETITION/matches?status=FINISHED" \
        -H "X-Auth-Token: $API_KEY" \
        -H "Content-Type: application/json")

    # Verificar si la API respondió correctamente
    if [[ -z "$response" ]]; then
        echo "⚠️ Error: No se pudo obtener la información de la API."
        return
    fi

    # Extraer y formatear los resultados con jq
    echo "$response" | jq -r '.matches[-5:] | .[] | "\(.utcDate): \(.homeTeam.name) \(.score.fullTime.home) - \(.score.fullTime.away) \(.awayTeam.name)"'

}

obtener_tabla_posiciones() {
    echo "📊 Obteniendo tabla de posiciones de La Liga..."
    
    response=$(curl -s -X GET "https://api.football-data.org/v4/competitions/$COMPETITION/standings" \
        -H "X-Auth-Token: $API_KEY" \
        -H "Content-Type: application/json")

    if [[ -z "$response" ]]; then
        echo "⚠️ Error: No se pudo obtener la información de la API."
        return
    fi

    echo "$response" | jq -r '.standings[0].table[] | "\(.position). \(.team.name) - \(.points) pts (PJ: \(.playedGames) | G: \(.won) | E: \(.draw) | P: \(.lost))"'
}

# Función para obtener el PID del proceso actual
mostrar_pid() {
    echo -e "${GREEN}El PID del proceso actual es: $$${NC}"
}

# Función para matar un proceso
matar_proceso() {
    read -p "Introduce el PID del proceso que deseas matar: " PID
    if kill -9 "$PID" 2>/dev/null; then
        echo -e "${GREEN}Proceso $PID terminado exitosamente.${NC}"
    else
        echo -e "${RED}Error: No se pudo terminar el proceso $PID. Asegúrate de que el PID es correcto.${NC}"
    fi
}

# Función para simular un proceso hijo
crear_proceso_hijo() {
    echo -e "${YELLOW}Creando un proceso hijo...${NC}"
    (sleep 10 && echo -e "${CYAN}Proceso hijo terminado después de 10 segundos.${NC}") &
    PIDHIJO=$!
    echo -e "${GREEN}Proceso hijo creado exitosamente, PID = $PIDHIJO${NC}"
}

# Función para simular una competencia de penalti con el rival
competencia_penalti() {
    RESPUESTA=""
    echo -e "${YELLOW}¡Bienvenido al juego de penalti! ¡Tienes que detener al rival!${NC}"
    
    # Explicación del juego
    echo -e "${CYAN}El rival tiene 5 segundos para lanzar su penalti. Tú debes decidir si detenerlo a tiempo.${NC}"
    echo -e "${CYAN}Si decides matar al proceso rival antes de que marque el gol, puedes evitarlo.${NC}"
    echo -e "${YELLOW}¡Buena suerte!${NC}"

    # Generar un número aleatorio entre 1 y 5 usando RANDOM
    TIEMPO_RIVAL=$((RANDOM % 5 + 1))

    # Crear el proceso hijo en segundo plano que simula al rival
    (sleep $TIEMPO_RIVAL && echo -e "${RED}⚽ ¡El rival ha marcado un gol! 💥${NC}") &

    # Obtener el PID del proceso rival
    RIVAL_PID=$!
    echo -e "${CYAN}El PID del proceso rival es: $RIVAL_PID${NC}"

    # Contar hasta 5 segundos para permitir que el usuario reaccione
    echo -e "${YELLOW}¡Tienes $TIEMPO_RIVAL segundos para tomar tu decisión!${NC}"

    # Leer la decisión del usuario
    read -t $TIEMPO_RIVAL -p "¿Quieres matar al proceso rival para evitar el gol? (s/n): " RESPUESTA

    # Si el usuario no responde en 5 segundos, automáticamente se asume que no lo mató
    if [[ -z "$RESPUESTA" ]]; then
        echo -e "${RED}¡El tiempo se agotó!${NC}"
        wait $RIVAL_PID
    elif [[ "$RESPUESTA" == "s" ]]; then
        # El usuario decide matar al proceso
        echo -e "${RED}¡Matando al proceso rival con PID $RIVAL_PID! 💣${NC}"
        kill -9 $RIVAL_PID
        echo -e "${GREEN}¡Has detenido al rival a tiempo! No hubo gol. 🛑${NC}"
    elif [[ "$RESPUESTA" == "n" ]]; then
        # El usuario decide no matar el proceso, entonces el rival lanza el penalti
        echo -e "${YELLOW}Esperando a que termine el proceso y el rival anote gol..."
        wait $RIVAL_PID
    else
        # Si la respuesta no es válida
        echo -e "${RED}Comando no reconocido.${NC}"
        wait $RIVAL_PID
    fi

}

# Comprobar argumentos
case "$1" in
    install) install ;;
    uninstall) uninstall ;;
    penalti) game ;;
    date-time) date_time ;;
    interactive) interactive_shell ;;
    betting) betting ;;
    resultados) obtener_resultados ;;
    posiciones) obtener_tabla_posiciones ;;
    mostrar-pid) mostrar_pid ;;
    matar-proceso) matar_proceso ;;
    crear-proceso) crear_proceso_hijo ;;
    competencia-penalti) competencia_penalti ;;
    help) help_menu ;;
    *) echo -e "${RED}Uso: $0 {install|uninstall|mini-game-1|date-time|interactive|betting|resultados|posiciones|mostrar-pid|matar-proceso|crear-proceso|competencia-penalti|help}${NC}" ;;
esac

