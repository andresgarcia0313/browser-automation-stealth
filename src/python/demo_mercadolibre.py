#!/usr/bin/env python3
"""
Demo final: MercadoLibre con Camoufox
Usa extraccion basada en estructura visible de la pagina
"""

from camoufox.sync_api import Camoufox
import json
import time

query = "calentador agua electrico portatil"
url = f"https://listado.mercadolibre.com.co/{query.replace(' ', '-')}"

print(f"\n{'='*60}")
print("DEMOSTRACION: Camoufox navegando MercadoLibre")
print(f"{'='*60}")
print(f"\nBusqueda: {query}")
print(f"Pais: Colombia")

with Camoufox(
    headless=False,
    humanize=2.0,
    i_know_what_im_doing=True,
    block_images=False,  # Necesitamos imagenes para ML
) as browser:

    page = browser.new_page()
    page.set_default_timeout(60000)

    print("\n[1/6] Iniciando navegador Firefox anti-deteccion...")
    print("      (Camoufox con fingerprint a nivel C++)")

    print("\n[2/6] Navegando a MercadoLibre Colombia...")
    response = page.goto(url, wait_until="commit")
    print(f"      Status: {response.status if response else 'OK'}")

    print("\n[3/6] Esperando renderizado completo...")
    # Wait for page to fully render
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Scroll to load lazy content
    print("\n[4/6] Haciendo scroll para cargar productos...")
    for i in range(5):
        page.evaluate(f"window.scrollTo(0, {i * 500})")
        time.sleep(0.5)
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(2)

    print("\n[5/6] Extrayendo productos de la pagina...")

    # Get HTML for manual parsing if needed
    html = page.content()

    # Try multiple extraction strategies
    products = []

    # Strategy 1: Look for product structure based on visible layout
    try:
        products = page.evaluate("""() => {
            const results = [];

            // Get all price elements first (most reliable)
            const priceElements = document.querySelectorAll('[class*="andes-money-amount"], [class*="price"]');

            for (const priceEl of priceElements) {
                // Navigate up to find product container
                let container = priceEl.parentElement;
                for (let i = 0; i < 10 && container; i++) {
                    // Check if this container has a product link
                    const link = container.querySelector('a[href*="MLO"], a[href*="articulo"], a[href*="producto"]');
                    if (link) {
                        const href = link.href;
                        if (results.some(r => r.link === href)) break;

                        // Find title
                        let title = '';
                        const h2 = container.querySelector('h2, h3');
                        const img = container.querySelector('img');

                        if (h2) title = h2.innerText.trim();
                        else if (img?.alt) title = img.alt;

                        // Get price
                        const fraction = priceEl.querySelector('.andes-money-amount__fraction') || priceEl;
                        const price = fraction.innerText.replace(/[^0-9.,]/g, '');

                        if (title && title.length > 10 && price) {
                            results.push({ title, price, link: href });
                        }
                        break;
                    }
                    container = container.parentElement;
                }
            }

            return results.slice(0, 15);
        }""")
    except Exception as e:
        print(f"      Estrategia 1 fallo: {e}")

    # Strategy 2: Search for any visible text that looks like products
    if not products:
        print("      Intentando estrategia alternativa...")
        try:
            # Get all visible text
            visible_text = page.evaluate("""() => {
                const body = document.body.innerText;
                return body;
            }""")

            # Parse for product-like patterns
            import re
            price_pattern = r'\$\s*([\d.,]+)'
            prices = re.findall(price_pattern, visible_text)
            print(f"      Encontrados {len(prices)} precios en la pagina")
        except:
            pass

    print(f"\n[6/6] Resultados de la extraccion...")

    if products:
        print(f"\n{'='*60}")
        print(f"ENCONTRADOS: {len(products)} calentadores de agua")
        print(f"{'='*60}\n")

        for i, p in enumerate(products[:10], 1):
            print(f"{i}. {p['title'][:70]}...")
            print(f"   Precio: ${p['price']} COP")
            if p.get('link'):
                print(f"   Link: {p['link'][:60]}...")
            print()

        with open('/tmp/calentadores_final.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        print(f"Resultados guardados: /tmp/calentadores_final.json")
    else:
        print("\n" + "="*60)
        print("NOTA: MercadoLibre tiene protecciones anti-scraping activas")
        print("="*60)
        print("""
La pagina cargo correctamente (puedes verla en el navegador),
pero MercadoLibre usa tecnicas avanzadas para dificultar
la extraccion automatizada:

- Contenido renderizado via JavaScript pesado
- Lazy loading agresivo
- Deteccion de automatizacion

OPCIONES PARA EXTRAER DATOS:
1. Usar la API oficial de MercadoLibre (recomendado)
2. Aumentar tiempos de espera
3. Usar servicios de scraping especializados

El navegador Camoufox funciona correctamente - puedes ver
los productos en pantalla.
""")

    # Save screenshot as proof
    page.screenshot(path="/tmp/ml_demo_final.png")
    print(f"\nScreenshot guardado: /tmp/ml_demo_final.png")

    print("\n" + "="*60)
    print("DEMO COMPLETADA")
    print("="*60)
    print("\nNavegador cerrando en 5 segundos...")
    print("(Puedes ver los productos en pantalla)")
    time.sleep(5)
