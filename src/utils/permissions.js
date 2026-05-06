export function canAccess(user, roles, feature) {
  if (!user || !user.active) return false;
  const role = roles?.[user.role];
  return Boolean(role?.[feature]);
}
