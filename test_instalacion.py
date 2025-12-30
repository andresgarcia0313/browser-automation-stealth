#!/usr/bin/env python3
"""
Test de Instalación - Browser Automation Stealth
=================================================

Verifica que todos los componentes están instalados correctamente.
Ejecutar después de install.sh para confirmar que todo funciona.

Uso: python3 test_instalacion.py
"""

import sys
import os
import subprocess
from datetime import datetime

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def ok(msg):
    print(f"  {Colors.GREEN}✓{Colors.END} {msg}")

def fail(msg):
    print(f"  {Colors.RED}✗{Colors.END} {msg}")

def warn(msg):
    print(f"  {Colors.YELLOW}!{Colors.END} {msg}")

def header(msg):
    print(f"\n{Colors.BLUE}[*] {msg}{Colors.END}")


def test_python_version():
    """Verificar versión de Python"""
    header("Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        ok(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        fail(f"Python {version.major}.{version.minor} (necesita 3.9+)")
        return False


def test_camoufox_import():
    """Verificar que Camoufox se puede importar"""
    header("Verificando Camoufox...")
    try:
        from camoufox.sync_api import Camoufox
        from camoufox.async_api import AsyncCamoufox
        ok("Módulo camoufox importado correctamente")
        return True
    except ImportError as e:
        fail(f"No se puede importar camoufox: {e}")
        print("    Instalar con: pip install camoufox[geoip]")
        return False


def test_camoufox_browser():
    """Verificar que el navegador Camoufox está descargado"""
    header("Verificando navegador Camoufox...")
    cache_dir = os.path.expanduser("~/.cache/camoufox")
    if os.path.exists(cache_dir) and os.listdir(cache_dir):
        ok(f"Navegador encontrado en {cache_dir}")
        return True
    else:
        fail("Navegador no encontrado")
        print("    Descargar con: python -m camoufox fetch")
        return False


def test_xvfb():
    """Verificar que Xvfb está instalado (para modo background)"""
    header("Verificando Xvfb...")
    try:
        result = subprocess.run(['which', 'Xvfb'], capture_output=True, text=True)
        if result.returncode == 0:
            ok(f"Xvfb encontrado: {result.stdout.strip()}")
            return True
        else:
            warn("Xvfb no encontrado (necesario para modo background)")
            print("    Instalar con: sudo apt install xvfb")
            return False
    except Exception as e:
        warn(f"No se pudo verificar Xvfb: {e}")
        return False


def test_node():
    """Verificar Node.js"""
    header("Verificando Node.js...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            ok(f"Node.js {version}")
            return True
        else:
            warn("Node.js no encontrado (opcional, solo para Hero)")
            return False
    except FileNotFoundError:
        warn("Node.js no instalado (opcional, solo para Hero)")
        return False


def test_hero():
    """Verificar Ulixee Hero"""
    header("Verificando Ulixee Hero...")
    hero_dir = os.path.expanduser("~/.claude/browser-tools/node_modules/@ulixee")
    if os.path.exists(hero_dir):
        ok("Hero instalado en ~/.claude/browser-tools/")
        return True
    else:
        warn("Hero no instalado (opcional)")
        print("    Instalar con: cd ~/.claude/browser-tools && npm install @ulixee/hero-playground")
        return False


def test_chrome_sandbox():
    """Verificar sandbox de Chrome para Hero"""
    header("Verificando Chrome sandbox...")
    cache_dir = os.path.expanduser("~/.cache/ulixee/chrome")
    if not os.path.exists(cache_dir):
        warn("Chrome de Hero no descargado aún")
        return False

    # Buscar chrome-sandbox
    for root, dirs, files in os.walk(cache_dir):
        if 'chrome-sandbox' in files:
            sandbox_path = os.path.join(root, 'chrome-sandbox')
            stat = os.stat(sandbox_path)
            # Verificar que tiene setuid bit (mode 4755)
            if stat.st_mode & 0o4000:
                ok(f"Chrome sandbox configurado correctamente")
                return True
            else:
                fail("Chrome sandbox sin permisos setuid")
                print(f"    Ejecutar: sudo chmod 4755 {sandbox_path}")
                return False

    warn("chrome-sandbox no encontrado")
    return False


def test_camoufox_quick():
    """Test rápido de Camoufox (modo background)"""
    header("Test rápido de Camoufox...")
    try:
        from camoufox.sync_api import Camoufox

        with Camoufox(headless="virtual", humanize=False, i_know_what_im_doing=True) as browser:
            page = browser.new_page()
            page.goto("https://example.com", wait_until="domcontentloaded")
            title = page.title()

            if "Example" in title:
                ok(f"Navegación exitosa: {title}")
                return True
            else:
                fail(f"Título inesperado: {title}")
                return False

    except Exception as e:
        fail(f"Error en test: {e}")
        return False


def test_claude_tools_dir():
    """Verificar directorio de herramientas de Claude"""
    header("Verificando ~/.claude/browser-tools/...")
    tools_dir = os.path.expanduser("~/.claude/browser-tools")
    if os.path.exists(tools_dir):
        files = os.listdir(tools_dir)
        py_files = [f for f in files if f.endswith('.py')]
        if py_files:
            ok(f"Directorio existe con {len(py_files)} scripts Python")
            return True
        else:
            warn("Directorio existe pero sin scripts Python")
            return False
    else:
        warn("Directorio no existe")
        print("    Crear con: mkdir -p ~/.claude/browser-tools")
        return False


def main():
    print("=" * 60)
    print("TEST DE INSTALACIÓN - Browser Automation Stealth")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {
        "Python": test_python_version(),
        "Camoufox módulo": test_camoufox_import(),
        "Camoufox navegador": test_camoufox_browser(),
        "Xvfb": test_xvfb(),
        "Node.js": test_node(),
        "Hero": test_hero(),
        "Chrome sandbox": test_chrome_sandbox(),
        "Claude tools dir": test_claude_tools_dir(),
    }

    # Test funcional solo si lo básico está OK
    if results["Camoufox módulo"] and results["Camoufox navegador"]:
        results["Camoufox test"] = test_camoufox_quick()

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test, passed_test in results.items():
        status = f"{Colors.GREEN}OK{Colors.END}" if passed_test else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {test}: {status}")

    print(f"\n  Total: {passed}/{total} tests pasados")

    if passed == total:
        print(f"\n{Colors.GREEN}¡Instalación completa y funcional!{Colors.END}")
        return 0
    elif passed >= total - 2:
        print(f"\n{Colors.YELLOW}Instalación básica OK (algunos componentes opcionales faltan){Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}Instalación incompleta. Revisar errores arriba.{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
