#!/usr/bin/env python3
"""
Ejemplos básicos de uso de Camoufox
===================================

Ejecutar con: python3 uso_basico.py
"""

from camoufox.sync_api import Camoufox
import time


def ejemplo_navegacion_simple():
    """Ejemplo 1: Navegación simple visible"""
    print("\n" + "="*50)
    print("Ejemplo 1: Navegación Simple (Visible)")
    print("="*50)

    with Camoufox(headless=False, humanize=True, i_know_what_im_doing=True) as browser:
        page = browser.new_page()

        print("Navegando a Google...")
        page.goto("https://www.google.com")
        time.sleep(2)

        print(f"Título: {page.title()}")
        print("Cerrando en 3 segundos...")
        time.sleep(3)


def ejemplo_background():
    """Ejemplo 2: Modo background (invisible)"""
    print("\n" + "="*50)
    print("Ejemplo 2: Modo Background (Invisible)")
    print("="*50)

    with Camoufox(headless="virtual", humanize=True, i_know_what_im_doing=True) as browser:
        page = browser.new_page()

        print("Navegando a Wikipedia (invisible)...")
        page.goto("https://es.wikipedia.org")
        time.sleep(2)

        title = page.title()
        print(f"Título: {title}")

        page.screenshot(path="/tmp/ejemplo_background.png")
        print("Screenshot guardado: /tmp/ejemplo_background.png")


def ejemplo_busqueda():
    """Ejemplo 3: Búsqueda en Google"""
    print("\n" + "="*50)
    print("Ejemplo 3: Búsqueda en Google")
    print("="*50)

    with Camoufox(headless=False, humanize=True, i_know_what_im_doing=True) as browser:
        page = browser.new_page()

        print("Navegando a Google...")
        page.goto("https://www.google.com", wait_until="domcontentloaded")
        time.sleep(2)

        print("Escribiendo búsqueda...")
        page.fill('textarea[name="q"]', "Camoufox browser automation")
        time.sleep(1)

        print("Presionando Enter...")
        page.press('textarea[name="q"]', "Enter")
        time.sleep(3)

        print(f"URL actual: {page.url}")
        page.screenshot(path="/tmp/ejemplo_busqueda.png")
        print("Screenshot guardado: /tmp/ejemplo_busqueda.png")

        time.sleep(2)


def ejemplo_extraccion():
    """Ejemplo 4: Extracción de datos"""
    print("\n" + "="*50)
    print("Ejemplo 4: Extracción de Datos")
    print("="*50)

    with Camoufox(headless="virtual", humanize=True, i_know_what_im_doing=True) as browser:
        page = browser.new_page()

        print("Navegando a Hacker News...")
        page.goto("https://news.ycombinator.com")
        time.sleep(2)

        print("Extrayendo títulos...")
        titles = page.evaluate("""() => {
            const items = document.querySelectorAll('.titleline a');
            return Array.from(items).slice(0, 5).map(a => a.innerText);
        }""")

        print("\nTop 5 títulos:")
        for i, title in enumerate(titles, 1):
            print(f"  {i}. {title[:60]}...")


def main():
    print("\n" + "#"*50)
    print("# EJEMPLOS DE USO DE CAMOUFOX")
    print("#"*50)

    while True:
        print("\nOpciones:")
        print("1. Navegación simple (visible)")
        print("2. Modo background (invisible)")
        print("3. Búsqueda en Google")
        print("4. Extracción de datos")
        print("5. Ejecutar todos")
        print("0. Salir")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            ejemplo_navegacion_simple()
        elif opcion == "2":
            ejemplo_background()
        elif opcion == "3":
            ejemplo_busqueda()
        elif opcion == "4":
            ejemplo_extraccion()
        elif opcion == "5":
            ejemplo_navegacion_simple()
            ejemplo_background()
            ejemplo_busqueda()
            ejemplo_extraccion()
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()
