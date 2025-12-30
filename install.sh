#!/bin/bash
#
# Script de instalación rápida - Browser Automation Stealth
# Ejecutar con: bash install.sh
#

set -e

echo "=========================================="
echo "Browser Automation Stealth - Instalación"
echo "=========================================="

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir pasos
step() {
    echo -e "\n${GREEN}[*] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[!] $1${NC}"
}

# 1. Verificar requisitos
step "Verificando requisitos..."

if ! command -v python3 &> /dev/null; then
    echo "Python3 no encontrado. Instalando..."
    sudo apt install -y python3 python3-pip
fi

if ! command -v node &> /dev/null; then
    echo "Node.js no encontrado. Instalando..."
    sudo apt install -y nodejs npm
fi

echo "Python: $(python3 --version)"
echo "Node: $(node --version)"

# 2. Instalar dependencias del sistema
step "Instalando dependencias del sistema..."
sudo apt update
sudo apt install -y xvfb libgtk-3-0 libdbus-glib-1-2 libxt6 libasound2

# 3. Instalar Camoufox
step "Instalando Camoufox..."
pip3 install -U camoufox[geoip]

step "Descargando navegador Camoufox..."
python3 -m camoufox fetch

# 4. Configurar directorio de Claude Code
step "Configurando directorio de herramientas..."
mkdir -p ~/.claude/browser-tools

# Copiar scripts Python
cp src/python/*.py ~/.claude/browser-tools/

# 5. Instalar Hero (opcional)
read -p "¿Instalar Ulixee Hero (Node.js)? [y/N] " install_hero

if [[ "$install_hero" =~ ^[Yy]$ ]]; then
    step "Instalando Ulixee Hero..."
    cd ~/.claude/browser-tools
    cp "$(dirname "$0")/src/nodejs/package.json" .
    npm install

    # Copiar scripts
    cp "$(dirname "$0")/src/nodejs/"*.mjs .

    # Configurar sandbox
    step "Configurando sandbox de Chrome..."
    CHROME_DIR=$(ls -d ~/.cache/ulixee/chrome/*/ 2>/dev/null | head -1)
    if [ -n "$CHROME_DIR" ]; then
        sudo chown root:root "${CHROME_DIR}chrome-sandbox"
        sudo chmod 4755 "${CHROME_DIR}chrome-sandbox"
        echo "Sandbox configurado correctamente"
    else
        warn "Chrome no descargado aún. Ejecutar Hero una vez para descargar."
    fi
fi

# 6. Verificar instalación
step "Verificando instalación..."

echo -e "\nTest Camoufox:"
python3 -c "from camoufox.sync_api import Camoufox; print('  Camoufox OK')" || echo "  Camoufox FALLÓ"

if [[ "$install_hero" =~ ^[Yy]$ ]]; then
    echo -e "\nTest Hero:"
    node -e "import('@ulixee/hero-playground').then(() => console.log('  Hero OK')).catch(() => console.log('  Hero FALLÓ'))"
fi

# 7. Resumen
echo ""
echo "=========================================="
echo "Instalación completada!"
echo "=========================================="
echo ""
echo "Archivos instalados en:"
echo "  ~/.claude/browser-tools/"
echo ""
echo "Uso rápido:"
echo "  python3 -c \""
echo "  import sys"
echo "  sys.path.insert(0, '$HOME/.claude/browser-tools')"
echo "  from camoufox_browser import browse"
echo "  browse('https://google.com', visible=True)"
echo "  \""
echo ""
echo "Documentación:"
echo "  docs/INSTALACION.md"
echo "  docs/USO.md"
echo "  docs/INVESTIGACION.md"
echo ""
