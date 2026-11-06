/* Only cache this public app shell. Never cache APIs, forms or payment responses. */
const CACHE = "sports-attendance-shell-v1";
const ROOT = "/assets/sports_app/attendance/";
const STATIC = []; // Replaced at build time with public JS/CSS chunks.
self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll([ROOT + "index.html", ROOT + "icon.svg", ...STATIC])));
});
self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith("sports-attendance-shell-") && key !== CACHE).map(key => caches.delete(key)))));
});
self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== self.location.origin || !url.pathname.startsWith(ROOT)) return;
  const asset = url.pathname.includes("/_next/") || url.pathname.endsWith(".svg");
  if (event.request.mode !== "navigate" && !asset) return;
  event.respondWith(fetch(event.request, {cache: event.request.mode === "navigate" ? "no-cache" : "default"}).then(response => {
    if (response.ok) { const copy = response.clone(); caches.open(CACHE).then(cache => cache.put(event.request, copy)); }
    return response;
  }).catch(async () => (await caches.match(event.request)) || (event.request.mode === "navigate" ? await caches.match(ROOT + "index.html") : Response.error())));
});
