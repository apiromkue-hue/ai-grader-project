// PWA Helper Functions for Streamlit Integration

// Register Service Worker
function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/static/service-worker.js')
        .then((registration) => {
          console.log('✅ Service Worker registered:', registration);
        })
        .catch((error) => {
          console.warn('❌ Service Worker registration failed:', error);
        });
    });
  }
}

// Add to Home Screen Prompt
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  
  // Show install button
  const installButton = document.getElementById('install-app-btn');
  if (installButton) {
    installButton.style.display = 'block';
  }
});

function installApp() {
  if (deferredPrompt) {
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('✅ App installed');
      } else {
        console.log('❌ App installation cancelled');
      }
      deferredPrompt = null;
    });
  }
}

// Detect if app is running in standalone mode (PWA)
function isStandalone() {
  return window.navigator.standalone === true ||
         window.matchMedia('(display-mode: standalone)').matches ||
         document.referrer.includes('android-app://');
}

// Request permission for notifications
function requestNotificationPermission() {
  if ('Notification' in window) {
    if (Notification.permission === 'granted') {
      return Promise.resolve();
    } else if (Notification.permission !== 'denied') {
      return Notification.requestPermission();
    }
  }
  return Promise.reject('Notifications not supported');
}

// Send notification
function sendNotification(title, options = {}) {
  if ('serviceWorker' in navigator && 'Notification' in window) {
    if (Notification.permission === 'granted') {
      navigator.serviceWorker.ready.then((registration) => {
        registration.showNotification(title, options);
      });
    }
  }
}

// Detect online/offline status
window.addEventListener('online', () => {
  console.log('✅ Back online');
  document.body.classList.remove('offline');
  // Trigger sync if available
  if ('serviceWorker' in navigator && 'SyncManager' in window) {
    navigator.serviceWorker.ready.then((registration) => {
      registration.sync.register('sync-analysis');
    });
  }
});

window.addEventListener('offline', () => {
  console.log('❌ Offline');
  document.body.classList.add('offline');
});

// Initialize PWA
function initPWA() {
  console.log('Initializing PWA...');
  
  // Register service worker
  registerServiceWorker();
  
  // Check standalone mode
  if (isStandalone()) {
    console.log('✅ Running in standalone mode');
    document.body.classList.add('pwa-standalone');
  }
  
  // Request notification permission
  requestNotificationPermission().catch(() => {
    console.log('Notifications permission not granted');
  });
  
  console.log('✅ PWA initialized');
}

// Call initialization when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initPWA);
} else {
  initPWA();
}

// Export functions for use in Streamlit
window.PWA = {
  registerServiceWorker,
  installApp,
  isStandalone,
  requestNotificationPermission,
  sendNotification,
  initPWA
};
