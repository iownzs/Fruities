export function migrateLocalOrdersToFirebase(localState) {
  // Map the existing single-file POS localStorage state into the Firebase order schema.
  // Wire this to ordersService.createOrder once Firebase Auth and products are active.
  return Object.values(localState?.orders || {}).map(order => ({
    orderNumber: order.orderNumber || order.id,
    customer: order.customer || {},
    items: order.items || {},
    subtotal: Number(order.subtotal || 0),
    discount: Number(order.discount || 0),
    total: Number(order.total || 0),
    payment: order.payment || {},
    orderType: order.orderType || 'walkin',
    priority: order.priority || 'normal',
    status: order.status || 'pending',
    kitchenStatus: order.kitchenStatus || 'new',
    deliveryStatus: order.deliveryStatus || 'waiting',
    pickupStatus: order.pickupStatus || 'waiting',
    notes: order.notes || '',
    createdBy: order.createdBy || null,
    createdAt: order.createdAt || Date.now(),
    updatedAt: order.updatedAt || Date.now()
  }));
}
