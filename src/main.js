import { initializeApp } from 'firebase/app';
import { getDatabase, ref, onValue, set, update } from 'firebase/database';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  databaseURL: import.meta.env.VITE_FIREBASE_DATABASE_URL,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};

const STORE_ID = 'fruit-story-main';

function hasFirebaseConfig(config) {
  return Boolean(
    config.apiKey &&
    config.authDomain &&
    config.databaseURL &&
    config.projectId &&
    config.appId
  );
}

function $(id) {
  return document.getElementById(id);
}

function setText(id, value) {
  const el = $(id);
  if (el) el.textContent = value;
}

function setInput(id, value) {
  const el = $(id);
  if (el) el.value = value;
}

function applySettings(settings = {}) {
  const storeName = settings.storeName || 'Fruit Story';
  const currency = settings.currency || '₱';
  const theme = settings.theme || 'light';
  const logoUrl = settings.logoUrl || '';

  window.FruitiesFirebase = window.FruitiesFirebase || {};
  window.FruitiesFirebase.settings = settings;

  // Keep original app state compatible, but do not override app functions.
  window.S = window.S || {};
  window.S.settings = {
    ...(window.S.settings || {}),
    ...settings
  };

  setText('store-name-sidebar', storeName);
  setText('store-name-login', storeName);
  setText('store-name-login-footer', `🍓 ${storeName} POS`);

  setInput('store-name-input', storeName);
  setInput('store-currency', currency);

  document.body.classList.toggle('dark', theme === 'dark');

  const sidebarLogoWrap = $('sidebar-logo-wrap');
  const sidebarLogoImg = $('sidebar-logo-img');
  const sidebarLogoEmoji = $('sidebar-logo-emoji');
  const loginLogoWrap = $('login-logo-wrap');
  const loginLogoImg = $('login-logo-img');

  if (logoUrl) {
    if (sidebarLogoImg) sidebarLogoImg.src = logoUrl;
    if (loginLogoImg) loginLogoImg.src = logoUrl;
    if (sidebarLogoWrap) sidebarLogoWrap.classList.add('has-logo');
    if (loginLogoWrap) loginLogoWrap.classList.add('has-logo');
    if (sidebarLogoEmoji) sidebarLogoEmoji.style.display = 'none';
  }

  console.log('[Fruities Firebase] Settings applied', settings);
}


function normalizeProducts(productsObject = {}) {
  return Object.entries(productsObject || {})
    .filter(([id, product]) => product && typeof product === 'object')
    .map(([id, product]) => ({
      id: product.id !== undefined ? product.id : id,
      e: product.e || product.emoji || '🍎',
      n: product.n || product.name || 'Product',
      cat: product.cat || product.category || 'Others',
      p: Number(product.p !== undefined ? product.p : product.price || 0),
      s: Number(product.s !== undefined ? product.s : product.stock || 0),
      min: Number(product.min !== undefined ? product.min : product.minStock || 5),
      d: product.d || product.description || '',
      img: product.img || product.imageUrl || '',
      active: product.active !== false
    }))
    .filter((product) => product.active !== false);
}

function applyProducts(productsObject = {}) {
  const products = normalizeProducts(productsObject);

  if (!products.length) {
    console.warn('[Fruities Firebase] No Firebase products found; keeping local products');
    return;
  }

  window.S = window.S || {};
  window.S.products = products;

  try {
    localStorage.setItem('fs', JSON.stringify(window.S));
  } catch (error) {
    console.warn('[Fruities Firebase] Failed to cache products locally', error);
  }

  try { if (typeof window.rGrid === 'function') window.rGrid(); } catch (e) {}
  try { if (typeof window.rProds === 'function') window.rProds(); } catch (e) {}
  try { if (typeof window.rPOS === 'function' && window.curV === 'pos') window.rPOS(); } catch (e) {}
  try { if (typeof window.rAdmProds === 'function' && window.curV === 'accounts') window.rAdmProds(); } catch (e) {}
  try { if (typeof window.rDash === 'function' && window.curV === 'dashboard') window.rDash(); } catch (e) {}

  console.log('[Fruities Firebase] Products applied', products.length);
}


function normalizeOrders(ordersObject = {}) {
  return Object.entries(ordersObject || {})
    .filter(([id, order]) => order && typeof order === 'object')
    .map(([id, order]) => ({
      ...order,
      id: order.id || id
    }))
    .sort((a, b) => Number(b.createdAt || 0) - Number(a.createdAt || 0));
}

