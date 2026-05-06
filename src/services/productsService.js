import { dbPaths } from '../config/paths.js';
import { pushPath, updatePath } from './firebaseDb.js';

export function createProduct(product) {
  const now = Date.now();
  return pushPath(dbPaths.products, {
    ...product,
    active: product.active !== false,
    createdAt: now,
    updatedAt: now
  });
}

export function updateProduct(productId, patch) {
  return updatePath(`${dbPaths.products}/${productId}`, {
    ...patch,
    updatedAt: Date.now()
  });
}
