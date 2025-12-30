#!/usr/bin/env python3
"""
MCP Server para Camoufox - Browser Automation Stealth
======================================================

Servidor MCP (Model Context Protocol) que permite a Claude Code
controlar un navegador Camoufox directamente.

Instalación:
1. pip install mcp camoufox[geoip]
2. python -m camoufox fetch
3. Agregar a ~/.claude/settings.json (ver abajo)

Configuración en settings.json:
{
    "mcpServers": {
        "camoufox": {
            "command": "python3",
            "args": ["/ruta/a/camoufox_mcp_server.py"]
        }
    }
}

Herramientas disponibles:
- browser_navigate: Navegar a una URL
- browser_click: Click en un elemento
- browser_fill: Llenar un campo de texto
- browser_screenshot: Tomar screenshot
- browser_extract: Extraer datos de la página
- browser_close: Cerrar navegador
"""

import asyncio
import json
import base64
import os
from typing import Optional, Any
from contextlib import asynccontextmanager

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent, ImageContent
except ImportError:
    print("ERROR: Instalar mcp con: pip install mcp")
    exit(1)

try:
    from camoufox.async_api import AsyncCamoufox
except ImportError:
    print("ERROR: Instalar camoufox con: pip install camoufox[geoip]")
    exit(1)

try:
    from pyvirtualdisplay import Display
except ImportError:
    Display = None


class BrowserState:
    def __init__(self):
        self.browser = None
        self.page = None
        self.context = None
        self.display = None

    async def ensure_browser(self, visible: bool = False):
        if self.browser is None:
            if not visible and Display:
                self.display = Display(visible=False, size=(1920, 1080))
                self.display.start()
            self.context = AsyncCamoufox(
                headless=False,
                humanize=True,
                i_know_what_im_doing=True
            )
            self.browser = await self.context.__aenter__()
            self.page = await self.browser.new_page()
        return self.page

    async def close(self):
        if self.context:
            await self.context.__aexit__(None, None, None)
        if self.display:
            self.display.stop()
        self.browser = None
        self.page = None
        self.context = None
        self.display = None


state = BrowserState()
server = Server("camoufox-browser")


