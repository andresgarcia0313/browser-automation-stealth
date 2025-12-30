#!/usr/bin/env node
/**
 * Test: 3 instancias paralelas de Ulixee Hero en modo background
 * Cada instancia realiza interacciones y toma capturas secuenciales
 */

import Hero from '@ulixee/hero-playground';
import * as fs from 'fs';
import * as path from 'path';

const SCREENSHOTS_DIR = '/tmp/hero_parallel_test';

// Crear y limpiar directorio
if (fs.existsSync(SCREENSHOTS_DIR)) {
    fs.rmSync(SCREENSHOTS_DIR, { recursive: true });
}
fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });

async function screenshot(hero, instanceName, step, description) {
    const dir = path.join(SCREENSHOTS_DIR, instanceName);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    const filename = `${String(step).padStart(2, '0')}_${description}.png`;
    const filepath = path.join(dir, filename);

    const buffer = await hero.takeScreenshot();
    fs.writeFileSync(filepath, buffer);
    console.log(`    [${instanceName}] Captura: ${filename}`);
    return filepath;
}

async function tareaGoogleSearch() {
    const name = '01_google_search';
    console.log(`\n[${name}] Iniciando busqueda en Google...`);

    const hero = new Hero({
        showChrome: false,  // Modo background
        showChromeInteractions: false
    });

    try {
        // Paso 1: Ir a Google
        console.log(`  [${name}] Navegando a Google...`);
        await hero.goto('https://www.google.com');
        await hero.waitForPaintingStable();
        await screenshot(hero, name, 1, 'google_inicio');

        // Paso 2: Click en buscador
        console.log(`  [${name}] Click en buscador...`);
        const searchBox = await hero.document.querySelector('textarea[name="q"], input[name="q"]');
        await hero.click(searchBox);
        await hero.waitForMillis(500);
        await screenshot(hero, name, 2, 'click_buscador');

        // Paso 3: Escribir busqueda (Hero simula typing humano)
        console.log(`  [${name}] Escribiendo busqueda...`);
        await hero.type('Ulixee Hero browser automation');
        await hero.waitForMillis(1000);
        await screenshot(hero, name, 3, 'texto_escrito');

        // Paso 4: Enter y resultados
        console.log(`  [${name}] Presionando Enter...`);
        await hero.activeTab.keyboard.press('Enter');
        await hero.waitForPaintingStable();
        await hero.waitForMillis(2000);
        await screenshot(hero, name, 4, 'resultados');

        // Paso 5: Scroll
        console.log(`  [${name}] Haciendo scroll...`);
        await hero.scrollTo({ top: 500 });
        await hero.waitForMillis(1000);
        await screenshot(hero, name, 5, 'scroll_resultados');

        console.log(`[${name}] COMPLETADO!`);
        return name;

    } catch (error) {
        console.log(`[${name}] ERROR: ${error.message}`);
        return null;
    } finally {
        await hero.close();
    }
}

async function tareaWikipediaNav() {
    const name = '02_wikipedia_nav';
    console.log(`\n[${name}] Iniciando navegacion en Wikipedia...`);

    const hero = new Hero({
        showChrome: false,
        showChromeInteractions: false
    });

    try {
        // Paso 1: Wikipedia
        console.log(`  [${name}] Navegando a Wikipedia...`);
        await hero.goto('https://es.wikipedia.org');
        await hero.waitForPaintingStable();
        await screenshot(hero, name, 1, 'wikipedia_inicio');

        // Paso 2: Click buscador
        console.log(`  [${name}] Click en buscador...`);
        const searchInput = await hero.document.querySelector('#searchInput');
        await hero.click(searchInput);
        await hero.waitForMillis(500);
        await screenshot(hero, name, 2, 'click_buscador');

        // Paso 3: Escribir
        console.log(`  [${name}] Escribiendo busqueda...`);
        await hero.type('Machine learning');
        await hero.waitForMillis(1000);
        await screenshot(hero, name, 3, 'texto_busqueda');

        // Paso 4: Buscar
        console.log(`  [${name}] Presionando Enter...`);
        await hero.activeTab.keyboard.press('Enter');
        await hero.waitForPaintingStable();
        await hero.waitForMillis(2000);
        await screenshot(hero, name, 4, 'articulo');

        // Paso 5: Scroll
        console.log(`  [${name}] Haciendo scroll...`);
        await hero.scrollTo({ top: 600 });
        await hero.waitForMillis(1000);
        await screenshot(hero, name, 5, 'scroll_contenido');

        console.log(`[${name}] COMPLETADO!`);
        return name;

    } catch (error) {
        console.log(`[${name}] ERROR: ${error.message}`);
        return null;
    } finally {
        await hero.close();
    }
}

