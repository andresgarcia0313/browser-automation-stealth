#!/usr/bin/env python3
"""
Camoufox Browser Utility for Claude Code
=========================================
Anti-detection browser automation with human-like behavior.

Modes:
  - visible: headless=False (see the browser)
  - background: headless="virtual" (invisible, uses virtual display)

Usage:
  from camoufox_browser import browse, browse_async

  # Simple navigation
  result = browse("https://example.com", visible=True)

  # With custom actions
  def my_task(page):
      page.click("#button")
      return page.content()

  result = browse("https://example.com", action=my_task)
"""

import sys
import json
import os
from typing import Callable, Optional, Any, List, Dict
from contextlib import contextmanager
from camoufox.sync_api import Camoufox
from camoufox.async_api import AsyncCamoufox

@contextmanager
def virtual_display(visible: bool):
    if visible:
        yield
    else:
        from pyvirtualdisplay import Display
        display = Display(visible=False, size=(1920, 1080))
        display.start()
        try:
            yield
        finally:
            display.stop()


def browse(
    url: str,
    visible: bool = True,
    action: Optional[Callable] = None,
    humanize: bool = True,
    timeout: int = 30000,
    screenshot_path: Optional[str] = None,
    wait_for: Optional[str] = None,
    extract_text: bool = False,
    extract_links: bool = False,
) -> Dict[str, Any]:
    """
    Navigate to URL with Camoufox browser.

    Args:
        url: URL to navigate to
        visible: True to see browser, False for background (virtual display)
        action: Optional function(page) to execute custom actions
        humanize: Enable human-like cursor movement (max 2 seconds)
        timeout: Page load timeout in milliseconds
        screenshot_path: Path to save screenshot (optional)
        wait_for: CSS selector to wait for before continuing
        extract_text: Extract all visible text from page
        extract_links: Extract all links from page

    Returns:
        Dict with: url, title, content (if extract_text), links (if extract_links),
                   screenshot (path if taken), action_result (if action provided)
    """
    result = {
        "url": url,
        "title": None,
        "success": False,
        "error": None,
    }

    try:
        with virtual_display(visible):
            with Camoufox(
                headless=False,
                humanize=2.0 if humanize else False,
                i_know_what_im_doing=True,
            ) as browser:
                page = browser.new_page()
                page.set_default_timeout(timeout)

                page.goto(url, wait_until="networkidle")

                if wait_for:
                    page.wait_for_selector(wait_for, timeout=timeout)

                result["title"] = page.title()
                result["final_url"] = page.url

                if extract_text:
                    result["content"] = page.inner_text("body")

                if extract_links:
                    links = page.eval_on_selector_all(
                        "a[href]",
                        "elements => elements.map(e => ({text: e.innerText.trim(), href: e.href}))"
                    )
                    result["links"] = [l for l in links if l["text"]]

                if screenshot_path:
                    page.screenshot(path=screenshot_path, full_page=True)
                    result["screenshot"] = screenshot_path

                if action:
                    result["action_result"] = action(page)

                result["success"] = True

    except Exception as e:
        result["error"] = str(e)
        result["success"] = False

    return result


async def browse_async(
    url: str,
    visible: bool = True,
    action: Optional[Callable] = None,
    humanize: bool = True,
    timeout: int = 30000,
) -> Dict[str, Any]:
    """
    Async version of browse(). See browse() for documentation.
    """
    headless = False if visible else "virtual"

    result = {
        "url": url,
        "title": None,
        "success": False,
        "error": None,
    }

    try:
        async with AsyncCamoufox(
            headless=headless,
            humanize=2.0 if humanize else False,
            i_know_what_im_doing=True,
        ) as browser:
            page = await browser.new_page()
            page.set_default_timeout(timeout)

            await page.goto(url, wait_until="domcontentloaded")

            result["title"] = await page.title()
            result["final_url"] = page.url
            result["success"] = True

            if action:
                result["action_result"] = await action(page)

    except Exception as e:
        result["error"] = str(e)
        result["success"] = False

    return result


def search_mercadolibre(
    query: str,
    visible: bool = True,
    max_results: int = 10,
    country: str = "co",  # co=Colombia, mx=Mexico, ar=Argentina, etc.
) -> List[Dict[str, Any]]:
    """
    Search MercadoLibre and extract product results.

    Args:
        query: Search term
        visible: Show browser or run in background
        max_results: Maximum number of results to return
        country: Country code (co, mx, ar, cl, etc.)

    Returns:
        List of products with: title, price, link, seller, shipping
    """
    base_url = f"https://listado.mercadolibre.com.{country}"
    search_url = f"{base_url}/{query.replace(' ', '-')}"

    def extract_products(page):
        import time
        time.sleep(3)

        products = page.evaluate('''() => {
            const results = [];
            const cards = document.querySelectorAll(".poly-card");

            cards.forEach(card => {
                const img = card.querySelector("img[title]");
                const priceEl = card.querySelector("[class*='price'] [class*='fraction'], [class*='money'] [class*='fraction']");
                const linkEl = card.querySelector("a[href]");
                const shippingEl = card.querySelector("[class*='shipping']");

                if (img && priceEl) {
                    results.push({
                        title: img.getAttribute("title"),
                        price: priceEl.innerText.replace(/[^0-9]/g, ""),
                        link: linkEl ? linkEl.href : null,
                        shipping: shippingEl ? shippingEl.innerText.trim() : null
                    });
                }
            });
            return results;
        }''')

        seen = set()
        unique = []
        for p in products:
            if p["title"] and p["title"] not in seen:
                seen.add(p["title"])
                unique.append(p)
        return unique[:max_results]

    result = browse(
        search_url,
        visible=visible,
        action=extract_products,
        humanize=True,
        wait_for=".poly-card",
        timeout=45000,
    )

    if result["success"] and result.get("action_result"):
        return result["action_result"]
    else:
        return []


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Camoufox Browser CLI")
    parser.add_argument("url", help="URL to navigate to")
    parser.add_argument("--visible", "-v", action="store_true", help="Show browser window")
    parser.add_argument("--text", "-t", action="store_true", help="Extract text content")
    parser.add_argument("--links", "-l", action="store_true", help="Extract links")
    parser.add_argument("--screenshot", "-s", help="Save screenshot to path")

    args = parser.parse_args()

    result = browse(
        args.url,
        visible=args.visible,
        extract_text=args.text,
        extract_links=args.links,
        screenshot_path=args.screenshot,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))
