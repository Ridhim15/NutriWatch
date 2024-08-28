const CACHE_NAME = "flask-pwa-cache-v1"
const urlsToCache = [
	"/",
	"/static/pwa/manifest.json",
	"/static/pwa/service-worker.js",
	"/static/css/style.css",
	// Add other files as needed
]

self.addEventListener("install", event => {
	event.waitUntil(
		caches.open(CACHE_NAME).then(cache => {
			return cache.addAll(urlsToCache)
		})
	)
})

self.addEventListener("fetch", event => {
	event.respondWith(
		caches.match(event.request).then(response => {
			return response || fetch(event.request)
		})
	)
})

