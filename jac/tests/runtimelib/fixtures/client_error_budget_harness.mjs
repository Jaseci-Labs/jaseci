// Drives a client error reporter under a stub window and counts the reports
// that would reach POST /cl/__error__. Prints one JSON line of results.
//
//   node client_error_budget_harness.mjs runtime <client_runtime_core.js>
//   node client_error_budget_harness.mjs inline <early-handler-script.js>
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const [mode, target] = process.argv.slice(2);
const START = 1_700_000_000_000;
const sent = [];
let now = START;
Date.now = () => now;
globalThis.fetch = (url, init) => {
  sent.push({ endpoint: url, ...JSON.parse(init.body) });
  return Promise.resolve({ ok: true });
};

// The stack the jachammer flood carried (jacBuilder#2354).
const EXTENSION_STACK = [
  "TypeError: Cannot read properties of undefined (reading 'M_ID')",
  "    at Y (chrome-extension://eppiocemhmnlbhjplcgkofciiegomcon/executors/200.js:1:761)",
  "    at E (chrome-extension://eppiocemhmnlbhjplcgkofciiegomcon/executors/200.js:1:1442)",
].join("\n");
const FIREFOX_EXTENSION_STACK = [
  "Y@moz-extension://0a1b2c3d/content.js:1:761",
  "E@moz-extension://0a1b2c3d/content.js:1:1442",
].join("\n");
const APP_STACK = "TypeError: boom\n    at render (https://app.test/static/client.js:1:200)";
const MIXED_STACK = [
  "TypeError: boom",
  "    at hook (chrome-extension://abc/inject.js:1:5)",
  "    at render (https://app.test/static/client.js:1:200)",
].join("\n");

function errorWith(message, stack) {
  const err = new Error(message);
  err.stack = stack;
  return err;
}

function rejection(message, stack) {
  const event = new Event("unhandledrejection");
  event.reason = errorWith(message, stack);
  window.dispatchEvent(event);
}

function windowError(message, error, filename) {
  const event = new Event("error");
  Object.assign(event, { message, error, filename });
  window.dispatchEvent(event);
}

let install;
if (mode === "runtime") {
  const core = await import(pathToFileURL(target).href);
  install = () => core.__jacInstallErrorHandlers();
} else if (mode === "inline") {
  const source = readFileSync(target, "utf8");
  install = () => new Function(source)();
} else {
  throw new Error(`unknown mode: ${mode}`);
}

// Each scenario is a fresh page: new window, no handlers, an empty budget.
function scenario(fire) {
  globalThis.window = new EventTarget();
  window.location = { href: "https://app.test/project/p1" };
  delete globalThis.__jacErrorHandlersInstalled;
  delete globalThis.__jacErrorReportBudget;
  now = START;
  sent.length = 0;
  install();
  fire();
  return { sent: sent.length, first: sent[0] ?? null };
}

function times(n, fn) {
  for (let i = 0; i < n; i++) fn(i);
}

const results = {
  extensionRejections: scenario(() =>
    times(1000, () => rejection("Cannot read properties of undefined (reading 'M_ID')", EXTENSION_STACK)),
  ),
  firefoxExtensionRejections: scenario(() =>
    times(1000, () => rejection("x is undefined", FIREFOX_EXTENSION_STACK)),
  ),
  extensionScriptWithoutStack: scenario(() =>
    times(100, () => windowError("Script error.", null, "chrome-extension://abc/content.js")),
  ),
  identicalAppErrors: scenario(() => times(1000, () => rejection("boom", APP_STACK))),
  mixedStack: scenario(() => rejection("boom", MIXED_STACK)),
  appWindowError: scenario(() =>
    windowError("boom", errorWith("boom", APP_STACK), "https://app.test/static/client.js"),
  ),
  distinctAppErrors: scenario(() => times(1000, (i) => rejection(`boom ${i}`, APP_STACK))),
  distinctAppErrorsOverTwoMinutes: scenario(() => {
    times(1000, (i) => rejection(`boom ${i}`, APP_STACK));
    now += 60_000;
    times(1000, (i) => rejection(`later ${i}`, APP_STACK));
  }),
  afterRuntimeHandlersInstalled: scenario(() => {
    window.__jacErrorHandlersInstalled = true;
    times(10, (i) => rejection(`boom ${i}`, APP_STACK));
  }),
};

console.log(JSON.stringify(results));
