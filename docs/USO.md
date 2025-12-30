# Guía de Uso

Ejemplos prácticos de uso de Camoufox y Hero para diferentes casos.

## Camoufox (Python)

### Navegación Simple

```python
from camoufox.sync_api import Camoufox

# Modo visible (ves el navegador)
with Camoufox(headless=False, humanize=True, i_know_what_im_doing=True) as browser:
    page = browser.new_page()
    page.goto("https://www.google.com")
    print(f"Título: {page.title()}")
```

### Modo Background (Invisible)

```python
from camoufox.sync_api import Camoufox

# headless="virtual" usa display virtual (mejor que headless=True)
with Camoufox(headless="virtual", humanize=True, i_know_what_im_doing=True) as browser:
    page = browser.new_page()
    page.goto("https://www.google.com")
    page.screenshot(path="screenshot.png")
    print("Captura tomada sin mostrar navegador")
```

### Búsqueda en Google

```python
from camoufox.sync_api import Camoufox
import time

with Camoufox(headless=False, humanize=True, i_know_what_im_doing=True) as browser:
    page = browser.new_page()

    # Ir a Google
    page.goto("https://www.google.com", wait_until="domcontentloaded")
    time.sleep(2)

    # Escribir en el buscador
    page.fill('textarea[name="q"]', "Python tutorial 2025")
    time.sleep(1)

    # Presionar Enter
    page.press('textarea[name="q"]', "Enter")
    time.sleep(3)

    # Tomar screenshot de resultados
    page.screenshot(path="google_results.png")
    print(f"Resultados guardados")
```

### Extracción de Datos

```python
from camoufox.sync_api import Camoufox

with Camoufox(headless="virtual", humanize=True, i_know_what_im_doing=True) as browser:
    page = browser.new_page()
    page.goto("https://news.ycombinator.com")

    # Extraer títulos usando JavaScript
    titles = page.evaluate("""() => {
        const items = document.querySelectorAll('.titleline a');
        return Array.from(items).map(a => ({
            title: a.innerText,
            url: a.href
        })).slice(0, 10);
    }""")

    for i, item in enumerate(titles, 1):
        print(f"{i}. {item['title']}")
```

### Múltiples Instancias Paralelas (Async)

```python
import asyncio
from camoufox.async_api import AsyncCamoufox

async def scrape_url(url):
    async with AsyncCamoufox(headless="virtual", humanize=True, i_know_what_im_doing=True) as browser:
        page = await browser.new_page()
        await page.goto(url)
        title = await page.title()
        return {"url": url, "title": title}

async def main():
    urls = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.wikipedia.org"
    ]

    # Ejecutar en paralelo
    results = await asyncio.gather(*[scrape_url(url) for url in urls])

    for r in results:
        print(f"{r['url']}: {r['title']}")

asyncio.run(main())
```

### Login en un Sitio

```python
from camoufox.sync_api import Camoufox
import time

with Camoufox(headless=False, humanize=True, i_know_what_im_doing=True) as browser:
    page = browser.new_page()

    # Ir a página de login
    page.goto("https://ejemplo.com/login")
    time.sleep(2)

    # Llenar formulario
    page.fill('input[name="email"]', "mi@email.com")
    time.sleep(0.5)
    page.fill('input[name="password"]', "mipassword")
    time.sleep(0.5)

    # Click en botón de login
    page.click('button[type="submit"]')
    time.sleep(3)

    # Verificar login exitoso
    if "dashboard" in page.url:
        print("Login exitoso!")
    else:
        print("Login fallido")
```

---

## Ulixee Hero (Node.js)

### Navegación Simple

```javascript
import Hero from '@ulixee/hero-playground';

const hero = new Hero({ showChrome: true });

await hero.goto('https://www.google.com');
console.log('Título:', await hero.document.title);

await hero.close();
```

### Modo Background

```javascript
import Hero from '@ulixee/hero-playground';

const hero = new Hero({ showChrome: false });

await hero.goto('https://www.google.com');
const screenshot = await hero.takeScreenshot();

// Guardar screenshot
import * as fs from 'fs';
fs.writeFileSync('screenshot.png', screenshot);

await hero.close();
```

### Interacción con Formularios

```javascript
import Hero from '@ulixee/hero-playground';

const hero = new Hero({ showChrome: true });

await hero.goto('https://www.google.com');
await hero.waitForPaintingStable();

// Hero simula typing humano automáticamente
await hero.type('mi búsqueda');
await hero.waitForMillis(1000);

// Click en botón
const searchButton = await hero.document.querySelector('input[name="btnK"]');
await hero.click(searchButton);

await hero.waitForPaintingStable();
console.log('URL actual:', await hero.url);

await hero.close();
```

