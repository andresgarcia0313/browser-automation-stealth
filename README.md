# Browser Automation Stealth

Herramientas de automatización de navegador anti-detección para uso con Claude Code y tareas de IA.

## Descripción

Este proyecto contiene configuraciones y scripts para controlar navegadores web de forma automatizada sin ser detectado como bot. Incluye dos herramientas principales:

- **Camoufox** (Python) - Firefox con fingerprint inyectado a nivel C++
- **Ulixee Hero** (Node.js) - Chrome con comportamiento humano nativo

## Características

| Característica | Camoufox | Hero |
|----------------|----------|------|
| Tasa de detección | ~1-3% | ~5-10% |
| Modo visible | ✅ | ✅ |
| Modo background | ✅ (virtual display) | ✅ (headless) |
| Múltiples instancias | ✅ | ✅ |
| Comportamiento humano | Cursor nativo C++ | Mouse/typing nativo |
| Lenguaje | Python | Node.js |

## Estructura del Proyecto

```
browser-automation-stealth/
├── README.md                    # Este archivo
├── docs/
│   ├── INVESTIGACION.md         # Comparativo de herramientas
│   ├── INSTALACION.md           # Guía de instalación paso a paso
│   └── USO.md                   # Ejemplos de uso
├── src/
│   ├── python/
│   │   ├── camoufox_browser.py  # Utilidad principal Camoufox
│   │   ├── test_parallel.py     # Test de instancias paralelas
│   │   └── demo_mercadolibre.py # Demo de búsqueda en ML
│   └── nodejs/
│       ├── hero_browser.mjs     # Utilidad principal Hero
│       ├── test_parallel_hero.mjs # Test paralelo Hero
│       └── package.json
├── examples/
│   └── uso_basico.py            # Ejemplos simples
└── screenshots/                 # Capturas de demostración
```

## Instalación Rápida

### Camoufox (Recomendado)

```bash
# Instalar Camoufox
pip install camoufox[geoip]

# Descargar navegador
python -m camoufox fetch

# Instalar Xvfb (para modo background)
sudo apt install xvfb
```

### Ulixee Hero

```bash
# Instalar Hero
npm install @ulixee/hero-playground

# Configurar sandbox de Chrome
sudo chown root:root ~/.cache/ulixee/chrome/*/chrome-sandbox
sudo chmod 4755 ~/.cache/ulixee/chrome/*/chrome-sandbox
```

## Uso Básico

### Camoufox - Modo Visible

```python
from camoufox.sync_api import Camoufox

with Camoufox(headless=False, humanize=True) as browser:
    page = browser.new_page()
    page.goto("https://google.com")
    page.fill('textarea[name="q"]', "mi búsqueda")
    page.press('textarea[name="q"]', "Enter")
```

### Camoufox - Modo Background

```python
from camoufox.sync_api import Camoufox

# headless="virtual" usa display virtual (menos detectable que headless=True)
with Camoufox(headless="virtual", humanize=True) as browser:
    page = browser.new_page()
    page.goto("https://google.com")
    # El navegador es invisible, puedes usar tu PC
```

### Hero - Modo Background

```javascript
import Hero from '@ulixee/hero-playground';

const hero = new Hero({ showChrome: false });
await hero.goto('https://google.com');
await hero.type('mi búsqueda');
await hero.close();
```

## Modos de Operación

| Modo | Camoufox | Hero | Descripción |
|------|----------|------|-------------|
| **Visible** | `headless=False` | `showChrome: true` | Ves el navegador |
| **Background** | `headless="virtual"` | `showChrome: false` | Invisible, display virtual |
| **Headless puro** | `headless=True` | N/A | Más detectable |

## Cuándo Usar Cada Herramienta

| Caso de Uso | Herramienta | Razón |
|-------------|-------------|-------|
| Máxima evasión | Camoufox | Fingerprint C++, menos detectable |
| Comportamiento humano complejo | Hero | Mouse/typing naturales |
| Scripts Python | Camoufox | Integración nativa |
| Scripts Node.js | Hero | API rica |
| Múltiples instancias paralelas | Camoufox | Más estable |

## Integración con Claude Code

Los scripts están configurados para usarse desde Claude Code:

```python
import sys
sys.path.insert(0, '/home/andres/.claude/browser-tools')
from camoufox_browser import browse, search_mercadolibre

# Navegar a cualquier URL
result = browse("https://example.com", visible=True)

# Buscar en MercadoLibre
products = search_mercadolibre("laptop gaming", visible=False)
```

## Tests Realizados

### Test Paralelo Camoufox (3 instancias)
- **Tiempo:** 35.8 segundos
- **Screenshots:** 12 capturas
- **Resultado:** 100% éxito en Google y GitHub

### Test Paralelo Hero (3 instancias)
- **Tiempo:** 13.7 segundos
- **Screenshots:** 7 capturas
- **Resultado:** Parcial (limitaciones de Playground)

## Documentación Adicional

- [Investigación de Herramientas](docs/INVESTIGACION.md) - Comparativo completo
- [Guía de Instalación](docs/INSTALACION.md) - Paso a paso detallado
- [Ejemplos de Uso](docs/USO.md) - Casos de uso comunes

## Requisitos del Sistema

- Python 3.9+
- Node.js 18+
- Linux (Ubuntu/Debian recomendado)
- Xvfb (para modo background)
- 4GB RAM mínimo

## Fecha de Creación

2025-12-30

## Autor

Configurado con Claude Code (Anthropic)
