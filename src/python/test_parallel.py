#!/usr/bin/env python3
"""
Test: 3 instancias paralelas en modo background (v2 con mejor error handling)
"""

import asyncio
import os
import traceback
from datetime import datetime
from camoufox.async_api import AsyncCamoufox

SCREENSHOTS_DIR = "/tmp/browser_parallel_test"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Limpiar directorio
for item in os.listdir(SCREENSHOTS_DIR):
    path = os.path.join(SCREENSHOTS_DIR, item)
    if os.path.isdir(path):
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
        os.rmdir(path)


async def screenshot(page, instance_name: str, step: int, description: str):
    """Toma screenshot con nombre descriptivo"""
    filename = f"{instance_name}/{step:02d}_{description}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    await page.screenshot(path=filepath)
    print(f"    [{instance_name}] Captura: {step:02d}_{description}.png")
    return filepath


async def tarea_google_search():
    """Instancia 1: Buscar en Google"""
    name = "01_google_search"
    print(f"\n[{name}] Iniciando...")

    try:
        async with AsyncCamoufox(headless="virtual", humanize=True, i_know_what_im_doing=True) as browser:
            page = await browser.new_page()
            page.set_default_timeout(30000)

            # Paso 1: Ir a Google
            print(f"  [{name}] Navegando a Google...")
            await page.goto("https://www.google.com", wait_until="domcontentloaded")
            await asyncio.sleep(2)
            await screenshot(page, name, 1, "google_inicio")

            # Paso 2: Click en buscador
            print(f"  [{name}] Haciendo click en buscador...")
            await page.click('textarea[name="q"], input[name="q"]')
            await asyncio.sleep(0.5)
            await screenshot(page, name, 2, "click_buscador")

            # Paso 3: Escribir busqueda
            print(f"  [{name}] Escribiendo busqueda...")
            await page.fill('textarea[name="q"], input[name="q"]', "Claude AI Anthropic")
            await asyncio.sleep(1)
            await screenshot(page, name, 3, "texto_escrito")

            # Paso 4: Enter y resultados
            print(f"  [{name}] Presionando Enter...")
            await page.press('textarea[name="q"], input[name="q"]', "Enter")
            await asyncio.sleep(3)
            await screenshot(page, name, 4, "resultados")

            # Paso 5: Scroll
            print(f"  [{name}] Haciendo scroll...")
            await page.evaluate("window.scrollTo(0, 500)")
            await asyncio.sleep(1)
            await screenshot(page, name, 5, "scroll_resultados")

            print(f"[{name}] COMPLETADO!")
            return name

    except Exception as e:
        print(f"[{name}] ERROR: {e}")
        traceback.print_exc()
        return None


async def tarea_wikipedia_navegacion():
    """Instancia 2: Navegar Wikipedia"""
    name = "02_wikipedia_nav"
    print(f"\n[{name}] Iniciando...")

    try:
        async with AsyncCamoufox(headless="virtual", humanize=True, i_know_what_im_doing=True) as browser:
            page = await browser.new_page()
            page.set_default_timeout(30000)

            # Paso 1: Wikipedia
            print(f"  [{name}] Navegando a Wikipedia...")
            await page.goto("https://es.wikipedia.org", wait_until="domcontentloaded")
            await asyncio.sleep(2)
            await screenshot(page, name, 1, "wikipedia_inicio")

            # Paso 2: Click buscador
            print(f"  [{name}] Click en buscador...")
            await page.click('#searchInput')
            await asyncio.sleep(0.5)
            await screenshot(page, name, 2, "click_buscador")

            # Paso 3: Escribir
            print(f"  [{name}] Escribiendo busqueda...")
            await page.fill('#searchInput', "Inteligencia artificial")
            await asyncio.sleep(1)
            await screenshot(page, name, 3, "texto_busqueda")

            # Paso 4: Buscar
            print(f"  [{name}] Presionando Enter...")
            await page.press('#searchInput', "Enter")
            await asyncio.sleep(3)
            await screenshot(page, name, 4, "articulo_ia")

            # Paso 5: Scroll
            print(f"  [{name}] Haciendo scroll...")
            await page.evaluate("window.scrollTo(0, 600)")
            await asyncio.sleep(1)
            await screenshot(page, name, 5, "scroll_contenido")

            # Paso 6: Click en enlace
            print(f"  [{name}] Buscando enlace relacionado...")
            try:
                await page.click('a[href*="/wiki/Aprendizaje_autom"]', timeout=5000)
                await asyncio.sleep(3)
                await screenshot(page, name, 6, "articulo_ml")
            except:
                await screenshot(page, name, 6, "sin_enlace_ml")

            print(f"[{name}] COMPLETADO!")
            return name

    except Exception as e:
        print(f"[{name}] ERROR: {e}")
        traceback.print_exc()
        return None


