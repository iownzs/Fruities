import { initializeApp } from 'firebase/app';
import { getDatabase, ref, onValue } from 'firebase/database';

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

function bootFirebaseSettingsProductsSync() {
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

    console.log('[Fruities Firebase] Settings/products listeners connected');
  } catch (error) {
    console.error('[Fruities Firebase] Boot failed', error);
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootFirebaseSettingsProductsSync);
} else {
  bootFirebaseSettingsProductsSync();
}
