import { dbPaths } from '../config/paths.js';
import { pushPath, updatePath, incrementTransaction, serverTimestamp } from './firebaseDb.js';

export async function createOrder(order) {
  const now = Date.now();
  const cleanOrder = {
    ...order,
    status: order.status || 'pending',
    kitchenStatus: order.kitchenStatus || 'new',
    deliveryStatus: order.deliveryStatus || 'waiting',
    pickupStatus: order.pickupStatus || 'waiting',
    createdAt: order.createdAt || now,
    updatedAt: now
  };

  const orderId = await pushPath(dbPaths.orders, cleanOrder);

  if (order.items) {
    await Promise.all(Object.values(order.items).map(item => {
      if (!item.productId || !item.qty) return null;
      return incrementTransaction(`${dbPaths.products}/${item.productId}/stock`, -Math.abs(Number(item.qty)));
    }).filter(Boolean));
  }

  return orderId;
}

export function updateOrderStatus(orderId, patch) {
  return updatePath(`${dbPaths.orders}/${orderId}`, {
    ...patch,
    updatedAt: Date.now()
  });
}