async def tarea_github_exploracion():
    """Instancia 3: Explorar GitHub"""
    name = "03_github_explore"
    print(f"\n[{name}] Iniciando...")

    try:
        async with AsyncCamoufox(headless="virtual", humanize=True, i_know_what_im_doing=True) as browser:
            page = await browser.new_page()
            page.set_default_timeout(30000)

            # Paso 1: GitHub Explore
            print(f"  [{name}] Navegando a GitHub Explore...")
            await page.goto("https://github.com/explore", wait_until="domcontentloaded")
            await asyncio.sleep(3)
            await screenshot(page, name, 1, "github_explore")

            # Paso 2: Scroll
            print(f"  [{name}] Haciendo scroll...")
            await page.evaluate("window.scrollTo(0, 400)")
            await asyncio.sleep(1)
            await screenshot(page, name, 2, "scroll_explore")

            # Paso 3: Ir a Trending
            print(f"  [{name}] Navegando a Trending...")
            await page.goto("https://github.com/trending", wait_until="domcontentloaded")
            await asyncio.sleep(3)
            await screenshot(page, name, 3, "github_trending")

            # Paso 4: Scroll en trending
            print(f"  [{name}] Scroll en trending...")
            await page.evaluate("window.scrollTo(0, 500)")
            await asyncio.sleep(1)
            await screenshot(page, name, 4, "trending_scroll")

            # Paso 5: Click en repo
            print(f"  [{name}] Intentando click en repositorio...")
            try:
                await page.click('article h2 a', timeout=5000)
                await asyncio.sleep(3)
                await screenshot(page, name, 5, "repo_detalle")
            except:
                await screenshot(page, name, 5, "lista_repos")

            print(f"[{name}] COMPLETADO!")
            return name

    except Exception as e:
        print(f"[{name}] ERROR: {e}")
        traceback.print_exc()
        return None


async def main():
    print("="*70)
    print("TEST: 3 Instancias Paralelas en Modo Background (v2)")
    print("="*70)
    print(f"\nCarpeta de capturas: {SCREENSHOTS_DIR}")
    print("Las 3 instancias correran EN PARALELO (no secuencial)")
    print("-"*70)

    start_time = datetime.now()

    # Ejecutar las 3 tareas en paralelo
    print("\n[INICIO] Lanzando 3 navegadores en paralelo...")
    results = await asyncio.gather(
        tarea_google_search(),
        tarea_wikipedia_navegacion(),
        tarea_github_exploracion(),
        return_exceptions=True
    )

    elapsed = (datetime.now() - start_time).total_seconds()

    # Mostrar resultados
    print(f"\n{'='*70}")
    print("CAPTURAS TOMADAS:")
    print("-"*70)

    total_screenshots = 0
    for task_dir in sorted(os.listdir(SCREENSHOTS_DIR)):
        task_path = os.path.join(SCREENSHOTS_DIR, task_dir)
        if os.path.isdir(task_path):
            files = sorted([f for f in os.listdir(task_path) if f.endswith('.png')])
            total_screenshots += len(files)
            print(f"\n{task_dir}/ ({len(files)} capturas)")
            for f in files:
                print(f"  {f}")

    print(f"\n{'='*70}")
    print("TEST COMPLETADO")
    print("="*70)
    print(f"Tiempo total: {elapsed:.1f} segundos")
    print(f"Instancias paralelas: 3")
    print(f"Total screenshots: {total_screenshots}")
    print(f"Carpeta: {SCREENSHOTS_DIR}")
    print(f"\n*** NINGUNA VENTANA FUE VISIBLE ***")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
