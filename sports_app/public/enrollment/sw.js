/* Retire the withdrawn enrollment PWA without touching other Sports workers. */
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(key => key.startsWith("sports-enrollment-shell-")).map(key => caches.delete(key)));
    await self.registration.unregister();
    const clients = await self.clients.matchAll({type:"window", includeUncontrolled:true});
    for (const client of clients) {
      if (new URL(client.url).pathname.startsWith("/assets/sports_app/enrollment/")) await client.navigate("/academy");
    }
  })());
});
