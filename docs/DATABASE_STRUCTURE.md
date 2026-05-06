# Firebase Realtime Database Structure

```txt
stores
  fruit-story-main
    settings
    users
    roles
    products
    orders
    inventoryLogs
    billing
    billingPayments
    chat
      channels
      messages
      reads
    activityLogs
```

## Order status fields

```json
{
  "status": "paid",
  "kitchenStatus": "new",
  "deliveryStatus": "waiting",
  "pickupStatus": "waiting"
}
```

## Status values

```txt
status:
  pending
  paid
  cod
  refunded
  cancelled

kitchenStatus:
  new
  preparing
  ready
  sent_out
  completed

deliveryStatus:
  waiting
  assigned
  out_for_delivery
  delivered
  failed

pickupStatus:
  waiting
  ready
  picked_up
```
