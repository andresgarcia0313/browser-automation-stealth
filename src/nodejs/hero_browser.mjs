#!/usr/bin/env node
/**
 * Ulixee Hero Browser Utility for Claude Code
 * ============================================
 * Human-like browser automation with TLS/TCP evasion.
 *
 * Modes:
 *   - visible: showChrome=true (see the browser)
 *   - background: showChrome=false (invisible)
 *
 * Usage:
 *   node hero_browser.mjs <url> [--visible] [--text] [--links] [--screenshot path]
 *
 * As module:
 *   import { browse, searchMercadoLibre } from './hero_browser.mjs';
 */

import Hero from '@ulixee/hero-playground';

/**
 * Navigate to URL with Hero browser
 * @param {string} url - URL to navigate to
 * @param {Object} options - Configuration options
 * @param {boolean} options.visible - Show browser window (default: true)
 * @param {Function} options.action - Custom action function(hero) to execute
 * @param {boolean} options.extractText - Extract visible text
 * @param {boolean} options.extractLinks - Extract all links
 * @param {string} options.screenshotPath - Path to save screenshot
 * @param {string} options.waitFor - CSS selector to wait for
 * @param {number} options.timeout - Navigation timeout in ms
 * @returns {Promise<Object>} Result object
 */
export async function browse(url, options = {}) {
  const {
    visible = true,
    action = null,
    extractText = false,
    extractLinks = false,
    screenshotPath = null,
    waitFor = null,
    timeout = 30000,
  } = options;

  const result = {
    url,
    title: null,
    success: false,
    error: null,
  };

  let hero;

  try {
    hero = new Hero({
      showChrome: visible,
      showChromeInteractions: visible,
      showDevtools: false,
    });

    // Navigate
    await hero.goto(url, { timeoutMs: timeout });
    await hero.waitForPaintingStable();

    // Wait for specific element if requested
    if (waitFor) {
      await hero.waitForElement(hero.document.querySelector(waitFor), {
        timeoutMs: timeout,
      });
    }

    // Get basic info
    result.title = await hero.document.title;
    result.finalUrl = await hero.url;

    // Extract text if requested
    if (extractText) {
      const body = hero.document.body;
      result.content = await body.innerText;
    }

    // Extract links if requested
    if (extractLinks) {
      const anchors = await hero.document.querySelectorAll('a[href]');
      const links = [];
      for (const anchor of anchors) {
        const text = (await anchor.innerText).trim();
        const href = await anchor.href;
        if (text) {
          links.push({ text, href });
        }
      }
      result.links = links;
    }

    // Take screenshot if requested
    if (screenshotPath) {
      const screenshot = await hero.takeScreenshot({ fullPage: true });
      const fs = await import('fs');
      fs.writeFileSync(screenshotPath, screenshot);
      result.screenshot = screenshotPath;
    }

    // Execute custom action if provided
    if (action) {
      result.actionResult = await action(hero);
    }

    result.success = true;

  } catch (error) {
    result.error = error.message;
    result.success = false;
  } finally {
    if (hero) {
      await hero.close();
    }
  }

  return result;
}

/**
 * Search MercadoLibre and extract products
 * @param {string} query - Search term
 * @param {Object} options - Options
 * @param {boolean} options.visible - Show browser
 * @param {number} options.maxResults - Max results to return
 * @param {string} options.country - Country code (co, mx, ar, cl)
 * @returns {Promise<Array>} Array of product objects
 */
export async function searchMercadoLibre(query, options = {}) {
  const {
    visible = true,
    maxResults = 10,
    country = 'co',
  } = options;

  const searchUrl = `https://listado.mercadolibre.com.${country}/${query.replace(/ /g, '-')}`;

  let hero;
  const products = [];

  try {
    hero = new Hero({
      showChrome: visible,
      showChromeInteractions: visible,
    });

    await hero.goto(searchUrl);
    await hero.waitForPaintingStable();

    // Wait for results
    await hero.waitForElement(hero.document.querySelector('.ui-search-results'), {
      timeoutMs: 15000,
    });

    // Extract products
    const items = await hero.document.querySelectorAll('.ui-search-result__wrapper');

    for (const item of items) {
      if (products.length >= maxResults) break;

      try {
        const titleEl = await item.querySelector('.ui-search-item__title');
        const priceEl = await item.querySelector('.andes-money-amount__fraction');
        const linkEl = await item.querySelector('a.ui-search-link');
        const shippingEl = await item.querySelector('.ui-search-item__shipping');

        const product = {
          title: titleEl ? await titleEl.innerText : null,
          price: priceEl ? await priceEl.innerText : null,
          link: linkEl ? await linkEl.href : null,
          shipping: shippingEl ? (await shippingEl.innerText).trim() : null,
        };

        if (product.title) {
          products.push(product);
        }
      } catch (e) {
        // Skip items that fail to parse
      }
    }

  } catch (error) {
    console.error('Search error:', error.message);
  } finally {
    if (hero) {
      await hero.close();
    }
  }

  return products;
}

// CLI interface
const args = process.argv.slice(2);

if (args.length > 0 && !args[0].startsWith('-')) {
  const url = args[0];
  const visible = args.includes('--visible') || args.includes('-v');
  const extractText = args.includes('--text') || args.includes('-t');
  const extractLinks = args.includes('--links') || args.includes('-l');

  let screenshotPath = null;
  const ssIndex = args.findIndex(a => a === '--screenshot' || a === '-s');
  if (ssIndex !== -1 && args[ssIndex + 1]) {
    screenshotPath = args[ssIndex + 1];
  }

  browse(url, {
    visible,
    extractText,
    extractLinks,
    screenshotPath,
  }).then(result => {
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.success ? 0 : 1);
  });
}
