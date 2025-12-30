# Guía de Instalación Completa

Instrucciones paso a paso para instalar y configurar las herramientas de browser automation anti-detección.

## Requisitos Previos

### Sistema Operativo
- Linux (Ubuntu 22.04+ / Debian 12+ recomendado)
- También funciona en macOS y Windows (con ajustes)

### Software Base
```bash
# Python 3.9+
python3 --version

# Node.js 18+
node --version

# pip
pip3 --version

# npm
npm --version
```

### Dependencias del Sistema (Linux)
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    xvfb \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libxt6 \
    libasound2
```

---

## Instalación de Camoufox (Python)

### Paso 1: Instalar el paquete

```bash
# Opción A: Instalación global
pip3 install -U camoufox[geoip]

# Opción B: En entorno virtual (recomendado)
python3 -m venv ~/venvs/browser-automation
source ~/venvs/browser-automation/bin/activate
pip install -U camoufox[geoip]
```

### Paso 2: Descargar el navegador Camoufox

```bash
python3 -m camoufox fetch
```

Esto descarga Firefox modificado (~200MB) a `~/.cache/camoufox/`

### Paso 3: Instalar Xvfb (para modo background)

```bash
sudo apt install -y xvfb
```

### Paso 4: Verificar instalación

```python
# test_camoufox.py
from camoufox.sync_api import Camoufox

with Camoufox(headless=False, humanize=True, i_know_what_im_doing=True) as browser:
    page = browser.new_page()
    page.goto("https://www.google.com")
    print(f"Título: {page.title()}")
    page.wait_for_timeout(3000)

print("Camoufox instalado correctamente!")
```

```bash
python3 test_camoufox.py
```

---

## Instalación de Ulixee Hero (Node.js)

### Paso 1: Crear directorio del proyecto

```bash
mkdir -p ~/.claude/browser-tools
cd ~/.claude/browser-tools
npm init -y
```

### Paso 2: Instalar Hero

```bash
npm install @ulixee/hero-playground
```

### Paso 3: Configurar sandbox de Chrome

Hero descarga Chrome automáticamente. El sandbox necesita permisos especiales:

```bash
# Encontrar la versión de Chrome descargada
CHROME_DIR=$(ls -d ~/.cache/ulixee/chrome/*/ | head -1)

# Configurar permisos del sandbox
sudo chown root:root ${CHROME_DIR}chrome-sandbox
sudo chmod 4755 ${CHROME_DIR}chrome-sandbox

# Verificar
ls -la ${CHROME_DIR}chrome-sandbox
# Debe mostrar: -rwsr-xr-x 1 root root ...
```

### Paso 4: Verificar instalación

```javascript
// test_hero.mjs
import Hero from '@ulixee/hero-playground';

const hero = new Hero({ showChrome: true });
await hero.goto('https://www.google.com');
console.log('Título:', await hero.document.title);
await hero.waitForMillis(3000);
await hero.close();
console.log('Hero instalado correctamente!');
```

```bash
node test_hero.mjs
```

---

## Configuración para Claude Code

### Paso 1: Copiar scripts de utilidad

```bash
# Crear directorio de herramientas de Claude
mkdir -p ~/.claude/browser-tools

# Copiar scripts (desde este proyecto)
cp src/python/*.py ~/.claude/browser-tools/
cp src/nodejs/*.mjs ~/.claude/browser-tools/
cp src/nodejs/package.json ~/.claude/browser-tools/

# Instalar dependencias de Node en el directorio
cd ~/.claude/browser-tools && npm install
```

### Paso 2: Actualizar CLAUDE.md

Agregar a `~/.claude/CLAUDE.md`:

```markdown
## Browser Automation (Anti-Detección)

Tengo acceso a navegadores anti-detección:

| Herramienta | Lenguaje | Ubicación |
|-------------|----------|-----------|
| **Camoufox** | Python | `~/.claude/browser-tools/camoufox_browser.py` |
| **Hero** | Node.js | `~/.claude/browser-tools/hero_browser.mjs` |

### Uso rápido

```python
import sys
sys.path.insert(0, '/home/andres/.claude/browser-tools')
from camoufox_browser import browse

result = browse("https://example.com", visible=True)
```
```

---

## Solución de Problemas

### Error: "Please install Xvfb to use headless mode"

```bash
sudo apt install -y xvfb
```

### Error: "chrome-sandbox is not configured correctly"

```bash
CHROME_DIR=$(ls -d ~/.cache/ulixee/chrome/*/ | head -1)
sudo chown root:root ${CHROME_DIR}chrome-sandbox
sudo chmod 4755 ${CHROME_DIR}chrome-sandbox
```

### Error: "No module named 'camoufox'"

```bash
pip3 install -U camoufox[geoip]
```

### Error: "Cannot find module '@ulixee/hero-playground'"

```bash
cd ~/.claude/browser-tools
npm install @ulixee/hero-playground
```

### Camoufox no abre (sin errores)

Verificar que tienes display disponible:
```bash
echo $DISPLAY
# Debe mostrar algo como :0 o :1
```

Si está vacío (SSH sin X11):
```bash
# Usar modo virtual
headless="virtual"
```

### Hero cierra inmediatamente

La versión Playground cierra automáticamente. Para producción usar Client/Core:
```bash
npm install @ulixee/hero @ulixee/cloud
```

---

## Verificación Final

### Test completo Camoufox

```bash
cd ~/Desarrollo/AI/browser-automation-stealth
python3 src/python/test_parallel.py
```

Debe crear 12 screenshots en `/tmp/browser_parallel_test/`

### Test completo Hero

```bash
cd ~/Desarrollo/AI/browser-automation-stealth
node src/nodejs/test_parallel_hero.mjs
```

Debe crear screenshots en `/tmp/hero_parallel_test/`

---

## Actualización

### Camoufox

```bash
pip3 install -U camoufox[geoip]
python3 -m camoufox fetch  # Re-descargar navegador si hay nueva versión
```

### Hero

```bash
cd ~/.claude/browser-tools
npm update @ulixee/hero-playground
```

---

## Desinstalación

### Camoufox

```bash
pip3 uninstall camoufox
rm -rf ~/.cache/camoufox/
```

### Hero

```bash
rm -rf ~/.claude/browser-tools/node_modules
rm -rf ~/.cache/ulixee/
```

---

*Guía creada: 2025-12-30*
