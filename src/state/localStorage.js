const prefix = 'fruitStoryPOS:';

export function loadLocal(key, fallback = null) {
  try {
    const raw = localStorage.getItem(prefix + key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

export function saveLocal(key, value) {
  localStorage.setItem(prefix + key, JSON.stringify(value));
}

export function removeLocal(key) {
  localStorage.removeItem(prefix + key);
}
