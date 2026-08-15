const { chromium } = require('playwright');

const URL = 'https://7366806822-pixel.github.io/mi-pagina-web/';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await context.newPage();
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });

  try {
    await page.goto(URL, { waitUntil: 'domcontentloaded' });
    await page.waitForSelector('#sidebarCollapse', { state: 'visible', timeout: 30000 });
    await page.waitForFunction(() =>
      typeof db !== 'undefined' && db.client &&
      typeof state !== 'undefined' &&
      document.querySelectorAll('#navRoot .nav-item').length > 0,
      { timeout: 45000 }
    );

    const btn = page.locator('#sidebarCollapse');

    // 1. Contraer con el botón.
    await btn.click();
    await page.waitForFunction(() => document.body.classList.contains('sidebar-collapsed'));
    if (!(await btn.isVisible())) throw new Error('El botón para reabrir el menú quedó oculto.');
    if ((await btn.getAttribute('aria-label')) !== 'Expandir menú') throw new Error('El botón no cambió a modo Expandir menú.');

    // 2. Volver a abrir con el mismo botón.
    await btn.click();
    await page.waitForFunction(() => !document.body.classList.contains('sidebar-collapsed'));
    if ((await btn.getAttribute('aria-label')) !== 'Contraer menú') throw new Error('El botón no volvió a modo Contraer menú.');

    // 3. Comprobar el atajo de respaldo Alt+M.
    await page.keyboard.press('Alt+M');
    await page.waitForFunction(() => document.body.classList.contains('sidebar-collapsed'));
    if (!(await btn.isVisible())) throw new Error('El botón quedó oculto tras usar Alt+M.');
    await page.keyboard.press('Alt+M');
    await page.waitForFunction(() => !document.body.classList.contains('sidebar-collapsed'));

    // 4. Persistencia del estado contraído y recuperación después de recargar.
    await btn.click();
    await page.waitForFunction(() => document.body.classList.contains('sidebar-collapsed'));
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForSelector('#sidebarCollapse', { state: 'visible', timeout: 30000 });
    await page.waitForFunction(() => document.body.classList.contains('sidebar-collapsed'));
    const reloadedBtn = page.locator('#sidebarCollapse');
    if (!(await reloadedBtn.isVisible())) throw new Error('Después de recargar, el menú quedó cerrado sin control visible.');
    await reloadedBtn.click();
    await page.waitForFunction(() => !document.body.classList.contains('sidebar-collapsed'));

    if (errors.some(x => /failed to fetch/i.test(x))) throw new Error('Se detectó Failed to fetch: ' + errors.join(' | '));

    console.log('SIDEBAR_COLLAPSE_REOPEN_OK');
    console.log('SIDEBAR_ALT_M_OK');
    console.log('SIDEBAR_RELOAD_RECOVERY_OK');
  } finally {
    await browser.close();
  }
})().catch(err => {
  console.error(err);
  process.exit(1);
});
