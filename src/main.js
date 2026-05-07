import { initializeApp } from 'firebase/app';
import { getDatabase, ref, get } from 'firebase/database';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  databaseURL: import.meta.env.VITE_FIREBASE_DATABASE_URL,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};

function hasFirebaseConfig(config) {
  return Boolean(
    config.apiKey &&
    config.authDomain &&
    config.databaseURL &&
    config.projectId &&
    config.appId
  );
}

async function bootFirebaseModule() {
  try {
    if (!hasFirebaseConfig(firebaseConfig)) {
      console.warn('[Fruities Firebase] Missing Firebase env config');
      return;
    }

    const app = initializeApp(firebaseConfig);
    const db = getDatabase(app);

    const snap = await get(ref(db, 'stores/fruit-story-main/settings'));

    window.FruitiesFirebase = {
      app,
      db,
      settings: snap.exists() ? snap.val() : null
    };

    console.log('[Fruities Firebase] Connected', window.FruitiesFirebase.settings);
  } catch (error) {
    console.error('[Fruities Firebase] Connection failed', error);
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootFirebaseModule);
} else {
  bootFirebaseModule();
}
