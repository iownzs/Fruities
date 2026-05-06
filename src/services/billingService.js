import { dbPaths } from '../config/paths.js';
import { updatePath, pushPath } from './firebaseDb.js';

export async function recordBillingPayment({ amount, months, paymentMethod, note, createdBy }) {
  const now = Date.now();
  const paymentId = await pushPath(dbPaths.billingPayments, {
    amount: Number(amount || 0),
    months: Number(months || 1),
    paymentMethod: paymentMethod || 'Manual',
    note: note || '',
    createdBy,
    createdAt: now
  });

  await updatePath(dbPaths.billing, {
    status: 'active',
    posAccessEnabled: true,
    paidMonths: Number(months || 1),
    lastPaymentAt: now,
    updatedBy: createdBy,
    updatedAt: now
  });

  return paymentId;
}
