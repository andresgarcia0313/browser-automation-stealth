# MCP Server - Camoufox Browser

Servidor MCP (Model Context Protocol) que permite a Claude Code controlar un navegador Camoufox directamente.

## Instalación

```bash
# 1. Instalar dependencias
pip install mcp camoufox[geoip]

# 2. Descargar navegador
python -m camoufox fetch
```

## Configuración en Claude Code

Agregar a `~/.claude/settings.json`:

```json
{
    "mcpServers": {
        "camoufox": {
            "command": "python3",
            "args": ["/home/andres/Desarrollo/AI/browser-automation-stealth/mcp-server/camoufox_mcp_server.py"]
        }
    }
}
```

## Herramientas Disponibles

| Herramienta | Descripción |
|-------------|-------------|
| `browser_navigate` | Navegar a una URL |
| `browser_click` | Click en un elemento |
| `browser_fill` | Llenar campo de texto |
| `browser_press` | Presionar tecla |
| `browser_screenshot` | Tomar captura |
| `browser_extract` | Extraer datos con JS |
| `browser_get_content` | Obtener texto |
| `browser_scroll` | Hacer scroll |
| `browser_wait` | Esperar tiempo/elemento |
| `browser_close` | Cerrar navegador |
| `browser_status` | Estado actual |

## Uso desde Claude Code

Una vez configurado, Claude Code puede usar el navegador:

```
Usuario: Busca en Google "clima bogota" y dime el resultado

Claude: [Usa browser_navigate para ir a Google]
        [Usa browser_fill para escribir la búsqueda]
        [Usa browser_press para presionar Enter]
        [Usa browser_get_content para obtener resultados]
```

## Test Manual

```bash
# Verificar que el servidor inicia correctamente
python3 camoufox_mcp_server.py
# Debería quedar esperando input (Ctrl+C para salir)
```
