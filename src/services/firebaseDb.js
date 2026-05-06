import { db } from '../config/firebase.js';
import { ref, get, set, update, push, remove, onValue, serverTimestamp, runTransaction } from 'firebase/database';

export function readPath(path) {
  return get(ref(db, path)).then(snapshot => snapshot.val());
}

export function writePath(path, value) {
  return set(ref(db, path), value);
}

export function updatePath(path, patch) {
  return update(ref(db, path), patch);
}

export function pushPath(path, value) {
  const itemRef = push(ref(db, path));
  return set(itemRef, value).then(() => itemRef.key);
}

export function deletePath(path) {
  return remove(ref(db, path));
}

export function listenPath(path, callback) {
  return onValue(ref(db, path), snapshot => callback(snapshot.val(), snapshot));
}

export function incrementTransaction(path, delta) {
  return runTransaction(ref(db, path), current => (Number(current || 0) + Number(delta || 0)));
}

export { serverTimestamp };
