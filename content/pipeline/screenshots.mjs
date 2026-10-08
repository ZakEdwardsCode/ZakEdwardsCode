#!/usr/bin/env node
// Captures real app screenshots from plasmo.uk into /content/screenshots.
//   PLASMO_TEST_EMAIL=... PLASMO_TEST_PASSWORD=... node pipeline/screenshots.mjs [--headed] [shot-name ...]
// Safety: payment/billing traffic is blocked, buttons that look like payments are never clicked,
// at most `maxAiMarks` answers are submitted for AI marking, and only the test account is used.
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import { DIRS, p } from './lib/paths.mjs';

const cfg = JSON.parse(fs.readFileSync(p('pipeline/screenshots.config.json'), 'utf8'));
const args = process.argv.slice(2);
const headed = args.includes('--headed');
const only = args.filter((a) => !a.startsWith('--'));
const { PLASMO_TEST_EMAIL: email, PLASMO_TEST_PASSWORD: password } = process.env;

const BLOCKED_URL = /stripe\.com|checkout|billing|payment|subscribe|upgrade|\/pricing\/buy|paypal/i;
const BLOCKED_CLICK = /\b(pay|buy|purchase|subscribe|upgrade|checkout|billing|delete|remove|cancel subscription|unsubscribe)\b/i;
const debugDir = path.join(DIRS.screenshots, '_debug');
let aiMarks = 0;

async function guardedClick(locator, label) {
  const text = ((await locator.innerText().catch(() => '')) + ' ' + ((await locator.getAttribute('href').catch(() => '')) || '')).trim();
  if (BLOCKED_CLICK.test(text) || BLOCKED_URL.test(text)) throw new Error(`refusing to click "${text}" (${label}): looks like a payment/destructive action`);
  await locator.click();
}

async function runStep(page, step) {
  if (step.goto) return page.goto(new URL(step.goto, cfg.baseUrl).href, { waitUntil: 'networkidle' });
  if (step.wait) return page.waitForTimeout(step.wait);
  if (step.waitFor) return page.locator(step.waitFor).first().waitFor({ timeout: step.timeout ?? 15000 });
  if (step.scroll) return page.mouse.wheel(0, step.scroll);
  if (step.fill) return page.locator(step.fill.selector).first().fill(step.fill.value);
  if (step.clickText) return guardedClick(page.getByText(step.clickText, { exact: false }).first(), step.clickText);
  if (step.click) return guardedClick(page.locator(step.click).first(), step.click);
  if (step.submitForMarking) {
    if (aiMarks >= cfg.maxAiMarks) throw new Error(`AI mark budget (${cfg.maxAiMarks}) used up`);
    aiMarks++;
    console.log(`    AI mark ${aiMarks}/${cfg.maxAiMarks}`);
    return guardedClick(page.locator(step.submitForMarking).first(), 'submitForMarking');
  }
  throw new Error(`unknown step ${JSON.stringify(step)}`);
}

async function login(page) {
  const l = cfg.login;
  await page.goto(new URL(l.path, cfg.baseUrl).href, { waitUntil: 'networkidle' });
  await page.locator(l.email).first().fill(email);
  await page.locator(l.password).first().fill(password);
  await page.locator(l.submit).first().click();
  await page.waitForURL((u) => !u.href.includes(l.successUrlNot), { timeout: 30000 });
}

async function main() {
  fs.mkdirSync(debugDir, { recursive: true });
  const shots = cfg.shots.filter((s) => !only.length || only.includes(s.name) || only.includes(s.name.replace(/\.png$/, '')));
  const needsLogin = shots.some((s) => s.loggedIn !== false);
  if (needsLogin && (!email || !password)) {
    console.error('Set PLASMO_TEST_EMAIL and PLASMO_TEST_PASSWORD (a dedicated test account, never a real student).');
    process.exit(1);
  }
  const browser = await chromium.launch({ headless: !headed });
  const ctxOpts = { viewport: cfg.viewport, deviceScaleFactor: cfg.deviceScaleFactor, isMobile: true, hasTouch: true, locale: 'en-GB', timezoneId: 'Europe/London' };
  const anon = await browser.newContext(ctxOpts);
  const authed = await browser.newContext(ctxOpts);
  for (const c of [anon, authed]) {
    await c.route('**/*', (route) => (BLOCKED_URL.test(route.request().url()) ? route.abort() : route.continue()));
  }
  const pages = { anon: await anon.newPage(), authed: await authed.newPage() };
  if (needsLogin) { console.log('• logging in as test account'); await login(pages.authed); }

  let failed = 0;
  for (const shot of shots) {
    const page = shot.loggedIn === false ? pages.anon : pages.authed;
    console.log(`• ${shot.name}`);
    try {
      for (const step of shot.steps) {
        try { await runStep(page, step); }
        catch (e) { if (step.optional) console.log(`    (optional step skipped: ${e.message.split('\n')[0]})`); else throw e; }
      }
      const mask = (cfg.maskSelectors || []).map((s) => page.locator(s));
      await page.screenshot({ path: path.join(DIRS.screenshots, shot.name), mask, animations: 'disabled' });
      console.log('    ✓ saved');
    } catch (e) {
      failed++;
      console.error(`    ✗ ${e.message.split('\n')[0]}`);
      await page.screenshot({ path: path.join(debugDir, shot.name) }).catch(() => {});
    }
  }
  await browser.close();
  console.log(`Done. AI marks used: ${aiMarks}/${cfg.maxAiMarks}. ${failed ? failed + ' shot(s) failed, see screenshots/_debug/' : 'All shots captured.'}`);
  process.exit(failed ? 1 : 0);
}

main();
