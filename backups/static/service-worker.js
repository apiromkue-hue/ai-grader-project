// Service Worker for AI Grader PWA
// This file enables offline functionality and app-like experience

const CACHE_NAME = 'ai-grader-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/manifest.json',
  '/static/css/main.css',
  '/static/js/app.js'
];

// Install event - cache assets
self.addEventListener('install', (event) => {
  console.log('Service Worker installing...');
  
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Caching assets');
      return cache.addAll(ASSETS_TO_CACHE);
    }).catch((error) => {
      console.warn('Cache installation failed:', error);
    })
  );
  
  self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('Service Worker activating...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  
  self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  const { request } = event;
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip external URLs
  if (!request.url.startsWith(self.location.origin)) {
    return;
  }
  
  event.respondWith(
    caches.match(request).then((response) => {
      if (response) {
        console.log('Serving from cache:', request.url);
        return response;
      }
      
      return fetch(request).then((response) => {
        // Cache successful responses
        if (response && response.status === 200) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseToCache);
          });
        }
        return response;
      }).catch(() => {
        // Fallback for offline
        console.warn('Offline - no cache available for:', request.url);
        // Return a custom offline page if needed
        return new Response('ไม่มีเชื่อมต่ออินเทอร์เน็ต', {
          status: 503,
          statusText: 'Service Unavailable'
        });
      });
    })
  );
});

// Background sync for offline submissions
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-analysis') {
    event.waitUntil(
      // Sync pending analyses when back online
      self.clients.matchAll().then((clients) => {
        clients.forEach((client) => {
          client.postMessage({
            type: 'SYNC_PENDING_ANALYSIS'
          });
        });
      })
    );
  }
});

// Push notifications
self.addEventListener('push', (event) => {
  if (!event.data) {
    console.log('Push received but no data');
    return;
  }
  
  const options = {
    body: event.data.text(),
    icon: '/icon-192x192.png',
    badge: '/badge-72x72.png',
    tag: 'ai-grader-notification',
    requireInteraction: false,
    actions: [
      {
        action: 'open',
        title: 'เปิด'
      },
      {
        action: 'close',
        title: 'ปิด'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('ระบบตรวจโครงงาน AI', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'open') {
    event.waitUntil(
      clients.matchAll({ type: 'window' }).then((clientList) => {
        // Focus or open the app
        for (let i = 0; i < clientList.length; i++) {
          const client = clientList[i];
          if (client.url === '/' && 'focus' in client) {
            return client.focus();
          }
        }
        if (clients.openWindow) {
          return clients.openWindow('/');
        }
      })
    );
  }
});

console.log('Service Worker loaded successfully');