### Extracción de Datos

```javascript
import Hero from '@ulixee/hero-playground';

const hero = new Hero({ showChrome: false });

await hero.goto('https://news.ycombinator.com');
await hero.waitForPaintingStable();

// Extraer títulos
const titles = await hero.document.querySelectorAll('.titleline a');
const results = [];

for (const title of titles) {
    const text = await title.innerText;
    const href = await title.href;
    results.push({ text, href });
    if (results.length >= 10) break;
}

results.forEach((r, i) => console.log(`${i+1}. ${r.text}`));

await hero.close();
```

---

## Casos de Uso Comunes

### Buscar Productos en E-commerce

```python
from camoufox.sync_api import Camoufox
import time
import json

def buscar_productos(query, sitio="mercadolibre.com.co"):
    url = f"https://listado.{sitio}/{query.replace(' ', '-')}"

    with Camoufox(headless="virtual", humanize=True, i_know_what_im_doing=True) as browser:
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        time.sleep(3)

        # Scroll para cargar productos
        for i in range(3):
            page.evaluate(f"window.scrollTo(0, {i * 500})")
            time.sleep(0.5)

        # Extraer productos
        productos = page.evaluate("""() => {
            const items = document.querySelectorAll('[class*="ui-search-result"]');
            return Array.from(items).slice(0, 10).map(item => {
                const title = item.querySelector('h2, [class*="title"]');
                const price = item.querySelector('[class*="price"], .andes-money-amount__fraction');
                const link = item.querySelector('a');
                return {
                    titulo: title ? title.innerText : '',
                    precio: price ? price.innerText : '',
                    url: link ? link.href : ''
                };
            }).filter(p => p.titulo);
        }""")

        return productos

# Uso
productos = buscar_productos("laptop gaming")
print(json.dumps(productos, indent=2, ensure_ascii=False))
```

### Monitoreo de Precios

```python
from camoufox.sync_api import Camoufox
import time
import json
from datetime import datetime

def obtener_precio(url):
    with Camoufox(headless="virtual", humanize=True, i_know_what_im_doing=True) as browser:
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        time.sleep(3)

        precio = page.evaluate("""() => {
            const el = document.querySelector('[class*="price"], .andes-money-amount__fraction, [itemprop="price"]');
            return el ? el.innerText : null;
        }""")

        return {
            "url": url,
            "precio": precio,
            "fecha": datetime.now().isoformat()
        }

# Uso
resultado = obtener_precio("https://articulo.mercadolibre.com.co/MCO-123456")
print(json.dumps(resultado, indent=2))
```

### Llenar Formularios Automáticamente

```python
from camoufox.sync_api import Camoufox
import time

def llenar_formulario(url, datos):
    with Camoufox(headless=False, humanize=True, i_know_what_im_doing=True) as browser:
        page = browser.new_page()
        page.goto(url)
        time.sleep(2)

        for selector, valor in datos.items():
            try:
                page.fill(selector, valor)
                time.sleep(0.3)  # Pausa natural entre campos
            except:
                print(f"Campo no encontrado: {selector}")

        # Screenshot antes de enviar
        page.screenshot(path="formulario_llenado.png")

        return True

# Uso
datos = {
    'input[name="nombre"]': "Juan Pérez",
    'input[name="email"]': "juan@ejemplo.com",
    'input[name="telefono"]': "3001234567",
    'textarea[name="mensaje"]': "Este es mi mensaje"
}

llenar_formulario("https://ejemplo.com/contacto", datos)
```

---

## Tips de Uso

### Evitar Detección

1. **Usar `humanize=True`** - Movimientos de cursor naturales
2. **Agregar delays** - No hacer acciones instantáneas
3. **Modo `headless="virtual"`** - Mejor que `headless=True`
4. **Scroll gradual** - No saltar a elementos directamente
5. **Variar tiempos** - No usar delays fijos

### Mejorar Rendimiento

1. **Reusar contextos** - No crear navegador por cada request
2. **Desactivar imágenes** - Si no las necesitas
3. **Limitar JavaScript** - Usar `wait_until="domcontentloaded"` en vez de `networkidle`

### Debugging

1. **Usar `headless=False`** primero - Ver qué hace el script
2. **Screenshots en cada paso** - Para identificar fallos
3. **Console logs** - `page.on("console", lambda msg: print(msg.text))`

---

*Guía creada: 2025-12-30*