async function tareaGitHubExplore() {
    const name = '03_github_explore';
    console.log(`\n[${name}] Iniciando exploracion de GitHub...`);

    const hero = new Hero({
        showChrome: false,
        showChromeInteractions: false
    });

    try {
        // Paso 1: GitHub Trending
        console.log(`  [${name}] Navegando a GitHub Trending...`);
        await hero.goto('https://github.com/trending');
        await hero.waitForPaintingStable();
        await hero.waitForMillis(2000);
        await screenshot(hero, name, 1, 'github_trending');

        // Paso 2: Scroll
        console.log(`  [${name}] Haciendo scroll...`);
        await hero.scrollTo({ top: 400 });
        await hero.waitForMillis(1000);
        await screenshot(hero, name, 2, 'scroll_repos');

        // Paso 3: Mas scroll
        console.log(`  [${name}] Mas scroll...`);
        await hero.scrollTo({ top: 800 });
        await hero.waitForMillis(1000);
        await screenshot(hero, name, 3, 'mas_repos');

        // Paso 4: Click en repo
        console.log(`  [${name}] Click en repositorio...`);
        try {
            const repoLink = await hero.document.querySelector('article h2 a');
            if (repoLink) {
                await hero.click(repoLink);
                await hero.waitForPaintingStable();
                await hero.waitForMillis(2000);
                await screenshot(hero, name, 4, 'repo_detalle');
            }
        } catch (e) {
            await screenshot(hero, name, 4, 'sin_click_repo');
        }

        // Paso 5: Scroll en repo
        console.log(`  [${name}] Scroll en repo...`);
        await hero.scrollTo({ top: 500 });
        await hero.waitForMillis(1000);
        await screenshot(hero, name, 5, 'repo_readme');

        console.log(`[${name}] COMPLETADO!`);
        return name;

    } catch (error) {
        console.log(`[${name}] ERROR: ${error.message}`);
        return null;
    } finally {
        await hero.close();
    }
}

async function main() {
    console.log('='.repeat(70));
    console.log('TEST: 3 Instancias Paralelas de Ulixee Hero (Background)');
    console.log('='.repeat(70));
    console.log(`\nCarpeta de capturas: ${SCREENSHOTS_DIR}`);
    console.log('Las 3 instancias correran EN PARALELO');
    console.log('-'.repeat(70));

    const startTime = Date.now();

    console.log('\n[INICIO] Lanzando 3 navegadores Hero en paralelo...');

    // Ejecutar las 3 tareas en paralelo
    const results = await Promise.allSettled([
        tareaGoogleSearch(),
        tareaWikipediaNav(),
        tareaGitHubExplore()
    ]);

    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

    // Contar screenshots
    console.log(`\n${'='.repeat(70)}`);
    console.log('CAPTURAS TOMADAS:');
    console.log('-'.repeat(70));

    let totalScreenshots = 0;
    const dirs = fs.readdirSync(SCREENSHOTS_DIR);

    for (const dir of dirs.sort()) {
        const dirPath = path.join(SCREENSHOTS_DIR, dir);
        if (fs.statSync(dirPath).isDirectory()) {
            const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.png')).sort();
            totalScreenshots += files.length;
            console.log(`\n${dir}/ (${files.length} capturas)`);
            for (const f of files) {
                console.log(`  ${f}`);
            }
        }
    }

    console.log(`\n${'='.repeat(70)}`);
    console.log('TEST COMPLETADO');
    console.log('='.repeat(70));
    console.log(`Tiempo total: ${elapsed} segundos`);
    console.log(`Instancias paralelas: 3`);
    console.log(`Total screenshots: ${totalScreenshots}`);
    console.log(`Carpeta: ${SCREENSHOTS_DIR}`);
    console.log(`\n*** NINGUNA VENTANA FUE VISIBLE (Hero headless) ***`);
    console.log('='.repeat(70));
}

main().catch(console.error);