function applyOrders(ordersObject = {}) {
  const orders = normalizeOrders(ordersObject);

  window.S = window.S || {};
  window.S.orders = orders;

  try {
    localStorage.setItem('fs', JSON.stringify(window.S));
  } catch (error) {
    console.warn('[Fruities Firebase] Failed to cache orders locally', error);
  }

  try { if (typeof window.rOrds === 'function') window.rOrds(); } catch (e) {}
  try { if (typeof window.rDash === 'function') window.rDash(); } catch (e) {}
  try { if (typeof window.rKitchen === 'function') window.rKitchen(); } catch (e) {}
  try { if (typeof window.rDel === 'function') window.rDel(); } catch (e) {}
  try { if (typeof window.rPickup === 'function') window.rPickup(); } catch (e) {}

  console.log('[Fruities Firebase] Orders applied', orders.length);
}

function makeFirebaseOrderId(order = {}) {
  const raw = order.id || order.orderNumber || order.no || order.num || `order_${Date.now()}`;
  return String(raw)
    .replace(/[.#$\[\]\/]/g, '_')
    .replace(/\s+/g, '_');
}

function normalizeOrderForFirebase(order = {}) {
  const now = Date.now();

  return {
    ...order,
    id: order.id || order.orderNumber || order.no || `order_${now}`,
    orderNumber: order.orderNumber || order.no || order.num || order.id || `ORD-${now}`,
    createdAt: order.createdAt || order.created || now,
    updatedAt: now,
    syncedAt: now
  };
}

async function saveOrderToFirebase(order = {}) {
  if (!window.FruitiesFirebase || !window.FruitiesFirebase.db) {
    console.warn('[Fruities Firebase] Database not ready; order saved locally only');
    return;
  }

  const db = window.FruitiesFirebase.db;
  const normalized = normalizeOrderForFirebase(order);
  const orderId = makeFirebaseOrderId(normalized);

  await set(
    ref(db, `stores/${STORE_ID}/orders/${orderId}`),
    normalized
  );

  console.log('[Fruities Firebase] Order synced', orderId);
}

function hookOrderCreation() {
  if (window.__fruitiesOrderHookInstalled) return;
  window.__fruitiesOrderHookInstalled = true;

  function getLatestOrderBefore(countBefore) {
    window.S = window.S || {};
    const orders = Array.isArray(window.S.orders) ? window.S.orders : [];

    if (orders.length <= countBefore) return null;

    return orders[orders.length - 1] || null;
  }

  const originalConfirmPay = window.confirmPay;

  if (typeof originalConfirmPay === 'function') {
    window.confirmPay = function confirmPayFirebaseBridge(...args) {
      window.S = window.S || {};
      const countBefore = Array.isArray(window.S.orders) ? window.S.orders.length : 0;

      const result = originalConfirmPay.apply(this, args);

      setTimeout(() => {
        const latest = getLatestOrderBefore(countBefore);
        if (latest) {
          saveOrderToFirebase(latest).catch((error) => {
            console.error('[Fruities Firebase] Failed to sync order', error);
          });
        }
      }, 250);

      return result;
    };

    console.log('[Fruities Firebase] confirmPay hook installed');
  } else {
    console.warn('[Fruities Firebase] confirmPay not found; order write hook not installed');
  }
}

function bootFirebaseSettingsSync() {
  if (!hasFirebaseConfig(firebaseConfig)) {
    console.warn('[Fruities Firebase] Missing Firebase env config');
    return;
  }

  try {
    const app = initializeApp(firebaseConfig);
    const db = getDatabase(app);

    window.FruitiesFirebase = {
      app,
      db,
      storeId: STORE_ID
    };

    const settingsRef = ref(db, `stores/${STORE_ID}/settings`);
    const productsRef = ref(db, `stores/${STORE_ID}/products`);
    const ordersRef = ref(db, `stores/${STORE_ID}/orders`);

    onValue(settingsRef, (snapshot) => {
      if (!snapshot.exists()) {
        console.warn('[Fruities Firebase] No settings found');
        return;
      }

      applySettings(snapshot.val());
    });

    onValue(productsRef, (snapshot) => {
      if (!snapshot.exists()) {
        console.warn('[Fruities Firebase] No products found');
        return;
      }

      applyProducts(snapshot.val());
    });

    onValue(ordersRef, (snapshot) => {
      if (!snapshot.exists()) {
        console.warn('[Fruities Firebase] No Firebase orders found');
        applyOrders({});
        return;
      }

      applyOrders(snapshot.val());
    });

    setTimeout(hookOrderCreation, 1200);

    console.log('[Fruities Firebase] Settings/products/orders listeners connected');
  } catch (error) {
    console.error('[Fruities Firebase] Boot failed', error);
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootFirebaseSettingsSync);
} else {
  bootFirebaseSettingsSync();
}