@server.list_tools()
async def list_tools():
    """Lista de herramientas disponibles"""
    return [
        Tool(
            name="browser_navigate",
            description="Navegar a una URL. El navegador se abre automáticamente si no está abierto.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL a la que navegar"
                    },
                    "visible": {
                        "type": "boolean",
                        "description": "True para ver el navegador, False para modo background",
                        "default": False
                    },
                    "wait_until": {
                        "type": "string",
                        "description": "Evento de espera: domcontentloaded, load, networkidle",
                        "default": "domcontentloaded"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="browser_click",
            description="Hacer click en un elemento usando selector CSS",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "Selector CSS del elemento (ej: '#boton', '.clase', 'button')"
                    }
                },
                "required": ["selector"]
            }
        ),
        Tool(
            name="browser_fill",
            description="Llenar un campo de texto con un valor",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "Selector CSS del campo"
                    },
                    "value": {
                        "type": "string",
                        "description": "Texto a escribir"
                    }
                },
                "required": ["selector", "value"]
            }
        ),
        Tool(
            name="browser_press",
            description="Presionar una tecla (Enter, Tab, Escape, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "Selector CSS del elemento"
                    },
                    "key": {
                        "type": "string",
                        "description": "Tecla a presionar (Enter, Tab, Escape, ArrowDown, etc.)"
                    }
                },
                "required": ["selector", "key"]
            }
        ),
        Tool(
            name="browser_screenshot",
            description="Tomar screenshot de la página actual",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta donde guardar el screenshot (opcional)"
                    },
                    "full_page": {
                        "type": "boolean",
                        "description": "Capturar página completa o solo viewport",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="browser_extract",
            description="Extraer datos de la página usando JavaScript",
            inputSchema={
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "Código JavaScript que retorna los datos a extraer"
                    }
                },
                "required": ["script"]
            }
        ),
        Tool(
            name="browser_get_content",
            description="Obtener el contenido de texto de la página o un elemento",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "Selector CSS (opcional, usa 'body' si no se especifica)"
                    }
                }
            }
        ),
        Tool(
            name="browser_scroll",
            description="Hacer scroll en la página",
            inputSchema={
                "type": "object",
                "properties": {
                    "y": {
                        "type": "integer",
                        "description": "Pixels a hacer scroll hacia abajo (negativo = arriba)"
                    }
                },
                "required": ["y"]
            }
        ),
        Tool(
            name="browser_wait",
            description="Esperar un tiempo o hasta que aparezca un elemento",
            inputSchema={
                "type": "object",
                "properties": {
                    "milliseconds": {
                        "type": "integer",
                        "description": "Milisegundos a esperar"
                    },
                    "selector": {
                        "type": "string",
                        "description": "Selector CSS a esperar (alternativa a milliseconds)"
                    }
                }
            }
        ),
        Tool(
            name="browser_close",
            description="Cerrar el navegador",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="browser_status",
            description="Obtener estado actual del navegador (URL, título, etc.)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """Ejecutar una herramienta"""
    try:
        if name == "browser_navigate":
            page = await state.ensure_browser(arguments.get("visible", False))
            url = arguments["url"]
            wait_until = arguments.get("wait_until", "domcontentloaded")
            await page.goto(url, wait_until=wait_until)
            await asyncio.sleep(1)  # Pequeña espera para estabilidad
            title = await page.title()
            return [TextContent(type="text", text=f"Navegado a: {url}\nTítulo: {title}")]

        elif name == "browser_click":
            if state.page is None:
                return [TextContent(type="text", text="Error: Navegador no inicializado. Usa browser_navigate primero.")]
            selector = arguments["selector"]
            await state.page.click(selector)
            await asyncio.sleep(0.5)
            return [TextContent(type="text", text=f"Click realizado en: {selector}")]

        elif name == "browser_fill":
            if state.page is None:
                return [TextContent(type="text", text="Error: Navegador no inicializado.")]
            selector = arguments["selector"]
            value = arguments["value"]
            await state.page.fill(selector, value)
            return [TextContent(type="text", text=f"Campo {selector} llenado con: {value}")]

        elif name == "browser_press":
            if state.page is None:
                return [TextContent(type="text", text="Error: Navegador no inicializado.")]
            selector = arguments["selector"]
            key = arguments["key"]
            await state.page.press(selector, key)
            await asyncio.sleep(0.5)
            return [TextContent(type="text", text=f"Tecla {key} presionada en {selector}")]

        elif name == "browser_screenshot":
            if state.page is None:
                return [TextContent(type="text", text="Error: Navegador no inicializado.")]
            path = arguments.get("path", "/tmp/mcp_screenshot.png")
            full_page = arguments.get("full_page", False)
            await state.page.screenshot(path=path, full_page=full_page)
            return [TextContent(type="text", text=f"Screenshot guardado en: {path}")]

        elif name == "browser_extract":
            if state.page is None:
                return [TextContent(type="text", text="Error: Navegador no inicializado.")]
            script = arguments["script"]
            result = await state.page.evaluate(script)
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]

        elif name == "browser_get_content":
            if state.page is None:
                return [TextContent(type="text", text="Error: Navegador no inicializado.")]
            selector = arguments.get("selector", "body")
            content = await state.page.inner_text(selector)
            # Limitar contenido para no saturar
            if len(content) > 5000:
                content = content[:5000] + "\n... (truncado)"
            return [TextContent(type="text", text=content)]

        elif name == "browser_scroll":
            if state.page is None:
                return [TextContent(type="text", text="Error: Navegador no inicializado.")]
            y = arguments["y"]
            await state.page.evaluate(f"window.scrollBy(0, {y})")
            await asyncio.sleep(0.3)
            return [TextContent(type="text", text=f"Scroll realizado: {y}px")]

        elif name == "browser_wait":
            if state.page is None:
                return [TextContent(type="text", text="Error: Navegador no inicializado.")]
            if "milliseconds" in arguments:
                ms = arguments["milliseconds"]
                await asyncio.sleep(ms / 1000)
                return [TextContent(type="text", text=f"Esperado {ms}ms")]
            elif "selector" in arguments:
                selector = arguments["selector"]
                await state.page.wait_for_selector(selector, timeout=10000)
                return [TextContent(type="text", text=f"Elemento encontrado: {selector}")]
            return [TextContent(type="text", text="Especifica milliseconds o selector")]

        elif name == "browser_close":
            await state.close()
            return [TextContent(type="text", text="Navegador cerrado")]

        elif name == "browser_status":
            if state.page is None:
                return [TextContent(type="text", text="Navegador: No inicializado")]
            url = state.page.url
            title = await state.page.title()
            return [TextContent(type="text", text=f"URL: {url}\nTítulo: {title}\nEstado: Activo")]

        else:
            return [TextContent(type="text", text=f"Herramienta desconocida: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Iniciar servidor MCP"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
