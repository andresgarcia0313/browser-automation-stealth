# Browser Automation Stealth - Docker Image
# ==========================================
#
# Build:   docker build -t browser-stealth .
# Run:     docker run -it --rm browser-stealth python3 examples/uso_basico.py
#
# Para modo visible (requiere X11):
#   docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix browser-stealth

FROM python:3.11-slim

LABEL maintainer="andres"
LABEL description="Browser Automation con Camoufox anti-detección"

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Firefox/Camoufox dependencies
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libxt6 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxcursor1 \
    libxi6 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxshmfence1 \
    libgbm1 \
    # Virtual display
    xvfb \
    # Fonts
    fonts-liberation \
    fonts-noto-color-emoji \
    # Utilities
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN useradd -m -s /bin/bash browser
WORKDIR /home/browser/app

# Copiar requirements e instalar Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Descargar navegador Camoufox
RUN python3 -m camoufox fetch

# Copiar código fuente
COPY src/python/ ./src/python/
COPY examples/ ./examples/
COPY docs/ ./docs/

# Cambiar ownership
RUN chown -R browser:browser /home/browser

# Cambiar a usuario no-root
USER browser

# Variables de entorno para Camoufox
ENV HOME=/home/browser
ENV CAMOUFOX_HEADLESS=virtual

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "from camoufox.sync_api import Camoufox; print('OK')"

# Comando por defecto
CMD ["python3", "-c", "print('Browser Automation Stealth - Ready'); print('Usar: python3 src/python/camoufox_browser.py')"]
