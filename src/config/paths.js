export const storeId = import.meta.env.VITE_STORE_ID || 'fruit-story-main';

export const dbPaths = {
  root: `stores/${storeId}`,
  settings: `stores/${storeId}/settings`,
  users: `stores/${storeId}/users`,
  roles: `stores/${storeId}/roles`,
  products: `stores/${storeId}/products`,
  orders: `stores/${storeId}/orders`,
  inventoryLogs: `stores/${storeId}/inventoryLogs`,
  billing: `stores/${storeId}/billing`,
  billingPayments: `stores/${storeId}/billingPayments`,
  chatChannels: `stores/${storeId}/chat/channels`,
  chatMessages: `stores/${storeId}/chat/messages`,
  chatReads: `stores/${storeId}/chat/reads`,
  activityLogs: `stores/${storeId}/activityLogs`
};
