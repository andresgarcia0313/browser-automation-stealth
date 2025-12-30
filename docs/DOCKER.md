# Docker - Browser Automation Stealth

Guía de uso de Docker para ejecutar navegadores anti-detección en contenedores.

## ¿Cuándo Usar Docker?

| Escenario | ¿Usar Docker? | Razón |
|-----------|---------------|-------|
| PC personal con GUI | No necesario | Ya tienes display, ejecuta directamente |
| Servidor sin GUI | **Sí** | El contenedor incluye Xvfb |
| Despliegue en cloud | **Sí** | Imagen lista, sin configurar dependencias |
| CI/CD pipelines | **Sí** | Entorno reproducible |
| Múltiples entornos | **Sí** | Aislamiento y consistencia |
| Compartir con equipo | **Sí** | Misma configuración garantizada |

## Cómo Funciona

El contenedor incluye:
- **Xvfb**: Display virtual (`:99`) donde el navegador "dibuja"
- **Camoufox**: Navegador anti-detección preinstalado
- **Dependencias**: GTK, librerías gráficas, fuentes
- **Python 3.11**: Entorno de ejecución

```
┌─────────────────────────────────────────┐
│             Contenedor Docker           │
│  ┌─────────────────────────────────┐    │
│  │         Xvfb (:99)              │    │
│  │   ┌─────────────────────────┐   │    │
│  │   │      Camoufox           │   │    │
│  │   │   (renderiza aquí)      │   │    │
│  │   └─────────────────────────┘   │    │
│  └─────────────────────────────────┘    │
│                  ↓                      │
│         Screenshots/Output              │
│              (volumen)                  │
└─────────────────────────────────────────┘
```

## Comandos Principales

### Construir la Imagen

```bash
cd ~/Desarrollo/AI/browser-automation-stealth
docker build -t browser-stealth .
```

### Ejecutar Test Rápido

```bash
docker-compose run test
```

Resultado esperado:
```
Test OK: Example Domain
```

### Sesión Interactiva

```bash
docker run -it --rm browser-stealth bash
```

Dentro del contenedor:
```bash
python3 src/python/test_parallel.py
```

### Ejecutar Script Específico

```bash
docker run -it --rm browser-stealth python3 src/python/demo_mercadolibre.py
```

### Obtener Screenshots

Los screenshots se guardan en el volumen `./output`:

```bash
docker run -it --rm \
  -v $(pwd)/output:/home/browser/app/output \
  browser-stealth \
  python3 -c "
from camoufox.sync_api import Camoufox
with Camoufox(headless='virtual', i_know_what_im_doing=True) as b:
    p = b.new_page()
    p.goto('https://google.com')
    p.screenshot(path='output/google.png')
    print('Screenshot guardado en output/google.png')
"
```

## Casos de Uso Principales

### 1. Servidor Linux sin GUI (VPS/Cloud)

```bash
# En el servidor
git clone <tu-repo>
cd browser-automation-stealth
docker build -t browser-stealth .

# Ejecutar scraping
docker run --rm \
  -v $(pwd)/output:/home/browser/app/output \
  browser-stealth \
  python3 tu_script.py
```

### 2. CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/scrape.yml
name: Browser Automation
on:
  schedule:
    - cron: '0 8 * * *'  # Diario a las 8am

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t browser-stealth .

      - name: Run automation
        run: |
          docker run --rm \
            -v ${{ github.workspace }}/output:/home/browser/app/output \
            browser-stealth \
            python3 src/python/tu_script.py

      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: screenshots
          path: output/
```

### 3. Kubernetes / Docker Swarm

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: browser-automation
spec:
  replicas: 3  # 3 instancias paralelas
  selector:
    matchLabels:
      app: browser-automation
  template:
    metadata:
      labels:
        app: browser-automation
    spec:
      containers:
      - name: browser
        image: browser-stealth:latest
        resources:
          limits:
            memory: "2Gi"
            cpu: "1"
        env:
        - name: CAMOUFOX_HEADLESS
          value: "virtual"
```

### 4. Múltiples Instancias Paralelas

```bash
# Ejecutar 5 contenedores en paralelo
for i in {1..5}; do
  docker run -d --rm \
    --name browser-$i \
    -v $(pwd)/output:/home/browser/app/output \
    browser-stealth \
    python3 -c "
from camoufox.sync_api import Camoufox
with Camoufox(headless='virtual', i_know_what_im_doing=True) as b:
    p = b.new_page()
    p.goto('https://example.com')
    p.screenshot(path='output/instance-$i.png')
"
done

# Ver estado
docker ps

# Ver logs
docker logs browser-1
```

### 5. Desarrollo Local con Hot Reload

```bash
# Montar código local para editar sin rebuild
docker run -it --rm \
  -v $(pwd)/src:/home/browser/app/src \
  -v $(pwd)/output:/home/browser/app/output \
  browser-stealth \
  bash

# Dentro del contenedor, edita src/ en tu PC y ejecuta aquí
```

## Variables de Entorno

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `CAMOUFOX_HEADLESS` | `virtual` | Usa Xvfb (recomendado) |
| `CAMOUFOX_HEADLESS` | `true` | Headless puro (más detectable) |
| `DISPLAY` | `:99` | Display de Xvfb |

## Límites de Recursos

El `docker-compose.yml` configura:
- **Memoria máxima**: 2GB
- **Memoria reservada**: 512MB

Ajustar según necesidad:

```yaml
deploy:
  resources:
    limits:
      memory: 4G  # Más RAM para más tabs
    reservations:
      memory: 1G
```

## Troubleshooting

### Error: "cannot open display"

```bash
# Verificar que Xvfb esté corriendo
docker exec -it <container> ps aux | grep Xvfb

# Si no está, el script debe iniciarlo
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
```

### Error: "out of memory"

```bash
# Aumentar límite de memoria
docker run --memory=4g browser-stealth ...
```

### Contenedor se cierra inmediatamente

```bash
# Ejecutar interactivo para debug
docker run -it --rm browser-stealth bash
# Luego ejecutar comandos manualmente
```

### Screenshots en negro

```bash
# Esperar a que la página cargue
page.wait_for_load_state('networkidle')
page.screenshot(path='output/test.png')
```

## Comparación: Docker vs Local

| Aspecto | Docker | Local |
|---------|--------|-------|
| Setup inicial | `docker build` (5-10 min) | Instalar dependencias (10-20 min) |
| Reproducibilidad | 100% garantizada | Depende del sistema |
| Aislamiento | Completo | Comparte sistema |
| Rendimiento | ~5-10% overhead | Nativo |
| Uso de disco | ~1.5GB por imagen | ~500MB |
| Ideal para | Servers, CI/CD, cloud | Desarrollo, PC personal |

## Integración con Claude Code (Futuro)

Cuando uses Docker desde Claude Code:

```bash
# Claude Code puede ejecutar
docker run --rm -v $(pwd)/output:/home/browser/app/output browser-stealth python3 -c "
from camoufox.sync_api import Camoufox
with Camoufox(headless='virtual', i_know_what_im_doing=True) as b:
    p = b.new_page()
    p.goto('$URL')
    content = p.content()
    print(content)
"
```

Esto permite automatización en cualquier entorno sin depender de la configuración local.
