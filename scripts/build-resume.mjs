// Builds resume.pdf from resume.json.
// Usage: node scripts/build-resume.mjs
// Requires Node 18+ and a Chromium-based browser (Chrome or Edge). Set CHROME_PATH to override detection.
import { readFileSync, writeFileSync, existsSync, mkdtempSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const data = JSON.parse(readFileSync(join(root, 'resume.json'), 'utf8'));
const outPdf = join(root, 'resume.pdf');

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const css = `
  @page { size: Letter; margin: 0.45in 0; }
  @page :first { margin: 0 0 0.45in 0; }
  :root { --accent: #0e8a43; --accent-dark: #0a6632; --tint: #dff3e6; --ink: #1a1f24; --muted: #55636c; --rule: #d5dde0; --band: #0b141b; }
  * { box-sizing: border-box; }
  html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body { margin: 0; font-family: Calibri, "Segoe UI", Arial, Helvetica, sans-serif; font-size: 9.7pt; line-height: 1.3; color: var(--ink); }
  a { color: inherit; text-decoration: none; }
  header { display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 0 18px; background: var(--band); color: #fff; border-bottom: 5px solid var(--accent); padding: 0.42in 0.55in 0.2in; }
  main { padding: 6px 0.55in 0; }
  h1 { font-size: 26pt; line-height: 1.05; margin: 0; letter-spacing: -0.01em; }
  .title { font-size: 12pt; color: #6ee7a0; font-weight: 600; margin-top: 3px; }
  .contact { grid-column: 1 / -1; margin-top: 8px; padding-top: 7px; border-top: 1px solid #22323d; display: flex; flex-wrap: wrap; gap: 0 14px; color: #c3d2d9; font-size: 9pt; line-height: 1.5; }
  .contact span { white-space: nowrap; }
  .stats { display: flex; gap: 16px; flex: none; }
  .stat { text-align: center; border-left: 1px solid #2a3a45; padding-left: 16px; }
  .stat:first-child { border-left: 0; padding-left: 0; }
  .stat b { display: block; font-size: 17pt; line-height: 1.1; color: #fff; }
  .stat span { display: block; font-size: 7.5pt; letter-spacing: 0.06em; text-transform: uppercase; color: #9fb2bb; margin-top: 1px; }
  h2 { display: flex; align-items: center; gap: 8px; font-size: 10.5pt; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent-dark); margin: 11px 0 5px; break-after: avoid; }
  h2 .ic { width: 15px; height: 15px; flex: none; fill: none; stroke: var(--accent); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
  h2::after { content: ""; height: 1px; background: var(--rule); flex: 1; }
  p { margin: 0; }
  .summary { font-size: 10.3pt; color: #26313a; }
  .job { position: relative; break-inside: avoid; margin: 0 0 6px 5px; padding-left: 13px; border-left: 2px solid var(--tint); }
  .job::before { content: ""; position: absolute; left: -6.5px; top: 3px; width: 10px; height: 10px; border-radius: 50%; background: var(--accent); border: 2px solid #fff; }
  .proj { break-inside: avoid; margin-bottom: 5px; }
  .row { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }
  .role { font-weight: 700; font-size: 10.8pt; }
  .org { font-weight: 700; color: var(--accent-dark); }
  .dates { color: var(--muted); white-space: nowrap; font-size: 9.3pt; font-weight: 600; }
  .loc { color: var(--muted); font-size: 9.3pt; }
  ul { margin: 2px 0 0; padding-left: 15px; }
  li { margin: 0 0 1px; }
  li::marker { color: var(--accent); }
  .kv { display: grid; grid-template-columns: 138px 1fr; gap: 3px 10px; }
  .kv b { color: var(--accent-dark); font-weight: 700; }
  .result { display: inline-block; background: var(--tint); color: var(--accent-dark); font-weight: 700; font-size: 8.8pt; padding: 0 7px; border-radius: 9px; margin-left: 2px; white-space: nowrap; }
  .proj p { margin-top: 1px; }
  .edu { margin-bottom: 3px; }
`;

const experience = data.experience.map((j) => `
  <div class="job">
    <div class="row"><div><span class="role">${esc(j.role)}</span> <span class="org">| ${esc(j.org)}</span></div><div class="dates">${esc(j.dates)}</div></div>
    <div class="loc">${esc(j.location)}</div>
    <ul>${j.bullets.map((b) => `<li>${esc(b)}</li>`).join('')}</ul>
  </div>`).join('');

const projects = data.projects.map((p) => `
  <div class="proj">
    <div class="row"><div><span class="role">${esc(p.title)}</span> <span class="org">| ${esc(p.client)}</span></div></div>
    <p>${esc(p.text)} <span class="result">${esc(p.result)}</span></p>
  </div>`).join('');

const skills = data.skills.map((s) => `<b>${esc(s.label)}</b><span>${s.items.map(esc).join(', ')}</span>`).join('');
const certs = data.certifications.map((c) => `<b>${esc(c.issuer)}</b><span>${c.items.map(esc).join(', ')}</span>`).join('');
const stats = data.stats.map((t) => `<div class="stat"><b>${esc(t.value)}</b><span>${esc(t.label)}</span></div>`).join('');
const education = data.education.map((e) => `
  <div class="row edu"><div><span class="role">${esc(e.school)}</span> <span class="org">| ${esc(e.degree)}</span></div><div class="dates">${esc(e.dates)}</div></div>`).join('');

const links = data.contact.links.map((l) => `<span><a href="${esc(l.url)}">${esc(l.label)}</a></span>`).join('');

const icons = {
  user: '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
  cpu: '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2M15 20v2M2 15h2M2 9h2M20 15h2M20 9h2M9 2v2M9 20v2"/>',
  building: '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4M10 10h4M10 14h4M10 18h4"/>',
  layers: '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
  award: '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
  cap: '<path d="M22 10 12 5 2 10l10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/><path d="M22 10v6"/>',
};
const h2 = (icon, text) => `<h2><svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">${icons[icon]}</svg>${text}</h2>`;

const html = `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>${esc(data.name)} - Resume</title><style>${css}</style></head>
<body>
  <header>
    <div>
    <h1>${esc(data.name)}</h1>
    <div class="title">${esc(data.title)}</div>
    </div>
    <div class="stats">${stats}</div>
    <div class="contact"><span>${esc(data.contact.location)}</span><span><a href="mailto:${esc(data.contact.email)}">${esc(data.contact.email)}</a></span>${links}</div>
  </header>
  <main>
  ${h2('user', 'Summary')}<p class="summary">${esc(data.summary)}</p>
  ${h2('cpu', 'Skills')}<div class="kv">${skills}</div>
  ${h2('building', 'Experience')}${experience}
  ${h2('layers', 'Selected Projects')}${projects}
  ${h2('award', 'Certifications')}<div class="kv">${certs}</div>
  ${h2('cap', 'Education')}${education}
  </main>
</body></html>`;

const candidates = [
  process.env.CHROME_PATH,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
].filter(Boolean);
const chrome = candidates.find((p) => existsSync(p));
if (!chrome) { console.error('No Chrome/Edge found. Set CHROME_PATH.'); process.exit(1); }

const tmp = mkdtempSync(join(tmpdir(), 'resume-'));
const htmlPath = join(tmp, 'resume.html');
writeFileSync(htmlPath, html);

execFileSync(chrome, [
  '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
  `--user-data-dir=${join(tmp, 'profile')}`,
  `--print-to-pdf=${outPdf}`,
  pathToFileURL(htmlPath).href,
], { stdio: 'ignore', timeout: 60000 });

console.log('Wrote', outPdf);
