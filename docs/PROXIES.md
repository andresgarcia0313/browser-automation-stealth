# Guía de Uso con Proxies

Para uso intensivo o cuando tu IP está bloqueada, necesitas proxies. Esta guía explica cómo configurarlos.

## Tipos de Proxies

| Tipo | Detección | Costo | Uso |
|------|-----------|-------|-----|
| **Residenciales** | Muy baja | $$$$ | Producción, scraping serio |
| **Datacenter** | Media-Alta | $ | Testing, desarrollo |
| **ISP/Static** | Baja | $$$ | Balance costo/calidad |
| **Mobile** | Muy baja | $$$$$ | Máxima evasión |

**Recomendación:** Para anti-detección real, usar **proxies residenciales**.

## Proveedores Recomendados

| Proveedor | Tipo | Precio aprox. | Notas |
|-----------|------|---------------|-------|
| **Bright Data** | Residencial | $15/GB | El más grande, buena calidad |
| **Oxylabs** | Residencial | $15/GB | Muy estable |
| **Smartproxy** | Residencial | $12/GB | Buena relación precio/calidad |
| **IPRoyal** | Residencial | $7/GB | Económico |
| **Webshare** | Datacenter | $0.05/proxy | Para desarrollo |

## Configuración con Camoufox

### Proxy Simple (HTTP/HTTPS)

```python
from camoufox.sync_api import Camoufox

proxy_config = {
    "server": "http://proxy.ejemplo.com:8080",
    "username": "usuario",
    "password": "contraseña"
}

with Camoufox(
    headless="virtual",
    humanize=True,
    proxy=proxy_config,
    i_know_what_im_doing=True
) as browser:
    page = browser.new_page()
    page.goto("https://httpbin.org/ip")
    print(page.content())  # Verifica que muestra IP del proxy
```

### Proxy SOCKS5

```python
from camoufox.sync_api import Camoufox

proxy_config = {
    "server": "socks5://proxy.ejemplo.com:1080",
    "username": "usuario",
    "password": "contraseña"
}

with Camoufox(
    headless="virtual",
    proxy=proxy_config,
    i_know_what_im_doing=True
) as browser:
    page = browser.new_page()
    page.goto("https://whatismyipaddress.com")
```

### Rotación de Proxies

```python
from camoufox.sync_api import Camoufox
import random

# Lista de proxies
proxies = [
    {"server": "http://proxy1.com:8080", "username": "u1", "password": "p1"},
    {"server": "http://proxy2.com:8080", "username": "u2", "password": "p2"},
    {"server": "http://proxy3.com:8080", "username": "u3", "password": "p3"},
]

def get_random_proxy():
    return random.choice(proxies)

# Usar proxy diferente por sesión
for i in range(3):
    proxy = get_random_proxy()
    with Camoufox(headless="virtual", proxy=proxy, i_know_what_im_doing=True) as browser:
        page = browser.new_page()
        page.goto("https://httpbin.org/ip")
        ip = page.inner_text("body")
        print(f"Sesión {i+1}: {ip}")
```

### Proxy Residencial con Bright Data

```python
from camoufox.sync_api import Camoufox

# Formato Bright Data
# Usuario: lum-customer-CLIENTE-zone-ZONA
# Host: brd.superproxy.io:22225

proxy_config = {
    "server": "http://brd.superproxy.io:22225",
    "username": "lum-customer-TUCLIENTE-zone-residential",
    "password": "TU_PASSWORD"
}

# Para país específico, agregar al username: -country-co (Colombia)
proxy_config_colombia = {
    "server": "http://brd.superproxy.io:22225",
    "username": "lum-customer-TUCLIENTE-zone-residential-country-co",
    "password": "TU_PASSWORD"
}

with Camoufox(headless="virtual", proxy=proxy_config_colombia, i_know_what_im_doing=True) as browser:
    page = browser.new_page()
    page.goto("https://www.mercadolibre.com.co")
    # Ahora navega desde IP colombiana
```

## Configuración con Hero

### Proxy Básico

```javascript
import Hero from '@ulixee/hero-playground';

const hero = new Hero({
    showChrome: false,
    upstreamProxyUrl: 'http://usuario:password@proxy.com:8080'
});

await hero.goto('https://httpbin.org/ip');
console.log(await hero.document.body.innerText);
await hero.close();
```

### Proxy con Autenticación

```javascript
import Hero from '@ulixee/hero-playground';

const hero = new Hero({
    showChrome: false,
    upstreamProxyUrl: 'http://proxy.ejemplo.com:8080',
    upstreamProxyCredentials: {
        username: 'usuario',
        password: 'contraseña'
    }
});
```

