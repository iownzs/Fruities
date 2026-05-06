export function money(value, currency = '₱') {
  return `${currency}${Number(value || 0).toLocaleString('en-PH', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

export function nowTimestamp() {
  return Date.now();
}

export function orderNumber(n) {
  return `ORD-${String(n).padStart(4, '0')}`;
}
