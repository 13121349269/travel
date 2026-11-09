/* 全国旅游攻略地图 - Service Worker
   策略：全部预缓存 + cache-first（静态站点，内容随部署更新，缓存名带版本号） */
const CACHE = 'travel-v31';
const PRECACHE = [
  './', './index.html', './map.html', './shanxi.html', './guide.html', './province.html', './taste.html', './free.html', './search.html',
  './data/spots.js', './data/national.json', './data/featured.json', './data/city_map.json', './data/search-index.json',
  './icon-192.png', './icon-512.png', './og-image.png', './manifest.json'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(PRECACHE))
      .then(() => self.skipWaiting())
      .catch(err => console.log('SW precache fail:', err.message))
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  // 高德瓦片不缓存（体积大、时效强），交给浏览器 HTTP 缓存
  if (url.hostname.includes('autonavi')) return;
  const isPage = e.request.mode === 'navigate' || url.pathname.endsWith('.html');
  // HTML：network-first 带 3s 超时兜底 —— 弱网不卡 30s，超时先用缓存、后台继续更新
  if (isPage) {
    e.respondWith((async () => {
      const cache = await caches.open(CACHE);
      try {
        const resp = await Promise.race([
          fetch(e.request).then(r => { if (r.ok) cache.put(e.request, r.clone()); return r; }),
          new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 3000))
        ]);
        // 拿到的仍是 404/5xx 时也回退缓存，避免把错误页展示给用户
        if (resp.ok) return resp;
        const fb = await caches.match(e.request);
        return fb || (await caches.match('./')) || resp;
      } catch (err) {
        const hit = await caches.match(e.request);
        return hit || (await caches.match('./')) || Response.error();
      }
    })());
    return;
  }
  // 其余资源：cache-first
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then(hit => hit ||
      fetch(e.request).then(resp => {
        if (!resp.ok) throw new Error('http ' + resp.status);
        const copy = resp.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return resp;
      }).catch(() => caches.match(e.request, { ignoreSearch: true }).then(hit => hit || Response.error()))
    )
  );
});