## Verificación de Proxy

### Script de Verificación

```python
#!/usr/bin/env python3
"""Verificar que el proxy funciona correctamente"""

from camoufox.sync_api import Camoufox
import json

def verificar_proxy(proxy_config):
    print(f"Probando proxy: {proxy_config['server']}")

    try:
        with Camoufox(
            headless="virtual",
            proxy=proxy_config,
            i_know_what_im_doing=True
        ) as browser:
            page = browser.new_page()
            page.set_default_timeout(30000)

            # Verificar IP
            page.goto("https://httpbin.org/ip")
            ip_data = json.loads(page.inner_text("body"))
            print(f"  IP detectada: {ip_data['origin']}")

            # Verificar geolocalización
            page.goto("https://ipapi.co/json/")
            geo_data = json.loads(page.inner_text("body"))
            print(f"  País: {geo_data.get('country_name', 'Desconocido')}")
            print(f"  Ciudad: {geo_data.get('city', 'Desconocida')}")

            return True

    except Exception as e:
        print(f"  ERROR: {e}")
        return False

# Uso
proxy = {
    "server": "http://tu-proxy.com:8080",
    "username": "usuario",
    "password": "password"
}

verificar_proxy(proxy)
```

## Mejores Prácticas

### 1. Rotación Inteligente

```python
import random
import time

class ProxyRotator:
    def __init__(self, proxies):
        self.proxies = proxies
        self.current_index = 0
        self.failed_proxies = set()

    def get_next(self):
        """Obtener siguiente proxy disponible"""
        available = [p for i, p in enumerate(self.proxies)
                     if i not in self.failed_proxies]
        if not available:
            self.failed_proxies.clear()  # Reset si todos fallaron
            available = self.proxies
        return random.choice(available)

    def mark_failed(self, proxy):
        """Marcar proxy como fallido"""
        idx = self.proxies.index(proxy)
        self.failed_proxies.add(idx)
```

### 2. Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_minute):
    """Decorador para limitar llamadas"""
    min_interval = 60.0 / calls_per_minute
    last_call = [0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(30)  # 30 llamadas por minuto máximo
def scrape_page(url, proxy):
    with Camoufox(headless="virtual", proxy=proxy, i_know_what_im_doing=True) as browser:
        page = browser.new_page()
        page.goto(url)
        return page.content()
```

### 3. Manejo de Errores de Proxy

```python
from camoufox.sync_api import Camoufox
import time

def navigate_with_retry(url, proxies, max_retries=3):
    """Navegar con reintentos y rotación de proxy"""
    for attempt in range(max_retries):
        proxy = proxies[attempt % len(proxies)]
        try:
            with Camoufox(
                headless="virtual",
                proxy=proxy,
                i_know_what_im_doing=True
            ) as browser:
                page = browser.new_page()
                page.set_default_timeout(30000)
                page.goto(url)
                return page.content()

        except Exception as e:
            print(f"Intento {attempt + 1} falló: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Backoff exponencial

    raise Exception(f"Falló después de {max_retries} intentos")
```

## Costos Estimados

| Escenario | Requests/día | GB/mes | Costo/mes |
|-----------|--------------|--------|-----------|
| Desarrollo | 100 | <1 GB | ~$10 |
| Producción ligera | 1,000 | ~5 GB | ~$60 |
| Producción media | 10,000 | ~20 GB | ~$200 |
| Producción alta | 100,000+ | ~100 GB | ~$1,000+ |

## Alternativas Gratuitas (Solo Testing)

⚠️ **No usar en producción** - Son lentos, inestables y fácilmente detectables.

```python
# Proxies gratuitos (solo para testing)
free_proxies = [
    "http://free-proxy.com:8080",  # Ejemplo, buscar en free-proxy-list.net
]

# Tor (lento pero funciona)
tor_proxy = {
    "server": "socks5://127.0.0.1:9050"
}
# Requiere instalar Tor: sudo apt install tor && sudo systemctl start tor
```

## Checklist Anti-Detección con Proxies

- [ ] Usar proxies residenciales (no datacenter)
- [ ] Rotar IPs regularmente
- [ ] Usar IP del mismo país que el sitio objetivo
- [ ] No hacer más de 1 request/segundo por IP
- [ ] Variar User-Agent junto con IP
- [ ] Implementar delays aleatorios entre requests
- [ ] Manejar CAPTCHAs y bloqueos gracefully

---

*Documentación creada: 2025-12-30*
